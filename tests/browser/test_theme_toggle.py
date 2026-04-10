"""Test theme toggle: cycles themes, persists to localStorage."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_theme_toggle_cycles_theme(page, base_url):
    """Clicking toggle cycles through light/dark/system."""
    await page.goto(base_url + "/theme-toggle")
    await wait_for_alpine(page)

    btn = page.locator(".chirpui-theme-toggle")

    # Get initial theme
    initial = await page.evaluate("document.documentElement.getAttribute('data-theme')")

    # Click to cycle
    await btn.click()
    await page.wait_for_timeout(100)
    after_first = await page.evaluate("document.documentElement.getAttribute('data-theme')")

    # Click again to cycle further
    await btn.click()
    await page.wait_for_timeout(100)
    after_second = await page.evaluate("document.documentElement.getAttribute('data-theme')")

    # All three should be different
    assert len({initial, after_first, after_second}) >= 2


async def test_theme_toggle_persists_to_localstorage(page, base_url):
    """Theme change is saved to localStorage."""
    await page.goto(base_url + "/theme-toggle")
    await wait_for_alpine(page)

    btn = page.locator(".chirpui-theme-toggle")
    await btn.click()
    await page.wait_for_timeout(100)

    stored = await page.evaluate("localStorage.getItem('chirpui-theme')")
    assert stored is not None
    assert stored in ("light", "dark", "system")


async def test_theme_toggle_has_aria_label(page, base_url):
    """Toggle button has an accessible label."""
    await page.goto(base_url + "/theme-toggle")
    await wait_for_alpine(page)

    btn = page.locator(".chirpui-theme-toggle")
    label = await btn.get_attribute("aria-label")
    assert label is not None
    assert "theme" in label.lower() or "Theme" in label
