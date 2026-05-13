"""Browser proof for packaged Bengal docs chrome."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.async_api import expect

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

VIEWPORTS = [
    pytest.param(390, 844, id="phone"),
    pytest.param(768, 1024, id="tablet"),
    pytest.param(1024, 768, id="tablet-wide"),
    pytest.param(1280, 900, id="desktop"),
]


@pytest.fixture(scope="module")
def static_site_url():
    handler = partial(SimpleHTTPRequestHandler, directory=str(SITE_PUBLIC))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture
async def page():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        yield page
        await ctx.close()
        await browser.close()


async def open_app_shell_docs(page, static_site_url: str, width: int, height: int) -> None:
    await page.set_viewport_size({"width": width, "height": height})
    await page.goto(f"{static_site_url}/docs/app-shell/")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)


async def assert_no_document_horizontal_overflow(page, label: str) -> None:
    result = await page.evaluate(
        """() => {
            const root = document.documentElement;
            return {
                overflow: Math.ceil(root.scrollWidth - root.clientWidth),
                scrollWidth: root.scrollWidth,
                clientWidth: root.clientWidth,
            };
        }"""
    )
    assert result["overflow"] <= 1, {label: result}


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
async def test_bengal_docs_chrome_regions_survive_responsive_widths(
    page, static_site_url, width, height
):
    await open_app_shell_docs(page, static_site_url, width, height)

    await assert_no_document_horizontal_overflow(page, f"bengal-docs-chrome-{width}x{height}")
    await expect(page.locator(".chirp-theme-docs-layout__main")).to_be_visible()
    await expect(page.locator(".chirp-theme-docs-layout__article")).to_be_visible()
    assert await page.locator("#nav-search-trigger").count() == 1
    assert await page.locator(".theme-dropdown__button").count() >= 1
    assert await page.locator("#mobile-nav-dialog").count() == 1

    if width <= 768:
        await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_hidden()
        await expect(page.locator(".mobile-nav-toggle")).to_be_visible()
    else:
        await expect(page.locator(".chirp-theme-docs-layout__sidebar")).to_be_visible()

    if width >= 1280:
        await expect(page.locator(".chirp-theme-docs-layout__toc")).to_be_visible()
        await expect(page.locator(".toc-sidebar[data-bengal='toc']")).to_be_visible()


async def test_bengal_docs_mobile_nav_opens_and_keeps_search_reachable(page, static_site_url):
    await open_app_shell_docs(page, static_site_url, 390, 844)

    await page.locator(".mobile-nav-toggle").click()
    dialog = page.locator("#mobile-nav-dialog")
    assert await dialog.evaluate("el => el.open")
    await expect(dialog.locator(".mobile-nav-content[role='navigation']")).to_be_visible()
    await expect(dialog.locator(".mobile-nav-search[data-open-search]")).to_be_visible()
    await expect(dialog.locator(".theme-dropdown__button")).to_be_visible()

    await page.keyboard.press("Escape")
    await page.wait_for_timeout(100)
    assert not await dialog.evaluate("el => el.open")


async def test_bengal_docs_theme_controls_use_native_popover(page, static_site_url):
    await open_app_shell_docs(page, static_site_url, 1280, 900)

    trigger = page.locator(".theme-dropdown__button[popovertarget='theme-menu-desktop']")
    menu_id = await trigger.get_attribute("popovertarget")
    assert menu_id == "theme-menu-desktop"
    await trigger.click()
    await expect(page.locator("#theme-menu-desktop")).to_be_visible()
    assert await page.locator("#theme-menu-desktop .theme-option[data-theme-pack='ember']").count() >= 1
