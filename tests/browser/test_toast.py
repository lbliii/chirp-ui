"""Test toast: render, dismiss, ARIA."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_toast_appears_on_trigger(page, base_url):
    """Triggering a toast appends it to the container."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator("[data-testid='toast-item']")
    await toast.wait_for(state="visible", timeout=3000)

    text = await toast.text_content()
    assert "Operation successful" in text


async def test_toast_dismissible(page, base_url):
    """Clicking dismiss button removes the toast."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator("[data-testid='toast-item']")
    await toast.wait_for(state="visible", timeout=3000)

    await page.click(".chirpui-toast__close")
    await page.wait_for_timeout(300)

    assert await page.locator("[data-testid='toast-item']").count() == 0


async def test_toast_has_alert_role(page, base_url):
    """Toast has role=alert for screen readers."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator("[data-testid='toast-item']")
    await toast.wait_for(state="visible", timeout=3000)

    assert await toast.get_attribute("role") == "alert"
