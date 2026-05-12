from pathlib import Path

import tinycss2

from chirp_ui.tokens import TOKEN_CATALOG

THEME_ROOT = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/themes"
LEGACY_SELECTOR_THEME_FILES = {
    # Retained pre-catalog app theme. New curated theme packs must be token-only.
    "holy-light.css",
}


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


def test_chirp_theme_entrypoint_css_has_no_parse_errors() -> None:
    css_path = (
        Path(__file__).resolve().parents[1] / "src/bengal_themes/chirp_theme/assets/css/style.css"
    )
    stylesheet = css_path.read_text(encoding="utf-8")
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        stylesheet.encode("utf-8"),
        skip_comments=False,
        skip_whitespace=False,
    )
    assert encoding.name == "utf-8"

    parse_errors = [token for token in rules if isinstance(token, tinycss2.ast.ParseError)]
    assert not parse_errors, "CSS parse errors found in style.css: " + ", ".join(
        str(error.message) for error in parse_errors
    )


def test_app_theme_starter_css_has_no_parse_errors() -> None:
    css_path = (
        Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/themes/app-theme-starter.css"
    )
    stylesheet = css_path.read_text(encoding="utf-8")
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        stylesheet.encode("utf-8"),
        skip_comments=False,
        skip_whitespace=False,
    )
    assert encoding.name == "utf-8"

    parse_errors = [token for token in rules if isinstance(token, tinycss2.ast.ParseError)]
    assert not parse_errors, "CSS parse errors found in app-theme-starter.css: " + ", ".join(
        str(error.message) for error in parse_errors
    )


def test_app_theme_starter_covers_system_mode_tokens() -> None:
    css_path = (
        Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/themes/app-theme-starter.css"
    )
    text = css_path.read_text(encoding="utf-8")

    assert '[data-theme="light"]' in text
    assert '[data-theme="dark"]' in text
    assert '[data-theme="system"]' in text
    assert "prefers-color-scheme: light" in text
    assert "prefers-color-scheme: dark" in text

    for media_query in ("prefers-color-scheme: light", "prefers-color-scheme: dark"):
        media_start = text.index(media_query)
        system_start = text.index('[data-theme="system"]', media_start)
        system_end = text.index("}", system_start)
        system_text = text[system_start:system_end]
        for token in (
            "--chirpui-bg",
            "--chirpui-surface",
            "--chirpui-text",
            "--chirpui-accent",
            "--chirpui-primary",
            "--chirpui-alert-info-bg",
        ):
            assert token in system_text


def _qualified_rule_preludes(rules: list[object]) -> list[str]:
    prelude: list[str] = []
    for rule in rules:
        if isinstance(rule, tinycss2.ast.QualifiedRule):
            prelude.append(tinycss2.serialize(rule.prelude).strip())
        elif isinstance(rule, tinycss2.ast.AtRule) and rule.content:
            nested = tinycss2.parse_rule_list(
                rule.content, skip_comments=True, skip_whitespace=True
            )
            prelude.extend(_qualified_rule_preludes(nested))
    return prelude


def test_packaged_app_themes_are_token_only() -> None:
    """Curated app themes may set tokens, but must not fork component CSS."""

    allowed_selectors = {
        ":root",
        '[data-theme="light"]',
        '[data-theme="dark"]',
        '[data-theme="system"]',
    }
    for css_path in sorted(THEME_ROOT.glob("*.css")):
        if css_path.name in LEGACY_SELECTOR_THEME_FILES:
            continue
        stylesheet = css_path.read_text(encoding="utf-8")
        rules = tinycss2.parse_stylesheet(
            stylesheet,
            skip_comments=True,
            skip_whitespace=True,
        )
        selectors = _qualified_rule_preludes(rules)
        invalid_selectors = sorted(
            selector for selector in selectors if selector not in allowed_selectors
        )
        assert not invalid_selectors, (
            f"{css_path.name} must be token-only; unsupported selectors: "
            + ", ".join(invalid_selectors)
        )

        referenced_tokens = set()
        for token in tinycss2.parse_component_value_list(stylesheet):
            if isinstance(token, tinycss2.ast.IdentToken) and token.value.startswith("--chirpui-"):
                referenced_tokens.add(token.value)
        unknown_tokens = sorted(referenced_tokens - set(TOKEN_CATALOG))
        assert not unknown_tokens, (
            f"{css_path.name} references tokens missing from TOKEN_CATALOG: "
            + ", ".join(unknown_tokens)
        )


def test_curated_theme_packs_cover_modes() -> None:
    """Catalog theme packs must cover light, dark, and system branches."""
    from chirp_ui.theme_packs import THEME_PACKS

    for pack in THEME_PACKS:
        text = (THEME_ROOT / Path(pack.path).name).read_text(encoding="utf-8")
        assert '[data-theme="light"]' in text
        assert '[data-theme="dark"]' in text
        assert '[data-theme="system"]' in text
        assert "prefers-color-scheme: light" in text
        assert "prefers-color-scheme: dark" in text
        assert ".chirpui-" not in text
