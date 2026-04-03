"""Tests for chirp_ui.route_tabs module."""

from kida import Environment

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


def test_tab_is_active_with_chirp_dict_shape() -> None:
    """Dict shape from Chirp's _tab_item_to_shell_dict works with tab_is_active."""
    tab = {
        "label": "Settings",
        "href": "/settings",
        "icon": "gear",
        "badge": "2",
        "match": "prefix",
    }
    assert tab_is_active(tab, "/settings") is True
    assert tab_is_active(tab, "/settings/wizard") is True
    assert tab_is_active(tab, "/admin") is False


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


def test_render_route_tabs_macro_renders_htmx_attrs(env: Environment) -> None:
    env.add_global("tab_is_active", tab_is_active)
    html = env.from_string(
        '{% from "chirpui/route_tabs.html" import render_route_tabs %}'
        '{{ render_route_tabs(tab_items, current_path, target="#page-root") }}'
    ).render(
        tab_items=(
            {"label": "Skills", "href": "/skills"},
            {"label": "Settings", "href": "/settings", "match": "prefix"},
        ),
        current_path="/settings/general",
    )

    assert 'hx-target="#page-root"' in html
    assert 'hx-push-url="true"' in html
    assert 'hx-boost="false"' in html
    assert 'hx-select="unset"' in html
    assert 'aria-current="page"' in html
    assert "chirpui-route-tab--active" in html


def test_route_tabs_alias_still_renders(env: Environment) -> None:
    env.add_global("tab_is_active", tab_is_active)
    html = env.from_string(
        '{% from "chirpui/route_tabs.html" import route_tabs %}{{ route_tabs(tabs, current_path) }}'
    ).render(
        tabs=({"label": "Workspace", "href": "/workspace"},),
        current_path="/workspace",
    )

    assert "Workspace" in html
    assert 'hx-target="#page-root"' in html


def test_tabbed_page_layout_template_exposes_contract_blocks(env: Environment) -> None:
    env.add_global("tab_is_active", tab_is_active)
    html = env.from_string(
        '{% extends "chirpui/tabbed_page_layout.html" %}'
        "{% block page_header %}<h1>Header</h1>{% end %}"
        '{% block page_toolbar %}<div class="toolbar">Toolbar</div>{% end %}'
        "{% block page_content %}<p>Body</p>{% end %}"
    ).render(
        tab_items=(
            {"label": "Workspace", "href": "/workspace"},
            {"label": "Settings", "href": "/settings", "match": "prefix"},
        ),
        current_path="/workspace",
    )

    assert 'id="page-root"' in html
    assert 'id="page-content-inner"' in html
    assert 'id="route-tabs"' in html
    assert "<h1>Header</h1>" in html
    assert "Toolbar" in html
    assert "<p>Body</p>" in html
