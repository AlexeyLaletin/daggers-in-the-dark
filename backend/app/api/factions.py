"""Factions API endpoints."""

import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Faction, World
from app.schemas import FactionCreate, FactionResponse, FactionUpdate


def get_default_world_id(session: Session) -> str:
    """Get the default world ID (first world in DB)."""
    world = session.execute(select(World)).scalars().first()
    if not world:
        raise HTTPException(status_code=500, detail="No world found in database")
    return world.id

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("", response_model=list[FactionResponse])
async def list_factions(
    session: Annotated[Session, Depends(get_session)],
) -> list[Faction]:
    """List all factions."""
    factions = session.execute(select(Faction)).scalars().all()
    return list(factions)


@router.post("", response_model=FactionResponse, status_code=201)
async def create_faction(
    faction_data: FactionCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Faction:
    """Create a new faction."""
    world_id = get_default_world_id(session)
    faction = Faction(
        id=str(uuid.uuid4()),
        world_id=world_id,
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
) -> Faction:
    """Get a faction by ID."""
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")
    return faction


@router.put("/{faction_id}", response_model=FactionResponse)
async def update_faction(
    faction_id: str,
    faction_data: FactionUpdate,
    session: Annotated[Session, Depends(get_session)],
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
) -> None:
    """Delete a faction."""
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    session.delete(faction)
    session.commit()
