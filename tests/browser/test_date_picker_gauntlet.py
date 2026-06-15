"""Browser gauntlet for the date / range picker (#201).

Proves the picker against a real use_chirp_ui app:
- the readonly input opens a role=dialog popover with a role=grid of gridcells
- clicking a day fills the hidden ISO value and closes (single)
- Arrow keys rove the grid (roving tabindex); Enter picks the focused day
- prev/next month navigation updates the month label
- min/max disable out-of-range days
- range mode: two clicks set ordered start/end hidden inputs and highlight the span
- Escape closes and returns focus to the input
- axe scan of the open popover: no serious/critical violations

Deterministic: the single picker is preselected to 2025-06-15 and the range
picker is bounded to June 2025, so assertions never depend on the real "today".
Hidden ISO values (locale-independent) are the primary assertions.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"

S = "[data-testid='date-picker-single']"
R = "[data-testid='date-picker-range']"
S_INPUT = S + " .chirpui-date-picker__input"
S_POP = S + " .chirpui-date-picker__popover"
R_INPUT = R + " .chirpui-date-picker__input"
R_POP = R + " .chirpui-date-picker__popover"


async def _wait_opaque(page, pop_sel):
    await page.wait_for_function(
        "(s) => { const p = document.querySelector(s);"
        " return !!p && parseFloat(getComputedStyle(p).opacity) >= 0.99; }",
        arg=pop_sel,
        timeout=5000,
    )


async def _open(page, base_url, input_sel, pop_sel):
    await page.goto(base_url + "/date-picker")
    await wait_for_alpine(page)
    await page.locator(input_sel).click()
    await expect(page.locator(pop_sel)).to_be_visible()
    await _wait_opaque(page, pop_sel)


async def _hidden(page, name):
    return await page.eval_on_selector(f"input[type=hidden][name='{name}']", "el => el.value")


async def test_opens_with_dialog_and_grid(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    pop = page.locator(S_POP)
    assert await pop.get_attribute("role") == "dialog"
    grid = page.locator(S + " .chirpui-date-picker__grid")
    assert await grid.get_attribute("role") == "grid"
    assert await page.locator(S + " [role=gridcell]").count() == 42
    assert await page.locator(S + " [role=columnheader]").count() == 7
    month = await page.locator(S + " .chirpui-date-picker__month").inner_text()
    assert month == "June 2025"
    # The preselected day is the roving-focus target.
    assert (
        await page.evaluate("() => document.activeElement && document.activeElement.dataset.iso")
        == "2025-06-15"
    )


async def test_single_click_day_fills_value_and_closes(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    await page.locator(S + ' [data-iso="2025-06-20"]').click()
    await expect(page.locator(S_POP)).to_be_hidden()
    assert await _hidden(page, "due") == "2025-06-20"
    assert await page.locator(S_INPUT).input_value() != ""


async def test_arrow_keys_move_grid_focus(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    await page.keyboard.press("ArrowRight")  # 15 -> 16
    await page.wait_for_function(
        "() => document.activeElement && document.activeElement.dataset.iso === '2025-06-16'",
        timeout=5000,
    )
    await page.keyboard.press("ArrowDown")  # 16 -> 23
    await page.wait_for_function(
        "() => document.activeElement && document.activeElement.dataset.iso === '2025-06-23'",
        timeout=5000,
    )


async def test_enter_picks_focused_day(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    await page.keyboard.press("ArrowDown")  # 15 -> 22
    await page.wait_for_function(
        "() => document.activeElement && document.activeElement.dataset.iso === '2025-06-22'",
        timeout=5000,
    )
    await page.keyboard.press("Enter")
    await expect(page.locator(S_POP)).to_be_hidden()
    assert await _hidden(page, "due") == "2025-06-22"


async def test_month_navigation_updates_label(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    await page.locator(S + " .chirpui-date-picker__nav[aria-label='Next month']").click()
    await expect(page.locator(S + " .chirpui-date-picker__month")).to_have_text("July 2025")
    await page.locator(S + " .chirpui-date-picker__nav[aria-label='Previous month']").click()
    await page.locator(S + " .chirpui-date-picker__nav[aria-label='Previous month']").click()
    await expect(page.locator(S + " .chirpui-date-picker__month")).to_have_text("May 2025")


async def test_escape_closes_and_returns_focus(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    await page.keyboard.press("Escape")
    await expect(page.locator(S_POP)).to_be_hidden()
    focused = await page.evaluate(
        "() => document.activeElement === document.querySelector("
        "\"[data-testid='date-picker-single'] .chirpui-date-picker__input\")"
    )
    assert focused


async def test_range_min_max_disables_out_of_bounds_days(page, base_url):
    await _open(page, base_url, R_INPUT, R_POP)
    # min 2025-06-05, max 2025-06-25.
    assert await page.locator(R + ' [data-iso="2025-06-04"]').is_disabled()
    assert await page.locator(R + ' [data-iso="2025-06-26"]').is_disabled()
    assert not await page.locator(R + ' [data-iso="2025-06-10"]').is_disabled()


async def test_range_select_sets_ordered_endpoints(page, base_url):
    await _open(page, base_url, R_INPUT, R_POP)
    await page.locator(R + ' [data-iso="2025-06-10"]').click()
    await page.locator(R + ' [data-iso="2025-06-20"]').click()
    await expect(page.locator(R_POP)).to_be_hidden()
    assert await _hidden(page, "span") == "2025-06-10"
    assert await _hidden(page, "span_end") == "2025-06-20"
    # Reopen and confirm a mid day is marked in-range.
    await page.locator(R_INPUT).click()
    await _wait_opaque(page, R_POP)
    cls = await page.locator(R + ' [data-iso="2025-06-15"]').get_attribute("class")
    assert "chirpui-date-picker__day--in-range" in cls


async def test_range_select_orders_reversed_clicks(page, base_url):
    await _open(page, base_url, R_INPUT, R_POP)
    await page.locator(R + ' [data-iso="2025-06-20"]').click()  # later first
    await page.locator(R + ' [data-iso="2025-06-10"]').click()  # earlier second
    await expect(page.locator(R_POP)).to_be_hidden()
    assert await _hidden(page, "span") == "2025-06-10"
    assert await _hidden(page, "span_end") == "2025-06-20"


async def test_axe_no_serious_or_critical_violations(page, base_url):
    await _open(page, base_url, S_INPUT, S_POP)
    try:
        await page.add_script_tag(url=AXE_CDN)
    except Exception:
        pytest.skip("axe-core CDN unreachable in this harness")
    await page.wait_for_function("() => window.axe", timeout=5000)
    results = await page.evaluate(
        "async () => await window.axe.run("
        "\"[data-testid='date-picker-single']\", "
        "{ runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] })"
    )
    serious = [v for v in results["violations"] if v["impact"] in ("serious", "critical")]
    detail = "; ".join(
        v["id"] + " -> " + ", ".join(n.get("target", [""])[0] for n in v.get("nodes", []))
        for v in serious
    )
    assert not serious, "axe serious/critical violations: " + detail


async def test_keyboard_does_not_strand_focus_at_bound(page, base_url):
    # The range picker (today is outside [2025-06-05, 2025-06-25]) opens focused
    # on the clamped boundary (max = 2025-06-25). Arrowing past the bound must keep
    # focus on an enabled in-bounds day — never a disabled one, which would strand
    # focus on <body> and kill the grid's keydown handler.
    await _open(page, base_url, R_INPUT, R_POP)
    await page.wait_for_function(
        "() => document.activeElement && document.activeElement.dataset.iso === '2025-06-25'",
        timeout=5000,
    )
    await page.keyboard.press("ArrowRight")  # → 06-26 (out of bounds) clamps to 06-25
    await page.keyboard.press("ArrowDown")  # → 07-02 (out of bounds) clamps to 06-25
    info = await page.evaluate(
        "() => { const a = document.activeElement;"
        " return { iso: a && a.dataset.iso, disabled: !!(a && a.disabled) }; }"
    )
    assert info["iso"] == "2025-06-25"
    assert info["disabled"] is False
    # Grid still responds — it was not stranded.
    await page.keyboard.press("ArrowLeft")
    await page.wait_for_function(
        "() => document.activeElement && document.activeElement.dataset.iso === '2025-06-24'",
        timeout=5000,
    )
