"""Browser gauntlet for the showcase composer demo (#308).

Proves Enter-to-send appends a right-aligned message bubble via HTMX + Alpine
against the real component-showcase app (same surface manual QA exercised).
"""

from __future__ import annotations

import importlib.util
import socket
import sys
import threading
import time
from pathlib import Path

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_SHOWCASE_DIR = Path(__file__).resolve().parents[2] / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"

FIELD = ".chirpui-composer__field"
THREAD = "#composer-thread"
BUBBLE = f"{THREAD} .chirpui-message-bubble--right"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _load_showcase_app():
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    spec = importlib.util.spec_from_file_location(
        "chirp_ui_component_showcase_composer_browser", _SHOWCASE_APP
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


async def test_composer_enter_to_send_appends_message_bubble(
    showcase_page,
    showcase_base_url: str,
) -> None:
    console_errors: list[str] = []
    showcase_page.on(
        "console",
        lambda msg: console_errors.append(msg.text)
        if msg.type == "error"
        else None,
    )

    await showcase_page.goto(showcase_base_url + "/composer")
    await wait_for_alpine(showcase_page)

    assert await showcase_page.evaluate(
        "() => typeof window.Alpine !== 'undefined'"
        " && typeof Alpine.data === 'function'"
        " && document.querySelector('.chirpui-composer')"
        " && document.querySelector('.chirpui-composer')._x_dataStack"
    ), "Alpine should initialize the composer factory on the showcase page"

    composer_defined = await showcase_page.evaluate(
        """() => {
            const root = document.querySelector('.chirpui-composer');
            if (!root || !root._x_dataStack || !root._x_dataStack[0]) return false;
            return typeof root._x_dataStack[0].onEnter === 'function';
        }"""
    )
    assert composer_defined, "chirpuiComposer factory should be mounted on .chirpui-composer"

    field = showcase_page.locator(FIELD)
    await expect(field).to_be_visible()
    await field.click()
    await field.press_sequentially("hello from gauntlet")
    await field.press("Enter")
    await wait_for_htmx(showcase_page)

    bubble = showcase_page.locator(BUBBLE).filter(has_text="hello from gauntlet")
    await expect(bubble).to_be_visible()
    await expect(showcase_page.locator(THREAD)).to_contain_text("hello from gauntlet")

    alpine_errors = [msg for msg in console_errors if "chirpuiComposer is not defined" in msg]
    assert not alpine_errors, "Composer Alpine factory errors: " + "; ".join(alpine_errors)
