# SIH26165 - SIF Precursor Detection API

## Setup (VS Code / local)
```
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Then open http://127.0.0.1:8000/docs for interactive API testing (Swagger UI).

## Files
- main.py           -> FastAPI app, all endpoints
- auth.py           -> JWT + password hashing + RBAC dependency
- database.py       -> SQLAlchemy models (User, Report) + SQLite setup
- schemas.py        -> Pydantic request/response models
- preprocessing.py  -> Phase 3 NLP pipeline (imported, not re-run)
- sif_model.pkl, sif_preprocessor.pkl, sif_explainer.pkl -> trained artifacts

## Roles
- field_worker    : can submit reports, sees only own reports
- safety_officer  : sees ALL reports (dashboard)
- admin           : sees ALL reports + /admin/users endpoint

## Key endpoints
- POST /auth/register  {username, password, role}
- POST /auth/login     (form data: username, password) -> JWT token
- POST /reports        (auth required) -> submits + auto-predicts
- GET  /reports         (auth required) -> RBAC-filtered list
- GET  /reports/{id}
- GET  /admin/users    (admin only)
