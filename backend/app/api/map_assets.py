"""Map assets API endpoints for uploading and downloading base map images."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import require_initialized_project
from app.models import MapAsset, Snapshot, World

router = APIRouter(prefix="/snapshots", tags=["map_assets"])


@router.post("/{snapshot_id}/map", status_code=201)
async def upload_map(
    snapshot_id: str,
    file: Annotated[UploadFile, File()],
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> dict[str, str]:
    """
    Upload base map image for a snapshot.

    Replaces existing map if already present (1 map per snapshot).
    Accepts image files (PNG, JPEG, etc).
    """
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Validate file type
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Must be an image.",
        )

    # Read file content
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    # Get image dimensions (simplified - in production, use PIL/Pillow)
    # For MVP, we'll accept any image and store dimensions as 0,0
    width = 0
    height = 0

    # Check if map already exists for this snapshot
    existing_map = session.query(MapAsset).filter(MapAsset.snapshot_id == snapshot_id).first()

    if existing_map:
        # Update existing map
        existing_map.image_blob = content
        existing_map.width = width
        existing_map.height = height
        map_asset = existing_map
    else:
        # Create new map asset
        map_asset = MapAsset(
            id=str(uuid.uuid4()),
            snapshot_id=snapshot_id,
            image_blob=content,
            width=width,
            height=height,
        )
        session.add(map_asset)

    session.commit()

    return {
        "status": "ok",
        "message": "Map uploaded successfully",
        "map_asset_id": map_asset.id,
        "snapshot_id": snapshot_id,
    }


@router.get("/{snapshot_id}/map")
async def download_map(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> Response:
    """
    Download base map image for a snapshot.

    Returns the image file as binary data.
    """
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Get map asset
    map_asset = session.query(MapAsset).filter(MapAsset.snapshot_id == snapshot_id).first()

    if not map_asset:
        raise HTTPException(status_code=404, detail="Map not found for this snapshot")

    # Return image as binary response
    # Default to image/png, but could be detected from blob header
    return Response(content=map_asset.image_blob, media_type="image/png")


@router.delete("/{snapshot_id}/map", status_code=204)
async def delete_map(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> None:
    """Delete base map for a snapshot."""
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Get map asset
    map_asset = session.query(MapAsset).filter(MapAsset.snapshot_id == snapshot_id).first()

    if not map_asset:
        raise HTTPException(status_code=404, detail="Map not found for this snapshot")

    session.delete(map_asset)
    session.commit()
