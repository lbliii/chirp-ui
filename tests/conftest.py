"""Shared fixtures for chirp-ui tests."""

import html
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from kida import Environment, FileSystemLoader
from kida.template import Markup

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


def _bem_stub(block: str, variant: str = "", modifier: str = "", cls: str = "") -> str:
    """Stub for Chirp's ``bem`` filter (chirpui BEM class builder)."""
    parts = [f"chirpui-{block}"]
    if variant:
        parts.append(f"chirpui-{block}--{variant}")
    if modifier:
        parts.append(f"chirpui-{block}--{modifier}")
    if cls:
        parts.append(cls)
    return " ".join(parts)


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
    # Register stubs for Chirp filters (field_errors, bem) used by chirp-ui
    e.update_filters({"field_errors": _field_errors_stub, "bem": _bem_stub})
    e.add_global("island_attrs", _island_attrs_stub)
    e.add_global("primitive_attrs", _primitive_attrs_stub)
    return e
