"""Tests for territory tiles API endpoints."""

from fastapi.testclient import TestClient


def test_get_tile_not_found(client: TestClient) -> None:
    """Test getting a tile that doesn't exist returns 404."""
    # Will implement after tiles API is working
    pass


def test_upload_tiles_batch(client: TestClient) -> None:
    """Test uploading a batch of territory tiles."""
    # Will implement after tiles API is working
    pass


def test_download_tile(client: TestClient) -> None:
    """Test downloading a territory tile."""
    # Will implement after tiles API is working
    pass


def test_tiles_per_snapshot(client: TestClient) -> None:
    """Test tiles are isolated per snapshot."""
    # Will implement after tiles API is working
    pass
