"""Browser proof: the floating back-to-top button honors prefers-reduced-motion (#164).

`enhancements/interactive.js` wires the `.back-to-top.chirp-theme-floating-top`
control to `window.scrollTo({ top: 0, behavior })`. CSS `scroll-behavior` does
NOT override an explicit `behavior:'smooth'` option, so the smooth/auto choice
must be made in JS. This test emulates a reduced-motion user (Playwright
`reduced_motion="reduce"`), patches `window.scrollTo` to capture the behavior
passed by the click handler, clicks the button, and asserts the handler chose
`behavior:'auto'` (an instant jump) — never `'smooth'`. A second context with
motion allowed asserts the handler chooses `'smooth'`.

Authored alongside the unit-level coverage in
``tests/js/interactive_reduced_motion.test.js`` (which exercises the same
handler against a stubbed BengalUtils). Runs in the non-required browser-smoke
job; mirrors the fixtures in ``test_docs_landmarks_a11y.py``.
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

# A long docs page so the back-to-top control becomes scroll-visible.
DOCS_PAGE = "/docs/theming/chirp-theme/"
DESKTOP = {"width": 1440, "height": 900}

# Capture every window.scrollTo({behavior}) the click handler issues.
CAPTURE_SCROLL_TO = """
() => {
    window.__scrollBehaviors = [];
    window.scrollTo = (opts) => {
        if (opts && typeof opts === 'object') {
            window.__scrollBehaviors.push(opts.behavior);
        }
    };
}
"""


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


async def _click_back_to_top(static_site_url, *, reduced_motion):
    """Open the docs page under the given motion preference, click the
    back-to-top control, and return the list of scroll behaviors it issued."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(reduced_motion=reduced_motion)
        page = await ctx.new_page()
        try:
            await page.set_viewport_size(DESKTOP)
            await page.goto(f"{static_site_url}{DOCS_PAGE}")
            await page.wait_for_load_state("networkidle")
            # Let interactive.js wire the control, then scroll so it is shown.
            await page.wait_for_timeout(200)
            await page.evaluate("window.scrollTo(0, 800)")
            await page.wait_for_timeout(100)

            button = page.locator(".back-to-top.chirp-theme-floating-top").first
            if await button.count() == 0:
                pytest.skip("floating back-to-top control not rendered on this page")
            await expect(button).to_be_attached()

            # Patch scrollTo AFTER the initial scroll so we only capture the click.
            await page.evaluate(CAPTURE_SCROLL_TO)
            await button.click(force=True)
            await page.wait_for_timeout(50)
            return await page.evaluate("() => window.__scrollBehaviors")
        finally:
            await ctx.close()
            await browser.close()


async def test_back_to_top_jumps_instantly_under_reduced_motion(static_site_url):
    """Reduced-motion users get an instant jump (behavior:'auto'), never smooth."""
    behaviors = await _click_back_to_top(static_site_url, reduced_motion="reduce")
    assert behaviors, "back-to-top click issued no window.scrollTo"
    assert "smooth" not in behaviors, f"reduced-motion user got a smooth scroll: {behaviors!r}"
    assert "auto" in behaviors, f"expected an instant 'auto' jump, got {behaviors!r}"


async def test_back_to_top_smooth_scrolls_when_motion_allowed(static_site_url):
    """With motion allowed, the back-to-top control smooth-scrolls as before."""
    behaviors = await _click_back_to_top(static_site_url, reduced_motion="no-preference")
    assert behaviors, "back-to-top click issued no window.scrollTo"
    assert "smooth" in behaviors, (
        f"expected a smooth scroll when motion is allowed, got {behaviors!r}"
    )
