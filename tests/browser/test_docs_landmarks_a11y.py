"""Browser proof: the docs chrome clears its landmark/role axe violations (#129).

Issue #129 confirmed three axe-core violations on the docs chrome:

  1. ``aria-allowed-role`` — the docs sidebar was
     ``<aside ... role="navigation">``. ``role="navigation"`` is NOT a permitted
     role for ``<aside>`` (whose implicit role is ``complementary``). The fix
     drops the role from every ``<aside>`` and keeps the INNER ``<nav>`` as the
     named navigation landmark.

  2. ``landmark-unique`` — the icon catalog rail and the inner section tree were
     BOTH named "Documentation sections". The rail is renamed to
     "Documentation catalog" so the two navigation landmarks have DISTINCT names.

  3. ``region`` — the reading-progress bar was injected as a direct ``<body>``
     child (outside every landmark) with ``role="progressbar"``. It is now
     decorative (``aria-hidden="true"``, no role/aria-value*), matching the
     chirp-ui ``nav_progress.html`` precedent.

These tests run axe-core (WCAG 2a/2aa/21a/21aa + best-practice) against a real
built docs page and assert ZERO ``landmark-unique`` / ``region`` /
``aria-allowed-role`` violations, plus that the rail and the inner tree expose
DISTINCT accessible names. axe is fetched from the CDN; if unreachable, the
axe-dependent test is skipped and a DOM structural fallback still proves the
distinct-names + decorative-progressbar invariants.
"""

import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.async_api import expect

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

# A docs page whose secondary (inner) tree AND the icon rail both render, so the
# two navigation landmarks coexist on the page (the landmark-unique surface).
DOCS_PAGE = "/docs/theming/chirp-theme/"

# Wide enough that the secondary docs-nav tree is visible (the responsive layout
# hides it below 1280px — see test_bengal_docs_chrome.py / test_docs_nav_labels).
DESKTOP = {"width": 1440, "height": 900}

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"

# The three rules issue #129 must keep at zero on the docs chrome.
TARGET_RULES = ["aria-allowed-role", "landmark-unique", "region"]

# WCAG levels + best-practice, per the issue's verification recipe.
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"]

RAIL_LABEL = "Documentation catalog"
TREE_LABEL = "Documentation sections"


@pytest.fixture(scope="module")
def static_site_url():
    page = SITE_PUBLIC / DOCS_PAGE.strip("/") / "index.html"
    if not page.exists():
        pytest.skip(f"docs site not built: {page} missing (run poe docs-build-all)")
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


@pytest.fixture(scope="module")
def axe_source():
    """Fetch axe-core once; None if the CDN is unreachable in the harness."""
    try:
        with urllib.request.urlopen(AXE_CDN, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError, TimeoutError, OSError:
        return None


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


async def _open_docs(page, static_site_url):
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{DOCS_PAGE}")
    await page.wait_for_load_state("networkidle")
    # Let docs-nav.js run (it names the inner tree landmark) and interactive.js
    # inject the reading-progress bar, then scroll so the bar is non-trivially
    # present in the DOM when axe inspects.
    await page.wait_for_timeout(200)
    await page.evaluate("window.scrollTo(0, 400)")
    await page.wait_for_timeout(100)


async def test_no_landmark_role_violations(page, static_site_url, axe_source):
    """ZERO aria-allowed-role / landmark-unique / region violations on the docs chrome."""
    if axe_source is None:
        pytest.skip("axe-core CDN unreachable; see structural fallbacks below")

    await _open_docs(page, static_site_url)
    await page.evaluate(axe_source)
    result = await page.evaluate(
        """async (cfg) => {
            return await window.axe.run(document, {
                runOnly: { type: 'tag', values: cfg.tags },
            });
        }""",
        {"tags": AXE_TAGS},
    )

    offenders = {
        v["id"]: [node["html"] for node in v["nodes"]]
        for v in result["violations"]
        if v["id"] in TARGET_RULES
    }
    assert offenders == {}, f"docs chrome still trips target axe rules: {offenders}"


async def test_sidebar_aside_is_not_role_navigation(page, static_site_url):
    """The layout <aside> must NOT carry role='navigation' (invalid for <aside>)."""
    await _open_docs(page, static_site_url)
    aside = page.locator("aside#docs-sidebar")
    await expect(aside).to_be_attached()
    assert (await aside.get_attribute("role")) is None, (
        "aside#docs-sidebar still declares an explicit role "
        "(role='navigation' is not permitted on <aside>)"
    )
    # The inner <nav> remains the named navigation landmark.
    inner_nav = aside.locator("nav.chirpui-sidebar")
    await expect(inner_nav).to_be_attached()


async def test_rail_and_tree_have_distinct_names(page, static_site_url):
    """The icon rail and the inner section tree expose DISTINCT accessible names."""
    await _open_docs(page, static_site_url)

    rail = page.locator("nav.chirpui-filter-rail.chirp-theme-doc-catalog-rail")
    tree = page.locator("nav.chirpui-sidebar.chirp-theme-docs-nav")
    await expect(rail).to_be_attached()
    await expect(tree).to_be_attached()

    rail_name = await rail.get_attribute("aria-label")
    tree_name = await tree.get_attribute("aria-label")

    assert rail_name == RAIL_LABEL, f"rail aria-label is {rail_name!r}, expected {RAIL_LABEL!r}"
    assert tree_name == TREE_LABEL, f"tree aria-label is {tree_name!r}, expected {TREE_LABEL!r}"
    assert rail_name != tree_name, (
        f"rail and tree share the accessible name {rail_name!r} (landmark-unique fails)"
    )


async def test_reading_progress_bar_is_decorative(page, static_site_url):
    """The reading-progress bar is decorative: aria-hidden, no role/aria-value*."""
    await _open_docs(page, static_site_url)
    bar = page.locator(".reading-progress")
    if await bar.count() == 0:
        pytest.skip("reading-progress bar not injected on this page")

    await expect(bar.first).to_be_attached()
    attrs = await bar.first.evaluate(
        """el => ({
            ariaHidden: el.getAttribute('aria-hidden'),
            role: el.getAttribute('role'),
            valuemin: el.getAttribute('aria-valuemin'),
            valuemax: el.getAttribute('aria-valuemax'),
            valuenow: el.getAttribute('aria-valuenow'),
            label: el.getAttribute('aria-label'),
        })"""
    )
    assert attrs["ariaHidden"] == "true", f"reading-progress not aria-hidden: {attrs}"
    assert attrs["role"] is None, f"reading-progress still has a role: {attrs}"
    assert attrs["valuemin"] is None, f"reading-progress still has aria-valuemin: {attrs}"
    assert attrs["valuemax"] is None, f"reading-progress still has aria-valuemax: {attrs}"
    assert attrs["valuenow"] is None, f"reading-progress still has aria-valuenow: {attrs}"
    assert attrs["label"] is None, f"reading-progress still has aria-label: {attrs}"
