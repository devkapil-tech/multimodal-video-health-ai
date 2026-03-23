"""WebSocket endpoint for real-time frame analysis (live camera mode)."""
import base64
import json
import logging
import numpy as np
import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.pose import analyze_pose
from app.services.biomechanics import analyze_biomechanics
import tempfile
import os

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/live")
async def live_analysis(websocket: WebSocket):
    """
    Accept base64-encoded JPEG frames, return pose + biomechanics JSON.
    Client sends: {"frame": "<base64 JPEG>", "exercise_type": "squat"}
    Server returns: {"knee_angle": 82.3, "hip_angle": 71.1, "risk_level": "low", "alerts": [...]}
    """
    await websocket.accept()
    logger.info("Live camera session started")

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            b64 = data.get("frame", "")
            exercise_type = data.get("exercise_type", "general")

            if not b64:
                continue

            # Decode base64 JPEG to numpy array
            img_bytes = base64.b64decode(b64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                continue

            # Save to temp file for pose service (reuses existing interface)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                cv2.imwrite(tmp.name, img)
                tmp_path = tmp.name

            try:
                pose = analyze_pose(tmp_path, frame_index=0, timestamp=0.0)
                bm = analyze_biomechanics([pose], exercise_type=exercise_type)
            finally:
                os.unlink(tmp_path)

            await websocket.send_text(json.dumps({
                "knee_angle": bm.knee_angle,
                "hip_angle": bm.hip_angle,
                "spine_deviation": bm.spine_deviation,
                "asymmetry_score": bm.asymmetry_score,
                "risk_level": bm.risk_level,
                "alerts": bm.alerts,
                "pose_detected": pose.shoulder is not None,
            }))

    except WebSocketDisconnect:
        logger.info("Live camera session ended")
    except Exception as e:
        logger.error(f"Live session error: {e}")
        await websocket.close(code=1011)
