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
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import init_db, get_db, User, Report
from schemas import UserCreate, Token, ReportCreate, ReportOut, ReportReview, AdminCreateUser, AdminCreateUserOut
from auth import hash_password, verify_password, create_access_token, get_current_user, require_role
from preprocessing import SIFPreprocessor
import retrain_service

app = FastAPI(title="SIH26165 - SIF Precursor Detection API")

# Allow the frontend (served from a different origin/file) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load ML artifacts once at startup ---------------------------------
# NOTE: these are plain module-level globals (not app.state) so that
# retrain_service.reload_active_model() can reassign them in place after
# a successful retrain, without needing a server restart.
preprocessor: SIFPreprocessor = SIFPreprocessor.load("sif_preprocessor.pkl")
model = joblib.load("sif_model.pkl")
explainer = joblib.load("sif_explainer.pkl")

with open("suggestion_bank.json") as f:
    SUGGESTION_BANK = json.load(f)


# --- Risk tier bucketing (for dashboard High/Medium/Low counts) ----------
def risk_tier(probability):
    """Bucket a predicted_probability (0-1) into High/Medium/Low.
    Returns None if probability is None (e.g. Precaution Act reports,
    which are never run through the risk model)."""
    if probability is None:
        return None
    if probability >= 0.7:
        return "High"
    elif probability >= 0.4:
        return "Medium"
    else:
        return "Low"


def to_report_out(report: Report) -> ReportOut:
    """Single place that builds a ReportOut from a Report row, so
    submitted_by_username AND reviewed_by_username are always populated
    consistently (previously reviewed_by_username was never set anywhere,
    even though app.js and ReportOut both expect it)."""
    out = ReportOut.model_validate(report)
    out.submitted_by_username = report.submitted_by.username if report.submitted_by else None
    out.reviewed_by_username = report.reviewed_by.username if report.reviewed_by else None
    return out


# --- Employee code generation (admin-created accounts) --------------------
ROLE_CODE_PREFIX = {"field_worker": "FW", "safety_officer": "SO", "admin": "AD"}


def generate_employee_code(db: Session, role: str) -> str:
    """e.g. FW260007 = Field Worker, year '26, sequence 0007.
    This code becomes the user's username/login id - like a school
    admission number. Sequence is per-role so each role has its own
    numbering; collisions (e.g. after a deletion) are handled by
    incrementing until a free code is found."""
    prefix = ROLE_CODE_PREFIX.get(role, "US")
    year = datetime.utcnow().strftime("%y")
    seq = db.query(User).filter(User.role == role).count() + 1
    code = f"{prefix}{year}{seq:04d}"
    while db.query(User).filter(User.username == code).first():
        seq += 1
        code = f"{prefix}{year}{seq:04d}"
    return code


@app.on_event("startup")
def on_startup():
    init_db()


# --- Auth endpoints ------------------------------------------------------
@app.post("/auth/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    SECURITY: this is a ONE-TIME bootstrap endpoint, not open self-signup.
    It only ever succeeds to create the very FIRST admin account - the
    moment any admin exists in the system, this endpoint locks itself out
    for everyone (admin included). After that, every field_worker /
    safety_officer / additional admin account MUST be created by an
    already-logged-in admin via POST /admin/users, which issues them a
    unique employee code (see generate_employee_code). This is what stops
    random people from self-registering as a worker or officer.
    """
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    admin_exists = db.query(User).filter(User.role == "admin").first() is not None
    if admin_exists:
        raise HTTPException(
            403,
            "Self-registration is disabled. Ask your organization's admin to create your account."
        )
    if user_in.role != "admin":
        raise HTTPException(
            403,
            "Only the first admin account can self-register here. "
            "Field workers and safety officers must be added by an admin from the Admin Console."
        )

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
    # Precaution Act reports log a GOOD safety practice, not a hazard -
    # they're never run through the SIF risk model. No risk label/probability.
    if report_type == "Precaution Act":
        return None, None, []

    row = pd.DataFrame([{
        "report_type": report_type,
        "location": location,
        "department": department,
        "report_text": report_text,
        # potential_severity / actual_outcome intentionally NOT used -
        # see preprocessing.py note on data leakage. SIFPreprocessor.transform()
        # doesn't even read these columns, they're kept here only because
        # preprocess_single_report()'s dict shape expects the keys to exist.
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

    return to_report_out(report)


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
    return [to_report_out(r) for r in reports]


# --- Controlled model retraining (HITL feedback -> candidate model) --------
# NOTE: these two MUST be declared before /reports/{report_id} below.
# FastAPI matches routes in declaration order, and /reports/{report_id}
# would otherwise swallow "/reports/retrain-status" too, trying (and
# failing) to parse "retrain-status" as an integer report_id -> 422 error.
@app.get("/reports/retrain-status")
def retrain_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """Drives the dashboard's 'Retrain Model' button: how many newly
    reviewed reports are waiting to be folded into training."""
    return retrain_service.get_retrain_status(db)


@app.post("/reports/retrain")
def trigger_retrain(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """Full controlled retrain: combine original dataset + all reviewed
    feedback, train a candidate model, evaluate it against the current
    production model on a held-out split, and auto-promote only if it's
    at least as good (see retrain_service.RETRAIN_THRESHOLD/ACCURACY_TOLERANCE)."""
    global preprocessor, model, explainer
    try:
        result = retrain_service.run_retraining(db, triggered_by=current_user.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if result["promoted"]:
        preprocessor, model, explainer = retrain_service.reload_active_model()
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

    return to_report_out(report)


# --- HITL Safety Review (Validate AI: Confirm / Override / Needs Evidence) --
@app.patch("/reports/{report_id}/review", response_model=ReportOut)
def review_report(
    report_id: int,
    review_in: ReportReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """
    Officer records the human decision on the AI recommendation.
      - confirm: officer agrees with the AI's own predicted risk tier
      - override: officer sets a different final risk (final_risk required)
      - needs_evidence: not finalized yet, report stays in the active queue
    review_status/officer_final_risk here are what retrain_service later
    treats as ground-truth labels for controlled retraining - see
    /reports/retrain-status and /reports/retrain.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(404, "Report not found")
    if report.report_type == "Precaution Act":
        raise HTTPException(400, "Precaution Act reports are not risk-reviewed")

    decision = review_in.decision
    if decision not in ("confirm", "override", "needs_evidence"):
        raise HTTPException(400, "decision must be one of: confirm, override, needs_evidence")

    if decision == "confirm":
        report.review_status = "Confirmed"
        report.officer_final_risk = risk_tier(report.predicted_probability)
    elif decision == "override":
        if review_in.final_risk not in ("High", "Medium", "Low"):
            raise HTTPException(400, "final_risk (High/Medium/Low) is required for an override")
        report.review_status = "Overridden"
        report.officer_final_risk = review_in.final_risk
    else:  # needs_evidence
        report.review_status = "Needs Evidence"
        report.officer_final_risk = None

    report.officer_decision = decision
    report.officer_feedback = review_in.feedback
    report.reviewed_by_id = current_user.id
    report.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(report)

    return to_report_out(report)


@app.patch("/reports/{report_id}/resolve", response_model=ReportOut)
def resolve_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """Safety officer (or admin) marks a report as Resolved."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(404, "Report not found")

    report.status = "Resolved"
    db.commit()
    db.refresh(report)

    return to_report_out(report)


# --- Officer dashboard analytics -------------------------------------------
@app.get("/reports/analytics/locations")
def analytics_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """Distinct station/location names, for the dashboard's station filter."""
    rows = db.query(Report.location).distinct().all()
    return {"locations": sorted(r[0] for r in rows if r[0])}


def _bucket_counts(reports):
    counts = {"high": 0, "medium": 0, "low": 0, "precaution_act": 0}
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
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """
    Counts for the dashboard's Reports / Resolved cards, each broken into
    High Risk / Medium / Low / Precaution Act. Optionally filtered to one
    station (location) for station-level comparison.
    """
    query = db.query(Report)
    if location:
        query = query.filter(Report.location == location)
    reports = query.all()
    resolved = [r for r in reports if r.status == "Resolved"]
    pending = [r for r in reports if r.status != "Resolved"]

    return {
        "total": _bucket_counts(reports),
        "pending": _bucket_counts(pending),
        "resolved": _bucket_counts(resolved),
        "reports": _bucket_counts(reports),
    }


@app.get("/reports/analytics/monthly")
def analytics_monthly(
    location: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("safety_officer", "admin")),
):
    """
    Month-by-month High/Medium/Low counts, for the 'Improvement in Station'
    trend chart. A falling High/Medium trend over months = improvement.
    """
    query = db.query(Report)
    if location:
        query = query.filter(Report.location == location)
    reports = query.all()

    months = {}
    for r in reports:
        if r.report_type == "Precaution Act" or not r.created_at:
            continue
        tier = risk_tier(r.predicted_probability)
        if tier is None:
            continue
        key = r.created_at.strftime("%Y-%m")
        months.setdefault(key, {"high": 0, "medium": 0, "low": 0})
        months[key][tier.lower()] += 1

    sorted_months = sorted(months.keys())
    return {
        "labels": sorted_months,
        "high": [months[m]["high"] for m in sorted_months],
        "medium": [months[m]["medium"] for m in sorted_months],
        "low": [months[m]["low"] for m in sorted_months],
    }


@app.get("/reports/feedback/dataset")
def feedback_dataset(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """Admin-restricted export of human-reviewed reports as labelled
    feedback, for offline evaluation/inspection (separate from the
    automatic /reports/retrain pipeline)."""
    reports = db.query(Report).filter(
        Report.status == "Resolved",
        Report.review_status.in_(["Confirmed", "Overridden"]),
    ).all()
    return [to_report_out(r) for r in reports]


# --- Admin-only example endpoint ------------------------------------------
@app.get("/admin/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    users = db.query(User).all()
    return [
        {"id": u.id, "username": u.username, "full_name": u.full_name, "phone_number": u.phone_number, "role": u.role}
        for u in users
    ]


@app.post("/admin/users", response_model=AdminCreateUserOut)
def admin_create_user(
    user_in: AdminCreateUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """
    Onboard a new field_worker / safety_officer / admin. The admin supplies
    the person's real name, role, and an initial password - the system
    generates a unique employee code (e.g. FW260007) as their login username.
    This code is only shown here, once - the admin is responsible for
    handing it to the worker/officer (write it down, print it, etc.).
    """
    if user_in.role not in ("field_worker", "safety_officer", "admin"):
        raise HTTPException(400, "Invalid role")
    if len(user_in.password) < 4:
        raise HTTPException(400, "Password must be at least 4 characters")
    if not user_in.full_name.strip():
        raise HTTPException(400, "Full name is required")

    code = generate_employee_code(db, user_in.role)
    user = User(
        username=code,
        full_name=user_in.full_name.strip(),
        phone_number=(user_in.phone_number or "").strip() or None,
        hashed_password=hash_password(user_in.password),
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return AdminCreateUserOut(
        id=user.id, username=user.username, full_name=user.full_name,
        phone_number=user.phone_number, role=user.role,
    )


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
