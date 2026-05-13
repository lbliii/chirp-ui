"""Browser proof for rail-to-drawer application chrome."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


VIEWPORTS = [
    pytest.param(320, 640, id="phone-narrow"),
    pytest.param(390, 844, id="phone"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(1024, 768, id="tablet-wide"),
    pytest.param(1280, 900, id="desktop"),
]


async def open_rail_to_tray(page, base_url: str, width: int = 1024, height: int = 768):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/rail-to-tray")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_rail_to_tray_recipe_keeps_core_chrome_reachable(
    page, base_url, width, height
):
    await open_rail_to_tray(page, base_url, width=width, height=height)

    await assert_no_document_horizontal_overflow(page, f"rail-to-tray-{width}x{height}")
    await expect(page.get_by_role("button", name="Search workspace")).to_be_visible()
    await expect(page.get_by_role("button", name="Deploy")).to_be_visible()
    await expect(page.get_by_role("navigation", name="Subsection navigation")).to_be_visible()

    active_visible_links = await page.locator(
        "a[aria-current='page']:visible"
    ).evaluate_all("(links) => links.map((link) => link.textContent.trim())")
    assert active_visible_links.count("Overview8") <= 1

    if width <= 640:
        await expect(page.get_by_test_id("desktop-product-rail")).to_be_hidden()
        await expect(page.get_by_role("button", name="Open product navigation")).to_be_visible()
    else:
        await expect(page.get_by_test_id("desktop-product-rail")).to_be_visible()
        await expect(page.get_by_role("button", name="Open product navigation")).to_be_hidden()


async def test_rail_to_tray_phone_drawer_opens_closes_and_returns_focus(page, base_url):
    await open_rail_to_tray(page, base_url, width=320, height=640)

    trigger = page.get_by_role("button", name="Open product navigation")
    await trigger.click()
    drawer = page.locator("#product-nav-drawer")
    await expect(drawer).to_be_visible()
    assert await drawer.evaluate("el => el.open")
    await expect(drawer.get_by_role("link", name="Runtime settings")).to_be_visible()

    await page.keyboard.press("Escape")
    await expect(drawer).not_to_be_visible()
    assert not await drawer.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.textContent?.includes('Open product navigation')"
    )


async def test_rail_to_tray_command_trigger_opens_palette(page, base_url):
    await open_rail_to_tray(page, base_url, width=390, height=844)

    await page.get_by_role("button", name="Search workspace").click()
    palette = page.locator("#rail-to-tray-palette")
    await palette.wait_for(state="visible", timeout=2000)
    assert await palette.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.closest('#rail-to-tray-palette') !== null"
    )
