"""Territory tile repository."""


from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import TerritoryTile


class TileRepository:
    """Repository for TerritoryTile entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_tile(
        self,
        snapshot_id: str,
        faction_id: str,
        z: int,
        x: int,
        y: int,
    ) -> TerritoryTile | None:
        """Get a specific tile."""
        return self.session.execute(
            select(TerritoryTile).where(
                and_(
                    TerritoryTile.snapshot_id == snapshot_id,
                    TerritoryTile.faction_id == faction_id,
                    TerritoryTile.z == z,
                    TerritoryTile.x == x,
                    TerritoryTile.y == y,
                )
            )
        ).scalars().first()

    def list_tiles_for_faction_snapshot(
        self, snapshot_id: str, faction_id: str
    ) -> list[TerritoryTile]:
        """List all tiles for a faction in a snapshot."""
        return list(
            self.session.execute(
                select(TerritoryTile).where(
                    and_(
                        TerritoryTile.snapshot_id == snapshot_id,
                        TerritoryTile.faction_id == faction_id,
                    )
                )
            ).scalars().all()
        )

    def create(self, tile: TerritoryTile) -> TerritoryTile:
        """Create a new tile."""
        self.session.add(tile)
        self.session.flush()
        return tile

    def update(self, tile: TerritoryTile) -> TerritoryTile:
        """Update a tile."""
        self.session.add(tile)
        self.session.flush()
        return tile

    def delete(self, tile: TerritoryTile) -> None:
        """Delete a tile."""
        self.session.delete(tile)
        self.session.flush()

    def delete_all_for_faction_snapshot(
        self, snapshot_id: str, faction_id: str
    ) -> int:
        """Delete all tiles for a faction in a snapshot. Returns count of deleted tiles."""
        tiles = self.list_tiles_for_faction_snapshot(snapshot_id, faction_id)
        count = len(tiles)
        for tile in tiles:
            self.session.delete(tile)
        self.session.flush()
        return count
