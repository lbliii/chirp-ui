"""Shared helpers for component-showcase route handlers."""

from __future__ import annotations

from chirp import Request, Template

from showcase.registry import golden_screen_pages, index_cards, nav_sections, shell_recipe_pages, visible_pages
from showcase.search import search_index_json

SHOWCASE_PALETTE_BOOST_ATTRS = (
    'hx-boost="true" hx-target="#main" hx-swap="innerHTML" '
    'hx-select="#page-content" hx-sync="#main:replace"'
)


def page(request: Request, template: str, **context: object) -> Template:
    """Render a full showcase page with route context for shell navigation."""
    context.setdefault("current_path", request.path)
    context.setdefault("showcase_nav_sections", nav_sections())
    context.setdefault("showcase_golden_screens", golden_screen_pages())
    context.setdefault("showcase_shell_recipes", shell_recipe_pages())
    context.setdefault("showcase_index_cards", index_cards())
    context.setdefault("showcase_pages", visible_pages())
    context.setdefault("showcase_search_index_json", search_index_json())
    context.setdefault("showcase_palette_boost_attrs", SHOWCASE_PALETTE_BOOST_ATTRS)
    return Template(template, **context)


def query_list(request: Request, key: str) -> list[str]:
    """Return repeated query values, accepting older comma-joined showcase links."""
    values = request.query.get_list(key)
    items: list[str] = []
    for value in values:
        items.extend(part.strip() for part in str(value).split(",") if part.strip())
    return items
