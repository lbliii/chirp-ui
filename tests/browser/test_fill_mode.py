"""Test fill mode: auto-toggle of --fill class on htmx:afterSettle."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_fill_page_adds_fill_class(page, base_url):
    """Page with .chirpui-page-fill gets --fill class on #main.

    Note: The --fill class is toggled by the htmx:afterSettle handler in
    app_shell_layout.html. On initial page load (non-htmx), the handler
    only fires if htmx processes the page. For a full-page GET, the class
    may not be set until the first htmx swap. Navigate away and back to
    trigger it via htmx.
    """
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    # Navigate to fill page via boosted nav (triggers afterSettle)
    await page.click("a[href='/fill']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(300)

    classes = await page.locator("#main").get_attribute("class")
    assert "chirpui-app-shell__main--fill" in classes


async def test_no_fill_page_removes_fill_class(page, base_url):
    """Page without .chirpui-page-fill does not get --fill class on #main."""
    await page.goto(base_url + "/no-fill")
    await wait_for_alpine(page)
    await page.wait_for_timeout(200)

    classes = await page.locator("#main").get_attribute("class")
    assert "chirpui-app-shell__main--fill" not in classes


async def test_fill_toggles_on_navigation(page, base_url):
    """Navigating between fill and no-fill pages toggles the class."""
    # Start on home page (no fill)
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    # Navigate to fill page via boost
    await page.click("a[href='/fill']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(500)

    classes = await page.locator("#main").get_attribute("class") or ""
    assert "chirpui-app-shell__main--fill" in classes

    # The sidebar on /fill has a /no-fill link. But after boosted nav,
    # only #page-content swaps — sidebar stays from original page.
    # Navigate to no-fill via direct goto (sidebar link may not exist).
    await page.goto(base_url + "/fill")
    await wait_for_alpine(page)

    # Now navigate to no-fill (sidebar has the link on this page)
    await page.click("a[href='/no-fill']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(500)

    classes = await page.locator("#main").get_attribute("class") or ""
    assert "chirpui-app-shell__main--fill" not in classes
