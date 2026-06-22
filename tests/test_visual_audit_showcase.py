import re
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = REPO_ROOT / "examples" / "design-system-gap-showcase" / "index.html"


class _AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.audit_sections: set[str] = set()
        self.token_jobs: set[str] = set()
        self.theme_profiles: set[str] = set()
        self.classes: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "link" and attr_map.get("href"):
            self.links.append(attr_map["href"] or "")
        if attr_map.get("id"):
            self.ids.add(attr_map["id"] or "")
        if attr_map.get("data-audit-section"):
            self.audit_sections.add(attr_map["data-audit-section"] or "")
        if attr_map.get("data-token-job"):
            self.token_jobs.add(attr_map["data-token-job"] or "")
        if attr_map.get("data-theme-profile"):
            self.theme_profiles.add(attr_map["data-theme-profile"] or "")
        if attr_map.get("class"):
            self.classes.update((attr_map["class"] or "").split())


def test_visual_audit_showcase_assets_resolve() -> None:
    parser = _AuditParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))

    assert parser.links
    for href in parser.links:
        assert not href.startswith(("http://", "https://"))
        assert (SHOWCASE.parent / href).resolve().is_file(), href


def test_visual_audit_showcase_has_required_sections() -> None:
    parser = _AuditParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))

    assert {
        "tokens",
        "navigation",
        "components",
        "interaction-chrome",
        "ascii-tui",
        "proof-patterns",
        "theme-gallery",
    }.issubset(parser.ids)
    assert {
        "token-explorer",
        "interaction-chrome",
        "ascii-tui",
        "proof-patterns",
        "theme-gallery",
    }.issubset(parser.audit_sections)
    assert {
        "chirpui-route-tab__badge--loading",
        "chirpui-route-tab__badge--reserved",
        "chirpui-sidebar__badge--reserved",
        "chirpui-command-palette__item",
        "chirpui-modal__header",
        "chirpui-drawer__header",
        "chirpui-ascii-7seg",
        "chirpui-ascii-badge",
        "chirpui-ascii-border",
        "chirpui-ascii-breaker-panel",
        "chirpui-ascii-card",
        "chirpui-ascii-checkbox",
        "chirpui-ascii-divider",
        "chirpui-ascii-empty",
        "chirpui-ascii-error",
        "chirpui-ascii-fader",
        "chirpui-ascii-indicator",
        "chirpui-ascii-knob",
        "chirpui-ascii-modal",
        "chirpui-ascii-radio",
        "chirpui-ascii-skeleton",
        "chirpui-ascii-sparkline",
        "chirpui-ascii-spinner",
        "chirpui-ascii-switch",
        "chirpui-ascii-stepper",
        "chirpui-ascii-tab",
        "chirpui-ascii-tabs",
        "chirpui-ascii-ticker",
        "chirpui-ascii-tile-btn",
        "chirpui-ascii-toggle",
        "chirpui-ascii-table",
        "chirpui-ascii-vu",
        "chirpui-split-flap",
        "chirpui-logo-cloud",
        "chirpui-story-card",
        "chirpui-cta-band",
        "audit-profile--default",
        "audit-profile--holy",
        "audit-profile--chirp-theme",
    }.issubset(parser.classes)
    assert {
        "page",
        "surface",
        "text",
        "accent",
        "semantic",
        "focus",
        "radius",
        "elevation",
        "typography",
        "motion",
    }.issubset(parser.token_jobs)
    assert {
        "default",
        "app-starter-light",
        "app-starter-dark",
        "holy-light",
        "chirp-theme",
    }.issubset(parser.theme_profiles)


def test_visual_audit_showcase_uses_existing_spacing_tokens() -> None:
    text = SHOWCASE.read_text(encoding="utf-8")
    numeric_space_aliases = sorted(set(re.findall(r"--chirpui-space-\d+", text)))

    assert numeric_space_aliases == []


def test_visual_audit_showcase_keeps_theme_tokens_public() -> None:
    text = SHOWCASE.read_text(encoding="utf-8")

    assert "--chirp-theme-" not in text
    assert "--chirp_theme-" not in text


def test_visual_audit_docs_link_live_golden_screens() -> None:
    text = (REPO_ROOT / "docs" / "patterns" / "visual-audit-showcase.md").read_text(
        encoding="utf-8"
    )

    assert "https://chirp-ui-showcase-production.up.railway.app" in text
    for route in [
        "/screen-command-center",
        "/screen-review-queue",
        "/screen-agent-run-monitor",
        "/screen-product-docs-home",
    ]:
        assert route in text


def test_visual_audit_docs_pin_application_chrome_rhythm_matrix() -> None:
    text = (REPO_ROOT / "docs" / "patterns" / "visual-audit-showcase.md").read_text(
        encoding="utf-8"
    )

    assert "Use this rhythm matrix for application chrome slices" in text
    for surface in [
        "Global shell and command row",
        "Product rail",
        "Object context",
        "Local route row",
        "Page tools",
        "Overlay chrome",
        "Attention states",
    ]:
        assert surface in text

    for proof in [
        "Browser-visible command trigger",
        "Rail width leaves the main pane readable",
        "Breadcrumb overflow remains navigable",
        "Route tabs keep `nowrap`",
        "Open/focus/close proof",
        "Badge placeholders are dimensioned",
    ]:
        assert proof in text


def test_visual_audit_showcase_does_not_teach_legacy_helper_classes() -> None:
    parser = _AuditParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))

    legacy_helpers = {
        "chirpui-clamp-2",
        "chirpui-clamp-3",
        "chirpui-display",
        "chirpui-focus-ring",
        "chirpui-font-2xl",
        "chirpui-font-base",
        "chirpui-font-lg",
        "chirpui-font-medium",
        "chirpui-font-mono",
        "chirpui-font-sm",
        "chirpui-font-xl",
        "chirpui-font-xs",
        "chirpui-list-reset",
        "chirpui-mb-md",
        "chirpui-measure-lg",
        "chirpui-measure-md",
        "chirpui-measure-sm",
        "chirpui-min-w-0",
        "chirpui-mt-md",
        "chirpui-mt-sm",
        "chirpui-placeholder-inline",
        "chirpui-prose-lg",
        "chirpui-prose-sm",
        "chirpui-scroll-x",
        "chirpui-text-muted",
        "chirpui-truncate",
        "chirpui-ui-base",
        "chirpui-ui-bold",
        "chirpui-ui-label",
        "chirpui-ui-lg",
        "chirpui-ui-medium",
        "chirpui-ui-meta",
        "chirpui-ui-normal",
        "chirpui-ui-semibold",
        "chirpui-ui-sm",
        "chirpui-ui-title",
        "chirpui-ui-xl",
        "chirpui-ui-xs",
    }

    assert parser.classes.isdisjoint(legacy_helpers)
    assert parser.classes.intersection({"chirpui-visually-hidden"}) == {"chirpui-visually-hidden"}


def test_visual_audit_showcase_status_tokens_use_base_semantics() -> None:
    text = SHOWCASE.read_text(encoding="utf-8")

    assert "--token-bg: var(--chirpui-success);" in text
    assert "--token-bg: var(--chirpui-warning);" in text
    assert "--token-bg: var(--chirpui-error);" in text
    assert "--token-bg: var(--chirpui-success-muted);" not in text
    assert "--token-bg: var(--chirpui-warning-muted);" not in text
