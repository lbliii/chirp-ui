"""Responsive composition gauntlet.

This suite exercises ChirpUI as downstream apps compose it: many components
sharing one shell, dense controls in the same row, hostile labels, and
viewport pressure from phone through desktop.
"""

from pathlib import Path

import pytest

from tests.browser.conftest import wait_for_alpine

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

ARTIFACT_DIR = Path("tests/browser/artifacts")

VIEWPORTS = [
    pytest.param(320, 640, id="phone-320"),
    pytest.param(375, 812, id="phone-375"),
    pytest.param(430, 932, id="phone-430"),
    pytest.param(768, 1024, id="tablet-portrait"),
    pytest.param(1024, 768, id="tablet-landscape"),
    pytest.param(1280, 800, id="desktop-1280"),
    pytest.param(1440, 900, id="desktop-1440"),
]


async def _open_gauntlet(page, base_url: str, width: int, height: int) -> None:
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + "/gauntlet")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def _assert_no_failures(page, failures, label: str) -> None:
    if failures:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(ARTIFACT_DIR / f"{label}.png"), full_page=True)
    assert not failures, "\n".join(str(failure) for failure in failures)


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_gauntlet_has_no_document_horizontal_overflow(page, base_url, width, height):
    await _open_gauntlet(page, base_url, width, height)

    result = await page.evaluate(
        """() => {
            const root = document.documentElement;
            const overflow = Math.ceil(root.scrollWidth - root.clientWidth);
            if (overflow <= 1) return { overflow, offenders: [] };

            const viewport = root.clientWidth;
            const offenders = [...document.body.querySelectorAll("*")]
                .filter((el) => {
                    const style = getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    return style.display !== "none"
                        && style.visibility !== "hidden"
                        && rect.width > 0
                        && rect.height > 0
                        && (rect.right > viewport + 1 || rect.left < -1);
                })
                .slice(0, 8)
                .map((el) => ({
                    tag: el.tagName.toLowerCase(),
                    className: el.className,
                    text: (el.textContent || "").trim().slice(0, 80),
                    rect: (() => {
                        const r = el.getBoundingClientRect();
                        return { left: r.left, right: r.right, width: r.width };
                    })(),
                }));
            return { overflow, offenders };
        }"""
    )

    failures = []
    if result["overflow"] > 1:
        failures.append(
            {
                "viewport": f"{width}x{height}",
                "overflow": result["overflow"],
                "offenders": result["offenders"],
            }
        )
    await _assert_no_failures(page, failures, f"gauntlet-overflow-{width}x{height}")


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_gauntlet_common_compositions_do_not_overlap(page, base_url, width, height):
    await _open_gauntlet(page, base_url, width, height)

    failures = await page.evaluate(
        """() => {
            function visible(el) {
                const style = getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style.display !== "none"
                    && style.visibility !== "hidden"
                    && rect.width > 0
                    && rect.height > 0;
            }
            function overlap(a, b) {
                const left = Math.max(a.left, b.left);
                const right = Math.min(a.right, b.right);
                const top = Math.max(a.top, b.top);
                const bottom = Math.min(a.bottom, b.bottom);
                return Math.max(0, right - left) * Math.max(0, bottom - top);
            }

            const failures = [];
            const containers = [
                ...document.querySelectorAll("[data-gauntlet-no-overlap] .chirpui-grid"),
                ...document.querySelectorAll("[data-gauntlet-no-overlap] .chirpui-frame"),
                ...document.querySelectorAll("[data-gauntlet-control-group]"),
            ];

            for (const container of containers) {
                const children = [...container.children].filter(visible);
                for (let i = 0; i < children.length; i += 1) {
                    for (let j = i + 1; j < children.length; j += 1) {
                        const a = children[i].getBoundingClientRect();
                        const b = children[j].getBoundingClientRect();
                        if (overlap(a, b) > 4) {
                            failures.push({
                                container: container.className || container.dataset.gauntletControlGroup,
                                a: children[i].className || children[i].tagName,
                                b: children[j].className || children[j].tagName,
                                overlap: overlap(a, b),
                            });
                        }
                    }
                }
            }
            return failures;
        }"""
    )

    await _assert_no_failures(page, failures, f"gauntlet-overlap-{width}x{height}")


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_gauntlet_control_rows_keep_coherent_heights(page, base_url, width, height):
    await _open_gauntlet(page, base_url, width, height)

    failures = await page.evaluate(
        """() => {
            const failures = [];
            const selector = [
                ":scope > .chirpui-btn",
                ":scope > .chirpui-dropdown",
                ":scope > .chirpui-ascii-toggle",
                ":scope > .chirpui-icon-btn",
                ":scope > .chirpui-pagination",
                ":scope > .chirpui-segmented",
            ].join(",");

            for (const group of document.querySelectorAll("[data-gauntlet-control-group]")) {
                const controls = [...group.querySelectorAll(selector)]
                    .filter((el) => {
                        const rect = el.getBoundingClientRect();
                        const style = getComputedStyle(el);
                        return style.display !== "none"
                            && style.visibility !== "hidden"
                            && rect.width > 0
                            && rect.height > 0;
                    });
                if (controls.length < 2) continue;
                const heights = controls.map((el) => Math.round(el.getBoundingClientRect().height));
                const min = Math.min(...heights);
                const max = Math.max(...heights);
                if (max - min > 6) {
                    failures.push({
                        group: group.dataset.gauntletControlGroup,
                        heights,
                        labels: controls.map((el) => (el.textContent || el.getAttribute("aria-label") || el.className).trim().slice(0, 40)),
                    });
                }
            }
            return failures;
        }"""
    )

    await _assert_no_failures(page, failures, f"gauntlet-control-heights-{width}x{height}")


@pytest.mark.parametrize(
    ("width", "height"),
    [
        pytest.param(320, 640, id="phone-320"),
        pytest.param(375, 812, id="phone-375"),
        pytest.param(768, 1024, id="tablet-portrait"),
    ],
)
async def test_gauntlet_touch_critical_controls_are_not_tiny(page, base_url, width, height):
    await _open_gauntlet(page, base_url, width, height)

    failures = await page.evaluate(
        """() => {
            const selector = [
                ":scope > .chirpui-btn",
                ":scope > .chirpui-dropdown",
                ":scope > .chirpui-ascii-toggle",
                ":scope > .chirpui-icon-btn",
                ":scope > .chirpui-pagination a",
                ":scope > .chirpui-pagination button",
            ].join(",");
            const failures = [];
            for (const group of document.querySelectorAll("[data-gauntlet-touch-critical]")) {
                for (const el of group.querySelectorAll(selector)) {
                    const rect = el.getBoundingClientRect();
                    const style = getComputedStyle(el);
                    if (style.display === "none" || style.visibility === "hidden") continue;
                    if (rect.width < 32 || rect.height < 32) {
                        failures.push({
                            group: group.dataset.gauntletControlGroup,
                            className: el.className,
                            text: (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 60),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                        });
                    }
                }
            }
            return failures;
        }"""
    )

    await _assert_no_failures(page, failures, f"gauntlet-touch-{width}x{height}")


async def test_gauntlet_linked_nav_branches_route_without_disclosure_conflict(page, base_url):
    await _open_gauntlet(page, base_url, 768, 1024)

    assert await page.locator(".chirpui-nav-tree--linked-branches summary").count() == 0
    branch = page.locator(
        ".chirpui-nav-tree--linked-branches .chirpui-nav-tree__item--branch"
        " > .chirpui-nav-tree__link"
    ).first
    href = await branch.get_attribute("href")
    assert href == "/gauntlet/workspace"
    assert await page.get_by_text("Hidden until open").count() == 0


async def test_gauntlet_survives_large_text_pressure(page, base_url):
    await _open_gauntlet(page, base_url, 375, 812)
    await page.add_style_tag(content="html { font-size: 20px !important; }")
    await page.wait_for_timeout(100)

    overflow = await page.evaluate(
        "() => Math.ceil(document.documentElement.scrollWidth - document.documentElement.clientWidth)"
    )
    failures = []
    if overflow > 1:
        failures.append({"viewport": "375x812", "font_size": "20px", "overflow": overflow})
    await _assert_no_failures(page, failures, "gauntlet-large-text")
