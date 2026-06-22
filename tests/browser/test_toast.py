"""Test toast: render, dismiss, stack, swipe, and server-driven status."""

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_toast_appears_on_trigger(page, base_url):
    """Triggering a toast appends it to the container."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator(".qa-toast")
    await toast.wait_for(state="visible", timeout=3000)

    text = await toast.text_content()
    assert "Operation successful" in text


async def test_toast_dismissible(page, base_url):
    """Clicking dismiss button removes the toast."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator(".qa-toast")
    await toast.wait_for(state="visible", timeout=3000)

    await page.click(".chirpui-toast__close")
    await page.wait_for_timeout(300)

    assert await page.locator(".qa-toast").count() == 0


async def test_toast_has_alert_role(page, base_url):
    """Toast has role=alert for screen readers."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator(".qa-toast")
    await toast.wait_for(state="visible", timeout=3000)

    assert await toast.get_attribute("role") == "alert"


async def test_toast_stacks_multiple(page, base_url):
    """Multiple OOB toasts stack in the container."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-stack']")
    await wait_for_htmx(page)

    toasts = page.locator("#chirpui-toasts .chirpui-toast")
    await toasts.first.wait_for(state="visible", timeout=3000)
    assert await toasts.count() == 3


async def test_toast_swipe_dismiss(page, base_url):
    """Dragging a toast off-screen dismisses it."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-toast']")
    await wait_for_htmx(page)

    toast = page.locator(".qa-toast")
    await toast.wait_for(state="visible", timeout=3000)
    await page.wait_for_function(
        """() => {
            const toast = document.querySelector('.qa-toast');
            return toast
                && toast._x_dataStack
                && typeof toast._x_dataStack[0]?.onPointerUp === 'function';
        }""",
        timeout=3000,
    )

    await page.evaluate(
        """() => {
            const toast = document.querySelector('.qa-toast');
            const data = toast._x_dataStack[0];
            const rect = toast.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            toast.setPointerCapture = () => {};
            toast.releasePointerCapture = () => {};
            data.onPointerDown({
                pointerType: 'mouse',
                button: 0,
                clientX: x,
                clientY: y,
                target: toast,
                closest: () => null,
                pointerId: 1,
            });
            data.onPointerMove({ clientX: x + 120, clientY: y });
            data.onPointerUp({ clientX: x + 120, clientY: y, pointerId: 1 });
        }"""
    )
    await page.wait_for_timeout(400)

    assert await page.locator(".qa-toast").count() == 0


async def test_toast_status_flow(page, base_url):
    """Pending toast is replaced by a resolved success toast."""
    await page.goto(base_url + "/toast")
    await wait_for_alpine(page)

    await page.click("[data-testid='trigger-status']")
    await wait_for_htmx(page)

    pending = page.locator("#status-toast")
    await pending.wait_for(state="visible", timeout=3000)
    assert "chirpui-toast--loading" in (await pending.get_attribute("class") or "")

    await page.click("[data-testid='trigger-status-resolve']")
    await wait_for_htmx(page)

    resolved = page.locator("#status-toast")
    await resolved.wait_for(state="visible", timeout=3000)
    assert "chirpui-toast--success" in (await resolved.get_attribute("class") or "")
    assert "Saved!" in (await resolved.text_content() or "")
