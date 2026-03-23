# Contributing to Multimodal Video Health AI

Thank you for your interest! Contributions of all kinds are welcome — bug fixes, new features, documentation, and clinical feedback from physios/trainers.

## Quick Start

```bash
git clone https://github.com/devkapil-tech/multimodal-video-health-ai.git
cd multimodal-video-health-ai

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

## Ways to Contribute

### Bug Reports
Open an issue with:
- Steps to reproduce
- Expected vs actual behaviour
- Video format / OS / Python version

### Feature Ideas
Before opening a PR for a large feature, open a discussion issue first to align on approach.

### Good First Issues
Look for issues tagged [`good first issue`](https://github.com/devkapil-tech/multimodal-video-health-ai/issues?q=is%3Aissue+label%3A%22good+first+issue%22).

Popular areas to contribute:
- **New exercise types** — add entries to `backend/app/services/exercise_library.py`
- **Better clinical thresholds** — if you're a physio, your input is invaluable
- **UI improvements** — React components in `frontend/src/components/`
- **New AI providers** — extend `backend/app/services/reasoning.py`
- **Tests** — add pytest tests in `backend/tests/`

## Pull Request Process

1. Fork the repo and create a feature branch: `git checkout -b feature/your-feature`
2. Keep PRs focused — one feature or fix per PR
3. Add a short description of what changed and why
4. Ensure `uvicorn` starts without errors and `npm run build` passes
5. Open the PR — CI will run lint and build checks automatically

## Code Style

- **Python**: Follow PEP 8. We use `ruff` for linting (`ruff check app/`)
- **JavaScript**: Functional React components, no class components
- **No secrets**: Never commit `.env` files, API keys, or credentials

## Clinical Accuracy

If you are modifying biomechanical thresholds or clinical logic:
- Cite your source (peer-reviewed paper, clinical guideline, etc.)
- Note the population the threshold applies to (e.g., general adult, athlete)
- Flag it in the PR for clinical review

## Licence

By contributing, you agree your contributions are licensed under the [MIT Licence](LICENSE).

---

Questions? Open a [GitHub Discussion](https://github.com/devkapil-tech/multimodal-video-health-ai/discussions) or reach out via issues.
