"""Browser proof for the first visual taste-floor golden screens."""

import importlib.util
import socket
import sys
import threading
import time
from pathlib import Path

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_SHOWCASE_DIR = Path(__file__).resolve().parents[2] / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"


def _px(value: str) -> float:
    return float(value.replace("px", ""))


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _load_showcase_app():
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    spec = importlib.util.spec_from_file_location(
        "chirp_ui_golden_screen_showcase_browser", _SHOWCASE_APP
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


@pytest.fixture(scope="session")
def showcase_base_url():
    from pounce import ServerConfig
    from pounce.server import Server

    port = _find_free_port()
    app = _load_showcase_app()
    config = ServerConfig(
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    server = Server(config, app)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Showcase server did not start on port {port}")

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
async def showcase_page():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        yield page
        await ctx.close()
        await browser.close()


@pytest.mark.parametrize(
    ("path", "surface", "profile", "required_text"),
    [
        (
            "/screen-command-center?q=queues&area=compute&status=warning",
            "#operations-shell-surface",
            "atlas",
            "Golden screen: Command Center",
        ),
        (
            "/screen-review-queue?q=latency&queue=priority&status=danger",
            "#support-shell-surface",
            "sage",
            "Golden screen: Review Queue",
        ),
        (
            "/screen-agent-run-monitor",
            "#agent-run-monitor-surface",
            "signal",
            "Golden screen: Agent Run Monitor",
        ),
        (
            "/screen-product-docs-home",
            "#product-docs-home-surface",
            "ember",
            "Signal Loom",
        ),
    ],
)
@pytest.mark.parametrize(
    ("width", "height"),
    [(320, 640), (390, 844), (768, 1024), (1280, 900)],
)
async def test_golden_screen_fixtures_have_no_document_horizontal_overflow(
    showcase_page,
    showcase_base_url: str,
    path: str,
    surface: str,
    profile: str,
    required_text: str,
    width: int,
    height: int,
) -> None:
    await showcase_page.set_viewport_size({"width": width, "height": height})
    await showcase_page.goto(showcase_base_url + path)
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(surface)).to_have_attribute("data-screen-profile", profile)
    await expect(showcase_page.locator("body")).to_contain_text(required_text)
    await assert_no_document_horizontal_overflow(
        showcase_page, f"golden-screen-{profile}-{width}x{height}"
    )


async def test_review_queue_golden_screen_uses_workspace_primitives(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1024, "height": 768})
    await showcase_page.goto(
        showcase_base_url + "/screen-review-queue?q=latency&queue=priority&status=danger"
    )
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-workspace-shell")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-filter-rail")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-result-collection")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-inspector-panel")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-result-card")).not_to_have_count(0)


async def test_command_center_golden_screen_keeps_inspector_visible(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(
        showcase_base_url + "/screen-command-center?q=queues&area=compute&status=warning"
    )
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".ops-shell-workspace")).to_have_count(1)
    await expect(showcase_page.locator(".ops-shell-inspector")).to_be_visible()
    await expect(showcase_page.locator(".ops-shell-workload-card")).not_to_have_count(0)


async def test_agent_run_monitor_golden_screen_uses_state_and_artifact_surfaces(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(showcase_base_url + "/screen-agent-run-monitor")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-timeline")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-streaming-block")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-result-collection")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-inspector-panel")).to_have_count(1)


async def test_product_docs_home_golden_screen_uses_product_pattern_surfaces(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(showcase_base_url + "/screen-product-docs-home")
    await wait_for_alpine(showcase_page)

    await expect(showcase_page.locator(".chirpui-site-header")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-hero--page")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-logo-cloud")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-lifecycle-showcase")).to_have_count(1)
    await expect(showcase_page.locator(".chirpui-cta-band")).to_have_count(1)


@pytest.mark.parametrize(
    ("path", "surface", "profile", "archetype"),
    [
        (
            "/screen-command-center?q=queues&area=compute&status=warning",
            "#operations-shell-surface",
            "atlas",
            "command-center",
        ),
        (
            "/screen-review-queue?q=latency&queue=priority&status=danger",
            "#support-shell-surface",
            "sage",
            "review-queue",
        ),
        (
            "/screen-agent-run-monitor",
            "#agent-run-monitor-surface",
            "signal",
            "agent-run-monitor",
        ),
        (
            "/screen-product-docs-home",
            "#product-docs-home-surface",
            "ember",
            "product-docs-home",
        ),
    ],
)
async def test_golden_screens_expose_screen_level_taste_signals(
    showcase_page,
    showcase_base_url: str,
    path: str,
    surface: str,
    profile: str,
    archetype: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(showcase_base_url + path)
    await wait_for_alpine(showcase_page)
    await assert_no_document_horizontal_overflow(
        showcase_page, f"golden-screen-taste-signals-{archetype}"
    )

    signals = await showcase_page.locator(surface).evaluate(
        """root => {
            const visible = el => {
                const style = getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return style.visibility !== "hidden" && style.display !== "none" &&
                    rect.width > 0 && rect.height > 0;
            };
            const h1 = Array.from(document.querySelectorAll("h1")).find(visible);
            const regionHeading = Array.from(root.querySelectorAll(
                "h2, h3, .chirpui-panel__title, .chirpui-card__title, " +
                ".chirpui-result-collection__title, .chirpui-inspector-panel__title"
            )).find(visible);
            const tasteSignals = Array.from(root.querySelectorAll(
                ".chirpui-badge, .chirpui-sse-status, [role='status'], " +
                ".chirpui-metric-card, .chirpui-logo-cloud, " +
                ".chirpui-lifecycle-showcase, .chirpui-cta-band"
            )).filter(visible);
            const controls = Array.from(root.querySelectorAll(
                "a[href], button, input, select"
            )).filter(visible);
            return {
                archetype: root.dataset.screenArchetype,
                profile: root.dataset.screenProfile,
                h1Size: h1 ? getComputedStyle(h1).fontSize : "0px",
                regionHeadingSize: regionHeading ?
                    getComputedStyle(regionHeading).fontSize : "0px",
                tasteSignalCount: tasteSignals.length,
                controlCount: controls.length
            };
        }"""
    )

    assert signals["archetype"] == archetype
    assert signals["profile"] == profile
    assert _px(signals["h1Size"]) > 0
    assert _px(signals["regionHeadingSize"]) > 0
    assert _px(signals["h1Size"]) != _px(signals["regionHeadingSize"])
    assert signals["tasteSignalCount"] >= 2
    assert signals["controlCount"] >= 2


async def test_golden_screen_typography_roles_have_browser_proof(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(
        showcase_base_url + "/screen-review-queue?q=latency&queue=priority&status=danger"
    )
    await wait_for_alpine(showcase_page)
    await assert_no_document_horizontal_overflow(
        showcase_page, "golden-screen-review-queue-typography"
    )

    review_styles = await showcase_page.locator(".chirpui-result-card__title").first.evaluate(
        """el => {
            const title = getComputedStyle(el);
            const body = getComputedStyle(document.querySelector(".chirpui-result-card__body"));
            const metric = getComputedStyle(document.querySelector(".chirpui-metric-strip__value"));
            return {
                titleWeight: title.fontWeight,
                bodySize: body.fontSize,
                bodyLineHeight: body.lineHeight,
                metricVariant: metric.fontVariantNumeric
            };
        }"""
    )
    assert int(review_styles["titleWeight"]) >= 600
    assert _px(review_styles["bodyLineHeight"]) > _px(review_styles["bodySize"])
    assert "tabular-nums" in review_styles["metricVariant"]

    await showcase_page.set_viewport_size({"width": 320, "height": 640})
    await showcase_page.goto(showcase_base_url + "/screen-product-docs-home")
    await wait_for_alpine(showcase_page)
    await assert_no_document_horizontal_overflow(
        showcase_page, "golden-screen-product-docs-home-typography"
    )

    product_styles = await showcase_page.locator(
        ".chirpui-hero--page .chirpui-hero__title"
    ).evaluate(
        """el => {
            const title = getComputedStyle(el);
            const subtitleEl = document.querySelector(".chirpui-hero--page .chirpui-hero__subtitle");
            const subtitle = getComputedStyle(subtitleEl);
            const titleRect = el.getBoundingClientRect();
            const subtitleRect = subtitleEl.getBoundingClientRect();
            return {
                titleSize: title.fontSize,
                titleWidth: titleRect.width,
                subtitleSize: subtitle.fontSize,
                subtitleLineHeight: subtitle.lineHeight,
                subtitleWidth: subtitleRect.width,
                viewportWidth: window.innerWidth
            };
        }"""
    )
    assert _px(product_styles["titleSize"]) > _px(product_styles["subtitleSize"])
    assert _px(product_styles["subtitleLineHeight"]) > _px(product_styles["subtitleSize"])
    assert product_styles["titleWidth"] <= product_styles["viewportWidth"]
    assert product_styles["subtitleWidth"] <= product_styles["viewportWidth"]

    await showcase_page.set_viewport_size({"width": 390, "height": 844})
    await showcase_page.goto(showcase_base_url + "/screen-agent-run-monitor")
    await wait_for_alpine(showcase_page)
    await assert_no_document_horizontal_overflow(
        showcase_page, "golden-screen-agent-run-monitor-typography"
    )

    log_styles = await showcase_page.locator(
        "#agent-run-monitor-log .chirpui-streaming-block"
    ).evaluate(
        """el => {
            const style = getComputedStyle(el);
            return { fontSize: style.fontSize, lineHeight: style.lineHeight };
        }"""
    )
    assert _px(log_styles["lineHeight"]) > _px(log_styles["fontSize"])


async def test_component_taste_defaults_render_in_golden_screens(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(
        showcase_base_url + "/screen-command-center?q=queues&area=compute&status=warning"
    )
    await wait_for_alpine(showcase_page)

    card_styles = await showcase_page.locator(".ops-shell-workload-card").first.evaluate(
        """el => {
            const title = getComputedStyle(el.querySelector(".chirpui-card__title"));
            const body = getComputedStyle(el.querySelector(".chirpui-card__body"));
            const footer = getComputedStyle(
                el.querySelector(".chirpui-card__footer, .chirpui-card__footer-wrap")
            );
            const hints = getComputedStyle(document.querySelector(".ops-shell-hints"));
            return {
                titleWeight: title.fontWeight,
                titleLineHeight: title.lineHeight,
                bodySize: body.fontSize,
                bodyLineHeight: body.lineHeight,
                footerNumeric: footer.fontVariantNumeric,
                footerLineHeight: footer.lineHeight,
                hintsLineHeight: hints.lineHeight
            };
        }"""
    )
    assert int(card_styles["titleWeight"]) >= 600
    assert _px(card_styles["titleLineHeight"]) > 0
    assert _px(card_styles["bodyLineHeight"]) > _px(card_styles["bodySize"])
    assert "tabular-nums" in card_styles["footerNumeric"]
    assert _px(card_styles["footerLineHeight"]) > 0
    assert _px(card_styles["hintsLineHeight"]) > 0

    await showcase_page.goto(showcase_base_url + "/screen-agent-run-monitor")
    await wait_for_alpine(showcase_page)

    timeline_styles = await showcase_page.locator(".chirpui-timeline__content").first.evaluate(
        """el => {
            const title = getComputedStyle(el.querySelector(".chirpui-timeline__title"));
            const date = getComputedStyle(el.querySelector(".chirpui-timeline__date"));
            const body = getComputedStyle(el.querySelector(".chirpui-timeline__body"));
            const sse = getComputedStyle(document.querySelector(".chirpui-sse-status"));
            return {
                titleWeight: title.fontWeight,
                dateNumeric: date.fontVariantNumeric,
                bodySize: body.fontSize,
                bodyLineHeight: body.lineHeight,
                sseWeight: sse.fontWeight,
                sseLineHeight: sse.lineHeight
            };
        }"""
    )
    assert int(timeline_styles["titleWeight"]) >= 600
    assert "tabular-nums" in timeline_styles["dateNumeric"]
    assert _px(timeline_styles["bodyLineHeight"]) > _px(timeline_styles["bodySize"])
    assert int(timeline_styles["sseWeight"]) >= 500
    assert _px(timeline_styles["sseLineHeight"]) > 0

    await showcase_page.goto(
        showcase_base_url + "/screen-review-queue?q=no-matching-ticket&queue=priority"
    )
    await wait_for_alpine(showcase_page)

    empty_styles = await showcase_page.locator(".chirpui-empty-state").evaluate(
        """el => {
            const title = getComputedStyle(el.querySelector(".chirpui-empty-state__title"));
            const body = getComputedStyle(el.querySelector(".chirpui-empty-state__body"));
            const bodyRect = el.querySelector(".chirpui-empty-state__body").getBoundingClientRect();
            return {
                titleSize: title.fontSize,
                titleLineHeight: title.lineHeight,
                bodySize: body.fontSize,
                bodyLineHeight: body.lineHeight,
                bodyWidth: bodyRect.width,
                viewportWidth: window.innerWidth
            };
        }"""
    )
    assert _px(empty_styles["titleLineHeight"]) > 0
    assert _px(empty_styles["bodyLineHeight"]) > _px(empty_styles["bodySize"])
    assert empty_styles["bodyWidth"] <= empty_styles["viewportWidth"]


async def test_second_sweep_component_defaults_render_in_golden_screens(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await showcase_page.set_viewport_size({"width": 1280, "height": 900})
    await showcase_page.goto(showcase_base_url + "/screen-agent-run-monitor")
    await wait_for_alpine(showcase_page)

    panel_styles = await showcase_page.locator(".chirpui-panel").first.evaluate(
        """el => {
            const title = getComputedStyle(el.querySelector(".chirpui-panel__title"));
            const body = getComputedStyle(el.querySelector(".chirpui-panel__body"));
            const progressLabel = getComputedStyle(
                document.querySelector(".chirpui-progress-bar__label")
            );
            return {
                titleWeight: title.fontWeight,
                titleLineHeight: title.lineHeight,
                bodySize: body.fontSize,
                bodyLineHeight: body.lineHeight,
                progressWeight: progressLabel.fontWeight,
                progressNumeric: progressLabel.fontVariantNumeric,
                progressLineHeight: progressLabel.lineHeight
            };
        }"""
    )

    assert int(panel_styles["titleWeight"]) >= 600
    assert _px(panel_styles["titleLineHeight"]) > 0
    assert _px(panel_styles["bodyLineHeight"]) > _px(panel_styles["bodySize"])
    assert int(panel_styles["progressWeight"]) >= 500
    assert "tabular-nums" in panel_styles["progressNumeric"]
    assert _px(panel_styles["progressLineHeight"]) > 0
