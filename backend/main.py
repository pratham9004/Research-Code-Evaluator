"""FastAPI application entry point."""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import FRONTEND_DIR
from backend.db.session import init_db
from backend.db.seed import load_problems
from backend.api import problems, comparisons, dashboard, export
from backend.api import data_management
from backend.statistics import statistics as stats_module
from backend.scoring.scoring import load_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise the database and seed benchmark problem definitions."""
    init_db()
    load_problems()

    yield


app = FastAPI(title="Research Code Evaluator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(problems.router)
app.include_router(comparisons.router)
app.include_router(dashboard.router)
app.include_router(export.router)
app.include_router(data_management.router)


@app.get("/api/statistics")
def statistics():
    cfg = load_config()
    with SessionLocal() as session:
        return stats_module.compute_statistics(session, cfg)


_frontend_dist = FRONTEND_DIR / "dist"
if _frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "message": "Research Code Evaluator API.",
            "status": "Frontend not built. Run `npm run build` in frontend/.",
            "docs": "/docs",
        }
