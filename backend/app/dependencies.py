"""FastAPI dependencies for API routes."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import World
from app.services.project_service import ProjectService
from app.services.visibility import ViewMode


def get_view_mode(x_view_mode: Annotated[str, Header(alias="X-View-Mode")] = "gm") -> ViewMode:
    """
    Get view mode from request header.

    Args:
        x_view_mode: View mode header value

    Returns:
        ViewMode enum value (gm or player)
    """
    if x_view_mode.lower() == "player":
        return "player"
    return "gm"


def require_initialized_project(session: Annotated[Session, Depends(get_session)]) -> World:
    """
    Dependency that ensures project is initialized.

    Args:
        session: Database session

    Returns:
        The World instance

    Raises:
        HTTPException(409): If project is not initialized
    """
    project_service = ProjectService(session)
    try:
        return project_service.require_initialized()
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
