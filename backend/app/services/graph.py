"""Graph building and querying service."""

from typing import Literal

from sqlmodel import Session, select

from app.models import Link, NotePage
from app.services.wikilinks import extract_unique_titles


def rebuild_wikilinks_for_page(session: Session, page_id: str) -> None:
    """
    Rebuild wikilinks for a page by parsing its markdown and creating Link entries.

    Args:
        session: Database session
        page_id: ID of the page to rebuild links for
    """
    page = session.get(NotePage, page_id)
    if not page:
        return

    # Delete existing wikilinks from this page
    existing_links = session.exec(
        select(Link).where(Link.from_page_id == page_id, Link.link_type == "wikilink")
    ).all()
    for link in existing_links:
        session.delete(link)

    # Parse new wikilinks
    referenced_titles = extract_unique_titles(page.body_markdown)

    # Create Link entries for each referenced page
    for title in referenced_titles:
        # Find the target page by title
        target_page = session.exec(select(NotePage).where(NotePage.title == title)).first()
        if target_page:
            # Create link
            link = Link(
                id=f"{page_id}-wikilink-{target_page.id}",
                from_page_id=page_id,
                to_page_id=target_page.id,
                link_type="wikilink",
                visibility=page.visibility,  # Inherit visibility from source page
            )
            session.add(link)

    session.commit()


def get_backlinks(
    session: Session, page_id: str, view_mode: Literal["gm", "player"] = "gm"
) -> list[NotePage]:
    """
    Get all pages that link to the given page.

    Args:
        session: Database session
        page_id: ID of the target page
        view_mode: View mode filter (gm sees all, player sees only public)

    Returns:
        List of pages that link to the target page
    """
    # Get all links pointing to this page
    query = select(NotePage).join(Link, Link.from_page_id == NotePage.id).where(Link.to_page_id == page_id)

    # Apply visibility filter for player mode
    if view_mode == "player":
        query = query.where(NotePage.visibility == "public")

    pages = session.exec(query).all()
    return list(pages)
