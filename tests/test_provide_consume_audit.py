"""Provide/consume graph audit — surface dead provides and annotation drift.

Guards against three rot patterns:

1. **Dead provides** — `{% provide %}` statements whose key nothing consumes.
   A known exception (``_bar_surface``) is explicitly reserved for future
   bar children; anything else is a regression.
2. **Unprovided consumes** — `consume()` calls whose key nothing provides in
   bundled templates. ``_sse_state`` is the one legitimate case (app-side
   provider); anything else signals an orphan consumer.
3. **Annotation drift** — a ``@provides`` comment lists a consumer macro that
   doesn't actually have a matching ``@consumes`` annotation for the key.
   Catches renamed macros and rotted docs.

See ``.context/composite-contracts-plan.md`` § Sprint 3.
"""

from chirp_ui.inspect import audit_provide_consume

# Keys intentionally provided without a bundled consumer. Apps wire these up
# to their own macros; `_bar_surface` is documented as reserved for future
# bar children in ``command_bar.html`` / ``filter_bar.html``.
KNOWN_RESERVED: frozenset[str] = frozenset({"_bar_surface"})

# Keys expected to be provided by app code, not bundled chirp-ui templates.
# ``_sse_state`` is set by app-side HTMX handlers driving ``sse_retry``.
EXTERNAL_PROVIDERS: frozenset[str] = frozenset({"_sse_state"})


def test_no_unexpected_dead_provides():
    report = audit_provide_consume()
    unexpected = sorted({r.key for r in report.dead_provides} - KNOWN_RESERVED)
    assert not unexpected, (
        f"unexpected dead provides (provided but never consumed): {unexpected}\n"
        f"either wire up a consumer or add the key to KNOWN_RESERVED with a comment."
    )


def test_no_unexpected_unprovided_consumes():
    report = audit_provide_consume()
    unexpected = sorted({r.key for r in report.unprovided_consumes} - EXTERNAL_PROVIDERS)
    assert not unexpected, (
        f"unexpected unprovided consumes (consumed but never provided): {unexpected}\n"
        f"either add a bundled provider or add the key to EXTERNAL_PROVIDERS."
    )


def test_no_annotation_drift():
    report = audit_provide_consume()
    assert not report.annotation_drift, "annotation drift detected:\n" + "\n".join(
        f"  {msg}" for msg in report.annotation_drift
    )


def test_known_reserved_actually_dead():
    """Sanity: KNOWN_RESERVED entries should actually appear in dead_provides.

    Catches the case where a previously-dead key gets wired up but we forget
    to remove it from the allow-list, letting future regressions sneak through.
    """
    report = audit_provide_consume()
    dead_keys = {r.key for r in report.dead_provides}
    stale_exemptions = KNOWN_RESERVED - dead_keys
    assert not stale_exemptions, (
        f"KNOWN_RESERVED contains keys that now have consumers: {sorted(stale_exemptions)}. "
        f"Remove them from the allow-list."
    )


def test_known_external_providers_actually_unprovided():
    """Sanity: EXTERNAL_PROVIDERS entries should actually be unprovided."""
    report = audit_provide_consume()
    unprovided_keys = {r.key for r in report.unprovided_consumes}
    stale_exemptions = EXTERNAL_PROVIDERS - unprovided_keys
    assert not stale_exemptions, (
        f"EXTERNAL_PROVIDERS contains keys now provided by bundled templates: "
        f"{sorted(stale_exemptions)}. Remove them from the allow-list."
    )
