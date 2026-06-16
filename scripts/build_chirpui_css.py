"""Concatenate CSS partials into the shipped ``chirpui.css``.

Pure Python, stdlib only, deterministic. See
``docs/DESIGN-css-registry-projection.md § Decision 3`` for the contract.

Usage
-----
From the repo root::

    python scripts/build_chirpui_css.py        # writes chirpui.css
    python scripts/build_chirpui_css.py --check # exits non-zero if stale

The ``--check`` flag is what CI uses: it regenerates into memory, diffs against
the committed output, and fails with a helpful message if they differ.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_SRC = REPO_ROOT / "src" / "chirp_ui" / "templates" / "css"
OUTPUT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css"

HEADER = """\
/* ============================================================================
 * chirp-ui — GENERATED FILE; do not hand-edit.
 *
 * Source partials: src/chirp_ui/templates/css/
 * Rebuild:         poe build-css   (or python scripts/build_chirpui_css.py)
 *
 * See docs/plans/PLAN-css-scope-and-layer.md for the authoring model.
 * ============================================================================
 */
"""

# Public cascade order. Consumers win without specificity wars by placing their
# rules in a later-declared layer (typically `@layer app.overrides`). See
# docs/CSS-OVERRIDE-SURFACE.md for the contract.
LAYER_DECLARATION = (
    "@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;\n"
)

# Per-partial layer assignment. Partials not listed default to DEFAULT_LAYER.
# The safe baseline for S3 is: everything in `chirpui.component`, utilities in
# `chirpui.utility`. The `reset`/`token`/`base` slots are declared but left
# empty so future cleanup sprints can move rules into them without a behavioral
# flip today. A partial whose body already starts with `@layer` opts out of
# build-time wrapping — that's how S5's @scope envelopes stay local.
DEFAULT_LAYER = "chirpui.component"
LAYER_BY_PARTIAL: dict[str, str] = {
    "partials/037_utilities.css": "chirpui.utility",
    "partials/086_utility-inline-grouping-and-measures.css": "chirpui.utility",
    "partials/087_utility-auto-fill-grid.css": "chirpui.utility",
}


# All partials, discovered in numeric-prefix (filename) order. The NNN_ prefix
# encodes cascade order, so a sorted glob IS the manifest: new partials are
# picked up automatically — no hand-registration, no "forgot to add it to the
# list" drift. LAYER_BY_PARTIAL still assigns non-default layers by name, and a
# partial whose body starts with @layer still opts out of build-time wrapping.
def _discover_partials() -> tuple[str, ...]:
    """Return every partial relative to CSS_SRC, in filename (cascade) order."""
    partials_dir = CSS_SRC / "partials"
    return tuple(f"partials/{path.name}" for path in sorted(partials_dir.glob("*.css")))


MANIFEST: tuple[str, ...] = _discover_partials()


def _wrap_in_layer(body: str, layer: str) -> str:
    """Wrap ``body`` in ``@layer NAME { … }``.

    If the body already starts with ``@layer`` (ignoring leading whitespace and
    comments), return it unchanged — the partial owns its own layering (S5's
    envelope form, or any other explicit author).
    """
    # Skip leading whitespace and CSS comments to check the first real token.
    i = 0
    while i < len(body):
        if body[i].isspace():
            i += 1
            continue
        if body.startswith("/*", i):
            end = body.find("*/", i + 2)
            i = len(body) if end == -1 else end + 2
            continue
        break
    if body[i:].lstrip().startswith("@layer "):
        return body
    # Ensure a trailing newline before the closing brace so it sits on its own line.
    if body and not body.endswith("\n"):
        body += "\n"
    return f"@layer {layer} {{\n{body}}}\n"


def build() -> str:
    """Return the full concatenated stylesheet as a string."""
    parts: list[str] = [HEADER, "\n", LAYER_DECLARATION]
    for rel in MANIFEST:
        path = CSS_SRC / rel
        if not path.is_file():
            raise FileNotFoundError(f"Manifest entry not found: {path}")
        layer = LAYER_BY_PARTIAL.get(rel, DEFAULT_LAYER)
        parts.append(f"\n/* === {rel} === */\n")
        parts.append(_wrap_in_layer(path.read_text(encoding="utf-8"), layer))
    # Single trailing newline, no blank-line drift.
    text = "".join(parts)
    if not text.endswith("\n"):
        text += "\n"
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed output is stale.",
    )
    args = parser.parse_args(argv)

    generated = build()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            sys.stderr.write(
                f"chirpui.css is stale relative to {CSS_SRC.relative_to(REPO_ROOT)}.\n"
                f"Run: poe build-css\n"
            )
            return 1
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
