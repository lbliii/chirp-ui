"""Forum/community pattern fixture from the forum-site recipe plan."""

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
async def test_forum_site_patterns_have_no_horizontal_overflow(page, base_url, width, height):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/forum-site-patterns")

    await assert_no_document_horizontal_overflow(page, f"forum-site-patterns-{width}x{height}")


async def test_forum_site_patterns_render_dense_forum_sections(page, base_url):
    await page.goto(base_url + "/forum-site-patterns")

    assert await page.locator("h1").filter(has_text="Harborlight Writers").count() == 1
    assert await page.get_by_text("Community threads").count() == 1
    assert await page.get_by_text("Thread page").count() == 1
    assert await page.get_by_text("Q&A answer set").count() == 1
    assert await page.get_by_text("Moderation queue").count() == 1
    assert await page.get_by_text("Activity and inbox").count() == 1


async def test_forum_site_patterns_keep_actions_labeled_and_separated(page, base_url):
    await page.goto(base_url + "/forum-site-patterns")

    assert await page.get_by_role("link", name="Reply as Rogue").count() >= 1
    assert await page.get_by_role("link", name="Read latest").count() == 1
    assert await page.get_by_role("link", name="Next unread").count() == 1
    assert await page.get_by_role("button", name="Reply to Rogue").count() == 1
    assert await page.get_by_role("navigation", name="Subsection navigation").count() == 1
