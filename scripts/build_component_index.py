"""Regenerate the on-site complete component index.

Issue #166 -- build an on-site component reference catalog so users never leave
for GitHub. The hand-written category table in
``site/content/docs/components/_index.md`` only names a representative subset of
the ~350 public macros in ``manifest.json``. This script emits the *complete*
per-macro index -- every public component grouped by category, with its one-line
description -- so all public components are discoverable on-site without leaving
the theme or running a local app.

"Public" = every component the manifest does **not** mark as ``internal``
(neither ``maturity == "internal"`` nor ``authoring == "internal"``). That is the
composition infrastructure (``fragment-island``, ``suspense-slot``) that is not
an app-level building block; everything else (stable, experimental, legacy) is
public and listed.

The generated block is spliced between
``<!-- chirpui:generated:start -->`` / ``<!-- chirpui:generated:end -->`` markers
in ``site/content/docs/components/all.md``. Hand-authored frontmatter and the
intro above the markers are preserved verbatim.

Pure-Python, stdlib only, deterministic. Mirrors ``scripts/build_manifest.py``
and ``scripts/build_component_options.py`` -- same ``--check`` gate pattern so CI
fails when the committed page drifts from the registry.

The companion drift guard is
``tests/docs_contracts/test_onsite_component_coverage.py``.

Usage
-----
From the repo root::

    python scripts/build_component_index.py          # writes the page
    python scripts/build_component_index.py --check   # exits non-zero if stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from chirp_ui.manifest import build_manifest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "site" / "content" / "docs" / "components" / "all.md"

START_MARKER = "<!-- chirpui:generated:start -->"
END_MARKER = "<!-- chirpui:generated:end -->"

# Frontmatter + intro written when the file does not yet exist. After the first
# run the human-owned region above START_MARKER is preserved verbatim; only the
# generated block between the markers is rewritten.
PREAMBLE = """\
---
title: All components
description: The complete on-site index of every public Chirp UI macro - generated from manifest.json
draft: false
weight: 21
lang: en
type: doc
keywords: [chirp-ui, components, catalog, index, macros, manifest]
tags: [components, reference]
category: components
---

# All components

This is the complete, manifest-backed index of **every public Chirp UI macro** -
grouped by category, each with its one-line description. It is generated from
`src/chirp_ui/manifest.json`, so it can never drift behind the registry: the
[on-site coverage test](https://github.com/lbliii/chirp-ui/blob/main/tests/docs_contracts/test_onsite_component_coverage.py)
fails CI if a public component is missing here.

You never need to leave the site or run a local app to discover a component:

- See any macro rendered in the [component showcase](/showcase/).
- Read every parameter, slot, variant, and maturity in the [API reference](/api/).
- Read the anatomy deep-dives linked from the [component catalog](./).

**Maturity:** `stable` = documented public surface for normal app use;
`experimental` = public but still settling; `legacy` = supported compatibility
surface with a preferred replacement. Components the manifest marks `internal`
(Chirp UI composition infrastructure) are intentionally omitted.
"""

# Human-readable category headings. Any category present in the manifest but
# missing from this map falls back to a title-cased key (and is still emitted,
# so the drift test stays honest).
CATEGORY_TITLES: dict[str, str] = {
    "layout": "Layout",
    "container": "Container",
    "navigation": "Navigation",
    "control": "Control",
    "form": "Form",
    "data-display": "Data display",
    "feedback": "Feedback",
    "interactive": "Interactive",
    "overlay": "Overlay",
    "content": "Content",
    "typography": "Typography",
    "marketing": "Marketing",
    "media": "Media",
    "social": "Social",
    "effect": "Effect",
    "ascii": "ASCII",
    "composite": "Composite",
    "infrastructure": "Infrastructure",
}

# Stable, human-meaningful ordering for the category sections.
CATEGORY_ORDER = [
    "layout",
    "container",
    "navigation",
    "control",
    "form",
    "data-display",
    "feedback",
    "interactive",
    "overlay",
    "content",
    "typography",
    "marketing",
    "media",
    "social",
    "effect",
    "ascii",
    "composite",
]


def is_public(entry: dict) -> bool:
    """Return True when *entry* is part of the public component surface.

    Public = not infrastructure. The manifest marks infrastructure with
    ``maturity == "internal"`` and/or ``authoring == "internal"``.
    """
    return entry.get("maturity") != "internal" and entry.get("authoring") != "internal"


def summary_line(description: str) -> str:
    """Return the first non-empty line of the doc-block as a one-liner."""
    for raw in (description or "").splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def _category_rank(category: str) -> tuple[int, str]:
    try:
        return (CATEGORY_ORDER.index(category), category)
    except ValueError:
        # Unknown categories sort after the known ones, alphabetically.
        return (len(CATEGORY_ORDER), category)


def _render_row(name: str, entry: dict) -> str:
    macro = entry.get("macro") or ""
    macro_cell = f"`{macro}`" if macro else f"`{name}` *(CSS / utility)*"
    maturity = entry.get("maturity") or ""
    summary = summary_line(entry.get("description", ""))
    # Escape pipes so a description never breaks the markdown table.
    summary = summary.replace("|", "\\|")
    if not summary:
        summary = "-"
    return f"| {macro_cell} | {maturity} | {summary} |"


def render_generated_body() -> str:
    manifest = build_manifest()
    components = manifest["components"]
    public = {name: entry for name, entry in components.items() if is_public(entry)}

    # Group by category.
    by_category: dict[str, list[str]] = {}
    for name, entry in public.items():
        by_category.setdefault(entry.get("category") or "other", []).append(name)

    out: list[str] = []
    out.append(f"_{len(public)} public components across {len(by_category)} categories._")
    out.append("")

    for category in sorted(by_category, key=_category_rank):
        names = sorted(by_category[category])
        title = CATEGORY_TITLES.get(category, category.replace("-", " ").title())
        out.append(f"## {title}")
        out.append("")
        out.append(f"_{len(names)} components._")
        out.append("")
        out.append("| Macro | Maturity | Description |")
        out.append("|-------|----------|-------------|")
        out.extend(_render_row(name, public[name]) for name in names)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _splice(existing: str, generated_body: str) -> str:
    """Insert (or replace) the generated block, preserving the human region."""
    block = f"{START_MARKER}\n{generated_body}{END_MARKER}\n"

    if START_MARKER in existing and END_MARKER in existing:
        before, _, rest = existing.partition(START_MARKER)
        _, _, after = rest.partition(END_MARKER)
        after = after.lstrip("\n")
        new = before.rstrip() + "\n\n" + block
        if after:
            new += "\n" + after
        return new

    trimmed = existing.rstrip()
    return f"{trimmed}\n\n{block}"


def build() -> str:
    """Return the full updated all.md text."""
    existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else PREAMBLE
    return _splice(existing, render_generated_body())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the committed component index page is stale.",
    )
    args = parser.parse_args(argv)

    generated = build()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            sys.stderr.write(
                f"{OUTPUT.relative_to(REPO_ROOT)} is stale relative to the manifest.\n"
                f"Run: poe build-component-index\n"
            )
            return 1
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
