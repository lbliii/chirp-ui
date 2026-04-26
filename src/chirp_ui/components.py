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
    "COMPONENT_MATURITY_LEVELS",
    "COMPONENT_ROLES",
    "RUNTIME_REQUIREMENTS",
    "ComponentDescriptor",
    "DesignSystemReport",
    "DesignSystemStats",
    "SlotForward",
    "design_system_report",
]

COMPONENT_MATURITY_LEVELS = ("stable", "experimental", "legacy", "internal")
COMPONENT_ROLES = ("primitive", "component", "pattern", "effect", "infrastructure")
RUNTIME_REQUIREMENTS = ("htmx", "alpine", "dialog", "view-transition")


# ---------------------------------------------------------------------------
# Sprint-4 parity reconciliation maps (see docs/PLAN-css-scope-and-layer.md)
#
# These close the drift between the hand-authored descriptors below and the
# CSS partials that ship today, without requiring an immediate line-by-line
# rewrite of 200+ descriptors. ``ComponentDescriptor.emits`` consults them
# transparently so the registry→CSS parity test is green.
#
# * ``_AUTO_TRIMS`` — BEM-grammar classes a descriptor would derive from its
#   ``variants`` / ``sizes`` / ``modifiers`` tuples but that the CSS never
#   styles (e.g. an implicit ``--md`` default). Keyed by
#   :attr:`ComponentDescriptor.block`.
# * ``_AUTO_EXTRAS`` — classes the CSS emits today that the descriptor's
#   typed fields don't capture (compound states, un-surfaced elements).
#   Keyed by :attr:`ComponentDescriptor.block`. Sprint 6 folds these into
#   proper ``elements`` / ``extra_emits=`` kwargs as each component migrates
#   to the ``@scope`` envelope convention.
#
# Direct reads of ``descriptor.variants`` / ``.sizes`` / ``.elements`` are
# unaffected — validation behaviour in ``bem()`` / ``validate_variant`` /
# ``validate_size`` stays exactly as authored.
# ---------------------------------------------------------------------------


_AUTO_TRIMS: dict[str, frozenset[str]] = {
    "animated-counter": frozenset({"chirpui-animated-counter--default"}),
    "ascii-7seg": frozenset({"chirpui-ascii-7seg--default"}),
    "ascii-badge": frozenset({"chirpui-ascii-badge--default"}),
    "ascii-border": frozenset({"chirpui-ascii-border--rounded", "chirpui-ascii-border--single"}),
    "ascii-checkbox": frozenset({"chirpui-ascii-checkbox--default"}),
    "ascii-divider": frozenset({"chirpui-ascii-divider--single"}),
    "ascii-empty": frozenset({"chirpui-ascii-empty--default"}),
    "ascii-fader": frozenset({"chirpui-ascii-fader--default"}),
    "ascii-knob": frozenset({"chirpui-ascii-knob--default"}),
    "ascii-progress": frozenset({"chirpui-ascii-progress--default"}),
    "ascii-radio-group": frozenset({"chirpui-ascii-radio-group--default"}),
    "ascii-sparkline": frozenset({"chirpui-ascii-sparkline--default"}),
    "ascii-stepper": frozenset({"chirpui-ascii-stepper--default"}),
    "ascii-switch": frozenset({"chirpui-ascii-switch--default", "chirpui-ascii-switch--md"}),
    "ascii-tab": frozenset({"chirpui-ascii-tab--accent", "chirpui-ascii-tab--default"}),
    "ascii-tabs": frozenset({"chirpui-ascii-tabs--default"}),
    "ascii-ticker": frozenset({"chirpui-ascii-ticker--default"}),
    "ascii-tile-btn": frozenset({"chirpui-ascii-tile-btn--default"}),
    "ascii-toggle": frozenset({"chirpui-ascii-toggle--default", "chirpui-ascii-toggle--md"}),
    "ascii-vu": frozenset({"chirpui-ascii-vu--default"}),
    "band": frozenset({"chirpui-band--default"}),
    "border-beam": frozenset(
        {
            "chirpui-border-beam--default",
            "chirpui-border-beam--lg",
            "chirpui-border-beam--md",
            "chirpui-border-beam--sm",
        }
    ),
    "breadcrumbs": frozenset({"chirpui-breadcrumbs"}),
    "btn": frozenset({"chirpui-btn--lg", "chirpui-btn--md"}),
    "children": frozenset({"chirpui-children"}),
    "confirm": frozenset({"chirpui-confirm", "chirpui-confirm--default"}),
    "constellation": frozenset({"chirpui-constellation--default"}),
    "description-list": frozenset(
        {
            "chirpui-description-list--horizontal",
            "chirpui-description-list--stacked",
        }
    ),
    "dock": frozenset({"chirpui-dock--default", "chirpui-dock--md"}),
    "dropdown__item": frozenset(
        {
            "chirpui-dropdown__item--default",
            "chirpui-dropdown__item--muted",
        }
    ),
    "filter-bar": frozenset({"chirpui-filter-bar"}),
    "glow-card": frozenset(
        {
            "chirpui-glow-card--default",
            "chirpui-glow-card--lg",
            "chirpui-glow-card--md",
            "chirpui-glow-card--sm",
        }
    ),
    "holy-light": frozenset({"chirpui-holy-light--default"}),
    "icon-btn": frozenset({"chirpui-icon-btn--default", "chirpui-icon-btn--md"}),
    "infinite-scroll": frozenset({"chirpui-infinite-scroll"}),
    "key-value-form": frozenset({"chirpui-key-value-form"}),
    "marquee": frozenset({"chirpui-marquee--default"}),
    "message-bubble": frozenset({"chirpui-message-bubble--default"}),
    "meteor": frozenset({"chirpui-meteor--default"}),
    "modal": frozenset({"chirpui-modal--md"}),
    "model-card": frozenset({"chirpui-model-card"}),
    "notification-dot": frozenset(
        {
            "chirpui-notification-dot--default",
            "chirpui-notification-dot--error",
            "chirpui-notification-dot--md",
        }
    ),
    "number-ticker": frozenset({"chirpui-number-ticker--default"}),
    "page-header": frozenset({"chirpui-page-header--default"}),
    "page-hero": frozenset(
        {
            "chirpui-page-hero",
            "chirpui-page-hero--editorial",
            "chirpui-page-hero--minimal",
        }
    ),
    "params-table": frozenset({"chirpui-params-table"}),
    "particle-bg": frozenset({"chirpui-particle-bg--default"}),
    "progress": frozenset({"chirpui-progress"}),
    "pulsing-btn": frozenset(
        {
            "chirpui-pulsing-btn--danger",
            "chirpui-pulsing-btn--default",
            "chirpui-pulsing-btn--primary",
            "chirpui-pulsing-btn--success",
        }
    ),
    "ripple-btn": frozenset({"chirpui-ripple-btn--default", "chirpui-ripple-btn--md"}),
    "row-actions": frozenset({"chirpui-row-actions"}),
    "rune-field": frozenset({"chirpui-rune-field--default"}),
    "search-bar": frozenset({"chirpui-search-bar"}),
    "search-header": frozenset({"chirpui-search-header"}),
    "section-collapsible": frozenset({"chirpui-section-collapsible"}),
    "section-header": frozenset({"chirpui-section-header--default"}),
    "segmented": frozenset({"chirpui-segmented--md"}),
    "shimmer-btn": frozenset({"chirpui-shimmer-btn--default", "chirpui-shimmer-btn--md"}),
    "site-footer": frozenset({"chirpui-site-footer--columns"}),
    "site-nav": frozenset({"chirpui-site-nav"}),
    "sparkle": frozenset({"chirpui-sparkle--lg", "chirpui-sparkle--md", "chirpui-sparkle--sm"}),
    "split-flap": frozenset({"chirpui-split-flap--default"}),
    "spotlight-card": frozenset({"chirpui-spotlight-card--default"}),
    "star-rating": frozenset({"chirpui-star-rating--md"}),
    "streaming": frozenset({"chirpui-streaming"}),
    "streaming-bubble": frozenset({"chirpui-streaming-bubble"}),
    "symbol-rain": frozenset({"chirpui-symbol-rain--default"}),
    "tag-browse": frozenset({"chirpui-tag-browse"}),
    "text-reveal": frozenset({"chirpui-text-reveal--default"}),
    "thumbs": frozenset({"chirpui-thumbs--md"}),
    "wizard-form": frozenset({"chirpui-wizard-form"}),
    "wobble": frozenset(
        {
            "chirpui-wobble--bounce-in",
            "chirpui-wobble--jello",
            "chirpui-wobble--rubber-band",
            "chirpui-wobble--wobble",
        }
    ),
}


_AUTO_EXTRAS: dict[str, frozenset[str]] = {
    "action-bar": frozenset(
        {
            "chirpui-action-bar__item--active",
            "chirpui-action-bar__item--disabled",
        }
    ),
    "animated-counter": frozenset(
        {
            "chirpui-animated-counter__label",
            "chirpui-animated-counter__prefix",
            "chirpui-animated-counter__value",
        }
    ),
    "animated-stat-card": frozenset(
        {
            "chirpui-animated-stat-card__trend--down",
            "chirpui-animated-stat-card__trend--up",
        }
    ),
    "ascii-7seg": frozenset(
        {
            "chirpui-ascii-7seg__digit",
            "chirpui-ascii-7seg__display",
            "chirpui-ascii-7seg__frame",
            "chirpui-ascii-7seg__label",
        }
    ),
    "ascii-badge": frozenset(
        {
            "chirpui-ascii-badge__close",
            "chirpui-ascii-badge__glyph",
            "chirpui-ascii-badge__open",
            "chirpui-ascii-badge__text",
        }
    ),
    "ascii-border": frozenset(
        {
            "chirpui-ascii-border__bottom",
            "chirpui-ascii-border__content",
            "chirpui-ascii-border__corner",
            "chirpui-ascii-border__line",
            "chirpui-ascii-border__mid",
            "chirpui-ascii-border__side",
            "chirpui-ascii-border__top",
        }
    ),
    "ascii-card": frozenset(
        {
            "chirpui-ascii-card__body",
            "chirpui-ascii-card__bottom",
            "chirpui-ascii-card__content",
            "chirpui-ascii-card__corner",
            "chirpui-ascii-card__divider",
            "chirpui-ascii-card__line",
            "chirpui-ascii-card__side",
            "chirpui-ascii-card__top",
        }
    ),
    "ascii-checkbox": frozenset(
        {
            "chirpui-ascii-checkbox--disabled",
            "chirpui-ascii-checkbox__box",
            "chirpui-ascii-checkbox__input",
            "chirpui-ascii-checkbox__label",
        }
    ),
    "ascii-divider": frozenset({"chirpui-ascii-divider__glyph"}),
    "ascii-empty": frozenset(
        {
            "chirpui-ascii-empty__action",
            "chirpui-ascii-empty__desc",
            "chirpui-ascii-empty__glyph",
            "chirpui-ascii-empty__heading",
        }
    ),
    "ascii-fader": frozenset(
        {
            "chirpui-ascii-fader__cap",
            "chirpui-ascii-fader__input",
            "chirpui-ascii-fader__label",
            "chirpui-ascii-fader__segment",
            "chirpui-ascii-fader__segment--filled",
            "chirpui-ascii-fader__track",
            "chirpui-ascii-fader__value",
        }
    ),
    "ascii-indicator": frozenset(
        {
            "chirpui-ascii-indicator--blink",
            "chirpui-ascii-indicator--blink-fast",
            "chirpui-ascii-indicator__label",
            "chirpui-ascii-indicator__light",
        }
    ),
    "ascii-knob": frozenset(
        {
            "chirpui-ascii-knob__dial",
            "chirpui-ascii-knob__frame",
            "chirpui-ascii-knob__input",
            "chirpui-ascii-knob__legend",
            "chirpui-ascii-knob__notch",
            "chirpui-ascii-knob__position",
            "chirpui-ascii-knob__positions",
            "chirpui-ascii-knob__tick",
            "chirpui-ascii-knob__value",
        }
    ),
    "ascii-modal": frozenset(
        {
            "chirpui-ascii-modal__body",
            "chirpui-ascii-modal__close",
            "chirpui-ascii-modal__header",
            "chirpui-ascii-modal__title",
        }
    ),
    "ascii-progress": frozenset(
        {
            "chirpui-ascii-progress__empty",
            "chirpui-ascii-progress__filled",
            "chirpui-ascii-progress__label",
            "chirpui-ascii-progress__track",
            "chirpui-ascii-progress__value",
        }
    ),
    "ascii-radio-group": frozenset(
        {
            "chirpui-ascii-radio-group--horizontal",
            "chirpui-ascii-radio-group__legend",
        }
    ),
    "ascii-skeleton": frozenset(
        {
            "chirpui-ascii-skeleton__fill",
            "chirpui-ascii-skeleton__line",
            "chirpui-ascii-skeleton__line--header",
        }
    ),
    "ascii-sparkline": frozenset({"chirpui-ascii-sparkline__bar"}),
    "ascii-spinner": frozenset(
        {
            "chirpui-ascii-spinner--lg",
            "chirpui-ascii-spinner--md",
            "chirpui-ascii-spinner--sm",
            "chirpui-ascii-spinner__char",
            "chirpui-ascii-spinner__chars",
            "chirpui-ascii-spinner__label",
        }
    ),
    "ascii-stepper": frozenset(
        {
            "chirpui-ascii-stepper__connector",
            "chirpui-ascii-stepper__connector--complete",
            "chirpui-ascii-stepper__label",
            "chirpui-ascii-stepper__node",
            "chirpui-ascii-stepper__step",
            "chirpui-ascii-stepper__step--active",
            "chirpui-ascii-stepper__step--complete",
            "chirpui-ascii-stepper__track",
        }
    ),
    "ascii-switch": frozenset(
        {
            "chirpui-ascii-switch--disabled",
            "chirpui-ascii-switch__body",
            "chirpui-ascii-switch__cap",
            "chirpui-ascii-switch__cap--bottom",
            "chirpui-ascii-switch__cap--top",
            "chirpui-ascii-switch__input",
            "chirpui-ascii-switch__label",
            "chirpui-ascii-switch__lever",
            "chirpui-ascii-switch__slot",
        }
    ),
    "ascii-tab": frozenset(
        {
            "chirpui-ascii-tab--active",
            "chirpui-ascii-tab__bracket",
            "chirpui-ascii-tab__label",
        }
    ),
    "ascii-table": frozenset(
        {
            "chirpui-ascii-table--compact",
            "chirpui-ascii-table--sticky",
            "chirpui-ascii-table--striped",
            "chirpui-ascii-table__body",
            "chirpui-ascii-table__border",
            "chirpui-ascii-table__border--bottom",
            "chirpui-ascii-table__border--mid",
            "chirpui-ascii-table__border--top",
            "chirpui-ascii-table__cell--center",
            "chirpui-ascii-table__cell--left",
            "chirpui-ascii-table__cell--right",
            "chirpui-ascii-table__head",
            "chirpui-ascii-table__row",
            "chirpui-ascii-table__td",
            "chirpui-ascii-table__th",
        }
    ),
    "ascii-ticker": frozenset(
        {
            "chirpui-ascii-ticker--fast",
            "chirpui-ascii-ticker--slow",
            "chirpui-ascii-ticker__bracket",
            "chirpui-ascii-ticker__text",
            "chirpui-ascii-ticker__track",
        }
    ),
    "ascii-tile-btn": frozenset(
        {
            "chirpui-ascii-tile-btn--disabled",
            "chirpui-ascii-tile-btn--lit",
            "chirpui-ascii-tile-btn__face",
            "chirpui-ascii-tile-btn__glyph",
            "chirpui-ascii-tile-btn__input",
            "chirpui-ascii-tile-btn__label",
        }
    ),
    "ascii-toggle": frozenset(
        {
            "chirpui-ascii-toggle--disabled",
            "chirpui-ascii-toggle__input",
            "chirpui-ascii-toggle__knob",
            "chirpui-ascii-toggle__label",
            "chirpui-ascii-toggle__rail",
            "chirpui-ascii-toggle__track",
        }
    ),
    "ascii-vu": frozenset(
        {
            "chirpui-ascii-vu--animate",
            "chirpui-ascii-vu__bracket",
            "chirpui-ascii-vu__cell",
            "chirpui-ascii-vu__cell--filled",
            "chirpui-ascii-vu__cell--hot",
            "chirpui-ascii-vu__cell--peak",
            "chirpui-ascii-vu__label",
            "chirpui-ascii-vu__readout",
            "chirpui-ascii-vu__track",
        }
    ),
    "aurora": frozenset(
        {
            "chirpui-aurora__blob",
            "chirpui-aurora__blobs",
            "chirpui-aurora__content",
        }
    ),
    "border-beam": frozenset({"chirpui-border-beam__beam", "chirpui-border-beam__content"}),
    "breadcrumbs": frozenset(
        {
            "chirpui-breadcrumbs__current",
            "chirpui-breadcrumbs__item",
            "chirpui-breadcrumbs__link",
            "chirpui-breadcrumbs__list",
        }
    ),
    "btn": frozenset({"chirpui-btn--secondary"}),
    "calendar": frozenset({"chirpui-calendar__day--empty"}),
    "card": frozenset(
        {
            "chirpui-card--feature",
            "chirpui-card--glass",
            "chirpui-card--horizontal",
            "chirpui-card--media",
            "chirpui-card--stats",
        }
    ),
    "confetti": frozenset(
        {
            "chirpui-confetti__piece",
            "chirpui-confetti__piece--active",
            "chirpui-confetti__piece--circle",
            "chirpui-confetti__piece--square",
            "chirpui-confetti__piece--strip",
        }
    ),
    "confirm": frozenset(
        {
            "chirpui-confirm__footer",
            "chirpui-confirm__icon",
            "chirpui-confirm__message",
        }
    ),
    "constellation": frozenset(
        {
            "chirpui-constellation--dense",
            "chirpui-constellation--sparse",
            "chirpui-constellation__content",
            "chirpui-constellation__field",
            "chirpui-constellation__star",
        }
    ),
    "dnd": frozenset(
        {
            "chirpui-dnd__card--dragging",
            "chirpui-dnd__column-body--over",
            "chirpui-dnd__item--dragging",
            "chirpui-dnd__item--over",
        }
    ),
    "dock": frozenset(
        {
            "chirpui-dock__indicator",
            "chirpui-dock__item",
            "chirpui-dock__item--active",
        }
    ),
    "dropdown": frozenset(
        {
            "chirpui-dropdown--split",
            "chirpui-dropdown__caret",
            "chirpui-dropdown__divider",
            "chirpui-dropdown__icon",
            "chirpui-dropdown__split-primary",
            "chirpui-dropdown__trigger--select",
            "chirpui-dropdown__trigger--split",
        }
    ),
    "dropdown__item": frozenset({"chirpui-dropdown__item--selected"}),
    "field": frozenset({"chirpui-field__input--multi", "chirpui-field__label--inline"}),
    "glow-card": frozenset({"chirpui-glow-card__content", "chirpui-glow-card__glow"}),
    "grain": frozenset({"chirpui-grain--animated", "chirpui-grain--dot"}),
    "hero": frozenset(
        {
            "chirpui-hero--page",
            "chirpui-hero--page-minimal",
            "chirpui-hero__action",
            "chirpui-hero__actions",
            "chirpui-hero__content",
            "chirpui-hero__eyebrow",
            "chirpui-hero__footer",
            "chirpui-hero__inner",
            "chirpui-hero__metadata",
            "chirpui-hero__subtitle",
            "chirpui-hero__title",
        }
    ),
    "holy-light": frozenset(
        {
            "chirpui-holy-light--intense",
            "chirpui-holy-light--subtle",
            "chirpui-holy-light__content",
            "chirpui-holy-light__layer",
            "chirpui-holy-light__layer--far",
            "chirpui-holy-light__layer--mid",
            "chirpui-holy-light__layer--near",
            "chirpui-holy-light__layers",
            "chirpui-holy-light__mote",
        }
    ),
    "infinite-scroll": frozenset({"chirpui-infinite-scroll__loading--skeleton"}),
    "marquee": frozenset(
        {
            "chirpui-marquee--fast",
            "chirpui-marquee--slow",
            "chirpui-marquee__fade",
            "chirpui-marquee__fade--end",
            "chirpui-marquee__fade--start",
            "chirpui-marquee__item",
            "chirpui-marquee__track",
        }
    ),
    "message-bubble": frozenset(
        {
            "chirpui-message-bubble--left",
            "chirpui-message-bubble--pending",
            "chirpui-message-bubble--read",
            "chirpui-message-bubble--right",
            "chirpui-message-bubble--sent",
        }
    ),
    "meteor": frozenset({"chirpui-meteor__streak"}),
    "metric-card": frozenset(
        {
            "chirpui-metric-card__icon-badge--error",
            "chirpui-metric-card__icon-badge--primary",
            "chirpui-metric-card__icon-badge--success",
            "chirpui-metric-card__icon-badge--warning",
            "chirpui-metric-card__trend--down",
            "chirpui-metric-card__trend--neutral",
            "chirpui-metric-card__trend--up",
        }
    ),
    "modal": frozenset(
        {
            "chirpui-modal--closed",
            "chirpui-modal--open",
            "chirpui-modal__backdrop",
            "chirpui-modal__panel",
        }
    ),
    "nav-tree": frozenset(
        {
            "chirpui-nav-tree__link--active",
            "chirpui-nav-tree__link--leaf",
            "chirpui-nav-tree__list--nested",
            "chirpui-nav-tree__text--leaf",
        }
    ),
    "navbar": frozenset({"chirpui-navbar__link--active", "chirpui-navbar__links--end"}),
    "neon": frozenset({"chirpui-neon--flicker", "chirpui-neon--pulse"}),
    "notification-dot": frozenset(
        {
            "chirpui-notification-dot__dot",
            "chirpui-notification-dot__ping",
        }
    ),
    "number-ticker": frozenset({"chirpui-number-ticker__value"}),
    "orbit": frozenset(
        {
            "chirpui-orbit--fast",
            "chirpui-orbit--reverse",
            "chirpui-orbit--slow",
            "chirpui-orbit__center",
            "chirpui-orbit__item",
            "chirpui-orbit__ring",
        }
    ),
    "pagination": frozenset(
        {
            "chirpui-pagination__link--active",
            "chirpui-pagination__link--disabled",
        }
    ),
    "panel": frozenset(
        {
            "chirpui-panel__actions",
            "chirpui-panel__body",
            "chirpui-panel__body--scroll",
            "chirpui-panel__footer",
            "chirpui-panel__header",
            "chirpui-panel__heading",
            "chirpui-panel__subtitle",
            "chirpui-panel__title",
        }
    ),
    "params-table": frozenset(
        {
            "chirpui-params-table__code--muted",
            "chirpui-params-table__td--default",
            "chirpui-params-table__td--name",
            "chirpui-params-table__td--type",
            "chirpui-params-table__th--default",
            "chirpui-params-table__th--name",
            "chirpui-params-table__th--type",
        }
    ),
    "particle-bg": frozenset(
        {
            "chirpui-particle-bg__canvas",
            "chirpui-particle-bg__content",
            "chirpui-particle-bg__dot",
        }
    ),
    "progress-bar": frozenset(
        {
            "chirpui-progress-bar--error",
            "chirpui-progress-bar--info",
            "chirpui-progress-bar--warning",
            "chirpui-progress-bar__fill",
            "chirpui-progress-bar__label",
            "chirpui-progress-bar__track",
        }
    ),
    "pulsing-btn": frozenset({"chirpui-pulsing-btn__ring"}),
    "ripple-btn": frozenset({"chirpui-ripple-btn__ripple"}),
    "route-tab": frozenset({"chirpui-route-tab--active"}),
    "rune-field": frozenset(
        {
            "chirpui-rune-field__content",
            "chirpui-rune-field__layer",
            "chirpui-rune-field__layer--far",
            "chirpui-rune-field__layer--mid",
            "chirpui-rune-field__layer--near",
            "chirpui-rune-field__layers",
            "chirpui-rune-field__rune",
        }
    ),
    "segmented": frozenset(
        {
            "chirpui-segmented__icon",
            "chirpui-segmented__input",
            "chirpui-segmented__label",
            "chirpui-segmented__option",
            "chirpui-segmented__option--active",
        }
    ),
    "settings-row-list": frozenset(
        {
            "chirpui-settings-row-list--on-accent",
            "chirpui-settings-row-list--on-muted",
        }
    ),
    "shimmer-btn": frozenset({"chirpui-shimmer-btn__shimmer"}),
    "sidebar": frozenset(
        {
            "chirpui-sidebar__footer",
            "chirpui-sidebar__link--active",
            "chirpui-sidebar__section-links",
        }
    ),
    "site-footer": frozenset({"chirpui-site-footer__link--external"}),
    "site-header": frozenset(
        {
            "chirpui-site-header__inner--center-brand",
            "chirpui-site-header__inner--center-nav",
        }
    ),
    "site-nav": frozenset({"chirpui-site-nav__link--active", "chirpui-site-nav__link--external"}),
    "skeleton": frozenset(
        {
            "chirpui-skeleton--card-img",
            "chirpui-skeleton--card-line",
            "chirpui-skeleton__line",
        }
    ),
    "sortable": frozenset({"chirpui-sortable__item--dragging", "chirpui-sortable__item--over"}),
    "sparkle": frozenset({"chirpui-sparkle__star"}),
    "split-flap": frozenset({"chirpui-split-flap--animate", "chirpui-split-flap__char"}),
    "split-panel": frozenset({"chirpui-split-panel__pane--second"}),
    "spotlight-card": frozenset(
        {
            "chirpui-spotlight-card__content",
            "chirpui-spotlight-card__spotlight",
        }
    ),
    "star-rating": frozenset({"chirpui-star-rating__input", "chirpui-star-rating__label"}),
    "status-indicator": frozenset(
        {
            "chirpui-status-indicator--on-accent",
            "chirpui-status-indicator--on-muted",
            "chirpui-status-indicator--pulse",
            "chirpui-status-indicator__dot",
            "chirpui-status-indicator__icon",
            "chirpui-status-indicator__label",
        }
    ),
    "stepper": frozenset({"chirpui-stepper__item--active", "chirpui-stepper__item--completed"}),
    "surface": frozenset(
        {
            "chirpui-surface--cornered",
            "chirpui-surface--deep",
            "chirpui-surface--inset-glow",
            "chirpui-surface--noise-overlay",
            "chirpui-surface--static-overlay",
        }
    ),
    "symbol-rain": frozenset(
        {
            "chirpui-symbol-rain__canvas",
            "chirpui-symbol-rain__content",
            "chirpui-symbol-rain__drop",
        }
    ),
    "tab": frozenset({"chirpui-tab--disabled"}),
    "table": frozenset(
        {
            "chirpui-table__td--actions",
            "chirpui-table__td--center",
            "chirpui-table__td--left",
            "chirpui-table__td--mono",
            "chirpui-table__td--right",
            "chirpui-table__td--truncate",
            "chirpui-table__th--actions",
            "chirpui-table__th--center",
            "chirpui-table__th--left",
            "chirpui-table__th--right",
        }
    ),
    "tabs": frozenset({"chirpui-tabs__tab", "chirpui-tabs__tab--active"}),
    "thumbs": frozenset({"chirpui-thumbs__input", "chirpui-thumbs__label"}),
    "timeline": frozenset(
        {
            "chirpui-timeline__item--error",
            "chirpui-timeline__item--info",
            "chirpui-timeline__item--link",
            "chirpui-timeline__item--success",
            "chirpui-timeline__item--warning",
        }
    ),
    "toast": frozenset({"chirpui-toast__close", "chirpui-toast__message"}),
    "tooltip": frozenset({"chirpui-tooltip__bubble"}),
    "tree": frozenset({"chirpui-tree__label--leaf"}),
    "typewriter": frozenset(
        {
            "chirpui-typewriter--delay-1",
            "chirpui-typewriter--delay-2",
            "chirpui-typewriter--delay-3",
            "chirpui-typewriter--no-cursor",
            "chirpui-typewriter__text",
        }
    ),
}


@dataclass(frozen=True, slots=True)
class SlotForward:
    """Explicit mapping from a composite's public slot to a composed child slot.

    ``slot`` and ``target_slot`` use ``""`` for the default slot, matching
    :attr:`ComponentDescriptor.slots` and the manifest convention.
    ``target`` is a key in :data:`COMPONENTS`, not a CSS block or macro name.
    """

    slot: str
    target: str
    target_slot: str = ""


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
        Public caller slots the macro accepts (``""`` = default slot). This
        includes direct Kida ``{% slot %}`` placeholders and caller content
        forwarded into composed children.
    composes : tuple[str, ...]
        Component registry keys this component semantically composes.
    slot_forwards : tuple[SlotForward, ...]
        Explicit public-slot forwarding contracts into composed children.
    tokens : tuple[str, ...]
        Component-scoped CSS custom properties (override knobs for theming).
    extra_emits : tuple[str, ...]
        Escape hatch for classes the BEM grammar cannot derive
        (compound-state classes, internal structural elements not surfaced
        as BEM elements, etc.). Joined into :attr:`emits`.
    template : str
        Filename in ``templates/chirpui/`` (e.g. ``"button.html"``).
    category : str
        Grouping label for documentation/introspection.
    maturity : str
        Stability tier for agents and docs. Public templated components must
        set this explicitly. Empty is reserved for CSS-only reconciliation
        descriptors and derives from category (``stable`` normally,
        ``experimental`` for ``category="auto"``).
    role : str
        Semantic role for discovery/agent planning. Empty means "derive from
        category" (effects → ``effect``, composites → ``pattern``, etc.).
    requires : tuple[str, ...]
        Runtime features the component needs when rendered. Keep explicit
        entries for non-obvious requirements; the manifest may add derived
        requirements (for example Alpine factories) during projection.
    macro : str | None
        Macro identifier inside :attr:`template` (e.g. ``"shimmer_button"``).
        When ``None``, defaults to ``block.replace("-", "_")`` at lookup
        time. Set explicitly only when the macro name diverges from the BEM
        block (e.g. ``block="shimmer-btn"`` → ``macro="shimmer_button"``).
        Used by :mod:`chirp_ui.manifest` to resolve param signatures from
        the template AST.
    """

    block: str
    variants: tuple[str, ...] = ()
    sizes: tuple[str, ...] = ()
    modifiers: tuple[str, ...] = ()
    elements: tuple[str, ...] = ()
    slots: tuple[str, ...] = ()
    composes: tuple[str, ...] = ()
    slot_forwards: tuple[SlotForward, ...] = ()
    tokens: tuple[str, ...] = ()
    extra_emits: tuple[str, ...] = ()
    template: str = ""
    category: str = ""
    maturity: str = ""
    role: str = ""
    requires: tuple[str, ...] = ()
    macro: str | None = None

    def __post_init__(self) -> None:
        if self.maturity and self.maturity not in COMPONENT_MATURITY_LEVELS:
            raise ValueError(
                f"chirp-ui: invalid maturity {self.maturity!r} for block {self.block!r}"
            )
        if self.role and self.role not in COMPONENT_ROLES:
            raise ValueError(f"chirp-ui: invalid role {self.role!r} for block {self.block!r}")
        invalid_requires = tuple(r for r in self.requires if r not in RUNTIME_REQUIREMENTS)
        if invalid_requires:
            joined = ", ".join(repr(r) for r in invalid_requires)
            raise ValueError(
                f"chirp-ui: invalid runtime requirement(s) {joined} for block {self.block!r}"
            )

    @property
    def resolved_maturity(self) -> str:
        """Return the effective stability tier for manifest/docs projection."""
        if self.maturity:
            return self.maturity
        if self.category == "auto":
            return "experimental"
        return "stable"

    @property
    def resolved_role(self) -> str:
        """Return the effective semantic role for manifest/docs projection."""
        if self.role:
            return self.role
        if self.category == "effect":
            return "effect"
        if self.category == "composite":
            return "pattern"
        if self.category == "infrastructure":
            return "infrastructure"
        if self.category == "auto":
            return "primitive"
        return "component"

    @property
    def emits(self) -> frozenset[str]:
        """Every ``chirpui-*`` class the component's CSS may legitimately emit.

        Derived from the BEM grammar: block + ``__element`` + ``--variant`` /
        ``--size`` / ``--modifier``, plus any :attr:`extra_emits` escape hatches.
        Module-level :data:`_AUTO_EXTRAS` / :data:`_AUTO_TRIMS` reconciliation
        maps (keyed by block) patch the result so it stays in lock-step with
        the shipped CSS. See ``docs/DESIGN-css-registry-projection.md § Decision 4``.
        """
        classes: set[str] = {f"chirpui-{self.block}"}
        classes |= {f"chirpui-{self.block}__{e}" for e in self.elements}
        classes |= {f"chirpui-{self.block}--{v}" for v in self.variants if v}
        classes |= {f"chirpui-{self.block}--{s}" for s in self.sizes if s}
        classes |= {f"chirpui-{self.block}--{m}" for m in self.modifiers if m}
        classes |= set(self.extra_emits)
        classes |= _AUTO_EXTRAS.get(self.block, frozenset())
        classes -= _AUTO_TRIMS.get(self.block, frozenset())
        return frozenset(classes)


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
        maturity="stable",
    ),
    "icon-btn": ComponentDescriptor(
        block="icon-btn",
        variants=("", "default", "primary", "ghost", "danger"),
        sizes=("", "sm", "md", "lg"),
        template="icon_btn.html",
        category="control",
        maturity="stable",
    ),
    "shimmer-btn": ComponentDescriptor(
        block="shimmer-btn",
        variants=("", "default", "primary"),
        sizes=("", "sm", "md", "lg"),
        template="shimmer_button.html",
        category="effect",
        maturity="experimental",
        macro="shimmer_button",
    ),
    "ripple-btn": ComponentDescriptor(
        block="ripple-btn",
        variants=("", "default", "primary"),
        sizes=("", "sm", "md", "lg"),
        template="ripple_button.html",
        category="effect",
        maturity="experimental",
        macro="ripple_button",
    ),
    "pulsing-btn": ComponentDescriptor(
        block="pulsing-btn",
        variants=("", "default", "primary", "success", "danger"),
        template="pulsing_button.html",
        category="effect",
        maturity="experimental",
        macro="pulsing_button",
    ),
    # -- Feedback -----------------------------------------------------------
    "alert": ComponentDescriptor(
        block="alert",
        variants=("info", "success", "warning", "error"),
        elements=("icon", "body", "title", "actions", "close"),
        slots=("", "actions"),
        template="alert.html",
        category="feedback",
        maturity="stable",
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
        maturity="stable",
    ),
    "toast": ComponentDescriptor(
        block="toast",
        variants=("info", "success", "warning", "error"),
        template="toast.html",
        category="feedback",
        maturity="stable",
    ),
    "confirm": ComponentDescriptor(
        block="confirm",
        variants=("default", "danger"),
        slots=("header_actions", "message", "form_content"),
        template="confirm.html",
        category="feedback",
        maturity="stable",
        macro="confirm_dialog",
    ),
    "skeleton": ComponentDescriptor(
        block="skeleton",
        variants=("", "avatar", "text", "card"),
        template="skeleton.html",
        category="feedback",
        maturity="stable",
    ),
    "progress-bar": ComponentDescriptor(
        block="progress-bar",
        variants=("gold", "radiant", "success", "watched", "custom"),
        sizes=("sm", "md", "lg"),
        template="progress.html",
        category="feedback",
        maturity="stable",
    ),
    "status-indicator": ComponentDescriptor(
        block="status-indicator",
        variants=("default", "success", "warning", "error", "info", "primary", "custom"),
        template="status.html",
        category="feedback",
        maturity="stable",
    ),
    "notification-dot": ComponentDescriptor(
        block="notification-dot",
        variants=("", "default", "error", "success", "warning"),
        sizes=("", "sm", "md", "lg"),
        template="notification_dot.html",
        category="feedback",
        maturity="stable",
    ),
    "streaming_bubble": ComponentDescriptor(
        block="streaming-bubble",
        variants=("thinking", "error"),
        elements=("thinking",),
        template="streaming.html",
        category="feedback",
        maturity="stable",
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
        maturity="stable",
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
        maturity="stable",
    ),
    "modal": ComponentDescriptor(
        block="modal",
        sizes=("sm", "md", "lg"),
        elements=("header", "title", "header-actions", "close", "body", "footer"),
        slots=("", "header_actions", "footer"),
        template="modal.html",
        category="container",
        maturity="stable",
    ),
    "panel": ComponentDescriptor(
        block="panel",
        slots=("", "actions", "footer"),
        template="panel.html",
        category="container",
        maturity="stable",
    ),
    "overlay": ComponentDescriptor(
        block="overlay",
        variants=("dark", "gradient-bottom", "gradient-top"),
        template="overlay.html",
        category="container",
        maturity="stable",
    ),
    # -- Navigation ---------------------------------------------------------
    "tabs": ComponentDescriptor(
        block="tabs",
        slots=("",),
        template="tabs.html",
        category="navigation",
        maturity="stable",
    ),
    "tab": ComponentDescriptor(
        block="tab",
        modifiers=("active",),
        template="tabs.html",
        category="navigation",
        maturity="stable",
    ),
    "dropdown": ComponentDescriptor(
        block="dropdown",
        elements=("trigger", "menu", "header", "footer"),
        slots=("", "header", "footer"),
        template="dropdown.html",
        category="navigation",
        maturity="stable",
    ),
    "dropdown__item": ComponentDescriptor(
        block="dropdown__item",
        variants=("default", "danger", "muted"),
        template="dropdown_menu.html",
        category="navigation",
        maturity="stable",
        macro="dropdown_menu",
    ),
    "breadcrumbs": ComponentDescriptor(
        block="breadcrumbs",
        template="breadcrumbs.html",
        category="navigation",
        maturity="stable",
    ),
    "tooltip": ComponentDescriptor(
        block="tooltip",
        variants=("top", "bottom", "left", "right"),
        template="tooltip.html",
        category="navigation",
        maturity="stable",
    ),
    # -- Layout -------------------------------------------------------------
    "page_header": ComponentDescriptor(
        block="page-header",
        variants=("default", "compact"),
        elements=("actions", "breadcrumbs", "meta", "top"),
        slots=("actions",),
        template="layout.html",
        category="layout",
        maturity="stable",
    ),
    "section_header": ComponentDescriptor(
        block="section-header",
        variants=("default", "inline"),
        elements=("actions", "icon", "title-block", "title-inline", "top"),
        slots=("actions",),
        template="layout.html",
        category="layout",
        maturity="stable",
    ),
    "description_list": ComponentDescriptor(
        block="description-list",
        variants=("stacked", "horizontal"),
        template="description_list.html",
        category="layout",
        maturity="stable",
    ),
    "hero": ComponentDescriptor(
        block="hero",
        variants=("solid", "muted", "gradient", "mesh", "animated-gradient"),
        template="hero.html",
        category="layout",
        maturity="stable",
    ),
    "page_hero": ComponentDescriptor(
        block="page-hero",
        variants=("editorial", "minimal"),
        template="hero.html",
        category="layout",
        maturity="stable",
    ),
    "message_bubble": ComponentDescriptor(
        block="message-bubble",
        variants=("default", "user", "assistant", "system"),
        template="message_bubble.html",
        category="layout",
        maturity="stable",
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
        maturity="experimental",
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
        maturity="experimental",
    ),
    "glow-card": ComponentDescriptor(
        block="glow-card",
        variants=("", "default", "accent", "muted"),
        sizes=("", "sm", "md", "lg"),
        template="glow_card.html",
        category="effect",
        maturity="experimental",
    ),
    "spotlight-card": ComponentDescriptor(
        block="spotlight-card",
        variants=("", "default", "accent"),
        template="spotlight_card.html",
        category="effect",
        maturity="experimental",
    ),
    "number-ticker": ComponentDescriptor(
        block="number-ticker",
        variants=("", "default", "mono"),
        sizes=("", "sm", "md", "lg", "xl"),
        template="number_ticker.html",
        category="effect",
        maturity="experimental",
    ),
    "animated-counter": ComponentDescriptor(
        block="animated-counter",
        variants=("", "default", "mono"),
        template="animated_counter.html",
        category="effect",
        maturity="experimental",
    ),
    "marquee": ComponentDescriptor(
        block="marquee",
        variants=("", "default", "reverse"),
        slots=("",),
        template="marquee.html",
        category="effect",
        maturity="experimental",
    ),
    "meteor": ComponentDescriptor(
        block="meteor",
        variants=("", "default", "accent", "muted"),
        template="meteor.html",
        category="effect",
        maturity="experimental",
    ),
    "text-reveal": ComponentDescriptor(
        block="text-reveal",
        variants=("", "default", "gradient"),
        template="text_reveal.html",
        category="effect",
        maturity="experimental",
    ),
    "dock": ComponentDescriptor(
        block="dock",
        variants=("", "default", "glass"),
        sizes=("", "sm", "md", "lg"),
        slots=("",),
        template="dock.html",
        category="effect",
        maturity="experimental",
    ),
    "particle-bg": ComponentDescriptor(
        block="particle-bg",
        variants=("", "default", "accent", "muted"),
        template="particle_bg.html",
        category="effect",
        maturity="experimental",
    ),
    "typewriter": ComponentDescriptor(
        block="typewriter",
        variants=("", "fast", "slow"),
        template="typewriter.html",
        category="effect",
        maturity="experimental",
    ),
    "glitch": ComponentDescriptor(
        block="glitch",
        variants=("", "subtle", "intense"),
        template="glitch_text.html",
        category="effect",
        maturity="experimental",
        macro="glitch_text",
    ),
    "neon": ComponentDescriptor(
        block="neon",
        variants=("cyan", "magenta", "green", "orange", "blue", "red"),
        template="neon_text.html",
        category="effect",
        maturity="experimental",
        macro="neon_text",
    ),
    "aurora": ComponentDescriptor(
        block="aurora",
        variants=("", "intense", "subtle"),
        template="aurora.html",
        category="effect",
        maturity="experimental",
    ),
    "scanline": ComponentDescriptor(
        block="scanline",
        variants=("", "heavy", "crt"),
        template="scanline.html",
        category="effect",
        maturity="experimental",
    ),
    "grain": ComponentDescriptor(
        block="grain",
        variants=("", "heavy", "subtle"),
        template="grain.html",
        category="effect",
        maturity="experimental",
    ),
    "orbit": ComponentDescriptor(
        block="orbit",
        variants=("", "sm", "lg", "xl"),
        sizes=("", "sm", "lg", "xl"),
        template="orbit.html",
        category="effect",
        maturity="experimental",
    ),
    "sparkle": ComponentDescriptor(
        block="sparkle",
        variants=("", "gold", "white", "rainbow"),
        sizes=("", "sm", "md", "lg"),
        template="sparkle.html",
        category="effect",
        maturity="experimental",
    ),
    "confetti": ComponentDescriptor(
        block="confetti",
        variants=("",),
        template="confetti.html",
        category="effect",
        maturity="experimental",
    ),
    "wobble": ComponentDescriptor(
        block="wobble",
        variants=("wobble", "jello", "rubber-band", "bounce-in"),
        template="wobble.html",
        category="effect",
        maturity="experimental",
    ),
    # -- ASCII background effects -------------------------------------------
    "symbol-rain": ComponentDescriptor(
        block="symbol-rain",
        variants=("", "default", "accent", "gold", "muted"),
        template="symbol_rain.html",
        category="effect",
        maturity="experimental",
    ),
    "holy-light": ComponentDescriptor(
        block="holy-light",
        variants=("", "default", "gold", "silver", "holy"),
        template="holy_light.html",
        category="effect",
        maturity="experimental",
    ),
    "rune-field": ComponentDescriptor(
        block="rune-field",
        variants=("", "default", "arcane", "frost", "ember"),
        template="rune_field.html",
        category="effect",
        maturity="experimental",
    ),
    "constellation": ComponentDescriptor(
        block="constellation",
        variants=("", "default", "warm", "cool", "mono"),
        template="constellation.html",
        category="effect",
        maturity="experimental",
    ),
    # -- ASCII primitives ---------------------------------------------------
    "ascii-border": ComponentDescriptor(
        block="ascii-border",
        variants=("", "single", "double", "rounded", "heavy", "spin"),
        template="ascii_border.html",
        category="ascii",
        maturity="experimental",
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
        maturity="experimental",
    ),
    "ascii-sparkline": ComponentDescriptor(
        block="ascii-sparkline",
        variants=("", "default", "accent", "muted", "gradient"),
        template="ascii_sparkline.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-progress": ComponentDescriptor(
        block="ascii-progress",
        variants=("", "default", "accent", "success", "warning"),
        template="ascii_progress.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-empty": ComponentDescriptor(
        block="ascii-empty",
        variants=("", "default", "muted", "accent"),
        template="ascii_empty.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-badge": ComponentDescriptor(
        block="ascii-badge",
        variants=("", "default", "success", "warning", "error", "accent", "muted"),
        template="ascii_badge.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-spinner": ComponentDescriptor(
        block="ascii-spinner",
        variants=("", "braille", "box", "dots", "arrows", "blocks"),
        template="ascii_spinner.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-skeleton": ComponentDescriptor(
        block="ascii-skeleton",
        variants=("", "text", "card", "avatar", "heading"),
        template="ascii_skeleton.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-toggle": ComponentDescriptor(
        block="ascii-toggle",
        variants=("", "default", "success", "danger", "accent"),
        sizes=("", "sm", "md", "lg"),
        template="ascii_toggle.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-switch": ComponentDescriptor(
        block="ascii-switch",
        variants=("", "default", "success", "danger", "accent"),
        sizes=("", "sm", "md", "lg"),
        template="ascii_toggle.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-table": ComponentDescriptor(
        block="ascii-table",
        variants=("single", "double", "heavy", "rounded"),
        template="ascii_table.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-indicator": ComponentDescriptor(
        block="ascii-indicator",
        variants=("success", "warning", "error", "muted", "accent"),
        template="ascii_indicator.html",
        category="ascii",
        maturity="experimental",
        macro="indicator",
    ),
    "ascii-tile-btn": ComponentDescriptor(
        block="ascii-tile-btn",
        variants=("", "default", "success", "warning", "danger", "accent"),
        template="ascii_tile_btn.html",
        category="ascii",
        maturity="experimental",
        macro="tile_btn",
    ),
    "ascii-knob": ComponentDescriptor(
        block="ascii-knob",
        variants=("", "default", "accent"),
        template="ascii_knob.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-fader": ComponentDescriptor(
        block="ascii-fader",
        variants=("", "default", "accent", "success", "warning", "danger"),
        template="ascii_fader.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-vu": ComponentDescriptor(
        block="ascii-vu",
        variants=("", "default", "accent", "success", "warning"),
        template="ascii_vu_meter.html",
        category="ascii",
        maturity="experimental",
        macro="ascii_vu_meter",
    ),
    "ascii-7seg": ComponentDescriptor(
        block="ascii-7seg",
        variants=("", "default", "accent", "success", "warning", "error"),
        template="ascii_7seg.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-checkbox": ComponentDescriptor(
        block="ascii-checkbox",
        variants=("", "default", "accent", "success", "danger"),
        template="ascii_checkbox.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-radio-group": ComponentDescriptor(
        block="ascii-radio-group",
        variants=("", "default", "accent"),
        template="ascii_radio.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-stepper": ComponentDescriptor(
        block="ascii-stepper",
        variants=("", "default", "accent", "success"),
        template="ascii_stepper.html",
        category="ascii",
        maturity="experimental",
    ),
    "split-flap": ComponentDescriptor(
        block="split-flap",
        variants=("", "default", "amber", "green"),
        template="ascii_split_flap.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-ticker": ComponentDescriptor(
        block="ascii-ticker",
        variants=("", "default", "accent", "success", "warning", "error"),
        template="ascii_ticker.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-card": ComponentDescriptor(
        block="ascii-card",
        variants=("", "single", "double", "rounded", "heavy"),
        template="ascii_card.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-tabs": ComponentDescriptor(
        block="ascii-tabs",
        variants=("", "default", "accent"),
        template="ascii_tabs.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-tab": ComponentDescriptor(
        block="ascii-tab",
        variants=("", "default", "accent"),
        template="ascii_tabs.html",
        category="ascii",
        maturity="experimental",
    ),
    "ascii-modal": ComponentDescriptor(
        block="ascii-modal",
        variants=("", "single", "double", "heavy"),
        template="ascii_modal.html",
        category="ascii",
        maturity="experimental",
    ),
    # -- Marketing (site mode) ----------------------------------------------
    "site-shell": ComponentDescriptor(
        block="site-shell",
        elements=("main",),
        slots=("", "header", "footer"),
        tokens=("--chirpui-site-shell-bg",),
        template="site_shell.html",
        category="marketing",
        maturity="experimental",
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
        maturity="experimental",
    ),
    "site-nav-link": ComponentDescriptor(
        block="site-nav",
        elements=("link", "glyph"),
        template="site_header.html",
        category="marketing",
        maturity="experimental",
        macro="site_nav_link",
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
        maturity="experimental",
    ),
    "band": ComponentDescriptor(
        block="band",
        variants=("default", "elevated", "accent", "glass", "gradient"),
        modifiers=("inset", "bleed", "contained"),
        elements=(),
        slots=("", "header"),
        extra_emits=("chirpui-band--pattern-dots", "chirpui-band--pattern-grid"),
        tokens=(
            "--chirpui-band-bg",
            "--chirpui-band-border",
            "--chirpui-band-radius",
            "--chirpui-band-padding",
            "--chirpui-band-breakout",
        ),
        template="band.html",
        category="marketing",
        maturity="experimental",
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
        maturity="experimental",
    ),
    "feature-stack": ComponentDescriptor(
        block="feature-stack",
        template="feature_section.html",
        category="marketing",
        maturity="experimental",
    ),
    # -- Composites (PR #57) ------------------------------------------------
    "settings-row-list": ComponentDescriptor(
        block="settings-row-list",
        modifiers=("hoverable", "divided", "relaxed"),
        slots=("",),
        template="settings_row.html",
        category="container",
        maturity="stable",
    ),
    "settings-row": ComponentDescriptor(
        block="settings-row",
        elements=("label", "status", "detail"),
        template="settings_row.html",
        category="container",
        maturity="stable",
    ),
    "install-snippet": ComponentDescriptor(
        block="install-snippet",
        elements=("label", "row", "command"),
        slots=("",),
        template="code.html",
        category="content",
        maturity="stable",
    ),
    "filter-row": ComponentDescriptor(
        block="filter-row",
        slots=("",),
        template="filter_bar.html",
        category="control",
        maturity="stable",
    ),
    "tag-browse": ComponentDescriptor(
        block="tag-browse",
        template="tag_browse.html",
        category="control",
        maturity="stable",
        macro="tag_browse_tray",
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
        maturity="stable",
        macro="segmented_control",
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
        maturity="stable",
    ),
    "table-wrap": ComponentDescriptor(
        block="table-wrap",
        modifiers=("sticky",),
        slots=("", "caption"),
        template="table.html",
        category="data-display",
        maturity="stable",
        macro="table",
    ),
    "pagination": ComponentDescriptor(
        block="pagination",
        elements=("link", "ellipsis"),
        template="pagination.html",
        category="navigation",
        maturity="stable",
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
        maturity="stable",
    ),
    "row-actions": ComponentDescriptor(
        block="row-actions",
        elements=("trigger",),
        template="row_actions.html",
        category="control",
        maturity="stable",
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
        maturity="stable",
    ),
    "bar-chart": ComponentDescriptor(
        block="bar-chart",
        variants=("", "gold", "radiant", "success", "muted"),
        sizes=("", "sm", "md", "lg"),
        elements=("row", "label", "label-link", "track", "bar", "value"),
        template="bar_chart.html",
        category="data-display",
        maturity="stable",
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
        maturity="stable",
    ),
    "metric-grid": ComponentDescriptor(
        block="metric-grid",
        slots=("",),
        template="metric_grid.html",
        category="layout",
        maturity="stable",
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
        maturity="stable",
    ),
    "stat": ComponentDescriptor(
        block="stat",
        elements=("value", "label", "icon"),
        template="stat.html",
        category="data-display",
        maturity="stable",
    ),
    "animated-stat-card": ComponentDescriptor(
        block="animated-stat-card",
        elements=("trend",),
        template="animated_stat_card.html",
        category="data-display",
        maturity="stable",
    ),
    "list": ComponentDescriptor(
        block="list",
        modifiers=("bordered",),
        elements=("item", "link"),
        slots=("",),
        template="list.html",
        category="data-display",
        maturity="stable",
        macro="list_group",
    ),
    "sortable": ComponentDescriptor(
        block="sortable",
        elements=("item", "handle", "content", "remove"),
        slots=("",),
        template="sortable_list.html",
        category="interactive",
        maturity="stable",
        macro="sortable_list",
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
        maturity="stable",
    ),
    "tree": ComponentDescriptor(
        block="tree",
        elements=("item", "node", "label"),
        template="tree_view.html",
        category="data-display",
        maturity="stable",
        macro="tree_view",
    ),
    "chapter-list": ComponentDescriptor(
        block="chapter-list",
        elements=("summary", "summary-text", "summary-actions", "list"),
        slots=("", "summary_actions"),
        template="chapter_list.html",
        category="data-display",
        maturity="stable",
    ),
    "chapter-item": ComponentDescriptor(
        block="chapter-item",
        elements=("link", "timestamp", "title"),
        template="chapter_list.html",
        category="data-display",
        maturity="stable",
    ),
    "playlist": ComponentDescriptor(
        block="playlist",
        elements=("header", "title", "header-actions", "list"),
        slots=("", "header_actions"),
        template="playlist.html",
        category="data-display",
        maturity="stable",
    ),
    "playlist-item": ComponentDescriptor(
        block="playlist-item",
        modifiers=("active",),
        elements=("link", "title", "duration"),
        template="playlist.html",
        category="data-display",
        maturity="stable",
    ),
    "conversation-list": ComponentDescriptor(
        block="conversation-list",
        slots=("",),
        template="conversation_list.html",
        category="navigation",
        maturity="stable",
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
        maturity="stable",
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
        maturity="stable",
    ),
    "channel-card": ComponentDescriptor(
        block="channel-card",
        elements=("link", "info", "name", "subscribers", "body", "actions"),
        slots=("", "body"),
        template="channel_card.html",
        category="data-display",
        maturity="stable",
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
        maturity="stable",
    ),
    "video-thumbnail": ComponentDescriptor(
        block="video-thumbnail",
        elements=("img-wrap", "play", "duration", "progress"),
        tokens=("--chirpui-video-aspect-ratio",),
        template="video_thumbnail.html",
        category="media",
        maturity="stable",
    ),
    "index-card": ComponentDescriptor(
        block="index-card",
        elements=("header", "badge", "title", "description"),
        template="index_card.html",
        category="navigation",
        maturity="stable",
    ),
    "trending-tag": ComponentDescriptor(
        block="trending-tag",
        modifiers=("up",),
        elements=("hash", "count"),
        template="trending_tag.html",
        category="data-display",
        maturity="stable",
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
        extra_emits=(
            "chirpui-app-shell__main--fill",
            "chirpui-app-shell__sidebar--glass",
            "chirpui-app-shell__sidebar--muted",
            "chirpui-app-shell__topbar--glass",
            "chirpui-app-shell__topbar--gradient",
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
        maturity="stable",
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
        slots=("", "toolbar", "sidebar", "inspector"),
        composes=("split-layout", "panel"),
        slot_forwards=(
            SlotForward("sidebar", "panel"),
            SlotForward("inspector", "panel"),
        ),
        template="workspace_shell.html",
        category="layout",
        maturity="stable",
    ),
    "shell-actions": ComponentDescriptor(
        block="shell-actions",
        elements=("group",),
        template="shell_actions.html",
        category="layout",
        maturity="stable",
        macro="shell_actions_bar",
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
            "badge",
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
        maturity="stable",
    ),
    "sidebar-toggle": ComponentDescriptor(
        block="sidebar-toggle",
        elements=("icon",),
        template="sidebar.html",
        category="navigation",
        maturity="stable",
    ),
    "tray": ComponentDescriptor(
        block="tray",
        variants=("right", "left", "bottom"),
        modifiers=("open", "closed"),
        elements=("backdrop", "panel", "header", "title", "close", "body"),
        slots=("",),
        template="tray.html",
        category="overlay",
        maturity="stable",
    ),
    "drawer": ComponentDescriptor(
        block="drawer",
        variants=("right", "left"),
        elements=("panel", "header", "title", "header-actions", "close", "body"),
        slots=("", "header_actions"),
        template="drawer.html",
        category="overlay",
        maturity="stable",
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
        maturity="stable",
    ),
    "split-panel": ComponentDescriptor(
        block="split-panel",
        modifiers=("vertical", "dragging"),
        elements=("pane", "handle", "handle-grip"),
        slots=("left", "right"),
        template="split_panel.html",
        category="layout",
        maturity="stable",
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
        maturity="stable",
    ),
    "accordion": ComponentDescriptor(
        block="accordion",
        elements=("item", "trigger", "trigger-text", "trigger-actions", "content"),
        slots=("",),
        template="accordion.html",
        category="interactive",
        maturity="stable",
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
        slots=("",),
        template="forms.html",
        category="form",
        maturity="stable",
        macro="field_wrapper",
    ),
    "form-actions": ComponentDescriptor(
        block="form-actions",
        modifiers=("end",),
        template="forms.html",
        category="form",
        maturity="stable",
    ),
    "form-error-summary": ComponentDescriptor(
        block="form-error-summary",
        elements=("heading", "list"),
        template="forms.html",
        category="form",
        maturity="stable",
    ),
    "search-bar": ComponentDescriptor(
        block="search-bar",
        modifiers=("with-icon",),
        elements=("input", "inner", "icon", "btn"),
        template="forms.html",
        category="form",
        maturity="stable",
    ),
    "input-group": ComponentDescriptor(
        block="input-group",
        elements=("input", "prefix", "suffix"),
        slots=("prefix", "suffix"),
        template="forms.html",
        category="form",
        maturity="stable",
    ),
    "toggle-wrap": ComponentDescriptor(
        block="toggle-wrap",
        variants=("", "sm", "lg", "accent", "danger", "success"),
        template="forms.html",
        category="form",
        maturity="stable",
        macro="toggle_field",
    ),
    "fieldset": ComponentDescriptor(
        block="fieldset",
        elements=("legend",),
        template="forms.html",
        category="form",
        maturity="stable",
    ),
    "chat-input": ComponentDescriptor(
        block="chat-input",
        elements=("composer", "field", "footer"),
        slots=("",),
        template="chat_input.html",
        category="form",
        maturity="stable",
    ),
    "inline-edit": ComponentDescriptor(
        block="inline-edit",
        variants=("display", "edit"),
        elements=("value", "trigger", "icon", "form", "input", "actions"),
        template="inline_edit_field.html",
        category="form",
        maturity="stable",
        macro="inline_edit_field_display",
    ),
    "tag-input": ComponentDescriptor(
        block="tag-input",
        elements=("label", "chips", "add", "add-field"),
        template="tag_input.html",
        category="form",
        maturity="stable",
    ),
    "tag": ComponentDescriptor(
        block="tag",
        elements=("remove", "remove-btn"),
        template="tag_input.html",
        category="form",
        maturity="stable",
        macro="tag_input",
    ),
    "wizard-form": ComponentDescriptor(
        block="wizard-form",
        elements=("body",),
        template="wizard_form.html",
        category="form",
        maturity="stable",
    ),
    "selection-bar": ComponentDescriptor(
        block="selection-bar",
        elements=("count", "actions"),
        slots=("",),
        template="selection_bar.html",
        category="control",
        maturity="stable",
    ),
    # -- Navigation (Sprint 3) ----------------------------------------------
    "primary-nav": ComponentDescriptor(
        block="primary-nav",
        elements=("link", "label", "badge", "divider"),
        template="primary_nav.html",
        category="navigation",
        maturity="stable",
        extra_emits=(
            "chirpui-primary-nav__link--active",
            "chirpui-primary-nav__link--disabled",
        ),
    ),
    "nav-tree": ComponentDescriptor(
        block="nav-tree",
        modifiers=("linked-branches",),
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
            "badge",
        ),
        slots=("", "header"),
        template="nav_tree.html",
        category="navigation",
        maturity="stable",
        extra_emits=(
            "chirpui-nav-tree__item--active",
            "chirpui-nav-tree__item--branch",
            "chirpui-nav-tree__item--child",
            "chirpui-nav-tree__item--muted",
            "chirpui-nav-tree__item--open",
        ),
    ),
    "navbar": ComponentDescriptor(
        block="navbar",
        modifiers=("sticky",),
        elements=("brand", "links", "link"),
        slots=("", "brand", "end"),
        template="navbar.html",
        category="navigation",
        maturity="stable",
    ),
    "navbar-dropdown": ComponentDescriptor(
        block="navbar-dropdown",
        elements=("trigger",),
        template="navbar.html",
        category="navigation",
        maturity="stable",
    ),
    "nav-progress": ComponentDescriptor(
        block="nav-progress",
        template="nav_progress.html",
        category="navigation",
        maturity="stable",
    ),
    "route-tab": ComponentDescriptor(
        block="route-tab",
        elements=("icon", "label", "badge"),
        template="route_tabs.html",
        category="navigation",
        maturity="stable",
        macro="render_route_tabs",
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
        maturity="stable",
    ),
    "collapse": ComponentDescriptor(
        block="collapse",
        elements=("trigger", "trigger-text", "trigger-actions", "content"),
        slots=("",),
        template="collapse.html",
        category="interactive",
        maturity="stable",
    ),
    # -- Utility & remaining (Sprint 4) -------------------------------------
    "action-bar": ComponentDescriptor(
        block="action-bar",
        elements=("item", "icon", "count"),
        template="action_bar.html",
        category="control",
        maturity="stable",
    ),
    "action-strip": ComponentDescriptor(
        block="action-strip",
        modifiers=("sm", "scroll", "collapse", "sticky"),
        elements=("inner", "primary", "controls", "actions"),
        slots=("",),
        template="action_strip.html",
        category="control",
        maturity="stable",
    ),
    "ascii-breaker-panel": ComponentDescriptor(
        block="ascii-breaker-panel",
        modifiers=("sm",),
        elements=("title", "divider", "master", "switches", "breaker", "status"),
        slots=("",),
        template="ascii_breaker_panel.html",
        category="ascii",
        maturity="experimental",
        macro="breaker_panel",
    ),
    "ascii-error": ComponentDescriptor(
        block="ascii-error",
        elements=("art", "code", "heading", "desc", "action"),
        template="ascii_error.html",
        category="ascii",
        maturity="experimental",
    ),
    "avatar": ComponentDescriptor(
        block="avatar",
        sizes=("", "sm", "lg"),
        modifiers=("online", "offline"),
        elements=("img", "initials", "placeholder"),
        template="avatar.html",
        category="data-display",
        maturity="stable",
    ),
    "avatar-stack": ComponentDescriptor(
        block="avatar-stack",
        elements=("more", "link"),
        template="avatar_stack.html",
        category="data-display",
        maturity="stable",
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
        maturity="stable",
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
        maturity="stable",
    ),
    "carousel": ComponentDescriptor(
        block="carousel",
        modifiers=("compact", "page"),
        elements=("track", "slide", "dots", "dot"),
        slots=("",),
        template="carousel.html",
        category="interactive",
        maturity="stable",
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
        maturity="stable",
    ),
    "config-row": ComponentDescriptor(
        block="config-row",
        elements=("label", "control", "form", "toggle-wrap", "select", "editable"),
        template="config_row.html",
        category="container",
        maturity="stable",
        macro="config_row_toggle",
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
        maturity="stable",
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
        slots=("",),
        template="dnd.html",
        category="interactive",
        maturity="stable",
        macro="dnd_list",
    ),
    "empty-panel-state": ComponentDescriptor(
        block="empty-panel-state",
        modifiers=("compact",),
        slots=("", "actions", "action"),
        composes=("empty-state",),
        slot_forwards=(
            SlotForward("", "empty-state"),
            SlotForward("actions", "empty-state", "actions"),
            SlotForward("action", "empty-state", "action"),
        ),
        template="empty_panel_state.html",
        category="feedback",
        maturity="stable",
    ),
    "entity-header": ComponentDescriptor(
        block="entity-header",
        elements=("content", "icon", "title", "meta", "actions"),
        slots=("", "actions"),
        template="entity_header.html",
        category="layout",
        maturity="stable",
    ),
    "file-tree": ComponentDescriptor(
        block="file-tree",
        elements=("nav",),
        slots=("actions", "header", "footer"),
        composes=("panel", "nav-tree"),
        slot_forwards=(
            SlotForward("actions", "panel", "actions"),
            SlotForward("header", "nav-tree", "header"),
            SlotForward("footer", "panel", "footer"),
        ),
        template="file_tree.html",
        category="data-display",
        maturity="stable",
    ),
    "gradient-text": ComponentDescriptor(
        block="gradient-text",
        modifiers=("secondary", "rainbow", "animated"),
        template="gradient_text.html",
        category="effect",
        maturity="experimental",
    ),
    "hero-effects": ComponentDescriptor(
        block="hero-effects",
        template="hero_effects.html",
        category="effect",
        maturity="experimental",
    ),
    "fragment-island": ComponentDescriptor(
        block="fragment-island",
        template="fragment_island.html",
        category="infrastructure",
        maturity="internal",
    ),
    "label-overline": ComponentDescriptor(
        block="label-overline",
        modifiers=("section",),
        template="label_overline.html",
        category="content",
        maturity="stable",
    ),
    "link": ComponentDescriptor(
        block="link",
        template="link.html",
        category="navigation",
        maturity="stable",
    ),
    "live-badge": ComponentDescriptor(
        block="live-badge",
        elements=("dot", "viewers"),
        template="live_badge.html",
        category="feedback",
        maturity="stable",
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
        maturity="stable",
    ),
    "media-object": ComponentDescriptor(
        block="media-object",
        modifiers=("align-center",),
        elements=("media", "body", "actions"),
        slots=("", "media", "actions"),
        template="media_object.html",
        category="layout",
        maturity="stable",
    ),
    "mention": ComponentDescriptor(
        block="mention",
        template="mention.html",
        category="content",
        maturity="stable",
    ),
    "message-thread": ComponentDescriptor(
        block="message-thread",
        template="message_thread.html",
        category="data-display",
        maturity="stable",
    ),
    "popover": ComponentDescriptor(
        block="popover",
        elements=("trigger", "header", "footer", "panel"),
        slots=("", "header", "footer"),
        template="popover.html",
        category="overlay",
        maturity="stable",
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
        maturity="stable",
    ),
    "reaction-pill": ComponentDescriptor(
        block="reaction-pill",
        modifiers=("active", "disabled"),
        elements=("emoji", "count"),
        template="reaction_pill.html",
        category="interactive",
        maturity="stable",
    ),
    "reveal-on-scroll": ComponentDescriptor(
        block="reveal-on-scroll",
        template="reveal_on_scroll.html",
        category="effect",
        maturity="experimental",
    ),
    "signature": ComponentDescriptor(
        block="signature",
        elements=("code",),
        template="signature.html",
        category="content",
        maturity="stable",
    ),
    "spinner": ComponentDescriptor(
        block="spinner",
        sizes=("", "sm", "md", "lg"),
        elements=("mote",),
        template="spinner.html",
        category="feedback",
        maturity="stable",
    ),
    "sse-status": ComponentDescriptor(
        block="sse-status",
        modifiers=("connected", "disconnected", "error"),
        elements=("dot",),
        template="sse_status.html",
        category="feedback",
        maturity="stable",
    ),
    "stepper": ComponentDescriptor(
        block="stepper",
        elements=("list", "item", "indicator", "check", "label", "connector"),
        template="stepper.html",
        category="navigation",
        maturity="stable",
    ),
    "theme-toggle": ComponentDescriptor(
        block="theme-toggle",
        elements=("icon",),
        template="theme_toggle.html",
        category="control",
        maturity="stable",
    ),
    "typing-indicator": ComponentDescriptor(
        block="typing-indicator",
        elements=("dot",),
        template="typing_indicator.html",
        category="feedback",
        maturity="stable",
    ),
    # -- Additional blocks discovered in multi-macro files ------------------
    "copy-btn": ComponentDescriptor(
        block="copy-btn",
        variants=("", "user", "assistant", "system"),
        elements=("label", "done"),
        template="copy_button.html",
        category="control",
        maturity="stable",
        macro="copy_button",
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
        maturity="stable",
        macro="split_button",
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
        slots=("", "actions", "action"),
        template="empty.html",
        category="feedback",
        maturity="stable",
    ),
    "inline-counter": ComponentDescriptor(
        block="inline-counter",
        elements=("mark", "value", "label"),
        template="inline_counter.html",
        category="data-display",
        maturity="stable",
    ),
    "latest-line": ComponentDescriptor(
        block="latest-line",
        elements=("label", "title", "meta", "tooltip"),
        template="latest_line.html",
        category="data-display",
        maturity="stable",
    ),
    "chip-group": ComponentDescriptor(
        block="chip-group",
        slots=("",),
        template="chip_group.html",
        category="data-display",
        maturity="stable",
    ),
    "chip": ComponentDescriptor(
        block="chip",
        modifiers=("selected", "muted", "custom"),
        template="chip_group.html",
        category="data-display",
        maturity="stable",
        macro="chip",
    ),
    "rendered-content": ComponentDescriptor(
        block="rendered-content",
        modifiers=("compact",),
        slots=("",),
        template="rendered_content.html",
        category="typography",
        maturity="stable",
    ),
    "composer-shell": ComponentDescriptor(
        block="composer-shell",
        elements=(
            "header",
            "identity",
            "fields",
            "toolbar",
            "body",
            "preview",
            "footer",
            "status",
            "actions",
        ),
        slots=(
            "header",
            "identity",
            "fields",
            "toolbar",
            "body",
            "preview",
            "status",
            "actions",
        ),
        template="composer_shell.html",
        category="form",
        maturity="experimental",
    ),
    "token-input": ComponentDescriptor(
        block="token-input",
        elements=(
            "label",
            "control",
            "input",
            "token",
            "token-label",
            "remove",
            "list",
            "result",
            "result-label",
            "result-meta",
        ),
        slots=("tokens", "input", "results"),
        template="token_input.html",
        category="form",
        maturity="experimental",
        extra_emits=("chirpui-token-input__result--active",),
    ),
    "filter-group": ComponentDescriptor(
        block="filter-group",
        template="filter_chips.html",
        category="control",
        maturity="stable",
    ),
    "infinite-scroll": ComponentDescriptor(
        block="infinite-scroll",
        elements=("loading",),
        template="infinite_scroll.html",
        category="interactive",
        maturity="stable",
    ),
    "suspense-slot": ComponentDescriptor(
        block="suspense-slot",
        template="suspense.html",
        category="infrastructure",
        maturity="internal",
    ),
}


# ---------------------------------------------------------------------------
# Sprint-4 parity reconciliation — stub descriptors for CSS-only blocks that
# pre-dated the registry. Merged into ``COMPONENTS`` at import so downstream
# consumers see a single dict. Sprint 6 promotes them to hand-authored entries
# as each component migrates to the ``@scope`` envelope convention.
# ---------------------------------------------------------------------------

_AUTO_NEW_DESCRIPTORS: dict[str, ComponentDescriptor] = {
    "actions": ComponentDescriptor(
        block="actions",
        extra_emits=(
            "chirpui-actions--between",
            "chirpui-actions--bordered",
            "chirpui-actions--center",
            "chirpui-actions--stacked",
            "chirpui-actions--start",
            "chirpui-actions--stretch",
        ),
        category="auto",
    ),
    "ambient": ComponentDescriptor(
        block="ambient",
        category="auto",
    ),
    "ambient-root": ComponentDescriptor(
        block="ambient-root",
        category="auto",
    ),
    "ascii": ComponentDescriptor(
        block="ascii",
        elements=("char",),
        extra_emits=(
            "chirpui-ascii--blink",
            "chirpui-ascii--bounce",
            "chirpui-ascii--glow",
            "chirpui-ascii--grow",
            "chirpui-ascii--lg",
            "chirpui-ascii--md",
            "chirpui-ascii--pulse",
            "chirpui-ascii--rotate",
            "chirpui-ascii--shrink",
            "chirpui-ascii--sm",
            "chirpui-ascii--spin",
            "chirpui-ascii--throb",
            "chirpui-ascii--wiggle",
            "chirpui-ascii--xl",
            "chirpui-ascii__char--1",
            "chirpui-ascii__char--2",
            "chirpui-ascii__char--3",
            "chirpui-ascii__char--4",
        ),
        category="auto",
    ),
    "ascii-checkbox-group": ComponentDescriptor(
        block="ascii-checkbox-group",
        elements=("legend",),
        category="auto",
    ),
    "ascii-fader-bank": ComponentDescriptor(
        block="ascii-fader-bank",
        elements=("faders", "title"),
        category="auto",
    ),
    "ascii-fill": ComponentDescriptor(
        block="ascii-fill",
        category="auto",
    ),
    "ascii-fill-hover": ComponentDescriptor(
        block="ascii-fill-hover",
        category="auto",
    ),
    "ascii-indicator-row": ComponentDescriptor(
        block="ascii-indicator-row",
        category="auto",
    ),
    "ascii-modal-trigger": ComponentDescriptor(
        block="ascii-modal-trigger",
        category="auto",
    ),
    "ascii-radio": ComponentDescriptor(
        block="ascii-radio",
        elements=("dot", "input", "label"),
        extra_emits=("chirpui-ascii-radio--disabled",),
        category="auto",
    ),
    "ascii-tile-grid": ComponentDescriptor(
        block="ascii-tile-grid",
        category="auto",
    ),
    "ascii-vu-stack": ComponentDescriptor(
        block="ascii-vu-stack",
        elements=("title",),
        category="auto",
    ),
    "bento": ComponentDescriptor(
        block="bento",
        elements=("item",),
        extra_emits=(
            "chirpui-bento__item--span-2",
            "chirpui-bento__item--span-full",
            "chirpui-bento__item--span-row",
        ),
        category="auto",
    ),
    "bg-pattern": ComponentDescriptor(
        block="bg-pattern",
        extra_emits=(
            "chirpui-bg-pattern--accent-dots",
            "chirpui-bg-pattern--crosshatch",
            "chirpui-bg-pattern--diag",
            "chirpui-bg-pattern--dots-md",
            "chirpui-bg-pattern--dots-sm",
            "chirpui-bg-pattern--grid",
            "chirpui-bg-pattern--weave",
        ),
        category="auto",
    ),
    "blade": ComponentDescriptor(
        block="blade",
        extra_emits=("chirpui-blade--parallax",),
        category="auto",
    ),
    "block": ComponentDescriptor(
        block="block",
        extra_emits=(
            "chirpui-block--span-2",
            "chirpui-block--span-3",
            "chirpui-block--span-full",
            "chirpui-block--tall",
            "chirpui-block--wide",
        ),
        category="auto",
    ),
    "bounce-in": ComponentDescriptor(
        block="bounce-in",
        category="auto",
    ),
    "btn-group": ComponentDescriptor(
        block="btn-group",
        extra_emits=(
            "chirpui-btn-group--between",
            "chirpui-btn-group--center",
            "chirpui-btn-group--end",
            "chirpui-btn-group--stretch",
        ),
        category="auto",
    ),
    "bulk-bar": ComponentDescriptor(
        block="bulk-bar",
        elements=("count",),
        category="auto",
    ),
    "children": ComponentDescriptor(
        block="children",
        extra_emits=(
            "chirpui-children--clip",
            "chirpui-children--equal",
            "chirpui-children--rounded",
            "chirpui-children--rounded-full",
            "chirpui-children--rounded-lg",
            "chirpui-children--rounded-sm",
            "chirpui-children--rounded-xl",
        ),
        category="auto",
    ),
    "clamp-2": ComponentDescriptor(
        block="clamp-2",
        category="auto",
    ),
    "clamp-3": ComponentDescriptor(
        block="clamp-3",
        category="auto",
    ),
    "click-jello": ComponentDescriptor(
        block="click-jello",
        category="auto",
    ),
    "click-wobble": ComponentDescriptor(
        block="click-wobble",
        category="auto",
    ),
    "cluster": ComponentDescriptor(
        block="cluster",
        extra_emits=(
            "chirpui-cluster--detail-two-sprites",
            "chirpui-cluster--lg",
            "chirpui-cluster--md",
            "chirpui-cluster--sm",
            "chirpui-cluster--xs",
        ),
        category="auto",
    ),
    "code": ComponentDescriptor(
        block="code",
        category="auto",
    ),
    "code-block": ComponentDescriptor(
        block="code-block",
        elements=("copy",),
        category="auto",
    ),
    "code-block-wrapper": ComponentDescriptor(
        block="code-block-wrapper",
        category="auto",
    ),
    "command-bar": ComponentDescriptor(
        block="command-bar",
        category="auto",
    ),
    "comment-thread": ComponentDescriptor(
        block="comment-thread",
        category="auto",
    ),
    "config-row-list": ComponentDescriptor(
        block="config-row-list",
        extra_emits=(
            "chirpui-config-row-list--divided",
            "chirpui-config-row-list--hoverable",
            "chirpui-config-row-list--relaxed",
        ),
        category="auto",
    ),
    "container": ComponentDescriptor(
        block="container",
        category="auto",
    ),
    "counter-badge": ComponentDescriptor(
        block="counter-badge",
        extra_emits=(
            "chirpui-counter-badge--danger",
            "chirpui-counter-badge--warning",
        ),
        category="auto",
    ),
    "display": ComponentDescriptor(
        block="display",
        extra_emits=("chirpui-display--xl",),
        category="auto",
    ),
    "dl": ComponentDescriptor(
        block="dl",
        elements=("detail", "detail-unset", "header", "icon", "row", "term", "term-group"),
        extra_emits=(
            "chirpui-dl--compact",
            "chirpui-dl--detail-center",
            "chirpui-dl--detail-left",
            "chirpui-dl--detail-right",
            "chirpui-dl--divided",
            "chirpui-dl--horizontal",
            "chirpui-dl--hoverable",
            "chirpui-dl--relaxed",
            "chirpui-dl__detail--number",
            "chirpui-dl__detail--path",
            "chirpui-dl__detail--url",
        ),
        category="auto",
    ),
    "document-header": ComponentDescriptor(
        block="document-header",
        elements=("detail", "details", "eyebrow", "page-header", "path", "status"),
        slots=("actions",),
        composes=("page_header",),
        slot_forwards=(SlotForward("actions", "page_header", "actions"),),
        template="document_header.html",
        category="layout",
        maturity="stable",
        macro="document_header",
    ),
    "filter-bar": ComponentDescriptor(
        block="filter-bar",
        elements=("form",),
        category="auto",
    ),
    "flow": ComponentDescriptor(
        block="flow",
        extra_emits=(
            "chirpui-flow--lg",
            "chirpui-flow--md",
            "chirpui-flow--sm",
        ),
        category="auto",
    ),
    "focus-ring": ComponentDescriptor(
        block="focus-ring",
        category="auto",
    ),
    "font-2xl": ComponentDescriptor(
        block="font-2xl",
        category="auto",
    ),
    "font-base": ComponentDescriptor(
        block="font-base",
        category="auto",
    ),
    "font-lg": ComponentDescriptor(
        block="font-lg",
        category="auto",
    ),
    "font-medium": ComponentDescriptor(
        block="font-medium",
        category="auto",
    ),
    "font-mono": ComponentDescriptor(
        block="font-mono",
        category="auto",
    ),
    "font-sm": ComponentDescriptor(
        block="font-sm",
        category="auto",
    ),
    "font-xl": ComponentDescriptor(
        block="font-xl",
        category="auto",
    ),
    "font-xs": ComponentDescriptor(
        block="font-xs",
        category="auto",
    ),
    "frame": ComponentDescriptor(
        block="frame",
        extra_emits=(
            "chirpui-frame--balanced",
            "chirpui-frame--bento",
            "chirpui-frame--gap-lg",
            "chirpui-frame--gap-md",
            "chirpui-frame--gap-sm",
            "chirpui-frame--hero",
            "chirpui-frame--sidebar-end",
        ),
        category="auto",
    ),
    "grid": ComponentDescriptor(
        block="grid",
        extra_emits=(
            "chirpui-grid--auto-fill",
            "chirpui-grid--cols-2",
            "chirpui-grid--cols-3",
            "chirpui-grid--cols-4",
            "chirpui-grid--detail-two-single",
            "chirpui-grid--gap-lg",
            "chirpui-grid--gap-md",
            "chirpui-grid--gap-sm",
            "chirpui-grid--items-center",
            "chirpui-grid--items-end",
            "chirpui-grid--items-start",
            "chirpui-grid--preset-bento-211",
            "chirpui-grid--preset-detail-two",
            "chirpui-grid--preset-thirds",
        ),
        category="auto",
    ),
    "hover-jello": ComponentDescriptor(
        block="hover-jello",
        category="auto",
    ),
    "hover-rubber": ComponentDescriptor(
        block="hover-rubber",
        category="auto",
    ),
    "hover-wobble": ComponentDescriptor(
        block="hover-wobble",
        category="auto",
    ),
    "inline": ComponentDescriptor(
        block="inline",
        category="auto",
    ),
    "jello": ComponentDescriptor(
        block="jello",
        category="auto",
    ),
    "key-value-form": ComponentDescriptor(
        block="key-value-form",
        elements=("key", "row", "submit", "value"),
        category="auto",
    ),
    "layer": ComponentDescriptor(
        block="layer",
        extra_emits=(
            "chirpui-layer--angle-moderate",
            "chirpui-layer--angle-none",
            "chirpui-layer--angle-subtle",
            "chirpui-layer--center",
            "chirpui-layer--hover",
            "chirpui-layer--left",
            "chirpui-layer--overlap-lg",
            "chirpui-layer--overlap-md",
            "chirpui-layer--overlap-sm",
            "chirpui-layer--right",
        ),
        category="auto",
    ),
    "list-reset": ComponentDescriptor(
        block="list-reset",
        category="auto",
    ),
    "mb-md": ComponentDescriptor(
        block="mb-md",
        category="auto",
    ),
    "measure-lg": ComponentDescriptor(
        block="measure-lg",
        category="auto",
    ),
    "measure-md": ComponentDescriptor(
        block="measure-md",
        category="auto",
    ),
    "measure-sm": ComponentDescriptor(
        block="measure-sm",
        category="auto",
    ),
    "message-reactions": ComponentDescriptor(
        block="message-reactions",
        category="auto",
    ),
    "min-w-0": ComponentDescriptor(
        block="min-w-0",
        category="auto",
    ),
    "model-card": ComponentDescriptor(
        block="model-card",
        elements=("badge", "body", "footer", "header", "title"),
        category="auto",
    ),
    "mt-md": ComponentDescriptor(
        block="mt-md",
        category="auto",
    ),
    "mt-sm": ComponentDescriptor(
        block="mt-sm",
        category="auto",
    ),
    "number-scale": ComponentDescriptor(
        block="number-scale",
        elements=("input", "label", "labels"),
        category="auto",
    ),
    "page-fill": ComponentDescriptor(
        block="page-fill",
        category="layout",
        maturity="experimental",
        role="primitive",
    ),
    "placeholder-inline": ComponentDescriptor(
        block="placeholder-inline",
        category="auto",
    ),
    "progress": ComponentDescriptor(
        block="progress",
        elements=("fill", "track"),
        category="auto",
    ),
    "prose": ComponentDescriptor(
        block="prose",
        category="auto",
    ),
    "prose-lg": ComponentDescriptor(
        block="prose-lg",
        category="auto",
    ),
    "prose-sm": ComponentDescriptor(
        block="prose-sm",
        category="auto",
    ),
    "resource-card": ComponentDescriptor(
        block="resource-card",
        elements=("description",),
        category="auto",
    ),
    "result-slot": ComponentDescriptor(
        block="result-slot",
        extra_emits=("chirpui-result-slot--sm",),
        category="auto",
    ),
    "route-tabs": ComponentDescriptor(
        block="route-tabs",
        category="auto",
    ),
    "rubber-band": ComponentDescriptor(
        block="rubber-band",
        category="auto",
    ),
    "scroll-x": ComponentDescriptor(
        block="scroll-x",
        category="auto",
    ),
    "search-header": ComponentDescriptor(
        block="search-header",
        elements=("form", "strip"),
        template="search_header.html",
        category="layout",
        maturity="experimental",
        role="primitive",
    ),
    "section-collapsible": ComponentDescriptor(
        block="section-collapsible",
        elements=("summary",),
        slots=("",),
        composes=("surface", "section_header"),
        slot_forwards=(SlotForward("", "surface"),),
        template="layout.html",
        category="layout",
        maturity="experimental",
        role="primitive",
    ),
    "shell-action-form": ComponentDescriptor(
        block="shell-action-form",
        category="layout",
        maturity="experimental",
        role="primitive",
    ),
    "shell-section": ComponentDescriptor(
        block="shell-section",
        elements=("content", "nav"),
        category="layout",
        maturity="experimental",
        role="primitive",
    ),
    "spinner-thinking": ComponentDescriptor(
        block="spinner-thinking",
        elements=("char",),
        extra_emits=(
            "chirpui-spinner-thinking--lg",
            "chirpui-spinner-thinking--md",
            "chirpui-spinner-thinking--sm",
        ),
        category="auto",
    ),
    "split-flap-board": ComponentDescriptor(
        block="split-flap-board",
        elements=("body", "title"),
        extra_emits=(
            "chirpui-split-flap-board--amber",
            "chirpui-split-flap-board--green",
        ),
        category="auto",
    ),
    "split-flap-row": ComponentDescriptor(
        block="split-flap-row",
        category="auto",
    ),
    "sse-retry": ComponentDescriptor(
        block="sse-retry",
        modifiers=("loading",),
        elements=("loading",),
        category="auto",
    ),
    "stack": ComponentDescriptor(
        block="stack",
        extra_emits=(
            "chirpui-stack--lg",
            "chirpui-stack--md",
            "chirpui-stack--sm",
            "chirpui-stack--xl",
            "chirpui-stack--xs",
        ),
        category="auto",
    ),
    "streaming": ComponentDescriptor(
        block="streaming",
        variants=("error",),
        category="auto",
    ),
    "streaming-block": ComponentDescriptor(
        block="streaming-block",
        modifiers=("active",),
        elements=("cursor",),
        category="auto",
    ),
    "suspense-group": ComponentDescriptor(
        block="suspense-group",
        category="auto",
    ),
    "tab-panel": ComponentDescriptor(
        block="tab-panel",
        category="auto",
    ),
    "text-muted": ComponentDescriptor(
        block="text-muted",
        category="auto",
    ),
    "texture": ComponentDescriptor(
        block="texture",
        extra_emits=(
            "chirpui-texture--checker",
            "chirpui-texture--crosshatch",
            "chirpui-texture--diag",
            "chirpui-texture--dots-md",
            "chirpui-texture--dots-sm",
            "chirpui-texture--grid",
            "chirpui-texture--hex",
            "chirpui-texture--noise-coarse",
            "chirpui-texture--noise-fine",
            "chirpui-texture--weave",
        ),
        category="auto",
    ),
    "toast-container": ComponentDescriptor(
        block="toast-container",
        category="auto",
    ),
    "toggle": ComponentDescriptor(
        block="toggle",
        elements=("label", "track", "track-label"),
        extra_emits=(
            "chirpui-toggle__track-label--off",
            "chirpui-toggle__track-label--on",
        ),
        category="auto",
    ),
    "truncate": ComponentDescriptor(
        block="truncate",
        category="auto",
    ),
    "ui-base": ComponentDescriptor(
        block="ui-base",
        category="auto",
    ),
    "ui-bold": ComponentDescriptor(
        block="ui-bold",
        category="auto",
    ),
    "ui-label": ComponentDescriptor(
        block="ui-label",
        category="auto",
    ),
    "ui-lg": ComponentDescriptor(
        block="ui-lg",
        category="auto",
    ),
    "ui-medium": ComponentDescriptor(
        block="ui-medium",
        category="auto",
    ),
    "ui-meta": ComponentDescriptor(
        block="ui-meta",
        category="auto",
    ),
    "ui-normal": ComponentDescriptor(
        block="ui-normal",
        category="auto",
    ),
    "ui-semibold": ComponentDescriptor(
        block="ui-semibold",
        category="auto",
    ),
    "ui-sm": ComponentDescriptor(
        block="ui-sm",
        category="auto",
    ),
    "ui-title": ComponentDescriptor(
        block="ui-title",
        category="auto",
    ),
    "ui-xl": ComponentDescriptor(
        block="ui-xl",
        category="auto",
    ),
    "ui-xs": ComponentDescriptor(
        block="ui-xs",
        category="auto",
    ),
    "visually-hidden": ComponentDescriptor(
        block="visually-hidden",
        category="auto",
    ),
}

COMPONENTS.update(_AUTO_NEW_DESCRIPTORS)


class DesignSystemStats(TypedDict):
    """Aggregate counts for the design system surface."""

    total_components: int
    total_tokens: int
    registry_debt: dict[str, int]
    component_categories: dict[str, int]
    component_maturity: dict[str, int]
    component_roles: dict[str, int]
    component_requirements: dict[str, int]
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
            "extra_emits": desc.extra_emits,
            "emits": tuple(sorted(desc.emits)),
            "template": desc.template,
            "category": desc.category,
            "maturity": desc.resolved_maturity,
            "role": desc.resolved_role,
            "requires": desc.requires,
        }
    component_categories: dict[str, int] = {}
    component_maturity: dict[str, int] = {}
    component_roles: dict[str, int] = {}
    component_requirements: dict[str, int] = {}
    for desc in COMPONENTS.values():
        cat = desc.category or "uncategorized"
        component_categories[cat] = component_categories.get(cat, 0) + 1
        maturity = desc.resolved_maturity
        component_maturity[maturity] = component_maturity.get(maturity, 0) + 1
        role = desc.resolved_role
        component_roles[role] = component_roles.get(role, 0) + 1
        for requirement in desc.requires:
            component_requirements[requirement] = component_requirements.get(requirement, 0) + 1
    registry_debt = {
        "auto_category_components": sum(
            1 for desc in COMPONENTS.values() if desc.category == "auto"
        ),
        "auto_extra_blocks": len(_AUTO_EXTRAS),
        "auto_extra_classes": sum(len(classes) for classes in _AUTO_EXTRAS.values()),
        "auto_trim_blocks": len(_AUTO_TRIMS),
        "auto_trim_classes": sum(len(classes) for classes in _AUTO_TRIMS.values()),
        "explicit_extra_blocks": sum(1 for desc in COMPONENTS.values() if desc.extra_emits),
        "explicit_extra_classes": sum(len(desc.extra_emits) for desc in COMPONENTS.values()),
    }
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
            "registry_debt": registry_debt,
            "component_categories": component_categories,
            "component_maturity": component_maturity,
            "component_roles": component_roles,
            "component_requirements": component_requirements,
            "token_categories": token_categories,
        },
    }
