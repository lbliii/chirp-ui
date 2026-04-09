"""Template filters required by chirp-ui components.

These match Chirp's filter API so chirp-ui works with any Chirp version.
Register via :func:`register_filters` when using Chirp.

Everything not in __all__ is internal and may change without notice.
"""

import logging
import re
from pathlib import PurePath

__all__ = [
    "bem",
    "contrast_text",
    "field_errors",
    "html_attrs",
    "icon",
    "register_colors",
    "resolve_color",
    "sanitize_color",
    "validate_size",
    "validate_variant",
    "validate_variant_block",
    "value_type",
]
from collections.abc import Callable, Mapping
from contextvars import ContextVar
from html import escape
from json import dumps
from typing import Any, Protocol, cast

from kida.template import Markup

from chirp_ui.icons import ICON_REGISTRY
from chirp_ui.icons import icon as _resolve_icon
from chirp_ui.validation import SIZE_REGISTRY, VARIANT_REGISTRY, _is_strict

_SORTED_ICON_NAMES: str = ", ".join(sorted(ICON_REGISTRY))

# Safe CSS color strings for inline styles (hex, rgb/hsl/oklch family).
_COLOR_RE = re.compile(
    r"^#[0-9a-fA-F]{3,8}$|^(?:rgb|hsl|oklch)a?\([\d.,% /]+\)$",
)

_chirpui_named_colors: ContextVar[dict[str, str] | None] = ContextVar(
    "chirpui_named_colors",
    default=None,
)
_chirpui_named_colors_lower: ContextVar[dict[str, str] | None] = ContextVar(
    "chirpui_named_colors_lower",
    default=None,
)


def _named_color_map() -> dict[str, str]:
    d = _chirpui_named_colors.get()
    return dict(d) if d else {}


def register_colors(mapping: Mapping[str, str]) -> None:
    """Register semantic color names (e.g. Pokémon types) for :func:`resolve_color`."""
    base = _named_color_map()
    for k, v in mapping.items():
        base[str(k).strip()] = str(v).strip()
    _chirpui_named_colors.set(base)
    _chirpui_named_colors_lower.set({k.lower(): v for k, v in base.items()})


def sanitize_color(value: object) -> str | None:
    """Return the color if it matches a safe CSS color pattern, else None."""
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    return stripped if _COLOR_RE.match(stripped) else None


def _hex_to_rgb_channels(hex_color: str) -> tuple[float, float, float] | None:
    """Parse #RGB / #RRGGBB / #RRGGBBAA into sRGB channels in 0..1."""
    h = hex_color.strip()
    if not h.startswith("#"):
        return None
    body = h[1:]
    if len(body) == 3:
        r = int(body[0] + body[0], 16) / 255.0
        g = int(body[1] + body[1], 16) / 255.0
        b = int(body[2] + body[2], 16) / 255.0
        return (r, g, b)
    if len(body) == 6:
        r = int(body[0:2], 16) / 255.0
        g = int(body[2:4], 16) / 255.0
        b = int(body[4:6], 16) / 255.0
        return (r, g, b)
    if len(body) == 8:
        r = int(body[0:2], 16) / 255.0
        g = int(body[2:4], 16) / 255.0
        b = int(body[4:6], 16) / 255.0
        return (r, g, b)
    return None


def contrast_text(css_color: str) -> str:
    """Return ``white`` or ``#1a1a1a`` for readable text on solid ``css_color`` (hex)."""
    safe = sanitize_color(css_color)
    if safe is None:
        return "white"
    ch = _hex_to_rgb_channels(safe)
    if ch is None:
        return "white"
    r_lin, g_lin, b_lin = (
        ch[0] / 12.92 if ch[0] <= 0.04045 else ((ch[0] + 0.055) / 1.055) ** 2.4,
        ch[1] / 12.92 if ch[1] <= 0.04045 else ((ch[1] + 0.055) / 1.055) ** 2.4,
        ch[2] / 12.92 if ch[2] <= 0.04045 else ((ch[2] + 0.055) / 1.055) ** 2.4,
    )
    luminance = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
    return "#1a1a1a" if luminance > 0.179 else "white"


def resolve_color(value: object) -> str | None:
    """Resolve a named color from the registry, then validate as a CSS color string."""
    if not isinstance(value, str):
        return None
    key = value.strip()
    if not key:
        return None
    reg = _chirpui_named_colors.get()
    if reg:
        resolved = reg.get(key)
        if resolved is None:
            lower_reg = _chirpui_named_colors_lower.get()
            if lower_reg:
                resolved = lower_reg.get(key.lower())
        if resolved is not None:
            return sanitize_color(resolved)
    return sanitize_color(key)


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
            _SORTED_ICON_NAMES,
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


def build_hx_attrs(**kwargs: Any) -> dict[str, Any]:
    """Build a dict of hyphenated HTML attributes from keyword arguments.

    Converts underscores to hyphens in keys: ``hx_post`` becomes ``hx-post``.
    Pipe through ``html_attrs`` to render: ``{{ build_hx_attrs(...) | html_attrs }}``.
    """
    return {k.replace("_", "-"): v for k, v in kwargs.items()}


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
    app.template_filter("sanitize_color")(sanitize_color)
    app.template_filter("contrast_text")(contrast_text)
    app.template_filter("resolve_color")(resolve_color)
    if hasattr(app, "template_global"):
        from chirp_ui.route_tabs import tab_is_active

        tg = cast(
            Callable[[str | None], Callable[[Callable[..., object]], Callable[..., object]]],
            app.template_global,
        )
        tg("tab_is_active")(tab_is_active)
        tg("build_hx_attrs")(build_hx_attrs)
