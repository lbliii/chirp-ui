"""Test streaming bubble: renders roles, ARIA attributes."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_streaming_bubble_renders_assistant_role(page, base_url):
    """Assistant bubble renders with correct role class and ARIA."""
    await page.goto(base_url + "/streaming")
    await wait_for_alpine(page)

    bubble = page.locator(".chirpui-message-bubble--assistant")
    assert await bubble.is_visible()

    label = await bubble.get_attribute("aria-label")
    assert label is not None
    assert "assistant" in label.lower()

    content = await page.text_content("[data-testid='bubble-content']")
    assert "Hello from the assistant" in content


async def test_streaming_bubble_renders_user_role(page, base_url):
    """User bubble renders with correct role class."""
    await page.goto(base_url + "/streaming")
    await wait_for_alpine(page)

    bubble = page.locator(".chirpui-message-bubble--user")
    assert await bubble.is_visible()

    content = await page.text_content("[data-testid='user-bubble-content']")
    assert "Hello from the user" in content
