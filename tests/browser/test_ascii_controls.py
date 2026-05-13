"""Browser proof for interactive ASCII controls."""

import pytest
from playwright.async_api import expect

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

    slider = page.get_by_role("slider", name="Volume")
    await expect(slider).to_have_value("40")

    await slider.press("End")
    await expect(slider).to_have_value("100")

    await slider.press("Home")
    await expect(slider).to_have_value("0")


async def test_ascii_reduced_motion_removes_indicator_animation(page, base_url):
    await page.emulate_media(reduced_motion="reduce")
    await page.goto(base_url + "/ascii-controls")

    animation = await page.locator(".motion-probe .chirpui-ascii-indicator__light").evaluate(
        "el => getComputedStyle(el).animationName"
    )
    assert animation == "none"
