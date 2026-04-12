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
from pathlib import Path

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
ASSET_STRING_RE = re.compile(r"""["'](/?assets/[^"'?#]+\.[A-Za-z0-9]+(?:\?[^"']*)?(?:#[^"']*)?)["']""")


def _prefer_workspace_bengal() -> None:
    """Force Bengal imports to resolve from a sibling workspace checkout when available."""
    if not _WORKSPACE_BENGAL.exists():
        return

    bengal_parent = _WORKSPACE_BENGAL.parent
    if str(bengal_parent) not in sys.path:
        sys.path.insert(0, str(bengal_parent))

    for module_name in [name for name in sys.modules if name == "bengal" or name.startswith("bengal.")]:
        sys.modules.pop(module_name, None)

    importlib.invalidate_caches()


def _copy_docs_site(root: Path) -> Path:
    site_root = root / "site"
    shutil.copytree(
        SITE_ROOT,
        site_root,
        ignore=shutil.ignore_patterns("public", ".cache", ".bengal-cache", "__pycache__"),
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

    for template_name in (*CANONICAL_TEMPLATES, *CORE_PARITY_TEMPLATES, *REQUIRED_PARTIALS):
        template = engine._env.get_template(template_name)

        assert template is not None
        assert template.filename is not None
        assert THEME_TEMPLATE_PATH_FRAGMENT in template.filename.replace("\\", "/")


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
