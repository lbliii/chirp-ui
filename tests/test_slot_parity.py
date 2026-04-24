"""Slot parity — descriptor.slots vs. extracted public macro slots.

Sprint 2 of the agent-grounding-depth epic auto-extracts ``{% slot %}`` tags
from each macro body and emits them in the manifest as ``slots_extracted``.
Composite wrappers also expose caller-provided slots via ``{% yield %}``,
emitted separately as ``slots_yielded``.
The manifest's ``slots`` field is the *union* of descriptor + extracted, so
the agent-facing surface never under-reports a real slot.

This test guards against three rot patterns:

1. **Union invariant** — ``slots ⊇ slots_extracted`` always (drop coverage of
   a slot that the template actually exposes is never OK).
2. **Drift baseline** — ``KNOWN_DRIFT`` freezes the components whose
   descriptor and template currently disagree. A new disagreement fails CI;
   resolving an old one (rebalancing the descriptor) also fails CI, forcing
   removal from the allow-list. Same pattern as
   :data:`tests.test_provide_consume_audit.KNOWN_RESERVED`.
3. **Stale baseline** — every name in ``KNOWN_DRIFT`` must still actually
   drift; once a component is brought into parity, its name has to come out.

Backfill is opportunistic per ``AGENTS.md`` envelope-conversion convention —
PRs touching a drifting component should rebalance the descriptor in the same
PR, then drop the entry from this list.
"""

from __future__ import annotations

from chirp_ui._macro_introspect import macros_in_template
from chirp_ui.components import COMPONENTS

# Components whose ``descriptor.slots`` does not match the AST-extracted set.
# Frozen on 2026-04-20 at the start of Sprint 2; shrinks as descriptors and
# templates are reconciled. Never grows without an explicit PR.
KNOWN_DRIFT: frozenset[str] = frozenset(
    {
        "action-bar",
        "action-strip",
        "alert",
        "ascii-border",
        "ascii-card",
        "ascii-empty",
        "ascii-error",
        "ascii-modal",
        "ascii-radio-group",
        "ascii-table",
        "ascii-tabs",
        "aurora",
        "avatar-stack",
        "badge",
        "border-beam",
        "btn",
        "channel-card",
        "collapse",
        "command-palette",
        "constellation",
        "description_list",
        "entity-header",
        "feature-stack",
        "fieldset",
        "filter-group",
        "form-actions",
        "glow-card",
        "grain",
        "hero",
        "holy-light",
        "infinite-scroll",
        "install-snippet",
        "message-thread",
        "message_bubble",
        "meteor",
        "metric-grid",
        "nav-tree",
        "navbar-dropdown",
        "notification-dot",
        "orbit",
        "page_hero",
        "particle-bg",
        "profile-header",
        "resource-index",
        "reveal-on-scroll",
        "rune-field",
        "scanline",
        "selection-bar",
        "site-header",
        "sparkle",
        "spotlight-card",
        "streaming_bubble",
        "surface",
        "suspense-slot",
        "symbol-rain",
        "tooltip",
        "wizard-form",
        "wobble",
    }
)


def _drift_set() -> set[str]:
    """Return names whose descriptor.slots differ from direct plus yielded slots."""
    drifting: set[str] = set()
    for name in sorted(COMPONENTS):
        desc = COMPONENTS[name]
        if not desc.template:
            continue
        macros = macros_in_template(desc.template)
        target = desc.macro or desc.block.replace("-", "_")
        info = macros.get(target)
        if info is None:
            continue
        forwarded_slots = {forward.slot for forward in desc.slot_forwards}
        public_slots = set(info.slots) | set(info.yielded_slots) | forwarded_slots
        if set(desc.slots) != public_slots:
            drifting.add(name)
    return drifting


def test_manifest_slots_superset_of_extracted() -> None:
    """``manifest.slots`` must always contain every AST-extracted slot.

    This is the load-bearing invariant: even when the descriptor disagrees,
    agents reading the manifest see *all* slots a macro accepts.
    """
    from chirp_ui.manifest import build_manifest

    m = build_manifest()
    underreports: list[str] = []
    for name, entry in m["components"].items():
        slots = set(entry["slots"])
        extracted = set(entry["slots_extracted"])
        if not extracted.issubset(slots):
            missing = sorted(extracted - slots)
            underreports.append(f"{name}: missing {missing}")
    assert not underreports, "manifest.slots under-reports extracted slots:\n" + "\n".join(
        underreports
    )


def test_no_unexpected_new_drift() -> None:
    """A new drift case (descriptor and template disagree) fails CI.

    Rebalance the descriptor in the same PR that introduced the divergence
    (or, if the new slots are intentional, add the component to KNOWN_DRIFT
    with a comment explaining why).
    """
    new_drift = sorted(_drift_set() - KNOWN_DRIFT)
    assert not new_drift, (
        "new slot drift detected (descriptor.slots ≠ template slots): "
        f"{new_drift}\nrebalance descriptor.slots= or add to KNOWN_DRIFT."
    )


def test_known_drift_still_drifts() -> None:
    """Stale exemptions: KNOWN_DRIFT entries must still actually disagree.

    Catches the case where a contributor reconciles a descriptor but forgets
    to remove the name from KNOWN_DRIFT, masking future regressions.
    """
    stale = sorted(KNOWN_DRIFT - _drift_set())
    assert not stale, (
        f"KNOWN_DRIFT contains components no longer drifting: {stale}\n"
        f"remove them from the allow-list."
    )
