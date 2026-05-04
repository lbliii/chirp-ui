"""Integration tests for component-showcase data page.

Requires chirp (pip install chirp or uv sync --group showcase).
"""

import ast
import re
import sys
import warnings
from pathlib import Path

import pytest

from chirp_ui.validation import ChirpUIDeprecationWarning, ChirpUIValidationWarning

pytest.importorskip("chirp")

from chirp.testing import TestClient

_SHOWCASE_DIR = Path(__file__).resolve().parent.parent / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"

SHOWCASE_ROUTE_SMOKE_PATHS = (
    "/",
    "/demo",
    "/htmx",
    "/navigation",
    "/layout",
    "/chrome",
    "/shell-actions",
    "/sections",
    "/carousel",
    "/cards",
    "/forms",
    "/ui",
    "/islands",
    "/islands/grid-state",
    "/islands/wizard-state",
    "/islands/upload-state",
    "/streaming",
    "/data-display",
    "/calendar",
    "/calendar/2026/5",
    "/calendar/2026/05",
    "/data",
    "/effects",
    "/typography",
    "/ascii-primitives",
    "/buttons",
    "/dashboard",
    "/animation",
    "/ascii",
    "/messenger",
    "/social",
    "/video",
    "/data/table?page=1&sort=name",
    "/data/bulk-bar",
    "/data/export",
    "/layout/dir?dir=rtl",
    "/animation/swap-demo",
    "/islands/remount",
)

SHOWCASE_FRAGMENT_OR_ACTION_ROUTES = {
    "/toast",
    "/demo/submit",
    "/demo/stream",
    "/forms/demo",
    "/ui/tab/{name}",
    "/streaming/demo",
    "/data/table",
    "/data/bulk-bar",
    "/data/export",
    "/layout/dir",
    "/animation/swap-demo",
}


def _showcase_route_patterns() -> set[str]:
    patterns: set[str] = set()
    for line in _SHOWCASE_APP.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("@app.route("):
            continue
        expr = ast.parse(line[1:]).body[0].value
        patterns.add(ast.literal_eval(expr.args[0]))
    return patterns


def _route_pattern_matches(pattern: str, path: str) -> bool:
    path = path.split("?", 1)[0]
    regex = re.escape(pattern)
    regex = re.sub(r"\\\{[^/]+\\\}", r"[^/]+", regex)
    return re.fullmatch(regex, path) is not None

ISLAND_ROUTE_SMOKE_PATHS = (
    "/islands",
    "/islands/grid-state",
    "/islands/wizard-state",
    "/islands/upload-state",
    "/islands/remount",
)

ISLAND_TEMPLATE_PATHS = (
    "showcase/islands.html",
    "showcase/islands_grid_state.html",
    "showcase/islands_wizard_state.html",
    "showcase/islands_upload_state.html",
)


@pytest.fixture
def showcase_app():
    """Load the component-showcase app."""
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    from app import app

    return app


class TestDataPage:
    """Verify /data and /data/table routes return 200 and expected HTML."""

    def test_showcase_page_routes_have_smoke_representatives(self) -> None:
        missing = sorted(
            route
            for route in _showcase_route_patterns() - SHOWCASE_FRAGMENT_OR_ACTION_ROUTES
            if not any(_route_pattern_matches(route, path) for path in SHOWCASE_ROUTE_SMOKE_PATHS)
        )
        assert not missing, "Showcase page routes missing route-smoke coverage: " + ", ".join(
            missing
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("path", SHOWCASE_ROUTE_SMOKE_PATHS)
    async def test_showcase_routes_return_200(self, showcase_app, path: str) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ChirpUIValidationWarning)
            warnings.simplefilter("always", ChirpUIDeprecationWarning)
            async with TestClient(showcase_app) as client:
                response = await client.get(path)
        assert response.status == 200
        chirp_warnings = [
            warning
            for warning in caught
            if issubclass(warning.category, (ChirpUIValidationWarning, ChirpUIDeprecationWarning))
        ]
        assert not chirp_warnings, f"{path} emitted chirp-ui warnings: " + "; ".join(
            str(warning.message) for warning in chirp_warnings
        )

    @pytest.mark.asyncio
    async def test_navigation_page_returns_dense_example(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/navigation")
            assert response.status == 200
            assert "Dense Object Navigation" in response.text
            assert "Project workspace navigation" in response.text
            assert "Settings workspace navigation" in response.text
            assert "Cloud Console Navigation" in response.text
            assert "Cloud console global navigation" in response.text
            assert "Cloud console favorites" in response.text
            assert "Suite Work Hub Navigation" in response.text
            assert "Suite work hub global navigation" in response.text
            assert "Suite work hub personal shortcuts" in response.text
            assert "Suite work hub saved views" in response.text
            assert "Ops Console Navigation" in response.text
            assert "Ops console global navigation" in response.text
            assert "Ops dashboard controls" in response.text
            assert "Jump to dashboard, log, trace" in response.text
            assert "Keyboard-First Tracker Navigation" in response.text
            assert "Tracker global navigation" in response.text
            assert "Tracker display controls" in response.text
            assert "Go to issue, project, view" in response.text
            assert "Knowledge Workspace Navigation" in response.text
            assert "Knowledge workspace global navigation" in response.text
            assert "Knowledge page controls" in response.text
            assert "Search or jump to page" in response.text
            assert "Editor Workbench Navigation" in response.text
            assert "Editor workbench global navigation" in response.text
            assert "Editor tool navigation" in response.text
            assert "Find file, frame, action" in response.text
            assert "Business Object Console Navigation" in response.text
            assert "Business object console global navigation" in response.text
            assert "Business object list controls" in response.text
            assert "Search customers, invoices, IDs" in response.text
            assert "Collaboration Inbox Navigation" in response.text
            assert "Collaboration inbox global navigation" in response.text
            assert "Collaboration inbox controls" in response.text
            assert "Jump to channel, DM, thread" in response.text
            assert "Developer Platform Navigation" in response.text
            assert "Developer platform global navigation" in response.text
            assert "Developer platform list controls" in response.text
            assert "Search or go to project, issue, MR" in response.text
            assert "Reference Docs Navigation" in response.text
            assert "Reference docs global navigation" in response.text
            assert "Reference docs page controls" in response.text
            assert "Search docs or jump to topic" in response.text
            assert "chirpui-breadcrumbs__overflow" in response.text
            assert "chirpui-route-tab__badge" in response.text
            assert "chirpui-route-tab__badge--reserved" in response.text
            assert "chirpui-sidebar__badge--loading" in response.text
            assert "chirpui-scope-switcher" in response.text
            assert "chirpui-saved-view-strip" in response.text
            assert "chirpui-command-palette-trigger--sm" in response.text
            assert "Find service, project, deployment" in response.text
            assert "Search work, people, projects" in response.text
            assert response.text.count("chirpui-frame--sidebar-start") >= 8
            assert "data-showcase-nav-shell-frame" not in response.text
            assert "data-showcase-nav-sidebar-viewport" not in response.text
            assert "/static/chirpui-logo.svg" in response.text
            logo_response = await client.get("/static/chirpui-logo.svg")
            assert logo_response.status == 200
            assert "<svg" in logo_response.text

    @pytest.mark.asyncio
    async def test_htmx_page_does_not_emit_demo_toasts_on_load(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/htmx")
        assert response.status == 200
        toast_section = response.text.split("<h3>oob_toast</h3>", 1)[1].split(
            "<h3>counter_badge</h3>", 1
        )[0]
        assert "oob_toast(&quot;Item saved!&quot;" in toast_section
        assert 'hx-swap-oob="beforeend:#chirpui-toasts"' not in toast_section

    @pytest.mark.asyncio
    async def test_effects_page_wraps_background_macros_with_canvas_height(
        self, showcase_app
    ) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/effects")
        assert response.status == 200
        html = response.text

        for root_class in (
            "chirpui-aurora",
            "chirpui-meteor",
            "chirpui-particle-bg",
            "chirpui-symbol-rain",
            "chirpui-holy-light",
            "chirpui-rune-field",
            "chirpui-constellation",
            "chirpui-scanline",
            "chirpui-grain",
        ):
            assert re.search(
                rf'class="{root_class}(?:[" ]|--).*?data-showcase-effect-fill',
                html,
                re.S,
            ), f"{root_class} showcase demo must call the wrapper macro with height"

        for replayable_class in (
            "chirpui-hover-wobble",
            "chirpui-hover-jello",
            "chirpui-hover-rubber",
        ):
            assert replayable_class in html

    @pytest.mark.asyncio
    @pytest.mark.parametrize("path", ISLAND_ROUTE_SMOKE_PATHS)
    async def test_island_showcase_routes_return_200(self, showcase_app, path: str) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ChirpUIValidationWarning)
            warnings.simplefilter("always", ChirpUIDeprecationWarning)
            async with TestClient(showcase_app) as client:
                response = await client.get(path)
        assert response.status == 200
        chirp_warnings = [
            warning
            for warning in caught
            if issubclass(warning.category, (ChirpUIValidationWarning, ChirpUIDeprecationWarning))
        ]
        assert not chirp_warnings, f"{path} emitted chirp-ui warnings: " + "; ".join(
            str(warning.message) for warning in chirp_warnings
        )

    def test_island_showcase_templates_use_composed_patterns(self) -> None:
        stale_patterns = {
            "inline style": r"\bstyle=",
            "direct card class": r'cls="chirpui-card"',
            "raw back link": r"<p><a href=",
            "missing field modifier": r"chirpui-field--file",
        }
        for rel_path in ISLAND_TEMPLATE_PATHS:
            template = (_SHOWCASE_DIR / "templates" / rel_path).read_text(encoding="utf-8")
            for label, pattern in stale_patterns.items():
                assert not re.search(pattern, template), (
                    f"{rel_path} still uses stale island showcase pattern: {label}"
                )

    @pytest.mark.asyncio
    async def test_data_page_returns_200(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data")
            assert response.status == 200
            assert "Data Display" in response.text
            assert 'id="data_table_content"' in response.text
            assert "chirpui-spinner" in response.text
            assert "chirpui-field--dense" in response.text
            assert "style=\"min-width" not in response.text

    @pytest.mark.asyncio
    async def test_data_table_fragment_returns_200(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?page=1&sort=name")
            assert response.status == 200
            assert "chirpui-table" in response.text
            assert "Alice" in response.text
            assert "chirpui-pagination" in response.text
            assert "Showing" in response.text

    @pytest.mark.asyncio
    async def test_data_table_search_returns_filtered(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?q=alice&role=")
            assert response.status == 200
            assert "Alice" in response.text
            assert "Bob" not in response.text

    @pytest.mark.asyncio
    async def test_data_table_empty_search_shows_empty_state(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data/table?q=nonexistentxyz&role=")
            assert response.status == 200
            assert "chirpui-empty-state" in response.text
            assert "No results" in response.text

    @pytest.mark.asyncio
    async def test_data_bulk_bar_and_export_accept_selected_values(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            bulk_response = await client.get(
                "/data/bulk-bar?selected=alice@example.com&selected=bob@example.com"
            )
            assert bulk_response.status == 200
            assert "2 selected" in bulk_response.text

            export_response = await client.get(
                "/data/export?selected=alice@example.com,bob@example.com"
            )
            assert export_response.status == 200
            assert "Alice,alice@example.com" in export_response.text
            assert "Bob,bob@example.com" in export_response.text
            assert "Carol" not in export_response.text
