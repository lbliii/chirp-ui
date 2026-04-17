"""Design system introspection — dump the chirp-ui API surface.

Usage::

    python -m chirp_ui.inspect              # JSON report
    python -m chirp_ui.inspect --summary    # compact table
    python -m chirp_ui.inspect --tokens     # token catalog only
    python -m chirp_ui.inspect --components # component descriptors only
    python -m chirp_ui.inspect --provides   # {% provide %} statements + annotations
    python -m chirp_ui.inspect --consumes   # consume() calls + annotations
    python -m chirp_ui.inspect --audit-context  # dead provides, unprovided consumes, annotation drift
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from chirp_ui.components import COMPONENTS, design_system_report
from chirp_ui.tokens import TOKEN_CATALOG

_TEMPLATES_DIR = Path(__file__).parent / "templates" / "chirpui"

# {% provide _key = expr %}
_PROVIDE_RE = re.compile(r"\{%\s*provide\s+(_\w+)\s*=")

# {# @provides _key — consumed by: btn, icon_btn #}
# {# @provides _key — no consumers yet (reserved for future use) #}
_PROVIDE_ANNOT_RE = re.compile(
    r"\{#\s*@provides\s+(_\w+)\s*[—\-]\s*(.+?)\s*#\}",
)

# consume("_key", default) or consume("_key")
_CONSUME_RE = re.compile(r'consume\(\s*"(_\w+)"(?:\s*,\s*([^)]*))?\s*\)')

# {# @consumes _key from: providers — falls back to default #}
# Compound form: {# @consumes _k1 from: p1, _k2 from: p2, p3 — falls back to default #}
_CONSUMES_ANNOT_RE = re.compile(
    r"\{#\s*@consumes\s+(.+?)\s*[—\-]\s*falls back to\s+(.+?)\s*#\}",
)

# {% def macro_name(...) %}
_MACRO_DEF_RE = re.compile(r"^\{%\s*def\s+(\w+)")

# Split compound annotation on `, _key from:` boundary (comma after a word,
# before an underscore-prefixed key); keeps multi-word provider lists intact.
_CONSUMES_SPLIT_RE = re.compile(r"(?<=\w),\s+(?=_\w+\s+from:)")
_CONSUMES_CLAUSE_RE = re.compile(r"^(_\w+)\s+from:\s*(.+)$")


@dataclass(frozen=True)
class ProvideRecord:
    """A `{% provide _key = ... %}` statement found in a chirp-ui template."""

    key: str
    template: str
    line: int
    consumed_by: tuple[str, ...]
    raw_annotation: str


@dataclass(frozen=True)
class ConsumeRecord:
    """A `consume("_key", default)` call found in a chirp-ui template."""

    key: str
    template: str
    line: int
    providers: tuple[str, ...]
    fallback: str
    raw_annotation: str


@dataclass(frozen=True)
class AuditReport:
    """Result of :func:`audit_provide_consume` — context-flow health at a glance.

    - ``dead_provides`` — `{% provide %}` statements whose key is never
      ``consume()``d anywhere in the bundled templates. Some are legitimate
      (reserved for apps to extend); apps should pin an allow-list.
    - ``unprovided_consumes`` — ``consume()`` calls whose key is never
      ``{% provide %}``d in the bundled templates. Usually means the value is
      expected to come from app code (see ``_sse_state``).
    - ``annotation_drift`` — human-readable diagnostics where a ``@provides``
      annotation names a consumer macro that lacks a matching ``@consumes``
      annotation for the same key. Flags rotted documentation.
    """

    dead_provides: tuple[ProvideRecord, ...]
    unprovided_consumes: tuple[ConsumeRecord, ...]
    annotation_drift: tuple[str, ...]


def _parse_provide_annotation(body: str) -> tuple[str, ...]:
    """Parse the body of a `@provides` annotation into a tuple of consumer macro names."""
    body = body.strip()
    if "no consumers yet" in body:
        return ()
    if body.startswith("consumed by:"):
        body = body[len("consumed by:") :].strip()
    return tuple(item.strip() for item in body.split(",") if item.strip())


def _parse_consumes_annotation(inner: str) -> list[tuple[str, tuple[str, ...]]]:
    """Parse one or more `_key from: providers` clauses inside a `@consumes` annotation.

    Handles compound annotations like:
        _card_variant from: card, _surface_variant from: panel, surface
    by splitting only at boundaries between distinct keys.
    """
    parts = _CONSUMES_SPLIT_RE.split(inner.strip())
    results: list[tuple[str, tuple[str, ...]]] = []
    for part in parts:
        match = _CONSUMES_CLAUSE_RE.match(part.strip())
        if not match:
            continue
        key, providers = match.group(1), match.group(2).strip()
        provider_tuple = tuple(p.strip() for p in providers.split(",") if p.strip())
        results.append((key, provider_tuple))
    return results


def _strip_default(raw: str) -> str:
    """Normalize a consume() default literal: strip quotes/whitespace."""
    text = raw.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ('"', "'"):
        return text[1:-1]
    return text


def _parse_template(
    template_name: str, text: str
) -> tuple[list[ProvideRecord], list[ConsumeRecord]]:
    provides: list[ProvideRecord] = []
    consumes: list[ConsumeRecord] = []

    pending_provides: dict[str, tuple[tuple[str, ...], str]] = {}
    pending_consumes: dict[str, tuple[tuple[str, ...], str, str]] = {}

    for line_no, line in enumerate(text.splitlines(), 1):
        annot = _PROVIDE_ANNOT_RE.search(line)
        if annot:
            key = annot.group(1)
            consumed_by = _parse_provide_annotation(annot.group(2))
            pending_provides[key] = (consumed_by, line.strip())
            continue

        annot = _CONSUMES_ANNOT_RE.search(line)
        if annot:
            inner, fallback = annot.group(1), annot.group(2).strip()
            for key, providers in _parse_consumes_annotation(inner):
                pending_consumes[key] = (providers, fallback, line.strip())
            continue

        provide_match = _PROVIDE_RE.search(line)
        if provide_match:
            key = provide_match.group(1)
            consumed_by, raw = pending_provides.pop(key, ((), ""))
            provides.append(
                ProvideRecord(
                    key=key,
                    template=template_name,
                    line=line_no,
                    consumed_by=consumed_by,
                    raw_annotation=raw,
                )
            )

        for consume_match in _CONSUME_RE.finditer(line):
            key = consume_match.group(1)
            inline_default = _strip_default(consume_match.group(2) or "")
            providers, fallback, raw = pending_consumes.pop(key, ((), inline_default, ""))
            consumes.append(
                ConsumeRecord(
                    key=key,
                    template=template_name,
                    line=line_no,
                    providers=providers,
                    fallback=fallback,
                    raw_annotation=raw,
                )
            )

    return provides, consumes


def _list_template_files() -> list[Path]:
    return sorted(p for p in _TEMPLATES_DIR.iterdir() if p.suffix == ".html")


def list_provides() -> list[ProvideRecord]:
    """Walk every chirp-ui template and return each `{% provide %}` statement.

    Statements adjacent to a `{# @provides _key — consumed by: ... #}` annotation
    have their ``consumed_by`` populated and ``raw_annotation`` set; statements
    without an annotation have empty defaults so callers can detect undocumented
    providers.
    """
    records: list[ProvideRecord] = []
    for path in _list_template_files():
        provides, _ = _parse_template(path.name, path.read_text())
        records.extend(provides)
    return sorted(records, key=lambda r: (r.template, r.line))


def list_consumes() -> list[ConsumeRecord]:
    """Walk every chirp-ui template and return each `consume(...)` call.

    Calls adjacent to a `{# @consumes _key from: ... — falls back to ... #}`
    annotation have their ``providers``, ``fallback``, and ``raw_annotation``
    populated; calls without an annotation fall back to the inline default
    literal (or ``""`` if none).
    """
    records: list[ConsumeRecord] = []
    for path in _list_template_files():
        _, consumes = _parse_template(path.name, path.read_text())
        records.extend(consumes)
    return sorted(records, key=lambda r: (r.template, r.line))


def _macro_to_template_map() -> dict[str, tuple[str, ...]]:
    """Index every `{% def macro_name %}` to the template file(s) it's defined in.

    Most macros have one definition; a few share names across files (e.g.
    ``segmented_control`` lives in both ``forms.html`` and
    ``segmented_control.html``). Returning a tuple keeps the drift check
    tolerant of these overlaps.
    """
    index: dict[str, list[str]] = {}
    for path in _list_template_files():
        for line in path.read_text().splitlines():
            match = _MACRO_DEF_RE.match(line)
            if match:
                index.setdefault(match.group(1), []).append(path.name)
    return {name: tuple(templates) for name, templates in index.items()}


def audit_provide_consume() -> AuditReport:
    """Audit chirp-ui's provide/consume graph against the templates.

    Returns an :class:`AuditReport` with three diagnostics: dead provides
    (provided but never consumed), unprovided consumes (consumed but never
    provided in bundled templates — usually an app-side provider is expected),
    and annotation drift (``@provides`` lists a consumer that has no matching
    ``@consumes`` for the same key).
    """
    provides = list_provides()
    consumes = list_consumes()

    provided_keys = {r.key for r in provides}
    consumed_keys = {r.key for r in consumes}

    dead = tuple(r for r in provides if r.key not in consumed_keys)
    unprovided = tuple(r for r in consumes if r.key not in provided_keys)

    macro_to_template = _macro_to_template_map()
    consumes_by_template: dict[str, set[str]] = {}
    for r in consumes:
        consumes_by_template.setdefault(r.template, set()).add(r.key)

    drift: list[str] = []
    for provide in provides:
        for consumer_name in provide.consumed_by:
            templates = macro_to_template.get(consumer_name)
            if not templates:
                drift.append(
                    f"{provide.template}:{provide.line} @provides {provide.key}: "
                    f"consumer {consumer_name!r} has no matching macro def "
                    f"(typo or renamed?)"
                )
                continue
            if not any(provide.key in consumes_by_template.get(t, set()) for t in templates):
                drift.append(
                    f"{provide.template}:{provide.line} @provides {provide.key}: "
                    f"consumer {consumer_name!r} (in {', '.join(templates)}) "
                    f"has no @consumes annotation for {provide.key}"
                )

    return AuditReport(
        dead_provides=dead,
        unprovided_consumes=unprovided,
        annotation_drift=tuple(drift),
    )


def _print_summary() -> None:
    report = design_system_report()
    stats = report["stats"]
    print("chirp-ui design system surface")
    print("=" * 40)
    print(f"Components: {stats['total_components']}")
    print(f"Tokens:     {stats['total_tokens']}")
    print()
    print("Component categories:")
    for cat, count in sorted(stats["component_categories"].items()):
        print(f"  {cat:20s} {count:3d}")
    print()
    print("Token categories:")
    for cat, count in sorted(stats["token_categories"].items()):
        print(f"  {cat:20s} {count:3d}")


def _print_components() -> None:
    for name, desc in sorted(COMPONENTS.items()):
        parts = [f"  block: {desc.block}"]
        if desc.variants:
            parts.append(f"  variants: {', '.join(v or '(empty)' for v in desc.variants)}")
        if desc.sizes:
            parts.append(f"  sizes: {', '.join(s or '(empty)' for s in desc.sizes)}")
        if desc.modifiers:
            parts.append(f"  modifiers: {', '.join(desc.modifiers)}")
        if desc.elements:
            parts.append(f"  elements: {', '.join(desc.elements)}")
        if desc.slots:
            parts.append(f"  slots: {', '.join(s or '(default)' for s in desc.slots)}")
        if desc.tokens:
            parts.append(f"  tokens: {', '.join(desc.tokens)}")
        if desc.template:
            parts.append(f"  template: {desc.template}")
        if desc.category:
            parts.append(f"  category: {desc.category}")
        print(f"{name}:")
        print("\n".join(parts))
        print()


def _print_tokens() -> None:
    by_category: dict[str, list[str]] = {}
    for name, tdef in sorted(TOKEN_CATALOG.items()):
        by_category.setdefault(tdef.category, []).append(
            f"  {name}" + (f" [{tdef.scope}]" if tdef.scope != "global" else "")
        )
    for cat in sorted(by_category):
        print(f"{cat} ({len(by_category[cat])}):")
        for line in by_category[cat]:
            print(line)
        print()


def _print_provides() -> None:
    records = list_provides()
    print(f"chirp-ui provide statements ({len(records)} total)")
    print("=" * 60)
    for r in records:
        consumers = ", ".join(r.consumed_by) if r.consumed_by else "(none documented)"
        print(f"{r.key}")
        print(f"  template:    {r.template}:{r.line}")
        print(f"  consumed by: {consumers}")
        if not r.raw_annotation:
            print("  WARNING:     no @provides annotation found adjacent to this statement")
        print()


def _print_consumes() -> None:
    records = list_consumes()
    print(f"chirp-ui consume calls ({len(records)} total)")
    print("=" * 60)
    for r in records:
        providers = ", ".join(r.providers) if r.providers else "(none documented)"
        print(f"{r.key}")
        print(f"  template:      {r.template}:{r.line}")
        print(f"  providers:     {providers}")
        print(f"  falls back to: {r.fallback or '(empty)'}")
        if not r.raw_annotation:
            print("  WARNING:       no @consumes annotation found adjacent to this call")
        print()


def _print_audit() -> None:
    report = audit_provide_consume()
    print("chirp-ui provide/consume audit")
    print("=" * 60)
    print(f"Dead provides ({len(report.dead_provides)}):")
    if report.dead_provides:
        for r in report.dead_provides:
            print(f"  {r.template}:{r.line} {r.key}  (provided, never consumed)")
    else:
        print("  (none)")
    print()
    print(f"Unprovided consumes ({len(report.unprovided_consumes)}):")
    if report.unprovided_consumes:
        for r in report.unprovided_consumes:
            print(f"  {r.template}:{r.line} {r.key}  (consumed, never provided)")
    else:
        print("  (none)")
    print()
    print(f"Annotation drift ({len(report.annotation_drift)}):")
    if report.annotation_drift:
        for msg in report.annotation_drift:
            print(f"  {msg}")
    else:
        print("  (none)")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="chirp-ui-inspect",
        description="Inspect the chirp-ui design system surface.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--summary", action="store_true", help="compact summary table")
    group.add_argument("--components", action="store_true", help="component descriptors only")
    group.add_argument("--tokens", action="store_true", help="token catalog only")
    group.add_argument(
        "--provides", action="store_true", help="{% provide %} statements + annotations"
    )
    group.add_argument("--consumes", action="store_true", help="consume() calls + annotations")
    group.add_argument(
        "--audit-context",
        action="store_true",
        help="audit provide/consume graph for dead provides, orphans, and annotation drift",
    )
    group.add_argument("--json", action="store_true", help="full JSON report (default)")
    args = parser.parse_args(argv)

    if args.summary:
        _print_summary()
    elif args.components:
        _print_components()
    elif args.tokens:
        _print_tokens()
    elif args.provides:
        _print_provides()
    elif args.consumes:
        _print_consumes()
    elif args.audit_context:
        _print_audit()
    else:
        report = design_system_report()
        json.dump(report, sys.stdout, indent=2, default=str)
        print()


if __name__ == "__main__":
    main()
