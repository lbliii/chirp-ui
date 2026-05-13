"""Executable contract for interactive ASCII controls."""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "chirpui"
CSS_PARTIAL_DIR = (
    Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "css" / "partials"
)


def _template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text()


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
    ]

    for partial in motion_partials:
        source = (CSS_PARTIAL_DIR / partial).read_text()
        assert "@media (prefers-reduced-motion: reduce)" in source
