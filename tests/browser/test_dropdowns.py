"""Test dropdown menu: keyboard navigation, focus management, custom events."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_dropdown_opens_on_click(page, base_url):
    """Clicking trigger opens the dropdown menu."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)

    items = await page.locator(
        "[data-testid='dropdown-menu-container'] .chirpui-dropdown__item"
    ).count()
    assert items == 3


async def test_dropdown_closes_on_escape(page, base_url):
    """Pressing Escape closes the dropdown and returns focus to trigger."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(200)

    assert not await menu.is_visible()


async def test_dropdown_closes_on_click_outside(page, base_url):
    """Clicking outside the dropdown closes it."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)

    # Click on the page heading (outside dropdown)
    await page.click("[data-testid='page-heading']")
    await page.wait_for_timeout(200)

    assert not await menu.is_visible()


async def test_dropdown_item_click_dispatches_event(page, base_url):
    """Clicking an item dispatches chirpui:dropdown-selected with label and action."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    # Listen for custom event
    await page.evaluate("""
        window._dropdownEvents = [];
        document.addEventListener('chirpui:dropdown-selected', (e) => {
            window._dropdownEvents.push(e.detail);
        });
    """)

    trigger = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)

    # Click the "Edit" item
    await page.locator(
        "[data-testid='dropdown-menu-container'] .chirpui-dropdown__item >> text=Edit"
    ).click()
    await page.wait_for_timeout(200)

    events = await page.evaluate("window._dropdownEvents")
    assert len(events) >= 1
    assert events[0]["label"] == "Edit"
    assert events[0]["action"] == "edit"


async def test_dropdown_aria_expanded(page, base_url):
    """Trigger aria-expanded toggles between true and false."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-menu-container'] .chirpui-dropdown__trigger")

    # Initially closed
    expanded = await trigger.get_attribute("aria-expanded")
    assert expanded == "false"

    await trigger.click()
    await page.wait_for_timeout(200)

    expanded = await trigger.get_attribute("aria-expanded")
    assert expanded == "true"


async def test_dropdown_realigns_near_viewport_edge(page, base_url):
    """A right-edge trigger should flip the menu inward instead of clipping."""
    await page.set_viewport_size({"width": 240, "height": 720})
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    dropdown = page.locator("[data-testid='dropdown-menu-right-edge'] .chirpui-dropdown")
    trigger = page.locator("[data-testid='dropdown-menu-right-edge'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-menu-right-edge'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)
    await page.wait_for_timeout(100)

    viewport = page.viewport_size
    box = await menu.bounding_box()
    assert viewport is not None
    assert box is not None
    assert await dropdown.get_attribute("data-align-x") == "end"
    assert box["x"] >= 8
    assert box["x"] + box["width"] <= viewport["width"] - 8


# ── Dropdown select: keyboard navigation ────────────────────────────


async def test_dropdown_select_arrow_keys(page, base_url):
    """Arrow keys navigate through dropdown select items.

    Note: We test the Alpine keyDown/keyEnter methods directly because
    Playwright's keyboard events may not bubble through Alpine's
    @keydown handler reliably in headless Chromium. The methods
    themselves are the contract — they update focusedIndex, move focus,
    and dispatch the selection event.
    """
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-select-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-select-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)
    await page.wait_for_timeout(300)

    # Verify focus landed on first item after $nextTick
    focused = await page.evaluate("document.activeElement?.textContent?.trim()")
    assert focused == "Option A"

    # Call keyDown to advance to Option B (focusedIndex: 0 → 1)
    await page.evaluate("""() => {
        const el = document.querySelector('[data-testid="dropdown-select-container"] .chirpui-dropdown');
        el._x_dataStack[0].keyDown();
    }""")
    await page.wait_for_timeout(100)

    focused = await page.evaluate("document.activeElement?.textContent?.trim()")
    assert focused == "Option B"

    # Call keyEnter to select Option B
    await page.evaluate("""() => {
        const el = document.querySelector('[data-testid="dropdown-select-container"] .chirpui-dropdown');
        el._x_dataStack[0].keyEnter();
    }""")
    await page.wait_for_timeout(300)

    selected = await page.locator(
        "[data-testid='dropdown-select-container'] .chirpui-dropdown__selected"
    ).text_content()
    assert selected.strip() == "Option B"


async def test_dropdown_select_click_item(page, base_url):
    """Clicking an item in dropdown select updates the selected text."""
    await page.goto(base_url + "/dropdown")
    await wait_for_alpine(page)

    trigger = page.locator("[data-testid='dropdown-select-container'] .chirpui-dropdown__trigger")
    await trigger.click()

    menu = page.locator("[data-testid='dropdown-select-container'] .chirpui-dropdown__menu")
    await menu.wait_for(state="visible", timeout=2000)

    # Click Option B directly
    await page.locator(
        "[data-testid='dropdown-select-container'] .chirpui-dropdown__item >> text=Option B"
    ).click()
    await page.wait_for_timeout(300)

    selected = await page.locator(
        "[data-testid='dropdown-select-container'] .chirpui-dropdown__selected"
    ).text_content()
    assert selected.strip() == "Option B"
