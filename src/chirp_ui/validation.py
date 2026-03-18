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
    "badge": ("primary", "success", "warning", "error", "muted", "info"),
    "surface": ("default", "muted", "elevated", "accent", "glass", "frosted", "smoke"),
    "toast": ("info", "success", "warning", "error"),
    "hero": ("solid", "muted", "gradient"),
    "page_hero": ("editorial", "minimal"),
    "description_list": ("stacked", "horizontal"),
    "skeleton": ("", "avatar", "text", "card"),
    "confirm": ("default", "danger"),
    "overlay": ("dark", "gradient-bottom", "gradient-top"),
    "progress-bar": ("gold", "radiant", "success", "watched"),
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
}


def set_strict(strict: bool) -> None:
    """Set strict mode for chirp-ui variant validation.

    When True, invalid variants log warnings and fall back to defaults.
    Chirp calls this per request when use_chirp_ui(app, strict=...) is used.
    """
    _chirpui_strict.set(strict)


def _is_strict() -> bool:
    return _chirpui_strict.get()
