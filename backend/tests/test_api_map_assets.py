"""Tests for map assets API endpoints."""

import io

from fastapi.testclient import TestClient


def test_upload_map_to_snapshot(client: TestClient, seed_small_town: dict) -> None:
    """Test uploading a base map image to a snapshot."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    # Create a fake PNG image
    fake_image = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    files = {"file": ("test_map.png", io.BytesIO(fake_image), "image/png")}

    response = client.post(f"/api/snapshots/{snapshot_id}/map", files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ok"
    assert data["snapshot_id"] == snapshot_id
    assert "map_asset_id" in data


def test_download_map_from_snapshot(client: TestClient, seed_small_town: dict) -> None:
    """Test downloading a base map image from a snapshot."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    # Upload first
    fake_image = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    files = {"file": ("test_map.png", io.BytesIO(fake_image), "image/png")}
    client.post(f"/api/snapshots/{snapshot_id}/map", files=files)

    # Download
    response = client.get(f"/api/snapshots/{snapshot_id}/map")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert len(response.content) > 0


def test_upload_map_replaces_existing(client: TestClient, seed_small_town: dict) -> None:
    """Test that uploading a map replaces the existing one."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    # Upload first map
    fake_image1 = b"FAKE_IMAGE_1"
    files1 = {"file": ("map1.png", io.BytesIO(fake_image1), "image/png")}
    response1 = client.post(f"/api/snapshots/{snapshot_id}/map", files=files1)
    map_id1 = response1.json()["map_asset_id"]

    # Upload second map
    fake_image2 = b"FAKE_IMAGE_2_DIFFERENT"
    files2 = {"file": ("map2.png", io.BytesIO(fake_image2), "image/png")}
    response2 = client.post(f"/api/snapshots/{snapshot_id}/map", files=files2)
    map_id2 = response2.json()["map_asset_id"]

    # Same map asset ID (updated)
    assert map_id1 == map_id2

    # Download returns new content
    response = client.get(f"/api/snapshots/{snapshot_id}/map")
    assert response.content == fake_image2


def test_upload_map_invalid_file_type(client: TestClient, seed_small_town: dict) -> None:
    """Test that uploading non-image file fails."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    fake_text = b"This is not an image"
    files = {"file": ("test.txt", io.BytesIO(fake_text), "text/plain")}

    response = client.post(f"/api/snapshots/{snapshot_id}/map", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_download_map_not_found(client: TestClient, seed_small_town: dict) -> None:
    """Test downloading map from snapshot without map returns 404."""
    snapshot_id = seed_small_town["snapshot_ids"]["day2"]  # No map uploaded

    response = client.get(f"/api/snapshots/{snapshot_id}/map")
    assert response.status_code == 404
    assert "Map not found" in response.json()["detail"]


def test_delete_map(client: TestClient, seed_small_town: dict) -> None:
    """Test deleting a map asset."""
    snapshot_id = seed_small_town["snapshot_ids"]["day1"]

    # Upload map
    fake_image = b"FAKE_IMAGE"
    files = {"file": ("map.png", io.BytesIO(fake_image), "image/png")}
    client.post(f"/api/snapshots/{snapshot_id}/map", files=files)

    # Delete
    response = client.delete(f"/api/snapshots/{snapshot_id}/map")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/snapshots/{snapshot_id}/map")
    assert response.status_code == 404


def test_upload_map_nonexistent_snapshot(client: TestClient) -> None:
    """Test uploading map to nonexistent snapshot returns 404."""
    # Initialize project first
    client.post("/api/project/init", json={})

    fake_image = b"FAKE_IMAGE"
    files = {"file": ("map.png", io.BytesIO(fake_image), "image/png")}

    response = client.post("/api/snapshots/nonexistent-id/map", files=files)
    assert response.status_code == 404
    assert "Snapshot not found" in response.json()["detail"]
