"""Shared fixtures for chirp-ui tests."""

import html
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from kida import Environment, FileSystemLoader
from kida.template import Markup

from chirp_ui.filters import (
    build_hx_attrs,
    contrast_text,
    make_route_link_attrs,
    resolve_color,
    resolve_status_variant,
    sanitize_color,
    value_type,
)
from chirp_ui.icons import icon as icon_filter

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "src" / "chirp_ui" / "templates"


def _field_errors_stub(errors: Any, field_name: str) -> Sequence[str]:
    """Stub for Chirp's ``field_errors`` filter.

    In production, this filter is provided by ``chirp.templating.filters``.
    For testing chirp-ui without Chirp, return an empty list so templates
    render without errors.
    """
    if errors is None:
        return []
    if isinstance(errors, dict):
        return errors.get(field_name, [])
    return []


def _bem_stub(
    block: str,
    variant: str = "",
    size: str = "",
    modifier: str | list[str] = "",
    cls: str = "",
) -> str:
    """Stub for Chirp's ``bem`` filter (chirpui BEM class builder)."""
    modifiers: list[str]
    if isinstance(modifier, list):
        modifiers = [m for m in modifier if m]
    else:
        modifiers = [modifier] if modifier else []
    parts = [f"chirpui-{block}"]
    if variant:
        parts.append(f"chirpui-{block}--{variant}")
    if size:
        parts.append(f"chirpui-{block}--{size}")
    parts.extend(f"chirpui-{block}--{m}" for m in modifiers)
    if cls:
        parts.append(cls)
    return " ".join(parts)


def _validate_variant_stub(
    value: str,
    allowed: Sequence[str],
    default: str = "",
) -> str:
    """Stub for chirp-ui ``validate_variant`` filter. Returns value if in allowed, else default."""
    return value if value in allowed else default


def _validate_variant_block_stub(value: str, block: str, default: str = "") -> str:
    """Stub for chirp-ui ``validate_variant_block`` filter."""
    from chirp_ui.validation import VARIANT_REGISTRY

    allowed = VARIANT_REGISTRY.get(block, ())
    return value if value in allowed else default


def _validate_size_stub(value: str, block: str, default: str = "") -> str:
    """Stub for chirp-ui ``validate_size`` filter."""
    from chirp_ui.validation import SIZE_REGISTRY

    allowed = SIZE_REGISTRY.get(block, ())
    return value if value in allowed else default


def _html_attrs_stub(value: Any) -> str | Markup:
    """Stub for structured attrs filter used by chirp-ui macros."""
    if value is None or value is False:
        return ""
    if isinstance(value, dict):
        parts: list[str] = []
        for key, raw in value.items():
            if raw is None or raw is False:
                continue
            escaped_key = html.escape(str(key), quote=True)
            if raw is True:
                parts.append(f" {escaped_key}")
                continue
            if isinstance(raw, (dict, list, tuple)):
                raw = json.dumps(raw, separators=(",", ":"), ensure_ascii=True)
            parts.append(f' {escaped_key}="{html.escape(str(raw), quote=True)}"')
        return Markup("".join(parts))
    text = str(value).strip()
    if not text:
        return Markup("")
    if text.startswith(" "):
        return Markup(text)
    return Markup(f" {text}")


def _island_attrs_stub(
    name: str,
    props: Any | None = None,
    *,
    mount_id: str | None = None,
    version: str = "1",
    src: str | None = None,
    cls: str = "",
) -> Markup:
    """Stub for Chirp's island mount attribute helper."""
    attrs = [
        f' data-island="{html.escape(name, quote=True)}"',
        f' data-island-version="{html.escape(version, quote=True)}"',
    ]
    if mount_id:
        attrs.append(f' id="{html.escape(mount_id, quote=True)}"')
    if src:
        attrs.append(f' data-island-src="{html.escape(src, quote=True)}"')
    if cls:
        attrs.append(f' class="{html.escape(cls, quote=True)}"')
    if props is not None:
        payload = html.escape(
            json.dumps(props, separators=(",", ":"), ensure_ascii=True), quote=True
        )
        attrs.append(f' data-island-props="{payload}"')
    return Markup("".join(attrs))


def _primitive_attrs_stub(
    primitive: str,
    props: dict[str, Any] | None = None,
    *,
    mount_id: str | None = None,
    version: str = "1",
    src: str | None = None,
    cls: str = "",
) -> Markup:
    data = dict(props or {})
    data.setdefault("primitive", primitive)
    base = _island_attrs_stub(
        primitive,
        props=data,
        mount_id=mount_id,
        version=version,
        src=src,
        cls=cls,
    )
    return Markup(f'{base} data-island-primitive="{html.escape(primitive, quote=True)}"')


@pytest.fixture
def env() -> Environment:
    """Kida environment with chirp-ui templates loaded via FileSystemLoader."""
    e = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    # Register stubs for Chirp/chirp-ui filters
    e.update_filters(
        {
            "field_errors": _field_errors_stub,
            "bem": _bem_stub,
            "html_attrs": _html_attrs_stub,
            "icon": icon_filter,
            "validate_variant": _validate_variant_stub,
            "validate_variant_block": _validate_variant_block_stub,
            "validate_size": _validate_size_stub,
            "value_type": value_type,
            "sanitize_color": sanitize_color,
            "contrast_text": contrast_text,
            "resolve_color": resolve_color,
            "resolve_status_variant": resolve_status_variant,
        }
    )
    e.add_global("build_hx_attrs", build_hx_attrs)
    e.add_global("route_link_attrs", make_route_link_attrs())
    e.add_global("island_attrs", _island_attrs_stub)
    e.add_global("primitive_attrs", _primitive_attrs_stub)
    e.add_global(
        "csrf_field",
        lambda: Markup('<input type="hidden" name="_csrf_token" value="test-csrf">'),
    )
    return e
