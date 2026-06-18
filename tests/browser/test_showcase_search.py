"""Browser gauntlet for showcase command-palette page search."""

from __future__ import annotations

import importlib.util
import socket
import sys
import threading
import time
from pathlib import Path

import pytest

from tests.browser.conftest import wait_for_alpine, wait_for_htmx

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_SHOWCASE_DIR = Path(__file__).resolve().parents[2] / "examples" / "component-showcase"
_SHOWCASE_APP = _SHOWCASE_DIR / "app.py"

_INPUT = "#showcase-command-palette .chirpui-command-palette__input"
_DIALOG = "#showcase-command-palette"
_RESULTS = "#showcase-command-palette-results"


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _load_showcase_app():
    if str(_SHOWCASE_DIR) not in sys.path:
        sys.path.insert(0, str(_SHOWCASE_DIR))
    spec = importlib.util.spec_from_file_location(
        "chirp_ui_component_showcase_search", _SHOWCASE_APP
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

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()


async def _open_palette(page, base_url: str) -> None:
    await page.goto(base_url + "/ui")
    await wait_for_alpine(page)
    await page.keyboard.press("Control+k")
    await page.locator(_DIALOG).wait_for(state="visible", timeout=4000)


async def _palette_activate(page) -> None:
    await page.evaluate(
        "() => {"
        "const dialog = document.getElementById('showcase-command-palette');"
        "const palette = dialog && dialog.parentElement && dialog.parentElement._x_dataStack"
        "  ? dialog.parentElement._x_dataStack[0]"
        "  : null;"
        "if (palette) palette.activate();"
        "}"
    )


async def test_showcase_palette_opens_from_keyboard_shortcut(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await _open_palette(showcase_page, showcase_base_url)
    assert await showcase_page.locator(_INPUT).is_visible()


async def test_showcase_palette_filters_catalog_and_streaming(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await _open_palette(showcase_page, showcase_base_url)

    await showcase_page.locator(_INPUT).fill("catalog")
    await showcase_page.wait_for_function(
        """() => {
            const links = [...document.querySelectorAll('#showcase-command-palette-results a')];
            return links.length === 1 && links[0].getAttribute('href') === '/catalog-shell';
        }""",
        timeout=4000,
    )

    await showcase_page.locator(_INPUT).fill("stream")
    await showcase_page.wait_for_function(
        """() => {
            const links = [...document.querySelectorAll('#showcase-command-palette-results a')];
            return links.some((link) => link.getAttribute('href') === '/streaming');
        }""",
        timeout=4000,
    )


async def test_showcase_palette_navigates_with_boosted_shell_swap(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await _open_palette(showcase_page, showcase_base_url)
    await showcase_page.locator(_INPUT).fill("catalog")
    await showcase_page.wait_for_function(
        """() => document.querySelector('#showcase-command-palette-results a[href=\"/catalog-shell\"]')""",
        timeout=4000,
    )
    await _palette_activate(showcase_page)
    await wait_for_htmx(showcase_page)

    assert showcase_page.url.endswith("/catalog-shell")
    assert await showcase_page.is_visible(".chirpui-app-shell__sidebar")
    assert await showcase_page.is_visible("#page-content")
    assert await showcase_page.locator(".catalog-shell-page").count() > 0


async def test_showcase_palette_closes_on_escape(
    showcase_page,
    showcase_base_url: str,
) -> None:
    await _open_palette(showcase_page, showcase_base_url)
    await showcase_page.keyboard.press("Escape")
    await showcase_page.wait_for_timeout(300)
    assert not await showcase_page.locator(_DIALOG).evaluate("el => el.open")
