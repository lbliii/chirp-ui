import re
from pathlib import Path

PARTIALS_DIR = (
    Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "css" / "partials"
)
CSS_PATH = Path(__file__).resolve().parents[1] / "src" / "chirp_ui" / "templates" / "chirpui.css"


def test_tabular_numeric_declarations_use_token() -> None:
    """font-variant-numeric must use --chirpui-nums-tabular, not inline tabular-nums."""
    hardcoded: list[str] = []
    pattern = re.compile(r"font-variant-numeric\s*:\s*([^;]+);")

    for css_file in sorted(PARTIALS_DIR.glob("*.css")):
        for line_number, line in enumerate(
            css_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            match = pattern.search(line)
            if not match:
                continue
            value = match.group(1).strip()
            if value == "var(--chirpui-nums-tabular)":
                continue
            hardcoded.append(f"{css_file.name}:{line_number}:{value}")

    assert not hardcoded, (
        "Hardcoded font-variant-numeric values found. Use var(--chirpui-nums-tabular): "
        + ", ".join(hardcoded)
    )


def test_tabular_numeric_token_and_utility_shipped() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    assert "--chirpui-nums-tabular: tabular-nums" in css
    assert ".chirpui-tabular { font-variant-numeric: var(--chirpui-nums-tabular); }" in css
