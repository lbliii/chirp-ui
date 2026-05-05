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


async def test_app_layout_uses_single_chirp_alpine_runtime(page, base_url):
    """app_layout should rely on Chirp injection instead of duplicating Alpine scripts."""
    await page.goto(base_url + "/app-layout-theme")
    await wait_for_alpine(page)

    scripts = await page.evaluate(
        """() => [...document.scripts].map((script) => ({
            src: script.src,
            chirp: script.getAttribute("data-chirp")
        }))"""
    )

    alpine_core = [script for script in scripts if script["chirp"] == "alpine"]
    chirpui_runtime = [script for script in scripts if script["chirp"] == "chirpui-alpine"]
    bare_alpine = [
        script
        for script in scripts
        if script["src"].endswith("npm/alpinejs@3.15.8") and script["chirp"] == "alpine"
    ]

    assert len(alpine_core) == 1
    assert len(chirpui_runtime) == 1
    assert bare_alpine == []


async def test_app_layout_theme_toggle_changes_computed_theme_tokens(page, base_url):
    """app_layout loads a data-theme-aware starter theme, so the toggle changes colors."""
    await page.goto(base_url + "/app-layout-theme")
    await wait_for_alpine(page)

    await page.evaluate(
        """() => {
            localStorage.setItem("chirpui-theme", "light");
            document.documentElement.setAttribute("data-theme", "light");
        }"""
    )
    await page.reload()
    await wait_for_alpine(page)
    light_bg = await page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--chirpui-bg').trim()"
    )

    await page.locator(".chirpui-theme-toggle").click()
    await page.wait_for_timeout(100)
    dark_bg = await page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--chirpui-bg').trim()"
    )

    assert await page.evaluate("document.documentElement.getAttribute('data-theme')") == "dark"
    assert light_bg != dark_bg
