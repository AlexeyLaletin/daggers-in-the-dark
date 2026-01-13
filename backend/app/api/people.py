"""People API endpoints."""

import json
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import get_view_mode, require_initialized_project
from app.models import Person, World
from app.schemas import PersonCreate, PersonResponse, PersonUpdate
from app.services.visibility import ViewMode, VisibilityService

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[PersonResponse])
async def list_people(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> list[dict[str, object]]:
    """List all people."""
    people = session.execute(select(Person)).scalars().all()
    visibility = VisibilityService()

    # Convert JSON strings to lists and apply visibility filter
    return [
        visibility.filter_notes_gm(
            {
                "id": p.id,
                "name": p.name,
                "aliases": json.loads(p.aliases) if p.aliases else [],
                "status": p.status,
                "workplace_place_id": p.workplace_place_id,
                "home_place_id": p.home_place_id,
                "tags": json.loads(p.tags) if p.tags else [],
                "notes_public": p.notes_public,
                "notes_gm": p.notes_gm,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            },
            view_mode,
        )
        for p in people
    ]


@router.post("", response_model=PersonResponse, status_code=201)
async def create_person(
    person_data: PersonCreate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> dict[str, object]:
    """Create a new person."""
    person = Person(
        id=str(uuid.uuid4()),
        world_id=world.id,
        name=person_data.name,
        aliases=json.dumps(person_data.aliases) if person_data.aliases else None,
        status=person_data.status,
        workplace_place_id=person_data.workplace_place_id,
        home_place_id=person_data.home_place_id,
        tags=json.dumps(person_data.tags) if person_data.tags else None,
        notes_public=person_data.notes_public,
        notes_gm=person_data.notes_gm,
    )
    session.add(person)
    session.commit()
    session.refresh(person)

    return {
        "id": person.id,
        "name": person.name,
        "aliases": json.loads(person.aliases) if person.aliases else [],
        "status": person.status,
        "workplace_place_id": person.workplace_place_id,
        "home_place_id": person.home_place_id,
        "tags": json.loads(person.tags) if person.tags else [],
        "notes_public": person.notes_public,
        "notes_gm": person.notes_gm,
        "created_at": person.created_at,
        "updated_at": person.updated_at,
    }


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    person_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
    view_mode: Annotated[ViewMode, Depends(get_view_mode)] = "gm",
) -> dict[str, object]:
    """Get a person by ID."""
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    visibility = VisibilityService()
    return visibility.filter_notes_gm(
        {
            "id": person.id,
            "name": person.name,
            "aliases": json.loads(person.aliases) if person.aliases else [],
            "status": person.status,
            "workplace_place_id": person.workplace_place_id,
            "home_place_id": person.home_place_id,
            "tags": json.loads(person.tags) if person.tags else [],
            "notes_public": person.notes_public,
            "notes_gm": person.notes_gm,
            "created_at": person.created_at,
            "updated_at": person.updated_at,
        },
        view_mode,
    )


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    person_data: PersonUpdate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> dict[str, object]:
    """Update a person."""
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Update only provided fields
    update_data = person_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "aliases" and value is not None:
            setattr(person, field, json.dumps(value))
        elif field == "tags" and value is not None:
            setattr(person, field, json.dumps(value))
        else:
            setattr(person, field, value)

    person.updated_at = datetime.utcnow()
    session.add(person)
    session.commit()
    session.refresh(person)

    return {
        "id": person.id,
        "name": person.name,
        "aliases": json.loads(person.aliases) if person.aliases else [],
        "status": person.status,
        "workplace_place_id": person.workplace_place_id,
        "home_place_id": person.home_place_id,
        "tags": json.loads(person.tags) if person.tags else [],
        "notes_public": person.notes_public,
        "notes_gm": person.notes_gm,
        "created_at": person.created_at,
        "updated_at": person.updated_at,
    }


@router.delete("/{person_id}", status_code=204)
async def delete_person(
    person_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> None:
    """Delete a person."""
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    session.delete(person)
    session.commit()
