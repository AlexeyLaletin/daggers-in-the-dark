"""Note pages API endpoints."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import get_view_mode, require_initialized_project
from app.models import NotePage, World
from app.schemas import NotePageCreate, NotePageResponse, NotePageUpdate
from app.services.pages_service import PagesService
from app.services.visibility import ViewMode, VisibilityService

router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("", response_model=list[NotePageResponse])
async def list_pages(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> list[NotePageResponse]:
    """List all note pages."""
    visibility = VisibilityService()
    allowed_scopes = visibility.get_allowed_scopes(view_mode)

    pages = session.execute(
        select(NotePage).where(NotePage.scope.in_(allowed_scopes))
    ).scalars().all()
    return [NotePageResponse.from_orm(p) for p in pages]


@router.post("", response_model=NotePageResponse, status_code=201)
async def create_page(
    page_data: NotePageCreate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> NotePageResponse:
    """Create a new note page."""
    # Check for duplicate title
    existing = session.execute(select(NotePage).where(NotePage.title == page_data.title)).scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Page with this title already exists")

    page = NotePage(
        id=str(uuid.uuid4()),
        world_id=world.id,
        title=page_data.title,
        body_markdown=page_data.body_markdown,
        scope=page_data.visibility,  # Accept 'visibility' from schema, map to 'scope' in model
        entity_type=page_data.entity_type,
        entity_id=page_data.entity_id,
    )
    session.add(page)
    session.commit()
    session.refresh(page)

    # Build wikilinks
    pages_service = PagesService(session)
    pages_service.rebuild_wikilinks(page.id)
    session.commit()

    return NotePageResponse.from_orm(page)


@router.get("/{page_id}", response_model=NotePageResponse)
async def get_page(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> NotePageResponse:
    """Get a note page by ID."""
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    # Check visibility
    visibility = VisibilityService()
    if not visibility.filter_scope(page.scope, view_mode):
        raise HTTPException(status_code=404, detail="Page not found")

    return NotePageResponse.from_orm(page)


@router.put("/{page_id}", response_model=NotePageResponse)
async def update_page(
    page_id: str,
    page_data: NotePageUpdate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> NotePageResponse:
    """Update a note page."""
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    # Check for duplicate title if title is being changed
    if page_data.title and page_data.title != page.title:
        existing = session.execute(select(NotePage).where(NotePage.title == page_data.title)).scalars().first()
        if existing:
            raise HTTPException(status_code=409, detail="Page with this title already exists")

    # Update only provided fields
    update_data = page_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        # Map 'visibility' from schema to 'scope' in model
        if field == "visibility":
            page.scope = value
        else:
            setattr(page, field, value)

    page.updated_at = datetime.utcnow()
    session.add(page)
    session.commit()
    session.refresh(page)

    # Rebuild wikilinks if body_markdown was updated
    if "body_markdown" in update_data:
        pages_service = PagesService(session)
        pages_service.rebuild_wikilinks(page.id)
        session.commit()

    return NotePageResponse.from_orm(page)


@router.delete("/{page_id}", status_code=204)
async def delete_page(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> None:
    """Delete a note page."""
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    session.delete(page)
    session.commit()
