# PassportTwin — Instrument Reliability & Circularity Twin

Master's in Industry 4.0 — TFM (Trabajo de Fin de Máster)
Team: Alexander Castillo (Track A — Data/Backend/AAS) · Pau Modolell Rodríguez (Track B — AI/BI/Visualization)
Partner: ReiBus
Deadline: November 15, 2026

## What this is

A predictive digital twin for laboratory instrument fleets: real-time synchronization,
calibration drift prediction, survival-analysis-based risk scoring, and a circularity/reuse
recommender, built on an AAS-based digital passport for each instrument.

See `docs/` for the full architecture diagram and Agile roadmap.

## Repository structure

```
passporttwin/
├── backend/          # FastAPI service (Track A) — API, business logic
├── ai/               # Drift model, health score, survival analysis
├── frontend/         # Dashboard (Track B) — Streamlit/React
├── data/
│   └── generator/    # Synthetic data generator scripts + schema.sql
├── infra/
│   └── docker/       # Dockerfiles, additional infra config
├── docs/
│   └── adr/          # Architecture Decision Records (mirrored from Notion)
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Getting started (once services have real code in them)

```bash
docker-compose up
```

- Backend API → http://localhost:8000
- Frontend dashboard → http://localhost:8501
- PostgreSQL/TimescaleDB → localhost:5432

## Definition of Done (per feature)

1. Code merged to `main`, runs in the Docker container without manual steps.
2. Meets the sprint's validation criterion (e.g., MAE for drift model, precision/recall for
   inconsistency detection).
3. Demonstrable end-to-end in the Sprint Review, not just unit-tested in isolation.
4. Documented — even briefly — in this README or `docs/`, since it feeds the memoria later.
