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
    "base.html",
    "home.html",
    "page.html",
    "doc/home.html",
    "doc/list.html",
    "doc/single.html",
)
CORE_PARITY_TEMPLATES = (
    "blog/shell.html",
    "blog/home.html",
    "blog/list.html",
    "blog/single.html",
    "post.html",
    "search.html",
    "404.html",
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
    "partials/components/tags.html",
    "partials/components/tiles.html",
    "partials/components/related-posts-simple.html",
)
REQUIRED_DIRECTIVE_TEMPLATES = (
    "directives/cards.html",
    "directives/card.html",
    "directives/child_cards.html",
)
ASSET_STRING_RE = re.compile(
    r"""["'](/?assets/[^"'?#]+\.[A-Za-z0-9]+(?:\?[^"']*)?(?:#[^"']*)?)["']"""
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


def test_chirp_theme_docs_frame_owns_grid_layout() -> None:
    """The docs frame class should render as the actual sidebar/content layout."""
    package_root = resources.files(THEME_PACKAGE)
    primitives = (package_root / "templates" / "partials" / "theme-primitives.html").read_text(
        encoding="utf-8"
    )
    css = (package_root / "assets" / "css" / "chirp-theme.css").read_text(encoding="utf-8")

    assert "chirp-theme-docs-layout" in primitives
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


def test_chirp_theme_css_assets_are_reachable_from_style_entrypoint() -> None:
    """The package should not ship copied CSS files outside the active theme graph."""
    package_root = resources.files(THEME_PACKAGE)
    css_root = package_root / "assets" / "css"

    all_css = {
        rel_path
        for rel_path, _resource in _iter_resource_files(css_root)
        if rel_path.endswith(".css")
    }
    reachable, missing = _reachable_css_assets(css_root)
    orphaned = sorted(all_css - reachable)

    assert not missing, "style.css imports missing CSS assets: " + ", ".join(sorted(missing))
    assert not orphaned, "CSS assets are not reachable from style.css: " + ", ".join(orphaned)


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
    ):
        template = engine._env.get_template(template_name)

        assert template is not None
        assert template.filename is not None
        assert THEME_TEMPLATE_PATH_FRAGMENT in template.filename.replace("\\", "/")

    provider_template = engine._env.get_template("chirpui/card.html")
    assert provider_template is not None
    assert "chirp_ui/templates/chirpui/card.html" in provider_template.filename.replace("\\", "/")


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
home_html = (site.output_dir / "index.html").read_text(encoding="utf-8")
releases_html = (site.output_dir / "releases" / "index.html").read_text(encoding="utf-8")
legacy_content_tile_re = re.compile(r'class="[^"]*\bcontent-(?:tile|tiles)\b')
result_path.write_text(
    json.dumps(
        {
            "has_chirpui_grid": "chirpui-grid" in docs_html,
            "has_chirpui_card": "chirpui-card" in docs_html,
            "home_has_chirpui_hero": "chirpui-hero chirpui-hero--page" in home_html,
            "home_has_chirpui_grid": "chirpui-grid" in home_html,
            "home_has_chirpui_resource_card": "chirpui-resource-card" in home_html,
            "home_has_legacy_hero_inner": "chirp-theme-home__hero-inner" in home_html,
            "has_legacy_card_grid": 'class="card-grid"' in docs_html,
            "has_legacy_card": 'class="card"' in docs_html,
            "has_chirpui_resource_card": "chirpui-resource-card" in releases_html,
            "has_legacy_content_tile": bool(legacy_content_tile_re.search(releases_html)),
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
    assert result["home_has_chirpui_hero"]
    assert result["home_has_chirpui_grid"]
    assert result["home_has_chirpui_resource_card"]
    assert not result["home_has_legacy_hero_inner"]
    assert not result["has_legacy_card_grid"]
    assert not result["has_legacy_card"]
    assert result["has_chirpui_resource_card"]
    assert not result["has_legacy_content_tile"]


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
    assert 'href="/showcase/"' in combined_nav
    assert "Documentation" in combined_nav
    assert 'href="/docs/"' in combined_nav


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


@pytest.mark.xfail(reason="chirp-theme asset pipeline not yet complete", strict=False)
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

site_root = Path(sys.argv[1])
result_path = Path(sys.argv[2])
asset_re = re.compile(r'''["'](/?assets/[^"'?#]+\.[A-Za-z0-9]+(?:\?[^"']*)?(?:#[^"']*)?)["']''')

site = Site.from_config(site_root)
site.build(BuildOptions(force_sequential=True, incremental=False, quiet=True))

manifest = AssetManifest.load(site.output_dir / "asset-manifest.json")
manifest_outputs = {entry.output_path.lstrip("/") for entry in manifest.entries.values()}
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

    assert referenced_assets, "Expected built docs HTML to reference packaged theme assets."
    assert not missing_manifest_entries, (
        "Built HTML referenced assets missing from asset-manifest.json: "
        + ", ".join(missing_manifest_entries)
    )
    assert not missing_files, "Built HTML referenced assets missing on disk: " + ", ".join(
        missing_files
    )
