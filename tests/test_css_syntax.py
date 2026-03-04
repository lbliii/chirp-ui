from pathlib import Path

import tinycss2


def test_chirpui_css_has_no_parse_errors() -> None:
    css_path = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
    stylesheet = css_path.read_text(encoding="utf-8")
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        stylesheet.encode("utf-8"),
        skip_comments=False,
        skip_whitespace=False,
    )
    assert encoding.name == "utf-8"

    parse_errors = [token for token in rules if isinstance(token, tinycss2.ast.ParseError)]
    assert not parse_errors, "CSS parse errors found in chirpui.css: " + ", ".join(
        str(error.message) for error in parse_errors
    )
