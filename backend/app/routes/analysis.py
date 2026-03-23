from fastapi import APIRouter

router = APIRouter()


@router.get("/analysis/models")
def list_models():
    """Show available AI models and their status."""
    models = {
        "pose_estimation": {"name": "MediaPipe Pose", "status": "active", "type": "local"},
        "llm": {"name": "Llama3 / GPT-4o-mini", "status": "configurable", "type": "local/api"},
        "audio": {"name": "Whisper", "status": "optional", "type": "local"},
        "vision": {"name": "LLaVA / Qwen-VL", "status": "coming_soon", "type": "local"},
    }
    return {"models": models}
