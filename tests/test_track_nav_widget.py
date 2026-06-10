"""Render tests for the cross-track membership widget (``partials/track_nav.html``).

Covers #144: a doc whose slug appears in two tracks must render two
``.chirp-theme-track-nav`` cards (one per membership) with working prev/next
hrefs; a doc in no track must render zero cards (and no empty card wrapper).

The widget reads ``page.relative_path``, ``site.data.tracks`` and the
``get_page(slug)`` global, so the test loads the real theme template through
Bengal's Kida engine and injects a stub page registry + a synthetic
``site.data.tracks`` map. Requires Bengal (``pytest.importorskip``).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
_WORKSPACE_BENGAL = REPO_ROOT.parent / "b-stack" / "bengal"

if _WORKSPACE_BENGAL.exists():
    bengal_parent = _WORKSPACE_BENGAL.parent
    if str(bengal_parent) not in sys.path:
        sys.path.insert(0, str(bengal_parent))


# Stub pages keyed by their content-relative slug (no ``.md``). Each carries the
# title + href the widget renders into the prev/next buttons.
STUB_PAGES = {
    "docs/get-started/installation": SimpleNamespace(
        title="Installation", href="/docs/get-started/installation/"
    ),
    "docs/theming/chirp-theme": SimpleNamespace(
        title="Chirp Theme", href="/docs/theming/chirp-theme/"
    ),
    "docs/theming/bengal-theme-controls": SimpleNamespace(
        title="Theme Controls", href="/docs/theming/bengal-theme-controls/"
    ),
    "docs/app-shell/ui-layers": SimpleNamespace(
        title="UI Layers", href="/docs/app-shell/ui-layers/"
    ),
}

# Two tracks that both include ``docs/theming/chirp-theme`` -> two memberships.
STUB_TRACKS = {
    "getting-started": {
        "title": "Getting Started",
        "items": [
            "docs/get-started/installation",
            "docs/theming/chirp-theme",
            "docs/app-shell/ui-layers",
        ],
    },
    "theming-deep-dive": {
        "title": "Theming Deep Dive",
        "items": [
            "docs/theming/chirp-theme",
            "docs/theming/bengal-theme-controls",
            "docs/app-shell/ui-layers",
        ],
    },
}


@pytest.fixture
def track_nav_template():
    """The real ``partials/track_nav.html`` with a stub ``get_page`` global."""
    pytest.importorskip("bengal")

    from bengal.core import Site
    from bengal.rendering.engines.kida import KidaTemplateEngine

    site = Site.from_config(SITE_ROOT)
    engine = KidaTemplateEngine(site)
    engine._env.add_global("get_page", lambda slug: STUB_PAGES.get(slug))
    return engine._env.get_template("partials/track_nav.html")


def _render(template, slug: str) -> str:
    page = SimpleNamespace(relative_path=f"{slug}.md")
    site = SimpleNamespace(data={"tracks": STUB_TRACKS})
    return template.render(page=page, site=site)


def test_doc_in_two_tracks_renders_two_membership_cards(track_nav_template) -> None:
    html = _render(track_nav_template, "docs/theming/chirp-theme")

    # One card per membership.
    card_opens = re.findall(r'<article class="[^"]*chirp-theme-track-nav[^"]*">', html)
    assert len(card_opens) == 2, f"expected 2 track-nav cards, found {len(card_opens)}"

    # Both track titles surface.
    assert "Getting Started" in html
    assert "Theming Deep Dive" in html

    # Prev/next anchors are real internal hrefs. chirp-theme is the middle item
    # of getting-started (prev=installation, next=ui-layers) and the first item
    # of theming-deep-dive (start of track, next=bengal-theme-controls).
    assert html.count('href="/docs/get-started/installation/"') == 1  # getting-started prev
    assert html.count('href="/docs/app-shell/ui-layers/"') == 1  # getting-started next
    assert html.count('href="/docs/theming/bengal-theme-controls/"') == 1  # deep-dive next
    # theming-deep-dive starts at chirp-theme, so that card has no prev button.
    assert "Start of track" in html

    # The progress bar + actions cluster render for each membership.
    assert html.count("chirp-theme-track-nav__actions") == 2
    assert html.count("chirp-theme-track-nav__progress") == 2


def test_prev_next_anchors_do_not_hijack_boosted_navigation(track_nav_template) -> None:
    """Prev/next are plain hrefs -- no hx-target, no hx-boost override.

    Site-wide ``hx-boost`` handles them; they must not carry ``hx-boost="false"``
    (that opt-out only applies to buttons that take an ``hx_target``).
    """
    html = _render(track_nav_template, "docs/theming/chirp-theme")

    assert "hx-target" not in html
    assert "hx-boost" not in html


def test_doc_in_no_track_renders_no_widget(track_nav_template) -> None:
    html = _render(track_nav_template, "docs/some/unrelated-page")

    assert "chirp-theme-track-nav" not in html
    # No empty card wrapper leaks for a non-member: the partial guards on
    # membership, so the rendered output is whitespace-only.
    assert html.strip() == ""
