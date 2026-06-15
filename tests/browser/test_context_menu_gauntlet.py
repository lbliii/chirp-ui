"""Browser gauntlet for the context menu (#202).

Proves the a11y acceptance criteria against a real use_chirp_ui app:
- right-click opens a role="menu" panel anchored at the pointer
- the menu opens from the focused region via the keyboard open contract
- roving tabindex: items are role="menuitem" tabindex="-1"; ArrowDown/Up/Home/End
  move focus (first item focused on open)
- Escape closes the menu and returns focus to the trigger region
- click-outside closes the menu
- selecting an item dispatches chirpui:context-menu-selected {label, action} and closes
- disabled items are aria-disabled and inert (no selection event)
- axe scan of the open menu: no serious/critical violations

Following the dropdown gauntlet precedent, roving-nav is exercised by calling the
Alpine factory methods directly (Playwright keydown does not reliably bubble
through Alpine's @keydown in headless Chromium); open/select/escape/click-outside
use real pointer/keyboard events.

The open is asynchronous: Alpine focuses the first item in a $nextTick and the
panel fades in via x-transition. Every assertion that depends on focus or on the
panel being opaque (axe contrast) waits for the menu to fully *settle* first —
otherwise CI races the transition (mid-fade opacity makes even dark-on-white text
fail contrast, and a too-early keystroke is overwritten by the pending open-focus).
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"

REGION = "[data-testid='context-menu-container'] .chirpui-context-menu"
TRIGGER = "[data-testid='context-menu-container'] .chirpui-context-menu__target"
PANEL = "[data-testid='context-menu-container'] .chirpui-context-menu__panel"
ITEM = "[data-testid='context-menu-container'] .chirpui-context-menu__item"


async def _open_page(page, base_url):
    await page.goto(base_url + "/context-menu")
    await wait_for_alpine(page)


async def _wait_settled(page):
    """Wait until the menu is fully open: panel opaque (transition done) and a
    role=menuitem focused (the $nextTick open-focus has landed)."""
    await page.wait_for_function(
        """() => {
            const p = document.querySelector(
                "[data-testid='context-menu-container'] .chirpui-context-menu__panel");
            if (!p || parseFloat(getComputedStyle(p).opacity) < 0.99) return false;
            const a = document.activeElement;
            return !!(a && a.classList && a.classList.contains('chirpui-context-menu__item'));
        }""",
        timeout=5000,
    )


async def _open_via_right_click(page):
    await page.locator(TRIGGER).click(button="right")
    await expect(page.locator(PANEL)).to_be_visible()
    await _wait_settled(page)


async def _call(page, method):
    """Invoke a chirpuiContextMenu factory method on the region directly."""
    await page.evaluate(
        "(m) => { const el = document.querySelector("
        "\"[data-testid='context-menu-container'] .chirpui-context-menu\");"
        " el._x_dataStack[0][m](); }",
        method,
    )


async def _wait_focused_contains(page, text):
    """Wait until the focused element's text contains *text* (roving focus)."""
    await page.wait_for_function(
        "(t) => (document.activeElement && document.activeElement.textContent || '').includes(t)",
        arg=text,
        timeout=5000,
    )


async def _add_event_listener(page):
    await page.evaluate(
        "() => { window._ctxEvents = [];"
        " document.addEventListener('chirpui:context-menu-selected',"
        " (e) => window._ctxEvents.push(e.detail)); }"
    )


async def test_right_click_opens_menu_at_pointer(page, base_url):
    await _open_page(page, base_url)
    panel = page.locator(PANEL)
    await expect(panel).to_be_hidden()
    await _open_via_right_click(page)
    assert await panel.get_attribute("role") == "menu"
    # Positioned (fixed) — has a concrete top/left, inside the viewport.
    box = await panel.bounding_box()
    viewport = page.viewport_size
    assert box is not None
    assert viewport is not None
    assert box["x"] >= 0
    assert box["x"] + box["width"] <= viewport["width"] + 1


async def test_menu_items_are_menuitems_with_roving_tabindex(page, base_url):
    await _open_page(page, base_url)
    await _open_via_right_click(page)
    assert await page.locator(ITEM).count() == 4
    roles = await page.eval_on_selector_all(ITEM, "els => els.map(e => e.getAttribute('role'))")
    assert all(r == "menuitem" for r in roles)
    tabindexes = await page.eval_on_selector_all(
        ITEM, "els => els.map(e => e.getAttribute('tabindex'))"
    )
    assert all(t == "-1" for t in tabindexes)
    # First item receives focus on open (settled above).
    await _wait_focused_contains(page, "Open")


async def test_arrow_home_end_move_focus(page, base_url):
    await _open_page(page, base_url)
    await _open_via_right_click(page)
    await _call(page, "keyDown")  # 0 -> 1 (Rename)
    await _wait_focused_contains(page, "Rename")
    await _call(page, "keyEnd")  # -> last (Delete)
    await _wait_focused_contains(page, "Delete")
    await _call(page, "keyHome")  # -> first (Open)
    await _wait_focused_contains(page, "Open")


async def test_disabled_item_stays_focusable_but_inert(page, base_url):
    await _open_page(page, base_url)
    await _add_event_listener(page)
    await _open_via_right_click(page)
    disabled = page.locator(ITEM, has_text="Duplicate")
    assert await disabled.get_attribute("aria-disabled") == "true"
    # Roving focus still reaches it (WAI-ARIA: disabled items are focusable).
    await _call(page, "keyDown")  # 0 -> 1
    await _wait_focused_contains(page, "Rename")
    await _call(page, "keyDown")  # 1 -> 2 (Duplicate)
    await _wait_focused_contains(page, "Duplicate")
    # Activating it (the factory's select path) dispatches nothing and keeps the
    # menu open — the aria-disabled guard short-circuits selectItem.
    await page.evaluate(
        "() => { const root = document.querySelector("
        "\"[data-testid='context-menu-container'] .chirpui-context-menu\");"
        " const dup = root.querySelector('[data-action=\"duplicate\"]');"
        " root._x_dataStack[0].selectItem(dup); }"
    )
    await page.wait_for_timeout(80)
    events = await page.evaluate("() => window._ctxEvents")
    assert not any(e.get("action") == "duplicate" for e in events)
    await expect(page.locator(PANEL)).to_be_visible()


async def test_escape_closes_and_returns_focus_to_region(page, base_url):
    await _open_page(page, base_url)
    await _open_via_right_click(page)
    panel = page.locator(PANEL)
    await page.keyboard.press("Escape")
    # Focus returns to the trigger.
    await page.wait_for_function(
        "() => document.activeElement === document.querySelector("
        "\"[data-testid='context-menu-container'] .chirpui-context-menu__target\")",
        timeout=5000,
    )
    await expect(panel).to_be_hidden()


async def test_click_outside_closes(page, base_url):
    await _open_page(page, base_url)
    await _open_via_right_click(page)
    panel = page.locator(PANEL)
    await page.click("[data-testid='main-content']")
    await expect(panel).to_be_hidden()


async def test_keyboard_opens_from_focused_region(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).focus()
    await _call(page, "openAtElement")
    await expect(page.locator(PANEL)).to_be_visible()
    await _wait_settled(page)
    await _wait_focused_contains(page, "Open")


async def test_item_select_dispatches_event_and_closes(page, base_url):
    await _open_page(page, base_url)
    await _add_event_listener(page)
    await _open_via_right_click(page)
    panel = page.locator(PANEL)
    await page.locator(ITEM, has_text="Rename").click()
    await expect(panel).to_be_hidden()
    events = await page.evaluate("() => window._ctxEvents")
    assert events[-1]["label"] == "Rename"
    assert events[-1]["action"] == "rename"


async def test_axe_no_serious_or_critical_violations(page, base_url):
    await _open_page(page, base_url)
    # Settle first: a mid-transition (semi-transparent) panel makes axe report
    # false color-contrast failures even for dark-on-white text.
    await _open_via_right_click(page)
    try:
        await page.add_script_tag(url=AXE_CDN)
    except Exception:
        pytest.skip("axe-core CDN unreachable in this harness")
    await page.wait_for_function("() => window.axe", timeout=5000)
    results = await page.evaluate(
        "async () => await window.axe.run("
        "\"[data-testid='context-menu-container']\", "
        "{ runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] })"
    )
    serious = [v for v in results["violations"] if v["impact"] in ("serious", "critical")]
    detail = "; ".join(
        v["id"] + " -> " + ", ".join(n.get("target", [""])[0] for n in v.get("nodes", []))
        for v in serious
    )
    assert not serious, "axe serious/critical violations: " + detail
