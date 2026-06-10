"""Browser a11y proof: search combobox/listbox ARIA + Escape focus return (#163).

The search input declares the combobox contract (``role=combobox``,
``aria-controls``, ``aria-autocomplete=list``) over a ``role=listbox`` of
``role=option`` items. #163 completed the wiring so a screen reader actually
hears the active option:

  * Each option carries a stable id (``search-opt-{n}`` in the modal,
    ``search-page-opt-{n}`` on /search).
  * After ArrowDown, the input's ``aria-activedescendant`` equals the active
    option's id, and that option has ``aria-selected="true"``.
  * On close / clear, ``aria-activedescendant`` is removed.
  * Closing the modal returns focus to the element that opened it (the trigger),
    not ``<body>``.

These assertions are verified on BOTH surfaces: the ⌘K modal (opened via the
nav trigger) and the /search page input.

AUTHORED for the non-required ``browser-smoke`` CI job (``poe
test-browser-chrome`` builds ``site/public/`` first). Mirrors the static-site
server pattern of ``test_bengal_docs_chrome.py`` and the modal-open pattern of
``test_command_palette.py``.
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

DOCS_PAGE = "/docs/theming/chirp-theme/"
SEARCH_PAGE = "/search/"
DESKTOP = {"width": 1280, "height": 900}

# A query that reliably returns results from the built corpus.
QUERY = "theme"


@pytest.fixture(scope="module")
def static_site_url():
    if not (SITE_PUBLIC / "index.html").exists():
        pytest.skip(
            "site/public not built — run `uv run poe docs-build-all` (the "
            "browser-smoke job does this before running tests/browser/)"
        )
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
        pg = await ctx.new_page()
        yield pg
        await ctx.close()
        await browser.close()


async def _wait_for_search(page):
    """Wait until BengalSearch reports the index is loaded."""
    await page.wait_for_function(
        "() => window.BengalSearch && window.BengalSearch.isLoaded()",
        timeout=8000,
    )


# ── Modal (⌘K) ───────────────────────────────────────────────────────


async def test_modal_arrowdown_sets_activedescendant(page, static_site_url):
    """ArrowDown points the modal input at the active option id (#163)."""
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{DOCS_PAGE}")
    await page.wait_for_load_state("networkidle")

    trigger = page.locator("#nav-search-trigger, .nav-search-trigger").first
    await trigger.click()

    modal = page.locator("#search-modal")
    await modal.wait_for(state="visible", timeout=2000)
    await _wait_for_search(page)

    modal_input = page.locator("#search-modal-input")
    await modal_input.fill(QUERY)
    # Results render asynchronously (debounced); wait for at least one option.
    await page.wait_for_selector("#search-modal-results-list [role='option']", timeout=4000)

    # No active option until the user navigates.
    assert await modal_input.get_attribute("aria-activedescendant") is None

    await page.keyboard.press("ArrowDown")

    active_id = await modal_input.get_attribute("aria-activedescendant")
    assert active_id is not None, "modal input has no aria-activedescendant after ArrowDown"
    assert active_id.startswith("search-opt-"), (
        f"modal aria-activedescendant not wired to an option id: {active_id!r}"
    )

    option = page.locator(f"#{active_id}")
    assert await option.get_attribute("role") == "option"
    assert await option.get_attribute("aria-selected") == "true", (
        "active option is not marked aria-selected=true"
    )


async def test_modal_escape_clears_activedescendant_and_returns_focus(page, static_site_url):
    """Escape clears aria-activedescendant and returns focus to the trigger (#163)."""
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{DOCS_PAGE}")
    await page.wait_for_load_state("networkidle")

    trigger = page.locator("#nav-search-trigger, .nav-search-trigger").first
    await trigger.focus()
    await trigger.click()

    modal = page.locator("#search-modal")
    await modal.wait_for(state="visible", timeout=2000)
    await _wait_for_search(page)

    modal_input = page.locator("#search-modal-input")
    await modal_input.fill(QUERY)
    await page.wait_for_selector("#search-modal-results-list [role='option']", timeout=4000)
    await page.keyboard.press("ArrowDown")
    assert await modal_input.get_attribute("aria-activedescendant")

    await page.keyboard.press("Escape")
    await page.wait_for_function(
        "() => !document.getElementById('search-modal').open", timeout=2000
    )

    # Closing clears the active-descendant pointer ...
    assert await modal_input.get_attribute("aria-activedescendant") is None

    # ... and returns focus to the trigger that opened the modal (not <body>).
    focused_id = await page.evaluate("() => document.activeElement?.id")
    trigger_id = await trigger.get_attribute("id")
    assert focused_id == trigger_id, (
        f"focus landed on {focused_id!r}, expected the trigger {trigger_id!r}"
    )


# ── /search page ─────────────────────────────────────────────────────


async def test_search_page_arrowdown_sets_activedescendant(page, static_site_url):
    """ArrowDown points the /search input at the active option id (#163)."""
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{SEARCH_PAGE}")
    await page.wait_for_load_state("networkidle")
    await _wait_for_search(page)

    page_input = page.locator("#search-input")
    await page_input.fill(QUERY)
    await page.wait_for_selector("#search-results-list [role='option']", timeout=4000)

    assert await page_input.get_attribute("aria-activedescendant") is None

    await page.keyboard.press("ArrowDown")

    active_id = await page_input.get_attribute("aria-activedescendant")
    assert active_id is not None, "/search input has no aria-activedescendant after ArrowDown"
    assert active_id.startswith("search-page-opt-"), (
        f"/search aria-activedescendant not wired to an option id: {active_id!r}"
    )

    option = page.locator(f"#{active_id}")
    assert await option.get_attribute("role") == "option"
    assert await option.get_attribute("aria-selected") == "true"


async def test_search_page_escape_clears_activedescendant(page, static_site_url):
    """Escape clears the query and drops aria-activedescendant on /search (#163)."""
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{SEARCH_PAGE}")
    await page.wait_for_load_state("networkidle")
    await _wait_for_search(page)

    page_input = page.locator("#search-input")
    await page_input.fill(QUERY)
    await page.wait_for_selector("#search-results-list [role='option']", timeout=4000)
    await page.keyboard.press("ArrowDown")
    assert await page_input.get_attribute("aria-activedescendant")

    # Escape clears the query on the page input (see onPageKeydown).
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(200)

    assert await page_input.get_attribute("aria-activedescendant") is None
