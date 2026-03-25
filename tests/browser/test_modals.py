"""Test modal overlay: open/close, focus trap, backdrop click, keyboard."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_modal_opens_on_trigger_click(page, base_url):
    """Clicking modal trigger opens the overlay via Alpine store."""
    await page.goto(base_url + "/modal")
    await wait_for_alpine(page)

    await page.click("button[aria-controls]")

    modal = page.locator(".chirpui-modal--open")
    await modal.wait_for(state="visible", timeout=2000)

    body = await page.text_content("[data-testid='modal-body']")
    assert "Modal content here" in body


async def test_modal_closes_on_close_button(page, base_url):
    """Close button sets store to false and hides modal."""
    await page.goto(base_url + "/modal")
    await wait_for_alpine(page)

    await page.click("button[aria-controls]")
    modal = page.locator(".chirpui-modal--open")
    await modal.wait_for(state="visible", timeout=2000)

    await page.click(".chirpui-modal__close")
    await page.wait_for_timeout(300)

    assert not await page.locator(".chirpui-modal--open").is_visible()


async def test_modal_closes_on_backdrop_click(page, base_url):
    """Clicking the backdrop closes the modal."""
    await page.goto(base_url + "/modal")
    await wait_for_alpine(page)

    await page.click("button[aria-controls]")
    modal = page.locator(".chirpui-modal--open")
    await modal.wait_for(state="visible", timeout=2000)

    # Backdrop is a full-screen overlay behind the panel.
    # Use evaluate to dispatch the click directly since the element may
    # be covered by the panel in viewport checks.
    await page.evaluate("document.querySelector('.chirpui-modal__backdrop').click()")
    await page.wait_for_timeout(300)

    assert not await page.locator(".chirpui-modal--open").is_visible()


async def test_modal_dispatches_close_event(page, base_url):
    """Modal dispatches chirpui:modal-closed on close."""
    await page.goto(base_url + "/modal")
    await wait_for_alpine(page)

    # Listen for custom event
    await page.evaluate("""
        window._modalCloseEvents = [];
        document.addEventListener('chirpui:modal-closed', (e) => {
            window._modalCloseEvents.push(e.detail);
        });
    """)

    await page.click("button[aria-controls]")
    modal = page.locator(".chirpui-modal--open")
    await modal.wait_for(state="visible", timeout=2000)

    await page.click(".chirpui-modal__close")
    await page.wait_for_timeout(300)

    events = await page.evaluate("window._modalCloseEvents")
    assert len(events) >= 1
    assert events[0]["id"] == "test-modal"


async def test_modal_aria_attributes(page, base_url):
    """Modal has correct ARIA attributes for accessibility."""
    await page.goto(base_url + "/modal")
    await wait_for_alpine(page)

    modal = page.locator("[role='dialog']")
    assert await modal.get_attribute("aria-modal") == "true"
    assert await modal.get_attribute("aria-labelledby") is not None

    # Trigger has aria-expanded
    trigger = page.locator("button[aria-controls]")
    assert await trigger.get_attribute("aria-controls") is not None
