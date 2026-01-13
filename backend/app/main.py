"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import export_import, factions, graph, pages, people, places, snapshots, tiles
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Initialize database on startup
    init_db()
    yield
    # Cleanup on shutdown (if needed)


app = FastAPI(
    title="Blades Faction Map API",
    description="Backend API for Blades in the Dark faction map and notes",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for local Electron renderer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(factions.router, prefix="/api")
app.include_router(people.router, prefix="/api")
app.include_router(places.router, prefix="/api")
app.include_router(pages.router, prefix="/api")
app.include_router(graph.router, prefix="/api")
app.include_router(snapshots.router, prefix="/api")
app.include_router(tiles.router, prefix="/api")
app.include_router(export_import.router, prefix="/api")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Blades Faction Map API"}
