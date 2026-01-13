"""People API endpoints."""

import json
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import Person
from app.schemas import PersonCreate, PersonResponse, PersonUpdate

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[PersonResponse])
async def list_people(
    session: Annotated[Session, Depends(get_session)],
) -> list[dict[str, str | list[str] | datetime | None]]:
    """List all people."""
    people = session.exec(select(Person)).all()
    # Convert JSON strings to lists for response
    return [
        {
            **person.model_dump(),
            "aliases": json.loads(person.aliases) if person.aliases else [],
            "tags": json.loads(person.tags) if person.tags else [],
        }
        for person in people
    ]


@router.post("", response_model=PersonResponse, status_code=201)
async def create_person(
    person_data: PersonCreate,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | list[str] | datetime | None]:
    """Create a new person."""
    person = Person(
        id=str(uuid.uuid4()),
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
        **person.model_dump(),
        "aliases": json.loads(person.aliases) if person.aliases else [],
        "tags": json.loads(person.tags) if person.tags else [],
    }


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(
    person_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | list[str] | datetime | None]:
    """Get a person by ID."""
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return {
        **person.model_dump(),
        "aliases": json.loads(person.aliases) if person.aliases else [],
        "tags": json.loads(person.tags) if person.tags else [],
    }


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    person_data: PersonUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | list[str] | datetime | None]:
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
        **person.model_dump(),
        "aliases": json.loads(person.aliases) if person.aliases else [],
        "tags": json.loads(person.tags) if person.tags else [],
    }


@router.delete("/{person_id}", status_code=204)
async def delete_person(
    person_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    """Delete a person."""
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    session.delete(person)
    session.commit()
