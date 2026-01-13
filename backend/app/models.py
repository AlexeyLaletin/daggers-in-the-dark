"""SQLAlchemy ORM database models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, LargeBinary, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class World(Base):
    """World/City model (singleton per project)."""

    __tablename__ = "worlds"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(Text, nullable=False, default="UTC")
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    factions: Mapped[list["Faction"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )
    people: Mapped[list["Person"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )
    places: Mapped[list["Place"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )
    note_pages: Mapped[list["NotePage"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )
    snapshots: Mapped[list["Snapshot"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="world", cascade="all, delete-orphan"
    )


class Faction(Base):
    """Faction model."""

    __tablename__ = "factions"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    color: Mapped[str] = mapped_column(Text, nullable=False)  # hex #RRGGBB
    opacity: Mapped[float] = mapped_column(Float, nullable=False, default=0.4)
    notes_public: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes_gm: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["World"] = relationship(back_populates="factions")
    memberships: Mapped[list["FactionMembership"]] = relationship(
        back_populates="faction", cascade="all, delete-orphan"
    )
    territory_tiles: Mapped[list["TerritoryTile"]] = relationship(
        back_populates="faction", cascade="all, delete-orphan"
    )


class Person(Base):
    """Person model (NPC or PC)."""

    __tablename__ = "people"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    aliases: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string of array
    status: Mapped[str] = mapped_column(Text, nullable=False, default="alive")  # alive|dead|unknown
    workplace_place_id: Mapped[str | None] = mapped_column(ForeignKey("places.id"), nullable=True)
    home_place_id: Mapped[str | None] = mapped_column(ForeignKey("places.id"), nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string of array
    notes_public: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes_gm: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["World"] = relationship(back_populates="people")
    memberships: Mapped[list["FactionMembership"]] = relationship(
        back_populates="person", cascade="all, delete-orphan"
    )
    workplace: Mapped[Optional["Place"]] = relationship(
        foreign_keys=[workplace_place_id], back_populates="workers"
    )
    home: Mapped[Optional["Place"]] = relationship(
        foreign_keys=[home_place_id], back_populates="residents"
    )
    player_character: Mapped[Optional["PlayerCharacter"]] = relationship(
        back_populates="person", uselist=False
    )


class PlayerCharacter(Base):
    """Player Character extension of Person."""

    __tablename__ = "player_characters"

    person_id: Mapped[str] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), primary_key=True
    )
    playbook: Mapped[str | None] = mapped_column(Text, nullable=True)
    crew: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    # Relationships
    person: Mapped["Person"] = relationship(back_populates="player_character")


class FactionMembership(Base):
    """Many-to-many relationship between Person and Faction."""

    __tablename__ = "faction_memberships"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    person_id: Mapped[str] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faction_id: Mapped[str] = mapped_column(
        ForeignKey("factions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    person: Mapped["Person"] = relationship(back_populates="memberships")
    faction: Mapped["Faction"] = relationship(back_populates="memberships")


class Place(Base):
    """Place model."""

    __tablename__ = "places"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)  # building|district|landmark|other
    position: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON {x, y}
    owner_faction_id: Mapped[str | None] = mapped_column(
        ForeignKey("factions.id", ondelete="SET NULL"), nullable=True
    )
    parent_place_id: Mapped[str | None] = mapped_column(
        ForeignKey("places.id", ondelete="SET NULL"), nullable=True, index=True
    )
    scope: Mapped[str] = mapped_column(Text, nullable=False, default="public")  # public|gm|player
    notes_public: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes_gm: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["World"] = relationship(back_populates="places")
    workers: Mapped[list["Person"]] = relationship(
        foreign_keys="Person.workplace_place_id", back_populates="workplace"
    )
    residents: Mapped[list["Person"]] = relationship(
        foreign_keys="Person.home_place_id", back_populates="home"
    )
    parent: Mapped[Optional["Place"]] = relationship(
        remote_side="Place.id", back_populates="children"
    )
    children: Mapped[list["Place"]] = relationship(back_populates="parent")


class NotePage(Base):
    """Note page model (Obsidian-like pages)."""

    __tablename__ = "note_pages"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[str] = mapped_column(Text, nullable=False, default="public")  # public|gm|player
    entity_type: Mapped[str | None] = mapped_column(Text, nullable=True)  # faction|person|place
    entity_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["World"] = relationship(back_populates="note_pages")
    links_from: Mapped[list["Link"]] = relationship(
        foreign_keys="Link.from_page_id", back_populates="from_page", cascade="all, delete-orphan"
    )
    links_to: Mapped[list["Link"]] = relationship(
        foreign_keys="Link.to_page_id", back_populates="to_page", cascade="all, delete-orphan"
    )


class Link(Base):
    """Links between pages (wikilinks or manual)."""

    __tablename__ = "links"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    from_page_id: Mapped[str] = mapped_column(
        ForeignKey("note_pages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    to_page_id: Mapped[str] = mapped_column(
        ForeignKey("note_pages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    link_type: Mapped[str] = mapped_column(Text, nullable=False)  # wikilink|manual|reference
    scope: Mapped[str] = mapped_column(Text, nullable=False, default="public")  # public|gm|player
    meta: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON metadata

    # Relationships
    world: Mapped["World"] = relationship()
    from_page: Mapped["NotePage"] = relationship(
        foreign_keys=[from_page_id], back_populates="links_from"
    )
    to_page: Mapped["NotePage"] = relationship(foreign_keys=[to_page_id], back_populates="links_to")


class Snapshot(Base):
    """Timeline snapshot."""

    __tablename__ = "snapshots"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    at_date: Mapped[datetime] = mapped_column(nullable=False, index=True)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    # Relationships
    world: Mapped["World"] = relationship(back_populates="snapshots")
    map_assets: Mapped[list["MapAsset"]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )
    territory_tiles: Mapped[list["TerritoryTile"]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )


class MapAsset(Base):
    """Base map images."""

    __tablename__ = "map_assets"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(
        ForeignKey("snapshots.id", ondelete="CASCADE"), nullable=False
    )
    image_blob: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    snapshot: Mapped["Snapshot"] = relationship(back_populates="map_assets")


class TerritoryTile(Base):
    """Territory mask tiles."""

    __tablename__ = "territory_tiles"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    snapshot_id: Mapped[str] = mapped_column(
        ForeignKey("snapshots.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faction_id: Mapped[str] = mapped_column(
        ForeignKey("factions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    z: Mapped[int] = mapped_column(Integer, nullable=False)  # zoom level
    x: Mapped[int] = mapped_column(Integer, nullable=False)  # tile x
    y: Mapped[int] = mapped_column(Integer, nullable=False)  # tile y
    tile_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # PNG/WebP blob

    # Relationships
    snapshot: Mapped["Snapshot"] = relationship(back_populates="territory_tiles")
    faction: Mapped["Faction"] = relationship(back_populates="territory_tiles")


class ActiveSnapshot(Base):
    """Singleton table for active snapshot."""

    __tablename__ = "active_snapshot"
    __table_args__ = (CheckConstraint("id = '1'", name="singleton_check"),)

    id: Mapped[str] = mapped_column(Text, primary_key=True, default="1")
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("snapshots.id"), nullable=False)


class Event(Base):
    """Event model (log-style, narrative)."""

    __tablename__ = "events"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    world_id: Mapped[str] = mapped_column(ForeignKey("worlds.id"), nullable=False, index=True)
    at_datetime: Mapped[datetime] = mapped_column(nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body_markdown: Mapped[str | None] = mapped_column(Text, nullable=True)
    scope: Mapped[str] = mapped_column(Text, nullable=False, default="gm")  # public|gm|player
    snapshot_id: Mapped[str | None] = mapped_column(
        ForeignKey("snapshots.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    world: Mapped["World"] = relationship(back_populates="events")
    refs: Mapped[list["EventRef"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


class EventRef(Base):
    """References from events to entities."""

    __tablename__ = "event_refs"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    event_id: Mapped[str] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(
        Text, nullable=False, index=True
    )  # faction|person|place|page
    entity_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    role: Mapped[str | None] = mapped_column(Text, nullable=True)  # involved|location|target|etc

    # Relationships
    event: Mapped["Event"] = relationship(back_populates="refs")


class ProjectMeta(Base):
    """Project metadata."""

    __tablename__ = "project_meta"

    key: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
