"""Snapshots API endpoints."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_session
from app.dependencies import require_initialized_project
from app.models import World
from app.services.snapshots_service import SnapshotsService

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


class SnapshotCreate(BaseModel):
    """Schema for creating a snapshot."""

    at_date: datetime
    label: str
    clone_from: str | None = None  # snapshot_id to clone from


class SnapshotResponse(BaseModel):
    """Schema for snapshot response."""

    id: str
    at_date: datetime
    label: str
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class SnapshotsListResponse(BaseModel):
    """Schema for snapshots list response."""

    snapshots: list[SnapshotResponse]
    active_snapshot_id: str | None = None


@router.get("", response_model=SnapshotsListResponse)
async def list_snapshots(
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> SnapshotsListResponse:
    """List all snapshots."""
    snapshots_service = SnapshotsService(session)
    snapshots, active_id = snapshots_service.list_snapshots()

    return SnapshotsListResponse(
        snapshots=[SnapshotResponse.model_validate(s) for s in snapshots],
        active_snapshot_id=active_id,
    )


@router.post("", response_model=SnapshotResponse, status_code=201)
async def create_snapshot(
    snapshot_data: SnapshotCreate,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> SnapshotResponse:
    """Create a new snapshot, optionally cloning data from another snapshot."""
    snapshots_service = SnapshotsService(session)
    try:
        snapshot = snapshots_service.create_snapshot(
            world_id=world.id,
            at_date=snapshot_data.at_date,
            label=snapshot_data.label,
            clone_from=snapshot_data.clone_from,
        )
        session.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return SnapshotResponse.model_validate(snapshot)


@router.get("/{snapshot_id}", response_model=SnapshotResponse)
async def get_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> SnapshotResponse:
    """Get a snapshot by ID."""
    from app.models import Snapshot

    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return SnapshotResponse.model_validate(snapshot)


@router.put("/active/{snapshot_id}", status_code=200)
async def set_active_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> dict[str, str]:
    """Set the active snapshot."""
    snapshots_service = SnapshotsService(session)
    try:
        snapshots_service.set_active_snapshot(snapshot_id)
        session.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return {"status": "ok", "active_snapshot_id": snapshot_id}


@router.delete("/{snapshot_id}", status_code=204)
async def delete_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
    world: Annotated[World, Depends(require_initialized_project)],
) -> None:
    """Delete a snapshot."""
    snapshots_service = SnapshotsService(session)
    try:
        snapshots_service.delete_snapshot(snapshot_id)
        session.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
