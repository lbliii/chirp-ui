from pathlib import Path
import re


CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"


def test_transition_declarations_use_tokens() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    hardcoded: list[str] = []
    transition_pattern = re.compile(r"transition\s*:\s*([^;]+);")
    duration_literal_pattern = re.compile(r"\b\d*\.?\d+(ms|s)\b")

    for line_number, line in enumerate(css.splitlines(), start=1):
        match = transition_pattern.search(line)
        if not match:
            continue
        value = match.group(1)
        # Allow tokenized transitions and explicit disable.
        if "none" in value or "var(--chirpui-transition" in value or "var(--chirpui-motion-" in value:
            continue
        if duration_literal_pattern.search(value):
            hardcoded.append(f"{line_number}:{value.strip()}")

    assert not hardcoded, (
        "Hardcoded transition timings found. Use motion/transition tokens instead: "
        + ", ".join(hardcoded)
    )
