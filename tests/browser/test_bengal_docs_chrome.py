"""Browser proof for packaged Bengal docs chrome."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

pytestmark = pytest.mark.integration

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
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context()
        page = ctx.new_page()
        yield page
        ctx.close()
        browser.close()


def open_app_shell_docs(page, static_site_url: str, width: int, height: int) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{static_site_url}/docs/app-shell/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(100)


def assert_no_document_horizontal_overflow(page, label: str) -> None:
    result = page.evaluate(
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
def test_bengal_docs_chrome_regions_survive_responsive_widths(
    page, static_site_url, width, height
):
    open_app_shell_docs(page, static_site_url, width, height)

    assert_no_document_horizontal_overflow(page, f"bengal-docs-chrome-{width}x{height}")
    assert page.locator(".chirp-theme-docs-layout__main").is_visible()
    assert page.locator(".chirp-theme-docs-layout__article").is_visible()
    assert page.locator("#nav-search-trigger").count() == 1
    assert page.locator(".theme-dropdown__button").count() >= 1
    assert page.locator("#mobile-nav-dialog").count() == 1

    if width <= 768:
        assert page.locator(".chirp-theme-docs-layout__sidebar").is_hidden()
        assert page.locator(".mobile-nav-toggle").is_visible()
    else:
        assert page.locator(".chirp-theme-docs-layout__sidebar").is_visible()

    if width >= 1280:
        assert page.locator(".chirp-theme-docs-layout__toc").is_visible()
        assert page.locator(".toc-sidebar[data-bengal='toc']").is_visible()


def test_bengal_docs_mobile_nav_opens_and_keeps_search_reachable(page, static_site_url):
    open_app_shell_docs(page, static_site_url, 390, 844)

    page.locator(".mobile-nav-toggle").click()
    dialog = page.locator("#mobile-nav-dialog")
    assert dialog.evaluate("el => el.open")
    assert dialog.locator(".mobile-nav-content[role='navigation']").is_visible()
    assert dialog.locator(".mobile-nav-search[data-open-search]").is_visible()
    assert dialog.locator(".theme-dropdown__button").is_visible()

    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    assert not dialog.evaluate("el => el.open")


def test_bengal_docs_theme_controls_use_native_popover(page, static_site_url):
    open_app_shell_docs(page, static_site_url, 1280, 900)

    trigger = page.locator(".site-nav .theme-dropdown__button").first
    menu_id = trigger.get_attribute("popovertarget")
    assert menu_id == "theme-menu-desktop"
    trigger.click()
    assert page.locator("#theme-menu-desktop").is_visible()
    assert page.locator("#theme-menu-desktop .theme-option[data-theme-pack='ember']").count() >= 1
