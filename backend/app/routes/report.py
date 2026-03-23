"""PDF and FHIR report endpoints, plus side-by-side comparison."""
import os
import uuid
import shutil
from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import Response
from app.schemas.analysis import AnalysisResult
from app.services.video import extract_frames
from app.services.pose import analyze_pose
from app.services.biomechanics import analyze_biomechanics
from app.services.audio import transcribe
from app.services.reasoning import generate_insights
from app.services.pdf_report import generate_pdf_report
from app.services.fhir import build_fhir_report
from app.core.config import settings

router = APIRouter()

# In-memory session store (replace with DB in production)
_sessions: dict = {}


def _store_result(result: AnalysisResult):
    _sessions[result.session_id] = result


def store_result(result: AnalysisResult):
    _store_result(result)


@router.get("/report/{session_id}/pdf")
async def download_pdf(session_id: str):
    result = _sessions.get(session_id)
    if not result:
        raise HTTPException(404, "Session not found. Upload a video first.")
    pdf_bytes = generate_pdf_report(result)
    media_type = "application/pdf" if pdf_bytes[:4] == b"%PDF" else "text/plain"
    return Response(
        content=pdf_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="report-{session_id}.pdf"'},
    )


@router.get("/report/{session_id}/fhir")
async def download_fhir(session_id: str):
    result = _sessions.get(session_id)
    if not result:
        raise HTTPException(404, "Session not found.")
    fhir = build_fhir_report(result)
    import json
    return Response(
        content=json.dumps(fhir, indent=2),
        media_type="application/fhir+json",
        headers={"Content-Disposition": f'attachment; filename="fhir-{session_id}.json"'},
    )


ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


async def _run_pipeline(file: UploadFile, exercise_type: str = "general") -> AnalysisResult:
    from app.services.exercise_library import get_exercise
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported format.")
    session_id = str(uuid.uuid4())[:8]
    os.makedirs(settings.data_dir, exist_ok=True)
    video_path = f"{settings.data_dir}/{session_id}{ext}"
    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    frame_paths, duration = extract_frames(video_path, session_id)
    pose_results = []
    for i, fp in enumerate(frame_paths):
        timestamp = i / max(settings.frame_rate, 1)
        pose_results.append(analyze_pose(fp, frame_index=i, timestamp=timestamp))
    biomechanics = analyze_biomechanics(pose_results, exercise_type=exercise_type)
    transcript = transcribe(video_path, session_id)
    summary, recommendations = generate_insights(biomechanics, transcript)
    return AnalysisResult(
        session_id=session_id,
        frames_processed=len(frame_paths),
        duration_sec=round(duration, 2),
        pose_results=pose_results,
        biomechanics=biomechanics,
        transcript=transcript,
        ai_summary=summary,
        recommendations=recommendations,
        overall_risk=biomechanics.risk_level,
        exercise_type=exercise_type,
    )


@router.post("/compare")
async def compare_videos(
    before: UploadFile = File(...),
    after: UploadFile = File(...),
    exercise_type: str = Form("general"),
):
    """Side-by-side comparison of two movement videos."""
    before_result = await _run_pipeline(before, exercise_type)
    after_result = await _run_pipeline(after, exercise_type)
    _store_result(before_result)
    _store_result(after_result)

    bm_b = before_result.biomechanics
    bm_a = after_result.biomechanics

    def delta(a, b):
        if a is None or b is None:
            return None
        return round(b - a, 2)

    return {
        "before": before_result,
        "after": after_result,
        "delta": {
            "knee_angle": delta(bm_b.knee_angle, bm_a.knee_angle),
            "hip_angle": delta(bm_b.hip_angle, bm_a.hip_angle),
            "spine_deviation": delta(bm_b.spine_deviation, bm_a.spine_deviation),
            "asymmetry_score": delta(bm_b.asymmetry_score, bm_a.asymmetry_score),
            "risk_improved": bm_a.risk_level in ("low", "medium") and bm_b.risk_level == "high",
        },
    }


@router.get("/exercises")
def list_exercises():
    from app.services.exercise_library import list_exercises as _list
    return {"exercises": _list()}
