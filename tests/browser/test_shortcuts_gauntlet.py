"""Keyboard shortcut guard + help modal parity (AI chat saga, Phase 2)."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_focus_composer_blocked_while_typing(page, base_url):
    await page.goto(base_url + "/shortcuts")
    await wait_for_alpine(page)

    composer = page.locator("#composer")
    await composer.focus()
    await composer.fill("typed")

    await page.evaluate(
        """() => {
            window.__shortcutFired = false;
            document.addEventListener("chirpui:shortcut:focus-composer", () => {
                window.__shortcutFired = true;
            });
        }"""
    )
    await page.keyboard.press("/")
    fired = await page.evaluate("() => window.__shortcutFired")
    assert fired is False
    assert await composer.input_value() == "typed"


async def test_escape_allowlisted_in_input(page, base_url):
    await page.goto(base_url + "/shortcuts")
    await wait_for_alpine(page)

    await page.keyboard.press("?")
    dialog = page.locator("#shortcuts-help")
    await expect(dialog).to_have_attribute("open", "")

    composer = page.locator("#composer")
    await composer.focus()
    await page.evaluate(
        """() => {
            window.__escapeFired = false;
            document.addEventListener("chirpui:shortcut:escape", () => {
                window.__escapeFired = true;
            });
        }"""
    )
    await page.keyboard.press("Escape")
    assert await page.evaluate("() => window.__escapeFired") is True
    await expect(dialog).not_to_have_attribute("open", "")


async def test_help_modal_lists_catalog_ids(page, base_url):
    await page.goto(base_url + "/shortcuts")
    await wait_for_alpine(page)
    await page.keyboard.press("?")

    row_ids = await page.locator("[data-shortcut-id]").evaluate_all(
        "els => els.map(el => el.getAttribute('data-shortcut-id')).sort()"
    )
    catalog_ids = await page.evaluate(
        """() => {
            const raw = document.querySelector('[x-ref="catalog"]').textContent;
            return JSON.parse(raw).map(entry => entry.id).sort();
        }"""
    )
    assert row_ids == catalog_ids
