from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "field_worker"  # field_worker | safety_officer | admin


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class ReportCreate(BaseModel):
    report_type: str
    location: str
    department: str
    report_text: str


class ReportReview(BaseModel):
    """Safety officer human validation of an AI recommendation."""
    decision: str  # confirm | override | needs_evidence
    final_risk: Optional[str] = None
    feedback: Optional[str] = None


class ReportOut(BaseModel):
    id: int
    report_type: str
    location: str
    department: str
    report_text: str
    predicted_label: Optional[int]
    predicted_probability: Optional[float]
    top_factors: Optional[str]
    status: str = "Open"
    created_at: datetime
    submitted_by_username: Optional[str] = None
    ml_probability_raw: Optional[float] = None
    rule_escalated: bool = False
    review_status: str = "Pending"
    officer_decision: Optional[str] = None
    officer_final_risk: Optional[str] = None
    officer_feedback: Optional[str] = None
    reviewed_by_username: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
