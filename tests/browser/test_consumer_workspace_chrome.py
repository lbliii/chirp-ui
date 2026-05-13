"""Browser proof for a workspace-style application chrome consumer."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def open_workspace_consumer(page, base_url: str, width: int = 1024, height: int = 768):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/consumer-workspace")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_workspace_consumer_renders_full_app_chrome_contract(page, base_url):
    await open_workspace_consumer(page, base_url)

    await assert_no_document_horizontal_overflow(page, "consumer-workspace")
    await expect(page.get_by_role("banner")).to_be_visible()
    await expect(page.get_by_role("link", name="Consumer Chrome")).to_be_visible()
    await expect(page.get_by_role("link", name="Workspace")).to_have_attribute(
        "aria-current", "page"
    )
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("New run")
    await expect(page.get_by_role("button", name="Search workspace")).to_be_visible()
    await expect(page.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(
        page.get_by_role("navigation", name="Subsection navigation", exact=True)
    ).to_be_visible()
    await expect(page.get_by_role("toolbar", name="Workspace page tools")).to_be_visible()
    await expect(page.get_by_test_id("consumer-view-title")).to_have_text("Workspace overview")


async def test_workspace_consumer_command_trigger_focuses_palette(page, base_url):
    await open_workspace_consumer(page, base_url, width=390, height=844)

    await page.get_by_role("button", name="Search workspace").click()
    palette = page.locator("#workspace-consumer-palette")
    await palette.wait_for(state="visible", timeout=2000)
    assert await palette.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.closest('#workspace-consumer-palette') !== null"
    )


async def test_workspace_consumer_route_tabs_swap_page_root(page, base_url):
    await open_workspace_consumer(page, base_url)

    await page.get_by_role("link", name="Runs").click()
    await wait_for_htmx(page)
    await expect(page).to_have_url(base_url + "/consumer-workspace/runs")
    await expect(page.get_by_test_id("consumer-view-title")).to_have_text("Workspace runs")
    await expect(page.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(page.get_by_role("button", name="Search workspace")).to_be_visible()
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)
    await expect(page.locator("#main")).to_have_count(1)


async def test_workspace_consumer_page_content_inner_swap(page, base_url):
    await open_workspace_consumer(page, base_url)

    await page.get_by_role("button", name="Filter").click()
    await wait_for_htmx(page)
    await expect(page.get_by_test_id("consumer-filter-result")).to_be_visible()
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)
