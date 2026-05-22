"""Test drawer: open/close, native dialog, content visible."""

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_drawer_opens_on_trigger(page, base_url):
    """Clicking drawer trigger opens the dialog."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)
    assert await dialog.evaluate("el => el.open")

    body = await page.text_content("[data-testid='drawer-body']")
    assert "Drawer content here" in body


async def test_drawer_trigger_uses_dialog_target_controller(page, base_url):
    """Drawer trigger is wired to the shared native dialog target controller."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    trigger = page.locator(".chirpui-drawer-trigger")
    assert await trigger.get_attribute("x-data") == "chirpuiDialogTarget()"
    assert await trigger.get_attribute("data-dialog-target") == "test-drawer"


async def test_drawer_closes_on_close_button(page, base_url):
    """Close button closes the drawer dialog."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.click(".chirpui-drawer__close")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")


async def test_drawer_closes_on_escape(page, base_url):
    """Pressing Escape closes the drawer."""
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)

    assert not await dialog.evaluate("el => el.open")


@pytest.mark.parametrize(("width", "height"), [(320, 640), (768, 1024)])
async def test_drawer_region_rhythm_contains_long_content(page, base_url, width, height):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/drawer")
    await wait_for_alpine(page)

    await page.click(".chirpui-drawer-trigger")
    dialog = page.locator("#test-drawer")
    await dialog.wait_for(state="visible", timeout=2000)
    await page.evaluate(
        """() => {
            const text = "drawer-region-owner-" + "beta".repeat(30);
            const drawer = document.querySelector("#test-drawer");
            drawer.querySelector(".chirpui-drawer__title").textContent = text;
            drawer.querySelector(".chirpui-drawer__body").innerHTML = `
                <p>${text}</p>
                <p>${text}</p>
            `;
        }"""
    )

    metrics = await dialog.evaluate(
        """(dialog) => {
            const panel = dialog.querySelector(".chirpui-drawer__panel");
            const body = dialog.querySelector(".chirpui-drawer__body");
            const title = dialog.querySelector(".chirpui-drawer__title");
            const firstBodyChild = body.querySelector(":scope > :not(script, style, template)");
            return {
                panelOverflow: Math.ceil(panel.scrollWidth - panel.clientWidth),
                bodyOverflow: Math.ceil(body.scrollWidth - body.clientWidth),
                titleMarginEnd: getComputedStyle(title).marginBlockEnd,
                bodyChildMargin: getComputedStyle(firstBodyChild).marginBlockStart,
            };
        }"""
    )
    assert metrics["panelOverflow"] <= 1, metrics
    assert metrics["bodyOverflow"] <= 1, metrics
    assert metrics["titleMarginEnd"] == "0px", metrics
    assert metrics["bodyChildMargin"] == "0px", metrics
