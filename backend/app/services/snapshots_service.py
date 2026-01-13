"""Snapshots management service."""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import MapAsset, Snapshot, TerritoryTile
from app.repositories import SnapshotRepository


class SnapshotsService:
    """Service for managing snapshots."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.snapshot_repo = SnapshotRepository(session)

    def list_snapshots(self) -> tuple[list[Snapshot], str | None]:
        """
        List all snapshots and get active snapshot ID.

        Returns:
            Tuple of (list of snapshots, active_snapshot_id or None)
        """
        snapshots = self.snapshot_repo.list_all()
        active = self.snapshot_repo.get_active()
        active_id = active.snapshot_id if active else None
        return snapshots, active_id

    def create_snapshot(
        self,
        world_id: str,
        at_date: datetime,
        label: str,
        clone_from: str | None = None,
    ) -> Snapshot:
        """
        Create a new snapshot.

        Args:
            world_id: ID of the world
            at_date: Date/time of the snapshot
            label: Human-readable label
            clone_from: Optional snapshot ID to clone data from

        Returns:
            Created snapshot
        """
        snapshot = Snapshot(
            id=str(uuid.uuid4()),
            world_id=world_id,
            at_date=at_date,
            label=label,
        )
        self.snapshot_repo.create(snapshot)

        # Clone data from source snapshot if specified
        if clone_from:
            self._clone_snapshot_data(source_id=clone_from, target_id=snapshot.id)

        # If this is the first snapshot, make it active
        if not self.snapshot_repo.get_active():
            self.snapshot_repo.set_active(snapshot.id)

        return snapshot

    def _clone_snapshot_data(self, source_id: str, target_id: str) -> None:
        """
        Clone snapshot-specific data from source to target snapshot.

        Clones:
        - Territory tiles (all factions/coordinates)
        - Map asset (base map image)

        Args:
            source_id: Source snapshot ID
            target_id: Target snapshot ID
        """
        # Verify source snapshot exists
        source_snapshot = self.snapshot_repo.get_by_id(source_id)
        if not source_snapshot:
            raise ValueError(f"Source snapshot {source_id} not found")

        # Clone territory tiles
        source_tiles = (
            self.session.query(TerritoryTile)
            .filter(TerritoryTile.snapshot_id == source_id)
            .all()
        )

        for source_tile in source_tiles:
            cloned_tile = TerritoryTile(
                id=str(uuid.uuid4()),
                snapshot_id=target_id,
                faction_id=source_tile.faction_id,
                z=source_tile.z,
                x=source_tile.x,
                y=source_tile.y,
                tile_data=source_tile.tile_data,  # Copy binary data
            )
            self.session.add(cloned_tile)

        # Clone map asset if exists
        source_map = (
            self.session.query(MapAsset)
            .filter(MapAsset.snapshot_id == source_id)
            .first()
        )

        if source_map:
            cloned_map = MapAsset(
                id=str(uuid.uuid4()),
                snapshot_id=target_id,
                image_blob=source_map.image_blob,  # Copy binary data
                width=source_map.width,
                height=source_map.height,
            )
            self.session.add(cloned_map)

    def set_active_snapshot(self, snapshot_id: str) -> None:
        """
        Set the active snapshot.

        Args:
            snapshot_id: ID of snapshot to make active

        Raises:
            ValueError: If snapshot doesn't exist
        """
        snapshot = self.snapshot_repo.get_by_id(snapshot_id)
        if not snapshot:
            raise ValueError("Snapshot not found")

        self.snapshot_repo.set_active(snapshot_id)

    def delete_snapshot(self, snapshot_id: str) -> None:
        """
        Delete a snapshot.

        Args:
            snapshot_id: ID of snapshot to delete

        Raises:
            ValueError: If snapshot doesn't exist
        """
        snapshot = self.snapshot_repo.get_by_id(snapshot_id)
        if not snapshot:
            raise ValueError("Snapshot not found")

        # Check if it's the active snapshot
        active = self.snapshot_repo.get_active()
        if active and active.snapshot_id == snapshot_id:
            # Switch to another snapshot or delete active record
            remaining = [
                s for s in self.snapshot_repo.list_all()
                if s.id != snapshot_id
            ]
            if remaining:
                # Switch to first remaining snapshot
                self.snapshot_repo.set_active(remaining[0].id)
            else:
                # This is the last snapshot, delete the active record
                self.snapshot_repo.delete_active()

        self.snapshot_repo.delete(snapshot)
