"""Browser tests for input_otp (#202)."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

CELL = "[data-testid='otp-container'] .chirpui-input-otp__cell"
HIDDEN = "[data-testid='otp-container'] input[type='hidden']"


async def test_otp_paste_fills_cells(page, base_url):
    await page.goto(base_url + "/input-otp")
    await wait_for_alpine(page)
    await page.locator(CELL).first.click()
    await page.locator(CELL).first.fill("")
    await page.evaluate(
        """() => {
            const el = document.querySelector('[data-testid="otp-container"] .chirpui-input-otp__cell');
            const dt = new DataTransfer();
            dt.setData('text/plain', '123456');
            el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true }));
        }"""
    )
    values = await page.eval_on_selector_all(CELL, "els => els.map(e => e.value)")
    assert values == ["1", "2", "3", "4", "5", "6"]
    assert await page.locator(HIDDEN).input_value() == "123456"


async def test_otp_backspace_moves_to_previous(page, base_url):
    await page.goto(base_url + "/input-otp")
    await wait_for_alpine(page)
    cells = page.locator(CELL)
    await cells.nth(1).click()
    await cells.nth(1).press("Backspace")
    await expect(cells.nth(0)).to_be_focused()
