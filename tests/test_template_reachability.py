"""Template reachability guard for the shipped Bengal ``chirp-theme``.

Wave 1 of the pre-1.0 productization saga (#150) deleted a large set of
orphaned partials — the ``partials/page-hero/`` family, ``action-bar.html``,
``connect-to-ide.html``, the DEPRECATED ``docs-nav-node.html``,
``partials/search.html`` (with its dead ``x-mark`` icon), and ``link-previews``.
This test stops new orphans from accumulating: it walks every template under
``templates/``, builds an extends/include/import graph, and asserts each
template is either

1. referenced by another theme template (an inbound graph edge), **or**
2. reachable by a Bengal routing/subsystem convention (top-level page kind,
   ``<section>/{list,single,home,...}.html`` layout, or a
   ``directives/`` / ``shortcodes/`` / ``autodoc/`` subsystem template
   resolved by path), **or**
3. on the small, documented ``INTENTIONALLY_RETAINED`` allowlist of partials we
   ship-but-do-not-yet-wire (blog component kit + theme primitives).

A genuinely dead partial that is none of the above fails the test with a
pointer to delete it or wire it in.
"""

from __future__ import annotations

import re
from importlib import resources

THEME_PACKAGE = "bengal_themes.chirp_theme"

# Theme-local references. ``chirpui/*`` imports resolve to the chirp-ui library
# (a separate package), not to a theme template, so they never count as a
# theme-template inbound edge.
REFERENCE_RE = re.compile(r"""\{%-?\s*(?:extends|include|from|import)\s+['"]([^'"]+\.html)['"]""")

# Top-level templates Bengal route-maps directly from a page's kind/layout.
# These never carry an inbound edge but are real, reachable entry points.
TOPLEVEL_ENTRIES = frozenset(
    {
        "base.html",
        "index.html",
        "home.html",
        "page.html",
        "post.html",
        "404.html",
        "tag.html",
        "tags.html",
        "archive.html",
        "archive-year.html",
        "author.html",
        "search.html",
        "category-browser.html",
    }
)

# Subsystem template trees resolved by path convention rather than by an
# explicit Kida include/import: Bengal's directive renderer, shortcode
# renderer, and autodoc generators each look templates up by name.
SUBSYSTEM_PREFIXES = ("directives/", "shortcodes/", "autodoc/")

# Leaf names that mark a section-scoped routing entry, e.g. ``blog/list.html``,
# ``tracks/single.html``, ``api-hub/home.html``. Bengal maps a content
# section's pages to ``<section>/<leaf>.html`` by layout convention.
ENTRY_LEAFS = frozenset(
    {
        "list.html",
        "single.html",
        "home.html",
        "about.html",
        "contact.html",
        "shell.html",
        "section-index.html",
        "module.html",
        "command.html",
        "command-group.html",
        "endpoint.html",
        "schema.html",
        "overview.html",
    }
)

# Partials we intentionally ship but do not (yet) wire into a live template.
#
# Recorded decision for #150: the blog component kit + theme primitives are a
# productization surface — a consumer building a blog/marketing site composes
# them directly, and several are pinned by the package surface contract in
# tests/test_bengal_theme_package.py (REQUIRED_PARTIALS). They are kept, not
# deleted; when a future blog-dogfood pass wires one into blog/single.html it
# simply drops off this list. Anything NOT on this list and NOT reachable is a
# real orphan and must be deleted or wired.
INTENTIONALLY_RETAINED = frozenset(
    {
        "partials/components/article.html",
        "partials/components/author-bio.html",
        "partials/components/blog-post-meta.html",
        "partials/components/blog-share-dropdown.html",
        "partials/components/card-base.html",
        "partials/components/comments-section.html",
        "partials/components/helpers.html",
        "partials/components/newsletter-cta.html",
        "partials/components/related-posts.html",
        "partials/components/social-share.html",
        "partials/components/widgets.html",
        "partials/nav-menu.html",
        "partials/tag-nav.html",
        "partials/theme-primitives.html",
    }
)


def _iter_templates(root, prefix: str = ""):
    for child in root.iterdir():
        rel = f"{prefix}{child.name}"
        if child.is_dir():
            yield from _iter_templates(child, prefix=f"{rel}/")
        elif rel.endswith(".html"):
            yield rel, child


def _build_graph() -> tuple[set[str], dict[str, set[str]]]:
    templates_root = resources.files(THEME_PACKAGE) / "templates"
    files = dict(_iter_templates(templates_root))
    names = set(files)
    inbound: dict[str, set[str]] = {name: set() for name in names}

    for name, resource in files.items():
        text = resource.read_text(encoding="utf-8")
        for match in REFERENCE_RE.finditer(text):
            target = match.group(1)
            if target.startswith("chirpui/"):
                continue
            if target in names:
                inbound[target].add(name)
    return names, inbound


def _is_convention_entry(name: str) -> bool:
    if name in TOPLEVEL_ENTRIES:
        return True
    if name.startswith(SUBSYSTEM_PREFIXES):
        return True
    return "/" in name and name.rsplit("/", 1)[1] in ENTRY_LEAFS


def test_no_referenced_template_is_missing() -> None:
    """Every theme-local extends/include/import target resolves to a real file."""
    templates_root = resources.files(THEME_PACKAGE) / "templates"
    files = dict(_iter_templates(templates_root))
    names = set(files)
    dangling: dict[str, set[str]] = {}

    for name, resource in files.items():
        text = resource.read_text(encoding="utf-8")
        for match in REFERENCE_RE.finditer(text):
            target = match.group(1)
            if target.startswith("chirpui/"):
                continue
            if target not in names:
                dangling.setdefault(target, set()).add(name)

    assert not dangling, "Templates reference missing theme templates: " + "; ".join(
        f"{target} (from {', '.join(sorted(src))})" for target, src in sorted(dangling.items())
    )


def test_every_template_is_reachable() -> None:
    """No orphaned partials: every template is referenced, routed, or allowlisted."""
    names, inbound = _build_graph()

    orphans = sorted(
        name
        for name in names
        if not inbound[name]
        and not _is_convention_entry(name)
        and name not in INTENTIONALLY_RETAINED
    )

    assert not orphans, (
        "Orphaned theme templates (no inbound include/import, not a routing entry, "
        "not on the INTENTIONALLY_RETAINED allowlist). Delete them, wire them into a "
        "live template, or add a documented allowlist entry: " + ", ".join(orphans)
    )


def test_allowlist_entries_still_exist_and_stay_orphaned() -> None:
    """Keep the retained-partials allowlist honest.

    If an allowlisted partial is deleted, or later gets wired in (gains an
    inbound edge), it should drop off the list so the allowlist never rots into
    a graveyard of stale names.
    """
    names, inbound = _build_graph()

    stale = sorted(name for name in INTENTIONALLY_RETAINED if name not in names)
    assert not stale, (
        "INTENTIONALLY_RETAINED references templates that no longer exist; "
        "remove them from the allowlist: " + ", ".join(stale)
    )

    now_wired = sorted(
        name for name in INTENTIONALLY_RETAINED if name in names and inbound.get(name)
    )
    assert not now_wired, (
        "These partials are now referenced by a live template; drop them from "
        "INTENTIONALLY_RETAINED so the allowlist stays minimal: " + ", ".join(now_wired)
    )


def test_wave1_orphans_stay_deleted() -> None:
    """The partials Wave 1 (#150) removed must not reappear."""
    templates_root = resources.files(THEME_PACKAGE) / "templates"
    removed = (
        "partials/page-hero.html",
        "partials/page-hero/index.html",
        "partials/page-hero/element.html",
        "partials/page-hero/section.html",
        "partials/page-hero/_macros.html",
        "partials/action-bar.html",
        "partials/connect-to-ide.html",
        "partials/docs-nav-node.html",
        "partials/search.html",
        "partials/link-previews.html",
    )
    resurrected = [name for name in removed if (templates_root / name).is_file()]
    assert not resurrected, "Templates deleted in Wave 1 (#150) have reappeared: " + ", ".join(
        resurrected
    )
