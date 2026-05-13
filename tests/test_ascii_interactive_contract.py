"""Executable contract for interactive ASCII controls."""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "chirpui"
CSS_PARTIAL_DIR = (
    Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "css" / "partials"
)

ASCII_PROOF_GROUPS = {
    "native_controls": {
        "ascii_checkbox.html",
        "ascii_fader.html",
        "ascii_knob.html",
        "ascii_radio.html",
        "ascii_toggle.html",
        "ascii_tile_btn.html",
        "ascii_breaker_panel.html",
    },
    "composites": {
        "ascii_card.html",
        "ascii_modal.html",
        "ascii_tabs.html",
    },
    "data_status": {
        "ascii_progress.html",
        "ascii_stepper.html",
        "ascii_table.html",
        "ascii_vu_meter.html",
    },
    "display_motion": {
        "ascii_7seg.html",
        "ascii_badge.html",
        "ascii_border.html",
        "ascii_divider.html",
        "ascii_empty.html",
        "ascii_error.html",
        "ascii_icon.html",
        "ascii_indicator.html",
        "ascii_skeleton.html",
        "ascii_sparkline.html",
        "ascii_spinner.html",
        "ascii_split_flap.html",
        "ascii_ticker.html",
    },
}

ASCII_DISPLAY_CONTRACTS = {
    "ascii_7seg.html": ("chirpui-ascii-7seg__display", "chirpui-ascii-7seg__frame"),
    "ascii_icon.html": ('aria-hidden="true"',),
    "ascii_indicator.html": ("chirpui-ascii-indicator__light", 'aria-hidden="true"'),
    "ascii_skeleton.html": ('aria-hidden="true"',),
    "ascii_sparkline.html": ('role="img"', "aria-label"),
    "ascii_spinner.html": ('role="status"', "aria-label"),
    "ascii_split_flap.html": ("chirpui-split-flap__char",),
    "ascii_ticker.html": ('role="marquee"', "chirpui-ascii-ticker__text"),
    "ascii_vu_meter.html": ('role="meter"', "aria-valuenow"),
}


def _template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text()


def test_ascii_maturity_proof_groups_cover_templates() -> None:
    grouped = set().union(*ASCII_PROOF_GROUPS.values())
    actual = {path.name for path in TEMPLATE_DIR.glob("ascii_*.html")}

    assert grouped == actual


def test_ascii_interactive_controls_are_native_input_backed() -> None:
    """Keyboard behavior comes from native inputs, not custom script handlers."""
    expectations = {
        "ascii_checkbox.html": ('type="checkbox"',),
        "ascii_toggle.html": ('type="checkbox"', "ascii_toggle", "ascii_switch"),
        "ascii_radio.html": ('type="radio"', "<fieldset"),
        "ascii_fader.html": ('type="range"',),
        "ascii_knob.html": ('type="radio"', "<fieldset"),
        "ascii_breaker_panel.html": ("ascii_switch",),
    }

    for template_name, needles in expectations.items():
        source = _template(template_name)
        for needle in needles:
            assert needle in source, f"{template_name} must keep {needle!r}"


def test_ascii_display_contracts_are_explicit() -> None:
    for template_name, needles in ASCII_DISPLAY_CONTRACTS.items():
        source = _template(template_name)
        for needle in needles:
            assert needle in source, f"{template_name} must keep {needle!r}"


def test_ascii_interactive_templates_do_not_embed_script_tags() -> None:
    for template_path in TEMPLATE_DIR.glob("ascii_*.html"):
        assert "<script" not in template_path.read_text().lower()


def test_ascii_fader_exposes_visible_focus_state() -> None:
    source = (CSS_PARTIAL_DIR / "149_ascii-fader.css").read_text()
    assert ".chirpui-ascii-fader__input:focus-visible" in source
    assert "outline: 2px solid var(--chirpui-focus-ring)" in source


def test_ascii_motion_variants_respect_reduced_motion() -> None:
    motion_partials = [
        "074_ascii-icons.css",
        "142_ascii-skeleton.css",
        "143_ascii-toggle.css",
        "144_ascii-switch.css",
        "146_ascii-indicator-light.css",
        "147_ascii-tile-button.css",
        "150_ascii-vu-meter.css",
        "155_ascii-split-flap-display.css",
        "156_ascii-ticker.css",
    ]

    for partial in motion_partials:
        source = (CSS_PARTIAL_DIR / partial).read_text()
        assert "@media (prefers-reduced-motion: reduce)" in source


def test_ascii_tabs_are_link_navigation_not_tabpanel_controller() -> None:
    source = _template("ascii_tabs.html")

    assert 'role="tablist"' not in source
    assert 'role="tab"' not in source
    assert 'aria-current="page"' in source
    assert "href=" in source
