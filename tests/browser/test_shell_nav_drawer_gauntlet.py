"""Browser gauntlet for the mobile shell nav drawer (#196).

Proves the built-in app_shell affordance (nav_drawer=True): below the 48rem
breakpoint a topbar hamburger opens the sidebar as an accessible off-canvas
slide-over (focus trap, ESC, scrim, scroll lock, focus return, link/close
dismiss) and a Context trigger opens the rail; above the breakpoint the regions
are normal grid columns and the triggers are hidden. No framework dependency —
the controller is vanilla JS in shell_runtime_script(). No horizontal overflow
at any width.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

PHONE = {"width": 320, "height": 720}
DESKTOP = {"width": 1280, "height": 800}

VIEWPORTS = [
    pytest.param(320, 720, id="phone-narrow"),
    pytest.param(390, 844, id="phone"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(1280, 900, id="desktop"),
]


async def _open(page, base_url, size, path="/shell-drawer"):
    await page.set_viewport_size(size)
    await page.goto(base_url + path)
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_no_horizontal_overflow_across_viewports(page, base_url, width, height):
    await _open(page, base_url, {"width": width, "height": height})
    await assert_no_document_horizontal_overflow(page, f"shell-drawer-{width}x{height}")


async def test_triggers_hidden_and_regions_docked_at_desktop(page, base_url):
    await _open(page, base_url, DESKTOP)
    await expect(page.get_by_role("button", name="Open Navigation")).to_be_hidden()
    await expect(page.get_by_role("button", name="Open Context")).to_be_hidden()
    # Sidebar + rail are normal in-grid columns (visible, not off-canvas).
    await expect(page.locator("#chirpui-app-shell-sidebar")).to_be_visible()
    await expect(page.locator("#chirpui-context-rail")).to_be_visible()
    await expect(page.get_by_role("link", name="Audit log")).to_be_visible()


async def test_triggers_visible_and_regions_offcanvas_at_phone(page, base_url):
    await _open(page, base_url, PHONE)
    await expect(page.get_by_role("button", name="Open Navigation")).to_be_visible()
    await expect(page.get_by_role("button", name="Open Context")).to_be_visible()
    # Off-canvas (visibility:hidden) until opened.
    await expect(page.locator("#chirpui-app-shell-sidebar")).to_be_hidden()
    await expect(page.locator("#chirpui-context-rail")).to_be_hidden()


async def test_sidebar_drawer_opens_traps_focus_and_returns_on_escape(page, base_url):
    await _open(page, base_url, PHONE)
    toggle = page.get_by_role("button", name="Open Navigation")
    await toggle.click()

    sidebar = page.locator("#chirpui-app-shell-sidebar")
    await expect(sidebar).to_be_visible()
    await expect(sidebar).to_have_attribute("aria-modal", "true")
    # The modal dialog must expose an accessible name (aria-labelledby -> head title).
    await expect(page.get_by_role("dialog", name="Navigation")).to_be_visible()
    await expect(toggle).to_have_attribute("aria-expanded", "true")
    # Initial focus landed inside the drawer (the close button is first focusable).
    assert await page.evaluate(
        "() => document.activeElement?.closest('#chirpui-app-shell-sidebar') !== null"
    )
    # Body scroll is locked while open.
    assert await page.evaluate("() => document.documentElement.style.overflow === 'hidden'")

    await page.keyboard.press("Escape")
    await expect(sidebar).to_be_hidden()
    await expect(toggle).to_have_attribute("aria-expanded", "false")
    assert await page.evaluate(
        "() => document.activeElement?.getAttribute('aria-label') === 'Open Navigation'"
    )
    assert await page.evaluate("() => document.documentElement.style.overflow !== 'hidden'")


async def test_focus_trap_wraps_both_directions(page, base_url):
    await _open(page, base_url, PHONE)
    await page.get_by_role("button", name="Open Navigation").click()
    await page.wait_for_timeout(50)

    # Focus starts on the first focusable (close button). Shift+Tab wraps to last.
    assert await page.evaluate(
        "() => document.activeElement?.getAttribute('data-chirpui-shell-drawer-close') !== null"
    )
    await page.keyboard.press("Shift+Tab")
    assert await page.evaluate("() => document.activeElement?.textContent?.includes('Audit log')")
    # Tab from the last focusable wraps back to the first.
    await page.keyboard.press("Tab")
    assert await page.evaluate(
        "() => document.activeElement?.getAttribute('data-chirpui-shell-drawer-close') !== null"
    )


async def test_scrim_click_closes_drawer(page, base_url):
    await _open(page, base_url, PHONE)
    await page.get_by_role("button", name="Open Navigation").click()
    sidebar = page.locator("#chirpui-app-shell-sidebar")
    await expect(sidebar).to_be_visible()

    await page.locator("[data-chirpui-shell-scrim]").click()
    await expect(sidebar).to_be_hidden()


async def test_close_button_closes_drawer(page, base_url):
    await _open(page, base_url, PHONE)
    await page.get_by_role("button", name="Open Navigation").click()
    sidebar = page.locator("#chirpui-app-shell-sidebar")
    await expect(sidebar).to_be_visible()

    await page.get_by_role("button", name="Close Navigation").click()
    await expect(sidebar).to_be_hidden()


async def test_nav_link_dismisses_drawer_and_navigates(page, base_url):
    await _open(page, base_url, PHONE)
    await page.get_by_role("button", name="Open Navigation").click()
    sidebar = page.locator("#chirpui-app-shell-sidebar")
    await expect(sidebar).to_be_visible()

    await sidebar.get_by_role("link", name="Deployments").click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(base_url + "/shell-drawer/deploys")
    await expect(page.locator('[data-testid="main-content"]')).to_have_text("Deployments")
    await expect(sidebar).to_be_hidden()


async def test_rail_drawer_opens_from_context_trigger(page, base_url):
    await _open(page, base_url, PHONE)
    rail = page.locator("#chirpui-context-rail")
    await expect(rail).to_be_hidden()

    await page.get_by_role("button", name="Open Context").click()
    await expect(rail).to_be_visible()
    await expect(rail).to_have_attribute("aria-modal", "true")
    await expect(rail.get_by_test_id("rail-content")).to_contain_text("Inspector")
    # The headless rail gets a runtime-injected floating close (kept out of the
    # OOB-swapped content), and focus lands inside the trapped panel on open.
    await page.wait_for_timeout(50)
    close = rail.locator("[data-chirpui-shell-drawer-close]")
    await expect(close).to_be_visible()
    assert await page.evaluate(
        "() => document.activeElement?.closest('#chirpui-context-rail') !== null"
    )
    await close.click()
    await expect(rail).to_be_hidden()


async def test_drawer_auto_closes_when_viewport_grows_past_breakpoint(page, base_url):
    await _open(page, base_url, PHONE)
    await page.get_by_role("button", name="Open Navigation").click()
    sidebar = page.locator("#chirpui-app-shell-sidebar")
    await expect(sidebar).to_be_visible()

    # Growing past 48rem must release the trap (otherwise focus strands on desktop).
    await page.set_viewport_size(DESKTOP)
    await expect(page.get_by_role("button", name="Open Navigation")).to_be_hidden()
    # The body-scroll-lock release runs from the matchMedia change handler, which
    # fires asynchronously after the viewport resize — poll rather than read
    # synchronously to avoid racing the handler.
    await page.wait_for_function("() => document.documentElement.style.overflow !== 'hidden'")
    await expect(page.locator("[data-chirpui-shell-scrim]")).to_be_hidden()


async def test_layout_exposes_region_announcer_wrappers(page, base_url):
    """#197 region-contract parity on the LAYOUT path (where it is renderable):
    the layout now exposes #chirpui-sidebar-nav (aria-live) wrapping the sidebar
    content, with .chirpui-app-shell__drawer-head as a SIBLING OUTSIDE it (same
    ordering as the macro). Also #chirpui-topbar-breadcrumbs on topbar-center."""
    await _open(page, base_url, DESKTOP)
    nav = page.locator("#chirpui-sidebar-nav")
    await expect(nav).to_have_count(1)
    assert await nav.get_attribute("aria-live") == "polite"
    assert await nav.get_attribute("aria-atomic") == "true"
    # The sidebar nav content lives inside the wrapper.
    await expect(nav.get_by_role("link", name="Audit log")).to_be_visible()
    # drawer-head is a sibling OUTSIDE #chirpui-sidebar-nav (not nested).
    assert await page.evaluate(
        "() => { var h = document.querySelector('.chirpui-app-shell__drawer-head');"
        " var n = document.getElementById('chirpui-sidebar-nav');"
        " return !!h && !!n && !n.contains(h); }"
    )
    bc = page.locator("#chirpui-topbar-breadcrumbs")
    await expect(bc).to_have_count(1)
    assert await bc.get_attribute("aria-live") == "polite"


async def test_prefix_match_activates_on_nested_route(page, base_url):
    """#197 server+JS parity: the prefix-match 'Deployments' link
    (/shell-drawer/deploys) activates on its own nested route via the canonical
    syncNav on the layout path, mirroring the server-computed _active."""
    await _open(page, base_url, DESKTOP, path="/shell-drawer/deploys")
    deploys = page.locator("a[href='/shell-drawer/deploys'].chirpui-sidebar__link")
    await deploys.wait_for(state="visible")
    assert "chirpui-sidebar__link--active" in (await deploys.get_attribute("class"))
    assert await deploys.get_attribute("aria-current") == "page"
    # The exact-match Overview link is NOT active on the nested route.
    overview = page.locator("a[href='/shell-drawer'].chirpui-sidebar__link")
    assert "chirpui-sidebar__link--active" not in (await overview.get_attribute("class"))


async def test_hamburger_is_separate_target_from_brand_anchor(page, base_url):
    """#220 anchor escape: the hamburger toggle is a separate focus/click target
    from the brand link, and clicking it opens the drawer rather than navigating
    to the brand href (proves the leading affordance escaped the anchor)."""
    await _open(page, base_url, PHONE)
    toggle = page.get_by_role("button", name="Open Navigation")
    # The hamburger is NOT nested inside the brand anchor.
    assert await page.evaluate(
        "() => { var t = document.querySelector('.chirpui-app-shell__nav-toggle');"
        " return !!t && t.closest('a.chirpui-app-shell__brand') === null; }"
    )
    start_url = page.url
    await toggle.click()
    await expect(page.locator("#chirpui-app-shell-sidebar")).to_be_visible()
    # Clicking the hamburger opened the drawer and did NOT navigate.
    assert page.url == start_url
