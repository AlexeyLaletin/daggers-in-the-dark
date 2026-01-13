"""Factions API endpoints."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import get_view_mode, require_initialized_project
from app.models import Faction, World
from app.schemas import FactionCreate, FactionResponse, FactionUpdate
from app.services.visibility import ViewMode, VisibilityService

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("", response_model=list[FactionResponse])
async def list_factions(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> list[dict[str, object]]:
    """List all factions."""
    factions = session.execute(select(Faction)).scalars().all()
    visibility = VisibilityService()

    return [
        visibility.filter_notes_gm(
            {
                "id": f.id,
                "name": f.name,
                "color": f.color,
                "opacity": f.opacity,
                "notes_public": f.notes_public,
                "notes_gm": f.notes_gm,
                "created_at": f.created_at,
                "updated_at": f.updated_at,
            },
            view_mode
        )
        for f in factions
    ]


@router.post("", response_model=FactionResponse, status_code=201)
async def create_faction(
    faction_data: FactionCreate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> Faction:
    """Create a new faction."""
    faction = Faction(
        id=str(uuid.uuid4()),
        world_id=world.id,
        name=faction_data.name,
        color=faction_data.color,
        opacity=faction_data.opacity,
        notes_public=faction_data.notes_public,
        notes_gm=faction_data.notes_gm,
    )
    session.add(faction)
    session.commit()
    session.refresh(faction)
    return faction


@router.get("/{faction_id}", response_model=FactionResponse)
async def get_faction(
    faction_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> dict[str, object]:
    """Get a faction by ID."""
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    visibility = VisibilityService()
    return visibility.filter_notes_gm(
        {
            "id": faction.id,
            "name": faction.name,
            "color": faction.color,
            "opacity": faction.opacity,
            "notes_public": faction.notes_public,
            "notes_gm": faction.notes_gm,
            "created_at": faction.created_at,
            "updated_at": faction.updated_at,
        },
        view_mode
    )


@router.put("/{faction_id}", response_model=FactionResponse)
async def update_faction(
    faction_id: str,
    faction_data: FactionUpdate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> Faction:
    """Update a faction."""
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    # Update only provided fields
    update_data = faction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faction, field, value)

    faction.updated_at = datetime.utcnow()
    session.add(faction)
    session.commit()
    session.refresh(faction)
    return faction


@router.delete("/{faction_id}", status_code=204)
async def delete_faction(
    faction_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> None:
    """Delete a faction."""
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    session.delete(faction)
    session.commit()
