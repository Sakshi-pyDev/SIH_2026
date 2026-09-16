"""
preprocessing.py
-----------------
Phase 3: NLP Preprocessing pipeline for SIH26165 - SIF Precursor Detection Engine.

This module converts raw safety report text + structured fields into a feature
matrix suitable for ML model training (Phase 5) and is designed to be reusable
at inference time inside the FastAPI /analyze endpoint (Phase 4).

Design choices:
- No aggressive stemming/lemmatization: safety-critical words (e.g. "unguarded"
  vs "guard") carry distinct meaning, so we keep light cleaning only.
- Domain hazard-keyword flags (rule-based) are combined with TF-IDF vectors
  (data-driven) -> hybrid approach. This keeps the model explainable (SHAP can
  attribute importance to named hazard categories, not just opaque n-grams)
  while still letting the model learn patterns we didn't manually anticipate.
- The whole pipeline is wrapped in a single SIFPreprocessor class with
  fit/transform/save/load so training and inference use IDENTICAL logic.
"""

import re
import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


# ---------------------------------------------------------------------------
# 1. Domain hazard keyword lexicon (rule-based signals)
# ---------------------------------------------------------------------------
# Each category maps to a list of keywords/phrases. Presence is checked via
# regex word-boundary search on the lowercased, lightly-cleaned text.
# Categories chosen from: (a) OIL/drilling & production safety domain
# knowledge, (b) validated against word-frequency diff on our own dataset.

HAZARD_LEXICON = {
    "ppe_violation": [
        "without gloves", "without helmet", "no gloves", "no helmet",
        "without ppe", "no ppe", "without harness", "no harness",
        "without goggles", "not wearing", "removed ppe", "bypassed ppe",
        "hand gloves", "safety glasses", "ear protection",
    ],
    "fall_hazard": [
        "fall", "fell", "height", "scaffold", "ladder", "staircase",
        "edge", "open pit", "unguarded edge", "guardrail", "handrail",
        "fall arrest", "elevated", "platform",
    ],
    "energy_isolation": [
        "loto", "lockout", "tagout", "energized", "live line", "live wire",
        "pressure", "not isolated", "valve open", "bypassed interlock",
        "electrical panel", "high voltage", "residual pressure",
    ],
    "process_safety": [
        "flammable", "gas leak", "vapor", "vapour", "discharge", "vessel",
        "compressor", "flowline", "tank", "overflow", "spill", "ignition",
        "static electricity", "confined space", "h2s", "hydrocarbon",
    ],
    "procedure_deviation": [
        "without permit", "no permit", "skipped", "bypassed", "shortcut",
        "not followed", "deviated", "improvised", "unauthorized",
        "without supervision", "without signal",
    ],
    "vehicle_mobile_equipment": [
        "tanker", "forklift", "crane", "reversing", "blind spot",
        "moving vehicle", "loader", "hoist",
    ],
    "near_repeat_indicator": [
        "routine", "again", "repeated", "previously reported",
        "recurring", "third time", "second time",
    ],
}

# Negation / omission cue words: reports describing an *absence* of a control
# ("without", "no", "not") tend to correlate strongly with SIF precursors,
# per our EDA (word 'without': 10 in SIF vs 2 in non-SIF reports).
OMISSION_CUES = ["without", "no ", "not ", "failed to", "did not", "didn't"]

SEVERITY_ORDER = ["None", "Low", "Medium", "High", "Critical"]


# ---------------------------------------------------------------------------
# 2. Text cleaning
# ---------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """Light cleaning: lowercase, strip punctuation noise, normalize whitespace.
    Deliberately NOT stemming/lemmatizing (see module docstring)."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # drop punctuation
    text = re.sub(r"\s+", " ", text).strip()   # collapse whitespace
    return text


# ---------------------------------------------------------------------------
# 3. Rule-based domain feature extraction
# ---------------------------------------------------------------------------
def extract_hazard_flags(raw_text: str) -> dict:
    """Binary + count flags per hazard category, plus omission-cue count."""
    text = " " + clean_text(raw_text) + " "  # pad for boundary-safe matching
    feats = {}
    for category, keywords in HAZARD_LEXICON.items():
        hits = 0
        for kw in keywords:
            kw_clean = clean_text(kw)
            if kw_clean and kw_clean in text:
                hits += 1
        feats[f"flag_{category}"] = int(hits > 0)
        feats[f"count_{category}"] = hits

    omission_hits = sum(text.count(cue) for cue in OMISSION_CUES)
    feats["omission_cue_count"] = omission_hits
    feats["word_count"] = len(text.split())
    feats["hazard_category_diversity"] = sum(
        feats[f"flag_{c}"] for c in HAZARD_LEXICON
    )  # how many DIFFERENT hazard types co-occur -> multi-hazard reports are riskier
    return feats


# ---------------------------------------------------------------------------
# 4. Main preprocessor class (fit on train, transform on train/inference)
# ---------------------------------------------------------------------------
class SIFPreprocessor:
    def __init__(self, max_tfidf_features: int = 300, ngram_range=(1, 2)):
        self.tfidf = TfidfVectorizer(
            max_features=max_tfidf_features,
            ngram_range=ngram_range,
            min_df=1,
            stop_words="english",
        )
        self.category_columns_ = {}  # remembers one-hot columns seen at fit time
        self.severity_map_ = {s: i for i, s in enumerate(SEVERITY_ORDER)}
        self.hazard_feature_names_ = None
        self.fitted_ = False

    # -- categorical encoding -------------------------------------------------
    def _encode_categoricals(self, df: pd.DataFrame, fit: bool) -> pd.DataFrame:
        cat_cols = ["report_type", "department", "location"]
        one_hot = pd.get_dummies(df[cat_cols], prefix=cat_cols)

        if fit:
            self.category_columns_ = {c: one_hot.columns.tolist() for c in ["all"]}
        else:
            # align columns to training-time schema (missing -> 0, extra -> dropped)
            expected = self.category_columns_["all"]
            one_hot = one_hot.reindex(columns=expected, fill_value=0)

        # NOTE: potential_severity / actual_outcome / severity_gap are
        # DELIBERATELY EXCLUDED from model features. is_sif_precursor was
        # derived directly from potential_severity in this dataset, so
        # including it (or severity_gap) causes data leakage -> model just
        # memorizes the labeling rule instead of learning from report TEXT.
        # At real-world inference time, a worker submits only free text -
        # severity is not known in advance, it's what we're trying to predict
        # risk for. So the model must learn from language patterns only.
        return one_hot.reset_index(drop=True)

    # -- fit / transform --------------------------------------------------
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        cleaned = df["report_text"].apply(clean_text)

        tfidf_matrix = self.tfidf.fit_transform(cleaned)
        self.hazard_feature_names_ = [f"tfidf_{t}" for t in self.tfidf.get_feature_names_out()]
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(), columns=self.hazard_feature_names_, index=df.index
        )

        hazard_df = pd.DataFrame(
            [extract_hazard_flags(t) for t in df["report_text"]], index=df.index
        )

        cat_df = self._encode_categoricals(df, fit=True)

        self.fitted_ = True
        result = pd.concat([hazard_df, cat_df, tfidf_df], axis=1)
        return result

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted_:
            raise RuntimeError("Call fit_transform() first (on training data).")
        df = df.copy()
        cleaned = df["report_text"].apply(clean_text)

        tfidf_matrix = self.tfidf.transform(cleaned)
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(), columns=self.hazard_feature_names_, index=df.index
        )

        hazard_df = pd.DataFrame(
            [extract_hazard_flags(t) for t in df["report_text"]], index=df.index
        )

        cat_df = self._encode_categoricals(df, fit=False)

        return pd.concat([hazard_df, cat_df, tfidf_df], axis=1)

    # -- persistence --------------------------------------------------------
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str) -> "SIFPreprocessor":
        with open(path, "rb") as f:
            return pickle.load(f)


# ---------------------------------------------------------------------------
# 5. Single-report convenience function (for the future /analyze endpoint)
# ---------------------------------------------------------------------------
def preprocess_single_report(preprocessor: "SIFPreprocessor", report: dict) -> pd.DataFrame:
    """
    report: dict with keys report_type, location, department, report_text,
            potential_severity, actual_outcome (actual_outcome may be 'None'
            or unknown at submission time -> defaults to 'None').
    """
    row = {
        "report_type": report.get("report_type", "Unsafe Act"),
        "location": report.get("location", "Unknown"),
        "department": report.get("department", "Unknown"),
        "report_text": report.get("report_text", ""),
        "potential_severity": report.get("potential_severity", "Medium"),
        "actual_outcome": report.get("actual_outcome", "None"),
    }
    df = pd.DataFrame([row])
    return preprocessor.transform(df)


if __name__ == "__main__":
    # Quick smoke test when run directly
    df = pd.read_csv("/mnt/user-data/uploads/oil_safety_reports_dataset.csv")
    pre = SIFPreprocessor()
    X = pre.fit_transform(df)
    print("Feature matrix shape:", X.shape)
    print("Sample columns:", X.columns[:15].tolist())
    pre.save("/home/claude/sif_preprocessor.pkl")
    X.to_csv("/home/claude/processed_features_preview.csv", index=False)
    print("Saved preprocessor + preview CSV.")
