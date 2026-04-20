"""Manifest round-trip and contract tests (Sprint 7).

The manifest is the agent-groundable artifact: AI coding agents read it to
cite real chirp-ui classes/tokens/slots. Drift between the registry and the
manifest makes agents hallucinate. These tests pin the contract:

* ``build_manifest()`` is deterministic (byte-identical across calls).
* Every ``COMPONENTS`` entry and every ``TOKEN_CATALOG`` entry appears.
* Every ``descriptor.emits`` class appears in the manifest.
* Output serializes to valid JSON.

See ``docs/PLAN-css-scope-and-layer.md § Sprint 7``.
"""

import json
import subprocess
import sys

from chirp_ui.components import COMPONENTS
from chirp_ui.manifest import SCHEMA, build_manifest, to_json
from chirp_ui.tokens import TOKEN_CATALOG


def test_manifest_is_deterministic() -> None:
    first = to_json(build_manifest())
    second = to_json(build_manifest())
    assert first == second, "build_manifest must be byte-for-byte deterministic"


def test_manifest_schema_and_version_present() -> None:
    m = build_manifest()
    assert m["schema"] == SCHEMA
    assert isinstance(m["version"], str)
    assert m["version"]


def test_manifest_covers_every_component() -> None:
    m = build_manifest()
    assert set(m["components"]) == set(COMPONENTS)
    for name, desc in COMPONENTS.items():
        entry = m["components"][name]
        assert entry["block"] == desc.block
        assert entry["template"] == desc.template
        assert entry["category"] == desc.category
        # Lists are sorted in the manifest for stability.
        assert entry["emits"] == sorted(desc.emits)
        assert entry["elements"] == sorted(desc.elements)
        assert entry["variants"] == sorted(desc.variants)
        assert entry["sizes"] == sorted(desc.sizes)
        assert entry["modifiers"] == sorted(desc.modifiers)
        assert entry["slots"] == sorted(desc.slots)
        assert entry["tokens"] == sorted(desc.tokens)
        assert entry["extra_emits"] == sorted(desc.extra_emits)


def test_manifest_covers_every_token() -> None:
    m = build_manifest()
    assert set(m["tokens"]) == set(TOKEN_CATALOG)
    for name, t in TOKEN_CATALOG.items():
        assert m["tokens"][name] == {"category": t.category, "scope": t.scope}


def test_manifest_stats_match_counts() -> None:
    m = build_manifest()
    assert m["stats"]["total_components"] == len(COMPONENTS)
    assert m["stats"]["total_tokens"] == len(TOKEN_CATALOG)


def test_manifest_serializes_to_valid_json() -> None:
    text = to_json(build_manifest())
    reloaded = json.loads(text)
    assert reloaded["schema"] == SCHEMA
    assert set(reloaded["components"]) == set(COMPONENTS)


def test_cli_emits_same_manifest() -> None:
    """`python -m chirp_ui.manifest --json` matches build_manifest()."""
    result = subprocess.run(
        [sys.executable, "-m", "chirp_ui.manifest", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    cli_manifest = json.loads(result.stdout)
    direct_manifest = build_manifest()
    # Compare parsed dicts (JSON-string compare would diff on trailing newline).
    assert cli_manifest == direct_manifest
