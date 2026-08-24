# PassportTwin — Instrument Reliability & Circularity Twin

Master's in Industry 4.0 — TFM (Trabajo de Fin de Máster)
Team: Alexander Castillo (Track A — Data/Backend/AAS) · Pau Modolell Rodríguez (Track B — AI/BI/Visualization)
Partner: ReiBus
Deadline: November 15, 2026

## What this is

A predictive digital twin for laboratory instrument fleets: real-time synchronization,
calibration drift prediction, survival-analysis-based risk scoring, and a circularity/reuse
recommender, built on an AAS-based digital passport for each instrument.

## Quick start

```bash
cp .env.example .env
docker compose up
```

- Backend API (FastAPI) → http://localhost:8000
- Backend Swagger/OpenAPI docs → http://localhost:8000/docs
- Frontend dashboard (React) → http://localhost:5173
- PostgreSQL/TimescaleDB → localhost:5432

> Note: this is the v0.1 Foundation skeleton. Services return placeholder responses until
> real endpoints, models, and components are implemented starting Sprint 1.

## Repository structure — what each folder is for

| Path | Purpose |
|---|---|
| `README.md` | This file — orientation for anyone opening the repo. |
| `CONTRIBUTING.md` | How Alexander and Pau branch, commit, and review each other's work. |
| `LICENSE` | Legal terms for reuse of the code (relevant since ReiBus is a partner). |
| `CHANGELOG.md` | Human-readable log of what changed each sprint — useful when writing the memoria. |
| `.gitignore` | Tells Git which files to never track (secrets, build artifacts, datasets). |
| `.editorconfig` | Forces consistent indentation/line endings between your and Pau's editors. |
| `.env.example` | Template for environment variables — copy to `.env`, which is never committed. |
| `docker-compose.yml` | Single command to start every service together (DB, backend, frontend). |
| **`backend/`** | The FastAPI service — all Track A business logic lives here. |
| `backend/app/` | Application entrypoint — `main.py`, app factory, startup/shutdown events. |
| `backend/api/` | HTTP route definitions (endpoints), grouped by resource (e.g. `instruments.py`, `passports.py`). |
| `backend/core/` | Cross-cutting configuration — settings, security, logging, dependency injection. |
| `backend/database/` | DB connection/session setup, Alembic migrations. |
| `backend/models/` | SQLAlchemy ORM models — the Python representation of your PostgreSQL tables. |
| `backend/schemas/` | Pydantic schemas — define what data looks like coming in/out of the API (validation layer). |
| `backend/services/` | Business logic that doesn't belong in a route handler (e.g. drift scoring, AAS export). |
| `backend/tests/` | Automated tests for the backend (pytest). |
| `backend/requirements.txt` | Python dependencies. |
| `backend/Dockerfile` | Instructions to build the backend's container image. |
| **`frontend/`** | The React dashboard — Track B visualization work. |
| `frontend/src/` | React components, pages, hooks, API client calls. |
| `frontend/public/` | Static assets (favicon, index.html, images) served as-is. |
| `frontend/package.json` | Node.js dependencies and npm scripts. |
| `frontend/Dockerfile` | Instructions to build the frontend's container image. |
| **`ai/`** | Everything related to the drift/risk/circularity models — Track A/B boundary. |
| `ai/datasets/` | Synthetic or real datasets used for training/validation (gitignored if large). |
| `ai/notebooks/` | Jupyter notebooks for exploration — not production code, just analysis. |
| `ai/preprocessing/` | Scripts that clean/transform raw data before it reaches a model. |
| `ai/training/` | Scripts that train the drift-prediction / survival-analysis models. |
| `ai/inference/` | Scripts/functions that load a trained model and score new data in production. |
| `ai/models/` | Serialized trained model artifacts (`.pkl`, `.joblib` — gitignored, usually too large for Git). |
| **`docs/`** | Everything that eventually feeds your memoria and defense. |
| `docs/architecture/` | The six-layer architecture diagram and written architecture description. |
| `docs/adr/` | Architecture Decision Records — one file per major decision, mirrored from Notion. |
| `docs/api/` | API documentation beyond auto-generated Swagger (e.g. usage examples). |
| `docs/diagrams/` | Data pipeline diagrams, ER diagrams, sequence diagrams. |
| `docs/experiments/` | Write-ups of EXP-01 through EXP-07 and their results. |
| `docs/thesis/` | Draft memoria chapters, written progressively sprint by sprint. |
| **`infra/`** | Infrastructure configuration that isn't application code. |
| `infra/postgres/` | Postgres-specific config (init scripts, tuning parameters). |
| `infra/nginx/` | Reverse proxy config, if you expose the app behind Nginx later. |
| `infra/docker/` | Shared Docker configuration not specific to one service. |
| `infra/monitoring/` | Grafana dashboards/config, if used for operational monitoring. |
| `infra/raspberry/` | Configuration for any Raspberry Pi used for MQTT sensor ingestion. |
| **`scripts/`** | One-off utility scripts (data seeding, backups, deployment helpers). |
| **`.github/workflows/`** | GitHub Actions — automated CI (run tests, lint, build Docker images on every push). |
| **`.github/ISSUE_TEMPLATE/`** | Standard forms for opening bug reports / feature requests as GitHub Issues. |
| **`.github/PULL_REQUEST_TEMPLATE.md`** | Checklist that appears automatically when either of you opens a PR. |

## Definition of Done (per feature)

1. Code merged to `main`, runs in Docker without manual steps.
2. Meets that sprint's validation criterion (e.g., MAE for drift model, precision/recall for
   inconsistency detection).
3. Demonstrable end-to-end in the Sprint Review, not just unit-tested in isolation.
4. Documented — even briefly — in `docs/`, since it feeds the memoria later.
