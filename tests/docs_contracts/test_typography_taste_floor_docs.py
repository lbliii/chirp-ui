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
        "The typography and rhythm implementation pass is complete",
        "The first component taste pass now applies the role/rhythm lessons",
        "existing tokens only",
        "A second component taste sweep extends the same existing-token treatment",
        "panel, callout, modal, tabs, collapse, dropdown, toast, pagination",
        "Draft a public token promotion proposal only after repeated component",
        "Defer public typography role tokens until repeated screen workarounds justify",
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
        "Implementation Outcome",
        "Product/Docs Home now uses `page_hero`",
        "Browser proof checks computed typography hierarchy",
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
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "163_story-card.css"
    ).read_text(encoding="utf-8")
    cta = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "164_cta-band.css"
    ).read_text(encoding="utf-8")
    pattern_assets = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "165_pattern-assets.css"
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
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "164_cta-band.css",
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "165_pattern-assets.css",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "--chirpui-display-sm" not in text


def test_component_taste_pass_uses_existing_role_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "action_bar": "013_action-bar.css",
            "action_containers": "014_action-containers.css",
            "description_list": "032_description-list.css",
            "settings_row": "033_settings-row.css",
            "timeline": "035_timeline.css",
            "streaming": "038_streaming-and-ai-components.css",
            "card": "045_card.css",
            "table": "059_table.css",
            "alert": "061_alert.css",
            "form": "070_form-fields.css",
            "button": "071_button.css",
            "badge": "072_badge.css",
            "empty": "078_empty-state.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name

    for signal in [
        "font-variant-numeric: tabular-nums;",
        "line-height: var(--chirpui-line-height-tight);",
    ]:
        assert signal in partials["action_bar"]

    assert "font-family: var(--chirpui-ui-font-family);" in partials["action_containers"]
    assert "color: var(--chirpui-text-muted);" in partials["action_containers"]

    assert "line-height: var(--chirpui-line-height-normal);" in partials["card"]
    assert "font-variant-numeric: tabular-nums;" in partials["card"]
    assert "overflow-wrap: anywhere;" in partials["card"]

    assert ".chirpui-timeline__date" in partials["timeline"]
    assert "font-variant-numeric: tabular-nums;" in partials["timeline"]
    assert ".chirpui-timeline__body" in partials["timeline"]

    assert ".chirpui-table__td--right" in partials["table"]
    assert "font-size: var(--chirpui-font-sm);" in partials["table"]

    assert ".chirpui-dl__detail--number" in partials["description_list"]
    assert "font-variant-numeric: tabular-nums;" in partials["description_list"]

    assert ".chirpui-settings-row__status" in partials["settings_row"]
    assert "font-variant-numeric: tabular-nums;" in partials["settings_row"]

    assert ".chirpui-streaming-block" in partials["streaming"]
    assert "font-size: var(--chirpui-font-sm);" in partials["streaming"]
    assert ".chirpui-sse-status" in partials["streaming"]

    assert ".chirpui-field__error" in partials["form"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["form"]

    assert ".chirpui-badge" in partials["badge"]
    assert "font-variant-numeric: tabular-nums;" in partials["badge"]

    assert ".chirpui-empty-state__body" in partials["empty"]
    assert "max-inline-size: var(--chirpui-measure-sm);" in partials["empty"]

    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["button"]
    assert "font-size: var(--chirpui-font-sm);" in partials["alert"]


def test_second_component_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "panel": "005_workbench.css",
            "callout": "041_callout.css",
            "modal": "052_modal.css",
            "tabs": "054_tabs.css",
            "collapse": "056_collapse.css",
            "dropdown": "057_dropdown.css",
            "toast": "058_toast.css",
            "pagination": "060_pagination.css",
            "tabs_panels": "067_tabs-panels.css",
            "progress": "079_progress-bar.css",
            "status": "082_status-indicator.css",
            "command_palette": "085_command-palette.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name

    for name in ["panel", "callout", "modal", "collapse", "dropdown", "toast"]:
        assert "line-height: var(--chirpui-line-height-normal);" in partials[name]

    for name in [
        "panel",
        "modal",
        "dropdown",
        "pagination",
        "progress",
        "status",
        "command_palette",
    ]:
        assert "font-variant-numeric: tabular-nums;" in partials[name]

    assert ".chirpui-panel__title" in partials["panel"]
    assert "line-height: var(--chirpui-line-height-tight);" in partials["panel"]
    assert ".chirpui-modal__title" in partials["modal"]
    assert "font-size: var(--chirpui-font-lg);" in partials["modal"]

    assert ".chirpui-tab" in partials["tabs"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["tabs"]
    assert ".chirpui-tabs__tab--active" in partials["tabs_panels"]
    assert "font-weight: var(--chirpui-ui-font-weight-semibold);" in partials["tabs_panels"]

    assert ".chirpui-command-palette__inner" in partials["command_palette"]
    assert "font-family: var(--chirpui-ui-font-family);" in partials["command_palette"]
    assert ".chirpui-command-palette__item-label" in partials["command_palette"]

    assert ".chirpui-status-indicator__label" in partials["status"]
    assert "overflow-wrap: anywhere;" in partials["status"]
