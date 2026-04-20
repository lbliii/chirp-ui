"""Parity between ``docs/PROVIDE-CONSUME-KEYS.md`` and the runtime registry.

Sprint 2.3 of the agent-grounding-depth epic: the docs table must be a
*projection* of the manifest, not a parallel source. Drift in either
direction fails CI:

* A key in the docs table that no template provides or consumes →
  the doc is rotting (key was renamed/removed; doc not updated).
* A key in the templates that the docs table doesn't list →
  the doc is incomplete (new key added; doc not updated).

Mirrors :file:`tests/test_provide_consume_audit.py` — same allow-list pattern
for legitimate exemptions, but here we audit against documentation rather
than against the provide/consume graph itself.
"""

from __future__ import annotations

import re
from pathlib import Path

from chirp_ui.inspect import list_consumes, list_provides

_DOC_PATH = Path(__file__).parent.parent / "docs" / "PROVIDE-CONSUME-KEYS.md"

# The Key column in the registry table: `| `_key_name` | ... | ... |`
# Captures the underscore-prefixed identifier inside backticks.
_KEY_ROW_RE = re.compile(r"^\|\s*`(_\w+)`\s*\|")


def _documented_keys() -> set[str]:
    """Parse the Key column of the registry table in PROVIDE-CONSUME-KEYS.md."""
    keys: set[str] = set()
    for line in _DOC_PATH.read_text(encoding="utf-8").splitlines():
        match = _KEY_ROW_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def _live_keys() -> set[str]:
    """Every context key currently provided or consumed in the bundled templates."""
    return {r.key for r in list_provides()} | {r.key for r in list_consumes()}


def test_doc_lists_only_real_keys() -> None:
    """Every key documented in the table must appear in a real template.

    A documented-but-dead key means the doc rotted (typically: key got
    renamed/removed and the markdown wasn't updated).
    """
    documented = _documented_keys()
    live = _live_keys()
    rotted = sorted(documented - live)
    assert not rotted, (
        f"docs/PROVIDE-CONSUME-KEYS.md lists keys not in any template: {rotted}\n"
        f"either restore the provide/consume site or delete the row."
    )


def test_every_live_key_is_documented() -> None:
    """Every key in templates must appear in the registry table.

    A live-but-undocumented key means a new context key was added without
    updating the registry — agents can't ground on it.
    """
    documented = _documented_keys()
    live = _live_keys()
    undocumented = sorted(live - documented)
    assert not undocumented, (
        f"context keys missing from docs/PROVIDE-CONSUME-KEYS.md: {undocumented}\n"
        f"add a row to the Key Registry table."
    )


def test_doc_table_is_non_trivial() -> None:
    """Sanity: at least the canonical 12 keys (per docs at Sprint 2 freeze) are present.

    Catches accidental table corruption (e.g. table header shifted, regex broken).
    """
    documented = _documented_keys()
    assert len(documented) >= 10, f"only {len(documented)} keys parsed from docs — table broken?"
    # Spot-check a high-traffic key.
    assert "_card_variant" in documented
    assert "_surface_variant" in documented
