"""Browser proof for dense object chrome recipes."""

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


async def open_dense_object_chrome(page, base_url: str, width: int = 768, height: int = 1024):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/dense-object-chrome")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_dense_object_chrome_recipes_render_expected_layers(page, base_url):
    await open_dense_object_chrome(page, base_url)

    project = page.get_by_test_id("dense-project-object")
    settings = page.get_by_test_id("dense-settings-object")

    await expect(
        project.get_by_role("toolbar", name="Project workspace navigation")
    ).to_be_visible()
    await expect(project.get_by_role("navigation", name="Primary")).to_be_visible()
    await expect(project.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(project.get_by_role("navigation", name="Subsection navigation")).to_be_visible()
    await expect(project.get_by_role("toolbar", name="Project page tools")).to_be_visible()
    await expect(project.get_by_role("heading", name="chirp-ui / navigation")).to_be_visible()

    await expect(
        settings.get_by_role("toolbar", name="Settings workspace navigation")
    ).to_be_visible()
    await expect(settings.get_by_role("navigation", name="Primary")).to_be_visible()
    await expect(settings.get_by_role("navigation", name="Breadcrumb")).to_be_visible()
    await expect(settings.get_by_role("navigation", name="Subsection navigation")).to_be_visible()
    await expect(settings.get_by_role("heading", name="Access policy")).to_be_visible()


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_dense_object_chrome_responsive_surfaces_do_not_overflow(
    page, base_url, width, height
):
    await open_dense_object_chrome(page, base_url, width=width, height=height)

    await assert_no_document_horizontal_overflow(page, f"dense-object-chrome-{width}x{height}")

    for test_id in ["dense-project-object", "dense-settings-object"]:
        section = page.get_by_test_id(test_id)
        await expect(section.locator(".chirpui-command-palette-trigger")).to_be_visible()
        await expect(section.locator(".chirpui-route-tab").first).to_be_visible()
        await expect(section.locator(".chirpui-route-tabs")).to_be_visible()

    if width <= 640:
        metrics = await page.locator(".chirpui-route-tabs").evaluate_all(
            """(tabs) => tabs.map((tab) => {
                const style = getComputedStyle(tab);
                const rect = tab.getBoundingClientRect();
                return {
                    height: Math.round(rect.height),
                    overflowX: style.overflowX,
                    flexWrap: style.flexWrap,
                    scrolls: tab.scrollWidth > tab.clientWidth,
                };
            })"""
        )
        assert metrics
        for metric in metrics:
            assert metric["height"] < 96, metric
            assert metric["flexWrap"] == "nowrap", metric
            assert metric["overflowX"] in {"auto", "scroll"}, metric


async def test_dense_object_chrome_command_triggers_open_named_palettes(page, base_url):
    await open_dense_object_chrome(page, base_url)

    await page.get_by_role("button", name="Search project").click()
    project_dialog = page.locator("#project-object-palette")
    await project_dialog.wait_for(state="visible", timeout=2000)
    assert await project_dialog.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.closest('#project-object-palette') !== null"
    )

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(100)
    assert not await project_dialog.evaluate("el => el.open")

    await page.get_by_role("button", name="Search settings").click()
    settings_dialog = page.locator("#settings-object-palette")
    await settings_dialog.wait_for(state="visible", timeout=2000)
    assert await settings_dialog.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.closest('#settings-object-palette') !== null"
    )


async def test_dense_object_chrome_badges_reserve_without_bad_counts(page, base_url):
    await open_dense_object_chrome(page, base_url, width=390, height=844)

    await expect(
        page.locator(".chirpui-primary-nav__badge[aria-label='27 open issues']")
    ).to_have_text("27")
    await expect(
        page.locator(".chirpui-route-tab__badge[aria-label='12 overview updates']")
    ).to_have_text("12")

    reserved_badges = page.locator(
        ".chirpui-primary-nav__badge--reserved, .chirpui-route-tab__badge--reserved"
    )
    assert await reserved_badges.count() >= 3
    assert await reserved_badges.evaluate_all(
        """(badges) => badges.every((badge) =>
            badge.getAttribute("aria-hidden") === "true"
            && badge.getBoundingClientRect().width > 0
            && !badge.textContent.trim()
        )"""
    )

    loading_badges = page.locator(
        ".chirpui-primary-nav__badge--loading, .chirpui-route-tab__badge--loading"
    )
    assert await loading_badges.count() >= 2


async def test_dense_object_chrome_overflow_controls_remain_reachable(page, base_url):
    await open_dense_object_chrome(page, base_url, width=320, height=640)

    await page.locator("#project-object-more-menu .chirpui-dropdown__trigger").click()
    await expect(page.get_by_role("menuitem", name="Export routes")).to_be_visible()
    await page.keyboard.press("Escape")

    await page.locator("#settings-audit-menu .chirpui-dropdown__trigger").click()
    await expect(page.get_by_role("menuitem", name="Export CSV")).to_be_visible()

    await page.get_by_label("Show collapsed breadcrumbs").click()
    await expect(page.get_by_role("link", name="chirp-ui")).to_be_visible()
