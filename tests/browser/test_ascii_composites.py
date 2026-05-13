"""Browser proof for ASCII composite components."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_ascii_modal_trigger_opens_named_dialog(page, base_url):
    await page.goto(base_url + "/ascii-composites")
    await wait_for_alpine(page)

    await page.get_by_role("button", name="Open ASCII Settings").click()

    dialog = page.get_by_role("dialog", name="ASCII Settings")
    await expect(dialog).to_be_visible()
    assert await page.locator("#ascii-settings").evaluate("el => el.open")
    await expect(page.get_by_test_id("ascii-modal-body")).to_be_visible()


async def test_ascii_modal_close_button_uses_native_dialog_form(page, base_url):
    await page.goto(base_url + "/ascii-composites")
    await wait_for_alpine(page)

    await page.get_by_role("button", name="Open ASCII Settings").click()
    dialog = page.locator("#ascii-settings")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.locator("#ascii-settings form[method='dialog'] button").click()
    await page.wait_for_timeout(100)

    assert not await dialog.evaluate("el => el.open")


async def test_ascii_modal_escape_closes_native_dialog(page, base_url):
    await page.goto(base_url + "/ascii-composites")
    await wait_for_alpine(page)

    await page.get_by_role("button", name="Open ASCII Settings").click()
    dialog = page.locator("#ascii-settings")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(100)

    assert not await dialog.evaluate("el => el.open")
