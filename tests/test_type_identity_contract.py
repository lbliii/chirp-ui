"""Per-surface STRUCTURAL identity contract (color-neutral).

Pure stdlib, source-only (no Playwright, no network, no timing): the assertions
read theme source files and reason about declared CSS / template text, so they
are non-flaky and fingerprint/format-tolerant.

Guards the decisions the identity pass settled on:

1. base.html loads tracks.js inside the site_scripts block (tracks P0 revive).
2. components/type-identity.css is COLOR-NEUTRAL: it must NOT re-point
   --chirpui-accent (or its on-accent / hover / the --type-accent alias) for any
   surface. Every surface keeps the one brand accent (teal) for cohesion. The
   per-type accent-hue experiment was pulled back (it read as disjoint and
   predated the planned light-palette redo); any future color identity must wait
   for the palette work and reference TOKENS, never raw hex.
3. type-identity.css is token-only (no raw hex anywhere).
4. Every surface block sets a --type-measure and is emitted by a template
   (no orphaned structural hooks).
"""

import re
from pathlib import Path

# Reuse the audited block-walker from the token-parity suite so this test reads
# CSS the same way the rest of the theme suite does.
from tests.test_theme_token_parity import _declares, _split_theme_blocks

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "src" / "bengal_themes" / "chirp_theme"
CSS_DIR = THEME / "assets" / "css"
TYPE_IDENTITY_CSS = CSS_DIR / "components" / "type-identity.css"
TRACKS_CSS = CSS_DIR / "components" / "tracks.css"
BASE_HTML = THEME / "templates" / "base.html"
TEMPLATES_DIR = THEME / "templates"

# Surfaces that carry a structural block (reading measure / rhythm). Adding a
# surface later is a one-line change here.
STRUCTURAL_SURFACES = {
    "doc",
    "doc-list",
    "api-reference",
    "api-list",
    "track",
    "blog",
    "release-list",
    "changelog",
    "authors",
    "notebook",
    "resume",
    "tutorial",
}

# Accent/hue properties that type-identity.css must NOT assign — re-pointing any
# of these would re-introduce the per-type color shift we deliberately reverted.
FORBIDDEN_ACCENT_PROPS = (
    "--type-accent",
    "--chirpui-accent",
    "--chirpui-accent-hover",
    "--chirpui-on-accent",
)

_HEX_RE = re.compile(r"#[0-9a-fA-F]{3,6}\b")


def _strip_block_comments(css: str) -> str:
    """Blank out /* … */ comment bodies, preserving newlines so reported line
    numbers stay accurate."""
    return re.sub(
        r"/\*.*?\*/",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        css,
        flags=re.DOTALL,
    )


# --------------------------------------------------------------------------- #
# (1) base.html loads tracks.js inside the site_scripts block
# --------------------------------------------------------------------------- #
def test_base_html_loads_tracks_js_in_site_scripts_block() -> None:
    html = BASE_HTML.read_text(encoding="utf-8")

    needle = "js/enhancements/tracks.js"
    assert needle in html, "base.html must reference js/enhancements/tracks.js"

    open_idx = html.find("{% block site_scripts %}")
    assert open_idx != -1, "base.html must declare a {% block site_scripts %}"

    # Bound the slice by the NEXT `{% block … %}` (or EOF) — a stable upper bound
    # that is line-number/format independent; tracks.js must land inside it.
    after_open = html[open_idx + len("{% block site_scripts %}") :]
    next_block = re.search(r"\{%\s*block\b", after_open)
    block_body = after_open[: next_block.start()] if next_block else after_open
    assert needle in block_body, (
        "tracks.js must be loaded INSIDE the {% block site_scripts %} slice "
        "(it joins the unconditional defer enhancement-module list)"
    )


# --------------------------------------------------------------------------- #
# (2) color-neutral: no per-surface accent re-pointing
# --------------------------------------------------------------------------- #
def test_type_identity_does_not_repoint_accent() -> None:
    """Every surface keeps the one brand accent. type-identity.css must not assign
    --chirpui-accent / --chirpui-on-accent / --chirpui-accent-hover / --type-accent
    on any block — that would re-introduce the reverted per-type color shift."""
    css = TYPE_IDENTITY_CSS.read_text(encoding="utf-8")
    blocks = _split_theme_blocks(css)

    offenders = [
        f"{selector} assigns {prop}"
        for selector, body in blocks.items()
        for prop in FORBIDDEN_ACCENT_PROPS
        if _declares(body, prop) is not None
    ]
    assert not offenders, (
        "type-identity.css must stay color-neutral (one brand accent); "
        "remove these accent assignments: " + "; ".join(offenders)
    )


# --------------------------------------------------------------------------- #
# (3) token-only: no raw hex
# --------------------------------------------------------------------------- #
def test_type_identity_is_token_only_no_raw_hex() -> None:
    no_comments = _strip_block_comments(TYPE_IDENTITY_CSS.read_text(encoding="utf-8"))
    for lineno, line in enumerate(no_comments.splitlines(), start=1):
        assert not _HEX_RE.search(line), (
            f"type-identity.css:{lineno} contains a raw hex color — the file must "
            f"be token-only (use --color-*/--chirpui-*/--type-* refs): {line.strip()!r}"
        )


# --------------------------------------------------------------------------- #
# (4) every structural surface sets a measure
# --------------------------------------------------------------------------- #
def test_every_structural_surface_sets_a_measure() -> None:
    """Each surface's block declares a --type-measure.

    Raw-scan (not the block-walker) because grouped selectors like
    `[…="doc"], […="doc-list"] { … }` share one body, and the block-walker keys a
    group by only its last selector. The surface attr only ever appears in its
    measure block (the shared consumer selects a bare `[data-chirp-theme-surface]`
    child, never `="<surface>"`), so "is --type-measure declared before the next
    closing brace" is an accurate, group-safe check.
    """
    css = TYPE_IDENTITY_CSS.read_text(encoding="utf-8")

    missing: list[str] = []
    for surface in STRUCTURAL_SURFACES:
        idx = css.find(f'[data-chirp-theme-surface="{surface}"]')
        if idx == -1:
            missing.append(surface)
            continue
        close = css.find("}", idx)
        body = css[idx : close if close != -1 else len(css)]
        if "--type-measure" not in body:
            missing.append(surface)
    assert not missing, "structural surfaces missing a --type-measure block: " + ", ".join(
        sorted(missing)
    )


# --------------------------------------------------------------------------- #
# (5) no orphaned surface block — every block is emitted by a template
# --------------------------------------------------------------------------- #
def _emitted_surface_attrs() -> set[str]:
    """Surface names emitted by type templates, covering both literal
    `data-chirp-theme-surface="blog"` and conditional ternary forms inside
    `{{ … }}` (index.html emits release-list that way)."""
    found: set[str] = set()
    literal = re.compile(r'data-chirp-theme-surface="([^"{}]+)"')
    quoted = re.compile(r"""['"]([a-z][a-z0-9-]*)['"]""")
    for path in TEMPLATES_DIR.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        for value in literal.findall(text):
            found.add(value)
        for line in text.splitlines():
            if "data-chirp-theme-surface=" in line and "{{" in line:
                found.update(quoted.findall(line))
    return found


def test_no_orphaned_surface_block() -> None:
    css = TYPE_IDENTITY_CSS.read_text(encoding="utf-8")
    emitted = _emitted_surface_attrs()

    for surface in STRUCTURAL_SURFACES:
        if f'[data-chirp-theme-surface="{surface}"]' in css:
            assert surface in emitted, (
                f"type-identity.css styles surface {surface!r} but no template "
                f'emits data-chirp-theme-surface="{surface}" (orphaned block)'
            )
