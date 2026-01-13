"""Page repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import NotePage


class PageRepository:
    """Repository for NotePage entity."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_id(self, page_id: str) -> NotePage | None:
        """Get page by ID."""
        return self.session.get(NotePage, page_id)

    def get_by_title(self, title: str) -> NotePage | None:
        """Get page by title."""
        return (
            self.session.execute(select(NotePage).where(NotePage.title == title)).scalars().first()
        )

    def list_all(self) -> list[NotePage]:
        """List all pages."""
        return list(self.session.execute(select(NotePage)).scalars().all())

    def create(self, page: NotePage) -> NotePage:
        """Create a new page."""
        self.session.add(page)
        self.session.flush()
        return page

    def update(self, page: NotePage) -> NotePage:
        """Update a page."""
        self.session.add(page)
        self.session.flush()
        return page

    def delete(self, page: NotePage) -> None:
        """Delete a page."""
        self.session.delete(page)
        self.session.flush()
