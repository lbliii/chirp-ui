"""Integration tests for component-showcase data page.

Requires chirp (pip install chirp or uv sync --group showcase).
"""

from __future__ import annotations

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
