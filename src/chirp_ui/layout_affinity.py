"""Layout-affinity vocabulary for recipe-level workspace contracts.

The current layout-affinity contract is intentionally narrow: rendered
templates may emit documented ``data-chirpui-*`` attributes, and parent
primitives may resolve those attributes inside their own scoped CSS. This
module centralizes the allowed vocabulary without projecting it into the public
manifest schema yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

__all__ = [
    "LAYOUT_AFFINITY_AFFINITIES",
    "LAYOUT_AFFINITY_PRESSURES",
    "LAYOUT_AFFINITY_RESOLVERS",
    "LAYOUT_AFFINITY_ROLES",
    "LayoutAffinityResolver",
    "validate_layout_affinity_values",
]

LAYOUT_AFFINITY_ROLES = (
    "actions",
    "aside",
    "content",
    "filters",
    "hints",
    "metadata",
    "nav",
    "rail",
    "search",
    "status",
)

LAYOUT_AFFINITY_PRESSURES = (
    "compress",
    "flex",
    "isolate",
    "overflow",
    "rigid",
)

LAYOUT_AFFINITY_AFFINITIES = (
    "block-end",
    "block-start",
    "center",
    "end",
    "fill",
    "start",
)


@dataclass(frozen=True, slots=True)
class LayoutAffinityResolver:
    """Documented parent resolver for layout-affinity attributes."""

    scope: str
    roles: tuple[str, ...]
    pressures: tuple[str, ...]
    affinities: tuple[str, ...]
    notes: str


LAYOUT_AFFINITY_RESOLVERS = MappingProxyType(
    {
        "command_bar": LayoutAffinityResolver(
            scope="direct-children",
            roles=("actions", "hints", "search", "status"),
            pressures=("compress", "flex", "rigid"),
            affinities=("end", "fill"),
            notes="Action-strip resolver for search, hints, status, and actions.",
        ),
        "filter_bar": LayoutAffinityResolver(
            scope="direct-children",
            roles=("actions", "filters", "search"),
            pressures=("compress", "flex", "rigid"),
            affinities=("end", "fill"),
            notes="Action-strip resolver for search, filter controls, and actions.",
        ),
        "card": LayoutAffinityResolver(
            scope="component-parts",
            roles=("actions", "content", "metadata"),
            pressures=("compress", "flex", "rigid"),
            affinities=("block-end", "block-start", "end", "fill", "start"),
            notes="Component-owned resolver for card header, body, and metadata parts.",
        ),
        "frame": LayoutAffinityResolver(
            scope="component-parts",
            roles=("content", "nav", "rail"),
            pressures=("compress", "flex"),
            affinities=("fill", "start"),
            notes="Structural resolver for frame rail, nav, and content overflow protection.",
        ),
        "workspace_shell": LayoutAffinityResolver(
            scope="component-parts",
            roles=("actions", "content", "nav", "rail"),
            pressures=("compress", "flex", "rigid"),
            affinities=("end", "fill", "start"),
            notes="Component-owned resolver for sidebar, main content, toolbar, and inspector.",
        ),
        "workspace_primitives": LayoutAffinityResolver(
            scope="component-parts",
            roles=("actions", "aside", "content", "metadata", "nav", "rail"),
            pressures=("compress", "flex", "rigid"),
            affinities=("block-end", "end", "fill", "start"),
            notes="Dense workspace primitives for rails, results, metrics, and inspectors.",
        ),
    }
)


def _split_values(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part for part in value.split() if part)


def validate_layout_affinity_values(
    *,
    role: str | None = None,
    pressure: str | None = None,
    affinity: str | None = None,
) -> tuple[str, ...]:
    """Return invalid layout-affinity tokens in deterministic order."""

    invalid: list[str] = []
    invalid.extend(value for value in _split_values(role) if value not in LAYOUT_AFFINITY_ROLES)
    invalid.extend(
        value for value in _split_values(pressure) if value not in LAYOUT_AFFINITY_PRESSURES
    )
    invalid.extend(
        value for value in _split_values(affinity) if value not in LAYOUT_AFFINITY_AFFINITIES
    )
    return tuple(invalid)
