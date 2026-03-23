"""
Audio transcription using OpenAI Whisper.
Extracts speech from video for context-aware analysis.
"""
import subprocess
import os
from app.core.config import settings

try:
    import whisper
    WHISPER_AVAILABLE = True
    _model = None
except ImportError:
    WHISPER_AVAILABLE = False


def _get_model():
    global _model
    if _model is None:
        import whisper
        _model = whisper.load_model(settings.whisper_model)
    return _model


def extract_audio(video_path: str, output_path: str) -> bool:
    """Extract audio track from video using ffmpeg."""
    result = subprocess.run(
        ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
         "-ar", "16000", "-ac", "1", output_path, "-y", "-loglevel", "error"],
        capture_output=True
    )
    return result.returncode == 0 and os.path.exists(output_path)


def transcribe(video_path: str, session_id: str) -> str | None:
    if not WHISPER_AVAILABLE:
        return None

    audio_path = f"data/outputs/{session_id}_audio.wav"
    os.makedirs("data/outputs", exist_ok=True)

    if not extract_audio(video_path, audio_path):
        return None

    try:
        model = _get_model()
        result = model.transcribe(audio_path)
        return result.get("text", "").strip() or None
    except Exception:
        return None
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
