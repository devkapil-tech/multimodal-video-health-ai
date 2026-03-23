"""Persist analysis results to the CML database."""
import logging
from app.schemas.analysis import AnalysisResult

logger = logging.getLogger(__name__)


def store_session(result: AnalysisResult, patient_token: str) -> bool:
    """Store a session. Returns True if saved, False if CML disabled."""
    from app.db.database import is_enabled, SessionLocal
    if not is_enabled() or not patient_token:
        return False

    try:
        from app.db.models import PatientSession
        bm = result.biomechanics
        record = PatientSession(
            patient_token=patient_token,
            session_id=result.session_id,
            exercise_type=result.exercise_type,
            knee_angle=bm.knee_angle,
            hip_angle=bm.hip_angle,
            spine_deviation=bm.spine_deviation,
            asymmetry_score=bm.asymmetry_score,
            risk_level=bm.risk_level,
            alerts=bm.alerts,
            ai_summary=result.ai_summary,
            recommendations=result.recommendations,
            transcript=result.transcript,
            frames_processed=result.frames_processed,
            duration_sec=result.duration_sec,
        )
        db = SessionLocal()
        try:
            db.add(record)
            db.commit()
            logger.info(f"CML: stored session {result.session_id} for token {patient_token[:8]}...")
            return True
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"CML: store failed: {e}")
        return False
