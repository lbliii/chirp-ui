"""Client search helpers for the showcase command palette."""

from __future__ import annotations

import json
from typing import Any

from showcase.registry import ShowcasePage, visible_pages


def page_to_search_entry(page: ShowcasePage) -> dict[str, Any]:
    """Serialize one registry page for palette search."""
    return {
        "path": page.path,
        "title": page.title,
        "section": page.section,
        "description": page.description,
        "tags": list(page.tags),
    }


def search_index() -> list[dict[str, Any]]:
    """Return searchable showcase pages for the client palette index."""
    return [page_to_search_entry(page) for page in visible_pages()]


def search_index_json() -> str:
    """JSON payload for ``<script type=\"application/json\">`` embedding."""
    return json.dumps(search_index(), separators=(",", ":"), ensure_ascii=True)


def _haystack(entry: dict[str, Any]) -> str:
    tags = entry.get("tags") or []
    return " ".join(
        (
            str(entry.get("title") or ""),
            str(entry.get("section") or ""),
            str(entry.get("description") or ""),
            " ".join(str(tag) for tag in tags),
        )
    ).lower()


def filter_search_index(query: str) -> list[dict[str, Any]]:
    """Substring filter over title, section, description, and tags."""
    needle = query.strip().lower()
    index = search_index()
    if not needle:
        return index
    return [entry for entry in index if needle in _haystack(entry)]
