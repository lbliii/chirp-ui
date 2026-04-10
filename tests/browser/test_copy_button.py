"""Test copy button: click copies text, feedback appears."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_copy_button_shows_copied_feedback(page, base_url):
    """Clicking copy button shows 'Copied!' feedback."""
    await page.goto(base_url + "/copy-button")
    await wait_for_alpine(page)

    # Grant clipboard permission and mock clipboard API
    await page.evaluate("""
        navigator.clipboard.writeText = async (text) => {
            window._lastCopied = text;
        };
    """)

    btn = page.locator(".chirpui-copy-btn")
    await btn.click()
    await page.wait_for_timeout(200)

    done = page.locator(".chirpui-copy-btn__done")
    assert await done.is_visible()
    assert "Copied" in await done.text_content()


async def test_copy_button_copies_correct_text(page, base_url):
    """Copy button copies the data-copy-text value."""
    await page.goto(base_url + "/copy-button")
    await wait_for_alpine(page)

    await page.evaluate("""
        navigator.clipboard.writeText = async (text) => {
            window._lastCopied = text;
        };
    """)

    await page.click(".chirpui-copy-btn")
    await page.wait_for_timeout(200)

    copied = await page.evaluate("window._lastCopied")
    assert copied == "Hello clipboard!"


async def test_copy_button_reverts_after_timeout(page, base_url):
    """Feedback reverts to original label after 1.5s."""
    await page.goto(base_url + "/copy-button")
    await wait_for_alpine(page)

    await page.evaluate("""
        navigator.clipboard.writeText = async (text) => {
            window._lastCopied = text;
        };
    """)

    await page.click(".chirpui-copy-btn")
    await page.wait_for_timeout(200)

    # "Copied!" should be visible
    assert await page.locator(".chirpui-copy-btn__done").is_visible()

    # Wait for revert (1.5s timeout + buffer)
    await page.wait_for_timeout(1600)

    label = page.locator(".chirpui-copy-btn__label")
    assert await label.is_visible()
