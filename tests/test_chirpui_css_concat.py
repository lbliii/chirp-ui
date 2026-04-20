"""Ensure the shipped ``chirpui.css`` is in sync with the authoring partials.

The build is pure-Python concat (``scripts/build_chirpui_css.py``). This test
regenerates into memory and diffs against the committed output — if someone
edited a partial but forgot to rebuild, CI catches it here.

See ``docs/PLAN-css-scope-and-layer.md § Sprint 1``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
OUTPUT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css"


def _load_build_module():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import build_chirpui_css  # type: ignore[import-not-found]

    return build_chirpui_css


def test_chirpui_css_matches_partials() -> None:
    build_chirpui_css = _load_build_module()
    generated = build_chirpui_css.build()
    current = OUTPUT.read_text(encoding="utf-8")
    assert generated == current, (
        "chirpui.css is stale. Run `poe build-css` (or "
        "`python scripts/build_chirpui_css.py`) and commit the result."
    )


def test_build_is_deterministic() -> None:
    build_chirpui_css = _load_build_module()
    first = build_chirpui_css.build()
    second = build_chirpui_css.build()
    assert first == second, "concat build must be byte-for-byte deterministic"


def test_layer_declaration_at_top() -> None:
    """The cascade order is part of the public API — first @-rule in the file
    must be the exact declaration documented in docs/CSS-OVERRIDE-SURFACE.md.

    See ``docs/PLAN-css-scope-and-layer.md § Sprint 3 T3.4``.
    """
    build_chirpui_css = _load_build_module()
    text = OUTPUT.read_text(encoding="utf-8")

    expected = (
        "@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;"
    )

    # Walk past comments + whitespace to find the first real rule.
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                break
            i = end + 2
            continue
        break

    first_rule_line = text[i:].split("\n", 1)[0].strip()
    assert first_rule_line == expected, (
        f"First non-comment line must be the layer declaration.\n"
        f"  expected: {expected}\n"
        f"  actual:   {first_rule_line}"
    )

    # Belt-and-braces — the module exports the same string.
    assert build_chirpui_css.LAYER_DECLARATION.strip() == expected
