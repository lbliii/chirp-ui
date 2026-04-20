"""Manifest signature contract tests (Sprint 1 of agent-grounding-depth epic).

These tests pin the ``@2`` schema additions: every component descriptor with
a discoverable macro surfaces ``params`` (positional order, ``has_default`` /
``is_required`` flags), ``macro`` (resolved identifier), and ``lineno``.

See ``docs/PLAN-agent-grounding-depth.md § Sprint 1`` and
``docs/DESIGN-manifest-signature-extraction.md``.
"""

from __future__ import annotations

from chirp_ui.components import COMPONENTS
from chirp_ui.manifest import SCHEMA, build_manifest


def test_schema_is_v2() -> None:
    assert SCHEMA == "chirpui-manifest@2"
    assert build_manifest()["schema"] == "chirpui-manifest@2"


def test_metric_card_signature() -> None:
    """Worked example from the design doc — the canary that proves the path works."""
    entry = build_manifest()["components"]["metric-card"]
    assert entry["macro"] == "metric_card"
    assert entry["template"] == "metric_grid.html"
    assert entry["lineno"] > 0

    names = [p["name"] for p in entry["params"]]
    assert names == [
        "value",
        "label",
        "icon",
        "trend",
        "trend_direction",
        "hint",
        "href",
        "icon_bg",
        "footer_label",
        "footer_href",
        "cls",
        "attrs",
        "attrs_unsafe",
        "attrs_map",
    ]
    # Trailing-defaults convention: the first two are positional/required.
    assert entry["params"][0] == {"name": "value", "has_default": False, "is_required": True}
    assert entry["params"][1] == {"name": "label", "has_default": False, "is_required": True}
    assert entry["params"][2]["has_default"] is True
    assert entry["params"][2]["is_required"] is False


def test_btn_signature_includes_hx_and_aria() -> None:
    entry = build_manifest()["components"]["btn"]
    assert entry["macro"] == "btn"
    names = [p["name"] for p in entry["params"]]
    # Spot-check the hx_* / aria_* surface — high-traffic and the docstring
    # contract for every htmx-aware caller.
    assert "label" in names
    assert "hx" in names
    assert "hx_post" in names
    assert "hx_target" in names
    assert "aria_label" in names
    # First param is required (positional label).
    assert names[0] == "label"
    assert entry["params"][0]["is_required"] is True


def test_card_signature_required_set() -> None:
    """All ``card()`` params have defaults — zero required."""
    entry = build_manifest()["components"]["card"]
    assert entry["macro"] == "card"
    required = [p for p in entry["params"] if p["is_required"]]
    assert required == []


def test_field_signature_resolves_through_forms_template() -> None:
    """``field`` descriptor maps to a macro inside the multi-macro forms.html."""
    entry = build_manifest()["components"]["field"]
    # forms.html holds form/fieldset/field_wrapper/text_field/etc.; the
    # 'field' descriptor's block→macro fallback won't match any of them
    # (no bare 'field' macro). Until an explicit ``macro=`` is added, this
    # surfaces the gap honestly: macro=None, params=[].  The contract is
    # that the build doesn't fail, which is the point of this test.
    assert entry["template"] == "forms.html"
    if entry["macro"] is None:
        assert entry["params"] == []
    else:
        assert isinstance(entry["params"], list)


def test_alert_signature_resolves() -> None:
    """``alert`` is a high-traffic feedback macro — must surface its params."""
    entry = build_manifest()["components"]["alert"]
    assert entry["macro"] == "alert"
    names = [p["name"] for p in entry["params"]]
    assert len(names) > 0
    assert "variant" in names


def test_components_with_no_template_emit_empty_params() -> None:
    """``category=auto`` descriptors (CSS-only, no macro) must not error."""
    m = build_manifest()
    for name, entry in m["components"].items():
        desc = COMPONENTS[name]
        if not desc.template:
            assert entry["macro"] is None, f"{name}: macro should be null with no template"
            assert entry["params"] == [], f"{name}: params should be empty with no template"
            assert entry["lineno"] == 0


def test_param_dict_shape_is_stable() -> None:
    """Every param dict has exactly {name, has_default, is_required}."""
    expected_keys = {"name", "has_default", "is_required"}
    for entry in build_manifest()["components"].values():
        for p in entry["params"]:
            assert set(p.keys()) == expected_keys
            assert isinstance(p["name"], str)
            assert isinstance(p["has_default"], bool)
            assert isinstance(p["is_required"], bool)
            # Invariant: is_required == not has_default
            assert p["is_required"] is (not p["has_default"])


def test_param_order_preserved_not_sorted() -> None:
    """Params are positional — order matters and must NOT be sorted alphabetically."""
    entry = build_manifest()["components"]["metric-card"]
    names = [p["name"] for p in entry["params"]]
    assert names != sorted(names), (
        "metric_card params must preserve declaration order (value, label first), "
        "not be alphabetically sorted"
    )


def test_components_with_params_count_in_stats() -> None:
    """Stats count tracks resolved-macro count, not non-empty-params count.

    A no-arg macro like ``theme_toggle()`` resolves cleanly but has zero
    params — it still counts as "macro discovered" because the manifest
    knows how to call it (just with no arguments).
    """
    m = build_manifest()
    expected = sum(1 for entry in m["components"].values() if entry["macro"] is not None)
    assert m["stats"]["components_with_params"] == expected
    # Sanity: should be a meaningful fraction of the registry, not zero.
    assert m["stats"]["components_with_params"] > 100


def test_unmapped_descriptors_degrade_gracefully() -> None:
    """``shimmer-btn`` block→macro mismatch (template has ``shimmer_button``).

    Without an explicit ``macro=`` field, the resolver returns no match and
    the entry surfaces empty ``params`` rather than raising. This is the
    safety net that lets the registry stay incomplete without breaking the
    manifest build.
    """
    entry = build_manifest()["components"]["shimmer-btn"]
    assert entry["template"] == "shimmer_button.html"
    # Either: explicit macro added in a follow-up commit (then params populated),
    # or: still unmapped (then macro is null).  Both are valid; the contract is
    # that the build doesn't fail.
    if entry["macro"] is None:
        assert entry["params"] == []
    else:
        assert entry["macro"] == "shimmer_button"
        assert len(entry["params"]) > 0


def test_param_extraction_is_cached() -> None:
    """Two manifest builds reuse the per-template AST cache (no re-parse)."""
    from chirp_ui._macro_introspect import macros_in_template

    macros_in_template.cache_clear()
    build_manifest()
    info_first = macros_in_template.cache_info()
    build_manifest()
    info_second = macros_in_template.cache_info()
    assert info_second.hits > info_first.hits
    # No new misses on the second call — every template was already in cache.
    assert info_second.misses == info_first.misses


# ---------------------------------------------------------------------------
# Sprint 2: slots / provides / consumes
# ---------------------------------------------------------------------------


def test_card_slots_extracted_match_template() -> None:
    """``card`` exposes the canonical 5-slot surface auto-extracted from AST."""
    entry = build_manifest()["components"]["card"]
    assert sorted(entry["slots_extracted"]) == sorted(
        ["", "header_actions", "media", "body_actions", "footer"]
    )
    # Manifest contract: union ⊇ extracted (never under-reports).
    assert set(entry["slots"]) >= set(entry["slots_extracted"])


def test_modal_slots_extracted_match_template() -> None:
    entry = build_manifest()["components"]["modal"]
    assert sorted(entry["slots_extracted"]) == sorted(["", "header_actions", "footer"])


def test_panel_slots_extracted_includes_actions() -> None:
    """``panel`` declares no slots in the descriptor but the template has 3."""
    entry = build_manifest()["components"]["panel"]
    assert sorted(entry["slots_extracted"]) == sorted(["", "actions", "footer"])


def test_metric_card_has_no_slots() -> None:
    """``metric_card`` is param-driven, no ``{% slot %}`` tags."""
    entry = build_manifest()["components"]["metric-card"]
    assert entry["slots_extracted"] == []


def test_default_slot_normalized_to_empty_string() -> None:
    """kida's ``"default"`` sentinel must surface as ``""`` to match descriptor convention."""
    entry = build_manifest()["components"]["card"]
    assert "" in entry["slots_extracted"]
    assert "default" not in entry["slots_extracted"]


def test_card_provides_card_variant() -> None:
    entry = build_manifest()["components"]["card"]
    assert entry["provides"] == ["_card_variant"]
    assert entry["consumes"] == []


def test_surface_provides_surface_variant() -> None:
    entry = build_manifest()["components"]["surface"]
    assert "_surface_variant" in entry["provides"]


def test_btn_consumes_bar_density_and_suspense_busy() -> None:
    entry = build_manifest()["components"]["btn"]
    assert "_bar_density" in entry["consumes"]
    assert "_suspense_busy" in entry["consumes"]


def test_callout_consumes_surface_variant() -> None:
    entry = build_manifest()["components"]["callout"]
    assert "_surface_variant" in entry["consumes"]


def test_alert_consumes_card_variant() -> None:
    entry = build_manifest()["components"]["alert"]
    assert "_card_variant" in entry["consumes"]


def test_provides_consumes_lists_are_sorted() -> None:
    """Determinism: every provides/consumes list must be sorted."""
    for entry in build_manifest()["components"].values():
        assert entry["provides"] == sorted(entry["provides"])
        assert entry["consumes"] == sorted(entry["consumes"])


def test_components_with_provides_consumes_stats() -> None:
    """Stats track macro-attributed provides/consumes counts."""
    m = build_manifest()
    expected_p = sum(1 for e in m["components"].values() if e["provides"])
    expected_c = sum(1 for e in m["components"].values() if e["consumes"])
    assert m["stats"]["components_with_provides"] == expected_p
    assert m["stats"]["components_with_consumes"] == expected_c
    # Sanity: at least the canonical providers/consumers are accounted for.
    assert m["stats"]["components_with_provides"] >= 5
    assert m["stats"]["components_with_consumes"] >= 5


def test_unmapped_descriptors_emit_empty_provides_consumes() -> None:
    """``shimmer-btn`` is unmapped — provides/consumes stay empty, not error."""
    entry = build_manifest()["components"]["shimmer-btn"]
    if entry["macro"] is None:
        assert entry["provides"] == []
        assert entry["consumes"] == []
        assert entry["slots_extracted"] == []
