"""Tests for the packaged Bengal theme shipped with chirp-ui."""

from importlib import metadata, resources
from pathlib import Path

import pytest

THEME_PACKAGE = "bengal_themes.chirp_theme"
REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"


def test_theme_entry_point_is_registered() -> None:
    """The Bengal theme entry point should resolve to the packaged theme module."""
    entry_points = metadata.entry_points(group="bengal.themes")
    match = next((entry for entry in entry_points if entry.name == "chirp-theme"), None)

    assert match is not None
    assert match.value == THEME_PACKAGE


def test_theme_package_contains_required_resources() -> None:
    """Package resources should include the theme manifest, templates, and assets."""
    package_root = resources.files(THEME_PACKAGE)

    assert (package_root / "theme.toml").is_file()
    assert (package_root / "templates" / "base.html").is_file()
    assert (package_root / "templates" / "home.html").is_file()
    assert (package_root / "templates" / "doc" / "home.html").is_file()
    assert (package_root / "templates" / "doc" / "list.html").is_file()
    assert (package_root / "templates" / "doc" / "single.html").is_file()
    assert (package_root / "assets" / "css" / "chirp-theme.css").is_file()


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
    """The chirp-ui docs site should resolve the packaged theme template surface."""
    pytest.importorskip("bengal")

    from bengal.core import Site
    from bengal.rendering.engines.kida import KidaTemplateEngine

    site = Site.from_config(SITE_ROOT)
    engine = KidaTemplateEngine(site)

    assert site.theme == "chirp-theme"
    assert any("bengal_themes/chirp_theme/templates" in str(path) for path in engine.template_dirs)

    for template_name in (
        "base.html",
        "home.html",
        "page.html",
        "doc/home.html",
        "doc/list.html",
        "doc/single.html",
    ):
        assert engine._env.get_template(template_name) is not None
