"""Agent-groundable manifest of the chirp-ui component surface.

This module publishes the component registry (``chirp_ui.components.COMPONENTS``
plus ``chirp_ui.tokens.TOKEN_CATALOG``) as a stable JSON snapshot. AI agents
and docs tooling can read the manifest to cite real classes, tokens, slots,
and templates instead of plausible-sounding ones.

Schema
------
``{"schema": "chirpui-manifest@1", "version": "<pkg>", "components": {...},
 "tokens": {...}, "stats": {...}}``

* ``components`` keys sorted; each entry contains ``block``, ``variants``,
  ``sizes``, ``modifiers``, ``elements``, ``slots``, ``tokens``, ``extra_emits``,
  ``emits``, ``template``, ``category``.
* ``tokens`` keys sorted; each entry is ``{"category": …, "scope": …}``.
* ``stats`` aggregates counts.

Deterministic: two calls to :func:`build_manifest` yield byte-identical JSON.

CLI
---
``python -m chirp_ui.manifest --json`` writes JSON to stdout.

See ``docs/PLAN-css-scope-and-layer.md § Sprint 7``.
"""

import argparse
import json
import sys
from typing import Any

from chirp_ui import __version__
from chirp_ui.components import COMPONENTS
from chirp_ui.tokens import TOKEN_CATALOG

SCHEMA = "chirpui-manifest@1"


def build_manifest() -> dict[str, Any]:
    """Return the component/token manifest as a JSON-serializable dict.

    Output is deterministic: components and tokens are sorted by key, and
    every per-entry list (emits, variants, etc.) is sorted. Callers can
    ``json.dumps(build_manifest(), indent=2, sort_keys=True)`` with confidence.
    """
    components: dict[str, dict[str, Any]] = {}
    for name in sorted(COMPONENTS):
        desc = COMPONENTS[name]
        components[name] = {
            "block": desc.block,
            "variants": sorted(desc.variants),
            "sizes": sorted(desc.sizes),
            "modifiers": sorted(desc.modifiers),
            "elements": sorted(desc.elements),
            "slots": sorted(desc.slots),
            "tokens": sorted(desc.tokens),
            "extra_emits": sorted(desc.extra_emits),
            "emits": sorted(desc.emits),
            "template": desc.template,
            "category": desc.category,
        }

    tokens: dict[str, dict[str, str]] = {
        name: {"category": TOKEN_CATALOG[name].category, "scope": TOKEN_CATALOG[name].scope}
        for name in sorted(TOKEN_CATALOG)
    }

    component_categories: dict[str, int] = {}
    for desc in COMPONENTS.values():
        cat = desc.category or "uncategorized"
        component_categories[cat] = component_categories.get(cat, 0) + 1
    token_categories: dict[str, int] = {}
    for t in TOKEN_CATALOG.values():
        token_categories[t.category] = token_categories.get(t.category, 0) + 1

    return {
        "schema": SCHEMA,
        "version": __version__,
        "components": components,
        "tokens": tokens,
        "stats": {
            "total_components": len(COMPONENTS),
            "total_tokens": len(TOKEN_CATALOG),
            "component_categories": dict(sorted(component_categories.items())),
            "token_categories": dict(sorted(token_categories.items())),
        },
    }


def to_json(manifest: dict[str, Any], *, indent: int = 2) -> str:
    """Serialize a manifest to stable JSON (sort_keys, UTF-8, no trailing NL)."""
    return json.dumps(manifest, indent=indent, sort_keys=True, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m chirp_ui.manifest",
        description="Emit the chirp-ui component manifest as JSON.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON (default).")
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent level (default: 2; use 0 for compact).",
    )
    args = parser.parse_args(argv)

    # --json is the only emitter today; flag kept so future --md is additive.
    _ = args.json

    indent = args.indent if args.indent > 0 else None
    sys.stdout.write(to_json(build_manifest(), indent=indent or 0))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
