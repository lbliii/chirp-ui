from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials"


def _partial(name: str) -> str:
    return (PARTIALS / name).read_text(encoding="utf-8")


def test_application_chrome_navigation_uses_control_block_tokens() -> None:
    route_tabs = _partial("062_route-tabs.css")
    primary_nav = _partial("161_navigation-metadata-authoring.css")
    sidebar = _partial("029_sidebar.css")

    assert ".chirpui-route-tab" in route_tabs
    assert "min-block-size: var(--chirpui-control-block-size-sm);" in route_tabs
    assert ".chirpui-primary-nav__link" in primary_nav
    assert "min-block-size: var(--chirpui-control-block-size-sm);" in primary_nav
    assert ".chirpui-primary-nav__divider" in primary_nav
    assert "block-size: var(--chirpui-control-block-size-sm);" in primary_nav
    assert ".chirpui-sidebar__link" in sidebar
    assert "min-block-size: var(--chirpui-control-block-size-sm);" in sidebar


def test_application_chrome_overlay_close_controls_use_token_sized_targets() -> None:
    drawer = _partial("053_drawer.css")
    tray = _partial("065_tray.css")

    for css in [drawer, tray]:
        assert "min-inline-size: var(--chirpui-control-block-size-sm);" in css
        assert "min-block-size: var(--chirpui-control-block-size-sm);" in css
        assert "outline: var(--chirpui-state-focus-outline);" in css
