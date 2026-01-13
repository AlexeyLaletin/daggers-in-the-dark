"""Wikilinks parser for markdown text."""

import re
from typing import TypedDict


class WikiLink(TypedDict):
    """Parsed wikilink structure."""

    title: str  # Target page title
    display: str  # Display text (may be different from title)
    start: int  # Start position in text
    end: int  # End position in text


# Regex pattern for wikilinks: [[Page Title]] or [[Page Title|Display Text]]
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def parse_wikilinks(text: str) -> list[WikiLink]:
    """
    Parse all wikilinks from markdown text.

    Args:
        text: Markdown text potentially containing wikilinks

    Returns:
        List of parsed wikilink dictionaries

    Examples:
        >>> parse_wikilinks("See [[Page One]] and [[Page Two|Two]]")
        [
            {'title': 'Page One', 'display': 'Page One', 'start': 4, 'end': 18},
            {'title': 'Page Two', 'display': 'Two', 'start': 23, 'end': 42}
        ]
    """
    links: list[WikiLink] = []

    for match in WIKILINK_PATTERN.finditer(text):
        title = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else title

        links.append(
            {
                "title": title,
                "display": display,
                "start": match.start(),
                "end": match.end(),
            }
        )

    return links


def extract_unique_titles(text: str) -> set[str]:
    """
    Extract unique page titles referenced in text.

    Args:
        text: Markdown text

    Returns:
        Set of unique page titles
    """
    links = parse_wikilinks(text)
    return {link["title"] for link in links}
