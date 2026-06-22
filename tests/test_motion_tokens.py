"""Motion-token enforcement for chirpui.css.

Transition declarations must use ``--chirpui-transition*`` / ``--chirpui-motion-*``
tokens. Animation declarations must use the same token family or the
``--chirpui-anim-*`` duration scale.

Existing hardcoded animation timings are grandfathered in
``tests/fixtures/motion_token_baseline.txt``; the ratchet fails on *new*
violations and when the baseline count grows.
"""

from __future__ import annotations

import re
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parents[1] / "src" / "chirp_ui/templates/chirpui.css"
BASELINE_PATH = Path(__file__).resolve().parent / "fixtures" / "motion_token_baseline.txt"

DURATION_LITERAL = re.compile(r"\b\d*\.?\d+(ms|s)\b")
TRANSITION_PATTERN = re.compile(r"transition\s*:\s*([^;]+);")
ANIMATION_PROPERTIES = ("animation", "animation-duration", "animation-delay")


def _uses_motion_tokens(value: str) -> bool:
    if "none" in value or "inherit" in value:
        return True
    return "var(--chirpui-transition" in value or "var(--chirpui-motion-" in value or "var(--chirpui-anim-" in value


def _transition_violations(css: str) -> list[str]:
    hardcoded: list[str] = []
    for line_number, line in enumerate(css.splitlines(), start=1):
        match = TRANSITION_PATTERN.search(line)
        if not match:
            continue
        value = match.group(1)
        if _uses_motion_tokens(value):
            continue
        if DURATION_LITERAL.search(value):
            hardcoded.append(f"{line_number}:{value.strip()}")
    return hardcoded


def _animation_violations(css: str) -> list[int]:
    lines: list[int] = []
    for line_number, line in enumerate(css.splitlines(), start=1):
        for prop in ANIMATION_PROPERTIES:
            match = re.search(rf"{prop}\s*:\s*([^;]+);", line)
            if not match:
                continue
            value = match.group(1)
            if _uses_motion_tokens(value):
                continue
            if DURATION_LITERAL.search(value):
                lines.append(line_number)
                break
    return lines


def _load_baseline() -> frozenset[int]:
    text = BASELINE_PATH.read_text(encoding="utf-8")
    return frozenset(int(line) for line in text.splitlines() if line.strip())


def test_transition_declarations_use_tokens() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    hardcoded = _transition_violations(css)
    assert not hardcoded, (
        "Hardcoded transition timings found. Use motion/transition tokens instead: "
        + ", ".join(hardcoded)
    )


def test_animation_declarations_use_tokens_or_baseline() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    current = frozenset(_animation_violations(css))
    baseline = _load_baseline()
    new_violations = sorted(current - baseline)
    assert not new_violations, (
        "New hardcoded animation timings found outside the motion-token baseline. "
        "Use --chirpui-motion-* / --chirpui-anim-* tokens instead. New lines: "
        + ", ".join(str(line) for line in new_violations)
    )
    assert len(current) <= len(baseline), (
        "Fix motion-token violations and shrink tests/fixtures/motion_token_baseline.txt "
        f"(baseline {len(baseline)} lines, current {len(current)})"
    )
