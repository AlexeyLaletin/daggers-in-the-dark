"""Export/Import API endpoints."""

import shutil
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.db import DATABASE_PATH, engine, get_session, init_db

router = APIRouter(tags=["export"])


@router.get("/export")
async def export_project(
    session: Annotated[Session, Depends(get_session)],
) -> FileResponse:
    """
    Export the entire project as a SQLite database file.

    Returns the database file for download.
    """
    # Close all connections to allow file copy
    session.close()
    engine.dispose()

    if not DATABASE_PATH.exists():
        raise HTTPException(status_code=404, detail="No project to export")

    # Return the SQLite file
    return FileResponse(
        path=str(DATABASE_PATH),
        filename="blades_project.db",
        media_type="application/x-sqlite3",
    )


@router.post("/import", status_code=201)
async def import_project(
    file: UploadFile = File(...),
) -> dict[str, str]:
    """
    Import a project from a SQLite database file.

    Replaces the current project with the uploaded one.
    """
    if not file.filename or not file.filename.endswith(".db"):
        raise HTTPException(status_code=400, detail="File must be a .db SQLite database")

    try:
        # Backup current database if it exists
        if DATABASE_PATH.exists():
            backup_path = DATABASE_PATH.with_suffix(".db.backup")
            shutil.copy(DATABASE_PATH, backup_path)

        # Write uploaded file to database path
        with DATABASE_PATH.open("wb") as f:
            content = await file.read()
            f.write(content)

        # Reinitialize database connection
        init_db()

        return {"status": "ok", "message": "Project imported successfully"}

    except Exception as e:
        # Restore backup if import failed
        backup_path = DATABASE_PATH.with_suffix(".db.backup")
        if backup_path.exists():
            shutil.copy(backup_path, DATABASE_PATH)
            backup_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to import project: {str(e)}",
        )
