from __future__ import annotations

from types import MappingProxyType

from chirp_ui.layout_affinity import (
    LAYOUT_AFFINITY_AFFINITIES,
    LAYOUT_AFFINITY_PRESSURES,
    LAYOUT_AFFINITY_RESOLVERS,
    LAYOUT_AFFINITY_ROLES,
    LAYOUT_RHYTHM_RELATIONSHIPS,
    validate_layout_affinity_values,
)
from tests.layout_affinity_contract import ALLOWED_SOURCE_VALUES, RESOLVER_MATRIX


def test_layout_affinity_importable_vocabulary_matches_source_scan_contract() -> None:
    assert set(ALLOWED_SOURCE_VALUES["data-chirpui-role"]).issubset(LAYOUT_AFFINITY_ROLES)
    assert set(ALLOWED_SOURCE_VALUES["data-chirpui-pressure"]).issubset(LAYOUT_AFFINITY_PRESSURES)
    assert set(ALLOWED_SOURCE_VALUES["data-chirpui-affinity"]).issubset(LAYOUT_AFFINITY_AFFINITIES)
    assert set(ALLOWED_SOURCE_VALUES["data-chirpui-rhythm"]).issubset(LAYOUT_RHYTHM_RELATIONSHIPS)


def test_layout_affinity_resolver_contracts_cover_documented_matrix() -> None:
    assert isinstance(LAYOUT_AFFINITY_RESOLVERS, MappingProxyType)
    for resolver in RESOLVER_MATRIX:
        assert resolver in LAYOUT_AFFINITY_RESOLVERS

    workspace = LAYOUT_AFFINITY_RESOLVERS["workspace_primitives"]
    assert workspace.scope == "component-parts"
    assert "rail" in workspace.roles
    assert "aside" in workspace.roles
    assert "compress" in workspace.pressures
    assert "fill" in workspace.affinities


def test_validate_layout_affinity_values_returns_only_unknown_tokens() -> None:
    assert (
        validate_layout_affinity_values(
            role="search hints",
            pressure="flex compress",
            affinity="fill end",
        )
        == ()
    )
    assert validate_layout_affinity_values(
        role="left search",
        pressure="grow flex",
        affinity="x-axis end",
    ) == ("left", "grow", "x-axis")
