"""Test command palette: keyboard open, search, close."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_command_palette_opens_on_trigger_click(page, base_url):
    """Clicking the trigger button opens the command palette dialog."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.click(".chirpui-command-palette-trigger")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)

    input_el = page.locator(".chirpui-command-palette__input")
    assert await input_el.is_visible()


async def test_command_palette_opens_on_keyboard_shortcut(page, base_url):
    """Pressing Cmd+K or Ctrl+K opens the command palette."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.keyboard.press("Control+k")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)


async def test_command_palette_closes_on_escape(page, base_url):
    """Pressing Escape closes the command palette."""
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)

    await page.click(".chirpui-command-palette-trigger")
    dialog = page.locator("#command-palette")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")


# ── Arrow-key result navigation (#201) ──────────────────────────────
#
# Roving is exercised via the chirpuiCommandPalette factory methods (Playwright
# keydown is unreliable through Alpine in headless Chromium); open/type/activate
# use real events. The native <dialog> opens instantly (no transition to await).

_INPUT = "#command-palette .chirpui-command-palette__input"
_RESULTS = "#command-palette-results"
_OPTIONS = "#command-palette-results [role=option]"


async def _open(page, base_url):
    await page.goto(base_url + "/command-palette")
    await wait_for_alpine(page)
    await page.click(".chirpui-command-palette-trigger")
    await page.locator("#command-palette").wait_for(state="visible", timeout=2000)


async def _palette_move(page, delta):
    await page.evaluate(
        "(d) => { document.getElementById('command-palette')"
        ".parentElement._x_dataStack[0].move(d); }",
        delta,
    )


async def _palette_activate(page):
    await page.evaluate(
        "() => { document.getElementById('command-palette')"
        ".parentElement._x_dataStack[0].activate(); }"
    )


async def test_command_palette_results_are_listbox_options(page, base_url):
    await _open(page, base_url)
    assert await page.locator(_RESULTS).get_attribute("role") == "listbox"
    assert await page.locator(_INPUT).get_attribute("role") == "combobox"
    assert await page.locator(_INPUT).get_attribute("aria-controls") == "command-palette-results"
    ids = await page.eval_on_selector_all(_OPTIONS, "els => els.map(e => e.id)")
    assert ids == ["cmd-new", "cmd-open", "cmd-settings", "cmd-search-all"]


async def test_command_palette_first_result_auto_active(page, base_url):
    await _open(page, base_url)
    await page.wait_for_function(
        """() => {
            const inp = document.querySelector(
                '#command-palette .chirpui-command-palette__input');
            const opt = document.getElementById('cmd-new');
            return inp.getAttribute('aria-activedescendant') === 'cmd-new'
                && opt.getAttribute('aria-selected') === 'true'
                && opt.classList.contains('chirpui-command-palette__item--active');
        }""",
        timeout=4000,
    )
    assert await page.locator(_INPUT).get_attribute("aria-expanded") == "true"


async def test_command_palette_arrow_keys_rove_aria_activedescendant(page, base_url):
    await _open(page, base_url)
    await _palette_move(page, 1)  # cmd-new -> cmd-open
    await page.wait_for_function(
        """() => {
            const inp = document.querySelector(
                '#command-palette .chirpui-command-palette__input');
            return inp.getAttribute('aria-activedescendant') === 'cmd-open'
                && document.getElementById('cmd-open').getAttribute('aria-selected') === 'true'
                && document.getElementById('cmd-new').getAttribute('aria-selected') === 'false';
        }""",
        timeout=4000,
    )
    await _palette_move(page, -1)  # back to cmd-new
    await page.wait_for_function(
        "() => document.querySelector('#command-palette .chirpui-command-palette__input')"
        ".getAttribute('aria-activedescendant') === 'cmd-new'",
        timeout=4000,
    )


async def test_command_palette_enter_activates_active_option(page, base_url):
    await _open(page, base_url)
    await _palette_move(page, 1)  # cmd-open is active
    await _palette_activate(page)
    # The active option is an <a href="#cmd-open"> — activating navigates the hash.
    await page.wait_for_function(
        "() => window.location.hash === '#cmd-open'",
        timeout=4000,
    )


async def test_command_palette_htmx_results_autohighlight_first(page, base_url):
    await _open(page, base_url)
    await page.locator(_INPUT).fill("set")  # matches only "Settings"
    # Filtered results swap in via htmx; the new first (only) result auto-activates.
    await page.wait_for_function(
        """() => {
            const opts = [...document.querySelectorAll(
                '#command-palette-results [role=option]')];
            if (opts.length !== 1 || opts[0].id !== 'cmd-settings') return false;
            const inp = document.querySelector(
                '#command-palette .chirpui-command-palette__input');
            return inp.getAttribute('aria-activedescendant') === 'cmd-settings';
        }""",
        timeout=5000,
    )
