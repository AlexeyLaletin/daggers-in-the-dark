"""Project initialization service."""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Snapshot, World
from app.repositories import SnapshotRepository, WorldRepository


class ProjectService:
    """Service for project initialization and management."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.world_repo = WorldRepository(session)
        self.snapshot_repo = SnapshotRepository(session)

    def is_initialized(self) -> bool:
        """Check if project is initialized (has a World)."""
        return self.world_repo.exists()

    def init_project(
        self,
        world_name: str = "Doskvol",
        description: str | None = None,
        timezone: str = "UTC",
        initial_snapshot_date: datetime | None = None,
        initial_snapshot_label: str = "Initial",
    ) -> tuple[World, Snapshot]:
        """
        Initialize a new project with World and initial Snapshot.

        Args:
            world_name: Name of the world/city
            description: Optional description
            timezone: Timezone for timeline
            initial_snapshot_date: Date for initial snapshot (defaults to 1847-01-01)
            initial_snapshot_label: Label for initial snapshot

        Returns:
            Tuple of (created World, created Snapshot)

        Raises:
            ValueError: If project is already initialized
        """
        if self.is_initialized():
            raise ValueError("Project already initialized")

        # Default epoch date for Blades in the Dark setting
        if initial_snapshot_date is None:
            initial_snapshot_date = datetime(1847, 1, 1, 0, 0, 0)

        # Create world
        world = World(
            id=str(uuid.uuid4()),
            name=world_name,
            description=description,
            timezone=timezone,
        )
        self.world_repo.create(world)

        # Create initial snapshot
        snapshot = Snapshot(
            id=str(uuid.uuid4()),
            world_id=world.id,
            at_date=initial_snapshot_date,
            label=initial_snapshot_label,
        )
        self.snapshot_repo.create(snapshot)

        # Set as active snapshot
        self.snapshot_repo.set_active(snapshot.id)

        # Commit transaction
        self.session.commit()

        return world, snapshot

    def require_initialized(self) -> World:
        """
        Get the world, raising an exception if project is not initialized.

        Returns:
            The World instance

        Raises:
            ValueError: If project is not initialized
        """
        world = self.world_repo.get_first()
        if not world:
            raise ValueError("Project not initialized. Call POST /api/project/init first")
        return world
