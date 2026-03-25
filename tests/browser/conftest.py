"""Playwright fixtures for chirp-ui browser tests.

Starts a real Chirp app on a random port for the test session,
provides a fresh Playwright page per test.
"""

from __future__ import annotations

import socket
import threading
import time

import pytest


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def app_port():
    """Start the test Chirp app on a random port for the session."""
    from pounce import ServerConfig
    from pounce.server import Server

    from tests.browser.app import create_app

    port = _find_free_port()
    app = create_app()

    config = ServerConfig(
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False,
    )
    server = Server(config, app)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to be ready
    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Test server did not start on port {port}")

    yield port

    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture(scope="session")
def base_url(app_port):
    return f"http://127.0.0.1:{app_port}"


@pytest.fixture
async def page(base_url):
    """Fresh Playwright page per test."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        page._base_url = base_url  # convenience for tests
        yield page
        await ctx.close()
        await browser.close()


# ── Helpers ──────────────────────────────────────────────────────────


async def wait_for_htmx(page, timeout: float = 5000):
    """Wait for all pending htmx requests to complete."""
    # Give htmx a moment to start the request (adds .htmx-request class)
    await page.wait_for_timeout(100)
    # Then wait for it to finish
    await page.wait_for_function(
        "() => !document.querySelector('.htmx-request')",
        timeout=timeout,
    )
    # Wait for settle (Alpine re-init, class toggles)
    await page.wait_for_timeout(100)


async def wait_for_alpine(page, timeout: float = 5000):
    """Wait for Alpine.js to be initialized."""
    await page.wait_for_function(
        "() => window.Alpine && Alpine.version",
        timeout=timeout,
    )
