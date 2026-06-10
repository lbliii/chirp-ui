"""Drift guard for the on-site component reference catalog (issue #166).

Locks the generated complete component index
(``site/content/docs/components/all.md``) against silent registry drift: every
**public** component in ``manifest.json`` must be discoverable on-site. A public
component is anything the manifest does *not* mark ``internal`` (neither
``maturity == "internal"`` nor ``authoring == "internal"``) -- i.e. everything
except Chirp UI composition infrastructure.

If a new public macro is added to the registry and the catalog is not
regenerated, this test fails and names exactly which components are missing.
Fix by running ``poe build-component-index`` and committing the result.
"""

import importlib.util

from chirp_ui.manifest import build_manifest
from tests.helpers import REPO_ROOT

ALL_PAGE = REPO_ROOT / "site" / "content" / "docs" / "components" / "all.md"
INDEX_PAGE = REPO_ROOT / "site" / "content" / "docs" / "components" / "_index.md"
GENERATOR = REPO_ROOT / "scripts" / "build_component_index.py"

START_MARKER = "<!-- chirpui:generated:start -->"
END_MARKER = "<!-- chirpui:generated:end -->"


def _load_generator():
    spec = importlib.util.spec_from_file_location("build_component_index", GENERATOR)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _generated_block(text: str) -> str:
    """Return only the manifest-generated region between the splice markers."""
    msg = "all.md is missing the generated-block markers. Run: poe build-component-index"
    assert START_MARKER in text, msg
    assert END_MARKER in text, msg
    return text.partition(START_MARKER)[2].partition(END_MARKER)[0]


def _is_internal(entry: dict) -> bool:
    return entry.get("maturity") == "internal" or entry.get("authoring") == "internal"


def _catalog_token(name: str, entry: dict) -> str:
    """The backticked token the catalog uses to list *entry* (macro, else name)."""
    macro = entry.get("macro")
    return f"`{macro}`" if macro else f"`{name}`"


def _public_components() -> dict[str, dict]:
    return {
        name: entry
        for name, entry in build_manifest()["components"].items()
        if not _is_internal(entry)
    }


def test_onsite_catalog_covers_every_public_component() -> None:
    """Every public manifest component must appear in the on-site index page."""
    assert ALL_PAGE.is_file(), (
        f"{ALL_PAGE.relative_to(REPO_ROOT)} is missing. Run: poe build-component-index"
    )
    block = _generated_block(ALL_PAGE.read_text(encoding="utf-8"))
    public = _public_components()

    missing = sorted(
        name for name, entry in public.items() if _catalog_token(name, entry) not in block
    )

    assert not missing, (
        f"{len(missing)} public component(s) are not listed in "
        f"{ALL_PAGE.relative_to(REPO_ROOT)} -- the on-site catalog has drifted from "
        f"the registry. Run `poe build-component-index` and commit the result. "
        f"Missing: {', '.join(missing)}"
    )


def test_onsite_catalog_omits_internal_infrastructure() -> None:
    """Internal composition infrastructure stays out of the public catalog body."""
    block = _generated_block(ALL_PAGE.read_text(encoding="utf-8"))
    components = build_manifest()["components"]
    internal = {name: entry for name, entry in components.items() if _is_internal(entry)}
    # Sanity: the manifest still marks some infrastructure internal.
    assert internal
    for name, entry in internal.items():
        # The generated body lists components by their row token. An internal
        # component must not appear as its own catalog row.
        assert _catalog_token(name, entry) not in block, (
            f"internal infrastructure {name!r} should not be listed in the public on-site catalog"
        )


def test_onsite_catalog_is_fresh() -> None:
    """The committed page must match what the generator emits (no manual drift)."""
    module = _load_generator()
    generated = module.build()
    current = ALL_PAGE.read_text(encoding="utf-8")
    assert current == generated, (
        "site/content/docs/components/all.md is stale relative to the manifest. "
        "Run: poe build-component-index"
    )


def test_onsite_catalog_links_back_to_discovery_surfaces() -> None:
    """The complete index must point on-site, never to GitHub or a local app."""
    text = ALL_PAGE.read_text(encoding="utf-8")
    assert "/showcase/" in text
    assert "/api/" in text
    # The catalog must not push readers off-site to run a local app.
    assert "examples/component-showcase/app.py" not in text
    assert "python examples/component-showcase" not in text


def test_components_index_links_to_complete_catalog() -> None:
    """The category landing page must link to the complete generated index."""
    text = INDEX_PAGE.read_text(encoding="utf-8")
    assert "./all/" in text or "(all.md)" in text or "/docs/components/all/" in text
