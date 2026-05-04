"""Integration tests for component-showcase data page.

Requires chirp (pip install chirp or uv sync --group showcase).
"""

import sys
import warnings
from pathlib import Path

import pytest

from chirp_ui.validation import ChirpUIDeprecationWarning, ChirpUIValidationWarning

pytest.importorskip("chirp")

from chirp.testing import TestClient

_SHOWCASE_DIR = Path(__file__).resolve().parent.parent / "examples" / "component-showcase"


@pytest.fixture
def showcase_app():
    """Load the component-showcase app."""
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    from app import app

    return app


class TestDataPage:
    """Verify /data and /data/table routes return 200 and expected HTML."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "path",
        [
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
        ],
    )
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

    @pytest.mark.asyncio
    async def test_data_page_returns_200(self, showcase_app) -> None:
        async with TestClient(showcase_app) as client:
            response = await client.get("/data")
            assert response.status == 200
            assert "Data Display" in response.text
            assert 'id="data_table_content"' in response.text
            assert "chirpui-spinner" in response.text

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
