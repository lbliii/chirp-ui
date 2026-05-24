from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
PLAN = ROOT / "docs" / "plans" / "PLAN-visual-taste-floor-saga.md"
RESEARCH = ROOT / "docs" / "decisions" / "typography-rhythm-taste-floor.md"
MATRIX = ROOT / "docs" / "decisions" / "typography-role-matrix.md"
INDEX = ROOT / "docs" / "INDEX.md"
ROADMAP = ROOT / "docs" / "strategy" / "roadmap-pre-1.0.md"
INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"
SOURCE_MAP = ROOT / "docs" / "agents" / "agent-source-map.md"


def test_typography_research_records_external_and_local_evidence() -> None:
    text = RESEARCH.read_text(encoding="utf-8")

    for phrase in [
        "Status: research-backed planning input",
        "This record captures the typography research",
        "It does not add public tokens, macro parameters",
        "Material 3 typography",
        "Fluent 2 typography",
        "Carbon typography",
        "Atlassian typography",
        "Primer typography",
        "GOV.UK layout/type scale",
        "USWDS typography",
        "WCAG text spacing",
        "Current Chirp UI typography has useful foundations",
        "UI and prose scales are named by size rather than role.",
        "viewport-driven `clamp()` values",
    ]:
        assert phrase in text


def test_typography_research_keeps_roles_recipe_only() -> None:
    text = RESEARCH.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "These names are planning vocabulary only",
        "They do not authorize public token names or macros",
        "Stop and ask before adding public typography role tokens",
        "New utility classes for type roles.",
        "New font dependency or bundled web font.",
        "Manifest schema for type roles.",
    ]:
        assert phrase in normalized

    for role_family in [
        "Structure",
        "Reading",
        "Metadata",
        "Controls",
        "State",
        "Data",
        "Technical",
        "Expressive",
    ]:
        assert f"| {role_family} |" in text


def test_visual_taste_plan_tracks_typography_next_phase() -> None:
    text = PLAN.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "Typography roles",
        "docs/decisions/typography-rhythm-taste-floor.md",
        "Epic 5a. Typography And Rhythm Taste Floor",
        "Audit current CSS partials, theme packs, examples, and golden screens",
        "docs/decisions/typography-role-matrix.md",
        "Draft a recipe-only role matrix",
        "Stop and ask before changing public token defaults",
        "Run the typography and rhythm audit before promoting visual patterns.",
        "Typography roles are screen-proven before becoming public token vocabulary.",
    ]:
        assert phrase in normalized


def test_typography_research_is_indexed_and_mapped() -> None:
    index_text = INDEX.read_text(encoding="utf-8")
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    inventory_text = INVENTORY.read_text(encoding="utf-8")
    source_map_text = SOURCE_MAP.read_text(encoding="utf-8")

    assert "decisions/typography-rhythm-taste-floor.md" in index_text
    assert "Typography role and rhythm research" in index_text
    assert "decisions/typography-role-matrix.md" in index_text
    assert "Recipe-only typography audit matrix" in index_text

    assert "docs/decisions/typography-rhythm-taste-floor.md" in roadmap_text
    assert "docs/decisions/typography-role-matrix.md" in roadmap_text
    assert "Typography improvements are role-backed and screen-proven" in roadmap_text

    for text in [inventory_text, source_map_text]:
        assert "docs/decisions/typography-rhythm-taste-floor.md" in text
        assert "docs/decisions/typography-role-matrix.md" in text
        assert "planning input" in text
        assert "not public token vocabulary" in text
        assert "source-only until public token promotion is approved" in text


def test_typography_role_matrix_records_audit_and_recipe_boundary() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "Status: recipe-only audit matrix",
        "It does not add public token names",
        "Core UI and prose sizes are fluid through viewport `clamp()` values.",
        "Golden screen templates do not hard-code typography declarations.",
        "Workspace primitives used an undefined typography token.",
        "Fixed by using `--chirpui-font-base`",
        "These role names are recipe vocabulary only.",
        "Stop and ask for a public typography-token promotion plan.",
    ]:
        assert phrase in normalized

    for role in [
        "`page-title`",
        "`panel-title`",
        "`object-title`",
        "`dense-body`",
        "`metadata`",
        "`count-label`",
        "`metric`",
        "`status-label`",
        "`log-line`",
        "`hero-display`",
        "`proof-copy`",
    ]:
        assert role in text


def test_workspace_primitives_do_not_reference_undefined_font_md_token() -> None:
    partial = (
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "167_workspace-primitives.css"
    ).read_text(encoding="utf-8")
    generated = (ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css").read_text(
        encoding="utf-8"
    )

    assert "--chirpui-font-md" not in partial
    assert "--chirpui-font-md" not in generated
    assert ".chirpui-result-card__title" in partial
    assert ".chirpui-inspector-panel__title" in partial
    assert "font-size: var(--chirpui-font-base);" in partial


def test_typography_role_polish_uses_existing_tokens() -> None:
    workspace = (
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "167_workspace-primitives.css"
    ).read_text(encoding="utf-8")
    hero = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "042_hero.css"
    ).read_text(encoding="utf-8")
    stat = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "012_stat.css"
    ).read_text(encoding="utf-8")
    story = (
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "163_story-card.css"
    ).read_text(encoding="utf-8")
    cta = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "164_cta-band.css"
    ).read_text(encoding="utf-8")
    pattern_assets = (
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "165_pattern-assets.css"
    ).read_text(encoding="utf-8")
    index_card = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "059_table.css"
    ).read_text(encoding="utf-8")

    for signal in [
        ".chirpui-filter-rail__label",
        "font-weight: var(--chirpui-ui-font-weight-medium);",
        ".chirpui-metric-strip__value",
        "font-variant-numeric: tabular-nums;",
        ".chirpui-result-card__body",
        "line-height: var(--chirpui-line-height-normal);",
        ".chirpui-inspector-panel__body",
    ]:
        assert signal in workspace

    assert ".chirpui-hero--page .chirpui-hero__title" in hero
    assert "font-size: var(--chirpui-prose-5xl);" in hero
    assert "letter-spacing: var(--chirpui-display-letter-spacing);" in hero
    assert ".chirpui-hero--page .chirpui-hero__subtitle" in hero
    assert "max-inline-size: 58ch;" in hero

    assert "font-variant-numeric: tabular-nums;" in stat
    assert "line-height: var(--chirpui-line-height-tight);" in stat

    assert ".chirpui-story-card__metric" in story
    assert "font-variant-numeric: tabular-nums;" in story
    assert ".chirpui-story-card__summary" in story
    assert "line-height: var(--chirpui-line-height-normal);" in story

    assert ".chirpui-cta-band__title" in cta
    assert "max-inline-size: 14ch;" in cta
    assert "font-size: var(--chirpui-prose-3xl);" in cta
    assert ".chirpui-cta-band__body" in cta
    assert "line-height: var(--chirpui-line-height-relaxed);" in cta

    assert ".chirpui-detail-header__title" in pattern_assets
    assert "font-size: var(--chirpui-prose-3xl);" in pattern_assets

    assert ".chirpui-index-card__badge" in index_card
    assert "font-weight: var(--chirpui-ui-font-weight-medium);\n    font-weight" not in index_card
    assert "line-height: var(--chirpui-line-height-tight);" in index_card


def test_typography_polish_does_not_reference_removed_display_tokens() -> None:
    for path in [
        ROOT / "src" / "chirp_ui" / "templates" / "chirpui.css",
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "164_cta-band.css",
        ROOT
        / "src"
        / "chirp_ui"
        / "templates"
        / "css"
        / "partials"
        / "165_pattern-assets.css",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "--chirpui-display-sm" not in text
