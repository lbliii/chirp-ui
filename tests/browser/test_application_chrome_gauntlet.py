"""Browser gauntlet for representative application chrome families."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


VIEWPORTS = [
    pytest.param(320, 640, id="phone-narrow"),
    pytest.param(390, 844, id="phone"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(1280, 900, id="desktop"),
]

FAMILIES = {
    "cloud": ("Cloud Control Plane", "Deploy", "Search cloud"),
    "suite": ("Suite Work Hub", "Create task", "Search work"),
    "knowledge": ("Knowledge Workbench", "New note", "Search docs"),
    "business": ("Business Object Console", "Add event", "Search accounts"),
}


async def open_gauntlet(page, base_url: str, width: int = 768, height: int = 1024):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/application-chrome-gauntlet")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_application_chrome_gauntlet_keeps_family_chrome_intact(
    page, base_url, width, height
):
    await open_gauntlet(page, base_url, width=width, height=height)

    await assert_no_document_horizontal_overflow(
        page, f"application-chrome-gauntlet-{width}x{height}"
    )

    for family_id, (title, action, search_label) in FAMILIES.items():
        family = page.get_by_test_id(f"chrome-family-{family_id}")
        await expect(family.get_by_role("heading", name=title)).to_be_visible()
        await expect(family.get_by_role("button", name=action)).to_be_visible()
        await expect(family.get_by_role("button", name=search_label)).to_be_visible()
        await expect(family.get_by_role("navigation", name="Navigation")).to_be_visible()
        await expect(family.get_by_role("navigation", name="Subsection navigation")).to_be_visible()

        route_tabs = family.locator(".chirpui-route-tabs")
        await expect(route_tabs).to_be_visible()
        if width <= 640:
            metrics = await route_tabs.evaluate(
                """(tab) => {
                    const style = getComputedStyle(tab);
                    const rect = tab.getBoundingClientRect();
                    return {
                        height: Math.round(rect.height),
                        overflowX: style.overflowX,
                        flexWrap: style.flexWrap,
                    };
                }"""
            )
            assert metrics["height"] < 96, metrics
            assert metrics["flexWrap"] == "nowrap", metrics
            assert metrics["overflowX"] in {"auto", "scroll"}, metrics


@pytest.mark.parametrize(("family_id", "search_label"), [
    ("cloud", "Search cloud"),
    ("suite", "Search work"),
    ("knowledge", "Search docs"),
    ("business", "Search accounts"),
])
async def test_application_chrome_gauntlet_command_triggers_focus_palettes(
    page, base_url, family_id, search_label
):
    await open_gauntlet(page, base_url, width=390, height=844)

    family = page.get_by_test_id(f"chrome-family-{family_id}")
    await family.get_by_role("button", name=search_label).click()
    palette = page.locator(f"#{family_id}-palette")
    await palette.wait_for(state="visible", timeout=2000)
    assert await palette.evaluate("el => el.open")
    assert await page.evaluate(
        f"() => document.activeElement?.closest('#{family_id}-palette') !== null"
    )
    await page.keyboard.press("Escape")
