"""Browser gauntlet for hover_card (#338).

Proves delayed hover/focus open, blur/Escape close, reduced-motion instant open,
and viewport containment against a real use_chirp_ui app.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

ROOT = "[data-testid='hover-card-container'] .chirpui-hover-card"
PANEL = "[data-testid='hover-card-container'] .chirpui-hover-card__content"
TRIGGER = "[data-testid='hover-card-trigger']"
EDGE_ROOT = "[data-testid='hover-card-edge-container'] .chirpui-hover-card"
EDGE_PANEL = "[data-testid='hover-card-edge-container'] .chirpui-hover-card__content"
EDGE_TRIGGER = "[data-testid='hover-card-edge-trigger']"


async def _open_page(page, base_url, *, width: int = 1280, height: int = 800):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/hover-card")
    await wait_for_alpine(page)


async def _wait_open(page, selector: str = PANEL):
    await page.wait_for_function(
        f"""() => {{
            const panel = document.querySelector({selector!r});
            if (!panel) return false;
            return parseFloat(getComputedStyle(panel).opacity) >= 0.99
                && getComputedStyle(panel).display !== "none";
        }}""",
        timeout=5000,
    )


async def _panel_in_viewport(page, selector: str = PANEL) -> bool:
    return await page.evaluate(
        f"""() => {{
            const panel = document.querySelector({selector!r});
            if (!panel) return false;
            const rect = panel.getBoundingClientRect();
            const vw = document.documentElement.clientWidth;
            const vh = document.documentElement.clientHeight;
            return rect.left >= -1 && rect.right <= vw + 1
                && rect.top >= -1 && rect.bottom <= vh + 1;
        }}"""
    )


async def test_hover_opens_after_delay(page, base_url):
    await _open_page(page, base_url)
    await expect(page.locator(PANEL)).to_be_hidden()
    await page.locator(TRIGGER).hover()
    await _wait_open(page)
    await expect(page.locator(PANEL)).to_be_visible()
    await expect(page.locator("[data-testid='hover-card-preview']")).to_be_visible()


async def test_focus_opens_after_delay(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).focus()
    await _wait_open(page)
    await expect(page.locator(PANEL)).to_be_visible()


async def test_blur_closes_open_card(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).focus()
    await _wait_open(page)
    await page.locator("[data-testid='main-content']").focus()
    await expect(page.locator(PANEL)).to_be_hidden()


async def test_escape_closes_open_card(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).focus()
    await _wait_open(page)
    await page.keyboard.press("Escape")
    await expect(page.locator(PANEL)).to_be_hidden()


async def test_open_panel_stays_within_viewport(page, base_url):
    await _open_page(page, base_url, width=360, height=720)
    await page.locator(EDGE_TRIGGER).focus()
    await _wait_open(page, EDGE_PANEL)
    assert await _panel_in_viewport(page, EDGE_PANEL)
    align_x = await page.locator(EDGE_ROOT).get_attribute("data-align-x")
    assert align_x in {"start", "end"}


async def test_reduced_motion_opens_immediately_on_focus(page, base_url):
    await _open_page(page, base_url)
    await page.emulate_media(reduced_motion="reduce")
    await page.reload()
    await wait_for_alpine(page)
    await page.locator(TRIGGER).focus()
    await page.wait_for_function(
        f"""() => {{
            const panel = document.querySelector({PANEL!r});
            return !!panel && getComputedStyle(panel).display !== "none";
        }}""",
        timeout=1000,
    )
