from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, sessions, analysis, report, live, memory
from app.core.config import settings
from app.db.init_db import init_db

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


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(report.router, prefix="/api/v1", tags=["reports"])
app.include_router(live.router, prefix="/api/v1", tags=["live"])
app.include_router(memory.router, prefix="/api/v1", tags=["memory"])


@app.get("/")
def root():
    return {"status": "Multimodal Video Health AI running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
