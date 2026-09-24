# retrain_service.py
#
# Controlled retraining pipeline. Every retrain is a FULL refit (original
# dataset + ALL reviewed feedback so far, not just the newest batch) so the
# model never "forgets" earlier officer feedback.
#
# Comparison method: instead of relying on a separately-saved eval CSV
# (your PRD's 25-report eval number came from 5-fold CV on ~121 reports,
# not a persisted holdout file), each retrain does a fresh stratified
# train/test split of the CURRENT combined dataset. The candidate model is
# trained on the train split; BOTH the current production model and the
# candidate are then scored on the same test split, so the comparison stays
# apples-to-apples even as the dataset grows over time.

import os
import shutil
import joblib
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session

import shap
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score

from database import Report, TrainingRun
from preprocessing import SIFPreprocessor

ORIGINAL_DATASET_PATH = "oil_safety_reports_dataset.csv"
LABEL_COL = "is_sif_precursor"

ACTIVE_MODEL_PATH = "sif_model.pkl"
ACTIVE_PREPROCESSOR_PATH = "sif_preprocessor.pkl"
ACTIVE_EXPLAINER_PATH = "sif_explainer.pkl"
MODEL_ARCHIVE_DIR = "model_versions"   # every past version kept here for rollback/audit

RETRAIN_THRESHOLD = 3          # new reviewed reports needed to unlock the dashboard button
ACCURACY_TOLERANCE = 0.02      # allow up to 2% accuracy drop if recall improves
TEST_SPLIT_SIZE = 0.2          # fraction held out for the fair old-vs-new comparison
RANDOM_STATE = 42

os.makedirs(MODEL_ARCHIVE_DIR, exist_ok=True)


def risk_tier_to_label(review_status: str, officer_final_risk: str, predicted_label: int) -> int:
    """Map an officer's HITL decision to the binary is_sif_precursor ground
    truth used for training.
    ⚠️ VERIFY: this assumes High/Medium == SIF-precursor (label 1) and
    Low == not-a-precursor (label 0) in your original CSV's labeling
    convention. If your dataset's is_sif_precursor was defined differently,
    adjust this mapping before relying on retrain results."""
    if review_status == "Confirmed":
        return predicted_label
    if review_status == "Overridden":
        return 1 if officer_final_risk in ("High", "Medium") else 0
    return predicted_label  # Needs Evidence / Pending should never reach here


def _eligible_reports_query(db: Session):
    return db.query(Report).filter(
        Report.status == "Resolved",
        Report.review_status.in_(["Confirmed", "Overridden"]),
        Report.report_type != "Precaution Act",
    )


def get_retrain_status(db: Session) -> dict:
    """Drives the dashboard's 'Retrain Model' button."""
    eligible_q = _eligible_reports_query(db)
    total_eligible = eligible_q.count()
    new_eligible = eligible_q.filter(Report.used_in_training == False).count()  # noqa: E712

    return {
        "new_eligible_reports": new_eligible,
        "total_labelled_reports": total_eligible,
        "threshold": RETRAIN_THRESHOLD,
        "can_retrain": new_eligible >= RETRAIN_THRESHOLD,
    }


def build_training_dataframe(db: Session) -> pd.DataFrame:
    """Original static dataset + every reviewed report so far, as a single
    DataFrame with columns [report_type, location, department, report_text,
    is_sif_precursor] — the only columns SIFPreprocessor actually reads."""
    base_df = pd.read_csv(ORIGINAL_DATASET_PATH)
    base_df = base_df[["report_type", "location", "department", "report_text", LABEL_COL]]

    reports = _eligible_reports_query(db).all()
    rows = [{
        "report_type": r.report_type,
        "location": r.location,
        "department": r.department,
        "report_text": r.report_text,
        LABEL_COL: risk_tier_to_label(r.review_status, r.officer_final_risk, r.predicted_label),
    } for r in reports]
    feedback_df = pd.DataFrame(rows, columns=base_df.columns)

    combined = pd.concat([base_df, feedback_df], ignore_index=True)
    combined = combined.drop_duplicates(subset=["report_text"], keep="last").reset_index(drop=True)
    return combined


def _score(model, preprocessor: SIFPreprocessor, test_df: pd.DataFrame) -> dict:
    X = preprocessor.transform(test_df)
    y_true = test_df[LABEL_COL]
    y_pred = model.predict(X)
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "recall_high": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
    }


def _build_explainer(model, preprocessor: SIFPreprocessor, train_df: pd.DataFrame):
    """Rebuild the SHAP explainer against the NEW model - reusing the old
    explainer after retraining would attribute the new model's predictions
    using stale coefficients, silently producing wrong SHAP factors.
    ⚠️ Assumes shap.LinearExplainer, matching the Logistic Regression model
    documented in ml-learnings. If your original training script built the
    explainer differently, tell me and I'll match it exactly."""
    X_train = preprocessor.transform(train_df)
    background = shap.sample(X_train, min(100, len(X_train)), random_state=RANDOM_STATE)
    return shap.LinearExplainer(model, background)


def reload_active_model():
    """Called by main.py right after a successful promotion, so /reports
    (POST) picks up the new model without a server restart."""
    new_preprocessor = SIFPreprocessor.load(ACTIVE_PREPROCESSOR_PATH)
    new_model = joblib.load(ACTIVE_MODEL_PATH)
    new_explainer = joblib.load(ACTIVE_EXPLAINER_PATH)
    return new_preprocessor, new_model, new_explainer


def run_retraining(db: Session, triggered_by: str) -> dict:
    status = get_retrain_status(db)
    if not status["can_retrain"]:
        raise ValueError(
            f"Only {status['new_eligible_reports']} new reviewed reports; "
            f"need {RETRAIN_THRESHOLD}."
        )

    old_preprocessor = SIFPreprocessor.load(ACTIVE_PREPROCESSOR_PATH)
    old_model = joblib.load(ACTIVE_MODEL_PATH)

    df = build_training_dataframe(db)
    train_df, test_df = train_test_split(
        df, test_size=TEST_SPLIT_SIZE, stratify=df[LABEL_COL], random_state=RANDOM_STATE
    )
    # train_test_split keeps the original (now-shuffled) index. SIFPreprocessor's
    # _encode_categoricals() does reset_index(drop=True) internally but the
    # hazard/tfidf frames don't -> pd.concat() misaligns rows -> NaN. Reset here
    # so every frame inside fit_transform()/transform() shares a clean 0..n-1 index.
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    # Train candidate model on the train split only
    new_preprocessor = SIFPreprocessor()
    X_train = new_preprocessor.fit_transform(train_df, y=train_df[LABEL_COL])
    new_model = LogisticRegression(class_weight="balanced", max_iter=1000)
    new_model.fit(X_train, train_df[LABEL_COL])

    # Fair comparison: both models scored on the SAME held-out test split
    old_metrics = _score(old_model, old_preprocessor, test_df)
    new_metrics = _score(new_model, new_preprocessor, test_df)

    promote = (
        new_metrics["recall_high"] >= old_metrics["recall_high"]
        and new_metrics["accuracy"] >= old_metrics["accuracy"] - ACCURACY_TOLERANCE
    )

    version = datetime.utcnow().strftime("v%Y%m%d_%H%M%S")
    new_explainer = _build_explainer(new_model, new_preprocessor, train_df)

    # Always archive the candidate for audit/rollback, promoted or not
    joblib.dump(new_model, os.path.join(MODEL_ARCHIVE_DIR, f"sif_model_{version}.pkl"))
    new_preprocessor.save(os.path.join(MODEL_ARCHIVE_DIR, f"sif_preprocessor_{version}.pkl"))
    joblib.dump(new_explainer, os.path.join(MODEL_ARCHIVE_DIR, f"sif_explainer_{version}.pkl"))

    if promote:
        for active, path in [
            (ACTIVE_MODEL_PATH, "sif_model_previous"),
            (ACTIVE_PREPROCESSOR_PATH, "sif_preprocessor_previous"),
            (ACTIVE_EXPLAINER_PATH, "sif_explainer_previous"),
        ]:
            if os.path.exists(active):
                shutil.copy(active, os.path.join(MODEL_ARCHIVE_DIR, f"{path}_before_{version}.pkl"))

        joblib.dump(new_model, ACTIVE_MODEL_PATH)
        new_preprocessor.save(ACTIVE_PREPROCESSOR_PATH)
        joblib.dump(new_explainer, ACTIVE_EXPLAINER_PATH)

    # Mark every eligible report as used (whole dataset was refit this run)
    _eligible_reports_query(db).update({Report.used_in_training: True}, synchronize_session=False)

    db.add(TrainingRun(
        triggered_by=triggered_by,
        reports_included=len(df),
        new_reports_included=status["new_eligible_reports"],
        old_recall_high=old_metrics["recall_high"],
        old_accuracy=old_metrics["accuracy"],
        new_recall_high=new_metrics["recall_high"],
        new_accuracy=new_metrics["accuracy"],
        promoted=promote,
        model_version=version,
        notes="Promoted: recall/accuracy met threshold" if promote
              else "Kept previous model: candidate did not clear threshold",
    ))
    db.commit()

    return {
        "promoted": promote,
        "old_metrics": old_metrics,
        "new_metrics": new_metrics,
        "model_version": version,
        "reports_used": len(df),
    }
