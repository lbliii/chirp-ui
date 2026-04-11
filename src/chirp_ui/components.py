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

__all__ = ["COMPONENTS", "ComponentDescriptor", "design_system_report"]


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
        modifiers=("full", "no-padding"),
        template="surface.html",
        category="container",
    ),
    "modal": ComponentDescriptor(
        block="modal",
        sizes=("small", "medium", "large"),
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
        template="ascii_switch.html",
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
}


def design_system_report() -> dict[str, object]:
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
            name: {"category": t.category, "scope": t.scope}
            for name, t in TOKEN_CATALOG.items()
        },
        "stats": {
            "total_components": len(COMPONENTS),
            "total_tokens": len(TOKEN_CATALOG),
            "component_categories": component_categories,
            "token_categories": token_categories,
        },
    }
