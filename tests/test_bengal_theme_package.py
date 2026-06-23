"""Tests for the packaged Bengal theme shipped with chirp-ui."""

import html as html_lib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from importlib import metadata, resources
from pathlib import Path, PurePosixPath

import pytest

THEME_PACKAGE = "bengal_themes.chirp_theme"
THEME_TEMPLATE_PATH_FRAGMENT = "bengal_themes/chirp_theme/templates"
REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
THEME_TOML = REPO_ROOT / "src" / "bengal_themes" / "chirp_theme" / "theme.toml"
BASE_TEMPLATE = REPO_ROOT / "src" / "bengal_themes" / "chirp_theme" / "templates" / "base.html"
_WORKSPACE_BENGAL = REPO_ROOT.parent / "b-stack" / "bengal"
BENGAL_ANATOMY_DOC = REPO_ROOT / "docs" / "theming" / "bengal-theme-anatomy.md"

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
    "partials/components/article.html",
    "partials/components/author-bio.html",
    "partials/components/blog-post-meta.html",
    "partials/components/blog-share-dropdown.html",
    "partials/components/card-base.html",
    "partials/components/social-share.html",
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
    "shortcodes/component_specimen.html",
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
ASSET_ATTR_RE = re.compile(r"""(?:href|src|content)\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+))""")
CSS_IMPORT_RE = re.compile(r"""@import\s+url\(['"]?([^'")]+\.css)['"]?\)""")


def _unwrap_theme_layer(css: str) -> str:
    """Strip the outer ``@layer chirp-theme { ... }`` wrapper for content assertions.

    The theme CSS now lives entirely inside a single ``@layer chirp-theme`` block
    (the cascade contract that lets the theme restyle the chirp-ui baseline while
    staying downstream-overridable). The wrapper indents every rule by two spaces.
    Tests that assert exact block formatting (``.selector {\\n  decl;``) describe the
    *authored* rule, not the layer wrapper, so we de-indent the layer body by two
    spaces before matching. Substring/selector-presence assertions are unaffected.
    """
    marker = "@layer chirp-theme {"
    start = css.find(marker)
    if start == -1:
        return css
    body_start = start + len(marker)
    end = css.rfind("}")
    if end <= body_start:
        return css
    body = css[body_start:end]
    deindented = "\n".join(
        line[2:] if line.startswith("  ") else line for line in body.splitlines()
    )
    return deindented


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
        for match in ASSET_ATTR_RE.finditer(text):
            raw = html_lib.unescape(next(group for group in match.groups() if group))
            asset_path = _normalize_referenced_asset(raw)
            if asset_path:
                paths.add(asset_path)
    return paths


def _normalize_referenced_asset(raw: str) -> str:
    asset_path = raw.split("?", 1)[0].split("#", 1)[0]
    if "assets/" not in asset_path:
        return ""
    asset_path = asset_path[asset_path.index("assets/") :].lstrip("/")
    while asset_path.startswith("./"):
        asset_path = asset_path[2:]
    while asset_path.startswith("../"):
        asset_path = asset_path[3:]
    return asset_path


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
    assert (package_root / "assets" / "favicon-16x16.png").is_file()
    assert (package_root / "assets" / "favicon-32x32.png").is_file()
    assert (package_root / "assets" / "favicon.ico").is_file()
    assert (package_root / "assets" / "apple-touch-icon.png").is_file()
    assert (package_root / "assets" / "site.webmanifest").is_file()


def test_chirp_theme_literal_template_asset_urls_exist() -> None:
    """Literal asset_url references in packaged templates should resolve to assets."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    assets_root = package_root / "assets"
    asset_pattern = re.compile(r"""asset_url\(\s*['"]([^'"]+)['"]\s*\)""")
    referenced: set[str] = set()

    for rel_path, resource in _iter_resource_files(templates_root):
        if not rel_path.endswith(".html"):
            continue
        text = resource.read_text(encoding="utf-8")
        referenced.update(asset_pattern.findall(text))

    # Bengal generates the display-font stylesheet and woff2 weights at build
    # time from site fonts config (fonts.yaml: fonts.display). They are not
    # committed source assets, so exclude them from the source-asset check.
    def _is_generated(path: str) -> bool:
        return path == "fonts.css" or (path.startswith("fonts/") and path.endswith(".woff2"))

    missing = sorted(
        path
        for path in referenced
        if not _is_generated(path) and not (assets_root / path).is_file()
    )

    assert "css/style.css" in referenced
    assert "js/enhancements/action-bar.js" in referenced
    assert not missing, "Literal template asset_url references missing assets: " + ", ".join(
        missing
    )


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
    assert "grid-template-columns: minmax(18rem, 21rem) minmax(0, 1fr) minmax(10rem, 14rem)" in css
    assert "chirp-theme-docs-layout--with-toc" in css


def test_bengal_theme_anatomy_records_application_chrome_parity() -> None:
    """Bengal docs chrome should stay a theme consumer, not a hidden Chirp UI API."""
    text = BENGAL_ANATOMY_DOC.read_text(encoding="utf-8")

    assert "## Application Chrome Parity" in text
    assert "Bengal docs chrome is a real application chrome consumer" in text
    assert "same contract as Chirp UI app shell chrome" in text
    for expectation in [
        "header identity, docs rail, TOC rail, search trigger, mobile nav, and theme",
        "persistent docs navigation uses Chirp UI sidebar/nav primitives",
        "mobile navigation uses the packaged dialog fallback",
        "search modal behavior remains Bengal-owned",
        "TOC and docs rail do not starve article content",
        "`--chirpui-*` tokens",
        "evaluated as a Chirp UI registry",
    ]:
        assert expectation in text


def test_chirp_theme_docs_chrome_mobile_width_contract() -> None:
    """Docs chrome should not give article or code content a fixed mobile width."""
    package_root = resources.files(THEME_PACKAGE)
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")
    main_js = (package_root / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    header_css = (package_root / "assets" / "css" / "layouts" / "header.css").read_text(
        encoding="utf-8"
    )

    assert "@media (max-width: 768px)" in css
    assert ".chirp-theme-docs-layout__hero" in css
    assert ".chirp-theme-docs-layout__article" in css
    assert ".chirp-theme-docs-layout__content" in css
    assert ".chirp-theme-doc-catalog {" in css
    assert ".chirp-theme-doc-catalog-rail__item" in css
    assert ".chirp-theme-docs-layout .code-block-wrapper" in css
    assert ".chirp-theme-docs-layout .code-block-wrapper pre code" in css
    assert ".chirp-theme-docs-layout .code-block-wrapper--specimen" in css
    assert ".chirp-theme-docs-layout .code-block-wrapper--specimen::before" in css
    assert "code-block-wrapper--specimen" in main_js
    assert "chirp-theme-reference-member__description" in main_js
    assert '.chirp-theme-docs-layout .rosettes[data-language="plaintext"]' in css
    assert "max-width: 100%;" in css
    assert "min-width: 0;" in css
    assert "@media (min-width: 769px)" in header_css


def test_chirp_theme_tokens_use_chirpui_vocabulary() -> None:
    """Theme-specific CSS should tune Chirp UI tokens instead of creating a parallel token API."""
    package_root = resources.files(THEME_PACKAGE)
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")

    assert "--chirpui-accent:" in css
    assert "--chirpui-container-max:" in css
    assert "--chirpui-prose-max-width:" in css
    assert "--chirp-theme-" not in css


def test_chirp_theme_theme_controls_are_appearance_only() -> None:
    """The bespoke theme control surface should not expose legacy Bengal palettes."""
    package_root = resources.files(THEME_PACKAGE)
    controls = (package_root / "templates" / "partials" / "theme-controls.html").read_text(
        encoding="utf-8"
    )
    base = (package_root / "templates" / "base.html").read_text(encoding="utf-8")
    theme_js = (package_root / "assets" / "js" / "core" / "theme.js").read_text(encoding="utf-8")

    assert "data-appearance" in controls
    assert "appearance_option('system'" in controls
    assert "appearance_option('light'" in controls
    assert "appearance_option('dark'" in controls

    assert "data-palette" not in controls
    assert "data-theme-pack" not in controls
    assert "theme.palette_" not in controls

    for source in (controls, base, theme_js):
        assert "snow-lynx" not in source
        assert "brown-bengal" not in source
        assert "silver-bengal" not in source
        assert "charcoal-bengal" not in source
        assert "blue-bengal" not in source

    assert "setAttribute('data-palette'" not in base
    assert "setAttribute('data-palette'" not in theme_js
    assert "bengal-palette" in base
    assert "bengal-palette" in theme_js
    assert "removeItem('bengal-palette')" in base
    # theme.js purges the legacy palette key through the guarded storage
    # wrapper (no raw localStorage in the module), so the cleanup reads as
    # safeStorage.remove('bengal-palette') rather than a direct removeItem.
    assert "remove('bengal-palette')" in theme_js


def test_chirp_theme_interactive_control_hooks_stay_aligned() -> None:
    """Theme partials and static JS should agree on packaged control hooks."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    assets_root = package_root / "assets"

    base = (templates_root / "base.html").read_text(encoding="utf-8")
    theme_controls = (templates_root / "partials" / "theme-controls.html").read_text(
        encoding="utf-8"
    )
    search_modal = (templates_root / "partials" / "search-modal.html").read_text(encoding="utf-8")
    search_page = (templates_root / "search.html").read_text(encoding="utf-8")
    toc_sidebar = (templates_root / "partials" / "docs-toc-sidebar.html").read_text(
        encoding="utf-8"
    )
    navigation = (templates_root / "partials" / "navigation-components.html").read_text(
        encoding="utf-8"
    )
    theme_js = (assets_root / "js" / "core" / "theme.js").read_text(encoding="utf-8")
    search_js = (assets_root / "js" / "core" / "search.js").read_text(encoding="utf-8")
    mobile_nav_js = (assets_root / "js" / "enhancements" / "mobile-nav.js").read_text(
        encoding="utf-8"
    )
    action_bar_js = (assets_root / "js" / "enhancements" / "action-bar.js").read_text(
        encoding="utf-8"
    )
    interactive_js = (assets_root / "js" / "enhancements" / "interactive.js").read_text(
        encoding="utf-8"
    )
    tabs_js = (assets_root / "js" / "enhancements" / "tabs.js").read_text(encoding="utf-8")
    toc_js = (assets_root / "js" / "enhancements" / "toc.js").read_text(encoding="utf-8")
    style = (assets_root / "css" / "style.css").read_text(encoding="utf-8")

    assert "asset_url('js/bundle.js')" not in base
    assert "asset_url('js/enhancements/action-bar.js')" in base

    assert 'popovertarget="{{ _theme_menu_id }}"' in theme_controls
    assert 'popover class="theme-dropdown__menu--popover"' in theme_controls
    assert 'class="theme-option"' in theme_controls
    assert "querySelectorAll('.theme-dropdown__menu--popover[popover]')" in theme_js
    assert "window.BengalTheme" in theme_js

    assert 'id="search-modal"' in search_modal
    assert 'id="search-modal-input"' in search_modal
    assert 'id="search-modal-results-list"' in search_modal
    assert "data-close-modal" in search_modal
    assert "document.getElementById('search-modal')" in search_js
    assert "window.BengalSearchModal" in search_js
    assert "#nav-search-trigger" in search_js

    # #172 — Cmd+K modal scope chips (Docs / API / Releases) wired to search.js.
    assert 'class="search-modal__scopes"' in search_modal
    assert 'data-scope="docs"' in search_modal
    assert 'data-scope="api"' in search_modal
    assert 'data-scope="releases"' in search_modal
    assert "querySelectorAll('.search-modal__scope')" in search_js
    assert "filterByScope" in search_js

    assert 'id="search-input"' in search_page
    assert 'data-chirp-theme-surface="search"' in search_page
    assert "document.getElementById('search-input')" in search_js

    assert 'id="mobile-nav-dialog"' in base
    assert 'class="mobile-nav-search" data-open-search' in base
    assert "theme-menu-desktop" in base
    assert "theme-menu-mobile" in base
    assert "chirp-theme-floating-top" in base
    assert "chirp-theme-floating-top" in toc_sidebar
    assert 'data-chirp-theme-floating-action="top"' in toc_sidebar
    assert "chirp-theme-rail-top" not in toc_sidebar
    assert "querySelectorAll('.back-to-top')" in interactive_js
    assert "chirp-theme-floating-top" in interactive_js
    assert "chirp-theme-footer__rule-mark" in interactive_js
    assert "--chirpui-floating-top-left" in interactive_js
    assert "document.getElementById('mobile-nav-dialog')" in mobile_nav_js
    assert "window.BengalNav" in mobile_nav_js
    assert "window.BengalSearchModal.open()" in mobile_nav_js

    assert 'data-action="copy-url"' in (
        templates_root / "partials" / "components" / "blog-share-dropdown.html"
    ).read_text(encoding="utf-8")
    assert "'data-action': 'copy-url'" in (
        templates_root / "partials" / "components" / "social-share.html"
    ).read_text(encoding="utf-8")
    assert "querySelectorAll('[popovertarget]')" in action_bar_js
    assert "closest('[data-action^=\"copy\"]')" in action_bar_js

    assert 'data-bengal="toc"' in navigation
    assert 'data-toc-mode="normal"' in navigation
    assert 'data-toc-item="#{{ node_id }}"' in navigation
    assert "details.toc-group" in toc_js
    assert "window.BengalTOC" in toc_js

    assert "const SELECTOR_TABS = '.tabs, .code-tabs';" in tabs_js
    assert "data-tab-target" in tabs_js
    assert "data-sync-value" in tabs_js
    assert "window.BengalTabs" in tabs_js

    assert "components/tabs-native.css" in style
    assert "components/search-modal.css" in style
    assert "components/toc.css" in style


def test_chirp_theme_does_not_ship_legacy_palette_aliases() -> None:
    """The bespoke theme should not ship or import old Bengal palette aliases."""
    package_root = resources.files(THEME_PACKAGE)
    css_root = package_root / "assets" / "css"
    style = (css_root / "style.css").read_text(encoding="utf-8")
    palette_root = css_root / "tokens" / "palettes"
    css_files = {
        rel_path: resource.read_text(encoding="utf-8")
        for rel_path, resource in _iter_resource_files(css_root)
        if rel_path.endswith(".css")
    }

    assert "tokens/palettes/" not in style
    if palette_root.is_dir():
        assert not [rel_path for rel_path, _resource in _iter_resource_files(palette_root)]
    for css in css_files.values():
        assert "data-palette" not in css
        assert "snow-lynx" not in css
        assert "brown-bengal" not in css
        assert "silver-bengal" not in css
        assert "charcoal-bengal" not in css
        assert "blue-bengal" not in css


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
    assert "../../../../chirp_ui/templates/chirpui.css" not in style
    assert "../../../../chirp_ui/templates/chirpui-transitions.css" not in style


def test_chirp_theme_css_avoids_bengal_minifier_spacing_regression() -> None:
    """Theme CSS should stay valid when Bengal minifies modern custom-property values."""
    from bengal.css.minify import minify_css

    package_root = resources.files(THEME_PACKAGE)
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")

    minified = minify_css(css)
    broken_scrollbar_value = re.compile(
        r"scrollbar-color:[^;]*(?:var\(--chirpui-accent\)34%|\)transparent)"
    )

    assert not broken_scrollbar_value.search(minified)
    assert "scrollbar-color:#0e7490 transparent" in minified
    assert "scrollbar-color:#2dd4bf transparent" in minified
    assert "color-mix(in srgb" in minified
    assert "calc(" in minified


def test_bengal_minifier_preserves_chirpui_scope_envelope() -> None:
    """Production CSS minification must not glue `@scope (...) to (` (#247 / bengal#510)."""
    from bengal.css.minify import minify_css

    envelope = (
        "@layer chirpui.component {\n"
        "  @scope (.chirpui-card) to (.chirpui-card .chirpui-card) {\n"
        "    :scope { padding: var(--chirpui-spacing); }\n"
        "  }\n"
        "}"
    )
    minified = minify_css(envelope)

    assert "to(" not in minified
    assert re.search(r"@scope\s*\(.+\)\s+to\s+\(", minified)
    assert ":scope{padding:" in minified.replace(" ", "")

    library_css = (
        Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "chirpui.css"
    ).read_text(encoding="utf-8")
    minified_library = minify_css(library_css)

    assert "@scope" in minified_library
    assert " to " in minified_library or " to(" not in minified_library
    assert ".chirpui-card" in minified_library
    assert ":scope" in minified_library


def test_theme_manifest_declares_standalone_package() -> None:
    """The packaged theme manifest should not inherit Bengal default anymore."""
    package_root = resources.files(THEME_PACKAGE)
    manifest_text = (package_root / "theme.toml").read_text(encoding="utf-8")

    assert 'name = "chirp-theme"' in manifest_text
    assert 'libraries = ["chirp_ui"]' in manifest_text
    assert "extends" not in manifest_text


def test_chirp_theme_base_uses_bespoke_chirpui_shell_spine() -> None:
    """The primary shell should be a custom Chirp UI composition, not default-theme nav."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    assets_root = package_root / "assets"
    base = (templates_root / "base.html").read_text(encoding="utf-8")
    css = _unwrap_theme_layer((assets_root / "css" / "chirp-theme.css").read_text(encoding="utf-8"))
    style = (assets_root / "css" / "style.css").read_text(encoding="utf-8")

    assert 'from "chirpui/navbar.html" import navbar, navbar_link, navbar_dropdown' in base
    assert 'from "chirpui/site_footer.html" import site_footer, footer_column, footer_link' in base
    assert "render_navbar_item" in base
    assert "library_asset_tags()" in base
    assert "library_asset_tags | default(none)" in base
    assert "_chirpAlpineData" in base
    assert base.index("_chirpAlpineData") < base.index("{{ library_asset_tags() }}")
    assert "alpinejs@3.15.8/dist/cdn.min.js" in base
    assert base.index("{{ library_asset_tags() }}") < base.index("alpinejs@3.15.8/dist/cdn.min.js")
    assert "chirpui_asset_path('chirpui.css')" not in base
    assert "chirpui_asset_path('chirpui-transitions.css')" not in base
    assert "chirpui_asset_path('chirpui.js')" not in base
    assert "chirpui_asset_path('chirpui-alpine.js')" not in base
    assert 'data-chirp-theme-spine="bespoke"' in base
    assert "_page_url == '/releases/' or _page_url.startswith('/releases/')" in base
    assert "asset_url('favicon.svg')" in base
    assert "asset_url('favicon-32x32.png')" in base
    assert "asset_url('apple-touch-icon.png')" in base
    assert "asset_url('site.webmanifest')" in base
    assert "chirp-theme-shell__desktop-nav" in base
    assert "chirp-theme-shell__mega" in base
    assert "chirp-theme-shell__mega-item" in base
    assert "chirp-theme-shell__main" in base
    assert "partials/site-footer.html" in base
    site_footer = (templates_root / "partials" / "site-footer.html").read_text(encoding="utf-8")
    assert "call site_footer" in site_footer
    assert "chirp-theme-footer__logo" in site_footer
    assert '<span class="chirp-theme-footer__mark" aria-hidden="true">ᗢ</span>' in site_footer
    assert '<ul class="nav-main hidden-mobile">' not in base
    assert '<footer class="chirp-theme-footer" role="contentinfo">' not in base

    assert ".chirp-theme-shell {" in css
    assert ".chirp-theme-shell__nav" in css
    assert ".chirp-theme-shell__nav {\n  display: flex;" in css
    assert "flex-wrap: nowrap;" in css
    assert (
        ".chirp-theme-shell__nav > .chirpui-navbar__links:not(.chirpui-navbar__links--end)" in css
    )
    assert ".chirp-theme-shell__nav > .chirpui-navbar__links--end" in css
    assert ".chirp-theme-shell__nav-dropdown {\n  position: relative;" in css
    assert ".chirp-theme-shell__mega {" in css
    assert ".chirp-theme-shell__nav-dropdown:hover > .chirpui-navbar-dropdown__menu" in css
    assert ".chirp-theme-shell__nav-dropdown > .chirpui-navbar-dropdown__trigger::after" in css
    assert ".chirp-theme-shell .chirpui-navbar__links" not in css
    assert ".chirp-theme-footer.chirpui-site-footer" in css
    assert "components/docs-nav.css" not in style
    assert "../../../../chirp_ui/templates/chirpui.css" not in style
    assert "../../../../chirp_ui/templates/chirpui-transitions.css" not in style

    favicon = (assets_root / "favicon.svg").read_text(encoding="utf-8")
    webmanifest = json.loads((assets_root / "site.webmanifest").read_text(encoding="utf-8"))
    assert "<title>chirp-ui</title>" in favicon
    assert ">ᗢ</text>" in favicon
    assert webmanifest["name"] == "chirp-ui"
    assert webmanifest["theme_color"] == "#071312"
    assert "/android-chrome-" not in json.dumps(webmanifest)


def test_theme_toml_declares_minimum_bengal_version() -> None:
    """#154 — theme.toml must declare the Bengal floor BOTH ways so resolution can
    warn/refuse on too-old Bengal (the bd4e298 regression class).

    The theme's whole chirp-ui CSS/JS load goes through Bengal's
    ``library_asset_tags()`` (>= 0.3.3). Declare the floor as the top-level
    ``requires_bengal`` string AND a ``[bengal] min_version`` table so whichever
    key Bengal's theme resolver reads finds it.
    """
    data = tomllib.loads(THEME_TOML.read_text(encoding="utf-8"))

    assert data.get("requires_bengal") == ">=0.3.3", (
        'theme.toml must declare requires_bengal = ">=0.3.3" (#154)'
    )
    assert data.get("bengal", {}).get("min_version") == "0.3.3", (
        'theme.toml must declare [bengal] min_version = "0.3.3" (#154)'
    )


def test_base_template_emits_loud_library_asset_fallback() -> None:
    """#154 — the library_asset_tags() guard must NOT silently no-op on old Bengal.

    Under Bengal < 0.3.3 ``library_asset_tags`` is undefined and the guard is
    falsy; the {% else %} branch must emit a dev-visible diagnostic that names the
    >= 0.3.3 floor instead of shipping a token-less style-only build.
    """
    base = BASE_TEMPLATE.read_text(encoding="utf-8")

    # The happy path stays.
    assert "library_asset_tags | default(none)" in base
    assert "library_asset_tags()" in base

    # The missing-provider path is a real, named diagnostic — not an empty no-op.
    else_index = base.index("{% if library_asset_tags | default(none) %}")
    block = base[else_index:]
    block = block[: block.index("{% end %}") + len("{% end %}")]
    assert "{% else %}" in block, "library_asset_tags guard has no {% else %} branch (#154)"
    fallback = block[block.index("{% else %}") :]
    # Names the Bengal floor so the failure is self-explaining.
    assert "Bengal >= 0.3.3" in fallback or "bengal>=0.3.3" in fallback, fallback
    assert "library_asset_tags" in fallback, fallback
    assert "--chirpui-" in fallback, fallback
    # The diagnostic is an HTML comment so it never paints but is visible in
    # devtools / view-source.
    assert "<!--" in fallback, fallback
    assert "-->" in fallback, fallback


def test_base_template_gates_d3_preconnect_behind_graph_feature() -> None:
    """#157 — the d3js.org preconnect is contacted only by graph pages, so it must
    be gated behind the graph feature flag, not emitted unconditionally.

    The jsdelivr preconnect stays unconditional (it serves chirp-ui/Alpine/katex
    CDNs), but d3 is a graph-only third party.
    """
    base = BASE_TEMPLATE.read_text(encoding="utf-8")

    assert 'href="https://d3js.org"' in base, "d3 preconnect should still exist (gated) (#157)"

    # Find the d3 preconnect line and assert it sits inside a graph-feature gate.
    d3_index = base.index('href="https://d3js.org"')
    preceding = base[:d3_index]
    last_if = preceding.rindex("{% if ")
    gate = base[last_if:d3_index]
    assert "graph." in gate, (
        "d3 preconnect must be gated behind a graph.* feature flag, not emitted "
        f"unconditionally (#157). Gate seen: {gate!r}"
    )
    assert "theme.features" in gate, gate


def test_base_template_loads_style_css_non_render_blocking() -> None:
    """#157 — style.css must load via preload+onload swap with a <noscript> fallback,
    not as a synchronous render-blocking <link rel=stylesheet>.

    First paint should not wait on the full theme bundle; the FOUC theme-guard
    script stays synchronous independently.
    """
    base = BASE_TEMPLATE.read_text(encoding="utf-8")

    # The async pattern: rel=preload as=style, flipped to a real stylesheet onload.
    preload_link = next(
        (line for line in base.splitlines() if 'rel="preload"' in line and 'as="style"' in line),
        None,
    )
    assert preload_link is not None, "no <link rel=preload as=style> for style.css (#157)"
    assert "css/style.css" in preload_link or "_style_href" in preload_link, preload_link
    assert "onload=" in preload_link, preload_link
    assert "this.rel='stylesheet'" in preload_link, preload_link

    # A JS-less fallback keeps the stylesheet render-blocking when JS is off.
    assert '<noscript><link rel="stylesheet"' in base, (
        "no <noscript> render-blocking fallback for style.css (#157)"
    )

    # The old unconditional synchronous link is gone for good.
    assert '<link rel="stylesheet" href="{{ asset_url(\'css/style.css\') }}">' not in base, (
        "style.css still loads as a synchronous render-blocking <link> (#157)"
    )


def _built_index_html():
    """The built home page, if the site has been built (else None)."""
    page = SITE_ROOT / "public" / "index.html"
    return page.read_text(encoding="utf-8") if page.is_file() else None


def test_built_home_gates_d3_preconnect_with_graph_feature_on() -> None:
    """#157 — with graph.contextual enabled in the docs site config, the built home
    page emits the d3 preconnect (proving the gate's ON path).

    The OFF path is covered by the template-gate test above (the docs site keeps
    graph on, so we cannot exercise both branches from one build); skipped when
    the site is unbuilt — the Gate rebuilds the site before verification.
    """
    html = _built_index_html()
    if html is None:
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    features = (SITE_ROOT / "config" / "_default" / "theme.yaml").read_text(encoding="utf-8")
    graph_on = "graph.contextual" in features or "graph.minimap" in features
    has_d3 = "https://d3js.org" in html
    assert has_d3 == graph_on, (
        "d3 preconnect presence must track the graph feature flag: "
        f"graph_on={graph_on} but d3_in_html={has_d3} (#157)"
    )


def test_built_home_loads_style_css_non_render_blocking() -> None:
    """#157 — the built home page must request style.css via the preload+onload swap
    with a <noscript> fallback (no bare synchronous render-blocking link)."""
    html = _built_index_html()
    if html is None:
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    assert re.search(r'<link[^>]*rel="preload"[^>]*as="style"[^>]*onload=', html), (
        "built home does not load style.css via preload+onload swap (#157)"
    )
    assert "<noscript>" in html, "built home lacks a <noscript> fallback (#157)"
    # Bengal fingerprints assets in built output (style.<hash>.css), so match the
    # stylesheet by stem+extension rather than the literal unhashed filename.
    assert re.search(r"style\.(?:[0-9a-f]+\.)?css", html), (
        "built home does not reference style.css (#157)"
    )


def test_chirp_theme_core_surfaces_have_bespoke_spine_markers() -> None:
    """Core pages should share explicit custom-theme surface hooks."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    assets_root = package_root / "assets"
    expected = {
        "home.html": 'data-chirp-theme-surface="home"',
        "page.html": 'data-chirp-theme-surface="page"',
        "index.html": "data-chirp-theme-surface=\"{{ 'release-list' if is_releases_index else 'section-list' }}\"",
        "doc/home.html": 'data-chirp-theme-surface="doc-home"',
        "doc/list.html": 'data-chirp-theme-surface="doc-list"',
        "doc/single.html": 'data-chirp-theme-surface="doc"',
        "blog/shell.html": "catalog_shell(surface='blog', current_path=_page_url)",
        "search.html": 'data-chirp-theme-surface="search"',
        "404.html": 'data-chirp-theme-surface="error"',
    }

    for template_name, marker in expected.items():
        text = (templates_root / template_name).read_text(encoding="utf-8")
        assert marker in text, f"{template_name} missing {marker}"

    search = (templates_root / "search.html").read_text(encoding="utf-8")
    not_found = (templates_root / "404.html").read_text(encoding="utf-8")
    doc_list = (templates_root / "doc" / "list.html").read_text(encoding="utf-8")
    doc_single = (templates_root / "doc" / "single.html").read_text(encoding="utf-8")
    page = (templates_root / "page.html").read_text(encoding="utf-8")
    blog_shell = (templates_root / "blog" / "shell.html").read_text(encoding="utf-8")
    section_index = (templates_root / "index.html").read_text(encoding="utf-8")
    page_actions = (templates_root / "partials" / "page-actions.html").read_text(encoding="utf-8")
    css = _unwrap_theme_layer((assets_root / "css" / "chirp-theme.css").read_text(encoding="utf-8"))
    interactive_css = (assets_root / "css" / "components" / "interactive.css").read_text(
        encoding="utf-8"
    )
    style = (assets_root / "css" / "style.css").read_text(encoding="utf-8")

    assert 'from "chirpui/hero.html" import page_hero' in search
    assert 'from "chirpui/surface.html" import surface' in search
    assert 'from "chirpui/card.html" import resource_card' in not_found
    assert "chirpui/hero.html" in doc_list
    assert "page_hero" in doc_list
    assert "chirpui/hero.html" in doc_single
    assert "page_hero" in doc_single
    # blog_shell now uses the global catalog shell so layout pages share the
    # same primary navigation rail as documentation and releases.
    for article_template in (doc_list, doc_single, page, section_index):
        assert "chirp-theme-docs-layout" in article_template
        assert "include 'partials/docs-nav.html'" in article_template
    assert "partials/catalog-shell.html" in blog_shell
    catalog_shell = (templates_root / "partials" / "catalog-shell.html").read_text(encoding="utf-8")
    assert "chirp-theme-docs-layout" in catalog_shell
    assert "include 'partials/docs-nav.html'" in catalog_shell
    assert "include 'partials/page-hero.html'" not in doc_list
    assert "include 'partials/page-hero.html'" not in doc_single
    assert 'from "partials/empty-state.html" import empty_state' not in not_found
    assert ".chirp-theme-search__panel" in css
    assert ".chirp-theme-error__panel" in css
    # The bespoke doc hero is now composed via the chirpui page_hero macro with a
    # theme cls (the old partials/page-hero.html + page-hero/_macros.html are gone).
    assert "chirp-theme-docs-layout__hero chirp-theme-doc-hero" in doc_list
    assert "chirp-theme-docs-layout__hero chirp-theme-doc-hero" in doc_single
    assert ".chirp-theme-page-hero" in css
    assert "partials/page-actions.html" in doc_list
    assert "partials/page-actions.html" in doc_single
    assert "page_actions(page)" in doc_list
    assert "page_actions(page)" in doc_single
    assert "chirp-theme-page-actions__trigger" in page_actions
    assert 'data-action="copy-url"' in page_actions
    assert 'data-action="copy-llm-txt"' in page_actions
    assert 'data-ai="{{ ai.id }}"' in page_actions
    assert "ensure_trailing_slash(page_url) ~ 'index.txt'" in page_actions
    # The legacy flat page-hero markup must not reappear in the doc templates that
    # now drive the hero through the chirpui page_hero macro.
    assert "page-hero--chirp" not in doc_list
    assert "page-hero--chirp" not in doc_single
    navigation = (templates_root / "partials" / "navigation-components.html").read_text(
        encoding="utf-8"
    )
    docs_nav = (templates_root / "partials" / "docs-nav.html").read_text(encoding="utf-8")
    assert "chirpui-pagination chirp-theme-pagination" in navigation
    assert "section-navigation" not in navigation
    assert "subsection-card gradient-border fluid-combined" not in navigation
    assert "chirpui-nav-tree toc-sidebar chirp-theme-doc-toc" in navigation
    assert "chirp-theme-doc-toc__context" in navigation
    assert "chirp-theme-doc-toc__context-mark" in navigation
    assert "chirp-theme-doc-toc__context-count" in navigation
    assert "chirp-theme-doc-toc__count-pill" in navigation
    assert "chirp-theme-doc-toc__mark" in navigation
    assert "chirp-theme-page-nav-card--prev" in navigation
    assert "chirp-theme-page-nav-card--next" in navigation
    assert "top_meta_title='Previous page'" in navigation
    assert "top_meta_title='Next page'" in navigation
    # The cd command targets the real sibling path `../<slug>` (no fake
    # human-title-with-spaces); the command text lives in the template, the
    # `$` prompt sigil and the PREV/NEXT direction eyebrow are styled in CSS.
    assert "top_meta='cd ../' ~ (prev_link.slug" in navigation
    assert "top_meta='cd ../' ~ (next_link.slug" in navigation
    assert ".chirp-theme-page-nav-card--prev" in css
    assert 'content: "$ "' in css
    assert 'content: "\\2190  prev"' in css
    assert 'content: "next  \\2192"' in css
    assert "chirpui/workspace_primitives.html" in docs_nav
    assert "chirp-theme-doc-catalog" in docs_nav
    assert "chirp-theme-doc-catalog-rail" in docs_nav
    assert "chirp-theme-doc-catalog-rail__brand-mark" in docs_nav
    assert ">ᗢ</span>" in docs_nav
    assert "def catalog_mark" in docs_nav
    assert "_main_menu" in docs_nav or 'get_menu_lang("main"' in docs_nav
    # Section iconography is centralized in partials/nav-icons.html so the docs
    # catalog rail and the desktop navbar mega-dropdown stay visually consistent
    # (single source of truth). docs-nav.html consumes it via section_icon_name.
    nav_icons = (templates_root / "partials" / "nav-icons.html").read_text(encoding="utf-8")
    assert "def section_icon_name" in nav_icons
    assert "cube" in nav_icons
    assert "book-open" in nav_icons
    assert "rocket" in nav_icons
    assert "from 'partials/nav-icons.html' import section_icon_name" in docs_nav
    assert "icon(_name, size=18)" in docs_nav
    assert "chirp-theme-doc-catalog-rail__label" in docs_nav
    assert "def nav_type_icon" in docs_nav
    assert "icon('folder'" in docs_nav
    assert "icon('article'" in docs_nav
    assert "icon('file-code'" in docs_nav
    assert "nav_type_icon(item_kind, true)" in docs_nav
    assert "chirp-theme-doc-catalog__context" not in docs_nav
    assert "chirp-theme-doc-catalog__context-mark" not in docs_nav
    assert "chirp-theme-doc-catalog__context-meta" not in docs_nav
    assert "chirp-theme-docs-nav__type-icon" in docs_nav
    assert "chirp-theme-docs-nav__summary-link" in docs_nav
    assert "chirp-theme-docs-nav__section-links" in docs_nav
    assert "chirp-theme-docs-nav__root-leaf" in docs_nav
    assert "chirp-theme-docs-nav__meta" not in docs_nav
    assert "chirp-theme-docs-nav__summary-count" not in docs_nav
    assert "chirp-theme-doc-catalog-rail__count" not in docs_nav
    assert "chirp-theme-docs-nav__link--{{ item_kind }}" in docs_nav
    assert "chirp-theme-docs-nav__branch-link" not in docs_nav
    # Disclosure section is an ALWAYS-VISIBLE header row, NOT a native
    # <details>/<summary>. The folder is a real <button> (`__toggle`) and the
    # navigable section label is its SIBLING <a> (`__summary-link`) — neither
    # nests in the other, so axe-core's `nested-interactive` stays clean. The
    # server seeds aria-expanded from is_branch_active so the active trail
    # starts expanded; JS mirrors that into the children region's visibility.
    # The folder glyph swaps closed→open off the button's aria-expanded state.
    assert "<details " not in docs_nav
    assert "chirp-theme-docs-nav__section-header" in docs_nav
    assert "chirp-theme-docs-nav__section--has-toggle" in docs_nav
    assert 'class="chirp-theme-docs-nav__toggle"' in docs_nav
    assert 'type="button"' in docs_nav
    assert "aria-expanded=\"{{ 'true' if is_branch_active else 'false' }}\"" in docs_nav
    assert "aria-controls=" in docs_nav
    assert "chirp-theme-docs-nav__folder--closed" in docs_nav
    assert "chirp-theme-docs-nav__folder--open" in docs_nav
    assert "icon('folder-open'" in docs_nav
    # No native disclosure markup or caret/chevron control.
    assert 'chirp-theme-docs-nav__summary"' not in docs_nav
    assert "icon('caret-right'" not in docs_nav
    assert "chirp-theme-docs-nav__toggle-icon" not in docs_nav
    assert "{% if is_branch_active %} open{% end %}" not in docs_nav
    assert "{{ item_kind_label }}" not in docs_nav
    assert "chirp-theme-release-index" in section_index
    # Sort on the flat `date` attribute: kida's attribute resolver does not descend
    # dotted paths, so "metadata.date,title" silently fell back to title-alpha.
    assert 'sort(attribute="date", reverse=true)' in section_index
    assert "chirp-theme-release-card" in section_index
    assert "grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr))" in css
    assert ".chirp-theme-release-card {\n  display: grid;" in css
    assert "padding: clamp(0.7rem, 1vw, 0.95rem)" in css
    assert ".chirp-theme-release-card .chirpui-card__top-meta" in css
    assert ".chirp-theme-release-card .chirpui-card__main-link" in css
    assert (
        ".chirp-theme-release-card:not(.chirp-theme-release-card--latest) .chirpui-card__header-badges"
        in css
    )
    assert ".chirp-theme-release-card .chirpui-card__body:not(:has(*))" in css
    assert (
        ".chirp-theme-footer--shell .chirpui-site-footer__grid {\n"
        "  grid-template-columns: minmax(13rem, 1.5fr) minmax(8rem, 0.8fr) minmax(7rem, 0.7fr);"
        in css
    )
    assert ".chirp-theme-footer .chirpui-site-footer__list {\n  display: grid;" in css
    assert ".chirp-theme-footer .chirpui-site-footer__link::before" in css
    assert "background-color: color-mix(in srgb, var(--chirpui-accent) 8%, transparent)" in css
    assert "grid-template-columns: 3.5rem minmax(0, 1fr);" in css
    assert ".chirp-theme-doc-catalog-rail__item:hover .chirp-theme-doc-catalog-rail__label" in css
    assert ".chirp-theme-doc-catalog-rail__brand-mark" in css
    assert "box-shadow: 0 1px 0 color-mix(in srgb, var(--chirpui-accent) 10%, transparent)" in css
    assert ".chirp-theme-doc-catalog__context" not in css
    assert ".chirp-theme-doc-catalog__context-mark" not in css
    assert ".chirp-theme-docs-nav__section.is-active" in css
    assert (
        ".chirp-theme-doc-catalog__primary {\n  overflow: visible;\n  border-inline-end: 0;\n  background: transparent;\n}"
        in css
    )
    assert ".chirp-theme-doc-catalog__secondary {\n  max-height: calc(100svh - 2.875rem);" in css
    assert "border-inline-start: 0;\n  background: transparent;" in css
    assert (
        ".chirp-theme-doc-catalog .chirp-theme-docs-nav {\n  width: 100%;\n  padding: 0.4rem;"
        in css
    )
    assert (
        "border: 1px solid color-mix(in srgb, var(--chirpui-accent) 22%, var(--chirpui-border))"
        in css
    )
    assert "border-radius: var(--radius-md)" in css
    assert "color-mix(in srgb, var(--chirpui-surface) 62%, transparent)" in css
    assert (
        ".chirp-theme-docs-nav__section {\n  padding: 0.35rem;\n  border: 1px solid transparent;"
        in css
    )
    assert (
        ".chirp-theme-docs-nav__section.is-active {\n  border-color: transparent;\n  background: transparent;\n}"
        in css
    )
    assert ".chirp-theme-docs-nav__link {\n  display: grid;" in css
    assert '.chirp-theme-docs-nav__link[aria-current="page"]' in css
    assert ".chirp-theme-docs-nav__link--component .chirp-theme-docs-nav__type-icon" in css
    assert ".chirp-theme-docs-nav__summary-link" in css
    assert ".chirp-theme-docs-nav__summary-copy" in css
    assert ".chirp-theme-docs-nav__section-header" in css
    assert ".chirp-theme-docs-nav__section--depth-1 > .chirp-theme-docs-nav__section-header" in css
    assert (
        ".chirp-theme-docs-nav__section--has-toggle > .chirp-theme-docs-nav__section-header" in css
    )
    assert (
        ".chirp-theme-docs-nav__section--has-toggle .chirp-theme-docs-nav__leaf-link:not(.chirp-theme-docs-nav__root-leaf)"
        in css
    )
    assert (
        ".chirp-theme-docs-nav__section--has-toggle > .chirp-theme-docs-nav__section-header "
        + '.chirp-theme-docs-nav__summary-link[aria-current="page"]'
    ) in css
    assert (
        ".chirp-theme-docs-nav__section--has-toggle > .chirp-theme-docs-nav__section-links "
        + "> .chirp-theme-docs-nav__section.chirp-theme-docs-nav__section"
        in css
    )
    assert ".chirp-theme-docs-nav__root-leaf" in css
    assert '.chirp-theme-docs-nav__root-leaf[aria-current="page"]' in css
    assert ".chirp-theme-page-actions__trigger" in css
    assert ".chirp-theme-page-actions__menu:popover-open" in css
    assert ".chirp-theme-page-actions__item" in css
    assert ".chirp-theme-docs-nav__meta" not in css
    assert ".chirp-theme-docs-nav__summary-count" not in css
    assert ".chirp-theme-doc-catalog-rail__count" not in css
    assert "components/docs-nav.css" not in style
    assert ".chirp-theme-docs-layout__hero .chirpui-hero__metadata:not(:has(*))" in css
    assert "scrollbar-color:" in css
    assert "::-webkit-scrollbar-thumb" in css
    assert "max-width: min(68ch, 100%);" in css
    assert ".chirp-theme-docs-layout__content h2" in css
    assert ".chirp-theme-docs-layout__content p > code" in css
    assert ".chirp-theme-doc-catalog__primary {\n  padding: 0.75rem 0.5rem;\n}" in css
    assert ".chirp-theme-docs-layout__sidebar {\n  padding: 0;\n}" in css
    assert "border-inline-end: 1px solid var(--color-border-light)" not in css
    assert "--chirpui-floating-top-left: calc((100vw + 21rem - 14rem) / 2)" in css
    assert ".chirp-theme-doc-toc__context" in css
    assert ".chirp-theme-doc-toc__count-pill" in css
    assert ".chirp-theme-doc-toc summary.toc-group-header:hover .toc-count" in css
    assert ".chirp-theme-doc-toc details.toc-group[open] .toc-count" in css
    assert ".chirp-theme-doc-toc__mark" in css
    assert ".chirp-theme-doc-toc__group[open]" in css
    assert ".chirp-theme-doc-toc__link.toc-link" in css
    assert ".chirp-theme-floating-top.back-to-top" in interactive_css
    assert "left: var(--chirpui-floating-top-left, 50vw)" in interactive_css
    assert ".back-to-top[hidden]" in interactive_css
    assert "width: 100%;" in css
    assert "min-height: calc(100svh - 2.875rem);" in css
    assert "overflow-x: clip;" in css
    assert ".chirp-theme-shell--rail-only .chirp-theme-docs-layout" in css
    assert ".chirp-theme-shell--rail-only .chirp-theme-shell__header" in css
    assert "TRANSITIONAL ASSET SHIM" not in style
    assert "RETAINED LEGACY CSS QUARANTINE" in style
    assert "BESPOKE ACTIVE THEME SURFACE" in style


def test_chirp_theme_blog_and_card_primitives_emit_chirpui_markup() -> None:
    """Blog/card compatibility macros should render through Chirp UI primitives."""
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"
    assets_root = package_root / "assets"

    blog_single = (templates_root / "blog" / "single.html").read_text(encoding="utf-8")
    article = (templates_root / "partials" / "components" / "article.html").read_text(
        encoding="utf-8"
    )
    card_base = (templates_root / "partials" / "components" / "card-base.html").read_text(
        encoding="utf-8"
    )
    author_bio = (templates_root / "partials" / "components" / "author-bio.html").read_text(
        encoding="utf-8"
    )
    blog_share = (
        templates_root / "partials" / "components" / "blog-share-dropdown.html"
    ).read_text(encoding="utf-8")
    social_share = (templates_root / "partials" / "components" / "social-share.html").read_text(
        encoding="utf-8"
    )
    blog_css = (assets_root / "css" / "components" / "blog.css").read_text(encoding="utf-8")
    author_css = (assets_root / "css" / "components" / "author.css").read_text(encoding="utf-8")
    share_css = (assets_root / "css" / "components" / "share.css").read_text(encoding="utf-8")

    assert "chirp-theme-blog-article" in blog_single
    # Guard against the legacy `blog-post` BEM block (renamed to
    # chirp-theme-blog-article). The blog-editorial pass imports
    # partials/components/blog-post-meta.html for the hero byline, whose path
    # legitimately contains the substring "blog-post" — so match the legacy
    # class usage specifically, not the bare substring.
    assert 'class="blog-post' not in blog_single
    assert "blog-post-card" not in blog_single
    assert "{{ blog_post_meta(" in blog_single
    assert "{{ author_bio(" in blog_single
    assert "{{ social_share(" in blog_single
    assert "from 'chirpui/card.html' import resource_card" in article
    assert "chirp-theme-article-card" in article
    assert "article-card gradient-border fluid-combined" not in article
    assert "chirpui-card" in card_base
    assert 'class="card__' not in card_base
    assert "from 'chirpui/card.html' import card" in author_bio
    assert "chirp-theme-author-bio" in author_bio
    assert 'class="author-bio"' not in author_bio
    assert "chirp-theme-blog-share" in blog_share
    assert "page-hero__share" not in blog_share
    assert "chirp-theme-social-share" in social_share
    assert "share-buttons" not in social_share
    assert "onclick=" not in social_share

    assert ".chirp-theme-blog-article" in blog_css
    assert ".blog-post" not in blog_css
    assert ".chirp-theme-author-bio" in author_css
    assert ".author-bio" not in author_css
    assert ".chirp-theme-social-share" in share_css
    assert ".share-button" not in share_css


def test_docs_site_config_points_at_chirp_theme() -> None:
    """The docs site should dogfood the packaged theme by default."""
    theme_config = SITE_ROOT / "config" / "_default" / "theme.yaml"
    site_config = SITE_ROOT / "config" / "_default" / "site.yaml"
    text = theme_config.read_text(encoding="utf-8")
    site_text = site_config.read_text(encoding="utf-8")

    assert 'name: "chirp-theme"' in text
    assert 'logo_text: "ᗢ"' in site_text


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

    # List pages compose page_hero + grid/timeline directly. The resource_index
    # search shell was removed: its GET form is inert on a static build and
    # duplicates the global Cmd+K search (see partials/learning-index.html).
    assert "chirpui/hero.html" in combined
    assert "chirpui/timeline.html" in combined
    assert "chirpui/stepper.html" in combined
    assert "chirpui/rendered_content.html" in combined
    assert "partials/components/post-card.html" in combined
    assert "chirp-theme-learning-hero" in combined
    assert "chirpui/resource_index.html" not in combined
    assert "<script" not in combined
    # Forbid the legacy un-namespaced `track-card` class while allowing the
    # flagship `chirp-theme-track-card` BEM block (#140 Tracks flagship).
    assert 'class="track-card' not in combined
    assert " track-card " not in combined
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
    assert "chirpui/toggle_group.html" in combined
    assert "chirpui/data_table.html" in combined
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
    assert "chirpui/rendered_content.html" in combined
    assert "chirp-theme-reference" in combined
    assert "chirp-theme-reference-hero__summary" in combined
    assert "partials/docs-nav.html" in combined
    assert "kind_icon" in combined
    assert 'data-chirp-theme-surface="api-reference"' in combined
    assert "chirp-theme-docs-layout__sidebar" in combined
    assert "chirp-theme-footer--shell" in combined
    assert "|> markdownify |> safe" in combined
    assert "|> markdownify |> truncatewords_html" in combined
    assert "<script" not in combined
    assert "autodoc-summary-table" not in combined
    assert "autodoc-table" not in combined
    assert "command-card" not in combined

    css = (package_root / "assets" / "css" / "components" / "reference.css").read_text(
        encoding="utf-8"
    )
    assert "grid-template-columns: 1.35rem minmax(0, 1fr) auto" in css
    assert ".chirp-theme-reference-member .chirpui-accordion__trigger::before" in css
    assert ".chirp-theme-reference-member .chirpui-accordion__content" in css
    assert ".chirp-theme-reference-hero__summary > :where(p, ul, ol)" in css
    assert ".chirp-theme-reference-card__description > :where(p, ul, ol)" in css
    assert "margin-inline-start: 0;" in css


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
    assert "partials/docs-nav.html" in combined
    assert 'data-chirp-theme-surface="api-list"' in combined
    assert 'data-chirp-theme-surface="api-reference"' in combined
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
controls_html = (site.output_dir / "docs" / "components" / "controls" / "index.html").read_text(
    encoding="utf-8"
)
home_html = (site.output_dir / "index.html").read_text(encoding="utf-8")
releases_html = (site.output_dir / "releases" / "index.html").read_text(encoding="utf-8")
tags_html = (site.output_dir / "tags" / "index.html").read_text(encoding="utf-8")
tag_html = (site.output_dir / "tags" / "installation" / "index.html").read_text(encoding="utf-8")
legacy_content_tile_re = re.compile(r'class="[^"]*\bcontent-(?:tile|tiles)\b')
nested_resource_grid_re = re.compile(
    r'chirpui-resource-index__results[^>]*>\s*<div class="chirpui-grid'
)
release_titles = [
    item
    for item in re.findall(
        r'class="chirpui-timeline__title[^"]*"[^>]*>([^<]+)<', releases_html
    )
    if item.startswith("chirp-ui ")
]
result_path.write_text(
    json.dumps(
        {
            "has_chirpui_grid": "chirpui-grid" in docs_html,
            "has_chirpui_card": "chirpui-card" in docs_html,
            "docs_section_has_chirpui_sidebar": "chirpui-sidebar" in docs_section_html,
            "docs_section_has_filter_rail": "chirpui-filter-rail" in docs_section_html,
            "docs_section_has_doc_catalog": "chirp-theme-doc-catalog" in docs_section_html,
            "docs_section_has_chirpui_breadcrumbs": "chirpui-breadcrumbs" in docs_section_html,
            "controls_has_component_specimen": "chirp-theme-component-specimen" in controls_html,
            "controls_has_toggle_group": "chirpui-toggle-group" in controls_html,
            "controls_has_data_table": "chirpui-data-table" in controls_html,
            "controls_has_escaped_specimen_markup": bool(
                re.search(r"<pre><code>\\s*&lt;(?:div|label|section|kbd)", controls_html)
            ),
            "controls_has_markdown_blockquote_artifact": "<blockquote>" in controls_html,
            "docs_section_has_bespoke_doc_hero": "chirp-theme-doc-hero" in docs_section_html,
            "docs_section_has_legacy_page_hero_root": 'class="page-hero' in docs_section_html,
            "docs_section_has_legacy_docs_nav": 'class="docs-nav"' in docs_section_html,
            "home_has_chirpui_hero": "chirpui-hero chirpui-hero--page" in home_html,
            "home_has_chirpui_grid": "chirpui-grid" in home_html,
            "home_has_chirpui_resource_card": "chirpui-resource-card" in home_html,
            "home_has_chirpui_bento": "chirpui-bento" in home_html,
            "home_has_chirpui_feature_section": "chirpui-feature-section" in home_html,
            "home_has_chirpui_logo_cloud": "chirpui-logo-cloud" in home_html,
            "home_has_chirpui_story_card": "chirpui-story-card" in home_html,
            "home_has_product_visual": "chirp-theme-home__product-visual" in home_html,
            "home_has_legacy_hero_inner": "chirp-theme-home__hero-inner" in home_html,
            "has_legacy_card_grid": 'class="card-grid"' in docs_html,
            "has_legacy_card": 'class="card"' in docs_html,
            "releases_has_timeline": "chirp-theme-release-timeline" in releases_html,
            "release_titles": release_titles,
            "release_has_custom_entries": "chirp-theme-release-entry" in releases_html,
            "releases_has_install_snippet": "uv add chirp-ui==" in releases_html,
            "releases_no_dead_filter": "chirpui-resource-index" not in releases_html,
            "release_has_nested_resource_grid": bool(nested_resource_grid_re.search(releases_html)),
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
        # ~4.5x the measured ~13-20s child wall time. A wedged Bengal build
        # raises TimeoutExpired (surfacing the child's stderr) instead of
        # stalling CI — the pytest-timeout thread method cannot reap a child.
        timeout=90,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))

    assert result["has_chirpui_grid"]
    assert result["has_chirpui_card"]
    assert result["docs_section_has_chirpui_sidebar"]
    assert result["docs_section_has_filter_rail"]
    assert result["docs_section_has_doc_catalog"]
    assert result["docs_section_has_chirpui_breadcrumbs"]
    assert result["controls_has_component_specimen"]
    assert result["controls_has_toggle_group"]
    assert result["controls_has_data_table"]
    assert not result["controls_has_escaped_specimen_markup"]
    assert not result["controls_has_markdown_blockquote_artifact"]
    assert result["docs_section_has_bespoke_doc_hero"]
    assert not result["docs_section_has_legacy_page_hero_root"]
    assert not result["docs_section_has_legacy_docs_nav"]
    assert result["home_has_chirpui_hero"]
    assert result["home_has_chirpui_grid"]
    assert result["home_has_chirpui_resource_card"]
    assert result["home_has_chirpui_bento"]
    assert result["home_has_chirpui_feature_section"]
    assert result["home_has_chirpui_logo_cloud"]
    assert result["home_has_chirpui_story_card"]
    assert result["home_has_product_visual"]
    assert not result["home_has_legacy_hero_inner"]
    assert not result["has_legacy_card_grid"]
    assert not result["has_legacy_card"]
    # /releases/ now renders the bespoke releases/list.html timeline (install
    # snippets + Latest/Feature/Patch tiers), not the generic index.html card grid.
    assert result["releases_has_timeline"]
    assert result["release_has_custom_entries"]
    assert result["releases_has_install_snippet"]
    assert result["releases_no_dead_filter"]
    assert result["release_titles"][:5] == [
        "chirp-ui 0.11.0",
        "chirp-ui 0.10.0",
        "chirp-ui 0.9.0",
        "chirp-ui 0.8.0",
        "chirp-ui 0.7.0",
    ]
    assert not result["release_has_nested_resource_grid"]
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
        # ~4.5x the measured ~13-20s child wall time. A wedged Bengal build
        # raises TimeoutExpired (surfacing the child's stderr) instead of
        # stalling CI — the pytest-timeout thread method cannot reap a child.
        timeout=90,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    combined_nav = result["header"] + result["mobile"]

    assert result["header"], "Expected built home page to include a header."
    assert result["mobile"], "Expected built home page to include mobile navigation."
    assert 'href=""' not in combined_nav
    assert "Component showcase" in combined_nav
    # The showcase nav link now points at the live Railway-hosted showcase app
    # (feat(showcase): live Railway showcase, #245) rather than the internal
    # /showcase/ route.
    assert "https://chirp-ui-showcase-production.up.railway.app" in combined_nav
    assert "Documentation" in combined_nav
    assert re.search(
        r"""href\s*=\s*(?:"[^"]*docs/"|'[^']*docs/'|[^\s>]*docs/)""",
        combined_nav,
    )


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
        # ~4.5x the measured ~13-20s child wall time. A wedged Bengal build
        # raises TimeoutExpired (surfacing the child's stderr) instead of
        # stalling CI — the pytest-timeout thread method cannot reap a child.
        timeout=90,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))

    assert result["has_404"]
    assert result["has_search"]
    assert "Page Not Found" in result["not_found_html"]
    assert "search-input" in result["search_html"]


def test_docs_site_build_only_references_emitted_assets(tmp_path: Path) -> None:
    """Built docs HTML should only reference asset-managed files that were emitted."""
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
asset_attr_re = re.compile(
    r'''(?:href|src|content)\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+))'''
)


def normalize_referenced_asset(raw):
    asset_path = raw.split("?", 1)[0].split("#", 1)[0]
    if "assets/" not in asset_path:
        return ""
    asset_path = asset_path[asset_path.index("assets/") :].lstrip("/")
    while asset_path.startswith("./"):
        asset_path = asset_path[2:]
    while asset_path.startswith("../"):
        asset_path = asset_path[3:]
    return asset_path

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

manifest = AssetManifest.load(site.output_dir / "asset-manifest.json")
manifest_outputs = {entry.output_path.lstrip("/") for entry in manifest.entries.values()}
standalone_asset_entries = [
    chirpui_asset_path("chirpui.css"),
    chirpui_asset_path("chirpui-transitions.css"),
    chirpui_asset_path("chirpui.js"),
    chirpui_asset_path("chirpui-alpine.js"),
]
expected_asset_entries = [
    *[
        logical_path
        for logical_path in standalone_asset_entries
        if logical_path in manifest.entries
    ],
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
    for match in asset_attr_re.finditer(text):
        raw = html_lib.unescape(next(group for group in match.groups() if group))
        asset_path = normalize_referenced_asset(raw)
        if asset_path:
            referenced_assets.add(asset_path)

missing_manifest_entries = sorted(referenced_assets - manifest_outputs)
stable_library_assets = set()
for logical_path in standalone_asset_entries:
    normalized_path = logical_path.removeprefix("assets/")
    filename = Path(normalized_path).name
    for candidate in {logical_path, f"assets/{normalized_path}", f"assets/{filename}"}:
        if candidate in referenced_assets and (site.output_dir / candidate).is_file():
            stable_library_assets.add(candidate)
# Social / Open Graph cards (assets/social/*) are deliberately served at a
# STABLE, unfingerprinted URL because social scrapers cache by URL — a hashed
# filename would break shared cards on every rebuild. They are therefore
# referenced raw and never appear in the fingerprint asset-manifest. Exclude
# them from the manifest requirement; `missing_files` below still guarantees
# the file is actually emitted to the build.
missing_manifest_entries = [
    path
    for path in missing_manifest_entries
    if path not in stable_library_assets and not path.startswith("assets/social/")
]
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
        # ~4.5x the measured ~13-20s child wall time. A wedged Bengal build
        # raises TimeoutExpired (surfacing the child's stderr) instead of
        # stalling CI — the pytest-timeout thread method cannot reap a child.
        timeout=90,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    referenced_assets = result["referenced_assets"]
    missing_manifest_entries = result["missing_manifest_entries"]
    missing_files = result["missing_files"]
    asset_outputs = result["asset_outputs"]
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


# ---------------------------------------------------------------------------
# Progressive-enhancement registry parity (#148) and lazy-asset wiring (#149)
# ---------------------------------------------------------------------------

# data-bengal values that are handled by a foreign/host registry rather than
# the theme's own bengal-enhance.js (none today). Kept as an explicit, empty
# allowlist so a future host-provided enhancement can be documented here
# instead of silently passing.
_EXTERNAL_DATA_BENGAL: set[str] = set()


def _theme_js_sources() -> dict[str, str]:
    """Map every packaged .js file (posix rel path) to its text, excluding docs."""
    package_root = resources.files(THEME_PACKAGE)
    js_root = package_root / "assets" / "js"
    sources: dict[str, str] = {}
    for rel_path, resource in _iter_resource_files(js_root):
        if rel_path.endswith(".js"):
            sources[rel_path] = resource.read_text(encoding="utf-8")
    return sources


def test_every_data_bengal_value_has_a_registered_enhancement() -> None:
    """Each data-bengal="<name>" in templates must have a Bengal.enhance.register('<name>').

    The progressive-enhancement registry (bengal-enhance.js) is the wired init
    path (loaded in base.html before the enhancement modules). A data-bengal
    hook with no matching register() is a dead declaration: the registry would
    try to lazy-load `<name>.js`, 404, and never enhance the element. This is
    the build-time assertion #148 asks for.
    """
    package_root = resources.files(THEME_PACKAGE)
    templates_root = package_root / "templates"

    # Capture both quoting styles; data-bengal values are simple slugs.
    data_bengal_re = re.compile(r"""data-bengal=["']([a-z0-9][a-z0-9-]*)["']""")
    declared: set[str] = set()
    for rel_path, resource in _iter_resource_files(templates_root):
        if not rel_path.endswith(".html"):
            continue
        declared.update(data_bengal_re.findall(resource.read_text(encoding="utf-8")))

    assert declared, "Expected at least one data-bengal hook in theme templates."

    register_re = re.compile(r"""\.register\(\s*["']([a-z0-9][a-z0-9-]*)["']""")
    registered: set[str] = set()
    for text in _theme_js_sources().values():
        registered.update(register_re.findall(text))

    missing = sorted(declared - registered - _EXTERNAL_DATA_BENGAL)
    assert not missing, (
        "data-bengal hooks with no Bengal.enhance.register('<name>') init path: "
        + ", ".join(missing)
    )


def test_no_dead_spa_navigation_listeners_remain() -> None:
    """Theme JS must not listen for events the theme never dispatches (#148).

    contentLoaded / turbo:* / pjax:* are SPA-framework events (Turbo, PJAX) that
    Bengal does not emit; htmx:afterSwap (handled centrally in bengal-enhance.js)
    is the real dynamic-content hook. Listening for the dead events is misleading
    dead code, so guard against regressions.
    """
    dead_event_re = re.compile(
        r"""addEventListener\(\s*['"](contentLoaded|turbo:[a-z-]+|pjax:[a-z-]+)['"]"""
    )
    offenders: dict[str, list[str]] = {}
    for rel_path, text in _theme_js_sources().items():
        hits = dead_event_re.findall(text)
        if hits:
            offenders[rel_path] = sorted(set(hits))

    assert not offenders, f"Dead SPA-navigation listeners found: {offenders}"


def test_retired_dead_js_modules_are_deleted() -> None:
    """Out-of-scope, template-unreferenced JS subsystems stay deleted (#149)."""
    package_root = resources.files(THEME_PACKAGE)
    retired = [
        ("assets", "js", "enhancements", "holo.js"),
        ("assets", "js", "core", "session-path-tracker.js"),
        ("assets", "js", "enhancements", "data-table.js"),
        ("assets", "js", "vendor", "tabulator.min.js"),
    ]
    present = []
    for parts in retired:
        node = package_root
        for part in parts:
            node = node / part
        if node.is_file():
            present.append("/".join(parts))
    assert not present, f"Retired dead JS modules still shipped: {present}"

    # The Tabulator/data-table wiring must be gone from the live lazy loader too.
    lazy = (package_root / "assets" / "js" / "enhancements" / "lazy-loaders.js").read_text(
        encoding="utf-8"
    )
    assert "tabulator" not in lazy.lower(), "lazy-loaders.js still references Tabulator"
    assert "bengal-data-table-wrapper" not in lazy, (
        "lazy-loaders.js still probes for .bengal-data-table-wrapper"
    )


def test_base_html_lazy_assets_match_enabled_features() -> None:
    """BENGAL_LAZY_ASSETS in base.html carries exactly the keys for live features (#149).

    Mermaid (content.mermaid / content.diagrams) and D3 graphs (graph.contextual /
    graph.minimap) are the surviving lazy features; their asset keys must sit under
    the right feature gate, and the retired Tabulator/data-table keys must be gone.
    """
    package_root = resources.files(THEME_PACKAGE)
    base_html = (package_root / "templates" / "base.html").read_text(encoding="utf-8")

    # The lazy bundle and its gates.
    assert "window.BENGAL_LAZY_ASSETS" in base_html
    assert "_lazy_diagrams = 'content.mermaid' in _ft or 'content.diagrams' in _ft" in base_html
    assert "_lazy_graphs = 'graph.contextual' in _ft or 'graph.minimap' in _ft" in base_html

    # Retired keys/gate are gone.
    assert "_lazy_tables" not in base_html, "Tabulator lazy gate (_lazy_tables) not removed"
    assert "tabulator" not in base_html.lower(), "Tabulator asset key not removed from base.html"
    assert "dataTable" not in base_html, "data-table asset key not removed from base.html"

    # Diagram keys live under the diagrams gate; graph keys under the graphs gate.
    diagrams_block = base_html.split("{% if _lazy_diagrams %}", 1)[1].split("{% end %}", 1)[0]
    assert "mermaidToolbar" in diagrams_block
    assert "mermaidTheme" in diagrams_block

    graphs_block = base_html.split("{% if _lazy_graphs %}", 1)[1].split("{% end %}", 1)[0]
    assert "graphMinimap" in graphs_block
    assert "graphContextual" in graphs_block


def test_mermaid_dogfood_feature_is_enabled() -> None:
    """The site enables content.mermaid so the blog mermaid dogfood renders (#149)."""
    import yaml

    theme_cfg = yaml.safe_load((SITE_ROOT / "config" / "_default" / "theme.yaml").read_text())
    features = theme_cfg["theme"]["features"]
    assert "content.mermaid" in features, (
        "content.mermaid must be enabled so the blog mermaid block gets the lazy "
        "toolbar/theme bundle"
    )

    # The dogfood page that exercises it must still ship a mermaid fence.
    dogfood = SITE_ROOT / "content" / "blog" / "how-a-request-becomes-a-fragment-swap.md"
    assert dogfood.is_file()
    assert "```mermaid" in dogfood.read_text(encoding="utf-8")
