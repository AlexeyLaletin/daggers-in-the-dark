"""Place repository."""


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Place


class PlaceRepository:
    """Repository for Place entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, place_id: str) -> Place | None:
        """Get place by ID."""
        return self.session.get(Place, place_id)

    def list_all(self) -> list[Place]:
        """List all places."""
        return list(self.session.execute(select(Place)).scalars().all())

    def create(self, place: Place) -> Place:
        """Create a new place."""
        self.session.add(place)
        self.session.flush()
        return place

    def update(self, place: Place) -> Place:
        """Update a place."""
        self.session.add(place)
        self.session.flush()
        return place

    def delete(self, place: Place) -> None:
        """Delete a place."""
        self.session.delete(place)
        self.session.flush()
