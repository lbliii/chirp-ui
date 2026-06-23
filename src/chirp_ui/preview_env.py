"""Kida preview environment for offline macro rendering.

Used by the blocks-gallery generator and component render tests. Mirrors the
Chirp runtime stubs registered in ``tests/conftest.py`` so manifest usage
snippets can be rendered without a full Chirp app.
"""

from __future__ import annotations

import html
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from kida import Environment, FileSystemLoader
from kida.template import Markup

from chirp_ui.filters import (
    _serialize_attr_value,
    build_hx_attrs,
    check_required_id,
    contrast_text,
    deprecate_param,
    make_route_link_attrs,
    resolve_color,
    resolve_status_variant,
    sanitize_color,
    shell_action_btn_variant,
    value_type,
)
from chirp_ui.grid_state import (
    column_aria_sort,
    parse_sort,
    selection_state,
    sort_columns,
    sort_query,
)
from chirp_ui.icons import icon as icon_filter
from chirp_ui.nav_pill import nav_pill_inline_style, segmented_pill_inline_style
from chirp_ui.route_tabs import tab_is_active
from chirp_ui.validation import ChirpUIValidationWarning, _warn

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def _field_errors_stub(errors: Any, field_name: str) -> Sequence[str]:
    if errors is None or not isinstance(errors, Mapping):
        return []
    val = errors.get(field_name)
    if val is None:
        return []
    if isinstance(val, (list, tuple)):
        return [str(x) for x in val]
    _warn(
        f"chirp-ui: field_errors expected list/tuple for field {field_name!r}, "
        f"got {type(val).__name__}; wrapping as [str(val)]",
        category=ChirpUIValidationWarning,
        stacklevel=3,
    )
    return [str(val)]


def _bem_stub(
    block: str,
    variant: str = "",
    appearance: str = "",
    tone: str = "",
    size: str = "",
    modifier: str | list[str] = "",
    cls: str = "",
) -> str:
    modifiers: list[str]
    if isinstance(modifier, list):
        modifiers = [m for m in modifier if m]
    else:
        modifiers = [modifier] if modifier else []
    parts = [f"chirpui-{block}"]
    seen = set(parts)
    for value in (appearance, tone, variant):
        if not value:
            continue
        cls_name = f"chirpui-{block}--{value}"
        if cls_name not in seen:
            parts.append(cls_name)
            seen.add(cls_name)
    if size:
        cls_name = f"chirpui-{block}--{size}"
        if cls_name not in seen:
            parts.append(cls_name)
            seen.add(cls_name)
    for mod in modifiers:
        cls_name = f"chirpui-{block}--{mod}"
        if cls_name not in seen:
            parts.append(cls_name)
            seen.add(cls_name)
    if cls:
        parts.append(cls)
    return " ".join(parts)


def _validate_variant_stub(value: str, allowed: Sequence[str], default: str = "") -> str:
    if value in allowed:
        return value
    result = default if default in allowed else (allowed[0] if allowed else "")
    if value:
        _warn(
            f"chirp-ui: variant {value!r} not in {allowed!r}; using {result!r}",
            category=ChirpUIValidationWarning,
        )
    return result


def _validate_variant_block_stub(value: str, block: str, default: str = "") -> str:
    from chirp_ui.validation import VARIANT_REGISTRY

    allowed = VARIANT_REGISTRY.get(block, ())
    return _validate_variant_stub(value, tuple(allowed), default)


def _validate_size_stub(value: str, block: str, default: str = "") -> str:
    from chirp_ui.validation import SIZE_REGISTRY

    allowed = SIZE_REGISTRY.get(block, ())
    if value in allowed:
        return value
    result = default if default in allowed else (allowed[0] if allowed else "")
    if value and allowed:
        _warn(
            f"chirp-ui: size {value!r} not in {allowed!r} for {block!r}; using {result!r}",
            category=ChirpUIValidationWarning,
        )
    return result


def _validate_appearance_block_stub(value: str, block: str, default: str = "") -> str:
    from chirp_ui.validation import APPEARANCE_REGISTRY

    if not value:
        return default
    return _validate_variant_stub(value, APPEARANCE_REGISTRY.get(block, ()), default)


def _validate_tone_block_stub(value: str, block: str, default: str = "") -> str:
    from chirp_ui.validation import TONE_REGISTRY

    if not value:
        return default
    return _validate_variant_stub(value, TONE_REGISTRY.get(block, ()), default)


def _html_attrs_stub(value: Any) -> str | Markup:
    if value is None or value is False:
        return ""
    if isinstance(value, Mapping):
        parts: list[str] = []
        for key, raw in value.items():
            k = str(key).strip()
            if not k or raw is None or raw is False:
                continue
            escaped_key = html.escape(k, quote=True)
            if raw is True:
                parts.append(f" {escaped_key}")
                continue
            serialized = _serialize_attr_value(raw)
            parts.append(f' {escaped_key}="{html.escape(serialized, quote=True)}"')
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


def make_preview_env() -> Environment:
    """Return a Kida environment wired for chirp-ui template previews."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    env.update_filters(
        {
            "field_errors": _field_errors_stub,
            "bem": _bem_stub,
            "html_attrs": _html_attrs_stub,
            "icon": icon_filter,
            "validate_variant": _validate_variant_stub,
            "validate_variant_block": _validate_variant_block_stub,
            "validate_appearance_block": _validate_appearance_block_stub,
            "validate_tone_block": _validate_tone_block_stub,
            "validate_size": _validate_size_stub,
            "value_type": value_type,
            "sanitize_color": sanitize_color,
            "contrast_text": contrast_text,
            "resolve_color": resolve_color,
            "deprecate_param": deprecate_param,
            "resolve_status_variant": resolve_status_variant,
            "shell_action_btn_variant": shell_action_btn_variant,
        }
    )
    env.add_global("build_hx_attrs", build_hx_attrs)
    env.add_global("check_required_id", check_required_id)
    env.add_global("route_link_attrs", make_route_link_attrs())
    env.add_global("island_attrs", _island_attrs_stub)
    env.add_global("primitive_attrs", _primitive_attrs_stub)
    env.add_global("parse_sort", parse_sort)
    env.add_global("sort_columns", sort_columns)
    env.add_global("selection_state", selection_state)
    env.add_global("column_aria_sort", column_aria_sort)
    env.add_global("sort_query", sort_query)
    from chirp_ui.config_schema import Field, Widget, project_fields

    env.add_global("project_fields", project_fields)
    env.add_global("config_field", Field)
    env.add_global("Widget", Widget)
    env.add_global("tab_is_active", tab_is_active)
    env.add_global("nav_pill_inline_style", nav_pill_inline_style)
    env.add_global("segmented_pill_inline_style", segmented_pill_inline_style)
    from chirp_ui.shortcuts import shortcuts_by_category, shortcuts_json
    from chirp_ui.text_fragment import build_text_fragment_url

    env.add_global("shortcuts_by_category", shortcuts_by_category)
    env.add_global("shortcuts_json", shortcuts_json)
    env.add_global("build_text_fragment_url", build_text_fragment_url)
    env.add_global(
        "csrf_field",
        lambda: Markup('<input type="hidden" name="_csrf_token" value="preview">'),
    )
    return env
