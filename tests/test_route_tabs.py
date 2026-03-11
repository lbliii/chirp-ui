"""Tests for chirp_ui.route_tabs module."""

from chirp_ui.route_tabs import tab_is_active


def test_tab_is_active_exact_match() -> None:
    tab = {"label": "Skills", "href": "/skills"}
    assert tab_is_active(tab, "/skills") is True
    assert tab_is_active(tab, "/skills/foo") is False
    assert tab_is_active(tab, "/shortcuts") is False


def test_tab_is_active_prefix_match() -> None:
    tab = {"label": "Settings", "href": "/settings", "match": "prefix"}
    assert tab_is_active(tab, "/settings") is True
    assert tab_is_active(tab, "/settings/general") is True
    assert tab_is_active(tab, "/settings/collections/foo") is True
    assert tab_is_active(tab, "/shortcuts") is False


def test_tab_is_active_with_dataclass() -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True, slots=True)
    class RouteTab:
        label: str
        href: str
        match: str = "exact"

    tab = RouteTab(label="Chains", href="/chains")
    assert tab_is_active(tab, "/chains") is True
    assert tab_is_active(tab, "/chains/abc") is False

    prefix_tab = RouteTab(label="Settings", href="/settings", match="prefix")
    assert tab_is_active(prefix_tab, "/settings") is True
    assert tab_is_active(prefix_tab, "/settings/wizard") is True
