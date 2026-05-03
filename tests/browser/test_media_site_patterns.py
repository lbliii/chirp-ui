"""Media/streaming pattern fixture from the media-site recipe plan."""

import pytest

from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.mark.parametrize(
    ("width", "height"),
    [
        pytest.param(375, 812, id="phone"),
        pytest.param(768, 1024, id="tablet"),
        pytest.param(1280, 800, id="desktop"),
    ],
)
async def test_media_site_patterns_have_no_horizontal_overflow(page, base_url, width, height):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/media-site-patterns")

    await assert_no_document_horizontal_overflow(page, f"media-site-patterns-{width}x{height}")


async def test_media_site_patterns_render_recipe_sections(page, base_url):
    await page.goto(base_url + "/media-site-patterns")

    assert await page.locator("h1").filter(has_text="Acme Stream").count() == 1
    assert await page.get_by_text("Hero shelf").count() == 1
    assert await page.get_by_text("Ranked catalog rail").count() == 1
    assert await page.get_by_text("Format tabs").count() == 1
    assert await page.get_by_text("Title detail page").count() == 1
    assert await page.get_by_text("Watch-side companion panel").count() == 1
    assert await page.get_by_text("Live event cards").count() == 1
    assert await page.get_by_text("Profile-safe catalog").count() == 1
    assert await page.get_by_text("Plan and add-on comparison").count() == 1


async def test_media_site_patterns_keep_watch_companion_responsive(page, base_url):
    await page.set_viewport_size({"width": 375, "height": 812})
    await page.goto(base_url + "/media-site-patterns")

    player = page.get_by_alt_text("Live relay player")
    companion = page.get_by_text("Live chat is app-owned")

    player_box = await player.bounding_box()
    companion_box = await companion.bounding_box()

    assert player_box is not None
    assert companion_box is not None
    assert player_box["width"] <= 375
    assert companion_box["y"] > player_box["y"]
    assert await page.get_by_role("tab", name="Transcript").count() == 1
