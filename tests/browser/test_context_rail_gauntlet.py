"""Browser gauntlet for the route-context rail (#195).

Proves the region contract end-to-end: the rail is docked at desktop width and
stacked-but-present on phones (no horizontal overflow), its content swaps on
boosted navigation via the OOB fragment, and a route that ships no fragment has
the rail emptied by shell_runtime_script's stale-clear (the keystone behavior).
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def _no_horizontal_overflow(page) -> bool:
    return await page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")


async def test_rail_docked_at_desktop_width(page, base_url):
    await page.set_viewport_size({"width": 1280, "height": 800})
    await page.goto(base_url + "/ctx")
    await wait_for_alpine(page)

    rail = page.locator("#chirpui-context-rail")
    await expect(rail).to_be_visible()
    await expect(rail).to_contain_text("Context A")
    assert await _no_horizontal_overflow(page)


async def test_rail_present_and_no_overflow_at_320px(page, base_url):
    await page.set_viewport_size({"width": 320, "height": 720})
    await page.goto(base_url + "/ctx")
    await wait_for_alpine(page)

    rail = page.locator("#chirpui-context-rail")
    # Stacked but in-flow and reachable at the narrowest supported width.
    await expect(rail).to_be_visible()
    await expect(rail).to_contain_text("Context A")
    assert await _no_horizontal_overflow(page), "rail must not cause overflow at 320px"


async def test_rail_content_swaps_on_boosted_nav(page, base_url):
    await page.set_viewport_size({"width": 1280, "height": 800})
    await page.goto(base_url + "/ctx")
    await wait_for_alpine(page)

    rail = page.locator("#chirpui-context-rail")
    await expect(rail).to_contain_text("Context A")

    await page.locator('a[href="/ctx/b"]').click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/ctx/b")
    await expect(page.locator('[data-testid="main-content"]')).to_have_text("Context B")
    # The rail rode the navigation via its OOB fragment.
    await expect(rail).to_contain_text("Context B")
    await expect(rail).not_to_contain_text("Context A")


async def test_rail_clears_on_contextless_route(page, base_url):
    """Keystone: navigating to a route with no rail fragment empties the rail
    (shell_runtime_script clears it) rather than stranding the prior content."""
    await page.set_viewport_size({"width": 1280, "height": 800})
    await page.goto(base_url + "/ctx")
    await wait_for_alpine(page)

    rail = page.locator("#chirpui-context-rail")
    await expect(rail).to_contain_text("Context A")

    await page.locator('a[href="/ctx/none"]').click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/ctx/none")
    await expect(page.locator('[data-testid="main-content"]')).to_have_text("No context")
    await expect(rail.locator('[data-testid="rail-content"]')).to_have_count(0)
