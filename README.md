# Multimodal Video Health AI

> Open-source physiotherapy assistant that analyses movement videos using computer vision, biomechanics engines, and LLM reasoning to deliver clinical-grade feedback.

[![CI](https://github.com/devkapil-tech/multimodal-video-health-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/devkapil-tech/multimodal-video-health-ai/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/react-18-61DAFB)](https://react.dev/)

---

## Features

- **Pose estimation** — MediaPipe 33-landmark skeleton with bilateral averaging (left + right)
- **Biomechanics engine** — knee, hip, and spine angle calculation using atan2/acos; asymmetry scoring
- **Clinical risk triage** — low / medium / high thresholds with evidence-based explanations
- **Audio transcription** — Whisper-based patient narration extraction via ffmpeg
- **LLM reasoning** — pluggable backend: OpenAI → Ollama → rule-based fallback
- **React dashboard** — drag-and-drop upload, metrics grid, AI summary, full transcript

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Browser  (React + Vite + Tailwind + SWR)           │
└──────────────────────┬──────────────────────────────┘
                       │ POST /api/v1/upload
┌──────────────────────▼──────────────────────────────┐
│  FastAPI (Python 3.11)                              │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Video       │  │ Pose (MediaP │  │ Audio     │  │
│  │ Extractor   │→ │ ipe + bilateral│→│ (Whisper) │  │
│  └─────────────┘  └──────┬───────┘  └───────────┘  │
│                          │                          │
│                   ┌──────▼───────┐                  │
│                   │ Biomechanics │                  │
│                   │ Engine       │                  │
│                   └──────┬───────┘                  │
│                          │                          │
│                   ┌──────▼───────┐                  │
│                   │ LLM Reasoning│ ← OpenAI/Ollama  │
│                   │ (+ fallback) │                  │
│                   └──────────────┘                  │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node 20+
- ffmpeg (`brew install ffmpeg` / `apt install ffmpeg`)

### 1 — Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # configure LLM provider if desired
uvicorn app.main:app --reload --port 8000
```

### 2 — Frontend

```bash
cd frontend
npm install
npm run dev            # http://localhost:3000
```

### 3 — Docker (full stack)

```bash
cd infra
cp ../.env.example .env   # set any overrides
docker compose up --build
# → http://localhost (nginx reverse proxy)
```

---

## Configuration

All options are controlled via environment variables (see `backend/.env.example`):

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `rule_based` | `openai` \| `ollama` \| `rule_based` |
| `OPENAI_API_KEY` | — | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Local Ollama endpoint |
| `OLLAMA_MODEL` | `llama3` | Ollama model to use |
| `WHISPER_MODEL` | `base` | `tiny` \| `base` \| `small` \| `medium` |
| `FRAME_SAMPLE_RATE` | `1` | Frames per second to analyse |
| `MAX_UPLOAD_SIZE_MB` | `200` | Upload size cap |

---

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/upload` | Upload video → full analysis JSON |
| `GET` | `/api/v1/analysis/models` | LLM model status |
| `GET` | `/api/v1/sessions` | Session list (stub) |
| `GET` | `/health` | Service health check |

---

## Contributing

Contributions are welcome. Please open an issue first for major changes.

```bash
git checkout -b feature/your-feature
# make changes
git commit -m "feat: describe your change"
git push origin feature/your-feature
# open a Pull Request
```

---

## Roadmap

- [ ] Session persistence (SQLite / Postgres)
- [ ] Side-by-side video comparison
- [ ] WebRTC live analysis (real-time pose)
- [ ] FHIR export for EHR integration
- [ ] Mobile PWA

---

## License

MIT © [Kapil Dev](https://github.com/devkapil-tech)
