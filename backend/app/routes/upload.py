import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.config import settings
from app.services.video import extract_frames, get_video_metadata
from app.services.pose import analyze_pose
from app.services.biomechanics import analyze_biomechanics
from app.services.audio import transcribe
from app.services.reasoning import generate_insights
from app.schemas.analysis import AnalysisResult
from app.routes.report import store_result

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


@router.post("/upload", response_model=AnalysisResult)
async def upload_video(
    file: UploadFile = File(...),
    exercise_type: str = Form("general"),
    patient_token: str = Form(""),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported format. Allowed: {ALLOWED_EXTENSIONS}")

    session_id = str(uuid.uuid4())[:8]
    os.makedirs(settings.data_dir, exist_ok=True)
    video_path = f"{settings.data_dir}/{session_id}{ext}"

    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Check file size
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if size_mb > settings.max_video_size_mb:
        os.remove(video_path)
        raise HTTPException(400, f"File too large ({size_mb:.1f} MB). Max: {settings.max_video_size_mb} MB")

    # Pipeline
    frame_paths, duration = extract_frames(video_path, session_id)

    pose_results = []
    for i, fp in enumerate(frame_paths):
        timestamp = i / max(settings.frame_rate, 1)
        pose_results.append(analyze_pose(fp, frame_index=i, timestamp=timestamp))

    biomechanics = analyze_biomechanics(pose_results, exercise_type=exercise_type)
    transcript = transcribe(video_path, session_id)
    summary, recommendations = generate_insights(biomechanics, transcript)

    # CML: retrieve history and store result
    longitudinal_insights = None
    if patient_token:
        from app.services.memory_retrieve import get_patient_history, build_longitudinal_insights, build_history_context
        from app.services.memory_store import store_session
        history = get_patient_history(patient_token)
        if history:
            history_ctx = build_history_context(history)
            # Re-run reasoning with history context
            summary, recommendations = generate_insights(biomechanics, transcript, history_context=history_ctx)
        longitudinal_insights = build_longitudinal_insights(history, exercise_type)
        result = AnalysisResult(
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
            patient_token=patient_token if patient_token else None,
            longitudinal_insights=longitudinal_insights,
        )
        store_session(result, patient_token)
    else:
        result = AnalysisResult(
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
    store_result(result)
    return result
