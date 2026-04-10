"""chirp-ui variant validation — strict mode and allowed options registry.

When strict mode is enabled (via :func:`set_strict`), invalid variant values
log warnings and fall back to defaults. Chirp sets strict from app.debug
when using use_chirp_ui(app, strict=None).

Everything not in __all__ is internal and may change without notice.
"""

from contextvars import ContextVar

__all__ = ["SIZE_REGISTRY", "VARIANT_REGISTRY", "set_strict"]

_chirpui_strict: ContextVar[bool] = ContextVar("chirpui_strict", default=False)

VARIANT_REGISTRY: dict[str, tuple[str, ...]] = {
    "alert": ("info", "success", "warning", "error"),
    "badge": ("primary", "success", "warning", "error", "muted", "info", "custom", "custom-solid"),
    "page_header": ("default", "compact"),
    "section_header": ("default", "inline"),
    "message_bubble": ("default", "user", "assistant", "system"),
    "surface": (
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
    "toast": ("info", "success", "warning", "error"),
    "hero": ("solid", "muted", "gradient", "mesh", "animated-gradient"),
    "page_hero": ("editorial", "minimal"),
    "description_list": ("stacked", "horizontal"),
    "skeleton": ("", "avatar", "text", "card"),
    "confirm": ("default", "danger"),
    "overlay": ("dark", "gradient-bottom", "gradient-top"),
    "progress-bar": ("gold", "radiant", "success", "watched", "custom"),
    "status-indicator": ("default", "success", "warning", "error", "info", "primary", "custom"),
    "btn": ("", "default", "primary", "ghost", "danger", "success", "warning"),
    "dropdown__item": ("default", "danger", "muted"),
    # Effects & new components
    "shimmer-btn": ("", "default", "primary"),
    "ripple-btn": ("", "default", "primary"),
    "pulsing-btn": ("", "default", "primary", "success", "danger"),
    "border-beam": ("", "default", "accent", "success", "warning"),
    "glow-card": ("", "default", "accent", "muted"),
    "spotlight-card": ("", "default", "accent"),
    "number-ticker": ("", "default", "mono"),
    "animated-counter": ("", "default", "mono"),
    "marquee": ("", "default", "reverse"),
    "meteor": ("", "default", "accent", "muted"),
    "text-reveal": ("", "default", "gradient"),
    "notification-dot": ("", "default", "error", "success", "warning"),
    "dock": ("", "default", "glass"),
    "particle-bg": ("", "default", "accent", "muted"),
    "icon-btn": ("", "default", "primary", "ghost", "danger"),
    "tooltip": ("top", "bottom", "left", "right"),
    # Playful / decorative effects
    "typewriter": ("", "fast", "slow"),
    "glitch": ("", "subtle", "intense"),
    "neon": ("cyan", "magenta", "green", "orange", "blue", "red"),
    "aurora": ("", "intense", "subtle"),
    "scanline": ("", "heavy", "crt"),
    "grain": ("", "heavy", "subtle"),
    "orbit": ("", "sm", "lg", "xl"),
    "sparkle": ("", "gold", "white", "rainbow"),
    "confetti": ("",),
    "wobble": ("wobble", "jello", "rubber-band", "bounce-in"),
    # ASCII background effects
    "symbol-rain": ("", "default", "accent", "gold", "muted"),
    "holy-light": ("", "default", "gold", "silver", "holy"),
    "rune-field": ("", "default", "arcane", "frost", "ember"),
    "constellation": ("", "default", "warm", "cool", "mono"),
    # ASCII primitives
    "ascii-border": ("", "single", "double", "rounded", "heavy", "spin"),
    "ascii-divider": (
        "",
        "single",
        "double",
        "heavy",
        "dots",
        "spin",
        "spin-reverse",
        "spin-drift",
    ),
    "ascii-sparkline": ("", "default", "accent", "muted", "gradient"),
    "ascii-progress": ("", "default", "accent", "success", "warning"),
    "ascii-empty": ("", "default", "muted", "accent"),
    "ascii-badge": ("", "default", "success", "warning", "error", "accent", "muted"),
    "ascii-spinner": ("", "braille", "box", "dots", "arrows", "blocks"),
    "ascii-skeleton": ("", "text", "card", "avatar", "heading"),
    "ascii-toggle": ("", "default", "success", "danger", "accent"),
    "ascii-switch": ("", "default", "success", "danger", "accent"),
    "ascii-table": ("single", "double", "heavy", "rounded"),
    "ascii-indicator": ("success", "warning", "error", "muted", "accent"),
    "ascii-tile-btn": ("", "default", "success", "warning", "danger", "accent"),
    "ascii-knob": ("", "default", "accent"),
    "ascii-fader": ("", "default", "accent", "success", "warning", "danger"),
    "ascii-vu": ("", "default", "accent", "success", "warning"),
    "ascii-7seg": ("", "default", "accent", "success", "warning", "error"),
    "ascii-checkbox": ("", "default", "accent", "success", "danger"),
    "ascii-radio-group": ("", "default", "accent"),
    "ascii-stepper": ("", "default", "accent", "success"),
    "split-flap": ("", "default", "amber", "green"),
    "ascii-ticker": ("", "default", "accent", "success", "warning", "error"),
    "ascii-card": ("", "single", "double", "rounded", "heavy"),
    "ascii-tabs": ("", "default", "accent"),
    "ascii-tab": ("", "default", "accent"),
    "ascii-modal": ("", "single", "double", "heavy"),
}

SIZE_REGISTRY: dict[str, tuple[str, ...]] = {
    "btn": ("", "sm", "md", "lg"),
    "modal": ("small", "medium", "large"),  # CSS: chirpui-modal--small, chirpui-modal--large
    "star-rating": ("", "sm", "md", "lg"),
    "thumbs": ("", "sm", "md", "lg"),
    "segmented": ("", "sm", "md", "lg"),
    "progress-bar": ("sm", "md", "lg"),
    # Effects & new components
    "shimmer-btn": ("", "sm", "md", "lg"),
    "ripple-btn": ("", "sm", "md", "lg"),
    "number-ticker": ("", "sm", "md", "lg", "xl"),
    "notification-dot": ("", "sm", "md", "lg"),
    "dock": ("", "sm", "md", "lg"),
    "border-beam": ("", "sm", "md", "lg"),
    "glow-card": ("", "sm", "md", "lg"),
    "icon-btn": ("", "sm", "md", "lg"),
    # Playful / decorative effects
    "orbit": ("", "sm", "lg", "xl"),
    "sparkle": ("", "sm", "md", "lg"),
    "ascii-toggle": ("", "sm", "md", "lg"),
    "ascii-switch": ("", "sm", "md", "lg"),
}


def set_strict(strict: bool) -> None:
    """Set strict mode for chirp-ui variant validation.

    When True, invalid variants log warnings and fall back to defaults.
    Chirp calls this per request when use_chirp_ui(app, strict=...) is used.
    """
    _chirpui_strict.set(strict)


def _is_strict() -> bool:
    return _chirpui_strict.get()
