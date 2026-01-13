"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


# Faction schemas
class FactionCreate(BaseModel):
    """Schema for creating a faction."""

    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    opacity: float = Field(default=0.4, ge=0.0, le=1.0)
    notes_public: str | None = None
    notes_gm: str | None = None


class FactionUpdate(BaseModel):
    """Schema for updating a faction."""

    name: str | None = Field(None, min_length=1, max_length=100)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    opacity: float | None = Field(None, ge=0.0, le=1.0)
    notes_public: str | None = None
    notes_gm: str | None = None


class FactionResponse(BaseModel):
    """Schema for faction response."""

    id: str
    name: str
    color: str
    opacity: float
    notes_public: str | None = None
    notes_gm: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# Person schemas
class PersonCreate(BaseModel):
    """Schema for creating a person."""

    name: str = Field(..., min_length=1, max_length=100)
    aliases: list[str] | None = None
    status: str = Field(default="alive")
    workplace_place_id: str | None = None
    home_place_id: str | None = None
    tags: list[str] | None = None
    notes_public: str | None = None
    notes_gm: str | None = None


class PersonUpdate(BaseModel):
    """Schema for updating a person."""

    name: str | None = Field(None, min_length=1, max_length=100)
    aliases: list[str] | None = None
    status: str | None = None
    workplace_place_id: str | None = None
    home_place_id: str | None = None
    tags: list[str] | None = None
    notes_public: str | None = None
    notes_gm: str | None = None


class PersonResponse(BaseModel):
    """Schema for person response."""

    id: str
    name: str
    aliases: list[str]
    status: str
    workplace_place_id: str | None = None
    home_place_id: str | None = None
    tags: list[str]
    notes_public: str | None = None
    notes_gm: str | None = None
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
    position: dict[str, float] | None = None
    owner_faction_id: str | None = None
    scope: str = Field(default="public", pattern=r"^(public|gm|player)$")
    notes_public: str | None = None
    notes_gm: str | None = None


class PlaceUpdate(BaseModel):
    """Schema for updating a place."""

    name: str | None = Field(None, min_length=1, max_length=100)
    type: str | None = Field(None, pattern=r"^(building|district|landmark|other)$")
    position: dict[str, float] | None = None
    owner_faction_id: str | None = None
    scope: str | None = Field(None, pattern=r"^(public|gm|player)$")
    notes_public: str | None = None
    notes_gm: str | None = None


class PlaceResponse(BaseModel):
    """Schema for place response."""

    id: str
    name: str
    type: str
    position: dict[str, float] | None = None
    owner_faction_id: str | None = None
    scope: str
    notes_public: str | None = None
    notes_gm: str | None = None
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
    visibility: str = Field(default="public", pattern=r"^(public|gm|player)$")
    entity_type: str | None = Field(None, pattern=r"^(faction|person|place)$")
    entity_id: str | None = None


class NotePageUpdate(BaseModel):
    """Schema for updating a note page."""

    title: str | None = Field(None, min_length=1, max_length=200)
    body_markdown: str | None = None
    visibility: str | None = Field(None, pattern=r"^(public|gm|player)$")
    entity_type: str | None = Field(None, pattern=r"^(faction|person|place)$")
    entity_id: str | None = None


class NotePageResponse(BaseModel):
    """Schema for note page response."""

    id: str
    title: str
    body_markdown: str
    visibility: str  # API uses 'visibility', but model uses 'scope'
    entity_type: str | None = None
    entity_id: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True

    @classmethod
    def from_orm(cls, obj: object) -> "NotePageResponse":
        """Custom from_orm to map scope to visibility."""
        from app.models import NotePage

        if not isinstance(obj, NotePage):
            raise TypeError("Expected NotePage instance")

        return cls(
            id=obj.id,
            title=obj.title,
            body_markdown=obj.body_markdown,
            visibility=obj.scope,  # Map scope to visibility
            entity_type=obj.entity_type,
            entity_id=obj.entity_id,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )
