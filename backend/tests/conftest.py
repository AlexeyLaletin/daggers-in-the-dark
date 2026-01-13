"""Pytest configuration and fixtures."""

import json
import uuid
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base, get_session
from app.models import (
    ActiveSnapshot,
    Event,
    EventRef,
    Faction,
    FactionMembership,
    NotePage,
    Person,
    Place,
    PlayerCharacter,
    ProjectMeta,
    Snapshot,
    TerritoryTile,
    World,
)

# Deterministic UUID namespace for test data
TEST_NAMESPACE = uuid.UUID("00000000-0000-0000-0000-000000000000")


def make_uuid(name: str) -> str:
    """Generate deterministic UUID for test data."""
    return str(uuid.uuid5(TEST_NAMESPACE, name))


@pytest.fixture(scope="function")
def temp_db_engine(tmp_path: Path) -> Generator[Engine, None, None]:
    """Create a temporary SQLite database engine for testing."""
    db_path = tmp_path / "test_blades.db"

    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        echo=False,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture(scope="function")
def db_session(temp_db_engine: Engine) -> Generator[Session, None, None]:
    """Create a database session for testing."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=temp_db_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """Create a test client with overridden database dependency."""
    # Create test app without lifespan to avoid init_db() using global DATABASE_PATH
    from fastapi.middleware.cors import CORSMiddleware

    from app.api import (
        export_import,
        factions,
        graph,
        map_assets,
        pages,
        people,
        places,
        project,
        snapshots,
        tiles,
    )

    test_app = FastAPI(
        title="Blades Faction Map API (Test)",
        description="Test instance",
        version="0.1.0",
    )

    # CORS for local Electron renderer
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    test_app.include_router(project.router, prefix="/api")
    test_app.include_router(factions.router, prefix="/api")
    test_app.include_router(people.router, prefix="/api")
    test_app.include_router(places.router, prefix="/api")
    test_app.include_router(pages.router, prefix="/api")
    test_app.include_router(graph.router, prefix="/api")
    test_app.include_router(snapshots.router, prefix="/api")
    test_app.include_router(tiles.router, prefix="/api")
    test_app.include_router(map_assets.router, prefix="/api")
    test_app.include_router(export_import.router, prefix="/api")

    # Health and root endpoints
    @test_app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @test_app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Blades Faction Map API (Test)"}

    def override_get_session() -> Generator[Session, None, None]:
        yield db_session

    test_app.dependency_overrides[get_session] = override_get_session

    test_client = TestClient(test_app, raise_server_exceptions=True)

    yield test_client

    test_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def initialized_client(client: TestClient) -> TestClient:
    """Create a test client with initialized project."""
    # Initialize project via API
    response = client.post(
        "/api/project/init",
        json={
            "world_name": "Doskvol",
            "timezone": "UTC",
            "initial_snapshot_date": "1847-01-01T00:00:00Z",
            "initial_snapshot_label": "Initial",
        }
    )
    assert response.status_code == 201
    return client


@pytest.fixture(scope="function")
def seed_small_town(db_session: Session) -> dict[str, any]:
    """
    Seed test database with 'Little Doskvol' town data.

    Returns dict with created entity IDs for easy reference in tests.
    """
    # === 1. World ===
    world = World(
        id=make_uuid("world_little_doskvol"),
        name="Little_Doskvol",
        description="A small industrial city on the edge of civilization",
        timezone="UTC",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 20, 0, 0),
    )
    db_session.add(world)

    # === 2. Snapshots (Day1, Day2, Day3) ===
    day1 = Snapshot(
        id=make_uuid("snapshot_day1"),
        world_id=world.id,
        at_date=datetime(1920, 1, 1, 8, 0, 0),
        label="Day1_Morning",
        created_at=datetime(1920, 1, 1, 7, 0, 0),
    )
    day2 = Snapshot(
        id=make_uuid("snapshot_day2"),
        world_id=world.id,
        at_date=datetime(1920, 1, 2, 8, 0, 0),
        label="Day2_Morning",
        created_at=datetime(1920, 1, 2, 7, 0, 0),
    )
    day3 = Snapshot(
        id=make_uuid("snapshot_day3"),
        world_id=world.id,
        at_date=datetime(1920, 1, 3, 8, 0, 0),
        label="Day3_Morning",
        created_at=datetime(1920, 1, 3, 7, 0, 0),
    )
    db_session.add_all([day1, day2, day3])

    # Active snapshot points to Day3
    active_snap = ActiveSnapshot(
        id="1",
        snapshot_id=day3.id,
    )
    db_session.add(active_snap)

    # === 3. Factions ===
    bluecoats = Faction(
        id=make_uuid("faction_bluecoats"),
        world_id=world.id,
        name="Bluecoats",
        color="#0066CC",
        opacity=0.4,
        notes_public="The city watch and law enforcement",
        notes_gm="Secretly corrupt, taking bribes from the Council",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 10, 0, 0),
    )
    crows = Faction(
        id=make_uuid("faction_crows"),
        world_id=world.id,
        name="The_Crows",
        color="#333333",
        opacity=0.5,
        notes_public="Notorious gang controlling Crow's Foot district",
        notes_gm="Planning to expand into Lampblack territory",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 2, 18, 0, 0),
    )
    lampblacks = Faction(
        id=make_uuid("faction_lampblacks"),
        world_id=world.id,
        name="Lampblacks",
        color="#FF6600",
        opacity=0.45,
        notes_public="Industrial gang, control docks and warehouses",
        notes_gm="Weakened after recent turf war",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 12, 0, 0),
    )
    council = Faction(
        id=make_uuid("faction_council"),
        world_id=world.id,
        name="City_Council",
        color="#9900CC",
        opacity=0.3,
        notes_public="",
        notes_gm="Shadow government, pulling strings behind the scenes",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    db_session.add_all([bluecoats, crows, lampblacks, council])

    # === 4. Places ===
    crows_foot = Place(
        id=make_uuid("place_crows_foot"),
        world_id=world.id,
        name="Crows_Foot",
        type="district",
        position=json.dumps({"x": 100, "y": 150}),
        owner_faction_id=crows.id,
        notes_public="Industrial district with narrow streets and tall buildings",
        notes_gm="Perfect for smuggling operations",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    leaky_bucket = Place(
        id=make_uuid("place_leaky_bucket"),
        world_id=world.id,
        name="The_Leaky_Bucket",
        type="building",
        position=json.dumps({"x": 120, "y": 160}),
        owner_faction_id=crows.id,
        parent_place_id=crows_foot.id,
        notes_public="A tavern and meeting place in Crow's Foot",
        notes_gm="Secret meeting room in the basement for Crows leadership",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 2, 20, 0, 0),
    )
    old_bridge = Place(
        id=make_uuid("place_old_bridge"),
        world_id=world.id,
        name="Old_Bridge",
        type="landmark",
        position=json.dumps({"x": 200, "y": 100}),
        owner_faction_id=None,
        notes_public="Ancient stone bridge over the canal",
        notes_gm="Common neutral meeting ground for faction negotiations",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    bluecoat_precinct = Place(
        id=make_uuid("place_bluecoat_precinct"),
        world_id=world.id,
        name="Bluecoat_Precinct_7",
        type="building",
        position=json.dumps({"x": 300, "y": 150}),
        owner_faction_id=bluecoats.id,
        notes_public="Main headquarters of the city watch",
        notes_gm="Evidence room is poorly guarded",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    warehouse_district = Place(
        id=make_uuid("place_warehouse_district"),
        world_id=world.id,
        name="Warehouse_District",
        type="district",
        position=json.dumps({"x": 50, "y": 200}),
        owner_faction_id=lampblacks.id,
        notes_public="Industrial zone filled with warehouses and docks",
        notes_gm="Lampblacks store contraband here",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    db_session.add_all([crows_foot, leaky_bucket, old_bridge, bluecoat_precinct, warehouse_district])

    # === 5. People (NPCs) ===
    lyssa = Person(
        id=make_uuid("person_lyssa"),
        world_id=world.id,
        name="Lyssa",
        aliases=json.dumps(["The Shadow", "Silent Blade"]),
        status="alive",
        workplace_place_id=leaky_bucket.id,
        home_place_id=crows_foot.id,
        tags=json.dumps(["smuggler", "informant", "spy"]),
        notes_public="Known smuggler in Crow's Foot",
        notes_gm="Actually a spy for the Bluecoats, double agent",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 15, 0, 0),
    )
    roric = Person(
        id=make_uuid("person_roric"),
        world_id=world.id,
        name="Roric",
        aliases=json.dumps(["Boss Roric"]),
        status="dead",
        workplace_place_id=leaky_bucket.id,
        home_place_id=None,
        tags=json.dumps(["leader", "deceased"]),
        notes_public="Former leader of The Crows, recently deceased",
        notes_gm="Murdered by Lampblacks, body never found",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 2, 0, 0, 0),
    )
    captain_vale = Person(
        id=make_uuid("person_captain_vale"),
        world_id=world.id,
        name="Captain_Vale",
        aliases=json.dumps([]),
        status="alive",
        workplace_place_id=bluecoat_precinct.id,
        home_place_id=None,
        tags=json.dumps(["bluecoat", "officer", "corrupt"]),
        notes_public="",
        notes_gm="Takes bribes from all factions, plays them against each other",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 10, 0, 0),
    )
    marlane = Person(
        id=make_uuid("person_marlane"),
        world_id=world.id,
        name="Marlane",
        aliases=json.dumps(["Doc"]),
        status="alive",
        workplace_place_id=warehouse_district.id,
        home_place_id=None,
        tags=json.dumps(["doctor", "alchemist"]),
        notes_public="Underground doctor, no questions asked",
        notes_gm="Supplies drugs to multiple factions",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 1, 0, 0, 0),
    )
    # Player Characters (to be linked later)
    cutter = Person(
        id=make_uuid("person_cutter"),
        world_id=world.id,
        name="Cutter_Kane",
        aliases=json.dumps(["Kane"]),
        status="alive",
        workplace_place_id=None,
        home_place_id=leaky_bucket.id,
        tags=json.dumps(["player", "cutter"]),
        notes_public="Tough fighter, enforcer for The Crows",
        notes_gm="",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 18, 0, 0),
    )
    lurk = Person(
        id=make_uuid("person_lurk"),
        world_id=world.id,
        name="Ghost_Whisper",
        aliases=json.dumps(["Ghost", "Whisper"]),
        status="alive",
        workplace_place_id=None,
        home_place_id=crows_foot.id,
        tags=json.dumps(["player", "lurk"]),
        notes_public="Mysterious thief and infiltrator",
        notes_gm="",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 18, 0, 0),
    )
    slide = Person(
        id=make_uuid("person_slide"),
        world_id=world.id,
        name="Silver_Tongue_Sara",
        aliases=json.dumps(["Sara", "Silver"]),
        status="alive",
        workplace_place_id=None,
        home_place_id=leaky_bucket.id,
        tags=json.dumps(["player", "slide"]),
        notes_public="Smooth talker and con artist",
        notes_gm="",
        created_at=datetime(1920, 1, 1, 0, 0, 0),
        updated_at=datetime(1920, 1, 3, 18, 0, 0),
    )
    db_session.add_all([lyssa, roric, captain_vale, marlane, cutter, lurk, slide])

    # === 6. Player Characters ===
    pc_cutter = PlayerCharacter(
        person_id=cutter.id,
        playbook="Cutter",
        crew="The_Shadow_Crew",
        is_active=True,
    )
    pc_lurk = PlayerCharacter(
        person_id=lurk.id,
        playbook="Lurk",
        crew="The_Shadow_Crew",
        is_active=True,
    )
    pc_slide = PlayerCharacter(
        person_id=slide.id,
        playbook="Slide",
        crew="The_Shadow_Crew",
        is_active=True,
    )
    db_session.add_all([pc_cutter, pc_lurk, pc_slide])

    # === 7. Faction Memberships ===
    memberships = [
        FactionMembership(
            id=make_uuid("membership_lyssa_crows"),
            person_id=lyssa.id,
            faction_id=crows.id,
            role="smuggler",
        ),
        FactionMembership(
            id=make_uuid("membership_roric_crows"),
            person_id=roric.id,
            faction_id=crows.id,
            role="boss",
        ),
        FactionMembership(
            id=make_uuid("membership_vale_bluecoats"),
            person_id=captain_vale.id,
            faction_id=bluecoats.id,
            role="captain",
        ),
        FactionMembership(
            id=make_uuid("membership_cutter_crows"),
            person_id=cutter.id,
            faction_id=crows.id,
            role="enforcer",
        ),
        FactionMembership(
            id=make_uuid("membership_lurk_crows"),
            person_id=lurk.id,
            faction_id=crows.id,
            role="thief",
        ),
        FactionMembership(
            id=make_uuid("membership_slide_crows"),
            person_id=slide.id,
            faction_id=crows.id,
            role="diplomat",
        ),
    ]
    db_session.add_all(memberships)

    # === 8. Note Pages ===
    page_crows = NotePage(
        id=make_uuid("page_crows"),
        world_id=world.id,
        title="The Crows",
        body_markdown="The dominant gang in [[Crows_Foot]]. Led by [[Boss Roric]] until his death. Key members include [[Lyssa]] and the player crew.",
        scope="public",
        entity_type="faction",
        entity_id=crows.id,
        created_at=datetime(1920, 1, 1, 12, 0, 0),
        updated_at=datetime(1920, 1, 3, 14, 0, 0),
    )
    page_leaky_bucket = NotePage(
        id=make_uuid("page_leaky_bucket"),
        world_id=world.id,
        title="The Leaky Bucket",
        body_markdown="A tavern in [[Crows_Foot]] owned by [[The Crows]]. Popular meeting spot. [[Lyssa]] works here as a barmaid.",
        scope="public",
        entity_type="place",
        entity_id=leaky_bucket.id,
        created_at=datetime(1920, 1, 1, 13, 0, 0),
        updated_at=datetime(1920, 1, 2, 21, 0, 0),
    )
    page_lyssa = NotePage(
        id=make_uuid("page_lyssa"),
        world_id=world.id,
        title="Lyssa",
        body_markdown="Smuggler working at [[The Leaky Bucket]]. Known as The Shadow. Has connections to [[Bluecoats]].",
        scope="public",
        entity_type="person",
        entity_id=lyssa.id,
        created_at=datetime(1920, 1, 1, 14, 0, 0),
        updated_at=datetime(1920, 1, 3, 16, 0, 0),
    )
    page_lyssa_secret = NotePage(
        id=make_uuid("page_lyssa_secret"),
        world_id=world.id,
        title="Lyssa Secret Intel",
        body_markdown="[[Lyssa]] is actually a double agent working for [[Captain Vale]] and the [[Bluecoats]]. She reports on [[The Crows]] activities.",
        scope="gm",
        entity_type=None,
        entity_id=None,
        created_at=datetime(1920, 1, 2, 10, 0, 0),
        updated_at=datetime(1920, 1, 3, 16, 0, 0),
    )
    page_player_notes = NotePage(
        id=make_uuid("page_player_theory"),
        world_id=world.id,
        title="Player Theory on Lyssa",
        body_markdown="We suspect [[Lyssa]] might be working with someone outside [[The Crows]]. Need to investigate her connection to [[Bluecoats]].",
        scope="player",
        entity_type=None,
        entity_id=None,
        created_at=datetime(1920, 1, 3, 19, 0, 0),
        updated_at=datetime(1920, 1, 3, 19, 0, 0),
    )
    page_roric_death = NotePage(
        id=make_uuid("page_roric_death"),
        world_id=world.id,
        title="Boss Roric",
        body_markdown="Former leader of [[The Crows]], found dead on Day 2. Suspected [[Lampblacks]] involvement. Body at [[Old_Bridge]].",
        scope="public",
        entity_type="person",
        entity_id=roric.id,
        created_at=datetime(1920, 1, 2, 9, 0, 0),
        updated_at=datetime(1920, 1, 2, 9, 0, 0),
    )
    page_warehouse_score = NotePage(
        id=make_uuid("page_warehouse_score"),
        world_id=world.id,
        title="Warehouse District Score",
        body_markdown="Planning heist in [[Warehouse_District]]. [[Marlane]] can provide distraction. Avoid [[Lampblacks]] patrols.",
        scope="player",
        entity_type=None,
        entity_id=None,
        created_at=datetime(1920, 1, 3, 20, 0, 0),
        updated_at=datetime(1920, 1, 3, 20, 0, 0),
    )
    db_session.add_all([page_crows, page_leaky_bucket, page_lyssa, page_lyssa_secret, page_player_notes, page_roric_death, page_warehouse_score])

    # === 9. Links (wikilinks) ===
    # Links will be created based on wikilink parsing in pages
    # Simplified - in real app, wikilinks parser would create these automatically
    # Example:
    # links = [
    #     Link(
    #         id=make_uuid("link_crows_crowsfoot"),
    #         world_id=world.id,
    #         from_page_id=page_crows.id,
    #         to_page_id=NotePage(title="Crows_Foot").title,
    #         link_type="wikilink",
    #         scope="public",
    #     ),
    # ]
    # db_session.add_all(links)

    # === 10. Territory Tiles (minimal test data) ===
    # Create tiny 1x1 PNG placeholder for testing
    # PNG header + minimal IEND chunk (valid but tiny PNG)
    tiny_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    tiles = [
        # Day1 tiles
        TerritoryTile(
            id=make_uuid("tile_day1_crows_0_0_0"),
            snapshot_id=day1.id,
            faction_id=crows.id,
            z=0, x=0, y=0,
            tile_data=tiny_png,
        ),
        TerritoryTile(
            id=make_uuid("tile_day1_bluecoats_0_1_0"),
            snapshot_id=day1.id,
            faction_id=bluecoats.id,
            z=0, x=1, y=0,
            tile_data=tiny_png,
        ),
        # Day2 tiles (expanded)
        TerritoryTile(
            id=make_uuid("tile_day2_crows_0_0_0"),
            snapshot_id=day2.id,
            faction_id=crows.id,
            z=0, x=0, y=0,
            tile_data=tiny_png,
        ),
        TerritoryTile(
            id=make_uuid("tile_day2_crows_0_0_1"),
            snapshot_id=day2.id,
            faction_id=crows.id,
            z=0, x=0, y=1,
            tile_data=tiny_png,
        ),
        # Day3 tiles
        TerritoryTile(
            id=make_uuid("tile_day3_lampblacks_0_2_0"),
            snapshot_id=day3.id,
            faction_id=lampblacks.id,
            z=0, x=2, y=0,
            tile_data=tiny_png,
        ),
    ]
    db_session.add_all(tiles)

    # === 11. Events ===
    event1 = Event(
        id=make_uuid("event_brawl"),
        world_id=world.id,
        at_datetime=datetime(1920, 1, 1, 22, 30, 0),
        title="Brawl at The Leaky Bucket",
        body_markdown="A fight broke out between [[The Crows]] and [[Lampblacks]] members. [[Lyssa]] called [[Bluecoats]].",
        scope="public",
        snapshot_id=day1.id,
    )
    event2 = Event(
        id=make_uuid("event_roric_death"),
        world_id=world.id,
        at_datetime=datetime(1920, 1, 2, 3, 15, 0),
        title="Boss Roric Found Dead",
        body_markdown="[[Boss Roric]]'s body discovered near [[Old_Bridge]]. Suspected murder by [[Lampblacks]].",
        scope="public",
        snapshot_id=day2.id,
    )
    event3 = Event(
        id=make_uuid("event_bluecoat_raid"),
        world_id=world.id,
        at_datetime=datetime(1920, 1, 2, 15, 0, 0),
        title="Bluecoats Raid Warehouse",
        body_markdown="[[Captain Vale]] led raid on [[Warehouse_District]]. [[Lampblacks]] took heavy losses.",
        scope="public",
        snapshot_id=day2.id,
    )
    event4 = Event(
        id=make_uuid("event_council_meeting"),
        world_id=world.id,
        at_datetime=datetime(1920, 1, 3, 0, 0, 0),
        title="Secret Council Meeting",
        body_markdown="[[City_Council]] met to discuss faction tensions. [[Captain Vale]] attended.",
        scope="gm",
        snapshot_id=day3.id,
    )
    event5 = Event(
        id=make_uuid("event_player_score"),
        world_id=world.id,
        at_datetime=datetime(1920, 1, 3, 21, 0, 0),
        title="Player Crew Heist",
        body_markdown="[[Cutter Kane]], [[Ghost Whisper]], and [[Silver Tongue Sara]] pulled off successful heist in [[Warehouse_District]].",
        scope="player",
        snapshot_id=day3.id,
    )
    db_session.add_all([event1, event2, event3, event4, event5])

    # === 12. Event Refs ===
    event_refs = [
        # Event 1 refs
        EventRef(id=make_uuid("ref_event1_place"), event_id=event1.id, entity_type="place", entity_id=leaky_bucket.id, role="location"),
        EventRef(id=make_uuid("ref_event1_faction_crows"), event_id=event1.id, entity_type="faction", entity_id=crows.id, role="involved"),
        EventRef(id=make_uuid("ref_event1_faction_lamps"), event_id=event1.id, entity_type="faction", entity_id=lampblacks.id, role="involved"),
        EventRef(id=make_uuid("ref_event1_person"), event_id=event1.id, entity_type="person", entity_id=lyssa.id, role="involved"),
        # Event 2 refs
        EventRef(id=make_uuid("ref_event2_person"), event_id=event2.id, entity_type="person", entity_id=roric.id, role="target"),
        EventRef(id=make_uuid("ref_event2_place"), event_id=event2.id, entity_type="place", entity_id=old_bridge.id, role="location"),
        EventRef(id=make_uuid("ref_event2_faction"), event_id=event2.id, entity_type="faction", entity_id=lampblacks.id, role="involved"),
        # Event 3 refs
        EventRef(id=make_uuid("ref_event3_person"), event_id=event3.id, entity_type="person", entity_id=captain_vale.id, role="involved"),
        EventRef(id=make_uuid("ref_event3_place"), event_id=event3.id, entity_type="place", entity_id=warehouse_district.id, role="location"),
        EventRef(id=make_uuid("ref_event3_faction"), event_id=event3.id, entity_type="faction", entity_id=lampblacks.id, role="target"),
        # Event 4 refs
        EventRef(id=make_uuid("ref_event4_faction"), event_id=event4.id, entity_type="faction", entity_id=council.id, role="involved"),
        EventRef(id=make_uuid("ref_event4_person"), event_id=event4.id, entity_type="person", entity_id=captain_vale.id, role="involved"),
        # Event 5 refs
        EventRef(id=make_uuid("ref_event5_person1"), event_id=event5.id, entity_type="person", entity_id=cutter.id, role="involved"),
        EventRef(id=make_uuid("ref_event5_person2"), event_id=event5.id, entity_type="person", entity_id=lurk.id, role="involved"),
        EventRef(id=make_uuid("ref_event5_person3"), event_id=event5.id, entity_type="person", entity_id=slide.id, role="involved"),
        EventRef(id=make_uuid("ref_event5_place"), event_id=event5.id, entity_type="place", entity_id=warehouse_district.id, role="location"),
    ]
    db_session.add_all(event_refs)

    # === 13. Project Meta ===
    meta = [
        ProjectMeta(key="version", value="1"),
        ProjectMeta(key="created_at", value=datetime(1920, 1, 1, 0, 0, 0).isoformat()),
        ProjectMeta(key="app_version", value="0.1.0-test"),
    ]
    db_session.add_all(meta)

    # Commit all
    db_session.commit()

    # Return IDs for easy test reference
    return {
        "world_id": world.id,
        "snapshot_ids": {
            "day1": day1.id,
            "day2": day2.id,
            "day3": day3.id,
        },
        "faction_ids": {
            "bluecoats": bluecoats.id,
            "crows": crows.id,
            "lampblacks": lampblacks.id,
            "council": council.id,
        },
        "place_ids": {
            "crows_foot": crows_foot.id,
            "leaky_bucket": leaky_bucket.id,
            "old_bridge": old_bridge.id,
            "bluecoat_precinct": bluecoat_precinct.id,
            "warehouse_district": warehouse_district.id,
        },
        "person_ids": {
            "lyssa": lyssa.id,
            "roric": roric.id,
            "captain_vale": captain_vale.id,
            "marlane": marlane.id,
            "cutter": cutter.id,
            "lurk": lurk.id,
            "slide": slide.id,
        },
        "pc_ids": [cutter.id, lurk.id, slide.id],
        "page_ids": {
            "crows": page_crows.id,
            "leaky_bucket": page_leaky_bucket.id,
            "lyssa": page_lyssa.id,
            "lyssa_secret": page_lyssa_secret.id,
            "player_notes": page_player_notes.id,
            "roric_death": page_roric_death.id,
            "warehouse_score": page_warehouse_score.id,
        },
        "event_ids": {
            "brawl": event1.id,
            "roric_death": event2.id,
            "raid": event3.id,
            "council_meeting": event4.id,
            "player_score": event5.id,
        },
    }


# Note: No longer using autouse world fixture.
# Tests should explicitly initialize project via POST /api/project/init or use initialized_client fixture.


# Legacy fixtures for backward compatibility
@pytest.fixture
def sample_faction() -> dict[str, str | float]:
    """Sample faction data for testing."""
    return {
        "name": "The Crows",
        "color": "#FF5733",
        "opacity": 0.4,
        "notes_public": "A notorious gang",
        "notes_gm": "Secret: they work for the City Council",
    }


@pytest.fixture
def sample_person() -> dict[str, str | list[str]]:
    """Sample person data for testing."""
    return {
        "name": "Lyssa",
        "aliases": ["The Shadow"],
        "status": "alive",
        "tags": ["smuggler", "informant"],
        "notes_public": "Known smuggler in Crow's Foot",
        "notes_gm": "Actually a spy for the Bluecoats",
    }


@pytest.fixture
def sample_place() -> dict[str, str]:
    """Sample place data for testing."""
    return {
        "name": "The Leaky Bucket",
        "type": "building",
        "notes_public": "A tavern in Crow's Foot",
        "notes_gm": "Secret meeting place for The Crows",
    }
