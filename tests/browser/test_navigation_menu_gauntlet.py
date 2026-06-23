"""Browser gauntlet for the navigation menu (#336).

Proves flyout submenu open/close, keyboard trigger behavior, outside dismiss,
viewport containment, and narrow-width overflow against a real use_chirp_ui app.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

ROOT = "[data-testid='navigation-menu-container'] .chirpui-navigation-menu"
TRIGGER = "[data-testid='navigation-menu-container'] .chirpui-navigation-menu__trigger"
PANEL = "[data-testid='navigation-menu-container'] .chirpui-navigation-menu__panel"
LINK = "[data-testid='navigation-menu-container'] .chirpui-navigation-menu__panel .chirpui-navigation-menu__link"


async def _open_page(page, base_url, *, width: int = 1280, height: int = 800):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/navigation-menu")
    await wait_for_alpine(page)


async def _no_horizontal_overflow(page) -> bool:
    return await page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")


async def _wait_panel_settled(page):
    await page.wait_for_function(
        """() => {
            const panels = document.querySelectorAll(
                "[data-testid='navigation-menu-container'] .chirpui-navigation-menu__panel");
            const open = Array.from(panels).find(
                (p) => parseFloat(getComputedStyle(p).opacity) >= 0.99
                    && getComputedStyle(p).display !== "none");
            if (!open) return false;
            const a = document.activeElement;
            return !!(a && a.classList && a.classList.contains("chirpui-navigation-menu__link"));
        }""",
        timeout=5000,
    )


async def _panel_in_viewport(page) -> bool:
    return await page.evaluate(
        """() => {
            const panel = Array.from(document.querySelectorAll(
                "[data-testid='navigation-menu-container'] .chirpui-navigation-menu__panel"))
                .find((p) => parseFloat(getComputedStyle(p).opacity) >= 0.99
                    && getComputedStyle(p).display !== "none");
            if (!panel) return false;
            const rect = panel.getBoundingClientRect();
            const vw = document.documentElement.clientWidth;
            return rect.left >= -1 && rect.right <= vw + 1;
        }"""
    )


async def test_arrow_down_opens_submenu_and_focuses_first_link(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.focus()
    await page.keyboard.press("ArrowDown")
    await expect(page.locator(PANEL).first).to_be_visible()
    await _wait_panel_settled(page)
    await page.wait_for_function(
        "() => (document.activeElement && document.activeElement.textContent || '').includes('Analytics')",
        timeout=5000,
    )


async def test_escape_closes_submenu_and_returns_focus_to_trigger(page, base_url):
    await _open_page(page, base_url)
    trigger = page.locator(TRIGGER).first
    await trigger.focus()
    await page.keyboard.press("ArrowDown")
    await _wait_panel_settled(page)
    await page.keyboard.press("Escape")
    await page.wait_for_function(
        "() => document.activeElement === document.querySelector("
        "\"[data-testid='navigation-menu-container'] .chirpui-navigation-menu__trigger\")",
        timeout=5000,
    )
    await expect(page.locator(PANEL).first).to_be_hidden()


async def test_click_outside_closes_open_submenu(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.click()
    await _wait_panel_settled(page)
    await page.click("[data-testid='main-content']")
    await expect(page.locator(PANEL).first).to_be_hidden()


async def test_open_panel_stays_within_viewport(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.click()
    await _wait_panel_settled(page)
    assert await _panel_in_viewport(page), "flyout panel must stay within the viewport"


@pytest.mark.parametrize(("width", "height"), [(320, 720), (768, 1024)])
async def test_no_horizontal_overflow_at_responsive_widths(page, base_url, width, height):
    await _open_page(page, base_url, width=width, height=height)
    assert await _no_horizontal_overflow(page), f"navigation menu must not overflow at {width}px"
    await page.locator(TRIGGER).first.click()
    await _wait_panel_settled(page)
    assert await _no_horizontal_overflow(page), f"open flyout must not overflow at {width}px"
    assert await _panel_in_viewport(page), f"flyout panel must stay in viewport at {width}px"
