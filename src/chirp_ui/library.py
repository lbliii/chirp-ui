"""Framework-neutral package metadata for Chirp UI consumers.

Frameworks and static-site generators can consume this module to discover the
public Chirp UI template root, static assets, and manifest path without reading
package internals or hardcoding filenames in theme templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

AssetKind = Literal["css", "js", "other"]

__all__ = [
    "LIBRARY_CONTRACT",
    "AssetKind",
    "LibraryAsset",
    "LibraryContract",
    "get_library_contract",
]


@dataclass(frozen=True, slots=True)
class LibraryAsset:
    """A static asset shipped from ``chirp_ui.static_path()``."""

    path: str
    kind: AssetKind
    required: bool = True
    runtime: str = ""


@dataclass(frozen=True, slots=True)
class LibraryContract:
    """Importable metadata that lets host frameworks wire Chirp UI safely."""

    package: str
    template_package: str
    template_path: str
    static_root: Path
    manifest_path: Path
    manifest_schema: str
    css: tuple[LibraryAsset, ...]
    js: tuple[LibraryAsset, ...]
    other: tuple[LibraryAsset, ...] = ()

    @property
    def assets(self) -> tuple[LibraryAsset, ...]:
        """All declared assets in stable loading order."""
        return self.css + self.js + self.other

    @property
    def required_assets(self) -> tuple[LibraryAsset, ...]:
        """Assets that hosts should include for a baseline Chirp UI install."""
        return tuple(asset for asset in self.assets if asset.required)

    def asset_path(self, asset: LibraryAsset) -> Path:
        """Resolve an asset path relative to ``static_root``."""
        return self.static_root / asset.path


_PACKAGE_ROOT = Path(__file__).parent
_STATIC_ROOT = _PACKAGE_ROOT / "templates"

LIBRARY_CONTRACT = LibraryContract(
    package="chirp_ui",
    template_package="chirp_ui",
    template_path="templates",
    static_root=_STATIC_ROOT,
    manifest_path=_PACKAGE_ROOT / "manifest.json",
    manifest_schema="chirpui-manifest@3",
    css=(
        LibraryAsset("chirpui.css", "css"),
        LibraryAsset("chirpui-transitions.css", "css"),
    ),
    js=(
        LibraryAsset("chirpui.js", "js"),
        LibraryAsset("chirpui-alpine.js", "js", required=False, runtime="alpine"),
    ),
    other=(LibraryAsset("chirpui-logo.svg", "other", required=False),),
)


def get_library_contract() -> LibraryContract:
    """Return the immutable Chirp UI package contract for host integrations."""
    return LIBRARY_CONTRACT
