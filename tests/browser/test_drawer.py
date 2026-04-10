"""Test drawer: open/close, native dialog, content visible."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_drawer_opens_on_trigger(page, base_url):
    """Clicking drawer trigger opens the dialog."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)

    body = await page.text_content("[data-testid='drawer-body']")
    assert "Drawer content here" in body


async def test_drawer_closes_on_close_button(page, base_url):
    """Close button closes the drawer dialog."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.click(".chirpui-drawer__close")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")


async def test_drawer_closes_on_escape(page, base_url):
    """Pressing Escape closes the drawer."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")
