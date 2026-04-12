"""chirp-ui variant validation — strict mode and allowed options registry.

When strict mode is enabled (via :func:`set_strict`), invalid variant values
log warnings and fall back to defaults. Chirp sets strict from app.debug
when using use_chirp_ui(app, strict=None).

``VARIANT_REGISTRY`` and ``SIZE_REGISTRY`` are derived from the canonical
component descriptors in :mod:`chirp_ui.components`.

Everything not in __all__ is internal and may change without notice.
"""

from contextvars import ContextVar

from chirp_ui.components import COMPONENTS

__all__ = ["SIZE_REGISTRY", "VARIANT_REGISTRY", "set_strict"]

_chirpui_strict: ContextVar[bool] = ContextVar("chirpui_strict", default=False)

VARIANT_REGISTRY: dict[str, tuple[str, ...]] = {
    name: desc.variants for name, desc in COMPONENTS.items() if desc.variants
}

SIZE_REGISTRY: dict[str, tuple[str, ...]] = {
    name: desc.sizes for name, desc in COMPONENTS.items() if desc.sizes
}


def set_strict(strict: bool) -> None:
    """Set strict mode for chirp-ui variant validation.

    When True, invalid variants log warnings and fall back to defaults.
    Chirp calls this per request when use_chirp_ui(app, strict=...) is used.
    """
    _chirpui_strict.set(strict)


def _is_strict() -> bool:
    return _chirpui_strict.get()
