"""Route-family tab helpers for chirp-ui route_tabs component.

Tab item: dict or object with ``href``, optional ``match`` (default ``"exact"``).
Full dict shape (from Chirp ``TabItem`` via ``_tab_item_to_shell_dict``):
``{ label, href, icon?, badge?, match? }``.
"""

from typing import Any, cast


def _get_attr(tab: dict[str, Any] | object, key: str, default: str = "") -> str:
    """Get href or match from tab (dict or object)."""
    if isinstance(tab, dict):
        d: dict[str, Any] = cast(dict[str, Any], tab)
        val = d.get(key, default)
        return default if val is None else str(val)
    return str(getattr(tab, key, default))


def tab_is_active(tab: dict | object, current_path: str) -> bool:
    """Return True when tab matches current_path.

    Tab must have href. Optionally has match: "exact" | "prefix".
    Returns False when href is empty (prevents prefix match against all paths).
    """
    href = _get_attr(tab, "href")
    if not href:
        return False
    match = _get_attr(tab, "match") or "exact"
    if match == "prefix":
        return current_path == href or current_path.startswith(href + "/")
    return current_path == href
