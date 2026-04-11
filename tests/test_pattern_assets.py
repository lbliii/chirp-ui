"""SVG pattern suite shipped with chirpui.css."""

from pathlib import Path

import pytest

PATTERNS = (
    "checker.svg",
    "dots-sm.svg",
    "dots-md.svg",
    "grid.svg",
    "diag.svg",
    "crosshatch.svg",
    "weave.svg",
    "noise-fine.svg",
    "noise-coarse.svg",
    "hex.svg",
)

EXPECTED_CSS_VARS = (
    "--chirpui-pattern-checker:",
    "--chirpui-pattern-dots-sm:",
    "--chirpui-pattern-dots-md:",
    "--chirpui-pattern-grid:",
    "--chirpui-pattern-diag:",
    "--chirpui-pattern-crosshatch:",
    "--chirpui-pattern-weave:",
    "--chirpui-pattern-noise-fine:",
    "--chirpui-pattern-noise-coarse:",
    "--chirpui-pattern-hex:",
)


@pytest.fixture
def templates_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates"


def test_pattern_svgs_exist(templates_dir: Path) -> None:
    d = templates_dir / "patterns"
    assert d.is_dir()
    for name in PATTERNS:
        p = d / name
        assert p.is_file(), f"missing {p}"
        text = p.read_text(encoding="utf-8")
        assert "<svg" in text


def test_chirpui_css_exports_pattern_tokens() -> None:
    css_path = (
        Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "chirpui.css"
    )
    text = css_path.read_text(encoding="utf-8")
    for token in EXPECTED_CSS_VARS:
        assert token in text
    assert ".chirpui-texture--checker" in text
    assert ".chirpui-texture--noise-fine" in text
