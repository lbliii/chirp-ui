"""Test inline edit: display/edit/save cycle inside a fragment island."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_inline_edit_shows_display_mode(page, base_url):
    """Initial render shows the display value and edit button."""
    await page.goto(base_url + "/inline-edit")
    await wait_for_alpine(page)

    value = await page.text_content("[data-testid='display-value']")
    assert "Hello World" in value

    assert await page.is_visible("[data-testid='edit-btn']")


async def test_inline_edit_switches_to_edit_mode(page, base_url):
    """Clicking edit loads the edit form via htmx."""
    await page.goto(base_url + "/inline-edit")
    await wait_for_alpine(page)

    await page.click("[data-testid='edit-btn']")
    await wait_for_htmx(page)

    # Edit input should appear
    assert await page.is_visible("[data-testid='edit-input']")
    assert await page.is_visible("[data-testid='save-btn']")
    assert await page.is_visible("[data-testid='cancel-btn']")


async def test_inline_edit_cancel_reverts(page, base_url):
    """Cancel returns to display mode with original value."""
    await page.goto(base_url + "/inline-edit")
    await wait_for_alpine(page)

    await page.click("[data-testid='edit-btn']")
    await wait_for_htmx(page)

    await page.click("[data-testid='cancel-btn']")
    await wait_for_htmx(page)

    value = await page.text_content("[data-testid='display-value']")
    assert "Hello World" in value


async def test_inline_edit_save_updates_value(page, base_url):
    """Save submits the form and displays the new value."""
    await page.goto(base_url + "/inline-edit")
    await wait_for_alpine(page)

    await page.click("[data-testid='edit-btn']")
    await wait_for_htmx(page)

    await page.fill("[data-testid='edit-input']", "Updated")
    await page.click("[data-testid='save-btn']")
    await wait_for_htmx(page)

    value = await page.text_content("[data-testid='display-value']")
    assert "Saved Value" in value


async def test_inline_edit_stays_inside_island(page, base_url):
    """Inline edit swaps stay inside the fragment island, don't affect shell."""
    await page.goto(base_url + "/inline-edit")
    await wait_for_alpine(page)

    await page.click("[data-testid='edit-btn']")
    await wait_for_htmx(page)

    # Shell survived
    assert await page.is_visible(".chirpui-app-shell__sidebar")
    assert await page.text_content("[data-testid='page-heading']") == "Inline Edit Test"

    await page.click("[data-testid='save-btn']")
    await wait_for_htmx(page)

    # Still survived
    assert await page.is_visible(".chirpui-app-shell__sidebar")
    assert await page.text_content("[data-testid='page-heading']") == "Inline Edit Test"
