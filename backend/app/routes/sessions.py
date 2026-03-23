from fastapi import APIRouter

router = APIRouter()


@router.get("/sessions")
def list_sessions():
    """List all analysis sessions. (Extend with DB in v2)"""
    return {"sessions": [], "message": "Connect a database to persist sessions"}
