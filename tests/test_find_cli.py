"""Tests for ``python -m chirp_ui find`` — Sprint 6.2 of the agent-grounding epic.

The CLI is a thin wrapper around ``chirp_ui.find.search``; tests exercise the
search function directly plus the argparse front door end-to-end.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout

from chirp_ui import load_manifest
from chirp_ui.__main__ import main as dispatch_main
from chirp_ui.find import format_rows, search


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
