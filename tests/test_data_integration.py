"""Integration tests for component-showcase data page.

Requires chirp (pip install chirp or uv sync --group showcase).
"""

import sys
from pathlib import Path

import pytest

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
            assert "chirpui-breadcrumbs__overflow" in response.text
            assert "chirpui-route-tab__badge" in response.text
            assert "chirpui-route-tab__badge--reserved" in response.text
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
