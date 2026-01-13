"""Places API endpoints."""

import json
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import Place
from app.schemas import PlaceCreate, PlaceResponse, PlaceUpdate

router = APIRouter(prefix="/places", tags=["places"])


@router.get("", response_model=list[PlaceResponse])
async def list_places(
    session: Annotated[Session, Depends(get_session)],
) -> list[dict[str, str | dict[str, float] | datetime | None]]:
    """List all places."""
    places = session.exec(select(Place)).all()
    # Convert JSON strings to dicts for response
    return [
        {
            **place.model_dump(),
            "position": json.loads(place.position) if place.position else None,
        }
        for place in places
    ]


@router.post("", response_model=PlaceResponse, status_code=201)
async def create_place(
    place_data: PlaceCreate,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | dict[str, float] | datetime | None]:
    """Create a new place."""
    place = Place(
        id=str(uuid.uuid4()),
        name=place_data.name,
        type=place_data.type,
        position=json.dumps(place_data.position) if place_data.position else None,
        owner_faction_id=place_data.owner_faction_id,
        notes_public=place_data.notes_public,
        notes_gm=place_data.notes_gm,
    )
    session.add(place)
    session.commit()
    session.refresh(place)

    return {
        **place.model_dump(),
        "position": json.loads(place.position) if place.position else None,
    }


@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(
    place_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | dict[str, float] | datetime | None]:
    """Get a place by ID."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return {
        **place.model_dump(),
        "position": json.loads(place.position) if place.position else None,
    }


@router.put("/{place_id}", response_model=PlaceResponse)
async def update_place(
    place_id: str,
    place_data: PlaceUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | dict[str, float] | datetime | None]:
    """Update a place."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Update only provided fields
    update_data = place_data.model_dump(exclude_unset=True)
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
        **place.model_dump(),
        "position": json.loads(place.position) if place.position else None,
    }


@router.delete("/{place_id}", status_code=204)
async def delete_place(
    place_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    """Delete a place."""
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    session.delete(place)
    session.commit()
