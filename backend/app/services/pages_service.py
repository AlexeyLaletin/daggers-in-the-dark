"""Pages and wikilinks service."""

import uuid

from sqlalchemy.orm import Session

from app.models import Link
from app.repositories import LinkRepository, PageRepository, WorldRepository
from app.services.wikilinks import extract_unique_titles


class PagesService:
    """Service for managing pages and wikilinks."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.page_repo = PageRepository(session)
        self.link_repo = LinkRepository(session)
        self.world_repo = WorldRepository(session)

    def rebuild_wikilinks(self, page_id: str) -> None:
        """
        Rebuild wikilinks for a page by parsing its markdown.

        Args:
            page_id: ID of the page to rebuild links for
        """
        page = self.page_repo.get_by_id(page_id)
        if not page:
            return

        # Delete existing wikilinks from this page
        self.link_repo.delete_wikilinks_from_page(page_id)

        # Parse new wikilinks
        referenced_titles = extract_unique_titles(page.body_markdown)

        # Get world_id
        world = self.world_repo.get_first()
        if not world:
            return

        # Create Link entries for each referenced page
        for title in referenced_titles:
            # Find the target page by title
            target_page = self.page_repo.get_by_title(title)
            if target_page:
                # Create link
                link = Link(
                    id=str(uuid.uuid4()),
                    world_id=world.id,
                    from_page_id=page_id,
                    to_page_id=target_page.id,
                    link_type="wikilink",
                    scope=page.scope,  # Inherit scope from source page
                )
                self.link_repo.create(link)

        # Note: We don't commit here - let the caller manage transaction
