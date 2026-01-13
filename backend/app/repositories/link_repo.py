"""Link repository."""

from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Link, NotePage


class LinkRepository:
    """Repository for Link entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, link_id: str) -> Link | None:
        """Get link by ID."""
        return self.session.get(Link, link_id)

    def list_all(self) -> list[Link]:
        """List all links."""
        return list(self.session.execute(select(Link)).scalars().all())

    def list_by_from_page(self, from_page_id: str) -> list[Link]:
        """List all links from a page."""
        return list(
            self.session.execute(select(Link).where(Link.from_page_id == from_page_id))
            .scalars()
            .all()
        )

    def list_wikilinks_from_page(self, from_page_id: str) -> list[Link]:
        """List wikilinks from a page."""
        return list(
            self.session.execute(
                select(Link).where(Link.from_page_id == from_page_id, Link.link_type == "wikilink")
            )
            .scalars()
            .all()
        )

    def get_backlinks(
        self, to_page_id: str, view_mode: Literal["gm", "player"] = "gm"
    ) -> list[NotePage]:
        """Get all pages that link to the given page."""
        query = (
            select(NotePage)
            .join(Link, Link.from_page_id == NotePage.id)
            .where(Link.to_page_id == to_page_id)
        )

        # Apply scope filter for player mode
        if view_mode == "player":
            query = query.where(NotePage.scope.in_(["public", "player"]))

        return list(self.session.execute(query).scalars().all())

    def create(self, link: Link) -> Link:
        """Create a new link."""
        self.session.add(link)
        self.session.flush()
        return link

    def delete(self, link: Link) -> None:
        """Delete a link."""
        self.session.delete(link)
        self.session.flush()

    def delete_wikilinks_from_page(self, from_page_id: str) -> None:
        """Delete all wikilinks from a page."""
        links = self.list_wikilinks_from_page(from_page_id)
        for link in links:
            self.session.delete(link)
        self.session.flush()
