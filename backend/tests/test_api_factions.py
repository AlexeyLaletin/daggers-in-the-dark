"""Tests for factions API endpoints."""

from fastapi.testclient import TestClient


def test_get_factions_empty(client: TestClient) -> None:
    """Test getting factions when none exist."""
    response = client.get("/api/factions")
    assert response.status_code == 200
    assert response.json() == []


def test_create_faction(client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test creating a new faction."""
    response = client.post("/api/factions", json=sample_faction)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_faction["name"]
    assert data["color"] == sample_faction["color"]
    assert data["opacity"] == sample_faction["opacity"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_faction_by_id(client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test getting a specific faction by ID."""
    # Create a faction first
    create_response = client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Get it by ID
    response = client.get(f"/api/factions/{faction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == faction_id
    assert data["name"] == sample_faction["name"]


def test_get_faction_not_found(client: TestClient) -> None:
    """Test getting a non-existent faction returns 404."""
    response = client.get("/api/factions/non-existent-id")
    assert response.status_code == 404


def test_update_faction(client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test updating a faction."""
    # Create a faction first
    create_response = client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Update it
    update_data = {"name": "Updated Name", "opacity": 0.7}
    response = client.put(f"/api/factions/{faction_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["opacity"] == 0.7
    assert data["color"] == sample_faction["color"]  # Unchanged


def test_delete_faction(client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test deleting a faction."""
    # Create a faction first
    create_response = client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/api/factions/{faction_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/api/factions/{faction_id}")
    assert get_response.status_code == 404


def test_factions_gm_mode_shows_all_fields(client: TestClient) -> None:
    """Test that GM mode returns notes_gm field."""
    # Will implement after view mode filter is working
    pass


def test_factions_player_mode_hides_gm_fields(client: TestClient) -> None:
    """Test that Player mode hides notes_gm field."""
    # Will implement after view mode filter is working
    pass
