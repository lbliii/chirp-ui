"""Agent-groundable manifest of the chirp-ui component surface.

This module publishes the component registry (``chirp_ui.components.COMPONENTS``
plus ``chirp_ui.tokens.TOKEN_CATALOG``) as a stable JSON snapshot. AI agents
and docs tooling can read the manifest to cite real classes, tokens, slots,
and templates instead of plausible-sounding ones.

Schema
------
``{"schema": "chirpui-manifest@2", "version": "<pkg>", "components": {...},
 "tokens": {...}, "stats": {...}}``

* ``components`` keys sorted; each entry contains ``block``, ``variants``,
  ``sizes``, ``modifiers``, ``elements``, ``slots``, ``tokens``, ``extra_emits``,
  ``emits``, ``template``, ``category``, ``maturity``, ``role``, ``requires``,
  plus the ``@2`` additions ``macro``, ``params``, and ``lineno``.
* ``params`` is a list of ``{"name": str, "has_default": bool,
  "is_required": bool}`` derived from the template AST via
  :mod:`chirp_ui._macro_introspect`. Empty when the descriptor has no
  template, the macro cannot be resolved, or the template has no
  ``{% def %}`` matching the resolved name.
* ``macro`` is the resolved macro identifier (``descriptor.macro`` if set,
  else ``block.replace("-", "_")``). ``null`` when the descriptor has no
  template or no matching macro is found.
* ``lineno`` is the source line of the ``{% def %}`` tag (``0`` when
  unavailable).
* ``slots`` is the sorted union of ``descriptor.slots`` and slots
  extracted from the macro body. The unnamed default slot is represented
  as ``""``. Hand-authored descriptor entries can over-declare (e.g. for
  documentation), but the manifest never under-reports a real slot.
* ``slots_extracted`` is the AST-derived slot list (sorted, default = ``""``)
  exposed separately so parity tests can spot descriptor↔template drift
  without losing the merged ``slots`` contract.
* ``provides`` / ``consumes`` are sorted lists of context keys (e.g.
  ``"_card_variant"``) sourced from :mod:`chirp_ui.inspect`. A key is
  attributed to the macro whose ``{% def %}`` lineno is the largest one
  preceding the ``{% provide %}`` / ``consume()`` site.
* ``description`` is the stripped text inside the leading
  ``{#- chirp-ui: ... -#}`` doc-block of the template file. One block per
  file, covering every macro; empty string when the descriptor has no
  template. New chirp-ui templates must carry a doc-block
  (``tests/test_description_coverage.py``).
* ``tokens`` keys sorted; each entry is ``{"category": …, "scope": …}``.
* ``stats`` aggregates counts, including ``components_with_params``, a
  ``registry_debt`` scorecard for descriptor/CSS reconciliation burn-down,
  and a ``manifest_quality`` scorecard for agent-facing metadata coverage.

Deterministic: two calls to :func:`build_manifest` yield byte-identical JSON.

CLI
---
``python -m chirp_ui.manifest --json`` writes JSON to stdout.

See ``docs/PLAN-agent-grounding-depth.md`` and
``docs/DESIGN-manifest-signature-extraction.md``.
"""

import argparse
import json
import re
import sys
from typing import Any

from chirp_ui import __version__
from chirp_ui._macro_introspect import (
    _TEMPLATES_DIR,
    MacroInfo,
    description_from_template,
    macros_in_template,
)
from chirp_ui.alpine import ALPINE_REQUIRED_COMPONENTS
from chirp_ui.components import _AUTO_EXTRAS, _AUTO_TRIMS, COMPONENTS, ComponentDescriptor
from chirp_ui.inspect import list_consumes, list_provides
from chirp_ui.tokens import TOKEN_CATALOG

SCHEMA = "chirpui-manifest@2"

_ALPINE_MACROS = frozenset(
    macro for requirement in ALPINE_REQUIRED_COMPONENTS.values() for macro in requirement.macros
)
_ALPINE_DIRECTIVE_RE = re.compile(
    r"""(?<![\w-])(?:x-data|x-show|x-ref|x-cloak|x-transition|x-on:|x-bind:|:aria-[\w-]+|:class|:id|@(?:click|keydown|keyup|submit|input|change|focus|blur|mouseenter|mouseleave)[\w:.-]*)\b"""
)
_HTMX_CONTRACT_RE = re.compile(r"""\b(?:hx-[\w:-]+|sse-[\w:-]+|hx_[A-Za-z]\w*)\b""")


def _resolve_macro(desc: ComponentDescriptor) -> MacroInfo | None:
    """Look up the ``MacroInfo`` for a descriptor, or ``None`` if unresolvable.

    Resolution order: explicit ``descriptor.macro`` → ``block.replace("-", "_")``.
    Returns ``None`` when the template is missing, the file has no defs, or
    no def name matches the resolved macro identifier.
    """
    if not desc.template:
        return None
    macros = macros_in_template(desc.template)
    if not macros:
        return None
    target = desc.macro or desc.block.replace("-", "_")
    return macros.get(target)


def _runtime_requirements(desc: ComponentDescriptor, macro_info: MacroInfo | None) -> list[str]:
    """Return sorted runtime requirements from descriptor + derived macro metadata."""
    requires = set(desc.requires)
    if macro_info is not None:
        macro_source = _macro_source(macro_info)
        if macro_info.name in _ALPINE_MACROS or _ALPINE_DIRECTIVE_RE.search(macro_source):
            requires.add("alpine")
        if _HTMX_CONTRACT_RE.search(macro_source):
            requires.add("htmx")
    return sorted(requires)


def _macro_source(macro_info: MacroInfo) -> str:
    """Return the source slice for one macro body, bounded by the next ``{% def %}``."""
    path = _TEMPLATES_DIR / macro_info.template
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    macros = sorted(macros_in_template(macro_info.template).values(), key=lambda info: info.lineno)
    following = [info.lineno for info in macros if info.lineno > macro_info.lineno]
    end_line = min(following) - 1 if following else len(lines)
    return "\n".join(lines[macro_info.lineno - 1 : end_line])


def _manifest_quality(components: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Return agent-facing metadata gap counts for public templated components."""
    public_templated = [
        name
        for name, entry in components.items()
        if entry["template"] and entry["maturity"] != "internal"
    ]
    return {
        "public_templated_components": len(public_templated),
        "missing_macro": sum(1 for name in public_templated if not components[name]["macro"]),
        "missing_maturity": sum(1 for name in public_templated if not components[name]["maturity"]),
        "missing_role": sum(1 for name in public_templated if not components[name]["role"]),
        "missing_description": sum(
            1 for name in public_templated if not components[name]["description"]
        ),
        "missing_slot_metadata": sum(
            1
            for name in public_templated
            if not isinstance(components[name]["slots"], list)
            or not isinstance(components[name]["slots_extracted"], list)
        ),
    }


def _owning_macro(macros: dict[str, MacroInfo], line: int) -> str | None:
    """Return the macro name whose ``{% def %}`` lineno most-recently precedes ``line``.

    Used to attribute a ``{% provide %}`` or ``consume()`` site (which has only
    a template + line) to the macro it lives inside. Returns ``None`` if the
    line is before any def (top-of-file noise).
    """
    candidates = [info for info in macros.values() if info.lineno <= line]
    if not candidates:
        return None
    return max(candidates, key=lambda info: info.lineno).name


def _provide_consume_index() -> dict[tuple[str, str], tuple[set[str], set[str]]]:
    """Index ``(template, macro_name) → (provides_keys, consumes_keys)``.

    Built once per manifest; relies on the line-walked records from
    :mod:`chirp_ui.inspect`. Templates with no defs (or sites before the
    first def) are dropped silently.
    """
    index: dict[tuple[str, str], tuple[set[str], set[str]]] = {}
    for record in list_provides():
        macros = macros_in_template(record.template)
        if not macros:
            continue
        owner = _owning_macro(macros, record.line)
        if owner is None:
            continue
        provides, consumes = index.setdefault((record.template, owner), (set(), set()))
        provides.add(record.key)
    for record in list_consumes():
        macros = macros_in_template(record.template)
        if not macros:
            continue
        owner = _owning_macro(macros, record.line)
        if owner is None:
            continue
        provides, consumes = index.setdefault((record.template, owner), (set(), set()))
        consumes.add(record.key)
    return index


def build_manifest() -> dict[str, Any]:
    """Return the component/token manifest as a JSON-serializable dict.

    Output is deterministic: components and tokens are sorted by key, and
    every per-entry list (emits, variants, etc.) is sorted. Param order is
    preserved as declared in the template (positional order matters for
    macro callers).
    """
    pc_index = _provide_consume_index()
    components: dict[str, dict[str, Any]] = {}
    components_with_params = 0
    components_with_provides = 0
    components_with_consumes = 0
    components_with_description = 0
    for name in sorted(COMPONENTS):
        desc = COMPONENTS[name]
        macro_info = _resolve_macro(desc)
        params: list[dict[str, Any]] = []
        slots_extracted: list[str] = []
        provides: list[str] = []
        consumes: list[str] = []
        description = description_from_template(desc.template) if desc.template else ""
        if description:
            components_with_description += 1
        if macro_info is not None:
            components_with_params += 1
            params = [
                {"name": p.name, "has_default": p.has_default, "is_required": p.is_required}
                for p in macro_info.params
            ]
            slots_extracted = sorted(macro_info.slots)
            pc_provides, pc_consumes = pc_index.get(
                (macro_info.template, macro_info.name), (set(), set())
            )
            provides = sorted(pc_provides)
            consumes = sorted(pc_consumes)
            if provides:
                components_with_provides += 1
            if consumes:
                components_with_consumes += 1
        slots_union = sorted(set(desc.slots) | set(slots_extracted))
        requires = _runtime_requirements(desc, macro_info)
        components[name] = {
            "block": desc.block,
            "variants": sorted(desc.variants),
            "sizes": sorted(desc.sizes),
            "modifiers": sorted(desc.modifiers),
            "elements": sorted(desc.elements),
            "slots": slots_union,
            "slots_extracted": slots_extracted,
            "tokens": sorted(desc.tokens),
            "extra_emits": sorted(desc.extra_emits),
            "emits": sorted(desc.emits),
            "template": desc.template,
            "category": desc.category,
            "maturity": desc.resolved_maturity,
            "role": desc.resolved_role,
            "requires": requires,
            "macro": macro_info.name if macro_info else None,
            "params": params,
            "lineno": macro_info.lineno if macro_info else 0,
            "provides": provides,
            "consumes": consumes,
            "description": description,
        }

    tokens: dict[str, dict[str, str]] = {
        name: {"category": TOKEN_CATALOG[name].category, "scope": TOKEN_CATALOG[name].scope}
        for name in sorted(TOKEN_CATALOG)
    }

    component_categories: dict[str, int] = {}
    component_maturity: dict[str, int] = {}
    component_roles: dict[str, int] = {}
    component_requirements: dict[str, int] = {}
    for name, desc in COMPONENTS.items():
        cat = desc.category or "uncategorized"
        component_categories[cat] = component_categories.get(cat, 0) + 1
        maturity = desc.resolved_maturity
        component_maturity[maturity] = component_maturity.get(maturity, 0) + 1
        role = desc.resolved_role
        component_roles[role] = component_roles.get(role, 0) + 1
        for requirement in components[name]["requires"]:
            component_requirements[requirement] = component_requirements.get(requirement, 0) + 1
    registry_debt = {
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
            "components_with_params": components_with_params,
            "components_with_provides": components_with_provides,
            "components_with_consumes": components_with_consumes,
            "components_with_description": components_with_description,
            "total_tokens": len(TOKEN_CATALOG),
            "registry_debt": registry_debt,
            "manifest_quality": _manifest_quality(components),
            "component_categories": dict(sorted(component_categories.items())),
            "component_maturity": dict(sorted(component_maturity.items())),
            "component_roles": dict(sorted(component_roles.items())),
            "component_requirements": dict(sorted(component_requirements.items())),
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
