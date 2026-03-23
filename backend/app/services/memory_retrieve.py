"""Retrieve patient history and compute longitudinal trends."""
import logging
from typing import Optional, List, Dict, Any
from app.schemas.analysis import LongitudinalInsights

logger = logging.getLogger(__name__)

# Maximum historical sessions to retrieve
MAX_HISTORY = 10


def get_patient_history(patient_token: str, limit: int = MAX_HISTORY) -> List[Dict]:
    """Return last N sessions for a patient token, ordered oldest first."""
    from app.db.database import is_enabled, SessionLocal
    if not is_enabled() or not patient_token:
        return []
    try:
        from app.db.models import PatientSession
        from sqlalchemy import desc
        db = SessionLocal()
        try:
            rows = (
                db.query(PatientSession)
                .filter(PatientSession.patient_token == patient_token)
                .order_by(desc(PatientSession.created_at))
                .limit(limit)
                .all()
            )
            # Return oldest-first for trend analysis
            return [r.to_dict() for r in reversed(rows)]
        finally:
            db.close()
    except Exception as e:
        logger.warning(f"CML: retrieve failed: {e}")
        return []


def compute_trend(values: List[Optional[float]]) -> str:
    """Determine trend direction from a series of values."""
    clean = [v for v in values if v is not None]
    if len(clean) < 2:
        return "insufficient_data"
    # Compare first half average vs second half average
    mid = len(clean) // 2
    first_avg = sum(clean[:mid]) / mid
    second_avg = sum(clean[mid:]) / (len(clean) - mid)
    delta = second_avg - first_avg
    threshold = first_avg * 0.03  # 3% change = meaningful
    if delta > threshold:
        return "increasing"
    elif delta < -threshold:
        return "decreasing"
    return "stable"


def build_longitudinal_insights(history: List[Dict], current_exercise: str) -> Optional[LongitudinalInsights]:
    """Build insights from session history."""
    if not history:
        return None

    session_count = len(history)
    knee_trend = [s.get("knee_angle") for s in history]
    hip_trend = [s.get("hip_angle") for s in history]
    risk_history = [s.get("risk_level", "unknown") for s in history]

    knee_direction = compute_trend(knee_trend)
    hip_direction = compute_trend(hip_trend)
    risk_counts = {"low": risk_history.count("low"), "medium": risk_history.count("medium"), "high": risk_history.count("high")}

    # Overall trend: use risk as primary signal
    recent_risk = risk_history[-3:] if len(risk_history) >= 3 else risk_history
    high_count = recent_risk.count("high")
    low_count = recent_risk.count("low")

    if high_count >= 2:
        overall_trend = "worsening"
    elif low_count >= 2:
        overall_trend = "improving"
    elif session_count < 2:
        overall_trend = "insufficient_data"
    else:
        overall_trend = "stable"

    # Key observation
    observation = None
    clean_knee = [v for v in knee_trend if v is not None]
    if len(clean_knee) >= 2:
        delta = clean_knee[-1] - clean_knee[0]
        if abs(delta) > 5:
            direction = "improved" if delta > 0 else "declined"
            observation = f"Knee angle has {direction} by {abs(delta):.1f}° over {session_count} sessions"

    if not observation and session_count >= 2:
        observation = f"Tracking {session_count} sessions — risk profile: {risk_counts['high']} high, {risk_counts['medium']} medium, {risk_counts['low']} low"

    # Trend summary
    trend_parts = []
    if knee_direction == "decreasing":
        trend_parts.append("knee flexion reducing")
    elif knee_direction == "increasing":
        trend_parts.append("knee flexion improving")
    if hip_direction == "decreasing":
        trend_parts.append("hip mobility reducing")

    trend_summary = "; ".join(trend_parts) if trend_parts else f"{session_count} sessions tracked, movement {overall_trend}"

    return LongitudinalInsights(
        session_count=session_count,
        trend=overall_trend,
        trend_summary=trend_summary,
        knee_angle_trend=knee_trend,
        hip_angle_trend=hip_trend,
        risk_history=risk_history,
        key_observation=observation,
    )


def build_history_context(history: List[Dict]) -> str:
    """Build a text block to inject into the LLM prompt."""
    if not history:
        return ""
    lines = ["=== PATIENT HISTORY (longitudinal context) ==="]
    for i, s in enumerate(history, 1):
        risk = s.get("risk_level", "?")
        knee = s.get("knee_angle")
        hip = s.get("hip_angle")
        ex = s.get("exercise_type", "general")
        date = s.get("created_at", "")[:10] if s.get("created_at") else ""
        lines.append(f"Session {i} [{date}] {ex}: knee={knee}° hip={hip}° risk={risk}")
        alerts = s.get("alerts", [])
        if alerts:
            lines.append(f"  Alerts: {'; '.join(a[:60] for a in alerts[:2])}")
    lines.append("Consider this history when generating insights about trajectory and trends.")
    return "\n".join(lines)
