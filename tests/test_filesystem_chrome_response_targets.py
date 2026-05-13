"""Response-shape contracts for the filesystem app chrome fixture."""

import pytest
from chirp.testing import TestClient

from tests.fixtures.filesystem_chrome.app import create_app

pytestmark = pytest.mark.asyncio


async def get_text(path: str, headers: dict[str, str] | None = None) -> str:
    async with TestClient(create_app()) as client:
        response = await client.get(path, headers=headers or {})
    assert response.status == 200
    return response.text


async def test_filesystem_full_page_returns_shell_and_single_page_root():
    html = await get_text("/workspace")

    assert 'id="main"' in html
    assert 'id="page-content"' in html
    assert 'id="page-root"' in html
    assert 'data-testid="fs-workspace-view-title"' in html
    assert "New workspace run" in html


async def test_filesystem_shell_target_returns_page_content_and_shell_actions_oob():
    html = await get_text(
        "/admin",
        headers={"HX-Request": "true", "HX-Target": "main", "HX-Boosted": "true"},
    )

    assert 'id="page-content"' in html
    assert 'id="page-root"' in html
    assert 'id="chirp-shell-actions" hx-swap-oob="innerHTML"' in html
    assert "Invite admin" in html
    assert 'data-testid="fs-admin-view-title"' in html


async def test_filesystem_page_root_target_returns_page_chrome_fragment():
    html = await get_text(
        "/workspace/runs",
        headers={"HX-Request": "true", "HX-Target": "page-root"},
    )

    assert 'id="main"' not in html
    assert 'id="page-content"' not in html
    assert 'id="chirp-shell-actions"' in html
    assert 'hx-swap-oob="innerHTML"' in html
    assert 'id="route-tabs"' in html
    assert 'id="page-content-inner"' in html
    assert 'data-testid="fs-workspace-view-title"' in html
    assert "Workspace runs" in html


async def test_filesystem_inner_fragment_target_returns_local_fragment_only():
    html = await get_text(
        "/workspace/filter_fragment",
        headers={"HX-Request": "true", "HX-Target": "page-content-inner"},
    )

    assert 'id="main"' not in html
    assert 'id="page-root"' not in html
    assert 'id="chirp-shell-actions"' not in html
    assert 'data-testid="fs-filter-result"' in html
