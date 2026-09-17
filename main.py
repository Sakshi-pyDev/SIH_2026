"""
main.py - SIH26165 SIF Precursor Detection API

Run locally with:
    uvicorn main:app --reload --port 8000

Then open http://127.0.0.1:8000/docs for interactive Swagger UI to test
every endpoint without needing the frontend.

This version keeps the existing ML + SHAP pipeline and adds a safety-rule
layer for strong SIF precursor patterns that the trained model may score too
low. The existing frontend only knows predicted_probability, so for a
critical precursor the stored probability is raised to the minimum High-risk
threshold (0.70). The original ML probability is preserved inside
top_factors as "ml_probability_raw".
"""

import json
import joblib
import pandas as pd

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import init_db, get_db, User, Report
from schemas import UserCreate, Token, ReportCreate, ReportReview, ReportOut
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_role,
)
from preprocessing import SIFPreprocessor


app = FastAPI(title="SIH26165 - SIF Precursor Detection API")


# Allow the frontend (served from a different origin/file) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Load ML artifacts once at startup ---------------------------------
preprocessor: SIFPreprocessor = SIFPreprocessor.load("sif_preprocessor.pkl")
model = joblib.load("sif_model.pkl")
explainer = joblib.load("sif_explainer.pkl")

with open("suggestion_bank.json", encoding="utf-8") as f:
    SUGGESTION_BANK = json.load(f)


# --- Risk tier bucketing ------------------------------------------------
def risk_tier(probability):
    """
    Bucket a probability (0-1) into High/Medium/Low.

    Precaution Act reports return None because they represent a good safety
    practice rather than a hazard/risk event.
    """
    if probability is None:
        return None

    if probability >= 0.7:
        return "High"
    elif probability >= 0.4:
        return "Medium"
    else:
        return "Low"


# --- Critical SIF precursor rule layer ---------------------------------
def detect_critical_precursor(report_text: str):
    """
    Detect strong, high-consequence precursor patterns.

    This is intentionally a small safety-rule layer on top of the ML model.
    It is not presented as a replacement for the trained classifier.

    Returns:
        list[str]: matched precursor signals.
    """
    text = " ".join((report_text or "").lower().split())
    signals = []

    # Falling / dropped objects, especially from height.
    if (
        ("fell" in text or "falling" in text or "dropped" in text)
        and ("height" in text or "high" in text)
    ):
        signals.append("falling_object_from_height")

    if any(
        phrase in text
        for phrase in (
            "falling object",
            "dropped object",
            "object fell",
            "object falling",
            "dropped from height",
            "fell from height",
            "fell from a height",
            "fell from high",
        )
    ):
        signals.append("falling_or_dropped_object")

    # Equipment failure associated with a physical hazard.
    if any(
        phrase in text
        for phrase in (
            "equipment failure",
            "equipment failed",
            "failed equipment",
            "equipment malfunction",
            "equipment failure caused",
        )
    ):
        signals.append("equipment_failure")

    # High-energy pressure events.
    if any(
        phrase in text
        for phrase in (
            "pressure surge",
            "uncontrolled pressure",
            "high pressure release",
            "pressure release",
            "blowout",
        )
    ):
        signals.append("high_energy_pressure_event")

    # Toxic gas / H2S events.
    if any(
        phrase in text
        for phrase in (
            "h2s",
            "hydrogen sulfide",
            "toxic gas",
            "gas leak",
            "gas leakage",
            "toxic exposure",
        )
    ):
        signals.append("toxic_gas_exposure")

    # Fire/explosion language that indicates an actual event or active hazard.
    # Generic phrases such as "fire extinguisher near the fire station" are
    # deliberately NOT treated as critical.
    if any(
        phrase in text
        for phrase in (
            "explosion",
            "blast occurred",
            "fire broke out",
            "fire broke",
            "fire observed",
            "fire started",
            "active fire",
            "smoke detected",
            "burning equipment",
            "burning gas",
        )
    ):
        signals.append("fire_or_explosion_event")

    # Suspended/heavy load hazards.
    if any(
        phrase in text
        for phrase in (
            "suspended load",
            "heavy suspended load",
            "load dropped",
            "load fell",
            "crane load fell",
            "crane load dropped",
        )
    ):
        signals.append("suspended_load_event")

    # Remove duplicates while preserving order.
    return list(dict.fromkeys(signals))


def apply_safety_override(
    report_text: str,
    ml_probability: float,
    top_factors: list,
):
    """
    Combine the ML output with the critical-precursor safety layer.

    For the current frontend, predicted_probability is the field used to
    display the risk badge. Therefore a critical precursor is represented by
    a final probability of at least 0.70, while the raw ML probability is
    retained in top_factors for transparency.
    """
    matched_signals = detect_critical_precursor(report_text)

    if not matched_signals:
        return ml_probability, top_factors, []

    final_probability = max(float(ml_probability), 0.70)

    # Keep the original ML score visible so the safety override is auditable.
    transparency_factors = [
        {
            "feature": "safety_override: critical_precursor_detected",
            "impact": 1.0,
        },
        {
            "feature": "ml_probability_raw",
            "impact": round(float(ml_probability), 4),
        },
    ]

    combined_factors = transparency_factors + top_factors

    return final_probability, combined_factors[:5], matched_signals


def build_report_out(report, current_user_username=None):
    """
    Builds ReportOut and extracts ml_probability_raw / rule_escalated
    from top_factors JSON (already embedded there by apply_safety_override),
    so the API exposes them as explicit top-level fields instead of
    burying them inside a JSON string.
    """
    out = ReportOut.model_validate(report)
    out.submitted_by_username = (
        current_user_username
        if current_user_username
        else (report.submitted_by.username if report.submitted_by else None)
    )
    out.reviewed_by_username = report.reviewed_by.username if report.reviewed_by else None

    if report.top_factors:
        try:
            factors = json.loads(report.top_factors)
        except (json.JSONDecodeError, TypeError):
            factors = []

        for f in factors:
            if f.get("feature") == "safety_override: critical_precursor_detected":
                out.rule_escalated = True
            if f.get("feature") == "ml_probability_raw":
                out.ml_probability_raw = f.get("impact")

    return out


@app.on_event("startup")
def on_startup():
    init_db()


# --- Auth endpoints ------------------------------------------------------
@app.post("/auth/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_in.username).first()

    if existing:
        raise HTTPException(400, "Username already exists")

    if user_in.role not in ("field_worker", "safety_officer", "admin"):
        raise HTTPException(400, "Invalid role")

    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        {"sub": user.username, "role": user.role}
    )

    return Token(
        access_token=token,
        role=user.role,
    )


@app.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(401, "Incorrect username or password")

    token = create_access_token(
        {"sub": user.username, "role": user.role}
    )

    return Token(
        access_token=token,
        role=user.role,
    )


# --- Core prediction logic ----------------------------------------------
def run_prediction(
    report_type: str,
    location: str,
    department: str,
    report_text: str,
):
    """
    Run the existing ML + SHAP pipeline.

    Precaution Act:
        No risk model is run.

    Other reports:
        ML probability is calculated first.
        Strong SIF precursor rules can then escalate the final risk score.
    """

    # Precaution Act reports log a GOOD safety practice, not a hazard.
    if report_type == "Precaution Act":
        return None, None, []

    row = pd.DataFrame(
        [
            {
                "report_type": report_type,
                "location": location,
                "department": department,
                "report_text": report_text,
                # potential_severity / actual_outcome intentionally NOT used.
                # This avoids data leakage from the training-time schema.
                "potential_severity": "Medium",
                "actual_outcome": "None",
            }
        ]
    )

    X = preprocessor.transform(row)

    pred = int(model.predict(X)[0])
    ml_probability = float(model.predict_proba(X)[0][1])

    # SHAP explanation.
    sv = explainer.shap_values(X)[0]
    top_idx = abs(sv).argsort()[::-1][:5]

    top_factors = [
        {
            "feature": X.columns[i],
            "impact": round(float(sv[i]), 4),
        }
        for i in top_idx
    ]

    # Safety-rule layer.
    final_probability, final_factors, matched_signals = apply_safety_override(
        report_text,
        ml_probability,
        top_factors,
    )

    # If a critical precursor is detected, make the binary prediction
    # consistent with the final High-risk classification.
    if matched_signals:
        pred = 1

    return pred, final_probability, final_factors


# --- Report endpoints ----------------------------------------------------
@app.post("/reports", response_model=ReportOut)
def submit_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("field_worker", "admin")
    ),
):
    """
    Only field workers (and admin, for testing) file ground reports.
    Safety officers monitor the dashboard.
    """

    pred, prob, top_factors = run_prediction(
        report_in.report_type,
        report_in.location,
        report_in.department,
        report_in.report_text,
    )

    report = Report(
        report_type=report_in.report_type,
        location=report_in.location,
        department=report_in.department,
        report_text=report_in.report_text,
        predicted_label=pred,
        predicted_probability=prob,
        top_factors=json.dumps(top_factors),
        status="Open",
        submitted_by_id=current_user.id,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    out = build_report_out(report, current_user.username)

    return out


@app.get("/reports", response_model=list[ReportOut])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    RBAC:
      - field_worker: sees only their OWN submitted reports
      - safety_officer / admin: sees ALL reports
    """

    query = db.query(Report)

    if current_user.role == "field_worker":
        query = query.filter(
            Report.submitted_by_id == current_user.id
        )

    reports = query.order_by(
        Report.created_at.desc()
    ).all()

    result = []

    for r in reports:
        out = build_report_out(r)
        result.append(out)

    return result


@app.get("/reports/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        raise HTTPException(404, "Report not found")

    if (
        current_user.role == "field_worker"
        and report.submitted_by_id != current_user.id
    ):
        raise HTTPException(
            403,
            "Not authorized to view this report",
        )

    out = build_report_out(report)

    return out


@app.patch("/reports/{report_id}/resolve", response_model=ReportOut)
def resolve_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("safety_officer", "admin")
    ),
):
    """Safety officer (or admin) marks a report as Resolved."""

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        raise HTTPException(404, "Report not found")

    report.status = "Resolved"

    db.commit()
    db.refresh(report)

    out = build_report_out(report)

    return out


# --- Human-in-the-loop review --------------------------------------------
@app.patch("/reports/{report_id}/review", response_model=ReportOut)
def review_report(
    report_id: int,
    review_in: ReportReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """
    Record a safety officer's human validation of the AI recommendation.
    The original AI prediction is never overwritten.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(404, "Report not found")

    decision = (review_in.decision or "").strip().lower()
    if decision not in ("confirm", "override", "needs_evidence"):
        raise HTTPException(400, "Use confirm, override, or needs_evidence.")

    if report.report_type == "Precaution Act":
        final_risk = "Precaution Act"
    elif decision == "confirm":
        final_risk = risk_tier(report.predicted_probability)
        if final_risk is None:
            raise HTTPException(400, "This report has no AI risk tier to confirm.")
    elif decision == "override":
        final_risk = (review_in.final_risk or "").strip().title()
        if final_risk not in ("High", "Medium", "Low"):
            raise HTTPException(400, "Override requires final_risk: High, Medium, or Low.")
    else:
        final_risk = None

    report.review_status = {
        "confirm": "Confirmed",
        "override": "Overridden",
        "needs_evidence": "Needs Evidence",
    }[decision]
    report.officer_decision = report.review_status
    report.officer_final_risk = final_risk
    report.officer_feedback = (review_in.feedback or "").strip() or None
    report.reviewed_by_id = current_user.id
    report.reviewed_at = pd.Timestamp.utcnow().to_pydatetime().replace(tzinfo=None)

    db.commit()
    db.refresh(report)
    return build_report_out(report)


@app.get("/reports/feedback/dataset")
def feedback_dataset(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Return human-reviewed reports as labelled feedback for controlled retraining/evaluation."""
    reports = db.query(Report).filter(
        Report.review_status.in_(["Confirmed", "Overridden"]),
        Report.officer_final_risk.isnot(None),
    ).order_by(Report.reviewed_at.asc()).all()

    return {
        "count": len(reports),
        "records": [
            {
                "report_id": r.id,
                "report_type": r.report_type,
                "location": r.location,
                "department": r.department,
                "report_text": r.report_text,
                "ai_probability": r.predicted_probability,
                "ai_risk": risk_tier(r.predicted_probability),
                "ai_rule_escalated": "safety_override: critical_precursor_detected" in (r.top_factors or ""),
                "human_decision": r.officer_decision,
                "human_final_risk": r.officer_final_risk,
                "feedback": r.officer_feedback,
                "reviewed_by": r.reviewed_by.username if r.reviewed_by else None,
                "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None,
            }
            for r in reports
        ],
    }


# --- Officer dashboard analytics ----------------------------------------
@app.get("/reports/analytics/locations")
def analytics_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("safety_officer", "admin")
    ),
):
    """Distinct station/location names for the dashboard filter."""

    rows = db.query(Report.location).distinct().all()

    return {
        "locations": sorted(
            r[0] for r in rows if r[0]
        )
    }


def _bucket_counts(reports):
    counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
        "precaution_act": 0,
    }

    for r in reports:

        if r.report_type == "Precaution Act":
            counts["precaution_act"] += 1
            continue

        tier = risk_tier(r.predicted_probability)

        if tier == "High":
            counts["high"] += 1
        elif tier == "Medium":
            counts["medium"] += 1
        elif tier == "Low":
            counts["low"] += 1

    return counts


@app.get("/reports/analytics/summary")
def analytics_summary(
    location: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("safety_officer", "admin")
    ),
):
    """
    Counts for the dashboard Reports / Resolved cards.

    Optionally filters to one station/location.
    """

    query = db.query(Report)

    if location:
        query = query.filter(
            Report.location == location
        )

    reports = query.all()

    resolved = [
        r for r in reports
        if r.status == "Resolved"
    ]

    return {
        "reports": _bucket_counts(reports),
        "resolved": _bucket_counts(resolved),
    }


@app.get("/reports/analytics/monthly")
def analytics_monthly(
    location: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("safety_officer", "admin")
    ),
):
    """
    Month-by-month High/Medium/Low counts for the trend chart.
    """

    query = db.query(Report)

    if location:
        query = query.filter(
            Report.location == location
        )

    reports = query.all()

    months = {}

    for r in reports:

        if r.report_type == "Precaution Act" or not r.created_at:
            continue

        tier = risk_tier(r.predicted_probability)

        if tier is None:
            continue

        key = r.created_at.strftime("%Y-%m")

        months.setdefault(
            key,
            {
                "high": 0,
                "medium": 0,
                "low": 0,
            },
        )

        months[key][tier.lower()] += 1

    sorted_months = sorted(months.keys())

    return {
        "labels": sorted_months,
        "high": [
            months[m]["high"]
            for m in sorted_months
        ],
        "medium": [
            months[m]["medium"]
            for m in sorted_months
        ],
        "low": [
            months[m]["low"]
            for m in sorted_months
        ],
    }


# --- Admin-only endpoint -------------------------------------------------
@app.get("/admin/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    ),
):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
        }
        for u in users
    ]


# --- Autocomplete suggestions -------------------------------------------
@app.get("/suggest")
def suggest(q: str = ""):
    """
    Autocomplete suggestions for the report-writing textarea.
    """

    q = q.strip().lower()

    if len(q) < 2:
        return {"suggestions": []}

    starts_with = [
        s
        for s in SUGGESTION_BANK
        if s.lower().startswith(q)
    ]

    contains = [
        s
        for s in SUGGESTION_BANK
        if q in s.lower() and s not in starts_with
    ]

    results = (
        starts_with + contains
    )[:8]

    return {"suggestions": results}


# --- Health check --------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "SIH26165 SIF Detection API running",
        "docs": "/docs",
    }
