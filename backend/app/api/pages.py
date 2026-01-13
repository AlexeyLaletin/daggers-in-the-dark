"""Note pages API endpoints."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import NotePage, World
from app.schemas import NotePageCreate, NotePageResponse, NotePageUpdate
from app.services.graph import rebuild_wikilinks_for_page


def get_default_world_id(session: Session) -> str:
    """Get the default world ID (first world in DB)."""
    world = session.execute(select(World)).scalars().first()
    if not world:
        raise HTTPException(status_code=500, detail="No world found in database")
    return world.id

router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("", response_model=list[NotePageResponse])
async def list_pages(
    session: Annotated[Session, Depends(get_session)],
) -> list[NotePage]:
    """List all note pages."""
    pages = session.execute(select(NotePage)).scalars().all()
    return list(pages)


@router.post("", response_model=NotePageResponse, status_code=201)
async def create_page(
    page_data: NotePageCreate,
    session: Annotated[Session, Depends(get_session)],
) -> NotePage:
    """Create a new note page."""
    world_id = get_default_world_id(session)

    # Check for duplicate title
    existing = session.execute(select(NotePage).where(NotePage.title == page_data.title)).scalars().first()
    if existing:
        raise HTTPException(status_code=409, detail="Page with this title already exists")

    page = NotePage(
        id=str(uuid.uuid4()),
        world_id=world_id,
        title=page_data.title,
        body_markdown=page_data.body_markdown,
        scope=page_data.visibility,  # TODO: Update schema to use 'scope' field name
        entity_type=page_data.entity_type,
        entity_id=page_data.entity_id,
    )
    session.add(page)
    session.commit()
    session.refresh(page)
    return page


@router.get("/{page_id}", response_model=NotePageResponse)
async def get_page(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> NotePage:
    """Get a note page by ID."""
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.put("/{page_id}", response_model=NotePageResponse)
async def update_page(
    page_id: str,
    page_data: NotePageUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> NotePage:
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
        setattr(page, field, value)

    page.updated_at = datetime.utcnow()
    session.add(page)
    session.commit()
    session.refresh(page)

    # Rebuild wikilinks if body_markdown was updated
    if "body_markdown" in update_data:
        rebuild_wikilinks_for_page(session, page.id)

    return page


@router.delete("/{page_id}", status_code=204)
async def delete_page(
    page_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    """Delete a note page."""
    page = session.get(NotePage, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    session.delete(page)
    session.commit()
