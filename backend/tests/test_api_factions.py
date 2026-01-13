"""Tests for factions API endpoints."""

from fastapi.testclient import TestClient


def test_get_factions_without_init_fails(client: TestClient) -> None:
    """Test getting factions without project initialization returns 409."""
    response = client.get("/api/factions")
    assert response.status_code == 409
    assert "not initialized" in response.json()["detail"].lower()


def test_get_factions_empty(initialized_client: TestClient) -> None:
    """Test getting factions when none exist."""
    response = initialized_client.get("/api/factions")
    assert response.status_code == 200
    assert response.json() == []


def test_create_faction(initialized_client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test creating a new faction."""
    response = initialized_client.post("/api/factions", json=sample_faction)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_faction["name"]
    assert data["color"] == sample_faction["color"]
    assert data["opacity"] == sample_faction["opacity"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_faction_by_id(initialized_client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test getting a specific faction by ID."""
    # Create a faction first
    create_response = initialized_client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Get it by ID
    response = initialized_client.get(f"/api/factions/{faction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == faction_id
    assert data["name"] == sample_faction["name"]


def test_get_faction_not_found(initialized_client: TestClient) -> None:
    """Test getting a non-existent faction returns 404."""
    response = initialized_client.get("/api/factions/non-existent-id")
    assert response.status_code == 404


def test_update_faction(initialized_client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test updating a faction."""
    # Create a faction first
    create_response = initialized_client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Update it
    update_data = {"name": "Updated Name", "opacity": 0.7}
    response = initialized_client.put(f"/api/factions/{faction_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["opacity"] == 0.7
    assert data["color"] == sample_faction["color"]  # Unchanged


def test_delete_faction(initialized_client: TestClient, sample_faction: dict[str, str | float]) -> None:
    """Test deleting a faction."""
    # Create a faction first
    create_response = initialized_client.post("/api/factions", json=sample_faction)
    faction_id = create_response.json()["id"]

    # Delete it
    response = initialized_client.delete(f"/api/factions/{faction_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = initialized_client.get(f"/api/factions/{faction_id}")
    assert get_response.status_code == 404


def test_factions_gm_mode_shows_all_fields(initialized_client: TestClient) -> None:
    """Test that GM mode returns notes_gm field."""
    faction_data = {
        "name": "Secret Faction",
        "color": "#FF0000",
        "opacity": 0.5,
        "notes_public": "Public info",
        "notes_gm": "Secret GM info",
    }
    create_response = initialized_client.post("/api/factions", json=faction_data)
    faction_id = create_response.json()["id"]

    # Get in GM mode (default)
    response = initialized_client.get(f"/api/factions/{faction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["notes_gm"] == "Secret GM info"
    assert data["notes_public"] == "Public info"


def test_factions_player_mode_hides_gm_fields(initialized_client: TestClient) -> None:
    """Test that Player mode hides notes_gm field."""
    faction_data = {
        "name": "Secret Faction",
        "color": "#FF0000",
        "opacity": 0.5,
        "notes_public": "Public info",
        "notes_gm": "Secret GM info",
    }
    create_response = initialized_client.post("/api/factions", json=faction_data)
    faction_id = create_response.json()["id"]

    # Get in Player mode
    response = initialized_client.get(
        f"/api/factions/{faction_id}",
        headers={"X-View-Mode": "player"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["notes_gm"] is None
    assert data["notes_public"] == "Public info"
