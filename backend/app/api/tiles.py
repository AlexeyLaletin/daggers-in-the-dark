"""Territory tiles API endpoints."""

import base64
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlmodel import Session, and_, select

from app.db import get_session
from app.models import Faction, Snapshot, TerritoryTile

router = APIRouter(prefix="/snapshots", tags=["tiles"])


class TileBatchItem(BaseModel):
    """Single tile in a batch upload."""

    z: int  # zoom level
    x: int  # tile x coordinate
    y: int  # tile y coordinate
    data: str  # base64-encoded PNG/WebP


class TileBatchUpload(BaseModel):
    """Batch upload of territory tiles."""

    faction_id: str
    tiles: list[TileBatchItem]


@router.get("/{snapshot_id}/territory/tiles")
async def get_tile(
    snapshot_id: str,
    faction_id: Annotated[str, Query()],
    z: Annotated[int, Query()],
    x: Annotated[int, Query()],
    y: Annotated[int, Query()],
    session: Annotated[Session, Depends(get_session)],
) -> Response:
    """
    Get a specific territory tile.

    Returns PNG/WebP image data.
    """
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Check if faction exists
    faction = session.get(Faction, faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    # Get tile
    tile = session.exec(
        select(TerritoryTile).where(
            and_(
                TerritoryTile.snapshot_id == snapshot_id,
                TerritoryTile.faction_id == faction_id,
                TerritoryTile.z == z,
                TerritoryTile.x == x,
                TerritoryTile.y == y,
            )
        )
    ).first()

    if not tile:
        # Return 404 for missing tiles (frontend will treat as empty)
        raise HTTPException(status_code=404, detail="Tile not found")

    return Response(content=tile.tile_data, media_type="image/png")


@router.put("/{snapshot_id}/territory/tiles/batch")
async def upload_tiles_batch(
    snapshot_id: str,
    batch: TileBatchUpload,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, int | str]:
    """
    Upload a batch of territory tiles.

    Idempotent: replaces existing tiles at same coordinates.
    """
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Check if faction exists
    faction = session.get(Faction, batch.faction_id)
    if not faction:
        raise HTTPException(status_code=404, detail="Faction not found")

    uploaded_count = 0

    for tile_item in batch.tiles:
        # Decode base64 data
        try:
            tile_data = base64.b64decode(tile_item.data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid base64 data for tile z={tile_item.z} x={tile_item.x} y={tile_item.y}: {e}",
            )

        # Check if tile already exists (upsert logic)
        existing = session.exec(
            select(TerritoryTile).where(
                and_(
                    TerritoryTile.snapshot_id == snapshot_id,
                    TerritoryTile.faction_id == batch.faction_id,
                    TerritoryTile.z == tile_item.z,
                    TerritoryTile.x == tile_item.x,
                    TerritoryTile.y == tile_item.y,
                )
            )
        ).first()

        if existing:
            # Update existing tile
            existing.tile_data = tile_data
            session.add(existing)
        else:
            # Create new tile
            new_tile = TerritoryTile(
                id=str(uuid.uuid4()),
                snapshot_id=snapshot_id,
                faction_id=batch.faction_id,
                z=tile_item.z,
                x=tile_item.x,
                y=tile_item.y,
                tile_data=tile_data,
            )
            session.add(new_tile)

        uploaded_count += 1

    session.commit()

    return {
        "status": "ok",
        "uploaded": uploaded_count,
        "snapshot_id": snapshot_id,
        "faction_id": batch.faction_id,
    }


@router.delete("/{snapshot_id}/territory/tiles")
async def delete_tiles(
    snapshot_id: str,
    faction_id: Annotated[str, Query()],
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str | int]:
    """Delete all tiles for a faction in a snapshot."""
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Delete all tiles
    tiles = session.exec(
        select(TerritoryTile).where(
            and_(
                TerritoryTile.snapshot_id == snapshot_id,
                TerritoryTile.faction_id == faction_id,
            )
        )
    ).all()

    deleted_count = len(tiles)
    for tile in tiles:
        session.delete(tile)

    session.commit()

    return {"status": "ok", "deleted": deleted_count}
