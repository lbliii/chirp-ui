from pathlib import Path

import tinycss2


def test_chirpui_min_w_0_utility_exists() -> None:
    css_path = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
    text = css_path.read_text(encoding="utf-8")
    assert ".chirpui-min-w-0" in text


def test_chirpui_grid_direct_children_allow_shrink() -> None:
    """Flow grid items must not use min-width:auto or rich cells overflow tracks (gap disappears)."""
    css_path = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
    text = css_path.read_text(encoding="utf-8")
    assert ".chirpui-grid > *" in text
    start = text.index(".chirpui-grid > *")
    snippet = text[start : start + 200]
    assert "min-width" in snippet
    assert "0" in snippet


def test_muted_tokens_mix_toward_surface_not_white() -> None:
    """Muted color-mix targets must use var(--chirpui-surface), not bare white.

    Bare ``white`` produces near-white backgrounds in dark mode because
    the mix percentage (~15%) leaves 85% white regardless of theme.
    """
    import re

    css_path = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
    text = css_path.read_text(encoding="utf-8")

    muted_vars = (
        "--chirpui-primary-muted",
        "--chirpui-success-muted",
        "--chirpui-warning-muted",
        "--chirpui-error-muted",
        "--chirpui-muted-bg",
        "--chirpui-accent-secondary-muted",
    )
    muted_re = re.compile(
        r"(" + "|".join(re.escape(v) for v in muted_vars) + r")\s*:\s*color-mix\([^)]+\)"
    )
    matches = muted_re.findall(text)
    assert len(matches) >= len(muted_vars), (
        f"Expected at least {len(muted_vars)} muted color-mix declarations, found {len(matches)}"
    )

    bad = []
    for m in muted_re.finditer(text):
        decl = m.group(0)
        if ", white)" in decl or ",white)" in decl:
            bad.append(decl)
    assert not bad, (
        "Muted color-mix declarations must mix toward var(--chirpui-surface), not white:\n"
        + "\n".join(bad)
    )


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


def test_chirp_theme_css_has_no_parse_errors() -> None:
    css_path = (
        Path(__file__).resolve().parents[1]
        / "src/bengal_themes/chirp_theme/assets/css/chirp-theme.css"
    )
    stylesheet = css_path.read_text(encoding="utf-8")
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        stylesheet.encode("utf-8"),
        skip_comments=False,
        skip_whitespace=False,
    )
    assert encoding.name == "utf-8"

    parse_errors = [token for token in rules if isinstance(token, tinycss2.ast.ParseError)]
    assert not parse_errors, "CSS parse errors found in chirp-theme.css: " + ", ".join(
        str(error.message) for error in parse_errors
    )
