"""Tests for people API endpoints."""

from fastapi.testclient import TestClient


def test_get_people_empty(client: TestClient) -> None:
    """Test getting people when none exist."""
    response = client.get("/api/people")
    # Will implement actual logic later
    # assert response.status_code == 200


def test_create_person(client: TestClient, sample_person: dict[str, str | list[str]]) -> None:
    """Test creating a new person."""
    # Will implement after CRUD is working
    pass


def test_person_faction_memberships(client: TestClient) -> None:
    """Test person can belong to multiple factions."""
    # Will implement after CRUD is working
    pass


def test_person_workplace_reference(client: TestClient) -> None:
    """Test person can reference a workplace place."""
    # Will implement after CRUD is working
    pass
