"""#170 — JSON-LD structured-data contract tests.

The chirp-theme emits three families of schema.org graphs in <head> via
``partials/{article,breadcrumb,product}-jsonld.html``:

  * Homepage    → Organization + WebSite (with a SearchAction) so search
                  engines can surface a sitelinks search box.
  * Doc page    → Organization + TechArticle, plus a BreadcrumbList.
  * Blog post   → Organization + BlogPosting.
  * Product     → Product (Offer + AggregateRating).

These tests render each partial through a kida ``Environment`` with the
Bengal-provided filters/globals stubbed (``absolute_url``, ``canonical_url``,
``get_breadcrumbs``, ``hasattr``, ``now``, ``dateformat``), extract every
``application/ld+json`` block, ``json.loads`` it (proving it is *valid* JSON,
not just present), and assert the ``@type`` set is correct. A regression here
means a crawler/AI scraper would get malformed or wrong-typed structured data.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

import pytest
from kida import Environment, FileSystemLoader

REPO_ROOT = Path(__file__).resolve().parents[1]
THEME_TEMPLATES = REPO_ROOT / "src" / "bengal_themes" / "chirp_theme" / "templates"

# Absolute origin Bengal derives canonical/og/sitemap URLs from (config site.yaml
# + production.yaml after #169). The stubbed filters mirror Bengal's behaviour:
# an absolute origin + path, with external http(s) inputs passing through.
ORIGIN = "https://lbliii.github.io/chirp-ui"

_LD_JSON_RE = re.compile(
    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
    re.DOTALL,
)


def _absolute_url(path: object) -> str:
    """Stub for Bengal's ``absolute_url`` filter: origin + path, http passthrough."""
    if not path:
        path = "/"
    text = str(path)
    if text.startswith("http"):
        return text
    return ORIGIN.rstrip("/") + "/" + text.lstrip("/")


def _stub_breadcrumbs(_page: object) -> list[dict[str, object]]:
    return [
        {"title": "Home", "href": "/", "is_current": False},
        {"title": "Docs", "href": "/docs/", "is_current": False},
        {"title": "Cards", "href": "/docs/components/cards/", "is_current": True},
    ]


@pytest.fixture
def theme_env() -> Environment:
    """Kida environment loading the chirp-theme templates with Bengal stubs."""
    env = Environment(loader=FileSystemLoader(str(THEME_TEMPLATES)), autoescape=True)
    env.add_filter("absolute_url", _absolute_url)
    # canonical_url() returns the absolute origin + path; the article/breadcrumb
    # partials only use absolute_url, but provide canonical_url for parity with
    # base.html's og:url/canonical/og:image surface.
    env.add_filter("canonical_url", _absolute_url)
    env.add_filter("dateformat", lambda dt, fmt: dt.strftime(fmt))
    env.add_global("canonical_url", _absolute_url)
    env.add_global("hasattr", hasattr)
    env.add_global("now", lambda: datetime(2026, 6, 10))
    env.add_global("get_breadcrumbs", _stub_breadcrumbs)
    return env


_SITE = {
    "title": "chirp-ui",
    "description": "Gorgeous Chirp components",
    "baseurl": ORIGIN,
    "organization": {
        "name": "chirp-ui",
        "url": ORIGIN,
        "logo": "/assets/chirp_ui/favicon.svg",
    },
}


def _ld_json_objects(rendered: str) -> list[dict]:
    """Extract + parse every ld+json block; proves each is *valid* JSON."""
    blocks = _LD_JSON_RE.findall(rendered)
    return [json.loads(block) for block in blocks]


def _types(objects: list[dict]) -> set[str]:
    return {obj.get("@type") for obj in objects}


def _render(env: Environment, name: str, **ctx) -> str:
    return env.get_template(f"partials/{name}").render(**ctx)


# ---------------------------------------------------------------------------
# Homepage: Organization + WebSite (with SearchAction)
# ---------------------------------------------------------------------------


def test_home_emits_website_searchaction_and_organization(theme_env: Environment) -> None:
    rendered = _render(
        theme_env,
        "article-jsonld.html",
        page={"kind": "home", "type": "page"},
        site=_SITE,
        config={},
        section=None,
        toc_items=[],
    )
    objects = _ld_json_objects(rendered)

    assert _types(objects) == {"Organization", "WebSite"}

    website = next(o for o in objects if o["@type"] == "WebSite")
    action = website["potentialAction"]
    assert action["@type"] == "SearchAction"
    # The SearchAction target must be an absolute https EntryPoint carrying the
    # {search_term_string} placeholder, or Google ignores the sitelinks box.
    target = action["target"]
    assert target["@type"] == "EntryPoint"
    assert target["urlTemplate"].startswith("https://")
    assert "{search_term_string}" in target["urlTemplate"]
    assert action["query-input"] == "required name=search_term_string"

    org = next(o for o in objects if o["@type"] == "Organization")
    assert org["@context"] == "https://schema.org"
    assert org["url"].startswith("https://")
    assert org["logo"].startswith("https://")


# ---------------------------------------------------------------------------
# Doc page: Organization + TechArticle, plus a BreadcrumbList
# ---------------------------------------------------------------------------


def test_doc_emits_techarticle_and_breadcrumblist(theme_env: Environment) -> None:
    page = {
        "kind": "doc",
        "type": "doc",
        "title": "Card component",
        "description": "How to compose cards",
        "date": "2026-01-01",
        "metadata": {},
        "author": "Lawrence",
        "word_count": 320,
        "href": "/docs/components/cards/",
        "toc_items": [],
    }
    article = _ld_json_objects(
        _render(
            theme_env,
            "article-jsonld.html",
            page=page,
            site=_SITE,
            config={},
            section={"title": "Components"},
            toc_items=[],
        )
    )
    breadcrumb = _ld_json_objects(
        _render(theme_env, "breadcrumb-jsonld.html", page=page, site=_SITE, config={})
    )

    assert _types(article) == {"Organization", "TechArticle"}
    assert _types(breadcrumb) == {"BreadcrumbList"}

    tech = next(o for o in article if o["@type"] == "TechArticle")
    assert tech["headline"] == "Card component"
    # Article URL is absolute and the publisher is the Organization.
    assert tech["url"].startswith("https://")
    assert tech["publisher"]["@type"] == "Organization"

    crumbs = breadcrumb[0]
    items = crumbs["itemListElement"]
    assert [c["@type"] for c in items] == ["ListItem", "ListItem", "ListItem"]
    assert [c["position"] for c in items] == [1, 2, 3]
    # Crumb item URLs must be absolute https.
    assert all(c["item"].startswith("https://") for c in items)


# ---------------------------------------------------------------------------
# Blog post: Organization + BlogPosting
# ---------------------------------------------------------------------------


def test_post_emits_blogposting(theme_env: Environment) -> None:
    page = {
        "kind": "post",
        "type": "post",
        "title": "chirp-ui 0.3 released",
        "description": "Release notes",
        "date": "2026-02-01",
        "metadata": {},
        "author": "Lawrence",
        "word_count": 140,
        "href": "/blog/chirp-ui-0-3/",
        "toc_items": [],
    }
    objects = _ld_json_objects(
        _render(
            theme_env,
            "article-jsonld.html",
            page=page,
            site=_SITE,
            config={},
            section={"title": "Blog"},
            toc_items=[],
        )
    )

    assert _types(objects) == {"Organization", "BlogPosting"}
    post = next(o for o in objects if o["@type"] == "BlogPosting")
    assert post["headline"] == "chirp-ui 0.3 released"
    assert post["datePublished"] == "2026-02-01"
    assert post["url"].startswith("https://")


# ---------------------------------------------------------------------------
# Product page: Product (Offer + AggregateRating)
# ---------------------------------------------------------------------------


def test_product_emits_product_with_offer(theme_env: Environment) -> None:
    page = {
        "metadata": {"structured_data": True},
        "type": "product",
        "title": "Pro Plan",
        "description": "Everything in chirp-ui",
        "images": ["/img/pro.png"],
        "sku": "PRO-1",
        "brand": "chirp-ui",
        "price": 99.0,
        "currency": "USD",
        "in_stock": True,
        "url": "/pricing/pro/",
        "aggregate_rating": {"value": 4.8, "count": 12},
    }
    objects = _ld_json_objects(
        _render(theme_env, "product-jsonld.html", page=page, site=_SITE, config={})
    )

    assert _types(objects) == {"Product"}
    product = objects[0]
    assert product["name"] == "Pro Plan"
    offer = product["offers"]
    assert offer["@type"] == "Offer"
    assert offer["availability"] == "https://schema.org/InStock"
    # The offer URL is absolute (origin + page url).
    assert offer["url"].startswith("https://")
    assert product["aggregateRating"]["@type"] == "AggregateRating"


def test_product_partial_skips_non_product_pages(theme_env: Environment) -> None:
    """No Product graph for ordinary pages (gate on type == 'product')."""
    rendered = _render(
        theme_env,
        "product-jsonld.html",
        page={"metadata": {}, "type": "doc"},
        site=_SITE,
        config={},
    )
    assert "application/ld+json" not in rendered
