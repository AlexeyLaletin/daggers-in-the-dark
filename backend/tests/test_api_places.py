"""Tests for places API endpoints."""

from fastapi.testclient import TestClient


def test_get_places_empty(client: TestClient) -> None:
    """Test getting places when none exist."""
    response = client.get("/api/places")
    # Will implement actual logic later
    # assert response.status_code == 200


def test_create_place(client: TestClient, sample_place: dict[str, str]) -> None:
    """Test creating a new place."""
    # Will implement after CRUD is working
    pass


def test_place_with_position(client: TestClient) -> None:
    """Test place can have map coordinates."""
    # Will implement after CRUD is working
    pass


def test_place_owner_faction(client: TestClient) -> None:
    """Test place can be owned by a faction."""
    # Will implement after CRUD is working
    pass
