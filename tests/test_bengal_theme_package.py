"""Tests for the packaged Bengal theme shipped with chirp-ui."""

import html as html_lib
import re
import shutil
from importlib import metadata, resources
from pathlib import Path

import pytest

THEME_PACKAGE = "bengal_themes.chirp_theme"
THEME_TEMPLATE_PATH_FRAGMENT = "bengal_themes/chirp_theme/templates"
REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
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
ASSET_STRING_RE = re.compile(r"""["'](/?assets/[^"'?#]+\.[A-Za-z0-9]+(?:\?[^"']*)?(?:#[^"']*)?)["']""")


def _copy_docs_site(root: Path) -> Path:
    site_root = root / "site"
    shutil.copytree(
        SITE_ROOT,
        site_root,
        ignore=shutil.ignore_patterns("public", ".cache", ".bengal-cache", "__pycache__"),
    )
    (site_root / "config" / "_default" / "fonts.yaml").write_text("fonts: null\n", encoding="utf-8")
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
    assert (package_root / "assets" / "css" / "style.css").is_file()
    assert (package_root / "assets" / "css" / "chirp-theme.css").is_file()
    assert (package_root / "assets" / "js" / "core" / "theme.js").is_file()
    assert (package_root / "assets" / "icons" / "close.svg").is_file()
    assert (package_root / "assets" / "favicon.svg").is_file()


def test_theme_manifest_declares_standalone_package() -> None:
    """The packaged theme manifest should not inherit Bengal default anymore."""
    package_root = resources.files(THEME_PACKAGE)
    manifest_text = (package_root / "theme.toml").read_text(encoding="utf-8")

    assert 'name = "chirp-theme"' in manifest_text
    assert "extends" not in manifest_text


def test_docs_site_config_points_at_chirp_theme() -> None:
    """The docs site should dogfood the packaged theme by default."""
    theme_config = SITE_ROOT / "config" / "_default" / "theme.yaml"
    text = theme_config.read_text(encoding="utf-8")

    assert 'name: "chirp-theme"' in text


def test_bengal_resolves_packaged_theme() -> None:
    """Bengal should discover chirp-theme through its installed theme registry."""
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
    pytest.importorskip("bengal")

    from bengal.core import Site
    from bengal.rendering.engines.kida import KidaTemplateEngine

    site = Site.from_config(SITE_ROOT)
    engine = KidaTemplateEngine(site)

    assert site.theme == "chirp-theme"
    assert any(THEME_TEMPLATE_PATH_FRAGMENT in str(path) for path in engine.template_dirs)

    for template_name in (*CANONICAL_TEMPLATES, *CORE_PARITY_TEMPLATES, *REQUIRED_PARTIALS):
        template = engine._env.get_template(template_name)

        assert template is not None
        assert template.filename is not None
        assert THEME_TEMPLATE_PATH_FRAGMENT in template.filename.replace("\\", "/")


def test_docs_site_build_only_references_emitted_assets(tmp_path: Path) -> None:
    """Built docs HTML should only reference fingerprinted assets that were emitted."""
    pytest.importorskip("bengal")

    from bengal.assets.manifest import AssetManifest
    from bengal.core import Site
    from bengal.orchestration.build.options import BuildOptions

    site_root = _copy_docs_site(tmp_path)
    site = Site.from_config(site_root)
    site.build(
        BuildOptions(
            force_sequential=True,
            incremental=False,
            quiet=True,
        )
    )

    manifest = AssetManifest.load(site.output_dir / "asset-manifest.json")
    manifest_outputs = {entry.output_path.lstrip("/") for entry in manifest.entries.values()}
    referenced_assets = _iter_local_asset_paths(site.output_dir)
    missing_manifest_entries = sorted(referenced_assets - manifest_outputs)
    missing_files = sorted(
        asset_path for asset_path in referenced_assets if not (site.output_dir / asset_path).is_file()
    )

    assert referenced_assets, "Expected built docs HTML to reference packaged theme assets."
    assert not missing_manifest_entries, (
        "Built HTML referenced assets missing from asset-manifest.json: "
        + ", ".join(missing_manifest_entries)
    )
    assert not missing_files, "Built HTML referenced assets missing on disk: " + ", ".join(
        missing_files
    )
