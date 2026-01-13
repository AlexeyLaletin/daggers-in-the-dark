"""Faction repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Faction


class FactionRepository:
    """Repository for Faction entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, faction_id: str) -> Faction | None:
        """Get faction by ID."""
        return self.session.get(Faction, faction_id)

    def list_all(self) -> list[Faction]:
        """List all factions."""
        return list(self.session.execute(select(Faction)).scalars().all())

    def create(self, faction: Faction) -> Faction:
        """Create a new faction."""
        self.session.add(faction)
        self.session.flush()
        return faction

    def update(self, faction: Faction) -> Faction:
        """Update a faction."""
        self.session.add(faction)
        self.session.flush()
        return faction

    def delete(self, faction: Faction) -> None:
        """Delete a faction."""
        self.session.delete(faction)
        self.session.flush()
