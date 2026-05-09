"""Tests for the packaged Bengal theme shipped with chirp-ui."""

import html as html_lib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from importlib import metadata, resources
from pathlib import Path, PurePosixPath

import pytest

THEME_PACKAGE = "bengal_themes.chirp_theme"
THEME_TEMPLATE_PATH_FRAGMENT = "bengal_themes/chirp_theme/templates"
REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
_WORKSPACE_BENGAL = REPO_ROOT.parent / "b-stack" / "bengal"

if _WORKSPACE_BENGAL.exists():
    bengal_parent = _WORKSPACE_BENGAL.parent
    if str(bengal_parent) not in sys.path:
        sys.path.insert(0, str(bengal_parent))

CANONICAL_TEMPLATES = (
    "index.html",
    "base.html",
    "home.html",
    "page.html",
    "doc/home.html",
    "doc/list.html",
    "doc/single.html",
)
CORE_PARITY_TEMPLATES = (
    "blog/shell.html",
    "blog/about.html",
    "blog/contact.html",
    "blog/home.html",
    "blog/list.html",
    "blog/single.html",
    "post.html",
    "search.html",
    "404.html",
    "tag.html",
    "tags.html",
    "archive.html",
    "archive-year.html",
    "author.html",
    "authors/list.html",
    "authors/single.html",
    "category-browser.html",
    "tracks/list.html",
    "tracks/single.html",
    "tutorial/list.html",
    "tutorial/single.html",
    "notebook/single.html",
    "changelog/list.html",
    "changelog/single.html",
    "resume/list.html",
    "resume/single.html",
)
REQUIRED_PARTIALS = (
    "partials/navigation-components.html",
    "partials/docs-nav.html",
    "partials/docs-toc-sidebar.html",
    "partials/page-hero.html",
    "partials/search-modal.html",
    "partials/theme-primitives.html",
    "partials/theme-controls.html",
    "partials/version-banner.html",
    "partials/stale-content-banner.html",
    "partials/taxonomy-pages.html",
    "partials/learning-pages.html",
    "partials/components/tags.html",
    "partials/components/tiles.html",
    "partials/components/related-posts-simple.html",
)
REQUIRED_DIRECTIVE_TEMPLATES = (
    "directives/admonition.html",
    "directives/cards.html",
    "directives/card.html",
    "directives/child_cards.html",
)
REQUIRED_SHORTCODE_TEMPLATES = (
    "shortcodes/audio.html",
    "shortcodes/blockquote.html",
    "shortcodes/danger.html",
    "shortcodes/details.html",
    "shortcodes/figure.html",
    "shortcodes/gallery.html",
    "shortcodes/highlight.html",
    "shortcodes/img.html",
    "shortcodes/param.html",
    "shortcodes/ref.html",
    "shortcodes/relref.html",
    "shortcodes/tip.html",
    "shortcodes/warning.html",
)
REQUIRED_AUTODOC_TEMPLATES = (
    "autodoc/partials/header.html",
    "autodoc/partials/signature.html",
    "autodoc/partials/params-table.html",
    "autodoc/partials/params-list.html",
    "autodoc/partials/returns.html",
    "autodoc/partials/raises.html",
    "autodoc/partials/examples.html",
    "autodoc/partials/usage.html",
    "autodoc/partials/badges.html",
    "autodoc/partials/cards.html",
    "autodoc/partials/members.html",
    "autodoc/partials/_macros/element-card.html",
    "autodoc/partials/_macros/function-member.html",
    "autodoc/partials/_macros/class-member.html",
    "autodoc/python/module.html",
    "autodoc/python/single.html",
    "autodoc/python/home.html",
    "autodoc/python/section-index.html",
    "autodoc/python/list.html",
    "autodoc/cli/command.html",
    "autodoc/cli/command-group.html",
    "autodoc/cli/single.html",
    "autodoc/cli/home.html",
    "autodoc/cli/section-index.html",
    "autodoc/cli/list.html",
)
REQUIRED_REFERENCE_HUB_TEMPLATES = (
    "autodoc/openapi/endpoint.html",
    "autodoc/openapi/schema.html",
    "autodoc/openapi/home.html",
    "autodoc/openapi/list.html",
    "autodoc/openapi/section-index.html",
    "autodoc/openapi/layouts/explorer.html",
    "autodoc/openapi/layouts/reference.html",
    "autodoc/openapi/partials/endpoint-header.html",
    "autodoc/openapi/partials/param-row.html",
    "autodoc/openapi/partials/playground-bar.html",
    "autodoc/openapi/partials/request-body.html",
    "autodoc/openapi/partials/responses.html",
    "autodoc/openapi/partials/code-samples.html",
    "autodoc/openapi/partials/example-rail.html",
    "autodoc/openapi/partials/request-example.html",
    "autodoc/openapi/partials/response-example.html",
    "autodoc/openapi/partials/schema-viewer.html",
    "autodoc/openapi/partials/sidebar-nav.html",
    "openapi-reference/endpoint.html",
    "openapi-reference/overview.html",
    "openapi-reference/schema.html",
    "openapi-reference/section-index.html",
    "api-reference/module.html",
    "api-reference/section-index.html",
    "api-hub/home.html",
    "api-hub/section-index.html",
    "cli-reference/section-index.html",
)
ASSET_STRING_RE = re.compile(
    r"""(?:["']|=)(/?assets/[^"'\s<>?#]+\.[A-Za-z0-9]+(?:\?[^"'\s<>]*)?(?:#[^"'\s<>]*)?)["']?"""
)
CSS_IMPORT_RE = re.compile(r"""@import\s+url\(['"]?([^'")]+\.css)['"]?\)""")


def _prefer_workspace_bengal() -> None:
    """Force Bengal imports to resolve from a sibling workspace checkout when available."""
    if not _WORKSPACE_BENGAL.exists():
        return

    bengal_parent = _WORKSPACE_BENGAL.parent
    if str(bengal_parent) not in sys.path:
        sys.path.insert(0, str(bengal_parent))

    for module_name in [
        name for name in sys.modules if name == "bengal" or name.startswith("bengal.")
    ]:
        sys.modules.pop(module_name, None)

    importlib.invalidate_caches()


def _copy_docs_site(root: Path) -> Path:
    site_root = root / "site"
    shutil.copytree(
        SITE_ROOT,
        site_root,
        ignore=shutil.ignore_patterns(
            "public", ".cache", ".bengal", ".bengal-cache", "__pycache__"
        ),
    )
    # Keep packaging tests self-contained and deterministic. The copied site does
    # not provision external fonts, so disable social-card generation rather than
    # leaving HTML pointing at assets that the build intentionally skips.
    (site_root / "config" / "_default" / "fonts.yaml").write_text("fonts: null\n", encoding="utf-8")
    (site_root / "config" / "_default" / "social_cards.yaml").write_text(
        "social_cards:\n  enabled: false\n",
        encoding="utf-8",
    )
    return site_root


def _iter_local_asset_paths(output_dir: Path) -> set[str]:
    paths: set[str] = set()
    for html_path in output_dir.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        for match in ASSET_STRING_RE.finditer(text):
            raw = html_lib.unescape(match.group(1))
            asset_path = raw.split("?", 1)[0].split("#", 1)[0].lstrip("/")
            if asset_path.startswith("assets/"):
                paths.add(asset_path)
    return paths


def _iter_resource_files(root, prefix: PurePosixPath | None = None):
    prefix = prefix or PurePosixPath("")
    for child in root.iterdir():
        rel = prefix / child.name
        if child.is_file():
            yield rel.as_posix(), child
        elif child.is_dir():
            yield from _iter_resource_files(child, rel)


def _reachable_css_assets(css_root) -> tuple[set[str], set[str]]:
    reachable: set[str] = set()
    missing: set[str] = set()
    pending = ["style.css"]

    while pending:
        rel_path = pending.pop()
        if rel_path in reachable:
            continue
        reachable.add(rel_path)

        resource = css_root / rel_path
        if not resource.is_file():
            missing.add(rel_path)
            continue

        base = PurePosixPath(rel_path).parent
        text = resource.read_text(encoding="utf-8")
        for match in CSS_IMPORT_RE.finditer(text):
            import_path = match.group(1)
            if "://" in import_path:
                continue
            pending.append((base / import_path).as_posix())

    return reachable, missing


def test_theme_entry_point_is_registered() -> None:
    """The Bengal theme entry point should resolve to the packaged theme module."""
    entry_points = metadata.entry_points(group="bengal.themes")
    match = next((entry for entry in entry_points if entry.name == "chirp-theme"), None)

    assert match is not None
    assert match.value == THEME_PACKAGE


def test_theme_package_contains_required_resources() -> None:
    """Package resources should include the standalone theme surface."""
    package_root = resources.files(THEME_PACKAGE)

    assert (package_root / "theme.toml").is_file()
    assert (package_root / "templates" / "base.html").is_file()
    assert (package_root / "templates" / "home.html").is_file()
    assert (package_root / "templates" / "search.html").is_file()
    assert (package_root / "templates" / "404.html").is_file()
    assert (package_root / "templates" / "post.html").is_file()
    assert (package_root / "templates" / "blog" / "shell.html").is_file()
    assert (package_root / "templates" / "blog" / "list.html").is_file()
    assert (package_root / "templates" / "blog" / "single.html").is_file()
    assert (package_root / "templates" / "doc" / "home.html").is_file()
    assert (package_root / "templates" / "doc" / "list.html").is_file()
    assert (package_root / "templates" / "doc" / "single.html").is_file()
    assert (package_root / "templates" / "partials" / "docs-nav.html").is_file()
    assert (package_root / "templates" / "partials" / "docs-toc-sidebar.html").is_file()
    assert (package_root / "templates" / "partials" / "theme-primitives.html").is_file()
    assert (package_root / "templates" / "partials" / "theme-controls.html").is_file()
    assert (package_root / "templates" / "directives" / "cards.html").is_file()
    assert (package_root / "templates" / "directives" / "card.html").is_file()
    assert (package_root / "templates" / "directives" / "child_cards.html").is_file()
    assert (package_root / "assets" / "css" / "style.css").is_file()
    assert (package_root / "assets" / "css" / "chirp-theme.css").is_file()
    assert (package_root / "assets" / "js" / "core" / "theme.js").is_file()
    assert (package_root / "assets" / "icons" / "close.svg").is_file()
    assert (package_root / "assets" / "favicon.svg").is_file()


def test_chirp_theme_templates_do_not_use_theme_adapter_macros() -> None:
    """Theme templates should import Chirp UI macros directly instead of theme adapters."""
    package_root = resources.files(THEME_PACKAGE)
    primitives = (package_root / "templates" / "partials" / "theme-primitives.html").read_text(
        encoding="utf-8"
    )
    template_text = "\n".join(
        resource.read_text(encoding="utf-8")
        for rel_path, resource in _iter_resource_files(package_root / "templates")
        if rel_path.endswith(".html")
    )
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")

    assert "def theme_" not in primitives
    assert "theme_page_header" not in template_text
    assert "theme_surface" not in template_text
    assert "theme_link_card" not in template_text
    assert "theme_docs_frame" not in template_text
    assert "theme_feed" not in template_text
    assert ".chirp-theme-docs-layout {" in css
    assert "display: grid;" in css
    assert "grid-template-columns:" in css
    assert "chirp-theme-docs-layout--with-toc" in css


def test_chirp_theme_tokens_use_chirpui_vocabulary() -> None:
    """Theme-specific CSS should tune Chirp UI tokens instead of creating a parallel token API."""
    package_root = resources.files(THEME_PACKAGE)
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")

    assert "--chirpui-accent:" in css
    assert "--chirpui-container-max:" in css
    assert "--chirpui-prose-max-width:" in css
    assert "--chirp-theme-" not in css


def test_chirp_theme_style_uses_chirpui_cards_instead_of_legacy_card_bundle() -> None:
    """The main theme bundle should not load Bengal's old bespoke card system."""
    package_root = resources.files(THEME_PACKAGE)
    css = (package_root / "assets" / "css" / "style.css").read_text(encoding="utf-8")

    assert not (package_root / "assets" / "css" / "components" / "cards.css").is_file()
    assert "components/cards.css" not in css


def test_chirp_theme_blog_cards_use_chirpui_resources() -> None:
    """Blog/list card templates should use Chirp UI cards instead of copied article-card markup."""
    package_root = resources.files(THEME_PACKAGE)
    post_card = (
        package_root / "templates" / "partials" / "components" / "post-card.html"
    ).read_text(encoding="utf-8")
    related_card = (
        package_root / "templates" / "partials" / "components" / "related-post-card.html"
    ).read_text(encoding="utf-8")
    tags = (package_root / "templates" / "partials" / "components" / "tags.html").read_text(
        encoding="utf-8"
    )
    style = (package_root / "assets" / "css" / "style.css").read_text(encoding="utf-8")

    assert "resource_card" in post_card
    assert "resource_card" in related_card
    assert "chirpui/badge.html" in tags
    assert "article-card" not in post_card
    assert "blog-card-" not in post_card
    assert "blog-read-more" not in post_card
    assert "components/related-posts.css" not in style


def test_chirp_theme_css_assets_are_reachable_from_style_entrypoint() -> None:
    """The package should not ship copied CSS files outside the active theme graph."""
    package_root = resources.files(THEME_PACKAGE)
    css_root = package_root / "assets" / "css"
    style = (css_root / "style.css").read_text(encoding="utf-8")

    all_css = {
        rel_path
        for rel_path, _resource in _iter_resource_files(css_root)
        if rel_path.endswith(".css")
    }
    reachable, missing = _reachable_css_assets(css_root)
    orphaned = sorted(all_css - reachable)

    assert not missing, "style.css imports missing CSS assets: " + ", ".join(sorted(missing))
    assert not orphaned, "CSS assets are not reachable from style.css: " + ", ".join(orphaned)
    assert "../../../../chirp_ui/templates/chirpui.css" in style
    assert "../../../../chirp_ui/templates/chirpui-transitions.css" in style


def test_theme_manifest_declares_standalone_package() -> None:
    """The packaged theme manifest should not inherit Bengal default anymore."""
    package_root = resources.files(THEME_PACKAGE)
    manifest_text = (package_root / "theme.toml").read_text(encoding="utf-8")

    assert 'name = "chirp-theme"' in manifest_text
    assert 'libraries = ["chirp_ui"]' in manifest_text
    assert "extends" not in manifest_text


def test_docs_site_config_points_at_chirp_theme() -> None:
    """The docs site should dogfood the packaged theme by default."""
    theme_config = SITE_ROOT / "config" / "_default" / "theme.yaml"
    text = theme_config.read_text(encoding="utf-8")

    assert 'name: "chirp-theme"' in text


def test_bengal_resolves_packaged_theme() -> None:
    """Bengal should discover chirp-theme through its installed theme registry."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")

    from bengal.core.theme import get_theme_package

    package = get_theme_package("chirp-theme")

    assert package is not None
    assert package.package == THEME_PACKAGE
    assert package.manifest_exists()
    assert package.templates_exists()
    assert package.assets_exists()


def test_docs_site_theme_templates_load_via_bengal_kida_engine() -> None:
    """The docs site should resolve theme templates and partials from chirp-theme itself."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")

    from bengal.core import Site
    from bengal.rendering.engines.kida import KidaTemplateEngine

    site = Site.from_config(SITE_ROOT)
    engine = KidaTemplateEngine(site)

    assert site.theme == "chirp-theme"
    assert any(THEME_TEMPLATE_PATH_FRAGMENT in str(path) for path in engine.template_dirs)

    for template_name in (
        *CANONICAL_TEMPLATES,
        *CORE_PARITY_TEMPLATES,
        *REQUIRED_PARTIALS,
        *REQUIRED_DIRECTIVE_TEMPLATES,
        *REQUIRED_SHORTCODE_TEMPLATES,
        *REQUIRED_AUTODOC_TEMPLATES,
        *REQUIRED_REFERENCE_HUB_TEMPLATES,
    ):
        template = engine._env.get_template(template_name)

        assert template is not None
        assert template.filename is not None
        assert THEME_TEMPLATE_PATH_FRAGMENT in template.filename.replace("\\", "/")

    provider_template = engine._env.get_template("chirpui/card.html")
    assert provider_template is not None
    assert "chirp_ui/templates/chirpui/card.html" in provider_template.filename.replace("\\", "/")


def test_chirp_theme_admonition_directive_uses_chirpui_callout() -> None:
    """Bengal admonitions should render through Chirp UI callout semantics."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")

    from bengal.core import Site
    from bengal.rendering.engines.kida import KidaTemplateEngine

    site = Site.from_config(SITE_ROOT)
    engine = KidaTemplateEngine(site)
    template = engine._env.get_template("directives/admonition.html")

    html = template.render(
        name="danger",
        title="Danger",
        css_class="danger user-class",
        icon_name="alert",
        icon_html='<svg aria-hidden="true"></svg>',
        extra_class="user-class",
        children="<p>Do not continue.</p>",
    )

    assert "chirpui-callout chirpui-callout--error" in html
    assert "chirp-theme-directive-admonition--danger" in html
    assert "user-class" in html
    assert "<p>Do not continue.</p>" in html
    assert '<svg aria-hidden="true"></svg>' in html
    assert 'class="admonition' not in html


def test_chirp_theme_taxonomy_templates_use_chirpui_resource_patterns() -> None:
    """Taxonomy/archive pages should be Chirp UI-native, not copied default shells."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    taxonomy_templates = (
        "tag.html",
        "tags.html",
        "archive.html",
        "archive-year.html",
        "author.html",
        "authors/list.html",
        "authors/single.html",
        "category-browser.html",
        "partials/taxonomy-pages.html",
    )

    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in taxonomy_templates
    )

    assert "chirpui/resource_index.html" in combined
    assert "chirpui/card.html" in combined
    assert "chirpui/badge.html" in combined
    assert "partials/components/post-card.html" in combined
    assert "chirp-theme-taxonomy-index" in combined
    assert "<script" not in combined
    assert "tag-card gradient-border" not in combined
    assert "archive-post-card" not in combined
    assert "category-card" not in combined
    assert "author-card-link" not in combined


def test_chirp_theme_learning_templates_use_chirpui_patterns() -> None:
    """Learning/content verticals should compose Chirp UI primitives."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    learning_templates = (
        "tracks/list.html",
        "tracks/single.html",
        "tutorial/list.html",
        "tutorial/single.html",
        "notebook/single.html",
        "changelog/list.html",
        "changelog/single.html",
        "resume/list.html",
        "resume/single.html",
        "partials/learning-pages.html",
        "partials/track-sidebar.html",
        "partials/track_nav.html",
    )

    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in learning_templates
    )

    assert "chirpui/resource_index.html" in combined
    assert "chirpui/stepper.html" in combined
    assert "chirpui/rendered_content.html" in combined
    assert "partials/components/post-card.html" in combined
    assert "chirp-theme-learning-index" in combined
    assert "<script" not in combined
    assert "track-card" not in combined
    assert "tutorial-card" not in combined
    assert "notebook-cell" not in combined
    assert "card mb-4" not in combined
    assert "btn btn-" not in combined
    assert 'class="progress"' not in combined


def test_chirp_theme_shortcodes_use_chirpui_components() -> None:
    """Shortcodes should map authored embeds to Chirp UI-backed output."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in REQUIRED_SHORTCODE_TEMPLATES
    )

    assert "chirpui/callout.html" in combined
    assert "chirpui/accordion.html" in combined
    assert "chirpui-card" in combined
    assert "chirpui-code-block" in combined
    assert "chirp-theme-shortcode-gallery" in combined
    assert "<script" not in combined
    assert "callout callout-tip" not in combined
    assert "callout callout-warning" not in combined
    assert "callout callout-danger" not in combined
    assert 'class="figure"' not in combined
    assert 'class="gallery' not in combined


def test_chirp_theme_autodoc_templates_use_chirpui_reference_patterns() -> None:
    """Python and CLI autodoc pages should be Chirp UI-native reference surfaces."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in REQUIRED_AUTODOC_TEMPLATES
    )

    assert "chirpui/resource_index.html" in combined
    assert "chirpui/params_table.html" in combined
    assert "chirpui/accordion.html" in combined
    assert "chirpui/code.html" in combined
    assert "chirpui/badge.html" in combined
    assert "chirp-theme-reference" in combined
    assert "<script" not in combined
    assert "autodoc-summary-table" not in combined
    assert "autodoc-table" not in combined
    assert "command-card" not in combined


def test_chirp_theme_reference_hubs_use_chirpui_patterns() -> None:
    """OpenAPI/API hub paths should resolve to Chirp UI reference components."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in REQUIRED_REFERENCE_HUB_TEMPLATES
    )

    assert "chirpui/resource_index.html" in combined
    assert "chirpui/params_table.html" in combined
    assert "chirpui/accordion.html" in combined
    assert "chirpui/code.html" in combined
    assert "chirpui/nav_tree.html" in combined
    assert "chirp-theme-rest-reference__examples" in combined
    assert "Request and response examples" in combined
    assert "autodoc/openapi/endpoint.html" in combined
    assert "autodoc/python/module.html" in combined
    assert "autodoc/cli/list.html" in combined
    assert "<script" not in combined
    assert "openapi-sidebar" not in combined
    assert "endpoint-card" not in combined
    assert "api-hub-card" not in combined


def test_chirp_theme_utility_pages_use_retained_chirpui_primitives() -> None:
    """Root aliases and utility blog pages should not reintroduce one-off shells."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    utility_templates = ("index.html", "blog/about.html", "blog/contact.html")
    combined = "\n".join(
        (templates_root / template_name).read_text(encoding="utf-8")
        for template_name in utility_templates
    )

    assert "chirpui/resource_index.html" in combined
    assert "blog/shell.html" in combined
    assert "chirpui/hero.html" in combined
    assert "chirpui/rendered_content.html" in combined
    assert "chirpui/surface.html" in combined
    assert "<script" not in combined
    assert "blog-about-header" not in combined
    assert "blog-contact-header" not in combined
    assert "contact-social" not in combined


def test_docs_site_cards_and_tiles_render_with_chirpui_templates(tmp_path: Path) -> None:
    """Bengal card-like content should render through chirp-theme's Chirp UI templates."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")
    site_root = _copy_docs_site(tmp_path)
    result_path = tmp_path / "directive-check.json"
    script = r"""
import json
import re
import sys
from pathlib import Path

from bengal.core import Site
from bengal.orchestration.build.options import BuildOptions

site_root = Path(sys.argv[1])
result_path = Path(sys.argv[2])

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

docs_html = (site.output_dir / "docs" / "index.html").read_text(encoding="utf-8")
docs_section_html = (site.output_dir / "docs" / "get-started" / "index.html").read_text(
    encoding="utf-8"
)
home_html = (site.output_dir / "index.html").read_text(encoding="utf-8")
releases_html = (site.output_dir / "releases" / "index.html").read_text(encoding="utf-8")
tags_html = (site.output_dir / "tags" / "index.html").read_text(encoding="utf-8")
tag_html = (site.output_dir / "tags" / "installation" / "index.html").read_text(encoding="utf-8")
legacy_content_tile_re = re.compile(r'class="[^"]*\bcontent-(?:tile|tiles)\b')
result_path.write_text(
    json.dumps(
        {
            "has_chirpui_grid": "chirpui-grid" in docs_html,
            "has_chirpui_card": "chirpui-card" in docs_html,
            "docs_section_has_chirpui_sidebar": "chirpui-sidebar" in docs_section_html,
            "docs_section_has_chirpui_breadcrumbs": "chirpui-breadcrumbs" in docs_section_html,
            "docs_section_has_legacy_docs_nav": 'class="docs-nav"' in docs_section_html,
            "home_has_chirpui_hero": "chirpui-hero chirpui-hero--page" in home_html,
            "home_has_chirpui_grid": "chirpui-grid" in home_html,
            "home_has_chirpui_resource_card": "chirpui-resource-card" in home_html,
            "home_has_legacy_hero_inner": "chirp-theme-home__hero-inner" in home_html,
            "has_legacy_card_grid": 'class="card-grid"' in docs_html,
            "has_legacy_card": 'class="card"' in docs_html,
            "has_chirpui_resource_card": "chirpui-resource-card" in releases_html,
            "has_legacy_content_tile": bool(legacy_content_tile_re.search(releases_html)),
            "tags_has_resource_index": "chirpui-resource-index" in tags_html,
            "tags_has_taxonomy_card": "chirp-theme-taxonomy-card" in tags_html,
            "tag_page_has_resource_index": "chirpui-resource-index" in tag_html,
            "tag_page_has_post_card": "chirp-theme-post-card" in tag_html,
            "tags_has_legacy_tag_card": "tag-card gradient-border" in tags_html,
        }
    ),
    encoding="utf-8",
)
"""
    env = dict(os.environ)
    if _WORKSPACE_BENGAL.exists():
        env["PYTHONPATH"] = (
            str(_WORKSPACE_BENGAL.parent)
            if "PYTHONPATH" not in env
            else str(_WORKSPACE_BENGAL.parent) + os.pathsep + env["PYTHONPATH"]
        )
    subprocess.run(
        [sys.executable, "-c", script, str(site_root), str(result_path)],
        check=True,
        env=env,
        cwd=str(_WORKSPACE_BENGAL if _WORKSPACE_BENGAL.exists() else REPO_ROOT),
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))

    assert result["has_chirpui_grid"]
    assert result["has_chirpui_card"]
    assert result["docs_section_has_chirpui_sidebar"]
    assert result["docs_section_has_chirpui_breadcrumbs"]
    assert not result["docs_section_has_legacy_docs_nav"]
    assert result["home_has_chirpui_hero"]
    assert result["home_has_chirpui_grid"]
    assert result["home_has_chirpui_resource_card"]
    assert not result["home_has_legacy_hero_inner"]
    assert not result["has_legacy_card_grid"]
    assert not result["has_legacy_card"]
    assert result["has_chirpui_resource_card"]
    assert not result["has_legacy_content_tile"]
    assert result["tags_has_resource_index"]
    assert result["tags_has_taxonomy_card"]
    assert result["tag_page_has_resource_index"]
    assert result["tag_page_has_post_card"]
    assert not result["tags_has_legacy_tag_card"]


def test_docs_site_build_resolves_header_navigation_links(tmp_path: Path) -> None:
    """Built docs HTML should not render empty top or mobile navigation URLs."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")
    site_root = _copy_docs_site(tmp_path)
    result_path = tmp_path / "nav-check.json"
    script = r"""
import json
import re
import sys
from pathlib import Path

from bengal.core import Site
from bengal.orchestration.build.options import BuildOptions

site_root = Path(sys.argv[1])
result_path = Path(sys.argv[2])

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

index_html = (site.output_dir / "index.html").read_text(encoding="utf-8")
header = re.search(r"<header\b.*?</header>", index_html, re.DOTALL)
mobile = re.search(r"<dialog\b[^>]*id=\"mobile-nav-dialog\".*?</dialog>", index_html, re.DOTALL)

result_path.write_text(
    json.dumps(
        {
            "header": header.group(0) if header else "",
            "mobile": mobile.group(0) if mobile else "",
        }
    ),
    encoding="utf-8",
)
"""
    env = dict(os.environ)
    if _WORKSPACE_BENGAL.exists():
        env["PYTHONPATH"] = (
            str(_WORKSPACE_BENGAL.parent)
            if "PYTHONPATH" not in env
            else str(_WORKSPACE_BENGAL.parent) + os.pathsep + env["PYTHONPATH"]
        )
    subprocess.run(
        [sys.executable, "-c", script, str(site_root), str(result_path)],
        check=True,
        env=env,
        cwd=str(_WORKSPACE_BENGAL if _WORKSPACE_BENGAL.exists() else REPO_ROOT),
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    combined_nav = result["header"] + result["mobile"]

    assert result["header"], "Expected built home page to include a header."
    assert result["mobile"], "Expected built home page to include mobile navigation."
    assert 'href=""' not in combined_nav
    assert "Component showcase" in combined_nav
    assert re.search(r"""href=(?:"/showcase/"|'/showcase/'|/showcase/)""", combined_nav)
    assert "Documentation" in combined_nav
    assert re.search(r"""href=(?:"/docs/"|'/docs/'|/docs/)""", combined_nav)


def test_docs_site_build_emits_special_pages(tmp_path: Path) -> None:
    """Bengal post-processing should render chirp-theme 404 and search pages."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")
    site_root = _copy_docs_site(tmp_path)
    result_path = tmp_path / "special-pages-check.json"
    script = r"""
import json
import sys
from pathlib import Path

from bengal.core import Site
from bengal.orchestration.build.options import BuildOptions

site_root = Path(sys.argv[1])
result_path = Path(sys.argv[2])

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

not_found = site.output_dir / "404.html"
search = site.output_dir / "search" / "index.html"
result_path.write_text(
    json.dumps(
        {
            "has_404": not_found.is_file(),
            "has_search": search.is_file(),
            "not_found_html": not_found.read_text(encoding="utf-8") if not_found.is_file() else "",
            "search_html": search.read_text(encoding="utf-8") if search.is_file() else "",
        }
    ),
    encoding="utf-8",
)
"""
    env = dict(os.environ)
    if _WORKSPACE_BENGAL.exists():
        env["PYTHONPATH"] = (
            str(_WORKSPACE_BENGAL.parent)
            if "PYTHONPATH" not in env
            else str(_WORKSPACE_BENGAL.parent) + os.pathsep + env["PYTHONPATH"]
        )
    subprocess.run(
        [sys.executable, "-c", script, str(site_root), str(result_path)],
        check=True,
        env=env,
        cwd=str(_WORKSPACE_BENGAL if _WORKSPACE_BENGAL.exists() else REPO_ROOT),
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))

    assert result["has_404"]
    assert result["has_search"]
    assert "Page Not Found" in result["not_found_html"]
    assert "search-input" in result["search_html"]


def test_docs_site_build_only_references_emitted_assets(tmp_path: Path) -> None:
    """Built docs HTML should only reference fingerprinted assets that were emitted."""
    _prefer_workspace_bengal()
    pytest.importorskip("bengal")
    site_root = _copy_docs_site(tmp_path)
    result_path = tmp_path / "asset-check.json"
    script = r"""
import html as html_lib
import json
import re
import sys
from pathlib import Path

from bengal.assets.manifest import AssetManifest
from bengal.core import Site
from bengal.orchestration.build.options import BuildOptions
from chirp_ui.filters import chirpui_asset_path

site_root = Path(sys.argv[1])
result_path = Path(sys.argv[2])
asset_re = re.compile(r'''(?:["']|=)(/?assets/[^"'\s<>?#]+\.[A-Za-z0-9]+(?:\?[^"'\s<>]*)?(?:#[^"'\s<>]*)?)["']?''')

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

manifest = AssetManifest.load(site.output_dir / "asset-manifest.json")
manifest_outputs = {entry.output_path.lstrip("/") for entry in manifest.entries.values()}
expected_asset_entries = [
    chirpui_asset_path("chirpui.js"),
    "css/style.css",
]
asset_outputs = {
    logical_path: (
        manifest.entries[logical_path].output_path.lstrip("/")
        if logical_path in manifest.entries
        else None
    )
    for logical_path in expected_asset_entries
}
referenced_assets = set()
for html_path in site.output_dir.rglob("*.html"):
    text = html_path.read_text(encoding="utf-8")
    for match in asset_re.finditer(text):
        raw = html_lib.unescape(match.group(1))
        referenced_assets.add(raw.split("?", 1)[0].split("#", 1)[0].lstrip("/"))

missing_manifest_entries = sorted(referenced_assets - manifest_outputs)
missing_files = sorted(
    asset_path for asset_path in referenced_assets if not (site.output_dir / asset_path).is_file()
)
result_path.write_text(
    json.dumps(
        {
            "referenced_assets": sorted(referenced_assets),
            "missing_manifest_entries": missing_manifest_entries,
            "missing_files": missing_files,
            "asset_outputs": asset_outputs,
        }
    ),
    encoding="utf-8",
)
"""
    env = dict(os.environ)
    if _WORKSPACE_BENGAL.exists():
        env["PYTHONPATH"] = (
            str(_WORKSPACE_BENGAL.parent)
            if "PYTHONPATH" not in env
            else str(_WORKSPACE_BENGAL.parent) + os.pathsep + env["PYTHONPATH"]
        )
    subprocess.run(
        [sys.executable, "-c", script, str(site_root), str(result_path)],
        check=True,
        env=env,
        cwd=str(_WORKSPACE_BENGAL if _WORKSPACE_BENGAL.exists() else REPO_ROOT),
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    referenced_assets = result["referenced_assets"]
    missing_manifest_entries = result["missing_manifest_entries"]
    missing_files = result["missing_files"]
    asset_outputs = result["asset_outputs"]
    forbidden_provider_css_refs = sorted(
        {
            "assets/chirp_ui/chirpui.css",
            "assets/chirp_ui/chirpui-transitions.css",
        }
        & set(referenced_assets)
    )
    missing_asset_outputs = sorted(
        logical_path for logical_path, output_path in asset_outputs.items() if not output_path
    )
    unreferenced_asset_outputs = sorted(
        output_path
        for output_path in asset_outputs.values()
        if output_path and output_path not in referenced_assets
    )

    assert referenced_assets, "Expected built docs HTML to reference packaged theme assets."
    assert not missing_asset_outputs, (
        "Expected Chirp theme assets in asset-manifest.json: " + ", ".join(missing_asset_outputs)
    )
    assert not forbidden_provider_css_refs, (
        "Built HTML referenced standalone Chirp UI provider CSS instead of the theme stylesheet: "
        + ", ".join(forbidden_provider_css_refs)
    )
    assert not unreferenced_asset_outputs, (
        "Built HTML did not reference emitted Chirp theme assets: "
        + ", ".join(unreferenced_asset_outputs)
    )
    assert not missing_manifest_entries, (
        "Built HTML referenced assets missing from asset-manifest.json: "
        + ", ".join(missing_manifest_entries)
    )
    assert not missing_files, "Built HTML referenced assets missing on disk: " + ", ".join(
        missing_files
    )
