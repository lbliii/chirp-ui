"""HTMX target-boundary proof for app chrome consumers."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def open_workspace_consumer(page, base_url: str):
    await page.set_viewport_size({"width": 1024, "height": 768})
    await page.goto(base_url + "/consumer-workspace")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_shell_navigation_updates_shell_content_without_duplicate_roots(page, base_url):
    await open_workspace_consumer(page, base_url)

    await page.locator('a[href="/consumer-admin"]').click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/consumer-admin")
    await expect(page.get_by_test_id("consumer-admin-view-title")).to_have_text("Access controls")
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("Invite member")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)


async def test_route_tab_swap_updates_page_root_without_replacing_shell(page, base_url):
    await open_workspace_consumer(page, base_url)

    await page.get_by_role("link", name="Runs").click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/consumer-workspace/runs")
    await expect(page.get_by_test_id("consumer-view-title")).to_have_text("Workspace runs")
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("New run")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)


async def test_inner_content_swap_updates_fragment_without_replacing_page_root(page, base_url):
    await open_workspace_consumer(page, base_url)

    await page.get_by_role("button", name="Filter").click()
    await wait_for_htmx(page)

    await expect(page.get_by_test_id("consumer-filter-result")).to_be_visible()
    await expect(page.get_by_test_id("consumer-heading")).to_have_text("Workspace consumer")
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("New run")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)
