import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials"
PLAN = ROOT / "docs" / "plans" / "PLAN-css-scope-and-layer.md"


def _first_non_comment_token(text: str) -> str:
    text = text.lstrip()
    while text.startswith("/*"):
        end = text.find("*/")
        if end == -1:
            return text
        text = text[end + 2 :].lstrip()
    return text


def _authored_layer_partials() -> list[str]:
    return sorted(
        path.name
        for path in PARTIALS.glob("*.css")
        if _first_non_comment_token(path.read_text(encoding="utf-8")).startswith(
            "@layer chirpui.component"
        )
    )


def _documented_layer_partials() -> list[str]:
    text = PLAN.read_text(encoding="utf-8")
    marker = "Converted partials currently include:"
    start = text.index(marker) + len(marker)
    end = text.index("**Legacy", start)
    return sorted(re.findall(r"- `([^`]+\.css)`", text[start:end]))


def test_css_scope_migration_plan_matches_authored_layer_envelopes() -> None:
    documented = _documented_layer_partials()
    authored = _authored_layer_partials()

    assert documented == authored
    assert f"**Current converted count:** {len(authored)} partials" in PLAN.read_text(
        encoding="utf-8"
    )
