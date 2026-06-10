"""Browser dogfood smoke for the Tracks learning-path feature (#143).

Loads the built ``/tracks/getting-started/`` pillar page from the static
``site/public`` output and proves the two behaviours that make a track more
than a landing page:

1. Scroll-spy: scrolling the reading column moves the ``data-track-active``
   marker from the first sidebar section link to a later one
   (``tracks.js`` -> ``updateCurrentSection``).
2. Progress persistence + resume: the active section is written to
   ``localStorage['bengal_track_progress_getting-started']`` (the storage key
   is ``bengal_track_progress_`` + the ``data-track-id`` on the track nav), and
   on reload the ``.track-resume-banner`` is offered to continue where the
   reader left off.

Authored to mirror ``tests/browser/test_bengal_docs_chrome.py`` (static
``site/public`` HTTP server + per-test Playwright page). Runs in the
non-required ``browser-smoke`` CI job after ``docs-build-all`` produces
``site/public/tracks/getting-started/``.
"""

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_PUBLIC = REPO_ROOT / "site" / "public"

TRACK_ID = "getting-started"
TRACK_PATH = f"/tracks/{TRACK_ID}/"
STORAGE_KEY = f"bengal_track_progress_{TRACK_ID}"


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


async def _open_track(page, static_site_url: str) -> None:
    await page.set_viewport_size({"width": 1280, "height": 900})
    await page.goto(f"{static_site_url}{TRACK_PATH}")
    await page.wait_for_load_state("networkidle")
    await page.wait_for_timeout(100)


async def test_track_pillar_renders_sidebar_and_sections(page, static_site_url):
    """The pillar page exposes the JS contract tracks.js drives."""
    await _open_track(page, static_site_url)

    track_nav = page.locator('[data-bengal="track-nav"][data-track-id]')
    await track_nav.first.wait_for(state="attached")
    assert await track_nav.get_attribute("data-track-id") == TRACK_ID

    # Server renders one section block per track item.
    assert await page.locator(".chirp-theme-track-section[data-track-section]").count() >= 2
    # And one sidebar link per section.
    assert await page.locator(".chirp-theme-track-sidebar__link[data-track-section]").count() >= 2


async def test_track_scroll_spy_moves_active_section(page, static_site_url):
    """Scrolling moves the data-track-active marker to a later section link."""
    await _open_track(page, static_site_url)

    active = page.locator(".chirp-theme-track-sidebar__link[data-track-active]")
    # The initial update marks the first section active.
    await active.first.wait_for(state="attached")
    first_active = await active.first.get_attribute("data-track-section")

    # Scroll to the last section block so the scroll-spy advances.
    last_section = page.locator(".chirp-theme-track-section[data-track-section]").last
    await last_section.scroll_into_view_if_needed()
    await page.wait_for_timeout(300)  # throttled scroll handler + section update

    new_active = await page.locator(
        ".chirp-theme-track-sidebar__link[data-track-active]"
    ).first.get_attribute("data-track-section")

    assert new_active is not None
    assert new_active != first_active, (
        f"data-track-active did not advance on scroll (stayed at {first_active})"
    )


async def test_track_progress_persists_and_resume_banner_appears(page, static_site_url):
    """Active section is saved to localStorage and offered as a resume on reload."""
    await _open_track(page, static_site_url)

    # Scroll past the first section so lastSection > 0 gets persisted.
    last_section = page.locator(".chirp-theme-track-section[data-track-section]").last
    await last_section.scroll_into_view_if_needed()
    await page.wait_for_timeout(300)

    stored = await page.evaluate("(key) => localStorage.getItem(key)", STORAGE_KEY)
    assert stored is not None, f"{STORAGE_KEY} was not written"

    progress = json.loads(stored)
    assert progress.get("lastSection", 0) > 0, progress
    assert isinstance(progress.get("visited"), list), progress
    assert progress["visited"], progress

    # Reload near the top of the page: tracks.js offers the resume banner
    # (checkResume runs ~500ms after init when lastSection > 0 and scrollY < 200).
    await page.reload()
    await page.wait_for_load_state("networkidle")

    # localStorage survives the reload.
    persisted = await page.evaluate("(key) => localStorage.getItem(key)", STORAGE_KEY)
    assert persisted is not None, f"{STORAGE_KEY} did not persist across reload"
    assert json.loads(persisted)["lastSection"] > 0

    banner = page.locator(".track-resume-banner")
    await banner.wait_for(state="visible", timeout=2000)
    await banner.get_by_role("button", name="Resume:").wait_for(state="visible")
