"""SQLModel database models."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Faction(SQLModel, table=True):
    """Faction model."""

    __tablename__ = "factions"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    color: str  # hex #RRGGBB
    opacity: float = Field(default=0.4)
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Person(SQLModel, table=True):
    """Person model."""

    __tablename__ = "people"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    aliases: Optional[str] = None  # JSON string of array
    status: str = Field(default="alive")  # alive|dead|unknown
    workplace_place_id: Optional[str] = Field(default=None, foreign_key="places.id")
    home_place_id: Optional[str] = Field(default=None, foreign_key="places.id")
    tags: Optional[str] = None  # JSON string of array
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class FactionMembership(SQLModel, table=True):
    """Many-to-many relationship between Person and Faction."""

    __tablename__ = "faction_memberships"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    person_id: str = Field(foreign_key="people.id", index=True)
    faction_id: str = Field(foreign_key="factions.id", index=True)
    role: Optional[str] = None


class Place(SQLModel, table=True):
    """Place model."""

    __tablename__ = "places"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    type: str  # building|district|landmark|other
    position: Optional[str] = None  # JSON {x, y}
    owner_faction_id: Optional[str] = Field(default=None, foreign_key="factions.id")
    notes_public: Optional[str] = None
    notes_gm: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class NotePage(SQLModel, table=True):
    """Note page model (Obsidian-like pages)."""

    __tablename__ = "note_pages"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    title: str = Field(unique=True, index=True)
    body_markdown: str
    visibility: str = Field(default="public")  # public|gm
    entity_type: Optional[str] = None  # faction|person|place
    entity_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Link(SQLModel, table=True):
    """Links between pages (wikilinks or manual)."""

    __tablename__ = "links"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    from_page_id: str = Field(foreign_key="note_pages.id", index=True)
    to_page_id: str = Field(foreign_key="note_pages.id", index=True)
    link_type: str  # wikilink|manual|reference
    visibility: str = Field(default="public")
    meta: Optional[str] = None  # JSON metadata


class Snapshot(SQLModel, table=True):
    """Timeline snapshot."""

    __tablename__ = "snapshots"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    at_date: datetime
    label: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MapAsset(SQLModel, table=True):
    """Base map images."""

    __tablename__ = "map_assets"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    snapshot_id: str = Field(foreign_key="snapshots.id")
    image_blob: bytes
    width: int
    height: int


class TerritoryTile(SQLModel, table=True):
    """Territory mask tiles."""

    __tablename__ = "territory_tiles"  # type: ignore[assignment]

    id: str = Field(primary_key=True)
    snapshot_id: str = Field(foreign_key="snapshots.id", index=True)
    faction_id: str = Field(foreign_key="factions.id", index=True)
    z: int  # zoom level
    x: int  # tile x
    y: int  # tile y
    tile_data: bytes  # PNG/WebP blob


class ActiveSnapshot(SQLModel, table=True):
    """Singleton table for active snapshot."""

    __tablename__ = "active_snapshot"  # type: ignore[assignment]

    id: str = Field(primary_key=True, default="1")
    snapshot_id: str = Field(foreign_key="snapshots.id")


class ProjectMeta(SQLModel, table=True):
    """Project metadata."""

    __tablename__ = "project_meta"  # type: ignore[assignment]

    key: str = Field(primary_key=True)
    value: str
