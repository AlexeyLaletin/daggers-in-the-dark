"""Graph API endpoints."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models import Link, NotePage
from app.services.graph import get_backlinks

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
    x_view_mode: Annotated[str, Header(alias="X-View-Mode")] = "gm",
) -> GraphResponse:
    """
    Get the full graph of pages and links.

    Args:
        session: Database session
        x_view_mode: View mode (gm or player)

    Returns:
        Graph with filtered nodes and edges
    """
    view_mode: Literal["gm", "player"] = "player" if x_view_mode == "player" else "gm"

    # Get pages (nodes)
    pages_query = select(NotePage)
    if view_mode == "player":
        pages_query = pages_query.where(NotePage.visibility == "public")
    pages = session.exec(pages_query).all()

    nodes = [
        GraphNode(
            id=page.id,
            type="page",
            title=page.title,
            visibility=page.visibility,
        )
        for page in pages
    ]

    # Get links (edges)
    links_query = select(Link)
    if view_mode == "player":
        links_query = links_query.where(Link.visibility == "public")
    links = session.exec(links_query).all()

    # Filter edges to only include links between visible nodes
    visible_node_ids = {node.id for node in nodes}
    edges = [
        GraphEdge(
            from_id=link.from_page_id,
            to_id=link.to_page_id,
            link_type=link.link_type,
            visibility=link.visibility,
        )
        for link in links
        if link.from_page_id in visible_node_ids and link.to_page_id in visible_node_ids
    ]

    return GraphResponse(nodes=nodes, edges=edges)


@router.get("/backlinks/{page_id}", response_model=list[dict[str, str]])
async def get_page_backlinks(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
    x_view_mode: Annotated[str, Header(alias="X-View-Mode")] = "gm",
) -> list[dict[str, str]]:
    """
    Get all pages that link to the given page.

    Args:
        page_id: Target page ID
        session: Database session
        x_view_mode: View mode (gm or player)

    Returns:
        List of pages linking to the target
    """
    # Check if page exists
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    view_mode: Literal["gm", "player"] = "player" if x_view_mode == "player" else "gm"
    backlink_pages = get_backlinks(session, page_id, view_mode)

    return [{"id": p.id, "title": p.title, "visibility": p.visibility} for p in backlink_pages]
