"""
SIH26165 - High-Risk (SIF Precursor) Class-Specific Evaluation
================================================================
Computes precision, recall, F1, confusion matrix, and False Negative Rate
SPECIFICALLY for the SIF-precursor (High-risk) class — not just overall
average metrics.

Usage: python evaluate_metrics.py
Run from the folder where sif_model.pkl, sif_preprocessor.pkl, and
oil_safety_reports_dataset.csv live.
"""

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------
# 1. CONFIG — adjust these if your filenames/column names differ
# ---------------------------------------------------------------
MODEL_PATH = "sif_model.pkl"
PREPROCESSOR_PATH = "sif_preprocessor.pkl"
DATASET_PATH = "oil_safety_reports_dataset.csv"

LABEL_COLUMN = "is_sif_precursor"      # <-- change if your label column has a different name
RANDOM_STATE = 42                   # <-- must match the split used during training
TEST_SIZE = 0.2

# ---------------------------------------------------------------
# 2. LOAD ARTIFACTS
# ---------------------------------------------------------------
print("Loading model, preprocessor, and dataset...")
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
df = pd.read_csv(DATASET_PATH)

if LABEL_COLUMN not in df.columns:
    raise ValueError(
        f"Column '{LABEL_COLUMN}' not found in dataset. "
        f"Available columns: {list(df.columns)}\n"
        f"Update LABEL_COLUMN at the top of this script."
    )

# These columns were excluded during training (to avoid data leakage / they
# are identifiers, not features) — must exclude them here too, or the
# preprocessor produces NaNs on columns it was never fit to handle.
COLUMNS_TO_DROP = ["report_id", "potential_severity", "actual_outcome", "severity_gap"]

X = df.drop(columns=[LABEL_COLUMN] + [c for c in COLUMNS_TO_DROP if c in df.columns])
y = df[LABEL_COLUMN]

# ---------------------------------------------------------------
# 3. REPRODUCE THE SAME TRAIN/TEST SPLIT USED DURING TRAINING
# ---------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# IMPORTANT FIX: preprocessing.py's _encode_categoricals() internally does
# .reset_index(drop=True) on the one-hot columns, but hazard_df/tfidf_df keep
# the ORIGINAL (scattered, post-split) index. pd.concat then aligns by index,
# creating phantom rows + NaNs wherever they don't match. Resetting the index
# here BEFORE calling transform() makes all three pieces agree on 0..N-1.
X_test = X_test.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

print(f"Test set size: {len(X_test)} reports "
      f"({y_test.sum()} SIF-precursor positive, {len(y_test) - y_test.sum()} negative)")

# ---------------------------------------------------------------
# 4. HANDLE MISSING VALUES (diagnostic + fix)
# ---------------------------------------------------------------
null_counts = X_test.isnull().sum()
nulls_found = null_counts[null_counts > 0]
if len(nulls_found) > 0:
    print("\nFound missing values in these columns (filling them in):")
    print(nulls_found)

# Text/categorical columns -> fill with empty string
# Numeric columns -> fill with 0
for col in X_test.columns:
    if X_test[col].dtype == "object":
        X_test[col] = X_test[col].fillna("")
    else:
        X_test[col] = X_test[col].fillna(0)

# ---------------------------------------------------------------
# 5. TRANSFORM + PREDICT
# ---------------------------------------------------------------
X_test_transformed = preprocessor.transform(X_test)

# PATCH: handle NaN regardless of what type preprocessor.transform() returns
# (pandas DataFrame, scipy sparse matrix, or numpy array) — converts
# everything to a clean numeric numpy array before prediction.
import numpy as np
import pandas as pd
from scipy import sparse

if isinstance(X_test_transformed, pd.DataFrame):
    X_test_transformed = X_test_transformed.apply(pd.to_numeric, errors="coerce")
    n_nans = int(X_test_transformed.isna().sum().sum())
    X_test_transformed = X_test_transformed.fillna(0).to_numpy(dtype=float)
elif sparse.issparse(X_test_transformed):
    X_test_transformed = X_test_transformed.astype(float)
    n_nans = int(np.isnan(X_test_transformed.data).sum())
    X_test_transformed.data = np.nan_to_num(X_test_transformed.data, nan=0.0)
else:
    X_test_transformed = np.asarray(X_test_transformed, dtype=float)
    n_nans = int(np.isnan(X_test_transformed).sum())
    X_test_transformed = np.nan_to_num(X_test_transformed, nan=0.0)

if n_nans > 0:
    print(f"\nPatched {n_nans} NaN value(s) in the transformed feature matrix.")

y_pred = model.predict(X_test_transformed)

# ---------------------------------------------------------------
# 5. OVERALL REPORT (for reference)
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("OVERALL CLASSIFICATION REPORT")
print("=" * 60)
print(classification_report(y_test, y_pred, target_names=["Not SIF Precursor", "SIF Precursor (High Risk)"]))

# ---------------------------------------------------------------
# 6. CONFUSION MATRIX
# ---------------------------------------------------------------
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

print("=" * 60)
print("CONFUSION MATRIX (raw counts)")
print("=" * 60)
print(f"                    Predicted: No    Predicted: Yes")
print(f"Actual: No          TN = {tn:<12} FP = {fp}")
print(f"Actual: Yes (SIF)   FN = {fn:<12} TP = {tp}")

# ---------------------------------------------------------------
# 7. THE NUMBERS THAT ACTUALLY MATTER FOR SIH JUDGES
# ---------------------------------------------------------------
precision_high = precision_score(y_test, y_pred, pos_label=1)
recall_high = recall_score(y_test, y_pred, pos_label=1)
f1_high = f1_score(y_test, y_pred, pos_label=1)
false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0.0

print("\n" + "=" * 60)
print("HIGH-RISK (SIF PRECURSOR) CLASS — KEY METRICS")
print("=" * 60)
print(f"Precision (High-risk):       {precision_high:.3f}")
print(f"Recall (High-risk):          {recall_high:.3f}  <-- most important: % of real SIF precursors caught")
print(f"F1 Score (High-risk):        {f1_high:.3f}")
print(f"False Negative Rate:         {false_negative_rate:.3f}  <-- % of real SIF precursors MISSED (dangerous)")
print(f"False Negatives (count):     {fn} out of {fn + tp} actual SIF-precursor reports")
print("=" * 60)

# ---------------------------------------------------------------
# 8. SAVE CONFUSION MATRIX AS AN IMAGE (for your PPT)
# ---------------------------------------------------------------
plt.figure(figsize=(5, 4))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Predicted: No", "Predicted: Yes"],
    yticklabels=["Actual: No", "Actual: Yes (SIF)"]
)
plt.title("Confusion Matrix — SIF Precursor Detection")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
print("\nSaved confusion_matrix.png — drop this straight into your PPT.")
