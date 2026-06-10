"""Regression proof: docs-nav section labels stay PAINTED when collapsed.

Issue #162 moved the navigable section label out of the disclosure
<summary> and into a sibling <a>. A *closed* native <details> hides every
non-<summary> descendant via `::details-content { content-visibility:
hidden }`, so collapsed sections rendered only the bare caret — the labels
("Get Started", "Components", "Reference", …) vanished until expanded.

The fix replaces <details> with an always-visible header row (caret <button>
+ sibling label link) and a JS-toggled children region. These tests assert
the labels are genuinely PAINTED while collapsed (Playwright is_visible plus a
non-zero painted rect that is NOT inside a content-visibility:hidden subtree),
that toggling shows/hides the children, that the caret is keyboard-operable,
and that no focusable control lives inside a <summary>.
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
    # Let docs-nav.js run its collapse pass.
    await page.wait_for_timeout(150)


def _secondary_section(page, *, collapsed: bool):
    """Locate a has-toggle section in the secondary tree in the wanted state."""
    state = "false" if collapsed else "true"
    return page.locator(
        ".chirp-theme-doc-catalog__secondary "
        ".chirp-theme-docs-nav__section--has-toggle:has("
        f'.chirp-theme-docs-nav__toggle[aria-expanded="{state}"]'
        ")"
    )


async def test_secondary_tree_has_collapsible_sections(page, static_site_url):
    """Sanity: the page actually exercises the has-toggle disclosure."""
    await _open_docs(page, static_site_url)
    await expect(page.locator(".chirp-theme-doc-catalog__secondary")).to_be_visible()
    sections = page.locator(
        ".chirp-theme-doc-catalog__secondary .chirp-theme-docs-nav__section--has-toggle"
    )
    assert await sections.count() >= 1, "no collapsible docs-nav sections rendered"


async def test_collapsed_section_label_is_painted(page, static_site_url):
    """A COLLAPSED section's label is visible and genuinely painted."""
    await _open_docs(page, static_site_url)

    collapsed = _secondary_section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    section = collapsed.first
    toggle = section.locator(".chirp-theme-docs-nav__toggle")
    label = section.locator(".chirp-theme-docs-nav__section-header .chirp-theme-docs-nav__label")

    await expect(toggle).to_have_attribute("aria-expanded", "false")
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

    # The children region of a collapsed section must NOT be visible.
    panel_id = await toggle.get_attribute("aria-controls")
    assert panel_id, "toggle is missing aria-controls"
    panel = page.locator(f"#{panel_id}")
    await expect(panel).to_be_hidden()


async def test_no_interactive_control_inside_summary(page, static_site_url):
    """#162 a11y win preserved: no focusable element nested in a <summary>."""
    await _open_docs(page, static_site_url)
    nested = await page.locator(
        ".chirp-theme-doc-catalog__secondary summary :is(a, button)"
    ).count()
    assert nested == 0, "found a focusable control nested inside a <summary>"
    # The disclosure control itself is a real <button>, never inside <summary>.
    assert (
        await page.locator(
            ".chirp-theme-doc-catalog__secondary button.chirp-theme-docs-nav__toggle"
        ).count()
        >= 1
    )


async def test_toggle_shows_and_hides_children(page, static_site_url):
    """Clicking the caret toggles aria-expanded AND children visibility."""
    await _open_docs(page, static_site_url)

    collapsed = _secondary_section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    # Pin a STABLE selector via aria-controls so re-resolution does not jump to
    # another section once this one's aria-expanded flips to "true".
    panel_id = await collapsed.first.locator(".chirp-theme-docs-nav__toggle").get_attribute(
        "aria-controls"
    )
    toggle = page.locator(f'.chirp-theme-docs-nav__toggle[aria-controls="{panel_id}"]')
    panel = page.locator(f"#{panel_id}")

    await expect(panel).to_be_hidden()
    await toggle.click()
    await expect(toggle).to_have_attribute("aria-expanded", "true")
    await expect(panel).to_be_visible()

    await toggle.click()
    await expect(toggle).to_have_attribute("aria-expanded", "false")
    await expect(panel).to_be_hidden()


async def test_toggle_is_keyboard_operable(page, static_site_url):
    """The caret is focusable and Enter/Space toggle aria-expanded."""
    await _open_docs(page, static_site_url)

    collapsed = _secondary_section(page, collapsed=True)
    if await collapsed.count() == 0:
        pytest.skip("every section is on the active trail; none collapsed")

    # Pin a stable selector via aria-controls (see test_toggle_shows_and_hides).
    panel_id = await collapsed.first.locator(".chirp-theme-docs-nav__toggle").get_attribute(
        "aria-controls"
    )
    toggle = page.locator(f'.chirp-theme-docs-nav__toggle[aria-controls="{panel_id}"]')
    await toggle.focus()
    assert await toggle.evaluate("el => el === document.activeElement")

    await expect(toggle).to_have_attribute("aria-expanded", "false")
    await page.keyboard.press("Enter")
    await expect(toggle).to_have_attribute("aria-expanded", "true")
    await page.keyboard.press("Space")
    await expect(toggle).to_have_attribute("aria-expanded", "false")


async def test_active_branch_is_expanded_with_aria_current(page, static_site_url):
    """The active section auto-expands and the current page is aria-current."""
    await _open_docs(page, static_site_url)

    current = page.locator('.chirp-theme-doc-catalog__secondary [aria-current="page"]')
    assert await current.count() >= 1, "no aria-current marker in the docs tree"

    # Any has-toggle section ancestor of the current page must be expanded.
    expanded = await current.first.evaluate(
        """el => {
            let node = el.closest('.chirp-theme-docs-nav__section--has-toggle');
            while (node) {
                const toggle = node.querySelector(
                    ':scope > .chirp-theme-docs-nav__section-header '
                    + '> .chirp-theme-docs-nav__toggle'
                );
                if (toggle && toggle.getAttribute('aria-expanded') !== 'true') {
                    return false;
                }
                node = node.parentElement
                    ? node.parentElement.closest(
                        '.chirp-theme-docs-nav__section--has-toggle'
                      )
                    : null;
            }
            return true;
        }"""
    )
    assert expanded, "an active-trail section was left collapsed"
