from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials"


def _partial(name: str) -> str:
    return (PARTIALS / name).read_text(encoding="utf-8")


def test_app_shell_collapses_to_single_column_on_phone_widths() -> None:
    tokens = _partial("002_reset.css")
    css = _partial("083_app-shell.css")
    sidebar = _partial("084_app-shell-sidebar.css")

    assert "--chirpui-sidebar-mobile-max-block-size: min(40dvh, 12rem);" in tokens
    assert "@media (max-width: 48rem)" in css
    assert (
        'grid-template-areas:\n            "topbar"\n            "sidebar"\n            "main";'
        in css
    )
    assert ".chirpui-app-shell__sidebar" in css
    assert "overflow-x: auto;" in css
    assert "overflow-y: auto;" in css
    assert "max-block-size: var(--chirpui-sidebar-mobile-max-block-size);" in css
    assert (
        ".chirpui-app-shell__sidebar .chirpui-sidebar__section-links :where(div, nav, ul, ol)"
        in css
    )
    assert (
        ".chirpui-app-shell__sidebar :where(.chirpui-sidebar__link, .chirpui-nav-tree__link)" in css
    )
    assert ".chirpui-app-shell--sidebar-collapsed .chirpui-sidebar__label" in css
    assert "@media (max-width: 48rem)" in sidebar
    assert ".chirpui-app-shell__sidebar .chirpui-sidebar__section-links" in sidebar
    assert "flex-direction: row;" in sidebar


def test_navigation_strips_scroll_horizontally_on_phone_widths() -> None:
    route_tabs = _partial("062_route-tabs.css")
    primary_nav = _partial("161_navigation-metadata-authoring.css")

    assert "@media (max-width: 40rem)" in route_tabs
    assert ".chirpui-route-tabs" in route_tabs
    assert "flex-wrap: nowrap;" in route_tabs
    assert "scroll-snap-type: x proximity;" in route_tabs

    assert "@media (max-width: 40rem)" in primary_nav
    assert ".chirpui-primary-nav" in primary_nav
    assert "flex-wrap: nowrap;" in primary_nav
    assert "scroll-snap-type: x proximity;" in primary_nav


def test_touch_targets_expand_on_phone_and_coarse_pointer_widths() -> None:
    tokens = _partial("002_reset.css")
    app_shell = _partial("083_app-shell.css")
    button = _partial("071_button.css")
    forms = _partial("070_form-fields.css")
    route_tabs = _partial("062_route-tabs.css")
    primary_nav = _partial("161_navigation-metadata-authoring.css")
    theme_toggle = _partial("063_theme-toggle.css")

    assert "--chirpui-control-touch-target: 2.5rem;" in tokens
    assert "--chirpui-control-block-size: 2.5rem;" in tokens
    assert "--chirpui-control-block-size-sm: 2rem;" in tokens
    assert ".chirpui-app-shell__topbar :where(a, button, select, input)" in app_shell
    assert "min-block-size: var(--chirpui-control-touch-target);" in app_shell
    assert "@media (max-width: 48rem), (pointer: coarse)" in button
    assert "@media (max-width: 48rem), (pointer: coarse)" in forms
    assert '.chirpui-field__input:not([type="checkbox"]):not([type="radio"])' in forms
    assert "min-block-size: var(--chirpui-control-touch-target);" in route_tabs
    assert "min-block-size: var(--chirpui-control-touch-target);" in primary_nav
    assert "min-inline-size: var(--chirpui-control-touch-target);" in theme_toggle


def test_single_line_controls_share_baseline_block_size() -> None:
    button = _partial("071_button.css")
    forms = _partial("070_form-fields.css")
    dropdown = _partial("064_dropdown-menu.css")
    pagination = _partial("060_pagination.css")
    theme_toggle = _partial("063_theme-toggle.css")
    ascii_toggle = _partial("143_ascii-toggle.css")

    assert "min-block-size: var(--chirpui-control-block-size);" in button
    assert ".chirpui-btn--sm" in button
    assert "min-block-size: var(--chirpui-control-block-size-sm);" in button
    assert (
        '.chirpui-field__input:not(textarea):not([type="checkbox"]):not([type="radio"]):not([multiple])'
        in forms
    )
    assert "min-block-size: var(--chirpui-control-block-size);" in dropdown
    assert "min-inline-size: var(--chirpui-control-block-size);" in pagination
    assert "min-block-size: var(--chirpui-control-block-size);" in theme_toggle
    assert "min-block-size: var(--chirpui-control-block-size);" in ascii_toggle


def test_tables_and_rendered_content_have_mobile_overflow_guards() -> None:
    table = _partial("059_table.css")
    rendered_content = _partial("161_navigation-metadata-authoring.css")

    assert ".chirpui-table-wrap" in table
    assert "-webkit-overflow-scrolling: touch;" in table
    assert "width: max-content;" in table
    assert "overflow-wrap: anywhere;" in table

    assert ".chirpui-rendered-content :where(a, code)" in rendered_content
    assert ".chirpui-rendered-content :where(img, video, iframe, embed, object)" in rendered_content
