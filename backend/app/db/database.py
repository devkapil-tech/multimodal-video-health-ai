"""SQLAlchemy sync engine. Gracefully disabled when DATABASE_URL is not set."""
import os
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "")

engine = None
SessionLocal = None

if DATABASE_URL:
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # Railway uses postgres:// but SQLAlchemy needs postgresql://
        url = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        engine = create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"CML database init failed: {e}")


def get_db() -> Generator:
    if SessionLocal is None:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_enabled() -> bool:
    return SessionLocal is not None
