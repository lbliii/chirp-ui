"""Reusable browser detectors for ChirpUI composition stress tests."""

from pathlib import Path
from typing import Any

from tests.browser.conftest import wait_for_alpine

ARTIFACT_DIR = Path("tests/browser/artifacts")


def artifact_label(value: str) -> str:
    """Make a stable filename fragment from a route/viewport/state label."""
    return (
        value.replace("://", "-")
        .replace("/", "-")
        .replace("#", "-")
        .replace("?", "-")
        .replace("&", "-")
        .strip("-")
    )


async def open_gauntlet(
    page,
    base_url: str,
    path: str = "/gauntlet",
    *,
    width: int = 768,
    height: int = 1024,
) -> None:
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(base_url + path)
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def assert_no_failures(page, failures: list[Any], label: str) -> None:
    if failures:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        await page.screenshot(
            path=str(ARTIFACT_DIR / f"{artifact_label(label)}.png"), full_page=True
        )
    assert not failures, "\n".join(str(failure) for failure in failures)


async def assert_no_document_horizontal_overflow(page, label: str) -> None:
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
        failures.append({"overflow": result["overflow"], "offenders": result["offenders"]})
    await assert_no_failures(page, failures, f"{label}-overflow")


async def assert_common_compositions_do_not_overlap(page, label: str) -> None:
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

    await assert_no_failures(page, failures, f"{label}-overlap")


async def assert_control_rows_keep_coherent_heights(page, label: str) -> None:
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

    await assert_no_failures(page, failures, f"{label}-control-heights")


async def assert_touch_critical_controls_not_tiny(page, label: str) -> None:
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

    await assert_no_failures(page, failures, f"{label}-touch-targets")


async def assert_focused_element_has_visible_ring(page, selector: str, label: str) -> None:
    await page.locator(selector).first.focus()
    failure = await page.evaluate(
        """() => {
            const el = document.activeElement;
            if (!el) return { reason: "no active element" };
            const style = getComputedStyle(el);
            const hasOutline = style.outlineStyle !== "none"
                && style.outlineWidth !== "0px"
                && style.outlineColor !== "rgba(0, 0, 0, 0)";
            const hasShadow = style.boxShadow && style.boxShadow !== "none";
            if (hasOutline || hasShadow) return null;
            return {
                reason: "missing visible focus indicator",
                tag: el.tagName.toLowerCase(),
                className: el.className,
                text: (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 80),
            };
        }"""
    )
    await assert_no_failures(page, [failure] if failure else [], f"{label}-focus-ring")
