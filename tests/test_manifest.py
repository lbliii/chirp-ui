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

from chirp_ui.components import (
    _AUTO_EXTRAS,
    _AUTO_TRIMS,
    COMPONENT_MATURITY_LEVELS,
    COMPONENT_ROLES,
    COMPONENTS,
    RUNTIME_REQUIREMENTS,
)
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
        assert entry["composes"] == sorted(desc.composes)
        assert entry["slot_forwards"] == [
            {"slot": f.slot, "target": f.target, "target_slot": f.target_slot}
            for f in sorted(desc.slot_forwards, key=lambda f: (f.slot, f.target, f.target_slot))
        ]
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


def test_layout_descriptor_burndown_stays_explicit() -> None:
    """PR-sized layout descriptor burn-down should not regress into auto extras."""
    migrated_blocks = {
        "app-shell",
        "band",
        "page-header",
        "section-header",
    }
    assert not (migrated_blocks & set(_AUTO_EXTRAS))

    explicit_classes = {
        "app-shell": {
            "chirpui-app-shell__main--fill",
            "chirpui-app-shell__sidebar--glass",
            "chirpui-app-shell__sidebar--muted",
            "chirpui-app-shell__topbar--glass",
            "chirpui-app-shell__topbar--gradient",
        },
        "band": {"chirpui-band--pattern-dots", "chirpui-band--pattern-grid"},
        "page_header": {
            "chirpui-page-header__actions",
            "chirpui-page-header__breadcrumbs",
            "chirpui-page-header__meta",
            "chirpui-page-header__top",
        },
        "section_header": {
            "chirpui-section-header__actions",
            "chirpui-section-header__icon",
            "chirpui-section-header__title-block",
            "chirpui-section-header__title-inline",
            "chirpui-section-header__top",
        },
    }
    for component_name, class_names in explicit_classes.items():
        assert class_names <= COMPONENTS[component_name].emits

    for component_name in (
        "page-fill",
        "search-header",
        "section-collapsible",
        "shell-action-form",
        "shell-section",
    ):
        assert COMPONENTS[component_name].category == "layout"

    m = build_manifest()
    assert m["components"]["search-header"]["macro"] == "search_header"
    assert m["components"]["section-collapsible"]["macro"] == "section_collapsible"


def test_slot_forward_metadata_is_structurally_valid() -> None:
    """Composite slot forwards point from real public slots to real child slots."""
    components = build_manifest()["components"]
    for name, entry in components.items():
        composes = set(entry["composes"])
        source_slots = set(entry["slots"])
        for forward in entry["slot_forwards"]:
            assert forward["slot"] in source_slots, f"{name}: source slot missing"
            assert forward["target"] in components, f"{name}: target component missing"
            assert forward["target"] in composes, f"{name}: target not listed in composes"
            target_slots = set(components[forward["target"]]["slots"])
            assert forward["target_slot"] in target_slots, f"{name}: target slot missing"


def test_composite_slot_forward_manifest_examples() -> None:
    components = build_manifest()["components"]

    assert components["document-header"]["composes"] == ["page_header"]
    assert components["document-header"]["slot_forwards"] == [
        {"slot": "actions", "target": "page_header", "target_slot": "actions"}
    ]

    workspace = components["workspace-shell"]
    assert workspace["composes"] == ["panel", "split-layout"]
    assert set(workspace["slots"]) >= {"", "toolbar", "sidebar", "inspector"}
    assert workspace["slots_yielded"] == ["", "inspector", "sidebar"]
    assert workspace["slot_forwards"] == [
        {"slot": "inspector", "target": "panel", "target_slot": ""},
        {"slot": "sidebar", "target": "panel", "target_slot": ""},
    ]

    assert components["empty-panel-state"]["slot_forwards"] == [
        {"slot": "", "target": "empty-state", "target_slot": ""},
        {"slot": "action", "target": "empty-state", "target_slot": "action"},
        {"slot": "actions", "target": "empty-state", "target_slot": "actions"},
    ]
    assert components["file-tree"]["slot_forwards"] == [
        {"slot": "actions", "target": "panel", "target_slot": "actions"},
        {"slot": "footer", "target": "panel", "target_slot": "footer"},
        {"slot": "header", "target": "nav-tree", "target_slot": "header"},
    ]


def test_manifest_runtime_requirements_include_known_alpine_macros() -> None:
    m = build_manifest()
    assert "alpine" in m["components"]["theme-toggle"]["requires"]
    assert "alpine" in m["components"]["dropdown__item"]["requires"]
    assert "alpine" in m["components"]["copy-btn"]["requires"]


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
