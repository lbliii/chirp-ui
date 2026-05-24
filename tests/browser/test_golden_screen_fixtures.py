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
