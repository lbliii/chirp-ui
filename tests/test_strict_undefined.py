"""Regression tests for kida strict_undefined=True compliance.

These render dict-iterating components with the MINIMAL required fields
(per macro docstring) and assert they don't raise UndefinedError.

If a new component ships with `{% if item.foo %}` style guards on
optional keys, add a test here so strict-mode breakage is caught fast.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest
from kida import Environment, FileSystemLoader
from kida.template import Markup

from chirp_ui.filters import (
    build_hx_attrs,
    check_required_id,
    contrast_text,
    deprecate_param,
    make_route_link_attrs,
    resolve_color,
    resolve_status_variant,
    sanitize_color,
    shell_action_btn_variant,
    value_type,
)
from chirp_ui.icons import icon as icon_filter

_ROOT = Path(__file__).resolve().parent.parent
_CHIRPUI_TEMPLATES = _ROOT / "src" / "chirp_ui" / "templates"
_THEME_TEMPLATES = _ROOT / "src" / "bengal_themes" / "chirp_theme" / "templates"

# Load conftest's filter stubs by file path (not importable as a bare module).
_conftest_path = Path(__file__).parent / "conftest.py"
_conftest_spec = importlib.util.spec_from_file_location("_conftest", _conftest_path)
_conftest = importlib.util.module_from_spec(_conftest_spec)
sys.modules["_conftest"] = _conftest
_conftest_spec.loader.exec_module(_conftest)


def _render(env: Environment, src: str, **ctx: Any) -> str:
    return env.from_string(src, name="strict_probe").render(**ctx)


@pytest.fixture
def theme_env() -> Environment:
    """Kida env that resolves chirp-theme partials AND chirpui macros.

    Stubs the Bengal-provided filters/globals the track partials depend on
    (content embedding, ``merge``, ``items``, the theme ``icon()`` global)
    so the self-contained track macros can render without a full site build.
    """
    e = Environment(
        loader=FileSystemLoader([str(_THEME_TEMPLATES), str(_CHIRPUI_TEMPLATES)]),
        autoescape=True,
    )
    e.update_filters(
        {
            "field_errors": _conftest._field_errors_stub,
            "bem": _conftest._bem_stub,
            "html_attrs": _conftest._html_attrs_stub,
            "icon": icon_filter,
            "validate_variant": _conftest._validate_variant_stub,
            "validate_variant_block": _conftest._validate_variant_block_stub,
            "validate_appearance_block": _conftest._validate_appearance_block_stub,
            "validate_tone_block": _conftest._validate_tone_block_stub,
            "validate_size": _conftest._validate_size_stub,
            "value_type": value_type,
            "sanitize_color": sanitize_color,
            "contrast_text": contrast_text,
            "resolve_color": resolve_color,
            "deprecate_param": deprecate_param,
            "resolve_status_variant": resolve_status_variant,
            "shell_action_btn_variant": shell_action_btn_variant,
        }
    )
    # Bengal-provided filters used by the track partials.
    e.add_filter("resolve_links_for_embedding", lambda html, page=None: html)
    e.add_filter("demote_headings", lambda html, levels=1: html)
    e.add_filter("prefix_heading_ids", lambda html, prefix="": html)
    e.add_filter("merge", lambda d1, d2, deep=True: {**(d1 or {}), **(d2 or {})})
    e.add_filter("items", lambda d: list((d or {}).items()))
    e.add_filter("absolute_url", lambda u: u)
    e.add_global("build_hx_attrs", build_hx_attrs)
    e.add_global("check_required_id", check_required_id)
    e.add_global("route_link_attrs", make_route_link_attrs())
    # The theme's icon() GLOBAL accepts size=; the chirp_ui icon FILTER does not.
    e.add_global("icon", lambda name, size=16, **kw: Markup(f'<svg data-icon="{name}"></svg>'))
    # No page resolves -> exercises the "missing"/fallback branches.
    e.add_global("get_page", lambda slug: None)
    return e


def test_mapping_optional_chain_missing_key_renders_empty(env: Environment) -> None:
    """Kida 0.8+ makes Mapping optional-chain misses soft under strict mode."""
    out = _render(env, "{{ params?.description }}", params={})
    assert out == ""


def test_timeline_minimal_item(env: Environment) -> None:
    out = _render(
        env, '{% from "chirpui/timeline.html" import timeline %}{{ timeline(items=[{}]) }}'
    )
    assert "chirpui-timeline__item" in out


def test_dock_minimal_item(env: Environment) -> None:
    out = _render(env, '{% from "chirpui/dock.html" import dock %}{{ dock(items=[{}]) }}')
    assert "chirpui-dock__item" in out


def test_segmented_control_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/segmented_control.html" import segmented_control %}'
        '{{ segmented_control(items=[{}], name="t") }}',
    )
    assert "chirpui-segmented__option" in out


def test_context_menu_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/context_menu.html" import context_menu %}'
        "{% call context_menu(items=[{}]) %}<span>x</span>{% end %}",
    )
    assert "chirpui-context-menu__item" in out


def test_combobox_minimal_option(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/combobox.html" import combobox %}{{ combobox(name="t", options=[{}]) }}',
    )
    assert "chirpui-combobox__option" in out


def test_toggle_group_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/toggle_group.html" import toggle_group %}'
        '{{ toggle_group(items=[{}], name="t") }}',
    )
    assert "chirpui-toggle-group__item" in out


def test_route_tabs_minimal_tab(env: Environment) -> None:
    from chirp_ui.route_tabs import tab_is_active

    env.add_global("tab_is_active", tab_is_active)
    out = _render(
        env,
        '{% from "chirpui/route_tabs.html" import render_route_tabs %}'
        '{{ render_route_tabs(tab_items=[{}], current_path="/") }}',
    )
    assert "chirpui-route-tab" in out


def test_route_tabs_minimal_expected_badge(env: Environment) -> None:
    from chirp_ui.route_tabs import tab_is_active

    env.add_global("tab_is_active", tab_is_active)
    out = _render(
        env,
        '{% from "chirpui/route_tabs.html" import render_route_tabs %}'
        '{{ render_route_tabs(tab_items=[{"badge_expected": true}], current_path="/") }}',
    )
    assert "chirpui-route-tab__badge--reserved" in out


def test_primary_nav_minimal_expected_badge(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/primary_nav.html" import primary_nav %}'
        '{{ primary_nav(items=[{"badge_expected": true}]) }}',
    )
    assert "chirpui-primary-nav__badge--reserved" in out


def test_sidebar_link_minimal_expected_badge(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/sidebar.html" import sidebar_link %}'
        '{{ sidebar_link("/", "Home", badge_expected=true) }}',
    )
    assert "chirpui-sidebar__badge--reserved" in out


def test_scope_switcher_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/scope_switcher.html" import scope_switcher %}'
        '{{ scope_switcher("Scope", items=[{}]) }}',
    )
    assert "chirpui-scope-switcher" in out


def test_saved_view_strip_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/saved_view_strip.html" import saved_view_strip %}'
        "{{ saved_view_strip(views=[{}]) }}",
    )
    assert "chirpui-saved-view-strip" in out


def test_nav_tree_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/nav_tree.html" import nav_tree %}{{ nav_tree(items=[{}]) }}',
    )
    assert "chirpui-nav-tree" in out


def test_media_hero_shelf_title_only_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/media_patterns.html" import media_hero_shelf %}'
        '{{ media_hero_shelf(items=[{"href": "/watch", "title": "Only title"}]) }}',
    )
    assert "Only title" in out
    assert "chirpui-media-hero-shelf" in out


def test_tree_view_minimal_node(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/tree_view.html" import tree_view %}{{ tree_view(nodes=[{}]) }}',
    )
    assert "chirpui-tree__item" in out


def test_data_grid_minimal_column_dict(env: Environment) -> None:
    # An empty {} column dict must coerce through sort_columns into a ColumnSort
    # with empty key/label and render without UndefinedError (kida 0.7.0).
    out = _render(
        env,
        '{% from "chirpui/data_grid.html" import data_grid %}'
        "{% set cols = sort_columns([{}], parse_sort('', default_key=''), '/x') %}"
        "{{ data_grid(columns=cols, rows=[['a']], row_ids=['1'], "
        "sort_url='/x', selection_id='g') }}",
    )
    assert "chirpui-data-grid" in out


def test_bar_chart_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/bar_chart.html" import bar_chart %}{{ bar_chart(items=[{}], max=10) }}',
    )
    assert "chirpui-bar-chart__row" in out


def test_breadcrumbs_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}{{ breadcrumbs(items=[{}]) }}',
    )
    assert "chirpui-breadcrumbs__item" in out


def test_breadcrumbs_overflow_minimal_items(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/breadcrumbs.html" import breadcrumbs %}'
        "{{ breadcrumbs(items=[{}, {}, {}, {}, {}], overflow='collapse') }}",
    )
    assert "chirpui-breadcrumbs__overflow" in out


def test_description_list_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/description_list.html" import description_list %}'
        "{{ description_list(items=[{}]) }}",
    )
    assert "chirpui-dl__row" in out


def test_select_field_minimal_option(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/forms.html" import select_field %}'
        '{{ select_field(name="t", options=[{}]) }}',
    )
    assert "<option" in out


def test_config_form_minimal_field(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/forms.html" import config_form %}'
        '{{ config_form([{"name": "x", "widget": "text"}], action="/save") }}',
    )
    assert 'name="x"' in out


def test_param_field_minimal(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/param_override.html" import param_field %}'
        '{{ param_field(name="temperature") }}',
    )
    assert "chirpui-param" in out


def test_message_meta_empty_usage(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/message_meta.html" import message_meta %}'
        '{{ message_meta(model="gpt-4o", usage={}) }}',
    )
    assert "gpt-4o" in out
    assert "chirpui-message-meta__usage" not in out


def test_tool_call_card_empty_args(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/reasoning.html" import tool_call_card %}'
        '{{ tool_call_card("run", args=[{}], files=[]) }}',
    )
    assert "chirpui-tool-call" in out


def test_status_step_minimal(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/status_timeline.html" import status_step %}'
        '{{ status_step(action_type="x", label="y") }}',
    )
    assert "chirpui-status-step" in out


def test_sources_summary_empty_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/citations.html" import sources_summary %}'
        "{{ sources_summary([{}]) }}",
    )
    assert "chirpui-sources-summary" in out


def test_shortcuts_help_minimal(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/shortcuts_help.html" import shortcuts_help %}'
        "{{ shortcuts_help() }}",
    )
    assert "chirpui-shortcuts-help" in out


def test_radio_field_minimal_option(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/forms.html" import radio_field %}'
        '{{ radio_field(name="t", options=[{}]) }}',
    )
    assert 'type="radio"' in out


def test_segmented_control_field_minimal_option(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/forms.html" import segmented_control_field %}'
        '{{ segmented_control_field(name="t", options=[{}]) }}',
    )
    assert "chirpui-segmented__label" in out


def test_multi_select_field_minimal_option(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/forms.html" import multi_select_field %}'
        '{{ multi_select_field(name="t", options=[{}], selected=[]) }}',
    )
    assert "<option" in out


def test_dropdown_menu_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/dropdown_menu.html" import dropdown_menu %}'
        '{{ dropdown_menu("Trigger", items=[{}]) }}',
    )
    assert "chirpui-dropdown__item" in out


# --- chirp-theme track templates (issue #140) ----------------------------------
# The data-file track pillar page reads site.data.tracks[id]; guard the empty
# `{}` track + empty member-page cases so strict_undefined never crashes a build.


def test_track_section_block_empty_page(theme_env: Environment) -> None:
    """A track member page with NO fields still renders a section shell."""
    out = _render(
        theme_env,
        '{% from "partials/track-helpers.html" import track_section_block %}'
        "{{ track_section_block({}, 1, true) }}",
    )
    assert 'id="track-section-1"' in out
    assert "chirp-theme-track-section__title" in out


def test_track_section_missing_placeholder(theme_env: Environment) -> None:
    out = _render(
        theme_env,
        '{% from "partials/track-helpers.html" import track_section_missing %}'
        '{{ track_section_missing("", 1) }}',
    )
    assert "chirp-theme-track-section--missing" in out
    assert 'id="track-section-1"' in out


def test_track_progress_indicator_zero_steps(theme_env: Environment) -> None:
    """Zero-length track => no progressbar (no division/range errors)."""
    out = _render(
        theme_env,
        '{% from "partials/track-helpers.html" import track_progress_indicator %}'
        "{{ track_progress_indicator(0, 1) }}",
    )
    assert "chirp-theme-track-progress" not in out


def test_track_progress_indicator_renders_steps(theme_env: Environment) -> None:
    out = _render(
        theme_env,
        '{% from "partials/track-helpers.html" import track_progress_indicator %}'
        "{{ track_progress_indicator(3, 2) }}",
    )
    assert "chirp-theme-track-progress__step--current" in out
