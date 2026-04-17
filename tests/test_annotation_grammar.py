"""Annotation contract: every `{% provide %}` and `consume()` call is documented.

Each `{% provide _key = ... %}` statement must have a sibling
`{# @provides _key — consumed by: ... #}` annotation, and each `consume("_key", ...)`
call must have a sibling `{# @consumes _key from: ... — falls back to ... #}`
annotation. New uses without annotations break the contract — failures point
at the file:line so authors can add the annotation immediately.

Annotation grammar lives in ``docs/PROVIDE-CONSUME-KEYS.md`` and is parsed by
``chirp_ui.inspect``. See ``.context/composite-contracts-plan.md`` § Sprint 2 D3.
"""

from chirp_ui.inspect import list_consumes, list_provides

# Allow-list of internal context keys. Any provide/consume using a key not in
# this set should be flagged for review (likely a typo or undocumented key).
KNOWN_KEYS: frozenset[str] = frozenset(
    {
        "_accordion_name",
        "_bar_density",
        "_bar_surface",
        "_card_variant",
        "_form_density",
        "_hero_variant",
        "_nav_current_path",
        "_site_nav_current_path",
        "_sse_state",
        "_streaming_role",
        "_surface_variant",
        "_suspense_busy",
        "_table_align",
    }
)


def test_every_provide_has_annotation():
    missing = [r for r in list_provides() if not r.raw_annotation]
    assert not missing, "provides without @provides annotation:\n" + "\n".join(
        f"  - {r.template}:{r.line} {{% provide {r.key} = ... %}}" for r in missing
    )


def test_every_consume_has_annotation():
    missing = [r for r in list_consumes() if not r.raw_annotation]
    assert not missing, "consumes without @consumes annotation:\n" + "\n".join(
        f"  - {r.template}:{r.line} consume({r.key!r}, ...)" for r in missing
    )


def test_all_provided_keys_are_known():
    unknown = sorted({r.key for r in list_provides()} - KNOWN_KEYS)
    assert not unknown, (
        f"unknown provided keys (add to KNOWN_KEYS or fix typo): {unknown}\n"
        f"see docs/PROVIDE-CONSUME-KEYS.md for the canonical registry"
    )


def test_all_consumed_keys_are_known():
    unknown = sorted({r.key for r in list_consumes()} - KNOWN_KEYS)
    assert not unknown, (
        f"unknown consumed keys (add to KNOWN_KEYS or fix typo): {unknown}\n"
        f"see docs/PROVIDE-CONSUME-KEYS.md for the canonical registry"
    )


def test_consume_fallback_is_documented():
    """Every annotated consume must declare its fallback (no empty 'falls back to')."""
    bad = [r for r in list_consumes() if r.raw_annotation and not r.fallback]
    assert not bad, "consumes with empty `falls back to` clause:\n" + "\n".join(
        f"  - {r.template}:{r.line} {r.key}" for r in bad
    )


def test_provide_annotations_match_statement_keys():
    """The @provides annotation key must match the statement's key (no typos)."""
    for record in list_provides():
        if not record.raw_annotation:
            continue
        # raw_annotation contains `@provides _key`; verify the statement key appears
        assert f"@provides {record.key} " in record.raw_annotation, (
            f"annotation key mismatch at {record.template}:{record.line}: "
            f"statement uses {record.key!r}, annotation says {record.raw_annotation!r}"
        )


def test_consume_annotations_match_call_keys():
    """The @consumes annotation must mention each consume() call's key."""
    for record in list_consumes():
        if not record.raw_annotation:
            continue
        assert record.key in record.raw_annotation, (
            f"annotation key mismatch at {record.template}:{record.line}: "
            f"call uses {record.key!r}, annotation says {record.raw_annotation!r}"
        )
