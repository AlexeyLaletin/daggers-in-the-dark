"""Tests for places API endpoints."""

from fastapi.testclient import TestClient


def _init_project(client: TestClient) -> None:
    """Helper to initialize project before tests."""
    client.post("/api/project/init", json={})


def test_get_places_empty(client: TestClient) -> None:
    """Test getting places when none exist."""
    _init_project(client)
    response = client.get("/api/places")
    assert response.status_code == 200
    assert response.json() == []


def test_create_place_with_scope(client: TestClient) -> None:
    """Test creating a place with scope field."""
    _init_project(client)
    place_data = {
        "name": "Test Place",
        "type": "building",
        "position": {"x": 100.0, "y": 200.0},
        "scope": "public",
        "notes_public": "Public notes",
    }
    response = client.post("/api/places", json=place_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Place"
    assert data["scope"] == "public"
    assert data["notes_public"] == "Public notes"


def test_create_place_player_mode_forces_public_scope(client: TestClient) -> None:
    """Test that player mode forces scope=public and blocks notes_gm."""
    _init_project(client)
    place_data = {
        "name": "Player Place",
        "type": "landmark",
        "position": {"x": 50.0, "y": 75.0},
        "scope": "gm",  # Try to set gm scope
        "notes_gm": "Secret notes",  # Try to set gm notes
    }
    response = client.post(
        "/api/places",
        json=place_data,
        headers={"X-View-Mode": "player"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["scope"] == "public"  # Forced to public
    assert data["notes_gm"] is None  # Blocked


def test_list_places_player_mode_hides_gm_places(client: TestClient) -> None:
    """Test that player mode hides gm-scope places."""
    _init_project(client)
    # Create public place
    client.post(
        "/api/places",
        json={"name": "Public Place", "type": "building", "scope": "public"},
    )
    # Create gm place
    client.post(
        "/api/places",
        json={"name": "GM Place", "type": "building", "scope": "gm"},
    )

    # GM mode sees both
    response_gm = client.get("/api/places", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200
    assert len(response_gm.json()) == 2

    # Player mode sees only public
    response_player = client.get("/api/places", headers={"X-View-Mode": "player"})
    assert response_player.status_code == 200
    places = response_player.json()
    assert len(places) == 1
    assert places[0]["name"] == "Public Place"


def test_get_place_player_mode_404_for_gm_place(client: TestClient) -> None:
    """Test that player mode returns 404 for gm-scope place."""
    _init_project(client)
    # Create gm place
    response = client.post(
        "/api/places",
        json={"name": "Secret Place", "type": "building", "scope": "gm"},
    )
    place_id = response.json()["id"]

    # GM mode can access
    response_gm = client.get(f"/api/places/{place_id}", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200

    # Player mode gets 404
    response_player = client.get(
        f"/api/places/{place_id}", headers={"X-View-Mode": "player"}
    )
    assert response_player.status_code == 404


def test_update_place_player_mode_ignores_scope_and_notes_gm(client: TestClient) -> None:
    """Test that player mode ignores scope and notes_gm updates."""
    _init_project(client)
    # Create public place
    response = client.post(
        "/api/places",
        json={"name": "Editable Place", "type": "building", "scope": "public"},
    )
    place_id = response.json()["id"]

    # Try to update scope and notes_gm in player mode
    response = client.put(
        f"/api/places/{place_id}",
        json={"scope": "gm", "notes_gm": "Secret", "notes_public": "Updated"},
        headers={"X-View-Mode": "player"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scope"] == "public"  # Unchanged
    assert data["notes_gm"] is None  # Unchanged
    assert data["notes_public"] == "Updated"  # Updated


def test_delete_place_player_mode_404_for_gm_place(client: TestClient) -> None:
    """Test that player mode cannot delete gm-scope place."""
    _init_project(client)
    # Create gm place
    response = client.post(
        "/api/places",
        json={"name": "Protected Place", "type": "building", "scope": "gm"},
    )
    place_id = response.json()["id"]

    # Player mode gets 404 when trying to delete
    response_player = client.delete(
        f"/api/places/{place_id}", headers={"X-View-Mode": "player"}
    )
    assert response_player.status_code == 404

    # Verify place still exists (GM can see it)
    response_gm = client.get(f"/api/places/{place_id}", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200
