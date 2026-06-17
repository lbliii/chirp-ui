import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_THEME = ROOT / "docs" / "theming" / "app-theme.md"
TOKENS = ROOT / "docs" / "fundamentals" / "tokens.md"
SHOWCASE = ROOT / "examples" / "design-system-gap-showcase" / "index.html"
RESET_CSS = ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "002_reset.css"
THEME_CSS_DIR = ROOT / "src" / "bengal_themes" / "chirp_theme" / "assets" / "css"
THEME_CSS = THEME_CSS_DIR / "chirp-theme.css"
STYLE_CSS = THEME_CSS_DIR / "style.css"

# WCAG 2.x AA contrast floor for normal-size text (button labels/icons).
WCAG_AA_NORMAL = 4.5

# Frozen ceiling for legacy `var(--color-*)` references in chirp-theme.css
# (occurrence count, not lines — a single rule may reference several). The theme
# is migrating off this bridge onto the public --chirpui-* namespace (issue
# #173). This count may only SHRINK: shipping a NEW legacy color token fails the
# steward below. Lower it whenever a migration batch lands.
LEGACY_COLOR_TOKEN_CEILING = 176


class _TokenJobParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.jobs: list[str] = []
        self.profiles: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if attr_map.get("data-token-job"):
            self.jobs.append(attr_map["data-token-job"] or "")
        if attr_map.get("data-theme-profile"):
            self.profiles.add(attr_map["data-theme-profile"] or "")


def _app_theme_jobs() -> list[str]:
    text = APP_THEME.read_text(encoding="utf-8")
    rows = re.findall(r"^\| ([A-Z][^|]+) \| `--chirpui-", text, flags=re.MULTILINE)
    return [row.strip().lower() for row in rows]


def test_app_theme_first_token_jobs_match_visual_audit_explorer() -> None:
    parser = _TokenJobParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))

    assert parser.jobs == _app_theme_jobs()


def test_token_docs_name_all_visual_theme_profiles() -> None:
    parser = _TokenJobParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))
    docs_text = APP_THEME.read_text(encoding="utf-8") + "\n" + TOKENS.read_text(encoding="utf-8")

    for profile in parser.profiles:
        assert profile in docs_text


def test_visual_audit_stays_in_public_token_namespace() -> None:
    text = SHOWCASE.read_text(encoding="utf-8")

    assert "--chirp-theme-" not in text
    assert "--chirp_theme-" not in text


def test_app_theme_docs_define_override_escalation_ladder() -> None:
    text = APP_THEME.read_text(encoding="utf-8")

    for required in [
        "## Override Escalation Ladder",
        "Public token",
        "Semantic alias",
        "App override",
        "Token proposal",
        "@layer app.overrides",
        "Do not skip directly to component selectors",
    ]:
        assert required in text


# --- Accent / on-accent contrast parity -----------------------------------
#
# `.chirpui-btn--primary` renders `background: var(--chirpui-accent);
# color: var(--chirpui-on-accent)`. When a theme block overrides the accent
# (e.g. dark mode swaps the muted teal #0e7490 for the bright #2dd4bf) it MUST
# also override --chirpui-on-accent, or the inherited :root ink fails WCAG AA.


def _split_theme_blocks(css: str) -> dict[str, str]:
    """Return {selector: declaration-body} for each top-level CSS block.

    Brace-balanced so nested at-rules/blocks stay attached to their owner.
    A ``@layer name { … }`` wrapper is transparent: the theme now ships inside
    a late-declared ``@layer chirp-theme`` (issue #173), so we descend into the
    layer body and surface its :root / [data-theme] blocks as if they were
    top-level. Bare ``@layer a, b;`` statements (no block) are ignored.
    """
    blocks: dict[str, str] = {}
    i = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            break
        selector = css[i:brace].strip().splitlines()[-1].strip()
        depth = 1
        j = brace + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        body = css[brace + 1 : j - 1]
        if selector.startswith("@layer"):
            # Transparent wrapper: recurse so nested blocks are surfaced.
            for sel, sub in _split_theme_blocks(body).items():
                blocks.setdefault(sel, "")
                blocks[sel] += sub
        elif selector:
            blocks.setdefault(selector, "")
            blocks[selector] += "\n" + body
        i = j
    return blocks


def _declares(body: str, prop: str) -> str | None:
    match = re.search(rf"(?<![\w-]){re.escape(prop)}\s*:\s*([^;}}]+)", body)
    return match.group(1).strip() if match else None


def _relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(ch * 2 for ch in hex_color)
    r, g, b = (int(hex_color[k : k + 2], 16) / 255 for k in (0, 2, 4))

    def _channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def _contrast_ratio(fg: str, bg: str) -> float:
    l1 = _relative_luminance(fg)
    l2 = _relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _theme_accent_blocks() -> dict[str, str]:
    css = THEME_CSS.read_text(encoding="utf-8")
    blocks = _split_theme_blocks(css)
    return {
        selector: body
        for selector, body in blocks.items()
        if "[data-theme" in selector and _declares(body, "--chirpui-accent")
    }


def test_every_theme_accent_override_pairs_on_accent() -> None:
    """Any [data-theme] block redefining --chirpui-accent must also redefine
    --chirpui-on-accent so the primary button label keeps a checked contrast."""
    accent_blocks = _theme_accent_blocks()

    # The dark block is the canonical accent override; guard against the test
    # silently passing if the parser ever stops finding it.
    assert any("dark" in selector for selector in accent_blocks), (
        "expected at least one [data-theme] accent override (e.g. dark)"
    )

    for selector, body in accent_blocks.items():
        assert _declares(body, "--chirpui-on-accent"), (
            f"{selector} overrides --chirpui-accent but not "
            f"--chirpui-on-accent; the primary button label inherits the "
            f":root ink and can fail WCAG AA"
        )


def test_primary_button_meets_aa_in_root_and_theme_overrides() -> None:
    """--chirpui-on-accent on --chirpui-accent must clear 4.5:1 in :root and
    in every theme block that overrides the accent."""
    css = THEME_CSS.read_text(encoding="utf-8")
    blocks = _split_theme_blocks(css)

    root_body = blocks.get(":root", "")
    root_accent = _declares(root_body, "--chirpui-accent")
    root_on_accent = _declares(root_body, "--chirpui-on-accent")
    assert root_accent, ":root must define --chirpui-accent"
    assert root_on_accent, ":root must define --chirpui-on-accent"

    pairs: list[tuple[str, str, str]] = [(":root", root_accent, root_on_accent)]
    for selector, body in _theme_accent_blocks().items():
        on_accent = _declares(body, "--chirpui-on-accent")
        assert on_accent, f"{selector} missing --chirpui-on-accent"
        pairs.append((selector, _declares(body, "--chirpui-accent"), on_accent))

    hex_re = re.compile(r"^#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?$")
    for selector, accent, on_accent in pairs:
        # Only assert when both ends are concrete hex (not var()/keyword) so we
        # measure resolved colors, not unresolved references.
        if not (hex_re.match(accent) and hex_re.match(on_accent)):
            continue
        ratio = _contrast_ratio(on_accent, accent)
        assert ratio >= WCAG_AA_NORMAL, (
            f"{selector}: primary button label {on_accent} on accent "
            f"{accent} is {ratio:.2f}:1, below WCAG AA {WCAG_AA_NORMAL}:1"
        )


def test_library_default_accent_on_accent_meets_aa() -> None:
    """Shipped chirp-ui baseline tokens must pair accent/on-accent for AA contrast."""
    css = RESET_CSS.read_text(encoding="utf-8")
    blocks = _split_theme_blocks(css)
    root_body = blocks.get(":root", "")
    accent = _declares(root_body, "--chirpui-accent")
    on_accent = _declares(root_body, "--chirpui-on-accent")
    assert accent, ":root must declare --chirpui-accent"
    assert on_accent, ":root must declare --chirpui-on-accent"

    light_accent = re.search(r"light-dark\(\s*(#[0-9a-fA-F]{3,6})", accent)
    light_on = re.search(r"light-dark\(\s*(#[0-9a-fA-F]{3,6})", on_accent)
    dark_on = re.search(r"light-dark\([^,]+,\s*(#[0-9a-fA-F]{3,6})", on_accent)
    assert light_accent, "library accent must use a light-dark() hex pairing"
    assert light_on, "library on-accent must use a light-dark() hex pairing"
    assert dark_on, "library on-accent must declare a dark-side hex fallback"

    light_ratio = _contrast_ratio(light_on.group(1), light_accent.group(1))
    assert light_ratio >= WCAG_AA_NORMAL, (
        f"library light accent {light_accent.group(1)} with on-accent "
        f"{light_on.group(1)} is {light_ratio:.2f}:1, below WCAG AA"
    )

    dark_accent = re.search(r"light-dark\([^,]+,\s*(#[0-9a-fA-F]{3,6})", accent)
    assert dark_accent, "library accent must declare a dark-side hex fallback"
    dark_ratio = _contrast_ratio(dark_on.group(1), dark_accent.group(1))
    assert dark_ratio >= WCAG_AA_NORMAL, (
        f"library dark accent {dark_accent.group(1)} with on-accent "
        f"{dark_on.group(1)} is {dark_ratio:.2f}:1, below WCAG AA"
    )

    light_block = blocks.get('[data-theme="light"]', "")
    light_override = _declares(light_block, "--chirpui-accent")
    if light_override and re.match(r"^#[0-9a-fA-F]{3,6}$", light_override):
        ratio = _contrast_ratio("#fff", light_override)
        assert ratio >= WCAG_AA_NORMAL, (
            f'[data-theme="light"] accent {light_override} with white on-accent '
            f"is {ratio:.2f}:1, below WCAG AA"
        )


# --- Cascade-layer override contract (issue #173) --------------------------
#
# chirp-theme.css must ride a single late-declared `@layer chirp-theme` so the
# theme dogfoods the chirp-ui override contract (consumers win via an even
# later layer such as `@layer app.overrides`) instead of beating every layer
# with unlayered rules. style.css must pin that layer name LAST in its named
# order so the position is deterministic regardless of @import timing.


def test_theme_css_rules_live_in_a_single_chirp_theme_layer() -> None:
    css = THEME_CSS.read_text(encoding="utf-8")

    layer_blocks = re.findall(r"@layer\s+([\w.-]+)\s*\{", css)
    assert layer_blocks == ["chirp-theme"], (
        "chirp-theme.css must wrap all rules in exactly one "
        f"`@layer chirp-theme {{ … }}` block, found: {layer_blocks}"
    )

    # No rule may sit outside the layer: only the file header comment and the
    # single layer wrapper precede the first selector. Strip comments, then the
    # first non-space character after the header must open the @layer block.
    no_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL).strip()
    assert no_comments.startswith("@layer chirp-theme"), (
        "every chirp-theme.css rule (incl. :root / [data-theme] token blocks) "
        "must live inside the @layer; no unlayered rules allowed"
    )

    # The contrast-checked dark on-accent pairing (wave-1 fix) rides inside the
    # layer — the parser already descends into it, so this also guards that the
    # token blocks were not accidentally hoisted out of the wrapper.
    blocks = _split_theme_blocks(css)
    dark = next((b for s, b in blocks.items() if "[data-theme" in s and "dark" in s), None)
    assert dark is not None, "dark [data-theme] block must be present inside the layer"
    assert _declares(dark, "--chirpui-on-accent"), (
        "dark accent override must keep its --chirpui-on-accent pairing"
    )


def test_style_css_declares_chirp_theme_layer_last() -> None:
    css = STYLE_CSS.read_text(encoding="utf-8")

    match = re.search(r"@layer\s+([\w.\-,\s]+);", css)
    assert match, "style.css must declare a named @layer order"
    layers = [name.strip() for name in match.group(1).split(",")]
    assert layers[-1] == "chirp-theme", (
        "`chirp-theme` must be the LAST layer in style.css's @layer "
        f"declaration so it overrides every theme layer; got order: {layers}"
    )


# --- Legacy color-token migration steward (issue #173) ---------------------
#
# The theme is migrating off the legacy `--color-*` bridge onto the public
# `--chirpui-*` namespace. This steward freezes the legacy reference count at a
# ceiling that may only shrink, so a new rule cannot quietly reintroduce the
# bridge. Lower LEGACY_COLOR_TOKEN_CEILING when a migration batch lands.


def _legacy_color_refs(css: str) -> list[str]:
    return re.findall(r"var\(\s*--color-[\w-]+", css)


def test_no_new_legacy_color_tokens() -> None:
    css = THEME_CSS.read_text(encoding="utf-8")
    count = len(_legacy_color_refs(css))

    assert count <= LEGACY_COLOR_TOKEN_CEILING, (
        f"chirp-theme.css has {count} legacy `var(--color-*)` references, above "
        f"the frozen ceiling of {LEGACY_COLOR_TOKEN_CEILING}. New theme rules "
        f"must author against the public --chirpui-* namespace (see "
        f"tokens/semantic.css for the bridge mapping)."
    )


def test_legacy_color_ceiling_is_not_stale() -> None:
    """Keep the ceiling honest: it should track the real count, not drift far
    above it. If a migration batch shrinks the count, lower the ceiling too."""
    css = THEME_CSS.read_text(encoding="utf-8")
    count = len(_legacy_color_refs(css))

    assert count == LEGACY_COLOR_TOKEN_CEILING, (
        f"chirp-theme.css now has {count} legacy `var(--color-*)` references but "
        f"LEGACY_COLOR_TOKEN_CEILING is {LEGACY_COLOR_TOKEN_CEILING}. A migration "
        f"reduced the count — lower the ceiling to {count} to lock in the gain."
    )
