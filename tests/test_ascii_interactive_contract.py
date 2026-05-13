"""Executable contract for interactive ASCII controls."""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates" / "chirpui"


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
