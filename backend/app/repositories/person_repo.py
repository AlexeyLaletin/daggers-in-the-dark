"""Person repository."""


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Person


class PersonRepository:
    """Repository for Person entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, person_id: str) -> Person | None:
        """Get person by ID."""
        return self.session.get(Person, person_id)

    def list_all(self) -> list[Person]:
        """List all people."""
        return list(self.session.execute(select(Person)).scalars().all())

    def create(self, person: Person) -> Person:
        """Create a new person."""
        self.session.add(person)
        self.session.flush()
        return person

    def update(self, person: Person) -> Person:
        """Update a person."""
        self.session.add(person)
        self.session.flush()
        return person

    def delete(self, person: Person) -> None:
        """Delete a person."""
        self.session.delete(person)
        self.session.flush()
