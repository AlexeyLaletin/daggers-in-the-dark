"""Snapshots API endpoints."""

import uuid
from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models import ActiveSnapshot, Snapshot

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


class SnapshotCreate(BaseModel):
    """Schema for creating a snapshot."""

    at_date: datetime
    label: str
    clone_from: Optional[str] = None  # snapshot_id to clone from


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
    active_snapshot_id: Optional[str] = None


@router.get("", response_model=SnapshotsListResponse)
async def list_snapshots(
    session: Annotated[Session, Depends(get_session)],
) -> SnapshotsListResponse:
    """List all snapshots."""
    snapshots = session.exec(select(Snapshot).order_by(Snapshot.at_date)).all()

    # Get active snapshot
    active = session.exec(select(ActiveSnapshot)).first()
    active_id = active.snapshot_id if active else None

    return SnapshotsListResponse(
        snapshots=[SnapshotResponse.model_validate(s) for s in snapshots],
        active_snapshot_id=active_id,
    )


@router.post("", response_model=SnapshotResponse, status_code=201)
async def create_snapshot(
    snapshot_data: SnapshotCreate,
    session: Annotated[Session, Depends(get_session)],
) -> Snapshot:
    """Create a new snapshot."""
    snapshot = Snapshot(
        id=str(uuid.uuid4()),
        at_date=snapshot_data.at_date,
        label=snapshot_data.label,
    )
    session.add(snapshot)

    # If this is the first snapshot, make it active
    active = session.exec(select(ActiveSnapshot)).first()
    if not active:
        active = ActiveSnapshot(id="1", snapshot_id=snapshot.id)
        session.add(active)

    session.commit()
    session.refresh(snapshot)

    # TODO: If clone_from is provided, clone territory tiles and other snapshot-specific data
    # This will be implemented when tiles API is done

    return snapshot


@router.get("/{snapshot_id}", response_model=SnapshotResponse)
async def get_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> Snapshot:
    """Get a snapshot by ID."""
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snapshot


@router.put("/active/{snapshot_id}", status_code=200)
async def set_active_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    """Set the active snapshot."""
    # Check if snapshot exists
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Update or create active snapshot record
    active = session.exec(select(ActiveSnapshot)).first()
    if active:
        active.snapshot_id = snapshot_id
    else:
        active = ActiveSnapshot(id="1", snapshot_id=snapshot_id)
        session.add(active)

    session.commit()

    return {"status": "ok", "active_snapshot_id": snapshot_id}


@router.delete("/{snapshot_id}", status_code=204)
async def delete_snapshot(
    snapshot_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    """Delete a snapshot."""
    snapshot = session.get(Snapshot, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Check if it's the active snapshot
    active = session.exec(select(ActiveSnapshot)).first()
    if active and active.snapshot_id == snapshot_id:
        # Cannot delete active snapshot, or switch to another one first
        remaining = session.exec(
            select(Snapshot).where(Snapshot.id != snapshot_id)
        ).first()
        if remaining:
            # Switch to another snapshot
            active.snapshot_id = remaining.id
        else:
            # This is the last snapshot, delete the active record too
            session.delete(active)

    session.delete(snapshot)
    session.commit()
