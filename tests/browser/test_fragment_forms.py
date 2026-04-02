"""Test forms inside boosted layouts: fragment island isolation, hx-select override."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_form_renders_inside_fragment_island(page, base_url):
    """Form page renders with fragment island wrapper and hx-disinherit."""
    await page.goto(base_url + "/form")
    await wait_for_alpine(page)

    # Fragment island exists with hx-disinherit
    island = page.locator("#test-island")
    disinherit = await island.get_attribute("hx-disinherit")
    assert "hx-select" in disinherit
    assert "hx-target" in disinherit
    assert "hx-swap" in disinherit


async def test_form_submit_targets_island_not_main(page, base_url):
    """Form submit swaps into fragment island result, not #main."""
    await page.goto(base_url + "/form")
    await wait_for_alpine(page)

    await page.fill("[data-testid='form-input']", "test value")
    await page.click("[data-testid='form-submit']")
    await wait_for_htmx(page)

    # Result appeared in the island result div
    result = await page.text_content("#form-result")
    assert "Saved successfully" in result

    # Shell survived — sidebar still present
    assert await page.is_visible(".chirpui-app-shell__sidebar")

    # Page heading survived — we didn't replace the whole page
    assert await page.text_content("[data-testid='page-heading']") == "Form Test"


async def test_form_has_unset_hx_select(page, base_url):
    """Form inside boosted layout must have hx-select='unset' to override inheritance."""
    await page.goto(base_url + "/form")
    await wait_for_alpine(page)

    form = page.locator("form.chirpui-form")
    hx_select = await form.get_attribute("hx-select")
    assert hx_select == "unset", (
        f"Form hx-select should be 'unset' to override inherited #page-content, got: {hx_select}"
    )


async def test_form_suppresses_view_transition(page, base_url):
    """Form swap uses transition:false to prevent VT flash."""
    await page.goto(base_url + "/form")
    await wait_for_alpine(page)

    form = page.locator("form.chirpui-form")
    hx_swap = await form.get_attribute("hx-swap")
    assert "transition:false" in hx_swap


async def test_form_submit_then_nav_works(page, base_url):
    """After form submit, boosted nav still works correctly."""
    await page.goto(base_url + "/form")
    await wait_for_alpine(page)

    # Submit form
    await page.click("[data-testid='form-submit']")
    await wait_for_htmx(page)

    # Navigate away
    await page.click("a[href='/']")
    await wait_for_htmx(page)

    assert await page.text_content("[data-testid='page-heading']") == "Home"
    assert await page.is_visible(".chirpui-app-shell__sidebar")
