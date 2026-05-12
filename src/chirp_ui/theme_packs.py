"""Immutable catalog of token-only Chirp UI theme packs."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass

__all__ = ["THEME_PACKS", "ThemePack", "get_theme_pack", "list_theme_packs"]


@dataclass(frozen=True, slots=True)
class ThemePack(Mapping[str, object]):
    """A packaged token-only CSS resource for Chirp UI applications."""

    name: str
    label: str
    path: str
    description: str = ""
    modes: tuple[str, ...] = ("light", "dark", "system")
    maturity: str = "experimental"

    def as_mapping(self) -> dict[str, object]:
        """Return the theme pack metadata as plain mapping data."""
        return {
            "name": self.name,
            "label": self.label,
            "path": self.path,
            "description": self.description,
            "modes": list(self.modes),
            "maturity": self.maturity,
        }

    def __getitem__(self, key: str) -> object:
        return self.as_mapping()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.as_mapping())

    def __len__(self) -> int:
        return len(self.as_mapping())


THEME_PACKS: tuple[ThemePack, ...] = (
    ThemePack(
        name="atlas",
        label="Atlas",
        path="themes/atlas.css",
        description="Cool operational palette for dense SaaS and dashboard interfaces.",
        maturity="experimental",
    ),
    ThemePack(
        name="ember",
        label="Ember",
        path="themes/ember.css",
        description="Warm editorial palette for content-heavy products and documentation.",
        maturity="experimental",
    ),
    ThemePack(
        name="sage",
        label="Sage",
        path="themes/sage.css",
        description="Low-glare green palette for review, planning, and knowledge work.",
        maturity="experimental",
    ),
)


def list_theme_packs() -> tuple[ThemePack, ...]:
    """Return packaged theme packs in stable display order."""
    return THEME_PACKS


def get_theme_pack(name: str) -> ThemePack | None:
    """Return a theme pack by name, or ``None`` when it is not packaged."""
    return next((pack for pack in THEME_PACKS if pack.name == name), None)
