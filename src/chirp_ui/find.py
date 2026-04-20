"""Fuzzy component discovery over the shipped manifest — ``python -m chirp_ui find``.

Sprint 6 of the agent-grounding-depth epic. The manifest is the registry
projection; this module turns it into a one-liner for humans and agents who
know *what* they want but not the exact BEM block name.

Search model
------------

A component matches a query when the query is a case-insensitive substring of
any of:

* ``name`` — the manifest key, e.g. ``metric-card``
* ``block`` — the BEM block, e.g. ``metric-card`` (usually same as name)
* ``category`` — e.g. ``data-display``, ``feedback``
* ``description`` — the ``{#- chirp-ui: ... -#}`` doc-block text

Query filters (``--category`` etc.) are applied AFTER substring match, so
``find --category=feedback`` lists every component in that category even when
no term is given.

Output
------

One line per hit, stable/sorted::

    {name:<30} {category:<16} {first-line-of-description}

Exit code ``0`` always (including zero hits) — this is discovery, not
validation.

See ``docs/plans/PLAN-agent-grounding-depth.md § Sprint 6``.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from typing import Any

from chirp_ui import load_manifest


def _summary(description: str) -> str:
    for raw in description.splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def _matches(entry: dict[str, Any], name: str, query: str, category: str | None) -> bool:
    if category and (entry.get("category") or "") != category:
        return False
    if not query:
        return True
    q = query.casefold()
    haystack = " ".join(
        [
            name,
            entry.get("block") or "",
            entry.get("category") or "",
            entry.get("description") or "",
        ]
    ).casefold()
    return q in haystack


def search(
    manifest: dict[str, Any],
    query: str = "",
    *,
    category: str | None = None,
) -> list[tuple[str, str, str]]:
    """Return ``(name, category, summary)`` rows sorted by name."""
    components = manifest.get("components", {})
    rows: list[tuple[str, str, str]] = []
    for name in sorted(components):
        entry = components[name]
        if not _matches(entry, name, query, category):
            continue
        rows.append((name, entry.get("category") or "", _summary(entry.get("description") or "")))
    return rows


def format_rows(rows: Iterable[tuple[str, str, str]]) -> str:
    """Format rows as an aligned three-column table (no header)."""
    rows = list(rows)
    if not rows:
        return ""
    name_w = max(len(r[0]) for r in rows)
    cat_w = max(len(r[1]) for r in rows)
    lines = [f"{name:<{name_w}}  {cat:<{cat_w}}  {summary}" for name, cat, summary in rows]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m chirp_ui find",
        description="Search the chirp-ui component manifest by name, category, or description.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Substring to match against name, block, category, or description (case-insensitive).",
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Filter to a single category (e.g. data-display, feedback, layout).",
    )
    args = parser.parse_args(argv)

    rows = search(load_manifest(), args.query, category=args.category)
    if rows:
        sys.stdout.write(format_rows(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
