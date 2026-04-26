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
