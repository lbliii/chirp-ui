"""Component descriptors — single source of truth for chirp-ui's BEM API surface.

Each :class:`ComponentDescriptor` declares the full public contract of a component:
block name, allowed variants (mutually exclusive), sizes, boolean modifiers
(additive), BEM elements, Kida slot names, and overridable CSS custom properties.

Downstream consumers:

* ``VARIANT_REGISTRY`` / ``SIZE_REGISTRY`` in :mod:`chirp_ui.validation` derive
  from ``COMPONENTS``.
* The ``bem()`` filter validates against descriptors when strict mode is on.
* Contract tests auto-generate expected CSS class names from descriptors.
* :func:`design_system_report` exposes the full surface for introspection.
"""

from dataclasses import dataclass
from typing import TypedDict

__all__ = [
    "COMPONENTS",
    "ComponentDescriptor",
    "DesignSystemReport",
    "DesignSystemStats",
    "design_system_report",
]


@dataclass(frozen=True, slots=True)
class ComponentDescriptor:
    """Frozen description of a single chirp-ui component's public CSS API.

    Fields
    ------
    block : str
        BEM block name (e.g. ``"btn"``).  CSS class becomes ``chirpui-{block}``.
    variants : tuple[str, ...]
        Mutually-exclusive modifiers (``chirpui-{block}--{variant}``).
        Empty string ``""`` means "no variant class emitted".
    sizes : tuple[str, ...]
        Size modifiers (``chirpui-{block}--{size}``).
    modifiers : tuple[str, ...]
        Additive boolean modifiers that can combine with variant/size
        (e.g. ``"loading"`` → ``chirpui-btn--loading``).
    elements : tuple[str, ...]
        BEM elements (``chirpui-{block}__{element}``).
    slots : tuple[str, ...]
        Kida ``{% slot %}`` names the macro defines (``""`` = default slot).
    tokens : tuple[str, ...]
        Component-scoped CSS custom properties (override knobs for theming).
    template : str
        Filename in ``templates/chirpui/`` (e.g. ``"button.html"``).
    category : str
        Grouping label for documentation/introspection.
    """

    block: str
    variants: tuple[str, ...] = ()
    sizes: tuple[str, ...] = ()
    modifiers: tuple[str, ...] = ()
    elements: tuple[str, ...] = ()
    slots: tuple[str, ...] = ()
    tokens: tuple[str, ...] = ()
    template: str = ""
    category: str = ""


# ---------------------------------------------------------------------------
# Component registry
#
# Start with components that already have VARIANT_REGISTRY / SIZE_REGISTRY
# entries, plus high-traffic components (card, tabs, modal, dropdown).
# Remaining 140+ templates will be added incrementally as they are touched.
# ---------------------------------------------------------------------------

COMPONENTS: dict[str, ComponentDescriptor] = {
    # -- Controls -----------------------------------------------------------
    "btn": ComponentDescriptor(
        block="btn",
        variants=("", "primary", "ghost", "danger", "success", "warning"),
        sizes=("", "sm", "md", "lg"),
        modifiers=("loading",),
        elements=("icon", "label", "spinner"),
        slots=("",),
        tokens=(
            "--chirpui-btn-bg",
            "--chirpui-btn-color",
            "--chirpui-btn-border",
            "--chirpui-btn-radius",
        ),
        template="button.html",
        category="control",
    ),
    "icon-btn": ComponentDescriptor(
        block="icon-btn",
        variants=("", "default", "primary", "ghost", "danger"),
        sizes=("", "sm", "md", "lg"),
        template="icon_btn.html",
        category="control",
    ),
    "shimmer-btn": ComponentDescriptor(
        block="shimmer-btn",
        variants=("", "default", "primary"),
        sizes=("", "sm", "md", "lg"),
        template="shimmer_button.html",
        category="effect",
    ),
    "ripple-btn": ComponentDescriptor(
        block="ripple-btn",
        variants=("", "default", "primary"),
        sizes=("", "sm", "md", "lg"),
        template="ripple_button.html",
        category="effect",
    ),
    "pulsing-btn": ComponentDescriptor(
        block="pulsing-btn",
        variants=("", "default", "primary", "success", "danger"),
        template="pulsing_button.html",
        category="effect",
    ),
    # -- Feedback -----------------------------------------------------------
    "alert": ComponentDescriptor(
        block="alert",
        variants=("info", "success", "warning", "error"),
        elements=("icon", "body", "title", "actions", "close"),
        slots=("", "actions"),
        template="alert.html",
        category="feedback",
    ),
    "badge": ComponentDescriptor(
        block="badge",
        variants=(
            "primary",
            "success",
            "warning",
            "error",
            "muted",
            "info",
            "custom",
            "custom-solid",
        ),
        elements=("icon", "text"),
        slots=("",),
        tokens=("--chirpui-badge-color", "--chirpui-badge-text"),
        template="badge.html",
        category="feedback",
    ),
    "toast": ComponentDescriptor(
        block="toast",
        variants=("info", "success", "warning", "error"),
        template="toast.html",
        category="feedback",
    ),
    "confirm": ComponentDescriptor(
        block="confirm",
        variants=("default", "danger"),
        template="confirm.html",
        category="feedback",
    ),
    "skeleton": ComponentDescriptor(
        block="skeleton",
        variants=("", "avatar", "text", "card"),
        template="skeleton.html",
        category="feedback",
    ),
    "progress-bar": ComponentDescriptor(
        block="progress-bar",
        variants=("gold", "radiant", "success", "watched", "custom"),
        sizes=("sm", "md", "lg"),
        template="progress.html",
        category="feedback",
    ),
    "status-indicator": ComponentDescriptor(
        block="status-indicator",
        variants=("default", "success", "warning", "error", "info", "primary", "custom"),
        template="status.html",
        category="feedback",
    ),
    "notification-dot": ComponentDescriptor(
        block="notification-dot",
        variants=("", "default", "error", "success", "warning"),
        sizes=("", "sm", "md", "lg"),
        template="notification_dot.html",
        category="feedback",
    ),
    "streaming_bubble": ComponentDescriptor(
        block="streaming-bubble",
        variants=("", "content", "thinking", "error"),
        template="streaming.html",
        category="feedback",
    ),
    # -- Containers ---------------------------------------------------------
    "card": ComponentDescriptor(
        block="card",
        modifiers=(
            "collapsible",
            "hoverable",
            "gradient-border",
            "gradient-header",
            "link",
            "linked",
        ),
        elements=(
            "header",
            "header-content",
            "header-actions",
            "header-badges",
            "header-subtitle",
            "title",
            "icon",
            "media",
            "body",
            "body-actions",
            "footer",
            "footer-wrap",
            "top-meta",
            "main-link",
        ),
        slots=("", "header_actions", "media", "body_actions", "footer"),
        template="card.html",
        category="container",
    ),
    "surface": ComponentDescriptor(
        block="surface",
        variants=(
            "default",
            "muted",
            "elevated",
            "accent",
            "gradient-subtle",
            "gradient-accent",
            "gradient-border",
            "gradient-mesh",
            "glass",
            "frosted",
            "smoke",
        ),
        modifiers=("full", "no-padding", "bento"),
        elements=("eyebrow", "title", "lede", "body"),
        template="surface.html",
        category="container",
    ),
    "modal": ComponentDescriptor(
        block="modal",
        sizes=("sm", "md", "lg"),
        elements=("header", "title", "header-actions", "close", "body", "footer"),
        slots=("", "header_actions", "footer"),
        template="modal.html",
        category="container",
    ),
    "panel": ComponentDescriptor(
        block="panel",
        template="panel.html",
        category="container",
    ),
    "overlay": ComponentDescriptor(
        block="overlay",
        variants=("dark", "gradient-bottom", "gradient-top"),
        template="overlay.html",
        category="container",
    ),
    # -- Navigation ---------------------------------------------------------
    "tabs": ComponentDescriptor(
        block="tabs",
        slots=("",),
        template="tabs.html",
        category="navigation",
    ),
    "tab": ComponentDescriptor(
        block="tab",
        modifiers=("active",),
        template="tabs.html",
        category="navigation",
    ),
    "dropdown": ComponentDescriptor(
        block="dropdown",
        elements=("trigger", "menu", "header", "footer"),
        slots=("", "header", "footer"),
        template="dropdown.html",
        category="navigation",
    ),
    "dropdown__item": ComponentDescriptor(
        block="dropdown__item",
        variants=("default", "danger", "muted"),
        template="dropdown_menu.html",
        category="navigation",
    ),
    "breadcrumbs": ComponentDescriptor(
        block="breadcrumbs",
        template="breadcrumbs.html",
        category="navigation",
    ),
    "tooltip": ComponentDescriptor(
        block="tooltip",
        variants=("top", "bottom", "left", "right"),
        template="tooltip.html",
        category="navigation",
    ),
    # -- Layout -------------------------------------------------------------
    "page_header": ComponentDescriptor(
        block="page-header",
        variants=("default", "compact"),
        template="document_header.html",
        category="layout",
    ),
    "section_header": ComponentDescriptor(
        block="section-header",
        variants=("default", "inline"),
        template="document_header.html",
        category="layout",
    ),
    "description_list": ComponentDescriptor(
        block="description-list",
        variants=("stacked", "horizontal"),
        template="description_list.html",
        category="layout",
    ),
    "hero": ComponentDescriptor(
        block="hero",
        variants=("solid", "muted", "gradient", "mesh", "animated-gradient"),
        template="hero.html",
        category="layout",
    ),
    "page_hero": ComponentDescriptor(
        block="page-hero",
        variants=("editorial", "minimal"),
        template="hero.html",
        category="layout",
    ),
    "message_bubble": ComponentDescriptor(
        block="message-bubble",
        variants=("default", "user", "assistant", "system"),
        template="message_bubble.html",
        category="layout",
    ),
    # -- Effects & decorative -----------------------------------------------
    "aura": ComponentDescriptor(
        block="aura",
        sizes=("sm", "md", "lg"),
        modifiers=("mirror",),
        elements=("content",),
        slots=("",),
        template="aura.html",
        category="effect",
    ),
    "aura_tone": ComponentDescriptor(
        block="aura",
        variants=("accent", "warm", "cool", "muted", "primary"),
        category="effect",
    ),
    "border-beam": ComponentDescriptor(
        block="border-beam",
        variants=("", "default", "accent", "success", "warning"),
        sizes=("", "sm", "md", "lg"),
        template="border_beam.html",
        category="effect",
    ),
    "glow-card": ComponentDescriptor(
        block="glow-card",
        variants=("", "default", "accent", "muted"),
        sizes=("", "sm", "md", "lg"),
        template="glow_card.html",
        category="effect",
    ),
    "spotlight-card": ComponentDescriptor(
        block="spotlight-card",
        variants=("", "default", "accent"),
        template="spotlight_card.html",
        category="effect",
    ),
    "number-ticker": ComponentDescriptor(
        block="number-ticker",
        variants=("", "default", "mono"),
        sizes=("", "sm", "md", "lg", "xl"),
        template="number_ticker.html",
        category="effect",
    ),
    "animated-counter": ComponentDescriptor(
        block="animated-counter",
        variants=("", "default", "mono"),
        template="animated_counter.html",
        category="effect",
    ),
    "marquee": ComponentDescriptor(
        block="marquee",
        variants=("", "default", "reverse"),
        template="marquee.html",
        category="effect",
    ),
    "meteor": ComponentDescriptor(
        block="meteor",
        variants=("", "default", "accent", "muted"),
        template="meteor.html",
        category="effect",
    ),
    "text-reveal": ComponentDescriptor(
        block="text-reveal",
        variants=("", "default", "gradient"),
        template="text_reveal.html",
        category="effect",
    ),
    "dock": ComponentDescriptor(
        block="dock",
        variants=("", "default", "glass"),
        sizes=("", "sm", "md", "lg"),
        template="dock.html",
        category="effect",
    ),
    "particle-bg": ComponentDescriptor(
        block="particle-bg",
        variants=("", "default", "accent", "muted"),
        template="particle_bg.html",
        category="effect",
    ),
    "typewriter": ComponentDescriptor(
        block="typewriter",
        variants=("", "fast", "slow"),
        template="typewriter.html",
        category="effect",
    ),
    "glitch": ComponentDescriptor(
        block="glitch",
        variants=("", "subtle", "intense"),
        template="glitch_text.html",
        category="effect",
    ),
    "neon": ComponentDescriptor(
        block="neon",
        variants=("cyan", "magenta", "green", "orange", "blue", "red"),
        template="neon_text.html",
        category="effect",
    ),
    "aurora": ComponentDescriptor(
        block="aurora",
        variants=("", "intense", "subtle"),
        template="aurora.html",
        category="effect",
    ),
    "scanline": ComponentDescriptor(
        block="scanline",
        variants=("", "heavy", "crt"),
        template="scanline.html",
        category="effect",
    ),
    "grain": ComponentDescriptor(
        block="grain",
        variants=("", "heavy", "subtle"),
        template="grain.html",
        category="effect",
    ),
    "orbit": ComponentDescriptor(
        block="orbit",
        variants=("", "sm", "lg", "xl"),
        sizes=("", "sm", "lg", "xl"),
        template="orbit.html",
        category="effect",
    ),
    "sparkle": ComponentDescriptor(
        block="sparkle",
        variants=("", "gold", "white", "rainbow"),
        sizes=("", "sm", "md", "lg"),
        template="sparkle.html",
        category="effect",
    ),
    "confetti": ComponentDescriptor(
        block="confetti",
        variants=("",),
        template="confetti.html",
        category="effect",
    ),
    "wobble": ComponentDescriptor(
        block="wobble",
        variants=("wobble", "jello", "rubber-band", "bounce-in"),
        template="wobble.html",
        category="effect",
    ),
    # -- ASCII background effects -------------------------------------------
    "symbol-rain": ComponentDescriptor(
        block="symbol-rain",
        variants=("", "default", "accent", "gold", "muted"),
        template="symbol_rain.html",
        category="effect",
    ),
    "holy-light": ComponentDescriptor(
        block="holy-light",
        variants=("", "default", "gold", "silver", "holy"),
        template="holy_light.html",
        category="effect",
    ),
    "rune-field": ComponentDescriptor(
        block="rune-field",
        variants=("", "default", "arcane", "frost", "ember"),
        template="rune_field.html",
        category="effect",
    ),
    "constellation": ComponentDescriptor(
        block="constellation",
        variants=("", "default", "warm", "cool", "mono"),
        template="constellation.html",
        category="effect",
    ),
    # -- ASCII primitives ---------------------------------------------------
    "ascii-border": ComponentDescriptor(
        block="ascii-border",
        variants=("", "single", "double", "rounded", "heavy", "spin"),
        template="ascii_border.html",
        category="ascii",
    ),
    "ascii-divider": ComponentDescriptor(
        block="ascii-divider",
        variants=(
            "",
            "single",
            "double",
            "heavy",
            "dots",
            "spin",
            "spin-reverse",
            "spin-drift",
        ),
        template="ascii_divider.html",
        category="ascii",
    ),
    "ascii-sparkline": ComponentDescriptor(
        block="ascii-sparkline",
        variants=("", "default", "accent", "muted", "gradient"),
        template="ascii_sparkline.html",
        category="ascii",
    ),
    "ascii-progress": ComponentDescriptor(
        block="ascii-progress",
        variants=("", "default", "accent", "success", "warning"),
        template="ascii_progress.html",
        category="ascii",
    ),
    "ascii-empty": ComponentDescriptor(
        block="ascii-empty",
        variants=("", "default", "muted", "accent"),
        template="ascii_empty.html",
        category="ascii",
    ),
    "ascii-badge": ComponentDescriptor(
        block="ascii-badge",
        variants=("", "default", "success", "warning", "error", "accent", "muted"),
        template="ascii_badge.html",
        category="ascii",
    ),
    "ascii-spinner": ComponentDescriptor(
        block="ascii-spinner",
        variants=("", "braille", "box", "dots", "arrows", "blocks"),
        template="ascii_spinner.html",
        category="ascii",
    ),
    "ascii-skeleton": ComponentDescriptor(
        block="ascii-skeleton",
        variants=("", "text", "card", "avatar", "heading"),
        template="ascii_skeleton.html",
        category="ascii",
    ),
    "ascii-toggle": ComponentDescriptor(
        block="ascii-toggle",
        variants=("", "default", "success", "danger", "accent"),
        sizes=("", "sm", "md", "lg"),
        template="ascii_toggle.html",
        category="ascii",
    ),
    "ascii-switch": ComponentDescriptor(
        block="ascii-switch",
        variants=("", "default", "success", "danger", "accent"),
        sizes=("", "sm", "md", "lg"),
        template="ascii_toggle.html",
        category="ascii",
    ),
    "ascii-table": ComponentDescriptor(
        block="ascii-table",
        variants=("single", "double", "heavy", "rounded"),
        template="ascii_table.html",
        category="ascii",
    ),
    "ascii-indicator": ComponentDescriptor(
        block="ascii-indicator",
        variants=("success", "warning", "error", "muted", "accent"),
        template="ascii_indicator.html",
        category="ascii",
    ),
    "ascii-tile-btn": ComponentDescriptor(
        block="ascii-tile-btn",
        variants=("", "default", "success", "warning", "danger", "accent"),
        template="ascii_tile_btn.html",
        category="ascii",
    ),
    "ascii-knob": ComponentDescriptor(
        block="ascii-knob",
        variants=("", "default", "accent"),
        template="ascii_knob.html",
        category="ascii",
    ),
    "ascii-fader": ComponentDescriptor(
        block="ascii-fader",
        variants=("", "default", "accent", "success", "warning", "danger"),
        template="ascii_fader.html",
        category="ascii",
    ),
    "ascii-vu": ComponentDescriptor(
        block="ascii-vu",
        variants=("", "default", "accent", "success", "warning"),
        template="ascii_vu_meter.html",
        category="ascii",
    ),
    "ascii-7seg": ComponentDescriptor(
        block="ascii-7seg",
        variants=("", "default", "accent", "success", "warning", "error"),
        template="ascii_7seg.html",
        category="ascii",
    ),
    "ascii-checkbox": ComponentDescriptor(
        block="ascii-checkbox",
        variants=("", "default", "accent", "success", "danger"),
        template="ascii_checkbox.html",
        category="ascii",
    ),
    "ascii-radio-group": ComponentDescriptor(
        block="ascii-radio-group",
        variants=("", "default", "accent"),
        template="ascii_radio.html",
        category="ascii",
    ),
    "ascii-stepper": ComponentDescriptor(
        block="ascii-stepper",
        variants=("", "default", "accent", "success"),
        template="ascii_stepper.html",
        category="ascii",
    ),
    "split-flap": ComponentDescriptor(
        block="split-flap",
        variants=("", "default", "amber", "green"),
        template="ascii_split_flap.html",
        category="ascii",
    ),
    "ascii-ticker": ComponentDescriptor(
        block="ascii-ticker",
        variants=("", "default", "accent", "success", "warning", "error"),
        template="ascii_ticker.html",
        category="ascii",
    ),
    "ascii-card": ComponentDescriptor(
        block="ascii-card",
        variants=("", "single", "double", "rounded", "heavy"),
        template="ascii_card.html",
        category="ascii",
    ),
    "ascii-tabs": ComponentDescriptor(
        block="ascii-tabs",
        variants=("", "default", "accent"),
        template="ascii_tabs.html",
        category="ascii",
    ),
    "ascii-tab": ComponentDescriptor(
        block="ascii-tab",
        variants=("", "default", "accent"),
        template="ascii_tabs.html",
        category="ascii",
    ),
    "ascii-modal": ComponentDescriptor(
        block="ascii-modal",
        variants=("", "single", "double", "heavy"),
        template="ascii_modal.html",
        category="ascii",
    ),
    # -- Marketing (site mode) ----------------------------------------------
    "site-shell": ComponentDescriptor(
        block="site-shell",
        elements=("main",),
        slots=("", "header", "footer"),
        tokens=("--chirpui-site-shell-bg",),
        template="site_shell.html",
        category="marketing",
    ),
    "site-header": ComponentDescriptor(
        block="site-header",
        variants=("glass", "solid", "transparent"),
        modifiers=("sticky",),
        elements=("inner", "brand", "nav", "nav-end", "tools"),
        slots=("", "brand", "nav", "nav_end", "tools"),
        tokens=(
            "--chirpui-site-header-bg",
            "--chirpui-site-header-blur",
            "--chirpui-site-header-border",
            "--chirpui-site-header-height",
            "--chirpui-site-header-padding-inline",
            "--chirpui-site-header-max-width",
        ),
        template="site_header.html",
        category="marketing",
    ),
    "site-nav-link": ComponentDescriptor(
        block="site-nav",
        elements=("link", "glyph"),
        template="site_header.html",
        category="marketing",
    ),
    "site-footer": ComponentDescriptor(
        block="site-footer",
        variants=("columns", "centered", "simple"),
        elements=(
            "grid",
            "brand",
            "column",
            "column-title",
            "list",
            "link",
            "link-glyph",
            "rule",
            "rule-line",
            "colophon",
        ),
        slots=("", "brand", "rule", "colophon"),
        tokens=(
            "--chirpui-site-footer-bg",
            "--chirpui-site-footer-border",
            "--chirpui-site-footer-columns",
            "--chirpui-site-footer-max-width",
            "--chirpui-site-footer-padding-inline",
        ),
        template="site_footer.html",
        category="marketing",
    ),
    "band": ComponentDescriptor(
        block="band",
        variants=("default", "elevated", "accent", "glass", "gradient"),
        modifiers=("inset", "bleed", "contained"),
        elements=(),
        slots=("", "header"),
        tokens=(
            "--chirpui-band-bg",
            "--chirpui-band-border",
            "--chirpui-band-radius",
            "--chirpui-band-padding",
            "--chirpui-band-breakout",
        ),
        template="band.html",
        category="marketing",
    ),
    "feature-section": ComponentDescriptor(
        block="feature-section",
        variants=("split", "balanced", "media-dominant", "stacked", "muted", "halo"),
        modifiers=("reverse",),
        elements=(
            "copy",
            "eyebrow",
            "title",
            "body",
            "actions",
            "media",
            "halo",
        ),
        slots=("", "eyebrow", "title", "actions", "media"),
        tokens=(
            "--chirpui-feature-section-gap",
            "--chirpui-feature-section-columns",
            "--chirpui-feature-halo-color",
            "--chirpui-feature-halo-size",
        ),
        template="feature_section.html",
        category="marketing",
    ),
    "feature-stack": ComponentDescriptor(
        block="feature-stack",
        template="feature_section.html",
        category="marketing",
    ),
    # -- Composites (PR #57) ------------------------------------------------
    "settings-row-list": ComponentDescriptor(
        block="settings-row-list",
        modifiers=("hoverable", "divided", "relaxed"),
        slots=("",),
        template="settings_row.html",
        category="container",
    ),
    "settings-row": ComponentDescriptor(
        block="settings-row",
        elements=("label", "status", "detail"),
        template="settings_row.html",
        category="container",
    ),
    "install-snippet": ComponentDescriptor(
        block="install-snippet",
        elements=("label", "row", "command"),
        slots=("",),
        template="code.html",
        category="content",
    ),
    "filter-row": ComponentDescriptor(
        block="filter-row",
        slots=("",),
        template="filter_bar.html",
        category="control",
    ),
    "tag-browse": ComponentDescriptor(
        block="tag-browse",
        template="tag_browse.html",
        category="control",
    ),
    # -- Sizing-only components ---------------------------------------------
    "star-rating": ComponentDescriptor(
        block="star-rating",
        sizes=("", "sm", "md", "lg"),
        category="control",
    ),
    "thumbs": ComponentDescriptor(
        block="thumbs",
        sizes=("", "sm", "md", "lg"),
        category="control",
    ),
    "segmented": ComponentDescriptor(
        block="segmented",
        sizes=("", "sm", "md", "lg"),
        template="segmented_control.html",
        category="control",
    ),
    # -- Data display -------------------------------------------------------
    "table": ComponentDescriptor(
        block="table",
        modifiers=("striped", "compact"),
        elements=(
            "caption",
            "head",
            "row",
            "th",
            "td",
            "sort",
            "avatar",
            "empty",
        ),
        slots=("", "caption"),
        template="table.html",
        category="data-display",
    ),
    "table-wrap": ComponentDescriptor(
        block="table-wrap",
        modifiers=("sticky",),
        template="table.html",
        category="data-display",
    ),
    "pagination": ComponentDescriptor(
        block="pagination",
        elements=("link", "ellipsis"),
        template="pagination.html",
        category="navigation",
    ),
    "resource-index": ComponentDescriptor(
        block="resource-index",
        elements=("search", "filters", "results"),
        slots=(
            "",
            "toolbar_controls",
            "filter_primary",
            "filter_controls",
            "filter_actions",
            "selection",
            "filters_panel",
            "empty",
        ),
        template="resource_index.html",
        category="composite",
    ),
    "row-actions": ComponentDescriptor(
        block="row-actions",
        elements=("trigger",),
        template="row_actions.html",
        category="control",
    ),
    "params-table": ComponentDescriptor(
        block="params-table",
        elements=(
            "title",
            "wrap",
            "table",
            "th",
            "td",
            "code",
            "empty",
        ),
        template="params_table.html",
        category="data-display",
    ),
    "bar-chart": ComponentDescriptor(
        block="bar-chart",
        variants=("", "gold", "radiant", "success", "muted"),
        sizes=("", "sm", "md", "lg"),
        elements=("row", "label", "label-link", "track", "bar", "value"),
        template="bar_chart.html",
        category="data-display",
    ),
    "donut": ComponentDescriptor(
        block="donut",
        variants=("", "gold", "success", "muted"),
        sizes=("", "sm", "md", "lg"),
        elements=("ring", "center", "caption"),
        tokens=(
            "--chirpui-donut-size",
            "--chirpui-donut-pct",
            "--chirpui-donut-fill",
        ),
        template="donut.html",
        category="data-display",
    ),
    "metric-grid": ComponentDescriptor(
        block="metric-grid",
        slots=("",),
        template="metric_grid.html",
        category="layout",
    ),
    "metric-card": ComponentDescriptor(
        block="metric-card",
        elements=(
            "stat",
            "trend",
            "trend-arrow",
            "icon-badge",
            "top",
            "values",
            "hint",
            "footer",
        ),
        template="metric_grid.html",
        category="data-display",
    ),
    "stat": ComponentDescriptor(
        block="stat",
        elements=("value", "label", "icon"),
        template="stat.html",
        category="data-display",
    ),
    "animated-stat-card": ComponentDescriptor(
        block="animated-stat-card",
        elements=("trend",),
        template="animated_stat_card.html",
        category="data-display",
    ),
    "list": ComponentDescriptor(
        block="list",
        modifiers=("bordered",),
        elements=("item", "link"),
        slots=("",),
        template="list.html",
        category="data-display",
    ),
    "sortable": ComponentDescriptor(
        block="sortable",
        elements=("item", "handle", "content", "remove"),
        slots=("",),
        template="sortable_list.html",
        category="interactive",
    ),
    "timeline": ComponentDescriptor(
        block="timeline",
        modifiers=("on-muted", "on-accent", "hoverable"),
        elements=(
            "item",
            "dot",
            "content",
            "header",
            "header-actions",
            "title",
            "date",
            "body",
            "icon",
            "avatar",
            "time",
            "link-overlay",
        ),
        slots=("",),
        template="timeline.html",
        category="data-display",
    ),
    "tree": ComponentDescriptor(
        block="tree",
        elements=("item", "node", "label"),
        slots=("",),
        template="tree_view.html",
        category="data-display",
    ),
    "chapter-list": ComponentDescriptor(
        block="chapter-list",
        elements=("summary", "summary-text", "summary-actions", "list"),
        slots=("", "summary_actions"),
        template="chapter_list.html",
        category="data-display",
    ),
    "chapter-item": ComponentDescriptor(
        block="chapter-item",
        elements=("link", "timestamp", "title"),
        template="chapter_list.html",
        category="data-display",
    ),
    "playlist": ComponentDescriptor(
        block="playlist",
        elements=("header", "title", "header-actions", "list"),
        slots=("", "header_actions"),
        template="playlist.html",
        category="data-display",
    ),
    "playlist-item": ComponentDescriptor(
        block="playlist-item",
        modifiers=("active",),
        elements=("link", "title", "duration"),
        template="playlist.html",
        category="data-display",
    ),
    "conversation-list": ComponentDescriptor(
        block="conversation-list",
        slots=("",),
        template="conversation_list.html",
        category="navigation",
    ),
    "conversation-item": ComponentDescriptor(
        block="conversation-item",
        modifiers=("muted",),
        elements=(
            "avatar",
            "body",
            "meta",
            "name",
            "time",
            "preview",
            "actions",
            "unread",
        ),
        slots=("", "actions"),
        template="conversation_item.html",
        category="navigation",
    ),
    "post-card": ComponentDescriptor(
        block="post-card",
        elements=(
            "header",
            "author",
            "avatar",
            "meta",
            "name",
            "handle",
            "time",
            "body",
            "media",
            "actions",
        ),
        slots=("", "avatar", "media", "actions"),
        template="post_card.html",
        category="data-display",
    ),
    "channel-card": ComponentDescriptor(
        block="channel-card",
        elements=("link", "info", "name", "subscribers", "body", "actions"),
        slots=("", "body"),
        template="channel_card.html",
        category="data-display",
    ),
    "video-card": ComponentDescriptor(
        block="video-card",
        elements=(
            "link",
            "thumbnail",
            "actions",
            "duration",
            "body",
            "title",
            "channel",
            "channel-link",
            "meta",
        ),
        slots=("actions",),
        template="video_card.html",
        category="data-display",
    ),
    "video-thumbnail": ComponentDescriptor(
        block="video-thumbnail",
        elements=("img-wrap", "play", "duration", "progress"),
        tokens=("--chirpui-video-aspect-ratio",),
        template="video_thumbnail.html",
        category="media",
    ),
    "index-card": ComponentDescriptor(
        block="index-card",
        elements=("header", "badge", "title", "description"),
        template="index_card.html",
        category="navigation",
    ),
    "trending-tag": ComponentDescriptor(
        block="trending-tag",
        modifiers=("up",),
        elements=("hash", "count"),
        template="trending_tag.html",
        category="data-display",
    ),
    # -- Layout & shell (Sprint 2) ------------------------------------------
    "app-shell": ComponentDescriptor(
        block="app-shell",
        modifiers=("sidebar-collapsible", "sidebar-collapsed"),
        elements=(
            "topbar",
            "brand",
            "topbar-start",
            "topbar-center",
            "topbar-end",
            "shell-actions",
            "sidebar",
            "sidebar-resize",
            "main",
        ),
        slots=("", "brand", "topbar", "topbar_end", "sidebar"),
        tokens=(
            "--chirpui-sidebar-width",
            "--chirpui-sidebar-collapsed-width",
            "--chirpui-sidebar-expanded-width",
            "--chirpui-sidebar-max-width",
        ),
        template="app_shell.html",
        category="layout",
    ),
    "workspace-shell": ComponentDescriptor(
        block="workspace-shell",
        elements=(
            "header",
            "heading",
            "title",
            "subtitle",
            "toolbar",
            "layout",
            "content-layout",
            "main",
        ),
        slots=("", "toolbar", "inspector"),
        template="workspace_shell.html",
        category="layout",
    ),
    "shell-actions": ComponentDescriptor(
        block="shell-actions",
        elements=("group",),
        slots=("",),
        template="shell_actions.html",
        category="layout",
    ),
    "sidebar": ComponentDescriptor(
        block="sidebar",
        elements=(
            "header",
            "nav",
            "section",
            "section-title",
            "link",
            "icon",
            "label",
        ),
        slots=("", "header", "footer"),
        tokens=(
            "--chirpui-sidebar-active-bg",
            "--chirpui-sidebar-active-color",
            "--chirpui-sidebar-section-gap",
            "--chirpui-sidebar-link-gap",
        ),
        template="sidebar.html",
        category="navigation",
    ),
    "sidebar-toggle": ComponentDescriptor(
        block="sidebar-toggle",
        elements=("icon",),
        template="sidebar.html",
        category="navigation",
    ),
    "tray": ComponentDescriptor(
        block="tray",
        variants=("right", "left", "bottom"),
        modifiers=("open", "closed"),
        elements=("backdrop", "panel", "header", "title", "close", "body"),
        slots=("",),
        template="tray.html",
        category="overlay",
    ),
    "drawer": ComponentDescriptor(
        block="drawer",
        variants=("right", "left"),
        elements=("panel", "header", "title", "header-actions", "close", "body"),
        slots=("", "header_actions"),
        template="drawer.html",
        category="overlay",
    ),
    "split-layout": ComponentDescriptor(
        block="split-layout",
        variants=(
            "horizontal",
            "vertical",
            "sidebar",
            "balanced",
            "wide-primary",
            "wide-secondary",
        ),
        modifiers=("gap-sm", "gap-md", "gap-lg"),
        elements=("primary", "secondary"),
        slots=("primary", "secondary"),
        template="split_layout.html",
        category="layout",
    ),
    "split-panel": ComponentDescriptor(
        block="split-panel",
        modifiers=("vertical", "dragging"),
        elements=("pane", "handle", "handle-grip"),
        slots=("left", "right"),
        template="split_panel.html",
        category="layout",
    ),
    "chat-layout": ComponentDescriptor(
        block="chat-layout",
        modifiers=("fill",),
        elements=("main", "messages", "input", "activity", "messages-body"),
        slots=("messages", "input", "activity"),
        tokens=(
            "--chirpui-chat-layout-gap",
            "--chirpui-chat-layout-messages-padding",
            "--chirpui-chat-layout-input-padding",
            "--chirpui-chat-layout-input-border",
            "--chirpui-chat-layout-activity-width",
            "--chirpui-chat-layout-min-height",
        ),
        template="chat_layout.html",
        category="layout",
    ),
    "accordion": ComponentDescriptor(
        block="accordion",
        elements=("item", "trigger", "trigger-text", "trigger-actions", "content"),
        slots=("",),
        template="accordion.html",
        category="interactive",
    ),
    # -- Forms (Sprint 3) ---------------------------------------------------
    "field": ComponentDescriptor(
        block="field",
        variants=(
            "dense",
            "error",
            "checkbox",
            "toggle",
            "range",
            "radio",
            "radio-horizontal",
        ),
        elements=(
            "label",
            "input",
            "required",
            "hint",
            "error",
            "errors",
            "checkbox",
            "file",
            "radio-group",
            "radio-option",
            "radio-label",
            "range",
            "range-header",
            "range-value",
        ),
        template="forms.html",
        category="form",
    ),
    "form-actions": ComponentDescriptor(
        block="form-actions",
        modifiers=("end",),
        template="forms.html",
        category="form",
    ),
    "form-error-summary": ComponentDescriptor(
        block="form-error-summary",
        elements=("heading", "list"),
        template="forms.html",
        category="form",
    ),
    "search-bar": ComponentDescriptor(
        block="search-bar",
        modifiers=("with-icon",),
        elements=("input", "inner", "icon", "btn"),
        template="forms.html",
        category="form",
    ),
    "input-group": ComponentDescriptor(
        block="input-group",
        elements=("input", "prefix", "suffix"),
        template="forms.html",
        category="form",
    ),
    "toggle-wrap": ComponentDescriptor(
        block="toggle-wrap",
        variants=("", "sm", "lg", "accent", "danger", "success"),
        template="forms.html",
        category="form",
    ),
    "fieldset": ComponentDescriptor(
        block="fieldset",
        elements=("legend",),
        template="forms.html",
        category="form",
    ),
    "chat-input": ComponentDescriptor(
        block="chat-input",
        elements=("composer", "field", "footer"),
        slots=("",),
        template="chat_input.html",
        category="form",
    ),
    "inline-edit": ComponentDescriptor(
        block="inline-edit",
        variants=("display", "edit"),
        elements=("value", "trigger", "icon", "form", "input", "actions"),
        template="inline_edit_field.html",
        category="form",
    ),
    "tag-input": ComponentDescriptor(
        block="tag-input",
        elements=("label", "chips", "add", "add-field"),
        template="tag_input.html",
        category="form",
    ),
    "tag": ComponentDescriptor(
        block="tag",
        elements=("remove", "remove-btn"),
        template="tag_input.html",
        category="form",
    ),
    "wizard-form": ComponentDescriptor(
        block="wizard-form",
        elements=("body",),
        template="wizard_form.html",
        category="form",
    ),
    "selection-bar": ComponentDescriptor(
        block="selection-bar",
        elements=("count", "actions"),
        slots=("",),
        template="selection_bar.html",
        category="control",
    ),
    # -- Navigation (Sprint 3) ----------------------------------------------
    "nav-tree": ComponentDescriptor(
        block="nav-tree",
        elements=(
            "header",
            "list",
            "item",
            "node",
            "label",
            "link",
            "text",
            "icon",
            "title",
        ),
        slots=("", "header"),
        template="nav_tree.html",
        category="navigation",
    ),
    "navbar": ComponentDescriptor(
        block="navbar",
        modifiers=("sticky",),
        elements=("brand", "links", "link"),
        slots=("", "brand", "end"),
        template="navbar.html",
        category="navigation",
    ),
    "navbar-dropdown": ComponentDescriptor(
        block="navbar-dropdown",
        elements=("trigger",),
        template="navbar.html",
        category="navigation",
    ),
    "nav-progress": ComponentDescriptor(
        block="nav-progress",
        template="nav_progress.html",
        category="navigation",
    ),
    "route-tab": ComponentDescriptor(
        block="route-tab",
        elements=("icon", "label", "badge"),
        template="route_tabs.html",
        category="navigation",
    ),
    "command-palette": ComponentDescriptor(
        block="command-palette",
        elements=(
            "inner",
            "input",
            "results",
            "group-title",
            "item",
            "item-label",
            "item-hint",
            "kbd",
            "trigger",
        ),
        template="command_palette.html",
        category="interactive",
    ),
    "collapse": ComponentDescriptor(
        block="collapse",
        elements=("trigger", "trigger-text", "trigger-actions", "content"),
        slots=("",),
        template="collapse.html",
        category="interactive",
    ),
    # -- Utility & remaining (Sprint 4) -------------------------------------
    "action-bar": ComponentDescriptor(
        block="action-bar",
        elements=("item", "icon", "count"),
        template="action_bar.html",
        category="control",
    ),
    "action-strip": ComponentDescriptor(
        block="action-strip",
        modifiers=("sm", "scroll", "collapse", "sticky"),
        elements=("inner", "primary", "controls", "actions"),
        slots=("",),
        template="action_strip.html",
        category="control",
    ),
    "ascii-breaker-panel": ComponentDescriptor(
        block="ascii-breaker-panel",
        modifiers=("sm",),
        elements=("title", "divider", "master", "switches", "breaker", "status"),
        template="ascii_breaker_panel.html",
        category="ascii",
    ),
    "ascii-error": ComponentDescriptor(
        block="ascii-error",
        elements=("art", "code", "heading", "desc", "action"),
        template="ascii_error.html",
        category="ascii",
    ),
    "avatar": ComponentDescriptor(
        block="avatar",
        sizes=("", "sm", "lg"),
        modifiers=("online", "offline"),
        elements=("img", "initials", "placeholder"),
        template="avatar.html",
        category="data-display",
    ),
    "avatar-stack": ComponentDescriptor(
        block="avatar-stack",
        elements=("more",),
        template="avatar_stack.html",
        category="data-display",
    ),
    "calendar": ComponentDescriptor(
        block="calendar",
        elements=(
            "header",
            "title",
            "nav",
            "nav-link",
            "weekdays",
            "grid",
            "day",
            "day-num",
            "event",
        ),
        template="calendar.html",
        category="data-display",
    ),
    "callout": ComponentDescriptor(
        block="callout",
        modifiers=(
            "info",
            "success",
            "warning",
            "error",
            "neutral",
            "on-muted",
            "on-accent",
        ),
        elements=("header", "icon", "title", "header-actions", "body"),
        slots=("", "header_actions"),
        template="callout.html",
        category="feedback",
    ),
    "carousel": ComponentDescriptor(
        block="carousel",
        modifiers=("compact", "page"),
        elements=("track", "slide", "dots", "dot"),
        slots=("",),
        template="carousel.html",
        category="interactive",
    ),
    "comment": ComponentDescriptor(
        block="comment",
        elements=(
            "header",
            "avatar",
            "meta",
            "author",
            "time",
            "body",
            "footer",
            "actions",
            "replies",
            "replies-link",
        ),
        slots=("", "actions"),
        template="comment.html",
        category="data-display",
    ),
    "config-row": ComponentDescriptor(
        block="config-row",
        elements=("label", "control", "form", "toggle-wrap", "select", "editable"),
        template="config_row.html",
        category="container",
    ),
    "divider": ComponentDescriptor(
        block="divider",
        modifiers=(
            "horizontal",
            "primary",
            "success",
            "warning",
            "error",
            "accent",
            "dotted",
            "fade",
        ),
        elements=("text",),
        template="divider.html",
        category="layout",
    ),
    "dnd": ComponentDescriptor(
        block="dnd",
        modifiers=("row", "board"),
        elements=(
            "item",
            "handle",
            "drop-indicator",
            "column",
            "column-header",
            "column-body",
            "card",
        ),
        template="dnd.html",
        category="interactive",
    ),
    "empty-panel-state": ComponentDescriptor(
        block="empty-panel-state",
        modifiers=("compact",),
        template="empty_panel_state.html",
        category="feedback",
    ),
    "entity-header": ComponentDescriptor(
        block="entity-header",
        elements=("content", "icon", "title", "meta", "actions"),
        slots=("", "actions"),
        template="entity_header.html",
        category="layout",
    ),
    "file-tree": ComponentDescriptor(
        block="file-tree",
        elements=("nav",),
        template="file_tree.html",
        category="data-display",
    ),
    "gradient-text": ComponentDescriptor(
        block="gradient-text",
        modifiers=("secondary", "rainbow", "animated"),
        template="gradient_text.html",
        category="effect",
    ),
    "hero-effects": ComponentDescriptor(
        block="hero-effects",
        template="hero_effects.html",
        category="effect",
    ),
    "fragment-island": ComponentDescriptor(
        block="fragment-island",
        template="fragment_island.html",
        category="infrastructure",
    ),
    "label-overline": ComponentDescriptor(
        block="label-overline",
        modifiers=("section",),
        template="label_overline.html",
        category="content",
    ),
    "link": ComponentDescriptor(
        block="link",
        template="link.html",
        category="navigation",
    ),
    "live-badge": ComponentDescriptor(
        block="live-badge",
        elements=("dot", "viewers"),
        template="live_badge.html",
        category="feedback",
    ),
    "logo": ComponentDescriptor(
        block="logo",
        modifiers=(
            "text",
            "image",
            "sm",
            "md",
            "lg",
            "start",
            "center",
            "end",
        ),
        elements=("img", "text"),
        template="logo.html",
        category="content",
    ),
    "media-object": ComponentDescriptor(
        block="media-object",
        modifiers=("align-center",),
        elements=("media", "body", "actions"),
        slots=("", "media", "actions"),
        template="media_object.html",
        category="layout",
    ),
    "mention": ComponentDescriptor(
        block="mention",
        template="mention.html",
        category="content",
    ),
    "message-thread": ComponentDescriptor(
        block="message-thread",
        template="message_thread.html",
        category="data-display",
    ),
    "popover": ComponentDescriptor(
        block="popover",
        elements=("trigger", "header", "footer", "panel"),
        slots=("", "header", "footer"),
        template="popover.html",
        category="overlay",
    ),
    "profile-header": ComponentDescriptor(
        block="profile-header",
        elements=(
            "cover",
            "content",
            "avatar",
            "info",
            "name",
            "bio",
            "stats",
            "action",
        ),
        slots=("", "actions"),
        template="profile_header.html",
        category="data-display",
    ),
    "reaction-pill": ComponentDescriptor(
        block="reaction-pill",
        modifiers=("active", "disabled"),
        elements=("emoji", "count"),
        template="reaction_pill.html",
        category="interactive",
    ),
    "reveal-on-scroll": ComponentDescriptor(
        block="reveal-on-scroll",
        template="reveal_on_scroll.html",
        category="effect",
    ),
    "signature": ComponentDescriptor(
        block="signature",
        elements=("code",),
        template="signature.html",
        category="content",
    ),
    "spinner": ComponentDescriptor(
        block="spinner",
        sizes=("", "sm", "md", "lg"),
        elements=("mote",),
        template="spinner.html",
        category="feedback",
    ),
    "sse-status": ComponentDescriptor(
        block="sse-status",
        modifiers=("connected", "disconnected", "error"),
        elements=("dot",),
        template="sse_status.html",
        category="feedback",
    ),
    "stepper": ComponentDescriptor(
        block="stepper",
        elements=("list", "item", "indicator", "check", "label", "connector"),
        template="stepper.html",
        category="navigation",
    ),
    "theme-toggle": ComponentDescriptor(
        block="theme-toggle",
        elements=("icon",),
        template="theme_toggle.html",
        category="control",
    ),
    "typing-indicator": ComponentDescriptor(
        block="typing-indicator",
        elements=("dot",),
        template="typing_indicator.html",
        category="feedback",
    ),
    # -- Additional blocks discovered in multi-macro files ------------------
    "copy-btn": ComponentDescriptor(
        block="copy-btn",
        variants=("", "user", "assistant", "system"),
        elements=("label", "done"),
        template="copy_button.html",
        category="control",
    ),
    "split-btn": ComponentDescriptor(
        block="split-btn",
        elements=(
            "primary",
            "dropdown",
            "trigger",
            "menu-header",
            "menu-footer",
            "menu",
        ),
        slots=("", "header", "footer"),
        template="split_button.html",
        category="control",
    ),
    "empty-state": ComponentDescriptor(
        block="empty-state",
        elements=(
            "icon",
            "illustration",
            "title",
            "code",
            "search-hint",
            "suggestions",
            "body",
            "action",
        ),
        slots=("",),
        template="empty.html",
        category="feedback",
    ),
    "filter-group": ComponentDescriptor(
        block="filter-group",
        template="filter_chips.html",
        category="control",
    ),
    "infinite-scroll": ComponentDescriptor(
        block="infinite-scroll",
        elements=("loading",),
        template="infinite_scroll.html",
        category="interactive",
    ),
    "suspense-slot": ComponentDescriptor(
        block="suspense-slot",
        template="suspense.html",
        category="infrastructure",
    ),
}


class DesignSystemStats(TypedDict):
    """Aggregate counts for the design system surface."""

    total_components: int
    total_tokens: int
    component_categories: dict[str, int]
    token_categories: dict[str, int]


class DesignSystemReport(TypedDict):
    """Machine-readable summary of the chirp-ui design system surface."""

    components: dict[str, dict[str, object]]
    tokens: dict[str, dict[str, str]]
    stats: DesignSystemStats


def design_system_report() -> DesignSystemReport:
    """Machine-readable summary of the full chirp-ui design system surface.

    Returns a dict with ``"components"`` keyed by block name,
    ``"tokens"`` keyed by CSS property name, and ``"stats"`` with
    aggregate counts.
    """
    from chirp_ui.tokens import TOKEN_CATALOG

    components: dict[str, dict[str, object]] = {}
    for name, desc in COMPONENTS.items():
        components[name] = {
            "block": desc.block,
            "variants": desc.variants,
            "sizes": desc.sizes,
            "modifiers": desc.modifiers,
            "elements": desc.elements,
            "slots": desc.slots,
            "tokens": desc.tokens,
            "template": desc.template,
            "category": desc.category,
        }
    component_categories: dict[str, int] = {}
    for desc in COMPONENTS.values():
        cat = desc.category or "uncategorized"
        component_categories[cat] = component_categories.get(cat, 0) + 1
    token_categories: dict[str, int] = {}
    for t in TOKEN_CATALOG.values():
        token_categories[t.category] = token_categories.get(t.category, 0) + 1
    return {
        "components": components,
        "tokens": {
            name: {"category": t.category, "scope": t.scope} for name, t in TOKEN_CATALOG.items()
        },
        "stats": {
            "total_components": len(COMPONENTS),
            "total_tokens": len(TOKEN_CATALOG),
            "component_categories": component_categories,
            "token_categories": token_categories,
        },
    }
