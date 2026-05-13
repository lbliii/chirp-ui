"""Browser proof for ASCII display and motion components."""

import pytest
from playwright.async_api import expect

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_ascii_display_accessible_names(page, base_url):
    await page.goto(base_url + "/ascii-displays")

    await expect(page.get_by_role("img", name="ETA: 08:42")).to_be_visible()
    await expect(page.get_by_role("img", name="Sparkline: 1, 3, 2, 8, 5")).to_be_visible()
    await expect(page.get_by_role("status", name="Loading feed")).to_be_visible()
    await expect(page.get_by_role("marquee", name="System healthy")).to_be_visible()
    await expect(page.get_by_role("meter", name="MIX")).to_have_attribute("aria-valuenow", "100")


async def test_ascii_display_visible_state_is_bounded(page, base_url):
    await page.goto(base_url + "/ascii-displays")

    vu = page.locator(".chirpui-ascii-vu")
    await expect(vu.locator(".chirpui-ascii-vu__readout")).to_have_text("100%")
    await expect(vu.locator(".chirpui-ascii-vu__cell--filled")).to_have_count(10)
    await expect(vu.locator(".chirpui-ascii-vu__cell--peak")).to_have_count(1)

    split_flap = page.locator(".chirpui-split-flap").first
    await expect(split_flap.locator(".chirpui-visually-hidden")).to_have_text("BOARD 12")
    await expect(split_flap.locator(".chirpui-split-flap__char")).to_have_count(8)


async def test_ascii_display_reduced_motion_stops_display_animation(page, base_url):
    await page.emulate_media(reduced_motion="reduce")
    await page.goto(base_url + "/ascii-displays")

    spinner_animation = await page.locator(".chirpui-ascii-spinner__char").first.evaluate(
        "el => getComputedStyle(el).animationName"
    )
    split_flap_animation = await page.locator(".chirpui-split-flap__char").first.evaluate(
        "el => getComputedStyle(el).animationName"
    )
    ticker_animation = await page.locator(".chirpui-ascii-ticker__text").evaluate(
        "el => getComputedStyle(el).animationName"
    )
    vu_animation = await page.locator(".chirpui-ascii-vu__cell--filled").first.evaluate(
        "el => getComputedStyle(el).animationName"
    )

    assert spinner_animation == "none"
    assert split_flap_animation == "none"
    assert ticker_animation == "none"
    assert vu_animation == "none"
