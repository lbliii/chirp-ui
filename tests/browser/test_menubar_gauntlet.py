"""Browser gauntlet for the menubar (#335).

Proves top-level roving focus, submenu open/close, selection events, and axe
coverage against a real use_chirp_ui app.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"

ROOT = "[data-testid='menubar-container'] .chirpui-menubar"
TRIGGER = "[data-testid='menubar-container'] .chirpui-menubar__trigger"
PANEL = "[data-testid='menubar-container'] .chirpui-menubar__menu"
ITEM = "[data-testid='menubar-container'] .chirpui-menubar__item"


async def _open_page(page, base_url):
    await page.goto(base_url + "/menubar")
    await wait_for_alpine(page)


async def _wait_submenu_settled(page):
    await page.wait_for_function(
        """() => {
            const panels = document.querySelectorAll(
                "[data-testid='menubar-container'] .chirpui-menubar__menu");
            const open = Array.from(panels).find(
                (p) => parseFloat(getComputedStyle(p).opacity) >= 0.99
                    && getComputedStyle(p).display !== "none");
            if (!open) return false;
            const a = document.activeElement;
            return !!(a && a.classList && a.classList.contains("chirpui-menubar__item"));
        }""",
        timeout=5000,
    )


async def _add_event_listener(page):
    await page.evaluate(
        "() => { window._menubarEvents = [];"
        " document.addEventListener('chirpui:menubar-selected',"
        " (e) => window._menubarEvents.push(e.detail)); }"
    )


async def test_arrow_right_moves_between_top_level_triggers(page, base_url):
    await _open_page(page, base_url)
    triggers = page.locator(TRIGGER)
    await triggers.first.focus()
    await page.keyboard.press("ArrowRight")
    await expect(triggers.nth(1)).to_be_focused()


async def test_arrow_down_opens_submenu_and_focuses_first_item(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.focus()
    await page.keyboard.press("ArrowDown")
    await expect(page.locator(PANEL).first).to_be_visible()
    await _wait_submenu_settled(page)
    await page.wait_for_function(
        "() => (document.activeElement && document.activeElement.textContent || '').includes('New')",
        timeout=5000,
    )


async def test_escape_closes_submenu_and_returns_focus_to_trigger(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.focus()
    await page.keyboard.press("ArrowDown")
    await _wait_submenu_settled(page)
    await page.keyboard.press("Escape")
    await page.wait_for_function(
        "() => document.activeElement === document.querySelector("
        "\"[data-testid='menubar-container'] .chirpui-menubar__trigger\")",
        timeout=5000,
    )
    await expect(page.locator(PANEL).first).to_be_hidden()


async def test_click_outside_closes_open_submenu(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.click()
    await _wait_submenu_settled(page)
    await page.click("[data-testid='main-content']")
    await expect(page.locator(PANEL).first).to_be_hidden()


async def test_item_select_dispatches_event(page, base_url):
    await _open_page(page, base_url)
    await _add_event_listener(page)
    await page.locator(TRIGGER).first.click()
    await _wait_submenu_settled(page)
    await page.locator(ITEM, has_text="New").click()
    events = await page.evaluate("() => window._menubarEvents")
    assert events[-1]["label"] == "New"
    assert events[-1]["action"] == "new"


async def test_axe_no_serious_or_critical_violations(page, base_url):
    await _open_page(page, base_url)
    await page.locator(TRIGGER).first.click()
    await _wait_submenu_settled(page)
    try:
        await page.add_script_tag(url=AXE_CDN)
    except Exception:
        pytest.skip("axe-core CDN unreachable in this harness")
    await page.wait_for_function("() => window.axe", timeout=5000)
    results = await page.evaluate(
        "async () => await window.axe.run("
        "\"[data-testid='menubar-container']\", "
        "{ runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] })"
    )
    serious = [v for v in results["violations"] if v["impact"] in ("serious", "critical")]
    detail = "; ".join(
        v["id"] + " -> " + ", ".join(n.get("target", [""])[0] for n in v.get("nodes", []))
        for v in serious
    )
    assert not serious, "axe serious/critical violations: " + detail
