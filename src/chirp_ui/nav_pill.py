"""Sliding-pill nav indicator helpers (#255).

Server-side CSS custom-property estimates for first paint; shell runtime
``syncPill()`` refines to measured pixels on client navigation.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, cast

from chirp_ui.route_tabs import tab_is_active

_PillItem = dict[str, Any] | object


def _item_get(item: _PillItem, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        d = cast(dict[str, Any], item)
        return d.get(key, default)
    return getattr(item, key, default)


def estimate_nav_item_width_em(item: _PillItem, *, kind: str = "route_tab") -> float:
    """Heuristic width in rem for SSR pill placement before client measurement."""
    label = str(_item_get(item, "label", "") or "")
    char_w = 0.55
    if kind == "segmented":
        padding_x = 1.0
        icon_w = 0.75 if _item_get(item, "icon") else 0.0
        badge_w = 0.0
    else:
        padding_x = 2.0
        icon_w = 1.25 if _item_get(item, "icon") else 0.0
        badge_w = (
            2.0
            if _item_get(item, "badge") is not None
            or _item_get(item, "badge_expected")
            or _item_get(item, "badge_loading")
            else 0.0
        )
    gaps = 0.5 * sum(bool(x) for x in (icon_w, badge_w))
    return padding_x + max(len(label), 1) * char_w + icon_w + badge_w + gaps


def nav_pill_inline_style(
    items: Iterable[_PillItem],
    current_path: str = "",
    is_active: Callable[[_PillItem, str], bool] | None = None,
    *,
    gap_em: float = 0.5,
    block_size_em: float = 2.0,
    match: str = "route",
) -> str:
    """Return inline ``style`` for ``--chirpui-pill-*`` vars from item list."""
    active_fn = is_active or tab_is_active
    x = 0.0
    for item in items:
        w = estimate_nav_item_width_em(item)
        on = bool(_item_get(item, "active")) if match == "flag" else active_fn(item, current_path)
        if on:
            return (
                f"--chirpui-pill-x:{x}rem;--chirpui-pill-y:0rem;"
                f"--chirpui-pill-w:{w}rem;--chirpui-pill-h:{block_size_em}rem"
            )
        x += w + gap_em
    return "--chirpui-pill-x:0rem;--chirpui-pill-y:0rem;--chirpui-pill-w:0rem;--chirpui-pill-h:0rem"


def segmented_pill_inline_style(items: Iterable[_PillItem]) -> str:
    """Sliding pill offsets for segmented_control item dicts."""
    return nav_pill_inline_style(
        items,
        match="flag",
        gap_em=0.25,
        block_size_em=2.5,
    )
