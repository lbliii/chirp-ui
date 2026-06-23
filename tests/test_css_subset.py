"""Tests for manifest-driven CSS subset selection (issue #205)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from chirp_ui.css_subset import (
    DEFAULT_FOUNDATION_PARTIALS,
    CssSubsetPlan,
    resolve_partial_paths,
    validate_component_names,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
FULL_CSS = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css"


def _load_build_module():
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import build_chirpui_css  # type: ignore[import-not-found]

    return build_chirpui_css


def test_foundation_partials_always_included() -> None:
    paths = resolve_partial_paths(("card",))
    assert set(paths) >= DEFAULT_FOUNDATION_PARTIALS


def test_subset_is_smaller_than_full_build() -> None:
    build = _load_build_module()
    subset = build.build(resolve_partial_paths(("card", "btn", "badge", "form", "alert")))
    full = build.build()
    assert len(subset) < len(full)
    # Five components should ship well under half the monolith.
    assert len(subset) < len(full) * 0.5


def test_unknown_component_raises_with_hint() -> None:
    with pytest.raises(KeyError, match="unknown component 'datagrid'"):
        validate_component_names(("datagrid",))


def test_subset_plan_reports_partial_count() -> None:
    plan = CssSubsetPlan.for_components(["data-grid", "btn"])
    assert plan.partial_count >= len(DEFAULT_FOUNDATION_PARTIALS) + 1
    assert plan.estimated_bytes() > 0


def test_resolve_preserves_cascade_order() -> None:
    paths = resolve_partial_paths(("card",))
    names = [p.removeprefix("partials/") for p in paths]
    assert names == sorted(names)
