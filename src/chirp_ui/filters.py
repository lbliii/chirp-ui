"""Template filters required by chirp-ui components.

These match Chirp's filter API so chirp-ui works with any Chirp version.
Register via :func:`register_filters` when using Chirp.
"""

import logging
from collections.abc import Callable
from typing import Protocol

from chirp_ui.validation import VARIANT_REGISTRY, _is_strict


class TemplateFilterApp(Protocol):
    """Protocol for Chirp App (or mock) with template_filter support."""

    def template_filter(
        self,
        name: str | None = None,
    ) -> Callable[[Callable[..., object]], Callable[..., object]]: ...


def bem(block: str, variant: str = "", modifier: str = "", cls: str = "") -> str:
    """Build chirpui BEM class string: chirpui-{block} chirpui-{block}--{variant} etc.

    Example:
        class="{{ "alert" | bem(variant=variant, cls=cls) }}"
        → "chirpui-alert chirpui-alert--success my-class"
    """
    if variant and block in VARIANT_REGISTRY and _is_strict():
        allowed = VARIANT_REGISTRY[block]
        if variant not in allowed:
            log = logging.getLogger("chirp_ui")
            log.warning(
                'chirp-ui: %s variant "%s" invalid; valid: %s',
                block,
                variant,
                ", ".join(allowed),
            )
            variant = allowed[0] if allowed else ""
    parts = [f"chirpui-{block}"]
    if variant:
        parts.append(f"chirpui-{block}--{variant}")
    if modifier:
        parts.append(f"chirpui-{block}--{modifier}")
    if cls:
        parts.append(cls)
    return " ".join(parts)


def validate_variant(
    value: str,
    allowed: tuple[str, ...],
    default: str = "",
) -> str:
    """Return value if in allowed, else default. When strict, log warning."""
    if value in allowed:
        return value
    if _is_strict():
        log = logging.getLogger("chirp_ui")
        log.warning(
            'chirp-ui: variant "%s" invalid; valid: %s',
            value,
            ", ".join(allowed),
        )
    return default if default in allowed else (allowed[0] if allowed else "")


def field_errors(errors: dict[str, object] | None, field_name: str) -> list[str]:
    """Extract error messages for a field from a ValidationError-style dict.

    Returns empty list if errors is None or field has no errors.
    """
    if errors is None:
        return []
    val = errors.get(field_name)
    if val is None:
        return []
    if isinstance(val, (list, tuple)):
        return [str(x) for x in val]
    return []


def register_filters(app: TemplateFilterApp) -> None:
    """Register chirp-ui filters (bem, field_errors) on a Chirp app.

    Call after App creation. Ensures chirp-ui components render correctly
    regardless of Chirp version::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)
    """
    app.template_filter("bem")(bem)
    app.template_filter("field_errors")(field_errors)
    app.template_filter("validate_variant")(validate_variant)
