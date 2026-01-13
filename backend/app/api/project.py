"""Project initialization API endpoints."""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import get_session
from app.services.project_service import ProjectService

router = APIRouter(prefix="/project", tags=["project"])


class ProjectInitRequest(BaseModel):
    """Schema for project initialization request."""

    world_name: str = Field(default="Doskvol", min_length=1, max_length=100)
    description: str | None = None
    timezone: str = Field(default="UTC", min_length=1)
    initial_snapshot_date: datetime | None = None
    initial_snapshot_label: str = Field(default="Initial", min_length=1, max_length=100)


class WorldResponse(BaseModel):
    """Schema for world response."""

    id: str
    name: str
    description: str | None
    timezone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class SnapshotResponse(BaseModel):
    """Schema for snapshot response."""

    id: str
    at_date: datetime
    label: str
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class ProjectInitResponse(BaseModel):
    """Schema for project initialization response."""

    world: WorldResponse
    initial_snapshot: SnapshotResponse


@router.post("/init", response_model=ProjectInitResponse, status_code=201)
async def init_project(
    request: ProjectInitRequest,
    session: Annotated[Session, Depends(get_session)],
) -> ProjectInitResponse:
    """
    Initialize a new project with World and initial Snapshot.

    This endpoint must be called before using any other CRUD endpoints.

    Args:
        request: Project initialization parameters
        session: Database session

    Returns:
        Created world and initial snapshot

    Raises:
        409: If project is already initialized
    """
    project_service = ProjectService(session)

    try:
        world, snapshot = project_service.init_project(
            world_name=request.world_name,
            description=request.description,
            timezone=request.timezone,
            initial_snapshot_date=request.initial_snapshot_date,
            initial_snapshot_label=request.initial_snapshot_label,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

    return ProjectInitResponse(
        world=WorldResponse.model_validate(world),
        initial_snapshot=SnapshotResponse.model_validate(snapshot),
    )
