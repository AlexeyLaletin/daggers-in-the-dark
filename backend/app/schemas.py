"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Faction schemas
class FactionCreate(BaseModel):
    """Schema for creating a faction."""

    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    opacity: float = Field(default=0.4, ge=0.0, le=1.0)
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class FactionUpdate(BaseModel):
    """Schema for updating a faction."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    opacity: Optional[float] = Field(None, ge=0.0, le=1.0)
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class FactionResponse(BaseModel):
    """Schema for faction response."""

    id: str
    name: str
    color: str
    opacity: float
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# Person schemas
class PersonCreate(BaseModel):
    """Schema for creating a person."""

    name: str = Field(..., min_length=1, max_length=100)
    aliases: Optional[list[str]] = None
    status: str = Field(default="alive")
    workplace_place_id: Optional[str] = None
    home_place_id: Optional[str] = None
    tags: Optional[list[str]] = None
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class PersonUpdate(BaseModel):
    """Schema for updating a person."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    aliases: Optional[list[str]] = None
    status: Optional[str] = None
    workplace_place_id: Optional[str] = None
    home_place_id: Optional[str] = None
    tags: Optional[list[str]] = None
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class PersonResponse(BaseModel):
    """Schema for person response."""

    id: str
    name: str
    aliases: list[str]
    status: str
    workplace_place_id: Optional[str] = None
    home_place_id: Optional[str] = None
    tags: list[str]
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# Place schemas
class PlaceCreate(BaseModel):
    """Schema for creating a place."""

    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., pattern=r"^(building|district|landmark|other)$")
    position: Optional[dict[str, float]] = None
    owner_faction_id: Optional[str] = None
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class PlaceUpdate(BaseModel):
    """Schema for updating a place."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, pattern=r"^(building|district|landmark|other)$")
    position: Optional[dict[str, float]] = None
    owner_faction_id: Optional[str] = None
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None


class PlaceResponse(BaseModel):
    """Schema for place response."""

    id: str
    name: str
    type: str
    position: Optional[dict[str, float]] = None
    owner_faction_id: Optional[str] = None
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# NotePage schemas
class NotePageCreate(BaseModel):
    """Schema for creating a note page."""

    title: str = Field(..., min_length=1, max_length=200)
    body_markdown: str
    visibility: str = Field(default="public", pattern=r"^(public|gm)$")
    entity_type: Optional[str] = Field(None, pattern=r"^(faction|person|place)$")
    entity_id: Optional[str] = None


class NotePageUpdate(BaseModel):
    """Schema for updating a note page."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body_markdown: Optional[str] = None
    visibility: Optional[str] = Field(None, pattern=r"^(public|gm)$")
    entity_type: Optional[str] = Field(None, pattern=r"^(faction|person|place)$")
    entity_id: Optional[str] = None


class NotePageResponse(BaseModel):
    """Schema for note page response."""

    id: str
    title: str
    body_markdown: str
    visibility: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
