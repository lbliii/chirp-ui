"""Promotion-readiness ratchets for ASCII/TUI public components."""

from pathlib import Path

from chirp_ui.manifest import build_manifest

ROOT = Path(__file__).resolve().parents[1]
ASCII_TESTS = ROOT / "tests" / "test_ascii_components.py"
BROWSER_TESTS = ROOT / "tests" / "browser" / "test_visual_audit_showcase.py"
SHOWCASE = ROOT / "examples" / "design-system-gap-showcase" / "index.html"
STATIC_DISPLAY_CANDIDATES = {
    "ascii-badge",
    "ascii-border",
    "ascii-divider",
    "ascii-empty",
}

ASCII_PROMOTION_MATRIX = {
    "ascii-7seg": "display-motion",
    "ascii-badge": "static-display",
    "ascii-border": "static-display",
    "ascii-breaker-panel": "interactive-control",
    "ascii-card": "composite",
    "ascii-checkbox": "interactive-control",
    "ascii-divider": "static-display",
    "ascii-empty": "static-display",
    "ascii-error": "static-display-deferred",
    "ascii-fader": "interactive-control",
    "ascii-indicator": "display-motion",
    "ascii-knob": "interactive-control",
    "ascii-modal": "composite",
    "ascii-progress": "data-status",
    "ascii-radio-group": "interactive-control",
    "ascii-skeleton": "display-motion",
    "ascii-sparkline": "display-motion",
    "ascii-spinner": "display-motion",
    "ascii-stepper": "data-status",
    "ascii-switch": "interactive-control",
    "ascii-tab": "composite",
    "ascii-table": "data-status",
    "ascii-tabs": "composite",
    "ascii-ticker": "display-motion",
    "ascii-tile-btn": "interactive-control",
    "ascii-toggle": "interactive-control",
    "ascii-vu": "data-status",
    "split-flap": "display-motion",
}

DEFERRED_TRACKS = {
    "composite",
    "data-status",
    "display-motion",
    "interactive-control",
    "static-display-deferred",
}


def _ascii_components() -> dict[str, dict[str, object]]:
    return {
        name: entry
        for name, entry in build_manifest()["components"].items()
        if entry["template"] and (name.startswith("ascii-") or name == "split-flap")
    }


def test_ascii_promotion_matrix_covers_public_ascii_templates() -> None:
    assert set(ASCII_PROMOTION_MATRIX) == set(_ascii_components())


def test_ascii_static_display_candidates_have_render_evidence_before_promotion() -> None:
    render_tests = ASCII_TESTS.read_text(encoding="utf-8")

    for name in sorted(STATIC_DISPLAY_CANDIDATES):
        css_class = f"chirpui-{name}"
        assert ASCII_PROMOTION_MATRIX[name] == "static-display"
        assert css_class in render_tests, name


def test_ascii_static_display_candidates_have_visual_audit_evidence() -> None:
    browser_tests = BROWSER_TESTS.read_text(encoding="utf-8")
    showcase = SHOWCASE.read_text(encoding="utf-8")

    for name in sorted(STATIC_DISPLAY_CANDIDATES):
        css_class = f"chirpui-{name}"
        assert css_class in browser_tests, name
        assert css_class in showcase, name


def test_ascii_non_static_display_candidates_stay_deferred() -> None:
    for name, entry in _ascii_components().items():
        if name in STATIC_DISPLAY_CANDIDATES:
            continue
        assert ASCII_PROMOTION_MATRIX[name] in DEFERRED_TRACKS, name
        assert entry["maturity"] == "experimental", name
