"""Test boosted navigation: shell survives, content swaps, nav state syncs."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def _scroll_document(page, top: int) -> None:
    await page.evaluate("value => window.scrollTo({ top: value, left: 0 })", top)
    await page.wait_for_timeout(100)


async def _document_scroll_y(page) -> float:
    return await page.evaluate("window.scrollY")


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
    await _scroll_document(page, 900)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)
    assert await page.text_content("[data-testid='page-heading']") == "Page B"
    assert await _document_scroll_y(page) < 5

    await page.go_back()
    await page.wait_for_selector("[data-testid='page-heading']")
    await page.wait_for_timeout(150)
    heading = await page.text_content("[data-testid='page-heading']")
    assert heading == "Home"
    assert await _document_scroll_y(page) > 400


async def test_topbar_stays_sticky_during_document_scroll(page, base_url):
    """The topbar remains pinned to the viewport during document scroll."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)
    await _scroll_document(page, 900)

    box = await page.locator(".chirpui-app-shell__topbar").bounding_box()
    assert box is not None
    assert abs(box["y"]) < 1


async def test_new_route_boosted_nav_scrolls_document_to_top(page, base_url):
    """New-route boosted nav resets document scroll, not an inner shell scrollport."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)
    await _scroll_document(page, 900)

    await page.click("a[href='/page-b']")
    await wait_for_htmx(page)

    assert await _document_scroll_y(page) < 5


async def test_same_route_boosted_refresh_preserves_document_scroll(page, base_url):
    """Same-route boosted swaps preserve the current document scroll position."""
    await page.goto(base_url + "/page-b")
    await wait_for_alpine(page)
    await _scroll_document(page, 800)

    await page.click("[data-testid='refresh-page-b']")
    await wait_for_htmx(page)

    assert await page.text_content("[data-testid='page-heading']") == "Page B"
    assert await _document_scroll_y(page) > 600


async def test_hash_navigation_lands_below_sticky_topbar(page, base_url):
    """Hash-based boosted nav scrolls the anchor below the sticky shell offset."""
    await page.goto(base_url + "/")
    await wait_for_alpine(page)

    await page.click("[data-testid='page-b-anchor-link']")
    await wait_for_htmx(page)
    await page.wait_for_timeout(150)

    assert page.url.endswith("/page-b#page-b-anchor")
    metrics = await page.evaluate(
        """() => {
            const topbar = document.querySelector(".chirpui-app-shell__topbar");
            const anchor = document.getElementById("page-b-anchor");
            return {
                topbarBottom: topbar ? topbar.getBoundingClientRect().bottom : null,
                anchorTop: anchor ? anchor.getBoundingClientRect().top : null,
            };
        }"""
    )
    assert metrics["topbarBottom"] is not None
    assert metrics["anchorTop"] is not None
    assert metrics["anchorTop"] >= metrics["topbarBottom"] - 1
    assert metrics["anchorTop"] < metrics["topbarBottom"] + 64


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
