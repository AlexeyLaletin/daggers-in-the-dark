"""Snapshot repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ActiveSnapshot, Snapshot


class SnapshotRepository:
    """Repository for Snapshot and ActiveSnapshot entities."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, snapshot_id: str) -> Snapshot | None:
        """Get snapshot by ID."""
        return self.session.get(Snapshot, snapshot_id)

    def list_all(self) -> list[Snapshot]:
        """List all snapshots ordered by date."""
        return list(
            self.session.execute(select(Snapshot).order_by(Snapshot.at_date)).scalars().all()
        )

    def create(self, snapshot: Snapshot) -> Snapshot:
        """Create a new snapshot."""
        self.session.add(snapshot)
        self.session.flush()
        return snapshot

    def delete(self, snapshot: Snapshot) -> None:
        """Delete a snapshot."""
        self.session.delete(snapshot)
        self.session.flush()

    def get_active(self) -> ActiveSnapshot | None:
        """Get the active snapshot record."""
        return self.session.execute(select(ActiveSnapshot)).scalars().first()

    def set_active(self, snapshot_id: str) -> ActiveSnapshot:
        """Set the active snapshot."""
        active = self.get_active()
        if active:
            active.snapshot_id = snapshot_id
        else:
            active = ActiveSnapshot(id="1", snapshot_id=snapshot_id)
            self.session.add(active)
        self.session.flush()
        return active

    def delete_active(self) -> None:
        """Delete the active snapshot record."""
        active = self.get_active()
        if active:
            self.session.delete(active)
            self.session.flush()
