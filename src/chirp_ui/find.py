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

Use ``--authoring=preferred`` to list the registry-blessed primitives agents
should reach for first, or ``--authoring=compatibility`` to audit legacy
helpers retained for existing templates.

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
from chirp_ui.components import COMPONENT_AUTHORING_LEVELS

ComponentEntry = dict[str, Any]
Manifest = dict[str, Any]


def _summary(description: str) -> str:
    for raw in description.splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def _matches(
    entry: dict[str, Any],
    name: str,
    query: str,
    category: str | None,
    authoring: str | None,
) -> bool:
    if category and (entry.get("category") or "") != category:
        return False
    if authoring and (entry.get("authoring") or "") != authoring:
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


def _ensure_manifest(manifest: Manifest | None) -> Manifest:
    return load_manifest() if manifest is None else manifest


def components_by_authoring(
    authoring: str,
    *,
    manifest: Manifest | None = None,
    category: str | None = None,
) -> dict[str, ComponentEntry]:
    """Return manifest component entries with the given authoring hint.

    This is the Python API twin of ``python -m chirp_ui find --authoring=...``.
    It returns a name-keyed dict in sorted order so downstream agents/tools can
    inspect full manifest entries without hand-filtering JSON.
    """
    if authoring not in COMPONENT_AUTHORING_LEVELS:
        allowed = ", ".join(COMPONENT_AUTHORING_LEVELS)
        raise ValueError(f"chirp-ui: authoring must be one of: {allowed}")
    components = _ensure_manifest(manifest).get("components", {})
    matches: dict[str, ComponentEntry] = {}
    for name in sorted(components):
        entry = components[name]
        if (entry.get("authoring") or "") != authoring:
            continue
        if category and (entry.get("category") or "") != category:
            continue
        matches[name] = entry
    return matches


def preferred_components(
    *, manifest: Manifest | None = None, category: str | None = None
) -> dict[str, ComponentEntry]:
    """Return components marked as preferred authoring vocabulary."""
    return components_by_authoring("preferred", manifest=manifest, category=category)


def compatibility_components(
    *, manifest: Manifest | None = None, category: str | None = None
) -> dict[str, ComponentEntry]:
    """Return compatibility components retained for existing or narrow uses."""
    return components_by_authoring("compatibility", manifest=manifest, category=category)


def search(
    manifest: Manifest,
    query: str = "",
    *,
    category: str | None = None,
    authoring: str | None = None,
) -> list[tuple[str, str, str]]:
    """Return ``(name, category, summary)`` rows sorted by name."""
    components = manifest.get("components", {})
    rows: list[tuple[str, str, str]] = []
    for name in sorted(components):
        entry = components[name]
        if not _matches(entry, name, query, category, authoring):
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
    parser.add_argument(
        "--authoring",
        choices=COMPONENT_AUTHORING_LEVELS,
        default=None,
        help="Filter by authoring hint: preferred, available, compatibility, or internal.",
    )
    args = parser.parse_args(argv)

    rows = search(load_manifest(), args.query, category=args.category, authoring=args.authoring)
    if rows:
        sys.stdout.write(format_rows(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
