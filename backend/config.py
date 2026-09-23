"""Application configuration paths and settings."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATABASE_DIR = PROJECT_ROOT / "database"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

PROBLEMS_YAML = CONFIG_DIR / "problems.yaml"
SCORING_YAML = CONFIG_DIR / "scoring.yaml"

# Allow pointing tests at an isolated database file.
if os.environ.get("RESEARCH_DB_PATH"):
    DATABASE_PATH = Path(os.environ["RESEARCH_DB_PATH"])
else:
    DATABASE_PATH = DATABASE_DIR / "research.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Execution safety limits (docs/05 section 19)
EXECUTION_TIMEOUT_SECONDS = 10
TEMP_BASE_DIR = DATABASE_DIR / "tmp"

# Static-analysis tool availability is detected at runtime.
