"""Regression proof: docs-nav disclosure is a11y-clean AND visually unchanged.

The docs sidebar renders each collapsible section as an ALWAYS-VISIBLE header
row (`__section-header`) holding two SIBLINGS — a folder <button> (`__toggle`,
the disclosure control) and the navigable section <a> (`__summary-link`).
Neither nests inside the other, so axe-core's `nested-interactive` rule passes
(a link inside a <summary>'s implicit button role used to trip it — 6 SERIOUS
instances). The section label stays painted whether the section is collapsed
or open because it lives in the always-visible header row.

The folder is the disclosure glyph: a closed folder when collapsed, an open
folder when expanded, swapped off the button's `aria-expanded` state in CSS —
NO caret. Clicking the folder toggles the section open/closed via JS with NO
navigation; clicking the label navigates. The active branch arrives expanded
(server-seeded aria-expanded="true").

These tests assert: (a) `nested-interactive` is GONE (axe-core, with a
structural fallback if the CDN is unreachable); (b) the toggle is a <button>
that is NOT nested in the link and does not nest the link; (c) clicking the
toggle flips aria-expanded + shows/hides children WITHOUT changing the URL;
(d) a collapsed section shows the closed folder, an expanded one the open
folder; (e) section labels are always visible; (f) there is no caret.
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

# A docs page whose secondary (inner "DOCUMENTATION") tree is rendered and
# whose sidebar contains several collapsible sections.
DOCS_PAGE = "/docs/theming/chirp-theme/"

# Wide enough that the secondary docs-nav tree is visible (the responsive
# layout hides it below 1280px — see test_bengal_docs_chrome.py).
DESKTOP = {"width": 1440, "height": 900}

AXE_CDN = "https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js"


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
    # Let docs-nav.js run (landmark label + toggle wiring + active-trail).
    await page.wait_for_timeout(150)


def _section(page, *, collapsed: bool):
    """Locate a `--has-toggle` section in the secondary tree in the wanted state."""
    state = '[aria-expanded="false"]' if collapsed else '[aria-expanded="true"]'
    return page.locator(
        ".chirp-theme-doc-catalog__secondary "
        f".chirp-theme-docs-nav__section--has-toggle:has(> .chirp-theme-docs-nav__section-header > "
        f".chirp-theme-docs-nav__toggle{state})"
    )


async def test_secondary_tree_has_collapsible_sections(page, static_site_url):
    """Sanity: the page actually exercises the folder-button disclosure."""
    await _open_docs(page, static_site_url)
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    sections = page.locator(
        ".chirp-theme-doc-catalog__secondary .chirp-theme-docs-nav__section--has-toggle"
    )
    assert await sections.count() >= 1, "no collapsible docs-nav sections rendered"


async def test_no_nested_interactive(page, static_site_url, axe_source):
    """The docs-nav must NOT report axe-core `nested-interactive` (was 6 SERIOUS).

    Uses axe-core when reachable; otherwise falls back to a DOM structural
    assertion that no <a>/<button>/<summary> is a descendant of another.
    """
    await _open_docs(page, static_site_url)

    if axe_source is not None:
        await page.evaluate(axe_source)
        result = await page.evaluate(
            """async () => {
                return await window.axe.run('.chirp-theme-docs-nav', {
                    runOnly: ['nested-interactive'],
                });
            }"""
        )
        violations = result["violations"]
        assert violations == [], f"axe-core reported nested-interactive in docs-nav: {violations}"
        return

    # Structural fallback: no interactive control nests another.
    nested = await page.evaluate(
        """() => {
            const nav = document.querySelector('.chirp-theme-docs-nav');
            if (!nav) return -1;
            const controls = nav.querySelectorAll('a, button, summary');
            let bad = 0;
            controls.forEach((el) => {
                if (el.parentElement && el.parentElement.closest('a, button, summary')) {
                    bad += 1;
                }
            });
            return bad;
        }"""
    )
    assert nested == 0, f"{nested} interactive control(s) nested inside another in docs-nav"


async def test_toggle_is_a_button_sibling_of_the_link(page, static_site_url):
    """The folder toggle is a <button>; it is NOT nested in the link, nor it in the toggle."""
    await _open_docs(page, static_site_url)
    secondary = page.locator(".chirp-theme-doc-catalog__secondary")

    toggle = secondary.locator(".chirp-theme-docs-nav__toggle").first
    await expect(toggle).to_be_attached()
    assert (await toggle.evaluate("el => el.tagName")) == "BUTTON"
    assert (await toggle.get_attribute("type")) == "button"

    # Neither control is a descendant of the other.
    relationship = await toggle.evaluate(
        """el => {
            const header = el.closest('.chirp-theme-docs-nav__section-header');
            const link = header.querySelector('.chirp-theme-docs-nav__summary-link');
            return {
                hasLink: !!link,
                linkInToggle: !!el.querySelector('a'),
                toggleInLink: link ? !!link.querySelector('button') : false,
                siblings: link ? (link.parentElement === el.parentElement) : false,
            };
        }"""
    )
    assert relationship["hasLink"], "no summary-link beside the toggle"
    assert not relationship["linkInToggle"], "link is nested inside the toggle button"
    assert not relationship["toggleInLink"], "toggle button is nested inside the link"
    assert relationship["siblings"], "toggle and link are not siblings in the header row"


async def test_no_caret_in_section_headers(page, static_site_url):
    """No caret/chevron control (owner's no-caret choice); folder glyphs only."""
    await _open_docs(page, static_site_url)
    secondary = page.locator(".chirp-theme-doc-catalog__secondary")
    # The #162-era chevron must not be present.
    assert await secondary.locator(".chirp-theme-docs-nav__toggle-icon").count() == 0, (
        "found a caret/chevron toggle-icon — should be folder glyphs only"
    )
    carets = await secondary.evaluate("""el => el.innerHTML.match(/icon-caret/g)?.length || 0""")
    assert carets == 0, f"found {carets} caret icon(s) in docs-nav"
    # No native <details>/<summary> disclosure survives.
    assert await secondary.locator("details.chirp-theme-docs-nav__section").count() == 0
    assert await secondary.locator("summary.chirp-theme-docs-nav__summary").count() == 0


async def test_section_labels_always_visible(page, static_site_url):
    """Every section label is painted, collapsed or expanded (header row is visible)."""
    await _open_docs(page, static_site_url)
    labels = page.locator(
        ".chirp-theme-doc-catalog__secondary "
        ".chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__label"
    )
    count = await labels.count()
    assert count >= 1, "no section labels rendered"
    for i in range(count):
        label = labels.nth(i)
        await expect(label).to_be_visible()
        paint = await label.evaluate(
            """el => {
                const rect = el.getBoundingClientRect();
                let node = el, hidden = false;
                while (node && node !== document.body) {
                    if (getComputedStyle(node).contentVisibility === 'hidden') { hidden = true; break; }
                    node = node.parentElement;
                }
                return { w: Math.round(rect.width), h: Math.round(rect.height), hidden };
            }"""
        )
        assert paint["w"] > 0, (i, paint)
        assert paint["h"] > 0, (i, paint)
        assert not paint["hidden"], (i, paint)


async def test_collapsed_section_shows_closed_folder(page, static_site_url):
    """A COLLAPSED section paints the closed folder; the open folder is hidden."""
    await _open_docs(page, static_site_url)

    collapsed = _section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    section = collapsed.first
    closed = section.locator(
        "> .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--closed"
    )
    opened = section.locator(
        "> .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--open"
    )

    await expect(closed).to_be_visible()
    await expect(opened).to_be_hidden()


async def test_expanded_section_shows_open_folder(page, static_site_url):
    """An EXPANDED section paints the open folder; the closed folder is hidden."""
    await _open_docs(page, static_site_url)

    expanded = _section(page, collapsed=False)
    if await expanded.count() == 0:
        pytest.skip("no expanded sections rendered")

    section = expanded.first
    closed = section.locator(
        "> .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--closed"
    )
    opened = section.locator(
        "> .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--open"
    )

    await expect(opened).to_be_visible()
    await expect(closed).to_be_hidden()


async def test_clicking_folder_toggles_without_navigation(page, static_site_url):
    """Clicking the folder button flips aria-expanded + shows/hides children — NO nav.

    The folder is a real <button>, so a click toggles the section via JS and
    never changes the URL. The closed/open folder swap follows aria-expanded.
    """
    await _open_docs(page, static_site_url)

    collapsed = _section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    section = await collapsed.first.element_handle()
    assert section is not None
    toggle = await section.query_selector(
        ":scope > .chirp-theme-docs-nav__section-header > .chirp-theme-docs-nav__toggle"
    )
    panel = await section.query_selector(":scope > .chirp-theme-docs-nav__section-links")
    closed = await section.query_selector(
        ":scope > .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--closed"
    )
    opened = await section.query_selector(
        ":scope > .chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__folder--open"
    )
    assert toggle is not None
    assert panel is not None
    assert closed is not None
    assert opened is not None

    url_before = page.url

    # Collapsed: aria-expanded false, children hidden, closed folder shown.
    assert await toggle.get_attribute("aria-expanded") == "false"
    assert not await panel.is_visible()
    assert await closed.is_visible()
    assert not await opened.is_visible()

    # Click → expands, children show, glyph swaps to open, NO navigation.
    await toggle.click()
    assert await toggle.get_attribute("aria-expanded") == "true"
    assert await panel.is_visible()
    assert await opened.is_visible()
    assert not await closed.is_visible()
    assert page.url == url_before, "clicking the folder toggle navigated"

    # Click again → collapses, children hide, glyph swaps back, still no nav.
    await toggle.click()
    assert await toggle.get_attribute("aria-expanded") == "false"
    assert not await panel.is_visible()
    assert await closed.is_visible()
    assert not await opened.is_visible()
    assert page.url == url_before, "clicking the folder toggle navigated"


async def test_clicking_label_navigates(page, static_site_url):
    """Clicking the section LABEL link navigates to that section's index page."""
    await _open_docs(page, static_site_url)

    link = page.locator(
        ".chirp-theme-doc-catalog__secondary "
        ".chirp-theme-docs-nav__section-header "
        ".chirp-theme-docs-nav__summary-link[href]"
    ).first
    await expect(link).to_be_visible()
    href = await link.get_attribute("href")
    assert href, "section link has no href"

    await link.click()
    await page.wait_for_load_state("networkidle")
    assert href in page.url, f"label click did not navigate to {href} (now {page.url})"


async def test_active_branch_is_expanded_with_aria_current(page, static_site_url):
    """The active section arrives expanded (server-seeded) and the page is aria-current."""
    await _open_docs(page, static_site_url)

    current = page.locator('.chirp-theme-doc-catalog__secondary [aria-current="page"]')
    assert await current.count() >= 1, "no aria-current marker in the docs tree"

    # Every section ancestor of the current page must have its toggle expanded.
    all_open = await current.first.evaluate(
        """el => {
            let node = el.closest('.chirp-theme-docs-nav__section--has-toggle');
            while (node) {
                const toggle = node.querySelector(
                    ':scope > .chirp-theme-docs-nav__section-header > .chirp-theme-docs-nav__toggle'
                );
                if (toggle && toggle.getAttribute('aria-expanded') !== 'true') return false;
                node = node.parentElement
                    ? node.parentElement.closest('.chirp-theme-docs-nav__section--has-toggle')
                    : null;
            }
            return true;
        }"""
    )
    assert all_open, "an active-trail section was left collapsed"
