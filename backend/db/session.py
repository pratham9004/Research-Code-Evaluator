from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.config import DATABASE_URL, DATABASE_DIR
from backend.db import models

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    models.Base.metadata.create_all(engine)


def get_session() -> Session:
    return SessionLocal()
