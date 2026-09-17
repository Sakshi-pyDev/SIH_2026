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

    reports = relationship("Report", back_populates="submitted_by", foreign_keys="Report.submitted_by_id")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, nullable=False)      # Unsafe Act / Unsafe Condition / Near Miss
    location = Column(String, nullable=False)
    department = Column(String, nullable=False)
    report_text = Column(String, nullable=False)

    # Prediction results (filled by /analyze at submission time)
    predicted_label = Column(Integer, nullable=True)     # 0 or 1 (None for Precaution Act reports)
    predicted_probability = Column(Float, nullable=True) # 0.0 - 1.0
    top_factors = Column(String, nullable=True)          # JSON string of SHAP top factors

    # "Open" (default) or "Resolved" - operational workflow state.
    status = Column(String, nullable=False, default="Open")

    # Human-in-the-loop review fields. AI output remains unchanged for auditability.
    review_status = Column(String, nullable=False, default="Pending")
    officer_decision = Column(String, nullable=True)
    officer_final_risk = Column(String, nullable=True)
    officer_feedback = Column(String, nullable=True)
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

    submitted_by_id = Column(Integer, ForeignKey("users.id"))
    submitted_by = relationship("User", back_populates="reports", foreign_keys=[submitted_by_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create tables and add HITL columns to an existing SQLite database."""
    Base.metadata.create_all(bind=engine)

    # create_all() does not alter an existing table. These small migrations
    # preserve the current demo database instead of forcing data deletion.
    from sqlalchemy import inspect, text
    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("reports")}
    migrations = {
        "review_status": "ALTER TABLE reports ADD COLUMN review_status VARCHAR NOT NULL DEFAULT 'Pending'",
        "officer_decision": "ALTER TABLE reports ADD COLUMN officer_decision VARCHAR",
        "officer_final_risk": "ALTER TABLE reports ADD COLUMN officer_final_risk VARCHAR",
        "officer_feedback": "ALTER TABLE reports ADD COLUMN officer_feedback VARCHAR",
        "reviewed_by_id": "ALTER TABLE reports ADD COLUMN reviewed_by_id INTEGER",
        "reviewed_at": "ALTER TABLE reports ADD COLUMN reviewed_at DATETIME",
    }
    with engine.begin() as conn:
        for name, statement in migrations.items():
            if name not in columns:
                conn.execute(text(statement))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
