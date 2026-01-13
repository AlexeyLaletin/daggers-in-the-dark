"""Tests for snapshots API endpoints."""

import io

from fastapi.testclient import TestClient


def test_list_snapshots(client: TestClient, seed_small_town: dict) -> None:
    """Test listing all snapshots."""
    response = client.get("/api/snapshots")
    assert response.status_code == 200
    data = response.json()
    assert len(data["snapshots"]) == 3
    assert data["active_snapshot_id"] == seed_small_town["snapshot_ids"]["day3"]


def test_create_snapshot(client: TestClient) -> None:
    """Test creating a new snapshot."""
    # Initialize project first
    client.post("/api/project/init", json={})

    snapshot_data = {
        "at_date": "1920-01-04T08:00:00Z",
        "label": "Day4",
    }
    response = client.post("/api/snapshots", json=snapshot_data)
    assert response.status_code == 201
    data = response.json()
    assert data["label"] == "Day4"
    assert "id" in data


def test_create_snapshot_with_clone_from(client: TestClient, seed_small_town: dict) -> None:
    """Test creating a snapshot with clone_from parameter."""
    source_snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    # Upload a map to source snapshot
    fake_image = b"SOURCE_MAP_IMAGE"
    files = {"file": ("map.png", io.BytesIO(fake_image), "image/png")}
    client.post(f"/api/snapshots/{source_snapshot_id}/map", files=files)

    # Create tiles for source snapshot (using existing faction)
    faction_id = seed_small_town["faction_ids"]["bluecoats"]
    tiles_data = {
        "faction_id": faction_id,
        "tiles": [
            {
                "z": 0,
                "x": 0,
                "y": 0,
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            },
        ],
    }
    client.put(f"/api/snapshots/{source_snapshot_id}/territory/tiles/batch", json=tiles_data)

    # Create new snapshot with clone_from
    snapshot_data = {
        "at_date": "1920-01-05T08:00:00Z",
        "label": "Day5_Cloned",
        "clone_from": source_snapshot_id,
    }
    response = client.post("/api/snapshots", json=snapshot_data)
    assert response.status_code == 201
    new_snapshot_id = response.json()["id"]

    # Verify map was cloned
    response_map = client.get(f"/api/snapshots/{new_snapshot_id}/map")
    assert response_map.status_code == 200
    assert response_map.content == fake_image

    # Verify tiles were cloned
    response_tile = client.get(
        f"/api/snapshots/{new_snapshot_id}/territory/tiles",
        params={"faction_id": faction_id, "z": 0, "x": 0, "y": 0},
    )
    assert response_tile.status_code == 200


def test_create_snapshot_clone_from_nonexistent(client: TestClient) -> None:
    """Test that cloning from nonexistent snapshot fails."""
    # Initialize project first
    client.post("/api/project/init", json={})

    snapshot_data = {
        "at_date": "1920-01-06T08:00:00Z",
        "label": "FailedClone",
        "clone_from": "nonexistent-snapshot-id",
    }
    response = client.post("/api/snapshots", json=snapshot_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_set_active_snapshot(client: TestClient, seed_small_town: dict) -> None:
    """Test switching the active snapshot."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    response = client.put(f"/api/snapshots/active/{snapshot_id}")
    assert response.status_code == 200
    assert response.json()["active_snapshot_id"] == snapshot_id

    # Verify active snapshot changed
    response_list = client.get("/api/snapshots")
    assert response_list.json()["active_snapshot_id"] == snapshot_id


def test_delete_snapshot(client: TestClient, seed_small_town: dict) -> None:
    """Test deleting a snapshot."""
    # Create a new snapshot to delete
    snapshot_data = {"at_date": "1920-01-07T08:00:00Z", "label": "ToDelete"}
    response = client.post("/api/snapshots", json=snapshot_data)
    snapshot_id = response.json()["id"]

    # Delete it
    response = client.delete(f"/api/snapshots/{snapshot_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/snapshots/{snapshot_id}")
    assert response.status_code == 404
