"""Browser proof for interactive ASCII controls."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_ascii_binary_controls_keep_native_keyboard_behavior(page, base_url):
    await page.goto(base_url + "/ascii-controls")

    checkbox = page.get_by_role("checkbox", name="Accept Terms")
    toggle = page.get_by_role("switch", name="Dark Mode")
    disabled_switch = page.get_by_role("switch", name="Disabled Switch")

    await expect(checkbox).not_to_be_checked()
    await checkbox.press("Space")
    await expect(checkbox).to_be_checked()

    await expect(toggle).not_to_be_checked()
    await toggle.press("Space")
    await expect(toggle).to_be_checked()

    await expect(disabled_switch).to_be_disabled()


async def test_ascii_radio_and_knob_groups_keep_native_selection(page, base_url):
    await page.goto(base_url + "/ascii-controls")

    high = page.get_by_role("radio", name="High").first
    await high.focus()
    await high.press("Space")
    await expect(high).to_be_checked()

    mode_high = page.get_by_role("radio", name="High").nth(1)
    await mode_high.focus()
    await mode_high.press("Space")
    await expect(mode_high).to_be_checked()


async def test_ascii_fader_keyboard_updates_native_range_value(page, base_url):
    await page.goto(base_url + "/ascii-controls")
    await wait_for_alpine(page)

    slider = page.get_by_role("slider", name="Volume")
    value = page.locator(".chirpui-ascii-fader__value")
    filled = page.locator(".chirpui-ascii-fader__segment--filled")

    await expect(slider).to_have_value("40")
    await expect(value).to_have_text("40")
    assert await filled.count() == 3

    await slider.press("End")
    await expect(slider).to_have_value("100")
    await expect(value).to_have_text("100")
    assert await filled.count() == 8

    await slider.press("Home")
    await expect(slider).to_have_value("0")
    await expect(value).to_have_text("0")
    assert await filled.count() == 0


async def test_ascii_tile_toggle_visual_state_follows_native_checked_state(page, base_url):
    await page.goto(base_url + "/ascii-controls")

    tile = page.get_by_role("checkbox", name="Power")
    face = page.locator(".chirpui-ascii-tile-btn", has=tile).locator(
        ".chirpui-ascii-tile-btn__face"
    )

    await expect(tile).to_be_checked()
    assert await face.evaluate("el => getComputedStyle(el).boxShadow") != "none"

    await tile.press("Space")
    await expect(tile).not_to_be_checked()
    assert await face.evaluate("el => getComputedStyle(el).boxShadow") == "none"


async def test_ascii_breaker_panel_groups_switches_and_status_follows_state(page, base_url):
    await page.goto(base_url + "/ascii-controls")

    panel = page.get_by_role("group", name="Services")
    await expect(panel).to_be_visible()

    worker = panel.get_by_role("switch", name="Worker")
    worker_breaker = panel.locator(".chirpui-ascii-breaker-panel__breaker").filter(
        has_text="Worker"
    )
    status = worker_breaker.locator(".chirpui-ascii-breaker-panel__status")

    await expect(worker).not_to_be_checked()
    assert await status.evaluate("el => getComputedStyle(el).opacity") == "0.45"

    await worker.press("Space")
    await expect(worker).to_be_checked()
    assert await status.evaluate("el => getComputedStyle(el).opacity") == "1"


async def test_ascii_reduced_motion_removes_indicator_animation(page, base_url):
    await page.emulate_media(reduced_motion="reduce")
    await page.goto(base_url + "/ascii-controls")

    animation = await page.locator(".motion-probe .chirpui-ascii-indicator__light").evaluate(
        "el => getComputedStyle(el).animationName"
    )
    assert animation == "none"
