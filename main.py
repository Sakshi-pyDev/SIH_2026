"""
main.py - SIH26165 SIF Precursor Detection API

Run locally with:
    uvicorn main:app --reload --port 8000

Then open http://127.0.0.1:8000/docs for interactive Swagger UI to test
every endpoint without needing the frontend.
"""

import json
import joblib
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import init_db, get_db, User, Report
from schemas import UserCreate, Token, ReportCreate, ReportOut
from auth import hash_password, verify_password, create_access_token, get_current_user, require_role
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

with open("suggestion_bank.json") as f:
    SUGGESTION_BANK = json.load(f)


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

    token = create_access_token({"sub": user.username, "role": user.role})
    return Token(access_token=token, role=user.role)


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")

    token = create_access_token({"sub": user.username, "role": user.role})
    return Token(access_token=token, role=user.role)


# --- Core prediction logic (used by /reports submission) -----------------
def run_prediction(report_type: str, location: str, department: str, report_text: str):
    row = pd.DataFrame([{
        "report_type": report_type,
        "location": location,
        "department": department,
        "report_text": report_text,
        # potential_severity / actual_outcome intentionally NOT used -
        # see preprocessing.py note on data leakage.
        "potential_severity": "Medium",
        "actual_outcome": "None",
    }])
    X = preprocessor.transform(row)
    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])

    sv = explainer.shap_values(X)[0]
    top_idx = abs(sv).argsort()[::-1][:5]
    top_factors = [
        {"feature": X.columns[i], "impact": round(float(sv[i]), 4)}
        for i in top_idx
    ]
    return pred, prob, top_factors


# --- Report endpoints ------------------------------------------------------
@app.post("/reports", response_model=ReportOut)
def submit_report(
    report_in: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("field_worker", "admin")),
):
    """Only field workers (and admin, for testing) file ground reports.
    Safety officers only monitor the dashboard - see GET /reports."""
    pred, prob, top_factors = run_prediction(
        report_in.report_type, report_in.location, report_in.department, report_in.report_text
    )

    report = Report(
        report_type=report_in.report_type,
        location=report_in.location,
        department=report_in.department,
        report_text=report_in.report_text,
        predicted_label=pred,
        predicted_probability=prob,
        top_factors=json.dumps(top_factors),
        submitted_by_id=current_user.id,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    out = ReportOut.model_validate(report)
    out.submitted_by_username = current_user.username
    return out


@app.get("/reports", response_model=list[ReportOut])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    RBAC:
      - field_worker: sees only their OWN submitted reports
      - safety_officer / admin: sees ALL reports (dashboard view)
    """
    query = db.query(Report)
    if current_user.role == "field_worker":
        query = query.filter(Report.submitted_by_id == current_user.id)

    reports = query.order_by(Report.created_at.desc()).all()
    result = []
    for r in reports:
        out = ReportOut.model_validate(r)
        out.submitted_by_username = r.submitted_by.username if r.submitted_by else None
        result.append(out)
    return result


@app.get("/reports/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(404, "Report not found")
    if current_user.role == "field_worker" and report.submitted_by_id != current_user.id:
        raise HTTPException(403, "Not authorized to view this report")

    out = ReportOut.model_validate(report)
    out.submitted_by_username = report.submitted_by.username if report.submitted_by else None
    return out


# --- Admin-only example endpoint ------------------------------------------
@app.get("/admin/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    users = db.query(User).all()
    return [{"id": u.id, "username": u.username, "role": u.role} for u in users]


@app.get("/suggest")
def suggest(q: str = ""):
    """
    Autocomplete suggestions for the report-writing textarea, like Google
    search suggestions. Matches against a bank of hazard-keyword phrases +
    real hazard-related clauses pulled from the training dataset.
    No auth required - it's just writing assistance, not sensitive data.
    """
    q = q.strip().lower()
    if len(q) < 2:
        return {"suggestions": []}

    starts_with = [s for s in SUGGESTION_BANK if s.lower().startswith(q)]
    contains = [s for s in SUGGESTION_BANK if q in s.lower() and s not in starts_with]

    results = (starts_with + contains)[:8]
    return {"suggestions": results}


@app.get("/")
def root():
    return {"status": "SIH26165 SIF Detection API running", "docs": "/docs"}
