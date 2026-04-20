"""Regression tests for kida 0.7.0 strict_undefined=True compliance.

These render dict-iterating components with the MINIMAL required fields
(per macro docstring) and assert they don't raise UndefinedError.

If a new component ships with `{% if item.foo %}` style guards on
optional keys, add a test here so strict-mode breakage is caught fast.
"""

from kida import Environment


def _render(env: Environment, src: str) -> str:
    return env.from_string(src, name="strict_probe").render()


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


def test_route_tabs_minimal_tab(env: Environment) -> None:
    from chirp_ui.route_tabs import tab_is_active

    env.add_global("tab_is_active", tab_is_active)
    out = _render(
        env,
        '{% from "chirpui/route_tabs.html" import render_route_tabs %}'
        '{{ render_route_tabs(tab_items=[{}], current_path="/") }}',
    )
    assert "chirpui-route-tab" in out


def test_nav_tree_minimal_item(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/nav_tree.html" import nav_tree %}{{ nav_tree(items=[{}]) }}',
    )
    assert "chirpui-nav-tree" in out


def test_tree_view_minimal_node(env: Environment) -> None:
    out = _render(
        env,
        '{% from "chirpui/tree_view.html" import tree_view %}{{ tree_view(nodes=[{}]) }}',
    )
    assert "chirpui-tree__item" in out


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
