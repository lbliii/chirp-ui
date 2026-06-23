"""Browser tests for input_otp (#202, #339)."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

CELL = "[data-testid='otp-container'] .chirpui-input-otp__cell"
HIDDEN = "[data-testid='otp-container'] input[type='hidden']"
ROOT = "[data-testid='otp-container'] .chirpui-input-otp"


async def _open_page(page, base_url):
    await page.goto(base_url + "/input-otp")
    await wait_for_alpine(page)


async def _add_change_listener(page):
    await page.evaluate(
        "() => { window._otpEvents = [];"
        " document.addEventListener('chirpui:otp-change',"
        " (e) => window._otpEvents.push(e.detail)); }"
    )


async def test_otp_paste_fills_cells(page, base_url):
    await _open_page(page, base_url)
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
    await _open_page(page, base_url)
    cells = page.locator(CELL)
    await cells.nth(1).click()
    await cells.nth(1).press("Backspace")
    await expect(cells.nth(0)).to_be_focused()


async def test_otp_typing_advances_and_syncs_hidden_value(page, base_url):
    await _open_page(page, base_url)
    await _add_change_listener(page)
    cells = page.locator(CELL)
    await cells.first.click()
    await cells.first.type("1")
    await expect(cells.nth(1)).to_be_focused()
    await cells.nth(1).type("2")
    assert await page.locator(HIDDEN).input_value() == "12"
    events = await page.evaluate("() => window._otpEvents")
    assert events[-1]["value"] == "12"


async def test_otp_arrow_keys_move_focus(page, base_url):
    await _open_page(page, base_url)
    cells = page.locator(CELL)
    await cells.nth(2).click()
    await cells.nth(2).press("ArrowLeft")
    await expect(cells.nth(1)).to_be_focused()
    await cells.nth(1).press("ArrowRight")
    await expect(cells.nth(2)).to_be_focused()


async def test_otp_cells_have_distinct_accessible_names(page, base_url):
    await _open_page(page, base_url)
    labels = await page.eval_on_selector_all(
        CELL, "els => els.map(e => e.getAttribute('aria-label'))"
    )
    assert labels == [
        "Digit 1 of 6",
        "Digit 2 of 6",
        "Digit 3 of 6",
        "Digit 4 of 6",
        "Digit 5 of 6",
        "Digit 6 of 6",
    ]


async def test_otp_group_exposes_group_semantics(page, base_url):
    await _open_page(page, base_url)
    assert await page.locator(f"{ROOT} .chirpui-input-otp__group").get_attribute("role") == "group"
