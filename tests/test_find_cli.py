"""Tests for ``python -m chirp_ui find`` — Sprint 6.2 of the agent-grounding epic.

The CLI is a thin wrapper around ``chirp_ui.find.search``; tests exercise the
search function directly plus the argparse front door end-to-end.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout

import pytest

from chirp_ui import load_manifest
from chirp_ui.__main__ import main as dispatch_main
from chirp_ui.find import (
    compatibility_components,
    components_by_authoring,
    components_by_maturity,
    components_by_role,
    detailed_search,
    format_detailed_rows,
    format_rows,
    preferred_components,
    search,
)


def test_search_metric_matches_card_and_grid() -> None:
    """Substring query matches both metric-card and metric-grid via name."""
    rows = search(load_manifest(), "metric")
    names = [r[0] for r in rows]
    assert "metric-card" in names
    assert "metric-grid" in names


def test_search_category_filter_returns_feedback_family() -> None:
    """``--category=feedback`` surfaces the canonical feedback components."""
    rows = search(load_manifest(), category="feedback")
    names = {r[0] for r in rows}
    assert {"alert", "badge", "callout"}.issubset(names)
    # Filter is exact match, not substring.
    for _name, category, _summary in rows:
        assert category == "feedback"


def test_search_authoring_filter_returns_preferred_primitives() -> None:
    """``--authoring=preferred`` surfaces the blessed composition vocabulary."""
    rows = search(load_manifest(), authoring="preferred")
    names = [r[0] for r in rows]
    assert names == [
        "actions",
        "block",
        "cluster",
        "container",
        "flow",
        "frame",
        "grid",
        "layer",
        "prose",
        "stack",
    ]


def test_search_authoring_filter_can_combine_with_category() -> None:
    """Authoring hints compose with existing exact category filtering."""
    rows = search(load_manifest(), category="typography", authoring="compatibility")
    names = {r[0] for r in rows}
    assert {"font-sm", "text-muted", "ui-title"}.issubset(names)
    for _name, category, _summary in rows:
        assert category == "typography"


def test_search_maturity_filter_returns_experimental_surface() -> None:
    """``--maturity=experimental`` surfaces components still under stabilization."""
    rows = search(load_manifest(), maturity="experimental")
    names = {r[0] for r in rows}

    assert {"site-shell", "token-input"}.issubset(names)
    assert "stack" not in names


def test_search_maturity_filter_combines_with_authoring() -> None:
    """Maturity and authoring filters compose for registry audits."""
    rows = search(load_manifest(), maturity="legacy", authoring="compatibility")
    names = {r[0] for r in rows}

    assert {"font-sm", "text-muted", "mt-md"}.issubset(names)
    assert all(" " not in name for name in names)


def test_search_role_filter_returns_blessed_primitives() -> None:
    """``--role=primitive`` lets agents inspect primitive vocabulary directly."""
    rows = search(load_manifest(), role="primitive", authoring="preferred")
    names = [r[0] for r in rows]

    assert names == [
        "actions",
        "block",
        "cluster",
        "container",
        "flow",
        "frame",
        "grid",
        "layer",
        "prose",
        "stack",
    ]


def test_search_role_filter_returns_pattern_surfaces() -> None:
    """``--role=pattern`` separates recipe-like surfaces from components."""
    rows = search(load_manifest(), role="pattern")
    names = {r[0] for r in rows}

    assert {"filter-rail", "result-card"}.issubset(names)
    assert "stack" not in names


def test_detailed_search_returns_registry_metadata() -> None:
    """Detailed discovery exposes existing manifest metadata without JSON filtering."""
    rows = detailed_search(load_manifest(), "stack")
    stack = next(row for row in rows if row[0] == "stack")

    assert stack[1] == "layout"
    assert stack[2] == "stable"
    assert stack[3] == "preferred"
    assert stack[4] == "primitive"
    assert stack[5] == "stack"
    assert stack[6] == "layout.html"
    assert stack[7] == "-"
    assert stack[8] == "default"


def test_detailed_search_honors_filters() -> None:
    """Detailed rows use the same category/authoring/maturity filters."""
    rows = detailed_search(
        load_manifest(),
        category="form",
        maturity="experimental",
        authoring="available",
    )
    names = {row[0] for row in rows}

    assert "token-input" in names
    assert "stack" not in names
    assert all(row[1] == "form" for row in rows)
    assert all(row[2] == "experimental" for row in rows)
    assert all(row[3] == "available" for row in rows)


def test_detailed_search_honors_role_filter() -> None:
    rows = detailed_search(load_manifest(), role="primitive", authoring="preferred")

    assert rows
    assert all(row[4] == "primitive" for row in rows)
    assert all(row[3] == "preferred" for row in rows)


def test_preferred_components_returns_manifest_entries() -> None:
    """Python callers can get full preferred entries without filtering JSON."""
    components = preferred_components(manifest=load_manifest())
    assert list(components) == [
        "actions",
        "block",
        "cluster",
        "container",
        "flow",
        "frame",
        "grid",
        "layer",
        "prose",
        "stack",
    ]
    assert components["stack"]["authoring"] == "preferred"
    assert components["stack"]["role"] == "primitive"
    assert components["stack"]["macro"] == "stack"
    assert components["stack"]["params"]


def test_compatibility_components_can_filter_category() -> None:
    """Compatibility helper audits can be sliced by category."""
    components = compatibility_components(manifest=load_manifest(), category="typography")
    assert {"font-sm", "text-muted", "ui-title"}.issubset(components)
    assert all(entry["category"] == "typography" for entry in components.values())


def test_components_by_authoring_rejects_unknown_hint() -> None:
    """Invalid authoring hints fail loudly for Python callers."""
    with pytest.raises(ValueError, match=r"preferred.*compatibility") as exc_info:
        components_by_authoring("recommended", manifest=load_manifest())
    message = str(exc_info.value)
    assert "preferred" in message
    assert "compatibility" in message


def test_components_by_maturity_returns_manifest_entries() -> None:
    """Python callers can inspect maturity groups without filtering JSON."""
    components = components_by_maturity("experimental", manifest=load_manifest())

    assert "token-input" in components
    assert components["token-input"]["maturity"] == "experimental"
    assert all(entry["maturity"] == "experimental" for entry in components.values())


def test_components_by_maturity_can_filter_category_and_authoring() -> None:
    """Maturity audits can be narrowed by category and authoring hint."""
    components = components_by_maturity(
        "legacy",
        manifest=load_manifest(),
        category="typography",
        authoring="compatibility",
    )

    assert {"font-sm", "text-muted", "ui-title"}.issubset(components)
    assert all(entry["category"] == "typography" for entry in components.values())
    assert all(entry["authoring"] == "compatibility" for entry in components.values())


def test_components_by_maturity_rejects_unknown_label() -> None:
    """Invalid maturity labels fail loudly for Python callers."""
    with pytest.raises(ValueError, match=r"stable.*experimental") as exc_info:
        components_by_maturity("ready", manifest=load_manifest())
    message = str(exc_info.value)
    assert "stable" in message
    assert "experimental" in message


def test_components_by_role_returns_manifest_entries() -> None:
    """Python callers can inspect role groups without filtering JSON."""
    components = components_by_role("pattern", manifest=load_manifest())

    assert "result-card" in components
    assert components["result-card"]["role"] == "pattern"
    assert all(entry["role"] == "pattern" for entry in components.values())


def test_components_by_role_can_filter_maturity_and_authoring() -> None:
    components = components_by_role(
        "primitive",
        manifest=load_manifest(),
        maturity="stable",
        authoring="preferred",
    )

    assert "stack" in components
    assert "font-sm" not in components
    assert all(entry["maturity"] == "stable" for entry in components.values())
    assert all(entry["authoring"] == "preferred" for entry in components.values())


def test_components_by_role_rejects_unknown_label() -> None:
    with pytest.raises(ValueError, match=r"primitive.*component") as exc_info:
        components_by_role("widget", manifest=load_manifest())
    message = str(exc_info.value)
    assert "primitive" in message
    assert "component" in message


def test_search_empty_query_lists_every_component() -> None:
    """No query, no filter → row per manifest component."""
    manifest = load_manifest()
    rows = search(manifest, "")
    assert len(rows) == len(manifest["components"])


def test_search_no_match_returns_empty_list() -> None:
    """A query nothing matches yields zero rows, not an error."""
    assert search(load_manifest(), "x-no-such-component-zzz") == []


def test_search_is_case_insensitive() -> None:
    """Query casing doesn't matter — Metric == metric == METRIC."""
    manifest = load_manifest()
    assert [r[0] for r in search(manifest, "METRIC")] == [r[0] for r in search(manifest, "metric")]


def test_search_results_are_sorted_by_name() -> None:
    """Deterministic output — names appear in alphabetical order."""
    rows = search(load_manifest(), "")
    names = [r[0] for r in rows]
    assert names == sorted(names)


def test_format_rows_aligns_columns() -> None:
    """Formatter pads name/category columns so the summary line aligns."""
    rows = [("btn", "control", "Button"), ("metric-card", "data-display", "Metric grid/card")]
    text = format_rows(rows)
    lines = text.splitlines()
    assert len(lines) == 2
    # Name column padded to width of longest name (metric-card → 11 chars).
    assert lines[0].startswith("btn" + " " * 8)


def test_format_rows_handles_empty() -> None:
    assert format_rows([]) == ""


def test_format_detailed_rows_includes_header_and_metadata() -> None:
    rows = detailed_search(load_manifest(), "token-input")
    text = format_detailed_rows(rows)
    lines = text.splitlines()

    assert lines[0].startswith("name")
    assert "maturity" in lines[0]
    assert "authoring" in lines[0]
    assert "runtime" in lines[0]
    assert "slots" in lines[0]
    assert "token-input" in text
    assert "experimental" in text
    assert "input,results,tokens" in text


def test_detailed_rows_use_manifest_requires_for_runtime() -> None:
    rows = detailed_search(load_manifest(), "copy-btn")
    assert rows
    assert rows[0][7] == "alpine"


def test_format_detailed_rows_handles_empty() -> None:
    assert format_detailed_rows([]) == ""


def test_dispatch_find_writes_to_stdout() -> None:
    """``python -m chirp_ui find metric`` → exit 0, non-empty stdout."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "metric"])
    assert rc == 0
    out = buf.getvalue()
    assert "metric-card" in out
    assert "metric-grid" in out


def test_dispatch_find_supports_authoring_filter() -> None:
    """``python -m chirp_ui find --authoring=preferred`` is the agent shortcut."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "--authoring=preferred"])
    assert rc == 0
    out = buf.getvalue()
    assert "stack" in out
    assert "grid" in out
    assert "font-sm" not in out


def test_dispatch_find_supports_maturity_filter() -> None:
    """``python -m chirp_ui find --maturity=experimental`` supports public-surface audits."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "--maturity=experimental"])
    assert rc == 0
    out = buf.getvalue()
    assert "site-shell" in out
    assert not any(line.startswith("stack ") for line in out.splitlines())


def test_dispatch_find_supports_role_filter() -> None:
    """``python -m chirp_ui find --role=pattern`` audits pattern surfaces."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "--role=pattern"])
    assert rc == 0
    out = buf.getvalue()
    assert "filter-rail" in out
    assert "result-card" in out
    assert not any(line.startswith("stack ") for line in out.splitlines())


def test_dispatch_find_supports_details() -> None:
    """``--details`` turns registry metadata into a human/agent-readable table."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "token-input", "--details"])
    assert rc == 0
    out = buf.getvalue()
    assert "maturity" in out
    assert "authoring" in out
    assert "token-input" in out
    assert "experimental" in out
    assert "input,results,tokens" in out


def test_dispatch_find_details_points_agents_at_real_page_primitives() -> None:
    """Page discovery should expose current primitives, not unpromoted proposal names."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "page", "--details"])

    assert rc == 0
    out = buf.getvalue()
    for expected in [
        "page_header",
        "page_hero",
        "page-fill",
        "page_header",
        "layout.html",
        "hero.html",
        "stable",
        "experimental",
    ]:
        assert expected in out

    for unpromoted in [
        "page-actions",
        "compact-page-header",
        "reference-page",
    ]:
        assert unpromoted not in out


def test_dispatch_find_pattern_details_surfaces_reference_building_blocks() -> None:
    """Reference planning can inspect pattern primitives without manifest schema changes."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["find", "--role=pattern", "--details"])

    assert rc == 0
    out = buf.getvalue()
    for expected in [
        "filter-rail",
        "resource-index",
        "result-card",
        "workspace_primitives.html",
        "resource_index.html",
        "experimental",
        "available",
    ]:
        assert expected in out

    assert "data-grid" not in out
    assert "reference-page" not in out


def test_dispatch_help_prints_usage() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main([])
    assert rc == 0
    assert "find" in buf.getvalue()


def test_dispatch_unknown_command_returns_2() -> None:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = dispatch_main(["nonesuch"])
    assert rc == 2
