"""chirp-ui variant validation — strict mode, warning infrastructure, and registries.

When strict mode is enabled (via :func:`set_strict`), validation warnings
escalate to ``ValueError``.  In non-strict mode, :func:`_warn` emits a
filterable :class:`ChirpUIValidationWarning` so developers see feedback
without crashes.

``VARIANT_REGISTRY`` and ``SIZE_REGISTRY`` are derived from the canonical
component descriptors in :mod:`chirp_ui.components`.

Everything not in __all__ is internal and may change without notice.
"""

import warnings
from contextvars import ContextVar

from chirp_ui.components import COMPONENTS

__all__ = [
    "SIZE_REGISTRY",
    "VARIANT_REGISTRY",
    "ChirpUIDeprecationWarning",
    "ChirpUIValidationWarning",
    "ChirpUIWarning",
    "is_strict",
    "set_strict",
]

_chirpui_strict: ContextVar[bool] = ContextVar("chirpui_strict", default=False)

VARIANT_REGISTRY: dict[str, tuple[str, ...]] = {
    name: desc.variants for name, desc in COMPONENTS.items() if desc.variants
}

SIZE_REGISTRY: dict[str, tuple[str, ...]] = {
    name: desc.sizes for name, desc in COMPONENTS.items() if desc.sizes
}


class ChirpUIWarning(UserWarning):
    """Base warning for chirp-ui issues."""


class ChirpUIValidationWarning(ChirpUIWarning):
    """Invalid input that was silently corrected."""


class ChirpUIDeprecationWarning(ChirpUIWarning, DeprecationWarning):
    """Deprecated chirp-ui feature."""


def set_strict(strict: bool) -> None:
    """Set strict mode for chirp-ui variant validation.

    When True, validation warnings escalate to ``ValueError``.
    Chirp calls this per request when use_chirp_ui(app, strict=...) is used.
    """
    _chirpui_strict.set(strict)


def is_strict() -> bool:
    """Return True when strict mode is active for this context."""
    return _chirpui_strict.get()


# Keep private alias for internal callers that already import it.
_is_strict = is_strict


def _warn(
    message: str,
    *,
    category: type[Warning] = ChirpUIValidationWarning,
    stacklevel: int = 3,
) -> None:
    """Emit a chirp-ui warning, or raise ValueError in strict mode.

    In strict mode, :class:`ChirpUIValidationWarning` escalates to
    ``ValueError``.  :class:`ChirpUIDeprecationWarning` always warns
    (deprecation ≠ error).

    *stacklevel* defaults to 3 (caller → filter function → ``_warn``).
    Pass a higher value when called from deeper internal helpers.
    """
    if (
        _is_strict()
        and issubclass(category, ChirpUIValidationWarning)
        and not issubclass(category, ChirpUIDeprecationWarning)
    ):
        raise ValueError(message)
    warnings.warn(message, category, stacklevel=stacklevel)
