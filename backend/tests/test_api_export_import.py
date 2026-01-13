"""Tests for export/import API endpoints."""

from fastapi.testclient import TestClient


def test_export_project(client: TestClient) -> None:
    """Test exporting project as SQLite file."""
    # Will implement after export API is working
    pass


def test_import_project(client: TestClient) -> None:
    """Test importing a project."""
    # Will implement after import API is working
    pass


def test_export_import_roundtrip(client: TestClient) -> None:
    """Test that export then import preserves all data."""
    # Will implement after both export and import are working
    # This is a critical integration test
    pass
