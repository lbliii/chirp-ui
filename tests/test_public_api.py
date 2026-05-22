"""Public API contract — ``MANIFEST_PATH`` and ``load_manifest()``.

Sprint 3.2 of the agent-grounding-depth epic: the shipped manifest is
reachable offline via the package itself, so an agent can ground zero-shot
after ``pip install chirp-ui`` with no build step.

See ``docs/plans/done/PLAN-agent-grounding-depth.md § Sprint 3`` and
``docs/DESIGN-manifest-signature-extraction.md``.
"""

from __future__ import annotations

from collections.abc import Mapping

import chirp_ui
from chirp_ui import LIBRARY_CONTRACT, MANIFEST_PATH, THEME_PACKS, load_manifest


def test_manifest_path_exists() -> None:
    """The shipped ``manifest.json`` exists relative to the installed package."""
    assert MANIFEST_PATH.exists(), f"manifest.json not shipped: {MANIFEST_PATH}"
    assert MANIFEST_PATH.is_file()
    assert MANIFEST_PATH.name == "manifest.json"


def test_manifest_path_lives_beside_package() -> None:
    """``MANIFEST_PATH`` resolves via ``importlib.resources``, not a hand-coded path.

    Guards against accidentally publishing a path that only works in-tree
    (e.g. ``Path(__file__).parent / 'manifest.json'`` relative to the repo).
    """
    import chirp_ui as pkg

    assert MANIFEST_PATH.parent == pkg.static_path().parent


def test_load_manifest_returns_dict_with_schema() -> None:
    m = load_manifest()
    assert isinstance(m, dict)
    assert m["schema"] == "chirpui-manifest@5"
    assert m["version"] == chirp_ui.__version__


def test_load_manifest_exposes_components_and_tokens() -> None:
    m = load_manifest()
    assert "components" in m
    assert "tokens" in m
    assert "theme_packs" in m
    assert "stats" in m
    assert m["stats"]["total_components"] > 100
    # Spot-check: metric-card's signature fields made it through the build pipeline.
    mc = m["components"]["metric-card"]
    assert mc["macro"] == "metric_card"
    assert len(mc["params"]) >= 10


def test_design_system_report_matches_live_manifest_projection() -> None:
    """The public report should expose the schema-current registry projection."""
    from chirp_ui.components import design_system_report
    from chirp_ui.manifest import build_manifest

    report = design_system_report()
    manifest = build_manifest()

    assert report["schema"] == manifest["schema"]
    assert report["version"] == manifest["version"]
    assert report["stats"]["component_requirements"] == manifest["stats"]["component_requirements"]
    assert report["components"]["btn"]["requires"] == manifest["components"]["btn"]["requires"]
    assert "htmx" in report["components"]["btn"]["requires"]
    assert (
        report["components"]["metric-card"]["params"]
        == manifest["components"]["metric-card"]["params"]
    )
    assert (
        report["components"]["card"]["description"] == manifest["components"]["card"]["description"]
    )


def test_load_manifest_is_cached() -> None:
    """Repeated calls return the same object — ``functools.cache`` is wired."""
    assert load_manifest() is load_manifest()


def test_manifest_public_api_listed_in_all() -> None:
    """Both names must be in ``__all__`` so ``from chirp_ui import *`` picks them up."""
    assert "MANIFEST_PATH" in chirp_ui.__all__
    assert "load_manifest" in chirp_ui.__all__


def test_library_contract_public_api_listed_in_all() -> None:
    """Library metadata is public so frameworks can wire Chirp UI without guesses."""
    assert "LIBRARY_CONTRACT" in chirp_ui.__all__
    assert "LibraryAsset" in chirp_ui.__all__
    assert "LibraryContract" in chirp_ui.__all__
    assert "get_library_contract" in chirp_ui.__all__
    assert "THEME_PACKS" in chirp_ui.__all__
    assert "ThemePack" in chirp_ui.__all__
    assert "get_theme_pack" in chirp_ui.__all__
    assert "list_theme_packs" in chirp_ui.__all__


def test_library_contract_describes_package_roots() -> None:
    contract = chirp_ui.get_library_contract()

    assert contract is LIBRARY_CONTRACT
    assert contract.package == "chirp_ui"
    assert contract.template_package == "chirp_ui"
    assert contract.template_path == "templates"
    assert contract.static_root == chirp_ui.static_path()
    assert contract.manifest_path == MANIFEST_PATH
    assert contract.manifest_schema == load_manifest()["schema"]
    assert isinstance(contract, Mapping)
    assert contract["asset_root"] == chirp_ui.static_path()
    assert contract["manifest_schema"] == "chirpui-manifest@5"


def test_library_contract_declares_ordered_assets() -> None:
    contract = chirp_ui.get_library_contract()

    assert [asset.path for asset in contract.css] == [
        "chirpui.css",
        "chirpui-transitions.css",
    ]
    assert [asset.path for asset in contract.js] == [
        "chirpui.js",
        "chirpui-alpine.js",
    ]
    assert [asset.path for asset in contract.required_assets] == [
        "chirpui.css",
        "chirpui-transitions.css",
        "chirpui.js",
    ]
    assert [asset["path"] for asset in contract["css"]] == [
        "chirpui.css",
        "chirpui-transitions.css",
    ]
    assert [asset["type"] for asset in contract["js"]] == [
        "javascript",
        "javascript",
    ]
    assert contract["runtime"] == ("alpine",)


def test_theme_pack_catalog_is_immutable_and_ordered() -> None:
    contract = chirp_ui.get_library_contract()

    assert chirp_ui.list_theme_packs() is THEME_PACKS
    assert contract.theme_packs is THEME_PACKS
    assert [pack.name for pack in THEME_PACKS] == ["atlas", "ember", "sage"]
    assert chirp_ui.get_theme_pack("ember").path == "themes/ember.css"
    assert chirp_ui.get_theme_pack("missing") is None
    assert [pack["name"] for pack in contract["theme_packs"]] == ["atlas", "ember", "sage"]
    assert all(pack.modes == ("light", "dark", "system") for pack in THEME_PACKS)


def test_theme_pack_resources_are_shipped() -> None:
    contract = chirp_ui.get_library_contract()

    for pack in contract.theme_packs:
        resolved = contract.static_root / pack.path
        assert resolved.exists(), f"{pack.path} declared but not shipped"
        assert resolved.is_file()


def test_library_contract_assets_are_shipped() -> None:
    contract = chirp_ui.get_library_contract()

    for asset in contract.assets:
        resolved = contract.asset_path(asset)
        assert resolved.exists(), f"{asset.path} declared but not shipped"
        assert resolved.is_file()


def test_committed_manifest_matches_live_build() -> None:
    """The checked-in manifest.json must match a freshly-built one.

    This is the in-process analog of ``poe build-manifest-check``: catches
    the case where a contributor bumped a descriptor but forgot to regenerate
    the shipped JSON.
    """
    from chirp_ui.manifest import build_manifest, to_json

    live = to_json(build_manifest(), indent=2) + "\n"
    on_disk = MANIFEST_PATH.read_text(encoding="utf-8")
    assert on_disk == live, (
        "src/chirp_ui/manifest.json is stale relative to the registry.\nRun: poe build-manifest"
    )
