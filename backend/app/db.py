"""Database connection and initialization."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

# Default database path (can be overridden)
DATABASE_PATH = Path("./data/blades.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with connection pooling for SQLite
engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite with FastAPI
    echo=False,  # Set to True for SQL debug logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database schema."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
