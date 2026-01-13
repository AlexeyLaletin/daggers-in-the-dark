"""Tests for factions API endpoints."""

from fastapi.testclient import TestClient


def test_get_factions_empty(client: TestClient) -> None:
    """Test getting factions when none exist."""
    response = client.get("/api/factions")
    assert response.status_code == 200
    # Will implement actual logic later
    # assert response.json() == {"factions": []}


def test_create_faction(client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test creating a new faction."""
    response = client.post("/api/factions", json=sample_faction)
    # Will implement actual logic later
    # assert response.status_code == 201
    # data = response.json()
    # assert data["name"] == sample_faction["name"]
    # assert data["color"] == sample_faction["color"]
    # assert "id" in data


def test_get_faction_by_id(client: TestClient) -> None:
    """Test getting a specific faction by ID."""
    # Will implement after CRUD is working
    pass


def test_update_faction(client: TestClient) -> None:
    """Test updating a faction."""
    # Will implement after CRUD is working
    pass


def test_delete_faction(client: TestClient) -> None:
    """Test deleting a faction."""
    # Will implement after CRUD is working
    pass


def test_factions_gm_mode_shows_all_fields(client: TestClient) -> None:
    """Test that GM mode returns notes_gm field."""
    # Will implement after view mode filter is working
    pass


def test_factions_player_mode_hides_gm_fields(client: TestClient) -> None:
    """Test that Player mode hides notes_gm field."""
    # Will implement after view mode filter is working
    pass
