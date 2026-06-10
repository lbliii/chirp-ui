"""Packaging + icon-reference guards for the shipped Bengal ``chirp-theme``.

These tests are the regression floor for two classes of defect that the
pre-1.0 productization saga (#150 / #155) had to clean up by hand:

* **Shipped cruft** — ``[tool.setuptools.package-data]`` declares
  ``"bengal_themes.chirp_theme" = ["assets/**/*"]``, a recursive glob that
  happily swept ``assets/icons_backup/`` (39 scratch SVGs) and a stray
  ``assets/COMPONENT-PATTERNS.md`` into every wheel. Both were removed; this
  module fails the build if any backup/scratch directory or non-asset document
  reappears under the shipped assets root.

* **Dangling icon references** — content sections (``:icon:`` frontmatter) and
  theme templates (``icon('name')``) both resolve a bare name to
  ``assets/icons/<name>.svg``. A typo or a removed glyph produces a silent
  "missing icon" build warning and a bare-text rail in the UI (the
  ``panels-top-left`` / ``layout-template`` regression). The icon-reference
  guard walks every reference and asserts each one resolves to a shipped SVG.

The icon guard is intentionally strict: it reflects the *post-fix* tree where
every referenced icon name maps to a real glyph. New content/templates that
introduce an icon name must ship (or repoint to) a real SVG.
"""

from __future__ import annotations

import re
from importlib import resources
from pathlib import Path

import pytest

THEME_PACKAGE = "bengal_themes.chirp_theme"
REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT = REPO_ROOT / "site" / "content"

# Extensions we consider legitimate static *assets* (anything a browser would
# actually fetch from the theme's assets root). Anything else under assets/ is
# treated as shipped cruft.
ASSET_EXTENSIONS = {
    ".css",
    ".js",
    ".mjs",
    ".cjs",
    ".map",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".avif",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".json",
    ".webmanifest",
    ".txt",
    ".xml",
}

# The theme historically co-locates authoring notes (README / design-system
# writeups) next to the CSS and JS they describe. Those are a pre-existing,
# broader cleanup that #155 did *not* scope (the issue called out exactly
# ``COMPONENT-PATTERNS.md`` and ``icons_backup/``); they are not packaging
# cruft of the kind this guard exists to stop. We allowlist the *known* in-tree
# docs so the guard fails on any *new* doc-shaped file (the regression we care
# about) while staying green on the pre-existing set, which a future
# packaging-narrowing pass can prune.
#
# Explicitly NOT allowlisted — these must never ship again (#155):
#   - COMPONENT-PATTERNS.md (was at the assets root)
#   - anything under a *_backup / scratch dir (covered separately below)
ALLOWED_MARKDOWN = {
    "icons/README.md",
    "css/README.md",
    "css/CSS_ARCHITECTURE_EVALUATION.md",
    "css/CSS_QUICK_REFERENCE.md",
    "css/CSS_SCOPING_RULES.md",
    "css/MODULAR_CSS_RATIONALE.md",
    "css/MOTION_DESIGN_SYSTEM.md",
    "css/RESPONSIVE_DESIGN_SYSTEM.md",
    "css/TYPOGRAPHY_MIGRATION.md",
    "css/TYPOGRAPHY_SYSTEM.md",
    "css/utilities/smooth-animations.md",
    "js/README.md",
    "js/IMPROVEMENTS.md",
    "js/enhancements/README.md",
}

# Documentation that the saga removed from shipped assets and must stay gone.
FORBIDDEN_SHIPPED_DOCS = ("COMPONENT-PATTERNS.md",)

# Directory-name patterns that must never ship inside the theme assets.
# (``.DS_Store`` and other stray files are caught by the non-asset guard below.)
CRUFT_DIR_PATTERNS = (
    re.compile(r".*_backup$"),
    re.compile(r".*-backup$"),
    re.compile(r"^backup$"),
    re.compile(r"^scratch$"),
    re.compile(r"^tmp$"),
    re.compile(r"^old$"),
)

# Literal ``icon('name')`` / ``icon("name")`` references in theme templates.
TEMPLATE_ICON_RE = re.compile(r"""icon\(\s*['"]([a-z0-9][a-z0-9_-]*)['"]""")

# ``:icon: name`` (directive option) and ``icon: name`` (YAML frontmatter)
# references in content markdown. We only match bare names so we never trip on
# inline HTML / shortcodes that happen to contain the word "icon".
CONTENT_ICON_RE = re.compile(r"""(?m)^\s*:?icon:\s*["']?([a-z0-9][a-z0-9_-]*)["']?\s*$""")


def _theme_root():
    return resources.files(THEME_PACKAGE)


def _shipped_icon_names() -> set[str]:
    """Stems of every SVG shipped under ``assets/icons/``."""
    icons_dir = _theme_root() / "assets" / "icons"
    return {
        entry.name[: -len(".svg")] for entry in icons_dir.iterdir() if entry.name.endswith(".svg")
    }


def _iter_asset_files(root, prefix: str = ""):
    for child in root.iterdir():
        rel = f"{prefix}{child.name}"
        if child.is_dir():
            yield from _iter_asset_files(child, prefix=f"{rel}/")
        else:
            yield rel, child


# ---------------------------------------------------------------------------
# Packaging surface — the theme ships the resources a consumer relies on.
# ---------------------------------------------------------------------------


def test_theme_ships_manifest_templates_and_assets() -> None:
    """The packaged theme exposes its manifest, templates, and assets surface."""
    root = _theme_root()

    assert (root / "theme.toml").is_file(), "theme.toml is the Bengal theme manifest"
    assert (root / "templates" / "base.html").is_file()
    assert (root / "templates" / "doc" / "single.html").is_file()
    assert (root / "assets" / "css" / "style.css").is_file()
    assert (root / "assets" / "icons" / "close.svg").is_file()


def test_theme_assets_ship_no_backup_or_scratch_dirs() -> None:
    """No ``*_backup`` / scratch directory may sneak into the shipped assets.

    Guards #155: ``assets/icons_backup/`` (39 SVGs) used to ride along inside
    every wheel because ``package-data`` globs ``assets/**/*``.
    """
    assets_root = _theme_root() / "assets"
    offenders: list[str] = []

    for rel, _resource in _iter_asset_files(assets_root):
        for segment in rel.split("/")[:-1]:
            if any(pattern.match(segment) for pattern in CRUFT_DIR_PATTERNS):
                offenders.append(rel)
                break

    assert not offenders, (
        "Backup/scratch directories must not ship under the theme assets root "
        "(narrow the package-data glob or delete the directory): " + ", ".join(sorted(offenders))
    )


def test_forbidden_docs_do_not_ship_under_assets() -> None:
    """The docs the saga pulled out of shipped assets stay out (#155)."""
    assets_root = _theme_root() / "assets"
    shipped = {rel for rel, _resource in _iter_asset_files(assets_root)}
    leaked = sorted(rel for rel in shipped if rel.rsplit("/", 1)[-1] in FORBIDDEN_SHIPPED_DOCS)
    assert not leaked, (
        "Documentation removed from shipped assets has reappeared "
        "(move it to docs/ or delete it): " + ", ".join(leaked)
    )


def test_theme_assets_ship_no_new_non_asset_files() -> None:
    """Only browser-fetchable assets (plus known in-tree docs) may ship under assets/.

    Guards #155 against a *new* doc/scratch file riding along on the broad
    ``assets/**/*`` package-data glob. The pre-existing co-located authoring
    docs (CSS/JS design-system writeups) are allowlisted in ``ALLOWED_MARKDOWN``
    — pruning those is a wider packaging-narrowing pass the issue did not scope.
    A new ``.md`` (or any non-asset extension, or a ``.DS_Store``) fails here.
    """
    assets_root = _theme_root() / "assets"
    offenders: list[str] = []

    for rel, _resource in _iter_asset_files(assets_root):
        name = rel.rsplit("/", 1)[-1]
        if name == ".DS_Store":
            offenders.append(rel)
            continue
        suffix = ("." + name.rsplit(".", 1)[-1].lower()) if "." in name else ""
        if rel in ALLOWED_MARKDOWN:
            continue
        if suffix in ASSET_EXTENSIONS:
            continue
        offenders.append(rel)

    assert not offenders, (
        "New non-asset files must not ship under the theme assets root "
        "(move docs to docs/, remove scratch files, or allowlist a deliberate "
        "in-tree note): " + ", ".join(sorted(offenders))
    )


# ---------------------------------------------------------------------------
# Icon-reference guard — every referenced glyph resolves to a shipped SVG.
# ---------------------------------------------------------------------------


def test_template_icon_references_resolve() -> None:
    """Every ``icon('name')`` in a theme template maps to a shipped SVG."""
    have = _shipped_icon_names()
    templates_root = _theme_root() / "templates"
    missing: dict[str, set[str]] = {}

    for rel, resource in _iter_asset_files(templates_root):
        if not rel.endswith(".html"):
            continue
        text = resource.read_text(encoding="utf-8")
        for match in TEMPLATE_ICON_RE.finditer(text):
            name = match.group(1)
            if name not in have:
                missing.setdefault(name, set()).add(rel)

    assert not missing, "Theme templates reference icons with no SVG: " + "; ".join(
        f"{name} (in {', '.join(sorted(files))})" for name, files in sorted(missing.items())
    )


def test_content_icon_frontmatter_references_resolve() -> None:
    """Every ``:icon:`` reference in site content maps to a shipped SVG.

    This is the regression guard for the bare-rail / "N missing icons" build
    warnings: a content section that names a glyph the theme does not ship
    renders bare text in the catalog rail. Both ``panels-top-left`` and
    ``layout-template`` are now real SVGs; any *other* dangling name fails here
    until it is repointed at an existing icon (or the SVG is added).
    """
    have = _shipped_icon_names()
    missing: dict[str, set[str]] = {}

    for md_file in SITE_CONTENT.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        for match in CONTENT_ICON_RE.finditer(text):
            name = match.group(1)
            if name not in have:
                rel = md_file.relative_to(SITE_CONTENT).as_posix()
                missing.setdefault(name, set()).add(rel)

    assert not missing, (
        "Content :icon: frontmatter references icons with no SVG "
        "(repoint to a shipped icon or add the glyph to assets/icons/): "
        + "; ".join(
            f"{name} (in {', '.join(sorted(files))})" for name, files in sorted(missing.items())
        )
    )


@pytest.mark.parametrize("icon_name", ["panels-top-left", "layout-template"])
def test_pattern_section_icons_are_real_svgs(icon_name: str) -> None:
    """The two pattern/baseline section icons resolve to real Phosphor-style SVGs.

    Guards #155: ``patterns/_index.md`` references both ``panels-top-left`` and
    ``layout-template`` for its Workspace Shells / Layout Affinity cards; neither
    SVG existed, so the build warned "2 missing icons" and both cards rendered a
    bare label. They now ship as 256x256, ``currentColor`` Phosphor-style glyphs.
    """
    svg = _theme_root() / "assets" / "icons" / f"{icon_name}.svg"
    assert svg.is_file(), f"{icon_name}.svg must ship under assets/icons/"

    text = svg.read_text(encoding="utf-8")
    assert 'viewBox="0 0 256 256"' in text
    assert "currentColor" in text
    assert "<title>" in text
    assert "width=" not in text
    assert "height=" not in text
