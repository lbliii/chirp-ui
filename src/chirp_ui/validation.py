"""chirp-ui variant validation — strict mode and allowed options registry.

When strict mode is enabled (via :func:`set_strict`), invalid variant values
log warnings and fall back to defaults. Chirp sets strict from app.debug
when using use_chirp_ui(app, strict=None).
"""

from contextvars import ContextVar

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
    "btn": ("default", "primary", "ghost", "danger", "success", "warning"),
}


def set_strict(strict: bool) -> None:
    """Set strict mode for chirp-ui variant validation.

    When True, invalid variants log warnings and fall back to defaults.
    Chirp calls this per request when use_chirp_ui(app, strict=...) is used.
    """
    _chirpui_strict.set(strict)


def _is_strict() -> bool:
    return _chirpui_strict.get()
