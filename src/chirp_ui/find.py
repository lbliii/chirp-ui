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
Use ``--maturity=experimental`` to inspect public surfaces still going through
pre-1.0 stabilization, or ``--maturity=stable`` to list normal public
vocabulary.
Use ``--role=pattern`` to inspect recipe-first or pattern-like surfaces without
mixing them into primitive/component searches.

Output
------

Default output is one line per hit, stable/sorted::

    {name:<30} {category:<16} {first-line-of-description}

Use ``--details`` to include the registry metadata agents need when choosing a
surface: role, maturity, authoring, macro, template, runtime requirements, and
slots.

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
from chirp_ui.components import (
    COMPONENT_AUTHORING_LEVELS,
    COMPONENT_MATURITY_LEVELS,
    COMPONENT_ROLES,
)

ComponentEntry = dict[str, Any]
Manifest = dict[str, Any]
SearchRow = tuple[str, str, str]
DetailedSearchRow = tuple[str, str, str, str, str, str, str, str, str, str]


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
    maturity: str | None,
    role: str | None,
) -> bool:
    if category and (entry.get("category") or "") != category:
        return False
    if authoring and (entry.get("authoring") or "") != authoring:
        return False
    if maturity and (entry.get("maturity") or "") != maturity:
        return False
    if role and (entry.get("role") or "") != role:
        return False
    if not query:
        return True
    q = query.casefold()
    haystack = " ".join(
        [
            name,
            entry.get("block") or "",
            entry.get("category") or "",
            entry.get("maturity") or "",
            entry.get("authoring") or "",
            entry.get("role") or "",
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


def components_by_maturity(
    maturity: str,
    *,
    manifest: Manifest | None = None,
    category: str | None = None,
    authoring: str | None = None,
) -> dict[str, ComponentEntry]:
    """Return manifest component entries with the given maturity label."""
    if maturity not in COMPONENT_MATURITY_LEVELS:
        allowed = ", ".join(COMPONENT_MATURITY_LEVELS)
        raise ValueError(f"chirp-ui: maturity must be one of: {allowed}")
    if authoring and authoring not in COMPONENT_AUTHORING_LEVELS:
        allowed = ", ".join(COMPONENT_AUTHORING_LEVELS)
        raise ValueError(f"chirp-ui: authoring must be one of: {allowed}")
    components = _ensure_manifest(manifest).get("components", {})
    matches: dict[str, ComponentEntry] = {}
    for name in sorted(components):
        entry = components[name]
        if (entry.get("maturity") or "") != maturity:
            continue
        if category and (entry.get("category") or "") != category:
            continue
        if authoring and (entry.get("authoring") or "") != authoring:
            continue
        matches[name] = entry
    return matches


def components_by_role(
    role: str,
    *,
    manifest: Manifest | None = None,
    category: str | None = None,
    maturity: str | None = None,
    authoring: str | None = None,
) -> dict[str, ComponentEntry]:
    """Return manifest component entries with the given role label."""
    if role not in COMPONENT_ROLES:
        allowed = ", ".join(COMPONENT_ROLES)
        raise ValueError(f"chirp-ui: role must be one of: {allowed}")
    if maturity and maturity not in COMPONENT_MATURITY_LEVELS:
        allowed = ", ".join(COMPONENT_MATURITY_LEVELS)
        raise ValueError(f"chirp-ui: maturity must be one of: {allowed}")
    if authoring and authoring not in COMPONENT_AUTHORING_LEVELS:
        allowed = ", ".join(COMPONENT_AUTHORING_LEVELS)
        raise ValueError(f"chirp-ui: authoring must be one of: {allowed}")
    components = _ensure_manifest(manifest).get("components", {})
    matches: dict[str, ComponentEntry] = {}
    for name in sorted(components):
        entry = components[name]
        if (entry.get("role") or "") != role:
            continue
        if category and (entry.get("category") or "") != category:
            continue
        if maturity and (entry.get("maturity") or "") != maturity:
            continue
        if authoring and (entry.get("authoring") or "") != authoring:
            continue
        matches[name] = entry
    return matches


def search(
    manifest: Manifest,
    query: str = "",
    *,
    category: str | None = None,
    authoring: str | None = None,
    maturity: str | None = None,
    role: str | None = None,
) -> list[SearchRow]:
    """Return ``(name, category, summary)`` rows sorted by name."""
    components = manifest.get("components", {})
    rows: list[SearchRow] = []
    for name in sorted(components):
        entry = components[name]
        if not _matches(entry, name, query, category, authoring, maturity, role):
            continue
        rows.append((name, entry.get("category") or "", _summary(entry.get("description") or "")))
    return rows


def _runtime_summary(entry: ComponentEntry) -> str:
    requirements = entry.get("requires") or entry.get("requirements") or entry.get("runtime") or ()
    if not requirements:
        return "-"
    if isinstance(requirements, str):
        return requirements
    return ",".join(str(item) for item in requirements)


def _slot_summary(entry: ComponentEntry) -> str:
    slots = entry.get("slots") or ()
    if not slots:
        return "-"
    rendered = ["default" if slot == "" else str(slot) for slot in slots]
    return ",".join(rendered)


def detailed_search(
    manifest: Manifest,
    query: str = "",
    *,
    category: str | None = None,
    authoring: str | None = None,
    maturity: str | None = None,
    role: str | None = None,
) -> list[DetailedSearchRow]:
    """Return detailed registry rows sorted by name."""
    components = manifest.get("components", {})
    rows: list[DetailedSearchRow] = []
    for name in sorted(components):
        entry = components[name]
        if not _matches(entry, name, query, category, authoring, maturity, role):
            continue
        rows.append(
            (
                name,
                entry.get("category") or "",
                entry.get("maturity") or "",
                entry.get("authoring") or "",
                entry.get("role") or "",
                entry.get("macro") or "-",
                entry.get("template") or "-",
                _runtime_summary(entry),
                _slot_summary(entry),
                _summary(entry.get("description") or ""),
            )
        )
    return rows


def format_rows(rows: Iterable[SearchRow]) -> str:
    """Format rows as an aligned three-column table (no header)."""
    rows = list(rows)
    if not rows:
        return ""
    name_w = max(len(r[0]) for r in rows)
    cat_w = max(len(r[1]) for r in rows)
    lines = [f"{name:<{name_w}}  {cat:<{cat_w}}  {summary}" for name, cat, summary in rows]
    return "\n".join(lines)


def format_detailed_rows(rows: Iterable[DetailedSearchRow]) -> str:
    """Format detailed rows as an aligned table with a header."""
    rows = list(rows)
    if not rows:
        return ""
    headers = (
        "name",
        "category",
        "maturity",
        "authoring",
        "role",
        "macro",
        "template",
        "runtime",
        "slots",
        "summary",
    )
    widths = [
        max(len(str(row[index])) for row in [*rows, headers]) for index in range(len(headers) - 1)
    ]
    header = "  ".join(f"{headers[index]:<{widths[index]}}" for index in range(len(widths)))
    lines = [f"{header}  {headers[-1]}"]
    for row in rows:
        prefix = "  ".join(f"{row[index]!s:<{widths[index]}}" for index in range(len(widths)))
        lines.append(f"{prefix}  {row[-1]}")
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
    parser.add_argument(
        "--maturity",
        choices=COMPONENT_MATURITY_LEVELS,
        default=None,
        help="Filter by maturity label: stable, experimental, legacy, or internal.",
    )
    parser.add_argument(
        "--role",
        choices=COMPONENT_ROLES,
        default=None,
        help="Filter by role: primitive, component, pattern, effect, or infrastructure.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show role, maturity, authoring, macro, template, runtime requirements, and slots.",
    )
    args = parser.parse_args(argv)

    manifest = load_manifest()
    if args.details:
        detailed_rows = detailed_search(
            manifest,
            args.query,
            category=args.category,
            authoring=args.authoring,
            maturity=args.maturity,
            role=args.role,
        )
        if detailed_rows:
            sys.stdout.write(format_detailed_rows(detailed_rows) + "\n")
        return 0

    rows = search(
        manifest,
        args.query,
        category=args.category,
        authoring=args.authoring,
        maturity=args.maturity,
        role=args.role,
    )
    if rows:
        sys.stdout.write(format_rows(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
