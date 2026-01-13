"""Territory tiles API endpoints."""

import base64
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import require_initialized_project
from app.models import Faction, Snapshot, World
from app.services.tiles_service import TileData, TilesService

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
    world: Annotated[World, Depends(require_initialized_project)],
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
    tiles_service = TilesService(session)
    tile = tiles_service.get_tile(snapshot_id, faction_id, z, x, y)

    if not tile:
        # Return 404 for missing tiles (frontend will treat as empty)
        raise HTTPException(status_code=404, detail="Tile not found")

    return Response(content=tile.tile_data, media_type="image/png")


@router.put("/{snapshot_id}/territory/tiles/batch")
async def upload_tiles_batch(
    snapshot_id: str,
    batch: TileBatchUpload,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
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

    # Decode and prepare tile data
    tiles_data = []
    for tile_item in batch.tiles:
        try:
            tile_data = base64.b64decode(tile_item.data)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid base64 data for tile z={tile_item.z} x={tile_item.x} y={tile_item.y}: {e}",
            ) from e
        tiles_data.append(TileData(tile_item.z, tile_item.x, tile_item.y, tile_data))

    # Upload tiles
    tiles_service = TilesService(session)
    uploaded_count = tiles_service.upload_tiles_batch(
        snapshot_id,
        batch.faction_id,
        tiles_data,
    )
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
    world: Annotated[World, Depends(require_initialized_project)],
) -> dict[str, str | int]:
    """Delete all tiles for a faction in a snapshot."""
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Delete all tiles
    tiles_service = TilesService(session)
    deleted_count = tiles_service.delete_tiles(snapshot_id, faction_id)
    session.commit()

    return {"status": "ok", "deleted": deleted_count}
