"""Places API endpoints."""

import json
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import get_view_mode, require_initialized_project
from app.models import Place, World
from app.schemas import PlaceCreate, PlaceResponse, PlaceUpdate
from app.services.visibility import ViewMode, VisibilityService

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=list[PlaceResponse])
async def list_places(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> list[dict[str, object]]:
    """List all places."""
    places = session.execute(select(Place)).scalars().all()
    visibility = VisibilityService()

    # Filter by scope and convert JSON strings to dicts
    return [
        visibility.filter_notes_gm(
            {
                "id": p.id,
                "name": p.name,
                "type": p.type,
                "position": json.loads(p.position) if p.position else None,
                "owner_faction_id": p.owner_faction_id,
                "scope": p.scope,
                "notes_public": p.notes_public,
                "notes_gm": p.notes_gm,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            },
            view_mode,
        )
        for p in places
        if visibility.filter_scope(p.scope, view_mode)
    ]


@router.post("", response_model=PlaceResponse, status_code=201)
async def create_place(
    place_data: PlaceCreate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> dict[str, object]:
    """Create a new place."""
    # Player-mode restrictions: force public scope and block gm notes
    if view_mode == "player":
        scope = "public"
        notes_gm = None
    else:
        scope = place_data.scope
        notes_gm = place_data.notes_gm

    place = Place(
        id=str(uuid.uuid4()),
        world_id=world.id,
        name=place_data.name,
        type=place_data.type,
        position=json.dumps(place_data.position) if place_data.position else None,
        owner_faction_id=place_data.owner_faction_id,
        scope=scope,
        notes_public=place_data.notes_public,
        notes_gm=notes_gm,
    )
    session.add(place)
    session.commit()
    session.refresh(place)

    return {
        "id": place.id,
        "name": place.name,
        "type": place.type,
        "position": json.loads(place.position) if place.position else None,
        "owner_faction_id": place.owner_faction_id,
        "scope": place.scope,
        "notes_public": place.notes_public,
        "notes_gm": place.notes_gm,
        "created_at": place.created_at,
        "updated_at": place.updated_at,
    }


@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(
    place_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> dict[str, object]:
    """Get a place by ID."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Check scope visibility
    visibility = VisibilityService()
    if not visibility.filter_scope(place.scope, view_mode):
        raise HTTPException(status_code=404, detail="Place not found")

    return visibility.filter_notes_gm(
        {
            "id": place.id,
            "name": place.name,
            "type": place.type,
            "position": json.loads(place.position) if place.position else None,
            "owner_faction_id": place.owner_faction_id,
            "scope": place.scope,
            "notes_public": place.notes_public,
            "notes_gm": place.notes_gm,
            "created_at": place.created_at,
            "updated_at": place.updated_at,
        },
        view_mode,
    )


@router.put("/{place_id}", response_model=PlaceResponse)
async def update_place(
    place_id: str,
    place_data: PlaceUpdate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> dict[str, object]:
    """Update a place."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Update only provided fields
    update_data = place_data.model_dump(exclude_unset=True)

    # Player-mode restrictions: forbid scope changes and notes_gm edits
    if view_mode == "player":
        update_data.pop("scope", None)  # Ignore scope changes in player mode
        update_data.pop("notes_gm", None)  # Ignore gm notes in player mode

    for field, value in update_data.items():
        if field == "position" and value is not None:
            setattr(place, field, json.dumps(value))
        else:
            setattr(place, field, value)

    place.updated_at = datetime.utcnow()
    session.add(place)
    session.commit()
    session.refresh(place)

    return {
        "id": place.id,
        "name": place.name,
        "type": place.type,
        "position": json.loads(place.position) if place.position else None,
        "owner_faction_id": place.owner_faction_id,
        "scope": place.scope,
        "notes_public": place.notes_public,
        "notes_gm": place.notes_gm,
        "created_at": place.created_at,
        "updated_at": place.updated_at,
    }


@router.delete("/{place_id}", status_code=204)
async def delete_place(
    place_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> None:
    """Delete a place."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Check scope visibility (prevent deleting gm-places in player mode)
    visibility = VisibilityService()
    if not visibility.filter_scope(place.scope, view_mode):
        raise HTTPException(status_code=404, detail="Place not found")

    session.delete(place)
    session.commit()
