"""Test command palette: keyboard open, search, close."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_command_palette_opens_on_trigger_click(page, base_url):
    """Clicking the trigger button opens the command palette dialog."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.click(".chirpui-command-palette-trigger")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)

    input_el = page.locator(".chirpui-command-palette__input")
    assert await input_el.is_visible()


async def test_command_palette_opens_on_keyboard_shortcut(page, base_url):
    """Pressing Cmd+K or Ctrl+K opens the command palette."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.keyboard.press("Control+k")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)


async def test_command_palette_closes_on_escape(page, base_url):
    """Pressing Escape closes the command palette."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.click(".chirpui-command-palette-trigger")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")
