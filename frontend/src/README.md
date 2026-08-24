# Frontend source

Suggested structure once React components are built:
- `components/` — reusable UI pieces (cards, tables, charts)
- `pages/` — one file per dashboard view (FleetOverview, InstrumentDetail, RiskDashboard)
- `api/` — functions that call the FastAPI backend (fetch/axios wrappers)
- `hooks/` — custom React hooks (e.g. useInstrumentList)
