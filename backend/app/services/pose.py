"""
Pose estimation using MediaPipe.
Extracts joint landmarks per frame.
"""
import cv2
import mediapipe as mp
from app.schemas.analysis import FramePose

mp_pose = mp.solutions.pose
POSE = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)


def analyze_pose(image_path: str, frame_index: int, timestamp: float) -> FramePose:
    image = cv2.imread(image_path)
    if image is None:
        return FramePose(frame_index=frame_index, timestamp_sec=timestamp, landmarks=None,
                         shoulder=None, hip=None, knee=None, ankle=None)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = POSE.process(rgb)

    if not results.pose_landmarks:
        return FramePose(frame_index=frame_index, timestamp_sec=timestamp, landmarks=None,
                         shoulder=None, hip=None, knee=None, ankle=None)

    lm = results.pose_landmarks.landmark

    def pt(idx):
        return (round(lm[idx].x, 4), round(lm[idx].y, 4))

    # MediaPipe landmark indices
    # 11=left shoulder, 23=left hip, 25=left knee, 27=left ankle
    # Use average of left/right for symmetry detection
    shoulder = (
        (lm[11].x + lm[12].x) / 2,
        (lm[11].y + lm[12].y) / 2,
    )
    hip = (
        (lm[23].x + lm[24].x) / 2,
        (lm[23].y + lm[24].y) / 2,
    )
    knee = (
        (lm[25].x + lm[26].x) / 2,
        (lm[25].y + lm[26].y) / 2,
    )
    ankle = (
        (lm[27].x + lm[28].x) / 2,
        (lm[27].y + lm[28].y) / 2,
    )

    landmarks_dict = {
        "left_shoulder": pt(11), "right_shoulder": pt(12),
        "left_hip": pt(23),      "right_hip": pt(24),
        "left_knee": pt(25),     "right_knee": pt(26),
        "left_ankle": pt(27),    "right_ankle": pt(28),
        "left_elbow": pt(13),    "right_elbow": pt(14),
        "left_wrist": pt(15),    "right_wrist": pt(16),
    }

    return FramePose(
        frame_index=frame_index,
        timestamp_sec=timestamp,
        landmarks=landmarks_dict,
        shoulder=shoulder,
        hip=hip,
        knee=knee,
        ankle=ankle,
    )
