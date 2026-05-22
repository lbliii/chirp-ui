"""Browser proof for dense object chrome recipes."""

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine
from tests.browser.gauntlet_detectors import (
    assert_direct_child_margins_trimmed,
    assert_direct_children_contained,
    assert_no_document_horizontal_overflow,
)

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


@pytest.mark.parametrize(("width", "height"), [(320, 640), (768, 1024)])
async def test_dense_metadata_primitives_own_pressure(page, base_url, width, height):
    await open_dense_object_chrome(page, base_url, width=width, height=height)

    await page.evaluate(
        """() => {
            const longText = "metadata-owner-" + "theta".repeat(24);
            document.querySelector("#dense-metadata-proof")?.remove();
            document.querySelector("main")?.insertAdjacentHTML(
                "afterbegin",
                `<section id="dense-metadata-proof" style="max-width: min(100%, 20rem);">
                    <span class="chirpui-inline-counter" title="${longText}">
                        <span class="chirpui-inline-counter__mark">M</span>
                        <span class="chirpui-inline-counter__value">${longText}</span>
                        <span class="chirpui-inline-counter__label">${longText}</span>
                    </span>
                    <div class="chirpui-latest-line">
                        <span class="chirpui-latest-line__label">Latest</span>
                        <span class="chirpui-tooltip chirpui-latest-line__tooltip">
                            <a class="chirpui-latest-line__title" href="#">${longText}</a>
                        </span>
                        <span class="chirpui-latest-line__meta">
                            <a href="#">${longText}</a>
                            <span>${longText}</span>
                        </span>
                    </div>
                    <div class="chirpui-chip-group" aria-label="Metadata chips">
                        <span class="chirpui-chip">${longText}</span>
                        <a class="chirpui-chip" href="#">${longText}</a>
                    </div>
                </section>`
            );
        }"""
    )

    await assert_no_document_horizontal_overflow(page, f"dense-metadata-{width}x{height}")
    await assert_direct_children_contained(
        page,
        "#dense-metadata-proof .chirpui-latest-line",
        f"dense-latest-line-{width}x{height}",
    )
    await assert_direct_child_margins_trimmed(
        page,
        "#dense-metadata-proof .chirpui-latest-line",
        f"dense-latest-line-{width}x{height}",
    )
    await assert_direct_children_contained(
        page,
        "#dense-metadata-proof .chirpui-chip-group",
        f"dense-chip-group-{width}x{height}",
    )
    await assert_direct_child_margins_trimmed(
        page,
        "#dense-metadata-proof .chirpui-chip-group",
        f"dense-chip-group-{width}x{height}",
    )
    metrics = await page.evaluate(
        """() => {
            const proof = document.querySelector("#dense-metadata-proof");
            const counter = proof.querySelector(".chirpui-inline-counter");
            const mark = proof.querySelector(".chirpui-inline-counter__mark");
            const value = proof.querySelector(".chirpui-inline-counter__value");
            const latest = proof.querySelector(".chirpui-latest-line");
            const latestFirstChild = latest.querySelector(":scope > :not(script, style, template)");
            const tooltip = proof.querySelector(".chirpui-latest-line__tooltip");
            const meta = proof.querySelector(".chirpui-latest-line__meta");
            const chipGroup = proof.querySelector(".chirpui-chip-group");
            const chip = proof.querySelector(".chirpui-chip");
            const proofRect = proof.getBoundingClientRect();
            return {
                proofOverflow: Math.ceil(proof.scrollWidth - proof.clientWidth),
                counterOverflow: Math.ceil(counter.scrollWidth - counter.clientWidth),
                counterContained: counter.getBoundingClientRect().right <= proofRect.right + 1,
                markFlex: getComputedStyle(mark).flex,
                valueWrap: getComputedStyle(value).overflowWrap,
                latestOverflow: Math.ceil(latest.scrollWidth - latest.clientWidth),
                latestContained: latest.getBoundingClientRect().right <= proofRect.right + 1,
                latestFirstMarginStart: getComputedStyle(latestFirstChild).marginBlockStart,
                latestFirstMarginEnd: getComputedStyle(latestFirstChild).marginBlockEnd,
                tooltipDisplay: getComputedStyle(tooltip).display,
                metaWrap: getComputedStyle(meta).flexWrap,
                chipGroupOverflow: Math.ceil(chipGroup.scrollWidth - chipGroup.clientWidth),
                chipGroupContained: chipGroup.getBoundingClientRect().right <= proofRect.right + 1,
                chipMarginStart: getComputedStyle(chip).marginBlockStart,
                chipMarginEnd: getComputedStyle(chip).marginBlockEnd,
                chipOverflow: Math.ceil(chip.scrollWidth - chip.clientWidth),
            };
        }"""
    )
    # The tooltip bubble is absolutely positioned and may expand the synthetic
    # proof section's scroll width while remaining invisible and document-safe.
    assert metrics["counterOverflow"] <= 1, metrics
    assert metrics["counterContained"], metrics
    assert metrics["markFlex"] == "0 0 auto", metrics
    assert metrics["valueWrap"] == "anywhere", metrics
    assert metrics["latestContained"], metrics
    assert metrics["latestFirstMarginStart"] == "0px", metrics
    assert metrics["latestFirstMarginEnd"] == "0px", metrics
    assert metrics["tooltipDisplay"] == "inline-flex", metrics
    assert metrics["metaWrap"] == "wrap", metrics
    assert metrics["chipGroupOverflow"] <= 1, metrics
    assert metrics["chipGroupContained"], metrics
    assert metrics["chipMarginStart"] == "0px", metrics
    assert metrics["chipMarginEnd"] == "0px", metrics
    assert metrics["chipOverflow"] > 1, metrics


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
