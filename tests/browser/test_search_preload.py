"""Browser proof: search.js honors the preload modes (#138).

Before #138, search.js ran an unconditional ``setTimeout(loadSearchIndex, 500)``
in its auto-init block, so EVERY page fetched both ``search-index.json``
(~328KB) and ``index.json`` (~75KB) 500ms after load — regardless of the
configured preload mode. That negated the intent-based preload design and made
``lazy`` a no-op.

The fix makes ``initPreload()`` the sole authority:

  * ``smart``    — warm only on hover/focus of a search trigger or on ⌘K.
  * ``lazy``     — never warm proactively; fetch on the first search.
  * ``immediate``— warm once during browser idle time.

These tests serve the built ``site/public/`` and drive each mode by rewriting
the ``bengal:search_preload`` meta tag on the served document (so a single build
can exercise all four behaviors). They count network requests to
``search-index.json`` / ``index.json`` to prove:

  1. ``smart`` + no interaction => ZERO index fetches.
  2. ``lazy``  + no interaction => ZERO index fetches.
  3. hover/focus on the trigger AND ⌘K each warm the index with a single
     ``search-index.json`` fetch BEFORE the modal opens.
  4. ``immediate`` warms once after idle.

This file is AUTHORED to run in the non-required ``browser-smoke`` CI job
(``poe test-browser-chrome`` builds ``site/public/`` first). It mirrors the
static-site-server pattern of ``test_bengal_docs_chrome.py``.
"""

import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

# A built docs page; the search modal is included on every page via base.html,
# so any real page carries the trigger + the preload meta.
DOCS_PAGE = "/docs/theming/chirp-theme/"
DESKTOP = {"width": 1280, "height": 900}

# Requests we treat as "the search index was fetched".
INDEX_REQUEST = re.compile(r"/(search-index|index)\.json(\?|$)")

# Idle warm-up budget for 'immediate' (requestIdleCallback timeout is 2000ms).
IDLE_WARM_MS = 2600


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


async def _route_preload_mode(page, mode: str) -> None:
    """Rewrite the served HTML so bengal:search_preload == *mode*.

    Lets one build exercise every preload mode without a rebuild. Only the main
    document is rewritten; JSON/JS pass through untouched so the network counters
    still see real index fetches.
    """

    async def handler(route):
        request = route.request
        if request.resource_type != "document":
            await route.continue_()
            return
        response = await route.fetch()
        body = await response.text()
        body = re.sub(
            r'(<meta name="bengal:search_preload" content=")[^"]*(")',
            rf"\g<1>{mode}\g<2>",
            body,
            count=1,
        )
        await route.fulfill(response=response, body=body)

    await page.route("**/*", handler)


def _track_index_requests(page) -> list:
    """Record URLs of every search index fetch the page issues."""
    seen: list[str] = []

    def on_request(request):
        if INDEX_REQUEST.search(request.url):
            seen.append(request.url)

    page.on("request", on_request)
    return seen


async def _goto(page, static_site_url: str) -> None:
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{DOCS_PAGE}")
    await page.wait_for_load_state("networkidle")


@pytest.mark.parametrize("mode", ["smart", "lazy"])
async def test_no_interaction_issues_zero_index_fetches(page, static_site_url, mode):
    """'smart'/'lazy' must not fetch the index on a cold, untouched page (#138)."""
    await _route_preload_mode(page, mode)
    seen = _track_index_requests(page)
    await _goto(page, static_site_url)

    # Idle past the OLD dead setTimeout(500) AND the requestIdleCallback budget.
    await page.wait_for_timeout(IDLE_WARM_MS)

    assert seen == [], f"preload mode '{mode}' fetched the search index with no interaction: {seen}"


async def test_smart_warms_on_trigger_hover_before_open(page, static_site_url):
    """Hover/focus on the search trigger warms the index before the modal opens."""
    await _route_preload_mode(page, "smart")
    seen = _track_index_requests(page)
    await _goto(page, static_site_url)
    await page.wait_for_timeout(IDLE_WARM_MS)
    assert seen == [], "smart mode warmed before any interaction"

    trigger = page.locator("#nav-search-trigger, .nav-search-trigger").first
    await trigger.hover()
    await trigger.focus()

    # The index warms (single fetch) while the modal is still closed.
    modal = page.locator("#search-modal")
    assert not await modal.evaluate("el => el.open"), "modal opened on mere hover"

    await page.wait_for_function(
        """() => performance.getEntriesByType('resource')
                  .some(e => /\\/search-index\\.json(\\?|$)/.test(e.name))""",
        timeout=4000,
    )
    index_only = [u for u in seen if "search-index.json" in u]
    assert len(index_only) == 1, f"expected one search-index fetch, got {index_only}"


async def test_smart_warms_on_cmd_k_before_open(page, static_site_url):
    """⌘K warms the index before the modal opens (no first-search delay)."""
    await _route_preload_mode(page, "smart")
    seen = _track_index_requests(page)
    await _goto(page, static_site_url)
    await page.wait_for_timeout(IDLE_WARM_MS)
    assert seen == [], "smart mode warmed before any interaction"

    # Cmd/Ctrl keydown alone should trigger the smart preload (see
    # setupSmartPreload's metaKey/ctrlKey listener).
    await page.keyboard.down("Control")
    await page.wait_for_function(
        """() => performance.getEntriesByType('resource')
                  .some(e => /\\/search-index\\.json(\\?|$)/.test(e.name))""",
        timeout=4000,
    )
    await page.keyboard.up("Control")

    index_only = [u for u in seen if "search-index.json" in u]
    assert len(index_only) == 1, f"expected one search-index fetch, got {index_only}"


async def test_immediate_warms_once_after_idle(page, static_site_url):
    """'immediate' warms the index during idle time, without interaction (#138)."""
    await _route_preload_mode(page, "immediate")
    seen = _track_index_requests(page)
    await _goto(page, static_site_url)

    await page.wait_for_function(
        """() => performance.getEntriesByType('resource')
                  .some(e => /\\/search-index\\.json(\\?|$)/.test(e.name))""",
        timeout=4000,
    )
    # Settle, then assert the index warmed exactly once (idempotent preload).
    await page.wait_for_timeout(500)
    index_only = [u for u in seen if "search-index.json" in u]
    assert len(index_only) == 1, f"immediate should warm once, got {index_only}"
