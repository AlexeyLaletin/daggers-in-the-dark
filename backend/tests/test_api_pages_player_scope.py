"""Tests for pages API with player scope support."""

from fastapi.testclient import TestClient


def _init_project(client: TestClient) -> None:
    """Helper to initialize project before tests."""
    client.post("/api/project/init", json={})


def test_create_page_with_player_scope(client: TestClient) -> None:
    _init_project(client)
    """Test creating a page with player scope."""
    page_data = {
        "title": "Player Notes",
        "body_markdown": "These are player notes",
        "visibility": "player",
    }
    response = client.post("/api/pages", json=page_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Player Notes"
    assert data["visibility"] == "player"


def test_list_pages_player_mode_shows_player_scope(client: TestClient) -> None:
    """Test that player mode shows player-scope pages."""
    _init_project(client)
    # Create pages with different scopes
    client.post("/api/pages", json={"title": "Public Page", "body_markdown": "Public", "visibility": "public"})
    client.post("/api/pages", json={"title": "GM Page", "body_markdown": "GM only", "visibility": "gm"})
    client.post("/api/pages", json={"title": "Player Page", "body_markdown": "Player notes", "visibility": "player"})

    # GM mode sees all
    response_gm = client.get("/api/pages", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200
    assert len(response_gm.json()) == 3

    # Player mode sees public + player (not gm)
    response_player = client.get("/api/pages", headers={"X-View-Mode": "player"})
    assert response_player.status_code == 200
    pages = response_player.json()
    assert len(pages) == 2
    titles = {p["title"] for p in pages}
    assert "Public Page" in titles
    assert "Player Page" in titles
    assert "GM Page" not in titles


def test_update_page_to_player_scope(client: TestClient) -> None:
    """Test updating a page to player scope."""
    _init_project(client)
    # Create public page
    response = client.post("/api/pages", json={"title": "Convert Page", "body_markdown": "Original", "visibility": "public"})
    page_id = response.json()["id"]

    # Update to player scope
    response = client.put(f"/api/pages/{page_id}", json={"visibility": "player"})
    assert response.status_code == 200
    assert response.json()["visibility"] == "player"


def test_graph_includes_player_scope_pages(client: TestClient) -> None:
    """Test that graph API includes player-scope pages and links."""
    _init_project(client)
    # Create pages
    client.post("/api/pages", json={"title": "Public Page", "body_markdown": "Link to [[Player Page]]", "visibility": "public"})
    client.post("/api/pages", json={"title": "Player Page", "body_markdown": "Player content", "visibility": "player"})
    client.post("/api/pages", json={"title": "GM Page", "body_markdown": "GM content", "visibility": "gm"})

    # GM mode sees all nodes
    response_gm = client.get("/api/graph", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200
    graph_gm = response_gm.json()
    assert len(graph_gm["nodes"]) == 3

    # Player mode sees public + player nodes
    response_player = client.get("/api/graph", headers={"X-View-Mode": "player"})
    assert response_player.status_code == 200
    graph_player = response_player.json()
    assert len(graph_player["nodes"]) == 2
    node_titles = {n["title"] for n in graph_player["nodes"]}
    assert "Public Page" in node_titles
    assert "Player Page" in node_titles
    assert "GM Page" not in node_titles


def test_backlinks_respect_player_scope(client: TestClient) -> None:
    """Test that backlinks API respects player scope."""
    _init_project(client)
    # Create target page
    response = client.post("/api/pages", json={"title": "Target", "body_markdown": "Target page", "visibility": "public"})
    target_id = response.json()["id"]

    # Create linking pages with different scopes
    client.post("/api/pages", json={"title": "Public Link", "body_markdown": "Link to [[Target]]", "visibility": "public"})
    client.post("/api/pages", json={"title": "Player Link", "body_markdown": "Link to [[Target]]", "visibility": "player"})
    client.post("/api/pages", json={"title": "GM Link", "body_markdown": "Link to [[Target]]", "visibility": "gm"})

    # GM mode sees all backlinks
    response_gm = client.get(f"/api/graph/backlinks/{target_id}", headers={"X-View-Mode": "gm"})
    assert response_gm.status_code == 200
    backlinks_gm = response_gm.json()
    assert len(backlinks_gm) == 3

    # Player mode sees public + player backlinks
    response_player = client.get(f"/api/graph/backlinks/{target_id}", headers={"X-View-Mode": "player"})
    assert response_player.status_code == 200
    backlinks_player = response_player.json()
    assert len(backlinks_player) == 2
    titles = {b["title"] for b in backlinks_player}
    assert "Public Link" in titles
    assert "Player Link" in titles
    assert "GM Link" not in titles
