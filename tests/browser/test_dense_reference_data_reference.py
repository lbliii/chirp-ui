from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine


async def _assert_no_document_horizontal_overflow(page) -> None:
    metrics = await page.evaluate(
        """() => ({
            clientWidth: document.documentElement.clientWidth,
            scrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
        })"""
    )
    assert metrics["scrollWidth"] <= metrics["clientWidth"] + 1, metrics
    assert metrics["bodyScrollWidth"] <= metrics["clientWidth"] + 1, metrics


async def test_dense_reference_data_reference_uses_existing_primitives_only(page, base_url):
    await page.goto(base_url + "/dense-reference-data-reference")
    await wait_for_alpine(page)

    fixture = page.get_by_test_id("dense-reference-data-reference")
    await expect(fixture).to_be_visible()
    assert await fixture.get_attribute("data-reference-implementation") == "dense-reference-data"
    assert await fixture.get_attribute("data-scenario-complete") == "true"
    assert await fixture.get_attribute("data-public-api") == "false"
    assert await fixture.get_attribute("data-existing-primitives") == (
        "resource_index resource_card filter_rail filter_bar search_header table "
        "params_table card badge callout"
    )
    assert await fixture.get_attribute("data-promotion-boundary") == (
        "no data_grid virtual_table reference_page_macro filter_count_api css manifest runtime"
    )

    for selector in [
        ".chirpui-resource-index",
        ".chirpui-resource-card",
        ".chirpui-filter-rail",
        ".chirpui-action-strip",
        ".chirpui-search-header",
        ".chirpui-table",
        ".chirpui-params-table",
        ".chirpui-card",
        ".chirpui-badge",
        ".chirpui-callout",
    ]:
        await expect(page.locator(selector).first).to_be_visible()

    await expect(page.locator(".chirpui-data-grid")).to_have_count(0)
    await expect(page.locator("[data-chirpui-component='data-grid']")).to_have_count(0)
    await expect(page.locator("[data-chirpui-component='reference-page']")).to_have_count(0)


async def test_dense_reference_data_reference_covers_state_pressure(page, base_url):
    await page.goto(base_url + "/dense-reference-data-reference")
    await wait_for_alpine(page)

    await expect(page.get_by_test_id("dense-reference-empty-state")).to_contain_text(
        "No members match this filter."
    )
    await expect(page.get_by_test_id("dense-reference-loading-state")).to_have_attribute(
        "aria-busy", "true"
    )
    await expect(page.get_by_test_id("dense-reference-error-state")).to_contain_text(
        "failed to load"
    )
    await expect(page.locator(".chirpui-selection-bar")).to_be_visible()


async def test_dense_reference_data_reference_long_names_stay_inside_document(page, base_url):
    for width, height in [(320, 760), (768, 900), (1280, 900)]:
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(base_url + "/dense-reference-data-reference")
        await wait_for_alpine(page)

        await expect(
            page.get_by_text("params_table_with_extremely_long_generated_member_name")
        ).to_be_visible()
        await expect(
            page.get_by_text("module_reference_identifier_with_deliberately_long_unbroken_name")
        ).to_be_visible()
        await _assert_no_document_horizontal_overflow(page)
