"""
database.py - SQLite database setup via SQLAlchemy.
Three tables: users (auth + role), reports (submitted safety reports +
prediction results).
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./sif_platform.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # role: "field_worker" | "safety_officer" | "admin"
    role = Column(String, nullable=False, default="field_worker")

    reports = relationship("Report", back_populates="submitted_by")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, nullable=False)      # Unsafe Act / Unsafe Condition / Near Miss
    location = Column(String, nullable=False)
    department = Column(String, nullable=False)
    report_text = Column(String, nullable=False)

    # Prediction results (filled by /analyze at submission time)
    predicted_label = Column(Integer, nullable=True)     # 0 or 1
    predicted_probability = Column(Float, nullable=True) # 0.0 - 1.0
    top_factors = Column(String, nullable=True)          # JSON string of SHAP top factors

    submitted_by_id = Column(Integer, ForeignKey("users.id"))
    submitted_by = relationship("User", back_populates="reports")
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
