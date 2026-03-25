"""Test boosted navigation: shell survives, content swaps, nav state syncs."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_initial_page_renders_shell(page, base_url):
    """Full page load renders the app shell with sidebar + main."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    assert await page.is_visible(".chirpui-app-shell__sidebar")
    assert await page.is_visible("#main")
    assert await page.text_content("[data-testid='page-heading']") == "Home"


async def test_boosted_nav_swaps_content_preserves_shell(page, base_url):
    """Clicking a sidebar link swaps #page-content but keeps sidebar intact."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    # Click boosted sidebar link to Page B
    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    # Content swapped
    assert await page.text_content("[data-testid='page-heading']") == "Page B"

    # Sidebar survived (still present in DOM — not wiped by swap)
    assert await page.is_visible(".chirpui-app-shell__sidebar")
    assert await page.is_visible(".chirpui-sidebar__link")


async def test_boosted_nav_updates_url(page, base_url):
    """Boosted navigation pushes the new URL into history."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    assert page.url.endswith("/page-b")


async def test_boosted_nav_updates_active_link(page, base_url):
    """After boosted nav, the active sidebar link updates via syncNav."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    # Page B link should have active class
    page_b_link = page.locator("a[href='/page-b'].chirpui-sidebar__link")
    await page_b_link.wait_for(state="visible")
    classes = await page_b_link.get_attribute("class")
    assert "chirpui-sidebar__link--active" in classes


async def test_back_button_restores_previous_page(page, base_url):
    """Browser back button restores the previous page content."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)
    assert await page.text_content("[data-testid='page-heading']") == "Page B"

    await page.go_back()
    await page.wait_for_selector("[data-testid='page-heading']")
    heading = await page.text_content("[data-testid='page-heading']")
    assert heading == "Home"


async def test_main_scrolls_to_top_after_swap(page, base_url):
    """After boosted nav, #main scrolls to top (htmx:afterSwap handler)."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    # Scroll main down
    await page.evaluate("document.getElementById('main').scrollTop = 100")

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    scroll_top = await page.evaluate("document.getElementById('main').scrollTop")
    assert scroll_top == 0


async def test_main_receives_focus_after_swap(page, base_url):
    """After boosted nav, #main receives focus for keyboard navigation."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    # Small delay for afterSettle
    await page.wait_for_timeout(100)

    focused_id = await page.evaluate("document.activeElement?.id")
    assert focused_id == "main"
