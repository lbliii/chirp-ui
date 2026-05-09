"""Framework-neutral package metadata for Chirp UI consumers.

Frameworks and static-site generators can consume this module to discover the
public Chirp UI template root, static assets, and manifest path without reading
package internals or hardcoding filenames in theme templates.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

AssetKind = Literal["css", "javascript", "other"]

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
class LibraryContract(Mapping[str, object]):
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

    def as_mapping(self) -> dict[str, object]:
        """Return the host-integration contract as plain mapping data."""
        return {
            "package": self.package,
            "template_package": self.template_package,
            "template_path": self.template_path,
            "asset_root": self.static_root,
            "static_path": self.static_root,
            "manifest_path": self.manifest_path,
            "manifest_schema": self.manifest_schema,
            "css": tuple(_asset_mapping(asset) for asset in self.css),
            "js": tuple(_asset_mapping(asset) for asset in self.js),
            "other": tuple(_asset_mapping(asset) for asset in self.other),
            "runtime": tuple(
                dict.fromkeys(asset.runtime for asset in self.assets if asset.runtime)
            ),
        }

    def __getitem__(self, key: str) -> object:
        return self.as_mapping()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.as_mapping())

    def __len__(self) -> int:
        return len(self.as_mapping())


def _asset_mapping(asset: LibraryAsset) -> dict[str, object]:
    return {
        "path": asset.path,
        "type": asset.kind,
        "required": asset.required,
        "runtime": asset.runtime,
    }


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
        LibraryAsset("chirpui.js", "javascript"),
        LibraryAsset(
            "chirpui-alpine.js",
            "javascript",
            required=False,
            runtime="alpine",
        ),
    ),
    other=(LibraryAsset("chirpui-logo.svg", "other", required=False),),
)


def get_library_contract() -> LibraryContract:
    """Return the immutable Chirp UI package contract for host integrations."""
    return LIBRARY_CONTRACT
