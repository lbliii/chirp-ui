"""Public API contract — ``MANIFEST_PATH`` and ``load_manifest()``.

Sprint 3.2 of the agent-grounding-depth epic: the shipped manifest is
reachable offline via the package itself, so an agent can ground zero-shot
after ``pip install chirp-ui`` with no build step.

See ``docs/PLAN-agent-grounding-depth.md § Sprint 3`` and
``docs/DESIGN-manifest-signature-extraction.md``.
"""

from __future__ import annotations

import chirp_ui
from chirp_ui import MANIFEST_PATH, load_manifest


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
    assert m["schema"] == "chirpui-manifest@3"
    assert m["version"] == chirp_ui.__version__


def test_load_manifest_exposes_components_and_tokens() -> None:
    m = load_manifest()
    assert "components" in m
    assert "tokens" in m
    assert "stats" in m
    assert m["stats"]["total_components"] > 100
    # Spot-check: metric-card's signature fields made it through the build pipeline.
    mc = m["components"]["metric-card"]
    assert mc["macro"] == "metric_card"
    assert len(mc["params"]) >= 10


def test_load_manifest_is_cached() -> None:
    """Repeated calls return the same object — ``functools.cache`` is wired."""
    assert load_manifest() is load_manifest()


def test_manifest_public_api_listed_in_all() -> None:
    """Both names must be in ``__all__`` so ``from chirp_ui import *`` picks them up."""
    assert "MANIFEST_PATH" in chirp_ui.__all__
    assert "load_manifest" in chirp_ui.__all__


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
