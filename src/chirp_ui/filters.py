"""Template filters required by chirp-ui components.

These match Chirp's filter API so chirp-ui works with any Chirp version.
Register via :func:`register_filters` when using Chirp.

Everything not in __all__ is internal and may change without notice.
"""

import math
import re
import warnings
from pathlib import PurePath

__all__ = [
    "bem",
    "build_hx_attrs",
    "contrast_text",
    "field_errors",
    "html_attrs",
    "icon",
    "make_route_link_attrs",
    "register_colors",
    "reset_colors",
    "resolve_color",
    "resolve_status_variant",
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
from chirp_ui.validation import (
    SIZE_REGISTRY,
    VARIANT_REGISTRY,
    ChirpUIValidationWarning,
    ChirpUIWarning,
    _warn,
)

_SORTED_ICON_NAMES: str = ", ".join(sorted(ICON_REGISTRY))

# Safe CSS color strings for inline styles (hex, rgb/hsl/oklch/lab/lch family).
# The character class inside parens allows digits, decimals, negatives, percent,
# commas, slashes, spaces, and lowercase alpha (for units: deg/turn/rad/grad
# and the 'none' keyword).  It blocks parens, semicolons, braces, angle brackets,
# and quotes — preventing CSS injection via url(), var(), expression(), etc.
_COLOR_RE = re.compile(
    r"^#[0-9a-fA-F]{3,8}$"
    r"|^(?:rgb|hsl|oklch|lab|lch)a?\([-\d.,%/ a-z]+\)$",
)
_URI_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

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


def reset_colors() -> None:
    """Clear all registered semantic color names for the current context."""
    _chirpui_named_colors.set(None)
    _chirpui_named_colors_lower.set(None)


def register_colors(mapping: Mapping[str, str]) -> None:
    """Register semantic color names (e.g. Pokémon types) for :func:`resolve_color`.

    Raises ``ValueError`` immediately if any color value fails
    :func:`sanitize_color` validation.
    """
    base = _named_color_map()
    for k, v in mapping.items():
        if not isinstance(k, str):
            raise TypeError(f"chirp-ui: register_colors key must be str, got {type(k).__name__}: {k!r}")
        if not isinstance(v, str):
            raise TypeError(f"chirp-ui: register_colors value must be str, got {type(v).__name__}: {v!r}")
        key = k.strip()
        val = v.strip()
        if val and sanitize_color(val) is None:
            raise ValueError(f"chirp-ui: invalid color value {val!r} for key {key!r}")
        base[key] = val
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


# Regex for splitting CSS function arguments: commas, slashes, or whitespace.
_CSS_FUNC_SPLIT = re.compile(r"[,/\s]+")


def _rgb_to_channels(s: str) -> tuple[float, float, float] | None:
    """Parse ``rgb(R, G, B)`` / ``rgba(R G B / A)`` into sRGB 0..1 channels."""
    m = re.match(r"rgba?\((.+)\)", s.strip())
    if not m:
        return None
    parts = _CSS_FUNC_SPLIT.split(m.group(1).strip())
    if len(parts) < 3:
        return None
    try:
        vals: list[float] = []
        for p in parts[:3]:
            if p.endswith("%"):
                vals.append(float(p[:-1]) / 100.0)
            else:
                vals.append(float(p) / 255.0)
        return (
            max(0.0, min(1.0, vals[0])),
            max(0.0, min(1.0, vals[1])),
            max(0.0, min(1.0, vals[2])),
        )
    except (ValueError, IndexError):  # fmt: skip
        return None


def _hsl_to_channels(s: str) -> tuple[float, float, float] | None:
    """Parse ``hsl(H, S%, L%)`` / ``hsla(...)`` and convert to sRGB 0..1."""
    m = re.match(r"hsla?\((.+)\)", s.strip())
    if not m:
        return None
    parts = _CSS_FUNC_SPLIT.split(m.group(1).strip())
    if len(parts) < 3:
        return None
    try:
        h = float(parts[0]) / 360.0
        sat = float(parts[1].rstrip("%")) / 100.0
        lit = float(parts[2].rstrip("%")) / 100.0
    except ValueError:
        return None
    # HSL to sRGB (standard algorithm)
    if sat == 0.0:
        return (lit, lit, lit)

    def _hue_to_rgb(p: float, q: float, t: float) -> float:
        if t < 0.0:
            t += 1.0
        if t > 1.0:
            t -= 1.0
        if t < 1.0 / 6.0:
            return p + (q - p) * 6.0 * t
        if t < 0.5:
            return q
        if t < 2.0 / 3.0:
            return p + (q - p) * (2.0 / 3.0 - t) * 6.0
        return p

    q = lit * (1.0 + sat) if lit < 0.5 else lit + sat - lit * sat
    p = 2.0 * lit - q
    return (
        max(0.0, min(1.0, _hue_to_rgb(p, q, h + 1.0 / 3.0))),
        max(0.0, min(1.0, _hue_to_rgb(p, q, h))),
        max(0.0, min(1.0, _hue_to_rgb(p, q, h - 1.0 / 3.0))),
    )


def _oklch_to_channels(s: str) -> tuple[float, float, float] | None:
    """Parse ``oklch(L C H)`` / ``oklcha(L C H / A)`` and convert to sRGB 0..1 via OKLab."""
    m = re.match(r"oklcha?\((.+)\)", s.strip())
    if not m:
        return None
    parts = _CSS_FUNC_SPLIT.split(m.group(1).strip())
    if len(parts) < 3:
        return None
    try:
        lightness = float(parts[0].rstrip("%"))
        # CSS oklch L is 0..1 (or 0%..100%)
        if parts[0].endswith("%"):
            lightness /= 100.0
        chroma = float(parts[1])
        hue_deg = float(parts[2])
    except ValueError:
        return None
    # OKLCh -> OKLab
    hue_rad = math.radians(hue_deg)
    a = chroma * math.cos(hue_rad)
    b = chroma * math.sin(hue_rad)
    # OKLab -> linear sRGB (via LMS intermediate)
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l_3 = l_ * l_ * l_
    m_3 = m_ * m_ * m_
    s_3 = s_ * s_ * s_
    r_lin = +4.0767416621 * l_3 - 3.3077115913 * m_3 + 0.2309699292 * s_3
    g_lin = -1.2684380046 * l_3 + 2.6097574011 * m_3 - 0.3413193965 * s_3
    b_lin = -0.0041960863 * l_3 - 0.7034186147 * m_3 + 1.7076147010 * s_3

    # Linear sRGB -> sRGB gamma
    def _linear_to_srgb(c: float) -> float:
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055

    return (_linear_to_srgb(r_lin), _linear_to_srgb(g_lin), _linear_to_srgb(b_lin))


def _css_color_to_srgb(css_color: str) -> tuple[float, float, float] | None:
    """Try all supported CSS color formats and return sRGB 0..1 channels."""
    ch = _hex_to_rgb_channels(css_color)
    if ch is not None:
        return ch
    ch = _rgb_to_channels(css_color)
    if ch is not None:
        return ch
    ch = _hsl_to_channels(css_color)
    if ch is not None:
        return ch
    return _oklch_to_channels(css_color)


def contrast_text(css_color: str) -> str:
    """Return ``white`` or ``#1a1a1a`` for readable text on solid *css_color*.

    Supports hex, ``rgb()``, ``hsl()``, and ``oklch()`` color formats.
    Emits :class:`~chirp_ui.validation.ChirpUIValidationWarning` when the
    color cannot be parsed (falls back to ``white``).
    """
    safe = sanitize_color(css_color)
    if safe is None:
        if css_color:
            _warn(
                f"chirp-ui: contrast_text could not parse color {css_color!r}; using 'white'",
                category=ChirpUIValidationWarning,
            )
        return "white"
    ch = _css_color_to_srgb(safe)
    if ch is None:
        _warn(
            f"chirp-ui: contrast_text could not convert color {css_color!r} to sRGB; using 'white'",
            category=ChirpUIValidationWarning,
        )
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


def bem(
    block: str,
    variant: str = "",
    size: str = "",
    modifier: str | list[str] = "",
    cls: str = "",
) -> str:
    """Build chirpui BEM class string from block, variant, size, and modifiers.

    Example::

        class="{{ "btn" | bem(variant="primary", size="lg", modifier="loading") }}"
        → "chirpui-btn chirpui-btn--primary chirpui-btn--lg chirpui-btn--loading"

    *modifier* accepts a single string or a list of strings for additive flags.
    """
    from chirp_ui.components import COMPONENTS

    desc = COMPONENTS.get(block)

    if variant:
        allowed = VARIANT_REGISTRY.get(block, ())
        if allowed and variant not in allowed:
            _warn(
                f"chirp-ui: {block} variant {variant!r} invalid; valid: {', '.join(allowed)}",
            )
            variant = allowed[0] if allowed else ""

    if size and desc and desc.sizes and size not in desc.sizes:
        _warn(
            f"chirp-ui: {block} size {size!r} invalid; valid: {', '.join(desc.sizes)}",
        )
        size = desc.sizes[0] if desc.sizes else ""

    modifiers: list[str]
    if isinstance(modifier, list):
        modifiers = [m for m in modifier if m]
    else:
        modifiers = [modifier] if modifier else []

    if desc and desc.modifiers:
        valid_modifiers: list[str] = []
        for m in modifiers:
            if m not in desc.modifiers:
                _warn(
                    f"chirp-ui: {block} modifier {m!r} invalid; valid: {', '.join(desc.modifiers)}",
                    stacklevel=4,
                )
            else:
                valid_modifiers.append(m)
        modifiers = valid_modifiers

    parts = [f"chirpui-{block}"]
    if variant:
        parts.append(f"chirpui-{block}--{variant}")
    if size:
        parts.append(f"chirpui-{block}--{size}")
    parts.extend(f"chirpui-{block}--{m}" for m in modifiers)
    if cls:
        parts.append(cls)
    return " ".join(parts)


def validate_variant(
    value: str,
    allowed: tuple[str, ...],
    default: str = "",
) -> str:
    """Return value if in allowed, else default.

    Always emits :class:`~chirp_ui.validation.ChirpUIValidationWarning`
    on fallback (raises ``ValueError`` in strict mode).
    """
    if value in allowed:
        return value
    result = default if default in allowed else (allowed[0] if allowed else "")
    if value:  # don't warn on empty string — common "no variant" case
        _warn(
            f"chirp-ui: variant {value!r} not in {allowed!r}; using {result!r}",
            category=ChirpUIValidationWarning,
        )
    return result


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
    """Return value if in SIZE_REGISTRY for block, else default.

    Always emits :class:`~chirp_ui.validation.ChirpUIValidationWarning`
    on fallback when the block has a registered size list
    (raises ``ValueError`` in strict mode).
    """
    allowed = SIZE_REGISTRY.get(block, ())
    if value in allowed:
        return value
    result = default if default in allowed else (allowed[0] if allowed else "")
    if value and allowed:  # only warn when block has registered sizes and value is non-empty
        _warn(
            f"chirp-ui: size {value!r} not in {allowed!r} for {block!r}; using {result!r}",
            category=ChirpUIValidationWarning,
        )
    return result


def icon(name: str) -> str:
    """Resolve icon name to glyph; unknown names pass through.

    Always emits :class:`~chirp_ui.validation.ChirpUIValidationWarning`
    for unrecognized names (raises ``ValueError`` in strict mode).
    """
    result = _resolve_icon(name)
    if name and name not in ICON_REGISTRY:
        _warn(
            f"chirp-ui: unrecognized icon name {name!r}",
            category=ChirpUIValidationWarning,
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


STATUS_WORDS: dict[str, str] = {
    # success
    "ok": "success",
    "yes": "success",
    "configured": "success",
    "true": "success",
    "1": "success",
    "on": "success",
    "ready": "success",
    "active": "success",
    "enabled": "success",
    "connected": "success",
    # warning
    "warning": "warning",
    "degraded": "warning",
    "pending": "warning",
    # error
    "error": "error",
    "issues": "error",
    "failed": "error",
    "offline": "error",
    "disabled": "error",
    "disconnected": "error",
    # info
    "info": "info",
    # muted
    "inactive": "muted",
    "unknown": "muted",
    "none": "muted",
}


def resolve_status_variant(status: str, default: str = "muted") -> str:
    """Map a status string to a badge variant using :data:`STATUS_WORDS`.

    Lookup is case-insensitive. Unrecognized words return *default* and
    emit :class:`~chirp_ui.validation.ChirpUIValidationWarning`.
    """
    if not status:
        return default
    variant = STATUS_WORDS.get(status.lower())
    if variant is not None:
        return variant
    _warn(
        f"chirp-ui: status {status!r} not in STATUS_WORDS; using {default!r}",
        category=ChirpUIValidationWarning,
    )
    return default


def build_hx_attrs(hx: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
    """Build a dict of hyphenated HTML attributes from keyword arguments.

    Converts underscores to hyphens in keys: ``hx_post`` becomes ``hx-post``.
    Pipe through ``html_attrs`` to render: ``{{ build_hx_attrs(...) | html_attrs }}``.

    Accepts an optional ``hx`` dict whose keys are the short htmx names
    (e.g. ``{"post": "/save", "target": "#out"}`` → ``hx-post``, ``hx-target``).
    Individual ``hx_*`` kwargs override keys from the ``hx`` dict.
    """
    merged: dict[str, Any] = {}
    if hx:
        for k, v in hx.items():
            if v is None:
                continue
            key = k.replace("_", "-")
            if not key.startswith("hx-"):
                key = f"hx-{key}"
            merged[key] = v
    for k, v in kwargs.items():
        if v is None:
            continue
        merged[k.replace("_", "-")] = v
    return merged


def _is_internal_href(href: str) -> bool:
    """Return True for app-local hrefs that can use route-aware swaps."""
    stripped = href.strip()
    if not stripped or stripped.startswith("#"):
        return False
    return not (stripped.startswith("//") or _URI_SCHEME_RE.match(stripped))


def _has_explicit_hx_attrs(
    *,
    attrs: Any = None,
    attrs_map: Mapping[str, Any] | None = None,
) -> bool:
    """Return True when legacy attrs already carry explicit htmx config."""
    if isinstance(attrs_map, Mapping):
        for raw_key in attrs_map:
            key = str(raw_key).strip().replace("_", "-")
            if key.startswith("hx-"):
                return True
    if isinstance(attrs, str):
        normalized = attrs.replace("_", "-")
        if "hx-" in normalized:
            return True
    return False


def make_route_link_attrs(
    *,
    swap_resolver: Callable[..., Mapping[str, Any]] | None = None,
) -> Callable[..., dict[str, Any]]:
    """Build a template global for route-aware link attrs.

    The default no-op version keeps standalone chirp-ui renderable. When
    ``swap_resolver`` is supplied (for example by Chirp's ``use_chirp_ui``),
    internal ``href`` values can inherit route-aware ``hx-target`` / ``hx-boost``
    attrs automatically.
    """

    def route_link_attrs(
        href: str | None,
        *,
        boost: bool = True,
        external: bool = False,
        disabled: bool = False,
        fallback: Mapping[str, Any] | None = None,
        attrs: Any = None,
        attrs_map: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if (
            href is None
            or disabled
            or not boost
            or external
            or not isinstance(href, str)
            or not _is_internal_href(href)
            or _has_explicit_hx_attrs(attrs=attrs, attrs_map=attrs_map)
        ):
            return {}
        if swap_resolver is None:
            return dict(fallback or {})
        attrs = swap_resolver(href, hx_boost=boost)
        if isinstance(attrs, Mapping):
            return dict(attrs)
        return {}

    return route_link_attrs


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

    # Legacy: accept pre-built attr strings.  Markup instances are already
    # safe; plain strings are treated as raw attrs for backwards compat but
    # should migrate to Markup or dict form.
    text = str(value).strip()
    if not text:
        return ""
    if isinstance(value, Markup):
        return Markup(f" {text}") if not text.startswith(" ") else value
    # Plain string — pass through for backwards compat (templates use
    # ``attrs`` params this way) but the dict form is preferred.
    return Markup(f" {text}") if not text.startswith(" ") else Markup(text)


def register_filters(app: TemplateFilterApp) -> None:
    """Register chirp-ui filters and globals on a Chirp app.

    Call after App creation. Ensures chirp-ui components render correctly
    regardless of Chirp version::

        from chirp import App
        import chirp_ui
        app = App(...)
        chirp_ui.register_filters(app)

    Also registers template globals such as ``build_hx_attrs`` and the
    standalone-safe ``route_link_attrs`` helper when the app exposes
    ``template_global``.
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
    app.template_filter("resolve_status_variant")(resolve_status_variant)
    if hasattr(app, "template_global"):
        from chirp_ui.route_tabs import tab_is_active

        tg = cast(
            Callable[[str | None], Callable[[Callable[..., object]], Callable[..., object]]],
            app.template_global,
        )
        tg("tab_is_active")(tab_is_active)
        tg("build_hx_attrs")(build_hx_attrs)
        tg("route_link_attrs")(make_route_link_attrs())
    else:
        warnings.warn(
            "chirp-ui: app has no template_global(); "
            "build_hx_attrs and route_link_attrs will not be available as template globals",
            ChirpUIWarning,
            stacklevel=2,
        )
