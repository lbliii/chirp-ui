"""Test tabs: server-driven htmx tabs and client-side Alpine tabs."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


# ── Server-driven htmx tabs ─────────────────────────────────────────


async def test_htmx_tab_loads_content(page, base_url):
    """Clicking an htmx tab loads content into the target.

    KNOWN ISSUE: tabs inside a boosted #main inherit hx-boost, which
    intercepts the click before the explicit hx-get fires. The boost
    navigation uses hx-select="#page-content" on the response, but
    the tab endpoint returns a fragment (no #page-content wrapper),
    so the swap empties the target.

    This test navigates directly to the full-page tab URL as a
    workaround, and documents the boost/hx-get interaction as a
    real integration bug to fix in the tab component.
    """
    await page.goto(base_url + "/tabs")
    await wait_for_alpine(page)

    # Initial content
    content = await page.text_content("[data-testid='tab-content']")
    assert "Overview content" in content

    # Navigate to details via full-page URL (not tab click, due to boost conflict)
    await page.goto(base_url + "/tabs/details")
    await page.wait_for_selector("[data-testid='tab-content']")

    content = await page.text_content("[data-testid='tab-content']")
    assert "Details content" in content


async def test_htmx_tab_click_inside_boosted_shell(page, base_url):
    """Tab click inside boosted #main works — hx-boost='false' prevents hijacking."""
    await page.goto(base_url + "/tabs")
    await wait_for_alpine(page)

    await page.click("#tab-details")
    await wait_for_htmx(page)

    content = await page.text_content("[data-testid='tab-content']")
    assert "Details content" in content


async def test_htmx_tab_does_not_push_url(page, base_url):
    """htmx tabs with hx-push-url=false don't change the URL."""
    await page.goto(base_url + "/tabs")
    await wait_for_alpine(page)

    original_url = page.url

    await page.click("#tab-details")
    await wait_for_htmx(page)

    assert page.url == original_url


async def test_htmx_tab_preserves_shell(page, base_url):
    """Tab content swap stays inside #tab-content, doesn't affect shell."""
    await page.goto(base_url + "/tabs")
    await wait_for_alpine(page)

    await page.click("#tab-details")
    await wait_for_htmx(page)

    # Shell still present
    assert await page.is_visible(".chirpui-app-shell__sidebar")
    # Page heading survived
    assert await page.text_content("[data-testid='page-heading']") == "Tabs Test"


# ── Client-side Alpine tabs ─────────────────────────────────────────


async def test_client_tabs_switch(page, base_url):
    """Alpine tabs_panels toggle visibility client-side."""
    await page.goto(base_url + "/tabs-panels")
    await wait_for_alpine(page)
    await page.wait_for_timeout(200)

    # First panel visible
    assert await page.locator("[data-testid='panel-first']").is_visible()

    # Click second tab
    await page.click("button:has-text('Second Tab')")
    await page.wait_for_timeout(200)

    # Second panel visible, first hidden
    assert await page.locator("[data-testid='panel-second']").is_visible()
    assert not await page.locator("[data-testid='panel-first']").is_visible()


async def test_client_tabs_dispatch_event(page, base_url):
    """Alpine tabs dispatch chirpui:tab-changed on switch."""
    await page.goto(base_url + "/tabs-panels")
    await wait_for_alpine(page)

    await page.evaluate("""
        window._tabEvents = [];
        document.addEventListener('chirpui:tab-changed', (e) => {
            window._tabEvents.push(e.detail);
        });
    """)

    await page.click("button:has-text('Second Tab')")
    await page.wait_for_timeout(200)

    events = await page.evaluate("window._tabEvents")
    assert len(events) >= 1
    assert events[0]["tab"] == "second"


async def test_client_tabs_aria_selected(page, base_url):
    """Active tab gets aria-selected=true, others false."""
    await page.goto(base_url + "/tabs-panels")
    await wait_for_alpine(page)
    await page.wait_for_timeout(200)

    first = page.locator("button:has-text('First Tab')")
    second = page.locator("button:has-text('Second Tab')")

    assert await first.get_attribute("aria-selected") == "true"
    assert await second.get_attribute("aria-selected") == "false"

    await second.click()
    await page.wait_for_timeout(200)

    assert await first.get_attribute("aria-selected") == "false"
    assert await second.get_attribute("aria-selected") == "true"
