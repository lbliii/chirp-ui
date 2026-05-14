"""Browser proof for a second application chrome consumer surface."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def open_admin_consumer(page, base_url: str, width: int = 1024, height: int = 768):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/consumer-admin")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_admin_consumer_renders_distinct_app_chrome_contract(page, base_url):
    await open_admin_consumer(page, base_url, width=390, height=844)

    await assert_no_document_horizontal_overflow(page, "consumer-admin")
    await expect(page.get_by_role("banner")).to_be_visible()
    await expect(page.get_by_role("link", name="Consumer Chrome")).to_be_visible()
    await expect(page.get_by_role("link", name="Admin console")).to_have_attribute(
        "aria-current", "page"
    )
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("Invite member")
    await expect(page.get_by_role("button", name="Search admin")).to_be_visible()
    await expect(page.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(
        page.get_by_role("navigation", name="Subsection navigation", exact=True)
    ).to_be_visible()
    await expect(page.get_by_role("toolbar", name="Admin console tools")).to_be_visible()
    await expect(page.get_by_test_id("consumer-admin-view-title")).to_have_text("Access controls")


async def test_admin_consumer_route_tabs_swap_page_root(page, base_url):
    await open_admin_consumer(page, base_url)

    await page.get_by_role("link", name="Jobs").click()
    await wait_for_htmx(page)
    await expect(page).to_have_url(base_url + "/consumer-admin/jobs")
    await expect(page.get_by_test_id("consumer-admin-view-title")).to_have_text("Background jobs")
    await expect(page.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(page.get_by_role("button", name="Search admin")).to_be_visible()
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)
    await expect(page.locator("#main")).to_have_count(1)
