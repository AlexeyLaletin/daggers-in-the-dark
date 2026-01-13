"""Database connection and initialization."""

from pathlib import Path
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

# Default database path (can be overridden)
DATABASE_PATH = Path("./data/blades.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with connection pooling for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite with FastAPI
    echo=False,  # Set to True for SQL debug logging
)


def init_db() -> None:
    """Initialize database schema."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection."""
    with Session(engine) as session:
        yield session
