"""
PassportTwin backend — application entrypoint.

This file wires together the FastAPI app. Route logic lives in `api/`,
configuration in `core/`, DB session handling in `database/`.
"""
from fastapi import FastAPI

app = FastAPI(
    title="PassportTwin API",
    description="Digital passport and reliability twin for measurement instrument fleets.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """Basic health/liveness check — confirms the container is running."""
    return {"status": "ok", "service": "passporttwin-backend", "version": "0.1.0"}


@app.get("/health")
def health_check():
    """Used by orchestration/monitoring to verify the service is alive."""
    return {"status": "healthy"}


# Route modules will be included here as they're built, e.g.:
# from api import instruments
# app.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
