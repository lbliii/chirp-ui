"""Product page pattern fixture from the LangChain design review plan."""

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
async def test_product_page_patterns_have_no_horizontal_overflow(
    page, base_url, width, height
):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/product-page-patterns")

    await assert_no_document_horizontal_overflow(
        page, f"product-page-patterns-{width}x{height}"
    )


async def test_product_page_patterns_render_recipe_sections(page, base_url):
    await page.goto(base_url + "/product-page-patterns")

    assert await page.locator("h1").filter(has_text="Acme Agents").count() == 1
    assert await page.get_by_text("Trusted by teams shipping production agents").count() == 1
    assert await page.get_by_text("Choose the right framework").count() == 1
    assert await page.get_by_text("Learn from teams running agents in production").count() == 1
