"""Browser proof for the filesystem-routed app chrome fixture."""

import socket
import threading
import time

import pytest
from playwright.async_api import expect

from tests.browser.conftest import wait_for_alpine, wait_for_htmx
from tests.browser.gauntlet_detectors import assert_no_document_horizontal_overflow
from tests.fixtures.filesystem_chrome.app import create_app

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def filesystem_base_url():
    from pounce import ServerConfig
    from pounce.server import Server

    port = _find_free_port()
    app = create_app()
    server = Server(
        ServerConfig(
            host="127.0.0.1",
            port=port,
            log_level="warning",
            access_log=False,
        ),
        app,
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        raise RuntimeError(f"Filesystem fixture server did not start on port {port}")

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)


async def open_workspace(page, filesystem_base_url: str, width: int = 1024, height: int = 768):
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(filesystem_base_url + "/workspace")
    await wait_for_alpine(page)
    await page.wait_for_timeout(100)


async def test_filesystem_chrome_shell_navigation_and_oob_actions(page, filesystem_base_url):
    await open_workspace(page, filesystem_base_url)

    await assert_no_document_horizontal_overflow(page, "filesystem-workspace")
    shell_actions = page.locator("#chirp-shell-actions")
    await expect(page.get_by_role("link", name="Filesystem Chrome")).to_be_visible()
    await expect(page.get_by_title("Workspace")).to_have_attribute("aria-current", "page")
    await expect(shell_actions).to_contain_text("New workspace run")
    await expect(page.locator("#page-content")).to_have_count(1)

    await page.get_by_title("Admin").click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(filesystem_base_url + "/admin")
    await expect(page.get_by_test_id("fs-admin-view-title")).to_have_text("Admin access")
    await expect(shell_actions).to_contain_text("Invite admin")
    await expect(shell_actions).not_to_contain_text("New workspace run")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)


async def test_filesystem_chrome_route_tabs_swap_page_root(page, filesystem_base_url):
    await open_workspace(page, filesystem_base_url)

    await page.get_by_role("link", name="Runs").click()
    await wait_for_htmx(page)

    await expect(page).to_have_url(filesystem_base_url + "/workspace/runs")
    await expect(page.get_by_test_id("fs-workspace-view-title")).to_have_text("Workspace runs")
    await expect(page.locator("#chirp-shell-actions")).to_contain_text("New workspace run")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)


async def test_filesystem_chrome_command_trigger_focuses_palette(page, filesystem_base_url):
    await open_workspace(page, filesystem_base_url, width=390, height=844)

    await page.get_by_role("button", name="Search workspace").click()

    palette = page.locator("#fs-workspace-palette")
    await palette.wait_for(state="visible", timeout=2000)
    assert await palette.evaluate("el => el.open")
    assert await page.evaluate(
        "() => document.activeElement?.closest('#fs-workspace-palette') !== null"
    )


async def test_filesystem_chrome_local_fragment_swap(page, filesystem_base_url):
    await open_workspace(page, filesystem_base_url)

    await page.get_by_role("button", name="Filter").click()
    await wait_for_htmx(page)

    await expect(page.get_by_test_id("fs-filter-result")).to_be_visible()
    await expect(page.get_by_test_id("fs-workspace-heading")).to_have_text("Filesystem workspace")
    await expect(page.locator("#main")).to_have_count(1)
    await expect(page.locator("#page-content")).to_have_count(1)
    await expect(page.locator("#page-root")).to_have_count(1)
    await expect(page.locator("#page-content-inner")).to_have_count(1)
