"""AST introspection for ``{% def %}`` macros — internal.

Wraps :mod:`kida.lexer` + :mod:`kida.parser` to extract per-macro parameter
metadata without compiling the template (so no chirp-ui filter stubs are
required at manifest-build time).

Used by :mod:`chirp_ui.manifest` to project macro Python signatures into the
agent-groundable manifest. See ``docs/PLAN-agent-grounding-depth.md`` and
``docs/DESIGN-manifest-signature-extraction.md``.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from kida.lexer import Lexer
from kida.nodes import Def, Node, Slot
from kida.parser import Parser

_TEMPLATES_DIR = Path(__file__).parent / "templates" / "chirpui"

# Leading ``{#- chirp-ui: ... -#}`` or ``{# chirp-ui: ... #}`` doc-block.
# Both the opener-dash and closer-dash are optional (kida whitespace-trim
# markers) so authors can pick either style. The first group captures
# everything between the marker and the closer.
_DOCBLOCK_RE = re.compile(
    r"\{#-?\s*chirp-ui:\s*(.*?)\s*-?#\}",
    re.DOTALL,
)
_YIELD_RE = re.compile(r"\{%-?\s*yield(?:\s+([a-zA-Z_][a-zA-Z0-9_]*))?\s*-?%\}")


@dataclass(frozen=True, slots=True)
class ParamInfo:
    """Single ``{% def %}`` parameter, derived from the AST.

    ``has_default`` follows Python's trailing-defaults convention: kida's
    ``Def`` node parallels ``defaults`` to the last *N* of ``params``.
    """

    name: str
    has_default: bool

    @property
    def is_required(self) -> bool:
        return not self.has_default


@dataclass(frozen=True, slots=True)
class MacroInfo:
    """Per-macro introspection result.

    ``slots`` is the tuple of ``{% slot name %}`` placeholders found in the
    macro body, in declaration order, deduplicated (a slot rendered twice
    appears once). The unnamed default slot is normalized from kida's
    ``"default"`` to ``""`` to match ``ComponentDescriptor.slots`` convention.
    ``yielded_slots`` is the tuple of ``{% yield %}`` / ``{% yield name %}``
    caller slots accepted by composite macros and forwarded into child calls.
    """

    name: str
    template: str
    lineno: int
    params: tuple[ParamInfo, ...]
    slots: tuple[str, ...]
    yielded_slots: tuple[str, ...]


@cache
def macros_in_template(template_name: str) -> dict[str, MacroInfo]:
    """Return ``{macro_name: MacroInfo}`` for every ``{% def %}`` in the template.

    Cached. Returns ``{}`` if the template file is missing or contains no defs.
    Template name is relative to ``src/chirp_ui/templates/chirpui/``.
    """
    path = _TEMPLATES_DIR / template_name
    if not path.is_file():
        return {}
    source = path.read_text(encoding="utf-8")
    tokens = list(Lexer(source).tokenize())
    ast = Parser(tokens, name=f"chirpui/{template_name}", source=source).parse()
    defs = list(_walk_defs(ast))
    yielded_slots = _yielded_slots_by_macro(source, defs)
    return {d.name: _to_macro_info(d, template_name, yielded_slots.get(d.name, ())) for d in defs}


def _to_macro_info(node: Def, template: str, yielded_slots: tuple[str, ...]) -> MacroInfo:
    n_required = len(node.params) - len(node.defaults)
    params = tuple(
        ParamInfo(name=p.name, has_default=i >= n_required) for i, p in enumerate(node.params)
    )
    seen: set[str] = set()
    slots: list[str] = []
    for name in _walk_slot_names(node):
        if name not in seen:
            seen.add(name)
            slots.append(name)
    return MacroInfo(
        name=node.name,
        template=template,
        lineno=node.lineno,
        params=params,
        slots=tuple(slots),
        yielded_slots=yielded_slots,
    )


def _walk_defs(node: Node) -> Iterator[Def]:
    if isinstance(node, Def):
        yield node
    body = getattr(node, "body", None)
    if body:
        for child in body:
            yield from _walk_defs(child)


def _walk_slot_names(node: Node) -> Iterator[str]:
    """Yield public slot names reachable from ``node`` without crossing a nested ``Def``.

    chirp-ui currently has no nested defs (verified at Sprint 2), so this is
    defensive only — keeps slot ownership per-macro if that ever changes.
    """
    if isinstance(node, Slot):
        yield "" if node.name == "default" else node.name
    body = getattr(node, "body", None)
    if body:
        for child in body:
            if isinstance(child, Def):
                continue
            yield from _walk_slot_names(child)
    else_body = getattr(node, "else_", None)
    if else_body:
        for child in else_body:
            if isinstance(child, Def):
                continue
            yield from _walk_slot_names(child)
    elif_bodies = getattr(node, "elif_", None)
    if elif_bodies:
        for _, elif_body in elif_bodies:
            for child in elif_body:
                if isinstance(child, Def):
                    continue
                yield from _walk_slot_names(child)


def _yielded_slots_by_macro(source: str, defs: list[Def]) -> dict[str, tuple[str, ...]]:
    """Return ``macro_name → yielded slot names`` attributed by source line.

    The installed kida AST exposes ``Slot`` placeholders but not a public
    ``Yield`` node, so composite forwarded slots are found from the raw source
    and attributed to the nearest preceding ``{% def %}`` line. chirp-ui does
    not use nested defs, which keeps the ownership rule straightforward.
    """
    if not defs:
        return {}
    sorted_defs = sorted(defs, key=lambda d: d.lineno)
    found: dict[str, list[str]] = {d.name: [] for d in sorted_defs}
    seen: dict[str, set[str]] = {d.name: set() for d in sorted_defs}
    current_index = -1
    for lineno, line in enumerate(source.splitlines(), start=1):
        while (
            current_index + 1 < len(sorted_defs) and sorted_defs[current_index + 1].lineno <= lineno
        ):
            current_index += 1
        if current_index < 0:
            continue
        owner = sorted_defs[current_index].name
        for match in _YIELD_RE.finditer(line):
            name = match.group(1) or ""
            if name not in seen[owner]:
                seen[owner].add(name)
                found[owner].append(name)
    return {name: tuple(slots) for name, slots in found.items() if slots}


@cache
def description_from_template(template_name: str) -> str:
    """Return the leading ``{#- chirp-ui: ... -#}`` doc-block text, or ``""``.

    One doc-block per file, covering the file's entire set of macros — verified
    at Sprint 4 across all 195 chirp-ui templates. The block must appear before
    any ``{% def %}`` or ``{% from %}`` statement (the parser scans only the
    first ~2 KB to honor that invariant cheaply).

    Whitespace inside the block is preserved except for a single leading /
    trailing strip — so multi-line usage examples keep their shape. Inner
    indentation is left alone; downstream renderers (COMPONENT-OPTIONS
    generator, etc.) can post-process as needed.
    """
    path = _TEMPLATES_DIR / template_name
    if not path.is_file():
        return ""
    # Only scan the file prologue; doc-blocks must precede the first def.
    prologue = path.read_text(encoding="utf-8")[:4096]
    match = _DOCBLOCK_RE.search(prologue)
    if not match:
        return ""
    return match.group(1).strip()
