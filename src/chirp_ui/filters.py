"""Template filters required by chirp-ui components.

These match Chirp's filter API so chirp-ui works with any Chirp version.
Register via :func:`register_filters` when using Chirp.

Everything not in __all__ is internal and may change without notice.
"""

import logging
from pathlib import PurePath

__all__ = [
    "bem",
    "field_errors",
    "html_attrs",
    "icon",
    "validate_size",
    "validate_variant",
    "validate_variant_block",
    "value_type",
]
from collections.abc import Callable, Mapping
from html import escape
from json import dumps
from typing import Any, Protocol, cast

from kida.template import Markup

from chirp_ui.icons import ICON_REGISTRY
from chirp_ui.icons import icon as _resolve_icon
from chirp_ui.validation import SIZE_REGISTRY, VARIANT_REGISTRY, _is_strict


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


def validate_variant_block(value: str, block: str, default: str = "") -> str:
    """Return value if in VARIANT_REGISTRY for block, else default. When strict, log warning."""
    allowed = VARIANT_REGISTRY.get(block, ())
    return validate_variant(value, allowed, default)


def value_type(value: Any) -> str:
    """Map Python types to ChirpUI CSS variant names for description_item.

    Returns: "unset" | "bool" | "number" | "path" | "" (plain string).
    """
    if value is None:
        return "unset"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, PurePath):
        return "path"
    return ""


def validate_size(
    value: str,
    block: str,
    default: str = "",
) -> str:
    """Return value if in SIZE_REGISTRY for block, else default. When strict, log warning."""
    allowed = SIZE_REGISTRY.get(block, ())
    if value in allowed:
        return value
    if _is_strict() and allowed:
        log = logging.getLogger("chirp_ui")
        log.warning(
            'chirp-ui: %s size "%s" invalid; valid: %s',
            block,
            value,
            ", ".join(allowed),
        )
    return default if default in allowed else (allowed[0] if allowed else "")


def icon(name: str) -> str:
    """Resolve icon name to glyph; unknown names pass through. When strict, log warning."""
    result = _resolve_icon(name)
    if name not in ICON_REGISTRY and _is_strict():
        log = logging.getLogger("chirp_ui")
        log.warning(
            'chirp-ui: icon "%s" invalid; valid: %s',
            name,
            ", ".join(sorted(ICON_REGISTRY)),
        )
    return result


def field_errors(errors: dict[str, object] | None, field_name: str) -> list[str]:
    """Extract error messages for a field from a ValidationError-style dict.

    Returns empty list if errors is None, not a dict, or field has no errors.
    """
    if errors is None or not isinstance(errors, Mapping):
        return []
    val = errors.get(field_name)
    if val is None:
        return []
    if isinstance(val, (list, tuple)):
        return [str(x) for x in val]
    return []


def _serialize_attr_value(value: Any) -> str:
    """Serialize structured attr values such as hx-vals payloads."""
    if isinstance(value, (dict, list, tuple)):
        return dumps(value, separators=(",", ":"), ensure_ascii=True)
    return str(value)


def html_attrs(value: Any) -> str | Markup:
    """Render HTML attrs from mapping or legacy raw string."""
    if value is None or value is False:
        return ""

    if isinstance(value, Mapping):
        chunks: list[str] = []
        for raw_key, raw_value in value.items():
            key = str(raw_key).strip()
            if not key or raw_value is None or raw_value is False:
                continue
            escaped_key = escape(key, quote=True)
            if raw_value is True:
                chunks.append(f" {escaped_key}")
                continue
            serialized = _serialize_attr_value(raw_value)
            chunks.append(f' {escaped_key}="{escape(serialized, quote=True)}"')
        return Markup("".join(chunks))

    text = str(value).strip()
    if not text:
        return ""
    if text.startswith(" "):
        return Markup(text)
    return Markup(f" {text}")


def register_filters(app: TemplateFilterApp) -> None:
    """Register chirp-ui filters (bem, field_errors, html_attrs) on a Chirp app.

    Call after App creation. Ensures chirp-ui components render correctly
    regardless of Chirp version::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)
    """
    app.template_filter("bem")(bem)
    app.template_filter("field_errors")(field_errors)
    app.template_filter("html_attrs")(html_attrs)
    app.template_filter("icon")(icon)
    app.template_filter("validate_variant")(validate_variant)
    app.template_filter("validate_variant_block")(validate_variant_block)
    app.template_filter("validate_size")(validate_size)
    app.template_filter("value_type")(value_type)
    if hasattr(app, "template_global"):
        from chirp_ui.route_tabs import tab_is_active

        tg = cast(
            Callable[[str | None], Callable[[Callable[..., object]], Callable[..., object]]],
            app.template_global,
        )
        tg("tab_is_active")(tab_is_active)
