"""Test-only shape for the proposed layout-affinity manifest projection."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class LayoutResolverFixture:
    scope: str
    roles: tuple[str, ...]
    pressures: tuple[str, ...]
    affinities: tuple[str, ...]
    notes: str

    def as_manifest(self) -> dict[str, object]:
        data = asdict(self)
        data["roles"] = sorted(self.roles)
        data["pressures"] = sorted(self.pressures)
        data["affinities"] = sorted(self.affinities)
        return data


@dataclass(frozen=True, slots=True)
class LayoutPartFixture:
    part: str
    role: str
    pressure: str
    affinity: str

    def as_manifest(self) -> dict[str, str]:
        return asdict(self)


def test_future_layout_resolver_projection_shape_matches_rfc() -> None:
    resolver = LayoutResolverFixture(
        scope="direct-children",
        roles=("search", "filters", "hints", "actions", "status"),
        pressures=("flex", "compress", "rigid"),
        affinities=("fill", "end"),
        notes="Resolved by command_bar/filter_bar action-strip chrome.",
    )

    assert resolver.as_manifest() == {
        "scope": "direct-children",
        "roles": ["actions", "filters", "hints", "search", "status"],
        "pressures": ["compress", "flex", "rigid"],
        "affinities": ["end", "fill"],
        "notes": "Resolved by command_bar/filter_bar action-strip chrome.",
    }


def test_future_layout_parts_projection_shape_matches_rfc() -> None:
    parts = [
        LayoutPartFixture("header-content", "content", "flex", "fill"),
        LayoutPartFixture("header-actions", "actions", "rigid", "end"),
    ]

    assert [part.as_manifest() for part in parts] == [
        {
            "part": "header-content",
            "role": "content",
            "pressure": "flex",
            "affinity": "fill",
        },
        {
            "part": "header-actions",
            "role": "actions",
            "pressure": "rigid",
            "affinity": "end",
        },
    ]
