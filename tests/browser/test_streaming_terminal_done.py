"""Terminal-done regression: dropped SSE must clear shimmer and aria-busy."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_sse_error_clears_active_and_aria_busy(page, base_url):
    """Simulated htmx:sseError must run chirpuiStreamLifecycle terminal cleanup."""
    await page.goto(base_url + "/streaming")
    await wait_for_alpine(page)

    block = page.locator(".chirpui-streaming-block").filter(
        has=page.locator("[data-testid='sse-bubble-content']")
    )
    await block.wait_for(state="visible")
    assert "chirpui-streaming-block--active" in (await block.get_attribute("class") or "")

    await block.evaluate(
        """el => {
            el.setAttribute('aria-busy', 'true');
            el.dispatchEvent(new Event('htmx:sseError', { bubbles: true }));
        }"""
    )

    classes = await block.get_attribute("class") or ""
    assert "chirpui-streaming-block--active" not in classes
    assert await block.get_attribute("aria-busy") is None

    article = page.locator(".chirpui-message-bubble").filter(
        has=page.locator("[data-testid='sse-bubble-content']")
    )
    assert await article.get_attribute("aria-busy") is None
