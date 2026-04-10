"""Test split panel: renders, handle has ARIA, drag updates split."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_split_panel_renders_both_panes(page, base_url):
    """Both panes render with content."""
    await page.goto(base_url + "/split-panel")
    await wait_for_alpine(page)

    first = page.locator("[data-testid='pane-first']")
    second = page.locator("[data-testid='pane-second']")

    assert await first.is_visible()
    assert await second.is_visible()
    assert "First pane" in await first.text_content()
    assert "Second pane" in await second.text_content()


async def test_split_panel_handle_has_separator_role(page, base_url):
    """Handle element has role=separator for accessibility."""
    await page.goto(base_url + "/split-panel")
    await wait_for_alpine(page)

    handle = page.locator(".chirpui-split-panel__handle")
    assert await handle.get_attribute("role") == "separator"

    valuenow = await handle.get_attribute("aria-valuenow")
    assert valuenow is not None
    assert float(valuenow) == 50.0


async def test_split_panel_drag_changes_split(page, base_url):
    """Dragging the handle updates the split percentage."""
    await page.goto(base_url + "/split-panel")
    await wait_for_alpine(page)

    handle = page.locator(".chirpui-split-panel__handle")
    box = await handle.bounding_box()

    # Drag handle 50px to the right
    await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    await page.mouse.down()
    await page.mouse.move(box["x"] + box["width"] / 2 + 50, box["y"] + box["height"] / 2)
    await page.mouse.up()
    await page.wait_for_timeout(100)

    # Check that aria-valuenow changed from initial 50
    valuenow = await handle.get_attribute("aria-valuenow")
    assert valuenow is not None
    assert float(valuenow) != 50.0
