"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_faction() -> dict[str, str | float]:
    """Sample faction data for testing."""
    return {
        "name": "The Crows",
        "color": "#FF5733",
        "opacity": 0.4,
        "notes_public": "A notorious gang",
        "notes_gm": "Secret: they work for the City Council",
    }


@pytest.fixture
def sample_person() -> dict[str, str | list[str]]:
    """Sample person data for testing."""
    return {
        "name": "Lyssa",
        "aliases": ["The Shadow"],
        "status": "alive",
        "tags": ["smuggler", "informant"],
        "notes_public": "Known smuggler in Crow's Foot",
        "notes_gm": "Actually a spy for the Bluecoats",
    }


@pytest.fixture
def sample_place() -> dict[str, str]:
    """Sample place data for testing."""
    return {
        "name": "The Leaky Bucket",
        "type": "building",
        "notes_public": "A tavern in Crow's Foot",
        "notes_gm": "Secret meeting place for The Crows",
    }
