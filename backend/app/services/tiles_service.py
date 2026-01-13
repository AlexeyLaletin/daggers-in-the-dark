"""Territory tiles management service."""

import uuid

from sqlalchemy.orm import Session

from app.models import TerritoryTile
from app.repositories import TileRepository


class TileData:
    """Data class for tile upload."""

    def __init__(self, z: int, x: int, y: int, data: bytes) -> None:
        """Initialize tile data."""
        self.z = z
        self.x = x
        self.y = y
        self.data = data


class TilesService:
    """Service for managing territory tiles."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.tile_repo = TileRepository(session)

    def get_tile(
        self,
        snapshot_id: str,
        faction_id: str,
        z: int,
        x: int,
        y: int,
    ) -> TerritoryTile | None:
        """
        Get a specific tile.

        Args:
            snapshot_id: Snapshot ID
            faction_id: Faction ID
            z: Zoom level
            x: Tile X coordinate
            y: Tile Y coordinate

        Returns:
            TerritoryTile if found, None otherwise
        """
        return self.tile_repo.get_tile(snapshot_id, faction_id, z, x, y)

    def upload_tiles_batch(
        self,
        snapshot_id: str,
        faction_id: str,
        tiles: list[TileData],
    ) -> int:
        """
        Upload a batch of tiles (upsert).

        Args:
            snapshot_id: Snapshot ID
            faction_id: Faction ID
            tiles: List of tile data to upload

        Returns:
            Number of tiles uploaded
        """
        uploaded_count = 0

        for tile_data in tiles:
            # Check if tile already exists (upsert logic)
            existing = self.tile_repo.get_tile(
                snapshot_id, faction_id, tile_data.z, tile_data.x, tile_data.y
            )

            if existing:
                # Update existing tile
                existing.tile_data = tile_data.data
                self.tile_repo.update(existing)
            else:
                # Create new tile
                new_tile = TerritoryTile(
                    id=str(uuid.uuid4()),
                    snapshot_id=snapshot_id,
                    faction_id=faction_id,
                    z=tile_data.z,
                    x=tile_data.x,
                    y=tile_data.y,
                    tile_data=tile_data.data,
                )
                self.tile_repo.create(new_tile)

            uploaded_count += 1

        return uploaded_count

    def delete_tiles(self, snapshot_id: str, faction_id: str) -> int:
        """
        Delete all tiles for a faction in a snapshot.

        Args:
            snapshot_id: Snapshot ID
            faction_id: Faction ID

        Returns:
            Number of tiles deleted
        """
        return self.tile_repo.delete_all_for_faction_snapshot(snapshot_id, faction_id)
