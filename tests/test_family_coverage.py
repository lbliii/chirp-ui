"""#147 — family-coverage + taxonomy smoke tests.

Two failure modes this module guards against:

1. A shipped template family (blog/tutorial/resume/authors/changelog/tracks/
   docs/releases) renders **zero** pages — the route lands on an empty list or a
   404, and nothing in CI notices because no test asserts the family is wired to
   content. The source-level checks here fail the suite the moment a family
   loses its ``_index.md`` or its last child page.

2. The tag/category/author taxonomy is barely exercised, so ``/tags/`` renders a
   near-empty cloud and the ``max_tags_display`` / ``popular_tags_count`` theme
   knobs are inert. The taxonomy checks assert the tag corpus is rich enough that
   ``popular_tags_count`` (20) actually truncates and the popular ordering is
   non-trivial (multiple tags shared across pages), and that at least one author
   landing carries multiple posts.

Source-level assertions always run (no build needed). Built-route assertions
read ``site/public`` and skip when the site is unbuilt — the Gate rebuilds the
site before verification, where a built ``index.html`` is the static-site
analogue of a 200 response.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT = REPO_ROOT / "site" / "content"
SITE_PUBLIC = REPO_ROOT / "site" / "public"
THEME_CONFIG = REPO_ROOT / "site" / "config" / "_default"
THEME_YAML = THEME_CONFIG / "theme.yaml"

# Every shipped template family that owns a top-level content section. Each must
# ship an ``_index.md`` (so the list route renders instead of 404ing) and at
# least one child page (so the list is non-empty). A family that drops to zero
# pages fails the suite — that is the core #147 guard.
SHIPPED_FAMILIES = (
    "blog",
    "tutorial",
    "resume",
    "authors",
    "changelog",
    "tracks",
    "docs",
    "releases",
)


def _read_frontmatter(md: Path) -> dict:
    """Parse a Markdown file's YAML frontmatter block into a dict.

    Returns ``{}`` for files without a leading ``---`` fence.
    """
    import yaml

    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, _, rest = text.partition("---\n")
    front_raw, sep, _ = rest.partition("\n---")
    if not sep:
        return {}
    return yaml.safe_load(front_raw) or {}


def _content_md_files() -> list[Path]:
    return sorted(SITE_CONTENT.rglob("*.md"))


def _tag_frequency() -> dict[str, int]:
    """Count how many content pages declare each tag (the popular-tags input)."""
    pytest.importorskip("yaml", reason="PyYAML not installed")
    freq: dict[str, int] = {}
    for md in _content_md_files():
        front = _read_frontmatter(md)
        tags = front.get("tags")
        if not isinstance(tags, list):
            continue
        for tag in tags:
            if isinstance(tag, str) and tag.strip():
                freq[tag.strip()] = freq.get(tag.strip(), 0) + 1
    return freq


def _child_pages(section: str) -> list[Path]:
    """Real child content pages under a family section (excludes ``_index.md``)."""
    section_dir = SITE_CONTENT / section
    if not section_dir.is_dir():
        return []
    return [p for p in section_dir.rglob("*.md") if p.name != "_index.md"]


# ---------------------------------------------------------------------------
# Source-level family coverage — a zero-page family fails the suite.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("section", SHIPPED_FAMILIES)
def test_shipped_family_has_section_index(section: str) -> None:
    """#147 — every shipped family has a section index so its route renders."""
    index = SITE_CONTENT / section / "_index.md"
    assert index.is_file(), f"{section}/ has no _index.md — /{section}/ would 404 (#147)"


@pytest.mark.parametrize("section", SHIPPED_FAMILIES)
def test_shipped_family_renders_at_least_one_page(section: str) -> None:
    """#147 — every shipped family ships >=1 child page, so the list is non-empty.

    This is the core guard: if a family drops to zero pages (its content is
    deleted or moved), its list route renders empty and this test fails.
    """
    children = _child_pages(section)
    assert children, (
        f"{section}/ has no child pages — /{section}/ would render an empty list "
        f"(#147). Add real content or remove the family."
    )


@pytest.mark.parametrize("section", sorted(SHIPPED_FAMILIES))
def test_built_family_route_renders_non_placeholder(section: str) -> None:
    """#147 — each family route builds to a 200-equivalent, real-content page.

    Skipped when the site is unbuilt; the Gate rebuilds before verification.
    """
    page = SITE_PUBLIC / section / "index.html"
    if not page.is_file():
        pytest.skip("site/public not built; the Gate rebuilds the site first")

    html = page.read_text(encoding="utf-8")
    assert "fallback-notice" not in html, (
        f"/{section}/ rendered the Bengal fallback page — its template crashed (#147)"
    )
    assert "<title" in html, f"/{section}/ has no <title> — not a real page (#147)"
    assert len(html) > 2000, f"/{section}/ index.html looks like a placeholder (#147)"


@pytest.mark.parametrize("section", sorted(SHIPPED_FAMILIES))
def test_built_family_has_child_route(section: str) -> None:
    """#147 — each family builds at least one child route, not just the list shell.

    A family index can render even with zero children; this proves the children
    actually produced output directories. Skipped when the site is unbuilt.
    """
    section_dir = SITE_PUBLIC / section
    if not section_dir.is_dir():
        pytest.skip("site/public not built; the Gate rebuilds the site first")

    child_routes = [d for d in section_dir.iterdir() if d.is_dir() and (d / "index.html").is_file()]
    assert child_routes, (
        f"/{section}/ built no child routes — the family rendered zero pages (#147)"
    )


# ---------------------------------------------------------------------------
# Taxonomy smoke — /tags/ is meaningful and exercises the theme knobs.
# ---------------------------------------------------------------------------


def _theme_knob(name: str, default: int) -> int:
    """Read an integer theme knob (max_tags_display / popular_tags_count)."""
    pytest.importorskip("yaml", reason="PyYAML not installed")
    import yaml

    data = yaml.safe_load(THEME_YAML.read_text(encoding="utf-8")) or {}
    theme = data.get("theme", {}) or {}
    value = theme.get(name, default)
    try:
        return int(value)
    except TypeError, ValueError:
        return default


def test_tag_corpus_exceeds_popular_tags_count() -> None:
    """#147 — there are more distinct tags than ``popular_tags_count``.

    ``popular_tags_widget`` requests ``popular_tags(limit=popular_tags_count)``.
    If the corpus has fewer distinct tags than the limit, the limit never
    truncates and the knob is inert. With more distinct tags than the limit, the
    popular-tags ordering genuinely selects a top-N slice.
    """
    freq = _tag_frequency()
    distinct = len(freq)
    popular_count = _theme_knob("popular_tags_count", 20)
    assert distinct > popular_count, (
        f"only {distinct} distinct tags across content, but popular_tags_count is "
        f"{popular_count} — the popular-tags limit never truncates, so the knob is "
        f"inert. Tag more pages so /tags/ is a meaningful cloud (#147)."
    )


def test_popular_tags_ordering_is_non_trivial() -> None:
    """#147 — popularity ordering is meaningful: several tags span multiple pages.

    ``popular_tags`` ranks tags by how many pages use them. If every tag is used
    once, the ordering is arbitrary and the popular cloud is just an alphabet
    soup. Require at least two tags shared by 2+ pages so the top of the cloud
    reflects real popularity.
    """
    freq = _tag_frequency()
    shared = sorted(
        (count for count in freq.values() if count >= 2),
        reverse=True,
    )
    assert len(shared) >= 2, (
        "fewer than two tags are shared across multiple pages, so the popular-tags "
        "ordering is arbitrary. Give the tag cloud a real frequency gradient (#147)."
    )
    # And the most popular tag must clearly lead, not tie everything at 2.
    assert shared[0] >= 3, (
        f"the most popular tag spans only {shared[0]} pages — there is no clear "
        f"popular state for /tags/ to surface (#147)."
    )


def test_pages_stay_within_max_tags_display_or_corpus_is_capped() -> None:
    """#147 — the ``max_tags_display`` per-page cap is a configured, sane knob.

    ``tag_list`` truncates a page's tag list at ``max_tags_display`` and appends
    a ``+N more`` badge past it. The knob must be a positive int so the truncation
    path is reachable, and no page should bury its identity under an absurd tag
    list that the cap would silently hide.
    """
    max_display = _theme_knob("max_tags_display", 0)
    assert max_display > 0, (
        "max_tags_display is unset/zero — the per-page tag cap is disabled, so a "
        "page could render an unbounded tag list (#147)."
    )

    freq = _tag_frequency()
    # Re-walk to find any single page that exceeds the display cap; a few are
    # fine (the +N more badge handles them) but a page with far more tags than
    # the cap is almost always a frontmatter mistake.
    overflowing = []
    for md in _content_md_files():
        front = _read_frontmatter(md)
        tags = front.get("tags")
        if isinstance(tags, list) and len(tags) > max_display * 2:
            overflowing.append(md.relative_to(REPO_ROOT))
    assert not overflowing, (
        f"pages carry more than 2x max_tags_display ({max_display}) tags, which the "
        f"cap would mostly hide: {overflowing} (#147)."
    )
    assert freq, "no content declares tags — /tags/ would be empty (#147)."


def test_built_tags_index_lists_a_meaningful_set() -> None:
    """#147 — the built ``/tags/`` page renders a real, multi-term cloud.

    Skipped when the site is unbuilt. Asserts the index exists, is real content,
    and that many tag-term routes were built (not the near-empty taxonomy the
    issue flagged).
    """
    index = SITE_PUBLIC / "tags" / "index.html"
    if not index.is_file():
        pytest.skip("site/public not built; the Gate rebuilds the site first")

    html = index.read_text(encoding="utf-8")
    assert "fallback-notice" not in html, "/tags/ rendered the fallback page (#147)"
    assert len(html) > 2000, "/tags/ index.html looks like a placeholder (#147)"

    term_routes = [
        d for d in (SITE_PUBLIC / "tags").iterdir() if d.is_dir() and (d / "index.html").is_file()
    ]
    # More than max_tags_display worth of terms proves the cloud is non-trivial.
    assert len(term_routes) > _theme_knob("max_tags_display", 10), (
        f"only {len(term_routes)} tag-term routes built — /tags/ is still a "
        f"near-empty taxonomy (#147)."
    )


def test_author_landing_has_multiple_posts() -> None:
    """#147 — at least one author landing renders with multiple associated pages.

    The blog section cascades ``author: chirp-ui-team`` onto every post, so the
    author landing must aggregate more than one page. Source-level so it holds
    before a rebuild: count posts whose resolved author is the team author.
    """
    pytest.importorskip("yaml", reason="PyYAML not installed")

    # The blog _index.md cascades an author onto its children.
    blog_index = _read_frontmatter(SITE_CONTENT / "blog" / "_index.md")
    cascade = blog_index.get("cascade") or {}
    cascade_author = cascade.get("author") if isinstance(cascade, dict) else None

    author_posts: dict[str, int] = {}
    for md in _content_md_files():
        front = _read_frontmatter(md)
        author = front.get("author")
        if not author and md.parent.name == "blog" and md.name != "_index.md":
            author = cascade_author
        if isinstance(author, str) and author.strip():
            author_posts[author] = author_posts.get(author, 0) + 1

    multi = {a: n for a, n in author_posts.items() if n >= 2}
    assert multi, (
        "no author is credited on 2+ pages, so no author landing aggregates a real feed (#147)."
    )


def _category_frequency() -> dict[str, int]:
    """Count how many content pages declare each ``category`` (singular).

    Bengal's taxonomy orchestrator collects categories from the singular
    ``page.metadata["category"]`` key (``bengal/orchestration/taxonomy.py``), so
    this mirrors exactly what feeds ``site.taxonomies["categories"]`` and the
    ``category-browser.html`` landing. The ``categories`` taxonomy is enabled by
    Bengal's defaults (``{"tags": {}, "categories": {}}``) — no ``taxonomies``
    config block is needed in ``site/config/_default``.
    """
    pytest.importorskip("yaml", reason="PyYAML not installed")
    freq: dict[str, int] = {}
    for md in _content_md_files():
        front = _read_frontmatter(md)
        category = front.get("category")
        if isinstance(category, str) and category.strip():
            freq[category.strip()] = freq.get(category.strip(), 0) + 1
    return freq


def test_category_landing_has_multiple_pages() -> None:
    """#147 — at least one category landing aggregates >=2 associated pages.

    Mirrors ``test_author_landing_has_multiple_posts``: source-level so it holds
    before a rebuild. Bengal reads the singular ``category:`` frontmatter into
    ``site.taxonomies["categories"]``; a category with only one page renders a
    near-empty landing, so require >=1 category shared by 2+ pages (the docs
    ``components`` and ``patterns`` categories already satisfy this).
    """
    freq = _category_frequency()
    multi = {category: count for category, count in freq.items() if count >= 2}
    assert multi, (
        "no category is declared on 2+ pages, so no category landing aggregates a "
        "real set (#147). Add a `category:` frontmatter key to related pages."
    )
