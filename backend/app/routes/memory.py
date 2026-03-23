"""CML memory API endpoints."""
from fastapi import APIRouter, HTTPException
from app.services.memory_retrieve import get_patient_history, build_longitudinal_insights

router = APIRouter()


@router.get("/memory/{patient_token}/history")
def get_history(patient_token: str, limit: int = 10):
    from app.db.database import is_enabled
    if not is_enabled():
        raise HTTPException(503, "CML not configured — set DATABASE_URL environment variable")
    history = get_patient_history(patient_token, limit=limit)
    insights = build_longitudinal_insights(history, "general")
    return {
        "patient_token": patient_token[:8] + "...",
        "session_count": len(history),
        "sessions": history,
        "insights": insights.dict() if insights else None,
    }


@router.get("/memory/status")
def cml_status():
    from app.db.database import is_enabled
    return {"cml_enabled": is_enabled(), "description": "Clinical Memory Layer status"}
