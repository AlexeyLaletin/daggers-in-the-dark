"""Tests for graph API endpoints."""

from fastapi.testclient import TestClient


def test_get_graph_empty(client: TestClient) -> None:
    """Test getting graph when no pages exist."""
    # Will implement after graph API is working
    pass


def test_graph_nodes_and_edges(client: TestClient) -> None:
    """Test graph returns nodes and edges."""
    # Will implement after graph API is working
    pass


def test_graph_gm_filter(client: TestClient) -> None:
    """Test graph filters GM-only nodes in player mode."""
    # Will implement after view mode filter is working
    pass


def test_backlinks(client: TestClient) -> None:
    """Test backlinks API returns pages linking to a given page."""
    # Will implement after wikilinks parser is working
    pass
