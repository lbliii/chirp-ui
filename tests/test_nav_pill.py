"""Tests for chirp_ui.nav_pill sliding-indicator helpers."""

from chirp_ui.nav_pill import (
    estimate_nav_item_width_em,
    nav_pill_inline_style,
    segmented_pill_inline_style,
)
from chirp_ui.route_tabs import tab_is_active


def test_estimate_nav_item_width_grows_with_label_and_icon() -> None:
    plain = estimate_nav_item_width_em({"label": "Runs"})
    rich = estimate_nav_item_width_em(
        {"label": "Pull requests", "icon": "git-pull-request", "badge": 2}
    )
    assert rich > plain


def test_nav_pill_inline_style_offsets_to_active_tab() -> None:
    items = (
        {"label": "Skills", "href": "/skills"},
        {"label": "Settings", "href": "/settings", "match": "prefix"},
    )
    style = nav_pill_inline_style(items, "/settings/general", tab_is_active)
    assert style.startswith("--chirpui-pill-x:")
    assert "--chirpui-pill-w:" in style
    assert "--chirpui-pill-h:" in style
    assert "rem" in style


def test_nav_pill_inline_style_first_tab_active_at_zero() -> None:
    items = ({"label": "Home", "href": "/"}, {"label": "Docs", "href": "/docs"})
    style = nav_pill_inline_style(items, "/", tab_is_active)
    assert "--chirpui-pill-x:0" in style.split("--chirpui-pill-y")[0]


def test_segmented_pill_inline_style_uses_active_flag() -> None:
    items = (
        {"label": "Grid", "value": "grid"},
        {"label": "List", "value": "list", "active": True},
    )
    style = segmented_pill_inline_style(items)
    assert "--chirpui-pill-x:" in style
    assert not style.startswith("--chirpui-pill-x:0rem;")
