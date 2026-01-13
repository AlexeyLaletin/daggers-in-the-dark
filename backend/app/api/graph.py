"""Graph API endpoints."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import get_view_mode, require_initialized_project
from app.models import World
from app.services.graph_service import GraphService
from app.services.visibility import ViewMode

router = APIRouter(prefix="/graph", tags=["graph"])


class GraphNode(BaseModel):
    """Graph node representation."""

    id: str
    type: Literal["page"]  # Can be extended to include faction, person, place
    title: str
    visibility: str


class GraphEdge(BaseModel):
    """Graph edge representation."""

    from_id: str
    to_id: str
    link_type: str
    visibility: str


class GraphResponse(BaseModel):
    """Graph response with nodes and edges."""

    nodes: list[GraphNode]
    edges: list[GraphEdge]


@router.get("", response_model=GraphResponse)
async def get_graph(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> GraphResponse:
    """
    Get the full graph of pages and links.

    Args:
        session: Database session
        world: World instance (ensures project is initialized)
        view_mode: View mode (gm or player)

    Returns:
        Graph with filtered nodes and edges
    """
    graph_service = GraphService(session)
    pages, links = graph_service.get_graph(view_mode)

    nodes = [
        GraphNode(
            id=page.id,
            type="page",
            title=page.title,
            visibility=page.scope,  # Map scope to visibility for API compat
        )
        for page in pages
    ]

    edges = [
        GraphEdge(
            from_id=link.from_page_id,
            to_id=link.to_page_id,
            link_type=link.link_type,
            visibility=link.scope,  # Map scope to visibility for API compat
        )
        for link in links
    ]

    return GraphResponse(nodes=nodes, edges=edges)


@router.get("/backlinks/{page_id}", response_model=list[dict[str, str]])
async def get_page_backlinks(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> list[dict[str, str]]:
    """
    Get all pages that link to the given page.

    Args:
        page_id: Target page ID
        session: Database session
        world: World instance (ensures project is initialized)
        view_mode: View mode (gm or player)

    Returns:
        List of pages linking to the target
    """
    # Check if page exists
    from app.models import NotePage

    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    graph_service = GraphService(session)
    backlink_pages = graph_service.get_backlinks(page_id, view_mode)

    return [{"id": p.id, "title": p.title, "visibility": p.scope} for p in backlink_pages]
