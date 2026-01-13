"""Graph building and querying service."""


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Link, NotePage
from app.repositories import LinkRepository, PageRepository
from app.services.visibility import ViewMode, VisibilityService


class GraphService:
    """Service for graph operations."""

    def __init__(self, session: Session) -> None:
        """Initialize service with database session."""
        self.session = session
        self.page_repo = PageRepository(session)
        self.link_repo = LinkRepository(session)
        self.visibility = VisibilityService()

    def get_graph(
        self, view_mode: ViewMode = "gm"
    ) -> tuple[list[NotePage], list[Link]]:
        """
        Get the full graph of pages and links with visibility filtering.

        Args:
            view_mode: View mode (gm or player)

        Returns:
            Tuple of (filtered pages, filtered links)
        """
        allowed_scopes = self.visibility.get_allowed_scopes(view_mode)

        # Get pages (nodes)
        pages_query = select(NotePage).where(NotePage.scope.in_(allowed_scopes))
        pages = list(self.session.execute(pages_query).scalars().all())

        # Get visible node IDs
        visible_node_ids = {page.id for page in pages}

        # Get links (edges)
        links_query = select(Link).where(Link.scope.in_(allowed_scopes))
        all_links = list(self.session.execute(links_query).scalars().all())

        # Filter edges to only include links between visible nodes
        links = [
            link for link in all_links
            if link.from_page_id in visible_node_ids and link.to_page_id in visible_node_ids
        ]

        return pages, links

    def get_backlinks(
        self, page_id: str, view_mode: ViewMode = "gm"
    ) -> list[NotePage]:
        """
        Get all pages that link to the given page.

        Args:
            page_id: ID of the target page
            view_mode: View mode filter (gm sees all, player sees only public+player)

        Returns:
            List of pages that link to the target page
        """
        return self.link_repo.get_backlinks(page_id, view_mode)
