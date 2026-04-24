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
import re
import subprocess
import sys

from chirp_ui.components import (
    _AUTO_EXTRAS,
    _AUTO_TRIMS,
    COMPONENT_MATURITY_LEVELS,
    COMPONENT_ROLES,
    COMPONENTS,
    RUNTIME_REQUIREMENTS,
)
from chirp_ui.manifest import SCHEMA, _macro_source, _resolve_macro, build_manifest, to_json
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
        assert entry["maturity"] == desc.resolved_maturity
        assert entry["role"] == desc.resolved_role
        assert set(entry["requires"]) >= set(desc.requires)
        assert set(entry["requires"]) <= set(RUNTIME_REQUIREMENTS)
        # Lists are sorted in the manifest for stability.
        assert entry["emits"] == sorted(desc.emits)
        assert entry["elements"] == sorted(desc.elements)
        assert entry["variants"] == sorted(desc.variants)
        assert entry["sizes"] == sorted(desc.sizes)
        assert entry["modifiers"] == sorted(desc.modifiers)
        # Sprint 2 widened ``slots`` to the union of descriptor + AST-extracted
        # slots. The manifest must always be a superset of the descriptor;
        # parity is enforced separately by ``tests/test_slot_parity.py``.
        assert set(entry["slots"]) >= set(desc.slots)
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
    assert sum(m["stats"]["component_maturity"].values()) == len(COMPONENTS)
    assert sum(m["stats"]["component_roles"].values()) == len(COMPONENTS)
    assert set(m["stats"]["component_maturity"]) <= set(COMPONENT_MATURITY_LEVELS)
    assert set(m["stats"]["component_roles"]) <= set(COMPONENT_ROLES)
    assert set(m["stats"]["component_requirements"]) <= set(RUNTIME_REQUIREMENTS)


def test_maturity_taxonomy_is_explicit_for_templated_components() -> None:
    """Rendered component descriptors must not rely on fallback maturity."""
    assert COMPONENT_MATURITY_LEVELS == ("stable", "experimental", "legacy", "internal")
    missing = sorted(
        name for name, desc in COMPONENTS.items() if desc.template and not desc.maturity
    )
    assert not missing, "templated components missing explicit maturity: " + ", ".join(missing)


def test_manifest_registry_debt_scorecard_matches_registry() -> None:
    """Stats expose the registry/CSS reconciliation burn-down as numbers."""
    debt = build_manifest()["stats"]["registry_debt"]
    assert debt == {
        "auto_category_components": sum(
            1 for desc in COMPONENTS.values() if desc.category == "auto"
        ),
        "auto_extra_blocks": len(_AUTO_EXTRAS),
        "auto_extra_classes": sum(len(classes) for classes in _AUTO_EXTRAS.values()),
        "auto_trim_blocks": len(_AUTO_TRIMS),
        "auto_trim_classes": sum(len(classes) for classes in _AUTO_TRIMS.values()),
        "explicit_extra_blocks": sum(1 for desc in COMPONENTS.values() if desc.extra_emits),
        "explicit_extra_classes": sum(len(desc.extra_emits) for desc in COMPONENTS.values()),
    }
    assert debt["auto_extra_classes"] > 0
    assert debt["auto_trim_classes"] > 0


def test_manifest_quality_scorecard_has_no_public_metadata_gaps() -> None:
    """Public templated components must be fully groundable for agent consumers."""
    m = build_manifest()
    quality = m["stats"]["manifest_quality"]
    public_templated = [
        name
        for name, entry in m["components"].items()
        if entry["template"] and entry["maturity"] != "internal"
    ]
    assert quality == {
        "public_templated_components": len(public_templated),
        "missing_macro": 0,
        "missing_maturity": 0,
        "missing_role": 0,
        "missing_description": 0,
        "missing_slot_metadata": 0,
    }


def test_public_templated_manifest_entries_have_quality_fields() -> None:
    """Quality gate with precise failure output when one component drifts."""
    m = build_manifest()
    missing: list[str] = []
    for name, entry in m["components"].items():
        if not entry["template"] or entry["maturity"] == "internal":
            continue
        missing.extend(
            f"{name}: {key}"
            for key in ("macro", "maturity", "role", "description")
            if not entry[key]
        )
        if not isinstance(entry["slots"], list):
            missing.append(f"{name}: slots")
        if not isinstance(entry["slots_extracted"], list):
            missing.append(f"{name}: slots_extracted")
    assert not missing, "public templated manifest entries missing quality fields: " + ", ".join(
        missing
    )


def test_manifest_runtime_requirements_include_known_alpine_macros() -> None:
    m = build_manifest()
    assert "alpine" in m["components"]["theme-toggle"]["requires"]
    assert "alpine" in m["components"]["dropdown__item"]["requires"]
    assert "alpine" in m["components"]["copy-btn"]["requires"]
    assert "alpine" in m["components"]["ripple-btn"]["requires"]
    assert "alpine" in m["components"]["split-panel"]["requires"]


def test_manifest_runtime_requirements_include_known_htmx_macros() -> None:
    m = build_manifest()
    assert "htmx" in m["components"]["btn"]["requires"]
    assert "htmx" in m["components"]["pagination"]["requires"]
    assert "htmx" in m["components"]["infinite-scroll"]["requires"]
    assert "htmx" in m["components"]["streaming_bubble"]["requires"]
    assert "htmx" in m["components"]["fragment-island"]["requires"]


def test_manifest_runtime_requirements_cover_template_runtime_markers() -> None:
    """Alpine/HTMX marker drift should surface in the manifest."""
    alpine_pattern = re.compile(
        r"""(?<![\w-])(?:x-data|x-show|x-ref|x-cloak|x-transition|x-on:|x-bind:|:aria-[\w-]+|:class|:id|@(?:click|keydown|keyup|submit|input|change|focus|blur|mouseenter|mouseleave)[\w:.-]*)\b"""
    )
    htmx_pattern = re.compile(r"""\b(?:hx-[\w:-]+|sse-[\w:-]+|hx_[A-Za-z]\w*)\b""")
    manifest_components = build_manifest()["components"]
    missing: list[str] = []
    for name, desc in COMPONENTS.items():
        macro_info = _resolve_macro(desc)
        if macro_info is None:
            continue
        source = _macro_source(macro_info)
        requirements = set(manifest_components[name]["requires"])
        if alpine_pattern.search(source) and "alpine" not in requirements:
            missing.append(f"{name}: alpine")
        if htmx_pattern.search(source) and "htmx" not in requirements:
            missing.append(f"{name}: htmx")
    assert not missing, "runtime markers missing from manifest requirements: " + ", ".join(missing)


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
