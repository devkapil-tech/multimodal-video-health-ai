"""SQLAlchemy ORM models for CML persistent memory."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PatientSession(Base):
    __tablename__ = "patient_sessions"

    id = Column(Integer, primary_key=True, index=True)
    patient_token = Column(String(64), index=True, nullable=False)
    session_id = Column(String(16), unique=True, index=True, nullable=False)
    exercise_type = Column(String(32), default="general")
    knee_angle = Column(Float, nullable=True)
    hip_angle = Column(Float, nullable=True)
    spine_deviation = Column(Float, nullable=True)
    asymmetry_score = Column(Float, nullable=True)
    risk_level = Column(String(16), nullable=False)
    alerts = Column(JSON, default=list)
    ai_summary = Column(Text, nullable=True)
    recommendations = Column(JSON, default=list)
    transcript = Column(Text, nullable=True)
    frames_processed = Column(Integer, default=0)
    duration_sec = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "exercise_type": self.exercise_type,
            "knee_angle": self.knee_angle,
            "hip_angle": self.hip_angle,
            "spine_deviation": self.spine_deviation,
            "asymmetry_score": self.asymmetry_score,
            "risk_level": self.risk_level,
            "alerts": self.alerts or [],
            "ai_summary": self.ai_summary,
            "recommendations": self.recommendations or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
