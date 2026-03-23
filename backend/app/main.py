from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, sessions, analysis
from app.core.config import settings

app = FastAPI(
    title="Multimodal Video Health AI",
    description="AI-powered movement analysis for physiotherapy and injury prevention",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])


@app.get("/")
def root():
    return {"status": "Multimodal Video Health AI running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
