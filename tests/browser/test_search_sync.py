"""Test live search request coordination inside boosted shells."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_live_search_keeps_latest_query(page, base_url):
    """A slower older query must not overwrite the latest live-search result."""
    await page.goto(base_url + "/search-sync")
    await wait_for_alpine(page)

    field = page.locator("input[name='q']")
    await field.type("a")
    await page.wait_for_timeout(30)
    await field.type("b")
    await wait_for_htmx(page, timeout=8000)

    assert await page.text_content("[data-testid='search-result']") == "Result for ab"
