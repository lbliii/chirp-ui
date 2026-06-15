"""Browser gauntlet for the combobox / autocomplete (#201).

Proves the WAI-ARIA combobox acceptance criteria against a real use_chirp_ui app:
- typing filters the role=option list (client-side substring match)
- ArrowDown/ArrowUp rove the visible options via aria-activedescendant; the
  active option carries aria-selected="true"
- Enter selects the active option (fills the input label, writes the hidden
  value, dispatches chirpui:combobox-selected) and closes the list
- clicking an option selects it
- Escape closes the list and keeps focus on the input; click-outside closes
- a no-matches query shows the empty state and no visible options
- axe scan of the open list: no serious/critical violations

Roving/select are exercised via the Alpine factory methods (Playwright keydown is
unreliable through Alpine in headless Chromium); filter/click/escape/click-outside
use real events. Every assertion that depends on the list being painted waits for
the x-transition to finish (opacity ~1) — otherwise CI races the fade.
"""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"

ROOT = "[data-testid='combobox-container'] .chirpui-combobox"
INPUT = "[data-testid='combobox-container'] .chirpui-combobox__input"
LIST = "[data-testid='combobox-container'] .chirpui-combobox__list"
OPTION = "[data-testid='combobox-container'] .chirpui-combobox__option"
EMPTY = "[data-testid='combobox-container'] .chirpui-combobox__empty"


async def _open_page(page, base_url):
    await page.goto(base_url + "/combobox")
    await wait_for_alpine(page)


async def _wait_list_opaque(page):
    await page.wait_for_function(
        """() => {
            const l = document.querySelector(
                "[data-testid='combobox-container'] .chirpui-combobox__list");
            return !!l && parseFloat(getComputedStyle(l).opacity) >= 0.99;
        }""",
        timeout=5000,
    )


async def _open(page):
    await page.locator(INPUT).click()
    await expect(page.locator(LIST)).to_be_visible()
    await _wait_list_opaque(page)


async def _factory_move(page, delta):
    await page.evaluate(
        "(d) => { document.querySelector("
        "\"[data-testid='combobox-container'] .chirpui-combobox\")"
        "._x_dataStack[0].move(d); }",
        delta,
    )


async def _factory_select_active(page):
    await page.evaluate(
        "() => { document.querySelector("
        "\"[data-testid='combobox-container'] .chirpui-combobox\")"
        "._x_dataStack[0].selectActive(); }"
    )


async def _visible_labels(page):
    return await page.eval_on_selector_all(
        OPTION,
        "els => els.filter(e => e.offsetParent !== null).map(e => e.dataset.label)",
    )


async def _add_event_listener(page):
    await page.evaluate(
        "() => { window._cbxEvents = [];"
        " document.addEventListener('chirpui:combobox-selected',"
        " (e) => window._cbxEvents.push(e.detail)); }"
    )


async def test_typing_filters_options(page, base_url):
    await _open_page(page, base_url)
    inp = page.locator(INPUT)
    await inp.click()
    await inp.fill("ap")
    await expect(page.locator(LIST)).to_be_visible()
    # Only the two "Ap…" options remain visible.
    await page.wait_for_function(
        """() => {
            const opts = [...document.querySelectorAll(
                "[data-testid='combobox-container'] .chirpui-combobox__option")];
            const vis = opts.filter(o => o.offsetParent !== null).map(o => o.dataset.label);
            return vis.length === 2 && vis.includes('Apple') && vis.includes('Apricot');
        }""",
        timeout=5000,
    )


async def test_no_matches_shows_empty_state(page, base_url):
    await _open_page(page, base_url)
    inp = page.locator(INPUT)
    await inp.click()
    await inp.fill("zzz")
    await expect(page.locator(EMPTY)).to_be_visible()
    assert await _visible_labels(page) == []


async def test_arrow_sets_aria_activedescendant_and_selected(page, base_url):
    await _open_page(page, base_url)
    await _open(page)
    await _factory_move(page, 1)
    # The input's aria-activedescendant points at an option that is aria-selected.
    await page.wait_for_function(
        """() => {
            const i = document.querySelector(
                "[data-testid='combobox-container'] .chirpui-combobox__input");
            const ad = i.getAttribute('aria-activedescendant');
            if (!ad) return false;
            const opt = document.getElementById(ad);
            return !!opt && opt.getAttribute('aria-selected') === 'true'
                && opt.classList.contains('chirpui-combobox__option--active');
        }""",
        timeout=5000,
    )
    assert await page.locator(INPUT).get_attribute("aria-expanded") == "true"


async def test_enter_selects_active_option(page, base_url):
    await _open_page(page, base_url)
    await _add_event_listener(page)
    await _open(page)
    await _factory_move(page, 1)  # active = first option (Apple)
    await _factory_select_active(page)
    inp = page.locator(INPUT)
    await expect(page.locator(LIST)).to_be_hidden()
    assert await inp.input_value() == "Apple"
    hidden_value = await page.eval_on_selector(
        "[data-testid='combobox-container'] input[type=hidden]", "el => el.value"
    )
    assert hidden_value == "apple"
    events = await page.evaluate("() => window._cbxEvents")
    assert events[-1] == {"value": "apple", "label": "Apple"}


async def test_click_option_selects(page, base_url):
    await _open_page(page, base_url)
    await _open(page)
    await page.locator(OPTION, has_text="Banana").click()
    await expect(page.locator(LIST)).to_be_hidden()
    assert await page.locator(INPUT).input_value() == "Banana"
    hidden_value = await page.eval_on_selector(
        "[data-testid='combobox-container'] input[type=hidden]", "el => el.value"
    )
    assert hidden_value == "banana"


async def test_escape_closes_and_keeps_input_focus(page, base_url):
    await _open_page(page, base_url)
    await _open(page)
    await page.keyboard.press("Escape")
    await expect(page.locator(LIST)).to_be_hidden()
    focused_is_input = await page.evaluate(
        "() => document.activeElement === document.querySelector("
        "\"[data-testid='combobox-container'] .chirpui-combobox__input\")"
    )
    assert focused_is_input


async def test_click_outside_closes(page, base_url):
    await _open_page(page, base_url)
    await _open(page)
    await page.click("[data-testid='main-content']")
    await expect(page.locator(LIST)).to_be_hidden()


async def test_axe_no_serious_or_critical_violations(page, base_url):
    await _open_page(page, base_url)
    await _open(page)
    try:
        await page.add_script_tag(url=AXE_CDN)
    except Exception:
        pytest.skip("axe-core CDN unreachable in this harness")
    await page.wait_for_function("() => window.axe", timeout=5000)
    results = await page.evaluate(
        "async () => await window.axe.run("
        "\"[data-testid='combobox-container']\", "
        "{ runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] })"
    )
    serious = [v for v in results["violations"] if v["impact"] in ("serious", "critical")]
    detail = "; ".join(
        v["id"] + " -> " + ", ".join(n.get("target", [""])[0] for n in v.get("nodes", []))
        for v in serious
    )
    assert not serious, "axe serious/critical violations: " + detail


# ── Multi-select (token-pill) mode (#201) ───────────────────────────

M_CT = "[data-testid='combobox-multi-container']"
M_INPUT = M_CT + " .chirpui-combobox__input"
M_LIST = M_CT + " .chirpui-combobox__list"
M_OPTION = M_CT + " .chirpui-combobox__option"
M_TOKEN = M_CT + " .chirpui-combobox__token"
M_HIDDEN = M_CT + " input[type=hidden][name=tags]"


async def _open_multi(page):
    await page.locator(M_INPUT).click()
    await expect(page.locator(M_LIST)).to_be_visible()
    await page.wait_for_function(
        '() => { const l = document.querySelector("' + M_LIST + '");'
        " return !!l && parseFloat(getComputedStyle(l).opacity) >= 0.99; }",
        timeout=5000,
    )


async def _multi_visible_values(page):
    return await page.eval_on_selector_all(
        M_OPTION,
        "els => els.filter(e => e.offsetParent !== null).map(e => e.dataset.value)",
    )


async def test_multi_select_adds_pills_and_hidden_inputs(page, base_url):
    await _open_page(page, base_url)
    await _open_multi(page)
    await page.locator(M_OPTION, has_text="Design").click()
    await page.locator(M_OPTION, has_text="Docs").click()
    await expect(page.locator(M_TOKEN)).to_have_count(2)
    # Each selected value submits as a repeated hidden `tags` input.
    vals = await page.eval_on_selector_all(M_HIDDEN, "els => els.map(e => e.value)")
    assert sorted(vals) == ["design", "docs"]
    # Selected options drop out of the list.
    visible = await _multi_visible_values(page)
    assert "design" not in visible
    assert "docs" not in visible


async def test_multi_remove_pill_restores_option(page, base_url):
    await _open_page(page, base_url)
    await _open_multi(page)
    await page.locator(M_OPTION, has_text="Design").click()
    await page.locator(M_OPTION, has_text="Docs").click()
    await expect(page.locator(M_TOKEN)).to_have_count(2)
    # Remove the Design pill via its remove button.
    await (
        page.locator(M_TOKEN, has_text="Design").locator(".chirpui-combobox__token-remove").click()
    )
    await expect(page.locator(M_TOKEN)).to_have_count(1)
    vals = await page.eval_on_selector_all(M_HIDDEN, "els => els.map(e => e.value)")
    assert vals == ["docs"]
    # Design returns to the list.
    await page.locator(M_INPUT).click()
    assert "design" in await _multi_visible_values(page)


async def test_multi_backspace_removes_last_pill(page, base_url):
    await _open_page(page, base_url)
    await _open_multi(page)
    await page.locator(M_OPTION, has_text="Design").click()
    await expect(page.locator(M_TOKEN)).to_have_count(1)
    inp = page.locator(M_INPUT)
    await inp.click()  # focus the (empty) input
    await inp.press("Backspace")
    await expect(page.locator(M_TOKEN)).to_have_count(0)


async def test_multi_axe_no_serious_or_critical_violations(page, base_url):
    await _open_page(page, base_url)
    await _open_multi(page)
    await page.locator(M_OPTION, has_text="Design").click()  # render a pill
    await expect(page.locator(M_TOKEN)).to_have_count(1)
    try:
        await page.add_script_tag(url=AXE_CDN)
    except Exception:
        pytest.skip("axe-core CDN unreachable in this harness")
    await page.wait_for_function("() => window.axe", timeout=5000)
    results = await page.evaluate(
        "async () => await window.axe.run("
        "\"[data-testid='combobox-multi-container']\", "
        "{ runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa'] })"
    )
    serious = [v for v in results["violations"] if v["impact"] in ("serious", "critical")]
    detail = "; ".join(
        v["id"] + " -> " + ", ".join(n.get("target", [""])[0] for n in v.get("nodes", []))
        for v in serious
    )
    assert not serious, "axe serious/critical violations: " + detail
