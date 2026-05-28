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
        "A third component taste sweep carries the same treatment into navigation",
        "breadcrumbs, sidebar, route tabs, segmented control, accordion, drawer, and tray",
        "A fourth component taste sweep covers smaller controls",
        "inline edit, logo/navbar",
        "A fifth component taste sweep applies the same existing-token treatment",
        "entity header, profile header, config row, wizard form, divider, theme toggle",
        "A sixth component taste sweep carries the existing-token treatment into content",
        "message bubble, conversation item, post card, comment, video card, channel card",
        "A seventh component taste sweep carries the existing-token treatment into data",
        "spinner, infinite scroll, bar chart, donut chart, number ticker, and animated counter",
        "An eighth component taste sweep applies the existing-token treatment to special form controls",
        "radio labels, file inputs, star ratings, thumbs, segmented labels, number scale",
        "A ninth component taste sweep applies the existing-token treatment to site and resource metadata",
        "site nav/footer links, feature sections, bento surfaces, resource cards, resource index",
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


def test_navigation_and_disclosure_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "breadcrumbs": "026_breadcrumbs.css",
            "sidebar": "029_sidebar.css",
            "drawer": "053_drawer.css",
            "accordion": "055_accordion.css",
            "route_tabs": "062_route-tabs.css",
            "tray": "065_tray.css",
            "segmented": "112_segmented-control.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name

    for name in [
        "breadcrumbs",
        "sidebar",
        "drawer",
        "accordion",
        "route_tabs",
        "tray",
        "segmented",
    ]:
        assert "line-height: var(--chirpui-line-height-tight);" in partials[name]

    for name in ["drawer", "accordion", "tray"]:
        assert "line-height: var(--chirpui-line-height-normal);" in partials[name]

    for name in ["sidebar", "route_tabs"]:
        assert "font-variant-numeric: tabular-nums;" in partials[name]

    assert ".chirpui-breadcrumbs__current" in partials["breadcrumbs"]
    assert "font-weight: var(--chirpui-ui-font-weight-normal);" in partials["breadcrumbs"]
    assert ".chirpui-sidebar__link--active" in partials["sidebar"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["sidebar"]
    assert ".chirpui-drawer__title" in partials["drawer"]
    assert "font-weight: var(--chirpui-ui-font-weight-semibold);" in partials["drawer"]
    assert ".chirpui-accordion__trigger-text" in partials["accordion"]
    assert "overflow-wrap: anywhere;" in partials["accordion"]
    assert ".chirpui-route-tab__badge" in partials["route_tabs"]
    assert "font-weight: var(--chirpui-ui-font-weight-semibold);" in partials["route_tabs"]
    assert ".chirpui-tray__body" in partials["tray"]
    assert "font-size: var(--chirpui-font-sm);" in partials["tray"]
    assert ".chirpui-segmented__option--active" in partials["segmented"]
    assert "font-weight: var(--chirpui-ui-font-weight-semibold);" in partials["segmented"]


def test_small_control_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "inline_edit": "007_inline-edit-field.css",
            "logo": "028_logo.css",
            "stepper": "030_stepper.css",
            "dropdown_menu": "064_dropdown-menu.css",
            "app_shell_sidebar": "084_app-shell-sidebar.css",
            "shimmer_button": "090_shimmer-button.css",
            "ripple_button": "091_ripple-button.css",
            "pulsing_button": "104_pulsing-button.css",
            "animated_stat": "107_animated-stat-card.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name

    for name in [
        "inline_edit",
        "logo",
        "stepper",
        "dropdown_menu",
        "shimmer_button",
        "ripple_button",
        "pulsing_button",
        "animated_stat",
    ]:
        assert "line-height: var(--chirpui-line-height-tight);" in partials[name]

    for name in ["stepper", "animated_stat"]:
        assert "font-variant-numeric: tabular-nums;" in partials[name]

    assert ".chirpui-inline-edit--display .chirpui-inline-edit__value" in partials["inline_edit"]
    assert "overflow-wrap: anywhere;" in partials["inline_edit"]
    assert ".chirpui-logo__text" in partials["logo"]
    assert "line-height: var(--chirpui-line-height-tight);" in partials["logo"]
    assert ".chirpui-stepper__check" in partials["stepper"]
    assert "font-size: var(--chirpui-font-sm);" in partials["stepper"]
    assert ".chirpui-dropdown__item--selected" in partials["dropdown_menu"]
    assert "font-weight: var(--chirpui-ui-font-weight-semibold);" in partials["dropdown_menu"]
    assert ".chirpui-sidebar__section > summary::after" in partials["app_shell_sidebar"]
    assert "font-size: var(--chirpui-font-xs);" in partials["app_shell_sidebar"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["shimmer_button"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["ripple_button"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["pulsing_button"]
    assert ".chirpui-animated-stat-card__trend" in partials["animated_stat"]


def test_header_setup_and_affordance_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "entity_header": "006_entity-header.css",
            "divider": "009_divider.css",
            "profile_header": "023_profile-header.css",
            "wizard_form": "031_wizard-form.css",
            "config_row": "034_config-row.css",
            "theme_toggle": "063_theme-toggle.css",
            "tooltip": "110_tooltip.css",
            "icon_button": "111_icon-button.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name

    for name in [
        "entity_header",
        "divider",
        "profile_header",
        "config_row",
        "theme_toggle",
        "icon_button",
    ]:
        assert "line-height: var(--chirpui-line-height-tight);" in partials[name]

    for name in ["profile_header", "wizard_form", "config_row"]:
        assert "line-height: var(--chirpui-line-height-normal);" in partials[name]

    assert ".chirpui-entity-header__meta" in partials["entity_header"]
    assert "color: var(--chirpui-text-muted);" in partials["entity_header"]
    assert ".chirpui-divider__text" in partials["divider"]
    assert ".chirpui-profile-header__stats" in partials["profile_header"]
    assert "font-variant-numeric: tabular-nums;" in partials["profile_header"]
    assert (
        ".chirpui-wizard-form__body > :where(:not(script, style, template))"
        in partials["wizard_form"]
    )
    assert ".chirpui-config-row__label" in partials["config_row"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["config_row"]
    assert ".chirpui-theme-toggle__icon" in partials["theme_toggle"]
    assert "font-size: var(--chirpui-ui-lg);" in partials["theme_toggle"]
    assert ".chirpui-tooltip__bubble" in partials["tooltip"]
    assert "overflow-wrap: anywhere;" in partials["tooltip"]
    assert ".chirpui-icon-btn" in partials["icon_button"]


def test_content_and_media_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "message": "016_message-bubble-and-thread.css",
            "conversation": "019_conversation-list-and-item.css",
            "post": "021_post-card.css",
            "comment": "022_comment-and-comment-thread.css",
            "video": "046_video-card.css",
            "channel": "047_channel-card.css",
            "playlist": "050_playlist.css",
            "chapter": "051_chapter-list.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name

    for name in [
        "message",
        "conversation",
        "post",
        "comment",
        "video",
        "channel",
        "playlist",
        "chapter",
    ]:
        assert "line-height: var(--chirpui-line-height-tight);" in partials[name]

    for name in ["message", "conversation", "post", "comment", "chapter"]:
        assert "line-height: var(--chirpui-line-height-normal);" in partials[name]

    for name in ["conversation", "post", "comment", "video", "channel", "playlist", "chapter"]:
        assert "font-variant-numeric: tabular-nums;" in partials[name]

    assert ".chirpui-message-bubble" in partials["message"]
    assert "overflow-wrap: anywhere;" in partials["message"]
    assert ".chirpui-conversation-item__unread" in partials["conversation"]
    assert ".chirpui-post-card__time" in partials["post"]
    assert ".chirpui-comment__replies-link" in partials["comment"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["comment"]
    assert ".chirpui-video-card__duration" in partials["video"]
    assert ".chirpui-channel-card__subscribers" in partials["channel"]
    assert ".chirpui-playlist-item__duration" in partials["playlist"]
    assert ".chirpui-chapter-item__timestamp" in partials["chapter"]


def test_data_and_loading_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "spinner": "073_spinner.css",
            "infinite_scroll": "076_infinite-scroll.css",
            "bar_chart": "080_bar-chart.css",
            "donut": "081_donut-chart.css",
            "number_ticker": "094_number-ticker.css",
            "animated_counter": "103_animated-counter.css",
        }.items()
    }

    for name, text in partials.items():
        assert "--chirpui-component-role" not in text, name
        assert "--chirpui-type-role" not in text, name
        assert "font-weight: 500;" not in text, name
        assert "font-weight: 400;" not in text, name

    for name in [
        "spinner",
        "bar_chart",
        "donut",
        "number_ticker",
        "animated_counter",
    ]:
        assert "line-height: var(--chirpui-line-height-tight);" in partials[name]

    assert "line-height: var(--chirpui-line-height-normal);" in partials["infinite_scroll"]

    for name in ["bar_chart", "donut", "number_ticker", "animated_counter"]:
        assert "font-variant-numeric: tabular-nums;" in partials[name]

    assert ".chirpui-spinner--sm { font-size: var(--chirpui-font-xs); }" in partials["spinner"]
    assert ".chirpui-infinite-scroll__loading" in partials["infinite_scroll"]
    assert "overflow-wrap: anywhere;" in partials["infinite_scroll"]
    assert ".chirpui-bar-chart__label" in partials["bar_chart"]
    assert "font-weight: var(--chirpui-ui-font-weight-medium);" in partials["bar_chart"]
    assert ".chirpui-donut__caption" in partials["donut"]
    assert "font-weight: var(--chirpui-ui-font-weight-normal);" in partials["donut"]
    assert ".chirpui-number-ticker__value" in partials["number_ticker"]
    assert ".chirpui-animated-counter__label" in partials["animated_counter"]


def test_special_form_control_taste_sweep_uses_existing_tokens() -> None:
    text = (
        ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / "070_form-fields.css"
    ).read_text(encoding="utf-8")

    for phrase in [
        "--chirpui-component-role",
        "--chirpui-type-role",
        "font-weight: 500;",
        "font-weight: 400;",
        "font-size: 1.125rem;",
        "font-size: 1.5rem;",
        "font-size: 2rem;",
    ]:
        assert phrase not in text

    for signal in [
        ".chirpui-field__radio-label",
        "font-weight: var(--chirpui-ui-font-weight-normal);",
        ".chirpui-field__file::file-selector-button",
        "font-weight: var(--chirpui-ui-font-weight-medium);",
        ".chirpui-star-rating__label",
        "font-size: var(--chirpui-font-2xl);",
        ".chirpui-star-rating--lg .chirpui-star-rating__label",
        "font-size: var(--chirpui-prose-3xl);",
        ".chirpui-thumbs__label",
        ".chirpui-segmented > .chirpui-segmented__input:checked + .chirpui-segmented__label",
        ".chirpui-number-scale__label",
        "font-variant-numeric: tabular-nums;",
        ".chirpui-sortable__handle",
        ".chirpui-dnd__handle",
        ".chirpui-field__range-value",
        "line-height: var(--chirpui-line-height-tight);",
    ]:
        assert signal in text


def test_site_resource_metadata_taste_sweep_uses_existing_tokens() -> None:
    partials = {
        name: (ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials" / filename).read_text(
            encoding="utf-8"
        )
        for name, filename in {
            "row_enhancements": "158_row-component-enhancements.css",
            "resource_card": "159_resource-card.css",
            "resource_index": "160_resource-index.css",
            "navigation_metadata": "161_navigation-metadata-authoring.css",
        }.items()
    }

    for phrase in [
        "font-weight: 500;",
        "font-size: 0.75em;",
        "font-size: 0.85em;",
        "line-height: 1.2;",
        "line-height: var(--chirpui-line-height-relaxed, 1.65);",
    ]:
        assert phrase not in partials["row_enhancements"]

    for signal in [
        ".chirpui-site-nav__link",
        "font-weight: var(--chirpui-ui-font-weight-medium);",
        ".chirpui-site-nav__link--external::after",
        ".chirpui-site-footer__link-glyph",
        ".chirpui-feature-section__title",
        "font-size: var(--chirpui-prose-2xl);",
        ".chirpui-surface__title",
        ".chirpui-surface__body",
        "line-height: var(--chirpui-line-height-normal);",
    ]:
        assert signal in partials["row_enhancements"]

    assert ".chirpui-resource-card__description" in partials["resource_card"]
    assert "font-size: var(--chirpui-font-sm);" in partials["resource_card"]
    assert ".chirpui-resource-index" in partials["resource_index"]
    assert "font-size: var(--chirpui-font-base);" in partials["resource_index"]
    assert ".chirpui-token-input__remove" in partials["navigation_metadata"]
    assert "font-size: var(--chirpui-font-sm);" in partials["navigation_metadata"]
