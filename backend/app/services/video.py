import os
import cv2
import uuid
from pathlib import Path
from app.core.config import settings


def extract_frames(video_path: str, session_id: str) -> tuple[list[str], float]:
    """Extract frames at configured FPS. Returns (frame_paths, duration_sec)."""
    output_dir = Path(settings.frames_dir) / session_id
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / video_fps
    sample_every = max(1, int(video_fps / settings.frame_rate))

    frame_paths = []
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % sample_every == 0:
            timestamp = count / video_fps
            path = str(output_dir / f"frame_{count:06d}_{timestamp:.2f}s.jpg")
            cv2.imwrite(path, frame)
            frame_paths.append(path)
        count += 1

    cap.release()
    return frame_paths, duration_sec


def get_video_metadata(video_path: str) -> dict:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return {
        "fps": fps,
        "width": width,
        "height": height,
        "total_frames": total_frames,
        "duration_sec": total_frames / fps if fps else 0,
    }
