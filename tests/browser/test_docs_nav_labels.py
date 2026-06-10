"""Regression proof: docs-nav section labels stay PAINTED when collapsed.

The docs sidebar uses a native <details> per collapsible section, with the
navigable section label INSIDE the <summary>. A closed <details> hides only
its NON-summary content (`::details-content { content-visibility: hidden }`),
so a label inside the summary stays painted whether the section is collapsed
or open. This keeps the "collapsed labels visible" guard with zero JavaScript
and — per the owner's preference — NO explicit caret control: the native
disclosure marker is suppressed in CSS.

These tests assert the labels are genuinely PAINTED while collapsed (Playwright
is_visible plus a non-zero painted rect that is NOT inside a
content-visibility:hidden subtree), that there is NO caret/toggle button in the
section headers, that toggling the native <details> shows/hides the children,
and that the active branch arrives open with aria-current. The section label
link intentionally lives back inside the <summary> — a deliberate UX choice by
the project owner (no caret), so the older "no <a>/<button> inside <summary>"
assertion does not apply here.
"""

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


async def _open_docs(page, static_site_url):
    await page.set_viewport_size(DESKTOP)
    await page.goto(f"{static_site_url}{DOCS_PAGE}")
    await page.wait_for_load_state("networkidle")
    # Let docs-nav.js run (landmark label + active-link scroll).
    await page.wait_for_timeout(150)


def _secondary_section(page, *, collapsed: bool):
    """Locate a <details> section in the secondary tree in the wanted state."""
    suffix = ":not([open])" if collapsed else "[open]"
    return page.locator(
        f".chirp-theme-doc-catalog__secondary details.chirp-theme-docs-nav__section{suffix}"
    )


async def test_secondary_tree_has_collapsible_sections(page, static_site_url):
    """Sanity: the page actually exercises the native <details> disclosure."""
    await _open_docs(page, static_site_url)
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    sections = page.locator(
        ".chirp-theme-doc-catalog__secondary details.chirp-theme-docs-nav__section"
    )
    assert await sections.count() >= 1, "no collapsible docs-nav <details> sections rendered"


async def test_no_caret_toggle_in_section_headers(page, static_site_url):
    """No explicit caret/toggle control anywhere in the docs-nav (owner's no-caret choice)."""
    await _open_docs(page, static_site_url)
    secondary = page.locator(".chirp-theme-doc-catalog__secondary")
    # The #162-era button toggle must be gone entirely.
    assert await secondary.locator(".chirp-theme-docs-nav__toggle").count() == 0, (
        "found a docs-nav caret/toggle button — should be removed"
    )
    assert await secondary.locator(".chirp-theme-docs-nav__section-header").count() == 0, (
        "found a docs-nav __section-header scaffold — should be removed"
    )
    # The summary's native disclosure marker is suppressed: list-style is none.
    summary = secondary.locator("summary.chirp-theme-docs-nav__summary").first
    if await summary.count():
        list_style = await summary.evaluate("el => getComputedStyle(el).listStyleType")
        assert list_style == "none", f"native disclosure marker not suppressed: {list_style!r}"


async def test_collapsed_section_label_is_painted(page, static_site_url):
    """A COLLAPSED <details> section's label is visible and genuinely painted.

    The label lives inside the <summary>, so it survives the closed state.
    """
    await _open_docs(page, static_site_url)

    collapsed = _secondary_section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    section = collapsed.first
    label = section.locator("> summary .chirp-theme-docs-nav__label")

    await expect(section).not_to_have_attribute("open", "")
    await expect(label).to_be_visible()
    assert (await label.inner_text()).strip(), "collapsed section label is empty"

    # PAINT check: non-zero painted box AND no content-visibility:hidden ancestor.
    paint = await label.evaluate(
        """el => {
            const rect = el.getBoundingClientRect();
            let node = el;
            let hidden = false;
            while (node && node !== document.body) {
                const cv = getComputedStyle(node).contentVisibility;
                if (cv === 'hidden') { hidden = true; break; }
                node = node.parentElement;
            }
            return {
                width: Math.round(rect.width),
                height: Math.round(rect.height),
                hiddenAncestor: hidden,
            };
        }"""
    )
    assert paint["width"] > 0, paint
    assert paint["height"] > 0, paint
    assert not paint["hiddenAncestor"], paint

    # The children region of a collapsed <details> must NOT be visible.
    panel = section.locator("> .chirp-theme-docs-nav__section-links")
    await expect(panel).to_be_hidden()


async def test_label_link_lives_inside_summary(page, static_site_url):
    """The section label link is intentionally INSIDE the <summary>.

    This is a deliberate UX choice by the project owner (no caret control): a
    closed <details> only hides its NON-summary content, so keeping the label
    link in the summary is what keeps collapsed labels visible without a caret.
    """
    await _open_docs(page, static_site_url)
    inside = await page.locator(
        ".chirp-theme-doc-catalog__secondary "
        "summary.chirp-theme-docs-nav__summary .chirp-theme-docs-nav__summary-link"
    ).count()
    assert inside >= 1, "expected the section label link inside <summary>"


async def test_toggle_shows_and_hides_children(page, static_site_url):
    """Toggling the native <details> shows/hides its children.

    The label link fills the <summary>, so a click on the label navigates
    rather than toggles — by design (the summary IS the section link). We
    exercise the native disclosure mechanism directly via the `open` property,
    which is exactly what the browser flips and what the CSS keys off.
    """
    await _open_docs(page, static_site_url)

    collapsed = _secondary_section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    # Pin a STABLE element handle: the `:not([open])` locator would stop
    # matching this section the moment we open it and jump to another one.
    section = await collapsed.first.element_handle()
    assert section is not None
    panel = await section.query_selector(":scope > .chirp-theme-docs-nav__section-links")
    assert panel is not None

    # Collapsed: children hidden via the native ::details-content content-visibility.
    assert not await panel.is_visible()

    # Open the native <details>: children become visible.
    await section.evaluate("el => { el.open = true; }")
    assert await section.evaluate("el => el.open") is True
    assert await panel.is_visible()

    # Close it again: children hide.
    await section.evaluate("el => { el.open = false; }")
    assert await section.evaluate("el => el.open") is False
    assert not await panel.is_visible()


async def test_active_branch_is_open_with_aria_current(page, static_site_url):
    """The active section arrives open (server-seeded) and the page is aria-current."""
    await _open_docs(page, static_site_url)

    current = page.locator('.chirp-theme-doc-catalog__secondary [aria-current="page"]')
    assert await current.count() >= 1, "no aria-current marker in the docs tree"

    # Every <details> section ancestor of the current page must be open.
    all_open = await current.first.evaluate(
        """el => {
            let node = el.closest('details.chirp-theme-docs-nav__section');
            while (node) {
                if (!node.open) return false;
                node = node.parentElement
                    ? node.parentElement.closest('details.chirp-theme-docs-nav__section')
                    : null;
            }
            return true;
        }"""
    )
    assert all_open, "an active-trail <details> section was left collapsed"
