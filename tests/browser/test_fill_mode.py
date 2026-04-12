"""Test fill mode: sync on initial load and boosted navigation."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_fill_page_adds_fill_class(page, base_url):
    """Full-page load syncs fill mode when #page-content owns a fill root."""
    await page.goto(base_url + "/fill")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)

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
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("a[href='/fill']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(200)

    classes = await page.locator("#main").get_attribute("class") or ""
    assert "chirpui-app-shell__main--fill" in classes

    await page.click("a[href='/no-fill']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(200)

    classes = await page.locator("#main").get_attribute("class") or ""
    assert "chirpui-app-shell__main--fill" not in classes
