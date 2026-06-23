"""Manifest-driven CSS subset selection for chirp-ui (issue #205).

The shipped ``chirpui.css`` concatenates every authoring partial (~350+
components). Consumers that use a handful of macros can emit a **fraction** of
that payload by naming the components they import.

Mapping strategy: each :class:`~chirp_ui.components.ComponentDescriptor` declares
a BEM ``block``; the subset resolver finds partials whose CSS defines the root
class ``.chirpui-{block}``. Foundation partials (tokens, reset, base, layout)
and utility partials are always included so a subset remains usable.

Pure stdlib — no I/O in :func:`resolve_partial_paths`; the build script reads files.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from chirp_ui.components import COMPONENTS

__all__ = [
    "DEFAULT_FOUNDATION_PARTIALS",
    "DEFAULT_UTILITY_PARTIALS",
    "CssSubsetPlan",
    "css_partial_root",
    "resolve_partial_paths",
    "validate_component_names",
]

_PACKAGE_ROOT = Path(__file__).resolve().parent
CSS_PARTIALS_DIR = _PACKAGE_ROOT / "templates" / "css" / "partials"

# Always shipped — tokens, reset, base, layout. Numeric prefix = cascade order.
DEFAULT_FOUNDATION_PARTIALS: frozenset[str] = frozenset(
    {
        "partials/001_tokens.css",
        "partials/002_reset.css",
        "partials/003_base.css",
        "partials/004_layout.css",
    }
)

# Shared utilities referenced across unrelated components.
DEFAULT_UTILITY_PARTIALS: frozenset[str] = frozenset(
    {
        "partials/037_utilities.css",
        "partials/086_utility-inline-grouping-and-measures.css",
        "partials/087_utility-auto-fill-grid.css",
    }
)

_CLASS_RE = re.compile(r"\.(chirpui-[A-Za-z0-9_-]+)")


def css_partial_root() -> Path:
    """Return the authoring partials directory."""
    return CSS_PARTIALS_DIR


@lru_cache(maxsize=1)
def _block_to_partials() -> dict[str, frozenset[str]]:
    """Map registry block name → partial filenames that define its root class."""
    # partial filename → classes
    per_partial: dict[str, set[str]] = {}
    for path in sorted(CSS_PARTIALS_DIR.glob("*.css")):
        rel = f"partials/{path.name}"
        per_partial[rel] = set(_CLASS_RE.findall(path.read_text(encoding="utf-8")))

    block_map: dict[str, set[str]] = {}
    for _name, desc in COMPONENTS.items():
        root = f"chirpui-{desc.block}"
        hits = {partial for partial, classes in per_partial.items() if root in classes}
        if hits:
            block_map.setdefault(desc.block, set()).update(hits)
            # Alias registry name when it differs from block (e.g. data_grid → data-grid).
            if _name != desc.block:
                block_map.setdefault(_name, set()).update(hits)

    return {block: frozenset(partials) for block, partials in block_map.items()}


def _normalize_name(raw: str) -> str:
    """Normalize registry lookup keys (accept ``data_grid`` or ``data-grid``)."""
    return raw.strip().replace("_", "-")


def validate_component_names(names: Sequence[str]) -> tuple[str, ...]:
    """Normalize and validate component names against the registry.

    Raises :class:`KeyError` with suggestions when a name is unknown.
    """
    if not names:
        raise ValueError("at least one component name is required for a CSS subset")
    block_map = _block_to_partials()
    known = set(COMPONENTS) | set(block_map)
    normalized: list[str] = []
    for raw in names:
        name = _normalize_name(raw)
        if not name:
            continue
        if name not in known:
            suggestions = sorted(k for k in known if name in k or k in name)[:5]
            hint = f" (did you mean: {', '.join(suggestions)})" if suggestions else ""
            raise KeyError(f"unknown component {raw.strip()!r}{hint}")
        normalized.append(name)
    if not normalized:
        raise ValueError("at least one non-empty component name is required")
    return tuple(dict.fromkeys(normalized))


@lru_cache(maxsize=128)
def resolve_partial_paths(
    components: tuple[str, ...],
    *,
    include_utilities: bool = True,
) -> tuple[str, ...]:
    """Return ordered partial paths for a component subset.

    Order follows numeric filename prefix (cascade order), same as the full build.
    """
    validate_component_names(components)
    block_map = _block_to_partials()
    selected: set[str] = set(DEFAULT_FOUNDATION_PARTIALS)
    if include_utilities:
        selected |= DEFAULT_UTILITY_PARTIALS

    for name in components:
        partials = block_map.get(name)
        if partials:
            selected |= partials
        elif name in COMPONENTS:
            # Descriptor exists but no dedicated partial (style-less / shares block).
            desc = COMPONENTS[name]
            shared = block_map.get(desc.block)
            if shared:
                selected |= shared

    # Preserve cascade order via sorted filename.
    ordered = sorted(
        selected,
        key=lambda rel: (CSS_PARTIALS_DIR / rel.removeprefix("partials/")).name,
    )
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class CssSubsetPlan:
    """Resolved subset plan with size diagnostics."""

    components: tuple[str, ...]
    partial_paths: tuple[str, ...]
    include_utilities: bool

    @classmethod
    def for_components(
        cls,
        components: Iterable[str],
        *,
        include_utilities: bool = True,
    ) -> CssSubsetPlan:
        names = validate_component_names(tuple(components))
        paths = resolve_partial_paths(names, include_utilities=include_utilities)
        return cls(
            components=names,
            partial_paths=paths,
            include_utilities=include_utilities,
        )

    @property
    def partial_count(self) -> int:
        return len(self.partial_paths)

    def estimated_bytes(self) -> int:
        """Sum on-disk partial sizes (approximate generated subset weight)."""
        total = 0
        for rel in self.partial_paths:
            path = CSS_PARTIALS_DIR / rel.removeprefix("partials/")
            total += path.stat().st_size
        return total
