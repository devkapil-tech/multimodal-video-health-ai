from pydantic import BaseModel
from typing import List, Optional


class PoseLandmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: float


class FramePose(BaseModel):
    frame_index: int
    timestamp_sec: float
    landmarks: Optional[dict]
    shoulder: Optional[tuple]
    hip: Optional[tuple]
    knee: Optional[tuple]
    ankle: Optional[tuple]


class BiomechanicsResult(BaseModel):
    knee_angle: Optional[float]
    hip_angle: Optional[float]
    spine_deviation: Optional[float]
    asymmetry_score: Optional[float]
    alerts: List[str]
    risk_level: str  # low / medium / high


class AnalysisResult(BaseModel):
    session_id: str
    frames_processed: int
    duration_sec: float
    pose_results: List[FramePose]
    biomechanics: BiomechanicsResult
    transcript: Optional[str]
    ai_summary: Optional[str]
    recommendations: List[str]
    overall_risk: str
    exercise_type: str = "general"
