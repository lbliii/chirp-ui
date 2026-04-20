"""Regenerate the ``API Reference (generated)`` appendix of ``docs/COMPONENT-OPTIONS.md``.

Sprint 5 of the agent-grounding-depth epic. The existing hand-authored file is
3.5k lines of narrative guides + embedded API tables — predominantly
*narrative-with-embedded-API*, not cleanly shreddable. Rather than shred it
section-by-section, we append **one** generated API reference at the end,
wrapped in ``<!-- chirpui:generated:start -->`` / ``<!-- chirpui:generated:end -->``
markers. Hand-authored sections above the markers are preserved verbatim.

Per-component entry (one per manifest key, sorted):

* ``### <name>``
* Description (first line of the template's ``{#- chirp-ui: ... -#}`` doc-block
  when available, else blank)
* ``- Template:`` path
* ``- Macro:`` resolved macro identifier (when extractable)
* Params table (name | required | default?)  — only when ``params`` non-empty
* Slots / Variants / Sizes / Modifiers / Provides / Consumes — one bullet each,
  only when the list is non-empty

Pure-Python, stdlib only, deterministic. Mirrors ``scripts/build_manifest.py``
— same ``--check`` gate pattern so CI fails when the committed doc drifts from
the registry.

Usage
-----
From the repo root::

    python scripts/build_component_options.py          # writes the file
    python scripts/build_component_options.py --check  # exits non-zero if stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from chirp_ui.manifest import build_manifest

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "docs" / "COMPONENT-OPTIONS.md"

START_MARKER = "<!-- chirpui:generated:start -->"
END_MARKER = "<!-- chirpui:generated:end -->"

HEADER = """\
## API Reference (generated)

> Generated from `src/chirp_ui/manifest.json` by `scripts/build_component_options.py`.
> Do not edit this section directly — edit the descriptor in `chirp_ui.components`
> or the template's `{#- chirp-ui: ... -#}` doc-block and re-run `poe build-docs`.
> Hand-authored narrative guides above are the source of truth for intent and
> idioms; this section is the projection of the registry for agent grounding.
"""


def _summary_line(description: str) -> str:
    """Return the first non-empty line of the doc-block as a one-liner."""
    for raw in description.splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def _params_table(params: list[dict]) -> list[str]:
    lines = ["", "| Param | Required | Default |", "|-------|----------|---------|"]
    for p in params:
        required = "yes" if p["is_required"] else "no"
        default = "—" if p["is_required"] else "(has default)"
        lines.append(f"| `{p['name']}` | {required} | {default} |")
    return lines


def _render_component(name: str, entry: dict) -> list[str]:
    lines: list[str] = [f"### `{name}`", ""]
    summary = _summary_line(entry.get("description", ""))
    if summary:
        lines.extend([summary, ""])

    if entry.get("template"):
        lines.append(f"- **Template:** `chirpui/{entry['template']}`")
    if entry.get("macro"):
        lines.append(f"- **Macro:** `{entry['macro']}`")
    if entry.get("category"):
        lines.append(f"- **Category:** `{entry['category']}`")

    list_fields = [
        ("Slots", entry.get("slots") or []),
        ("Variants", entry.get("variants") or []),
        ("Sizes", entry.get("sizes") or []),
        ("Modifiers", entry.get("modifiers") or []),
        ("Provides", entry.get("provides") or []),
        ("Consumes", entry.get("consumes") or []),
    ]
    for label, values in list_fields:
        if not values:
            continue
        rendered = ", ".join(f"`{v or '(default)'}`" for v in values)
        lines.append(f"- **{label}:** {rendered}")

    params = entry.get("params") or []
    if params:
        lines.extend(_params_table(params))

    lines.append("")
    return lines


def _render_generated_body() -> str:
    manifest = build_manifest()
    out: list[str] = [HEADER]
    for name in sorted(manifest["components"]):
        out.extend(_render_component(name, manifest["components"][name]))
    return "\n".join(out).rstrip() + "\n"


def _splice(existing: str, generated_body: str) -> str:
    """Insert (or replace) the generated block in ``existing`` and return the new file.

    If markers are absent, the block is appended to the end with a leading
    ``---`` separator so the narrative section ends cleanly.
    """
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
    return f"{trimmed}\n\n---\n\n{block}"


def build() -> str:
    """Return the full updated COMPONENT-OPTIONS.md text."""
    existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    return _splice(existing, _render_generated_body())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if docs/COMPONENT-OPTIONS.md is stale.",
    )
    args = parser.parse_args(argv)

    generated = build()

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != generated:
            sys.stderr.write(
                f"{OUTPUT.relative_to(REPO_ROOT)} is stale relative to the manifest.\n"
                f"Run: poe build-docs\n"
            )
            return 1
        return 0

    OUTPUT.write_text(generated, encoding="utf-8")
    sys.stdout.write(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(generated):,} bytes)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
