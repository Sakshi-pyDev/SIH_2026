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


class ReportOut(BaseModel):
    id: int
    report_type: str
    location: str
    department: str
    report_text: str
    predicted_label: Optional[int]
    predicted_probability: Optional[float]
    top_factors: Optional[str]
    created_at: datetime
    submitted_by_username: Optional[str] = None

    class Config:
        from_attributes = True
