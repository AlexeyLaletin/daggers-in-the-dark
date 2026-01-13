"""Tests for project initialization API endpoints."""

from fastapi.testclient import TestClient


def test_init_project_success(client: TestClient) -> None:
    """Test successful project initialization."""
    response = client.post(
        "/api/project/init",
        json={
            "world_name": "Test World",
            "description": "A test world",
            "timezone": "America/New_York",
            "initial_snapshot_label": "Beginning",
        },
    )
    assert response.status_code == 201
    data = response.json()

    # Check world
    assert data["world"]["name"] == "Test World"
    assert data["world"]["description"] == "A test world"
    assert data["world"]["timezone"] == "America/New_York"
    assert "id" in data["world"]

    # Check initial snapshot
    assert data["initial_snapshot"]["label"] == "Beginning"
    assert "id" in data["initial_snapshot"]
    assert "at_date" in data["initial_snapshot"]


def test_init_project_with_defaults(client: TestClient) -> None:
    """Test project initialization with default values."""
    response = client.post("/api/project/init", json={})
    assert response.status_code == 201
    data = response.json()

    assert data["world"]["name"] == "Doskvol"
    assert data["world"]["timezone"] == "UTC"
    assert data["initial_snapshot"]["label"] == "Initial"


def test_init_project_already_initialized(initialized_client: TestClient) -> None:
    """Test that re-initializing returns 409."""
    response = initialized_client.post("/api/project/init", json={})
    assert response.status_code == 409
    assert "already initialized" in response.json()["detail"].lower()


def test_crud_without_init_fails(client: TestClient) -> None:
    """Test that CRUD operations fail without project initialization."""
    # Try to create a faction
    response = client.post(
        "/api/factions", json={"name": "Test Faction", "color": "#FF0000", "opacity": 0.5}
    )
    assert response.status_code == 409
    assert "not initialized" in response.json()["detail"].lower()
