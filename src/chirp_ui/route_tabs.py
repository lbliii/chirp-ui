"""Route-family tab helpers for chirp-ui route_tabs component.

Tab item: dict or object with href, match (optional, default "exact").
"""


def _get_attr(tab: dict | object, key: str, default: str = "") -> str:
    """Get href or match from tab (dict or object)."""
    if isinstance(tab, dict):
        return tab.get(key, default)
    return getattr(tab, key, default)


def tab_is_active(tab: dict | object, current_path: str) -> bool:
    """Return True when tab matches current_path.

    Tab must have href. Optionally has match: "exact" | "prefix".
    """
    href = _get_attr(tab, "href")
    match = _get_attr(tab, "match") or "exact"
    if match == "prefix":
        return current_path == href or current_path.startswith(href + "/")
    return current_path == href
