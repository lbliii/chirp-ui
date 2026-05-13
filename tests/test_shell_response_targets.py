"""Server response-shape contracts for app-shell HTMX targets."""

import pytest
from chirp.testing import TestClient

from tests.browser.app import create_app

pytestmark = pytest.mark.asyncio


async def get_text(path: str, headers: dict[str, str] | None = None) -> str:
    async with TestClient(create_app()) as client:
        response = await client.get(path, headers=headers or {})
    assert response.status == 200
    return response.text


async def test_shell_target_returns_full_page_with_page_content_and_shell_oob():
    html = await get_text(
        "/consumer-admin",
        headers={"HX-Request": "true", "HX-Target": "main"},
    )

    assert 'id="page-content"' in html
    assert 'id="page-root"' in html
    assert 'id="chirp-shell-actions" hx-swap-oob="innerHTML"' in html
    assert "Invite member" in html
    assert 'data-testid="consumer-admin-view-title"' in html


async def test_page_root_target_returns_page_chrome_fragment_only():
    html = await get_text(
        "/consumer-admin/jobs",
        headers={"HX-Request": "true", "HX-Target": "page-root"},
    )

    assert 'id="page-content"' not in html
    assert 'id="chirp-shell-actions"' not in html
    assert 'id="route-tabs"' in html
    assert 'data-testid="consumer-admin-view-title"' in html
    assert "Background jobs" in html


async def test_hx_request_without_page_root_target_does_not_get_page_root_fragment():
    html = await get_text(
        "/consumer-workspace/runs",
        headers={"HX-Request": "true", "HX-Target": "main"},
    )

    assert 'id="page-content"' in html
    assert 'id="chirp-shell-actions" hx-swap-oob="innerHTML"' in html
    assert "Workspace runs" in html


async def test_inner_fragment_target_returns_local_fragment_only():
    html = await get_text(
        "/consumer-workspace/filter-fragment",
        headers={"HX-Request": "true", "HX-Target": "page-content-inner"},
    )

    assert 'id="page-content"' not in html
    assert 'id="page-root"' not in html
    assert 'id="chirp-shell-actions"' not in html
    assert 'data-testid="consumer-filter-result"' in html
