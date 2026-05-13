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


async def test_ascii_table_roles_and_hidden_borders(page, base_url):
    await page.goto(base_url + "/ascii-composites")

    table = page.get_by_role("table", name="ASCII table")
    await expect(table).to_be_visible()
    await expect(page.get_by_role("columnheader", name="Service")).to_be_visible()
    await expect(
        page.locator(".chirpui-ascii-table [role='cell']").filter(has_text="api")
    ).to_be_visible()

    hidden_borders = await page.locator(".chirpui-ascii-table__border[aria-hidden='true']").count()
    assert hidden_borders == 3


async def test_ascii_composite_data_states_render_consistently(page, base_url):
    await page.goto(base_url + "/ascii-composites")

    progress = page.get_by_role("progressbar", name="Deploy")
    await expect(progress).to_have_attribute("aria-valuenow", "100")
    await expect(progress.locator(".chirpui-ascii-progress__value")).to_have_text("100%")

    current_step = page.locator(".chirpui-ascii-stepper__step[aria-current='step']")
    await expect(current_step).to_have_count(1)
    await expect(current_step).to_contain_text("Deploy")

    await expect(page.locator(".chirpui-ascii-tab[aria-current='page']")).to_contain_text(
        "Overview"
    )
