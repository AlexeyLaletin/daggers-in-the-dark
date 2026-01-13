"""World repository."""


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import World


class WorldRepository:
    """Repository for World entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_first(self) -> World | None:
        """Get the first (and typically only) world in the database."""
        return self.session.execute(select(World)).scalars().first()

    def get_by_id(self, world_id: str) -> World | None:
        """Get world by ID."""
        return self.session.get(World, world_id)

    def create(self, world: World) -> World:
        """Create a new world."""
        self.session.add(world)
        self.session.flush()
        return world

    def exists(self) -> bool:
        """Check if any world exists in the database."""
        return self.get_first() is not None
