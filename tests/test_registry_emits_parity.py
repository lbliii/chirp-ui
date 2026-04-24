"""Bidirectional parity between ``ComponentDescriptor.emits`` and the CSS partials.

Every ``.chirpui-<ident>`` class name found in any authoring partial must be
declared by some descriptor's :attr:`~chirp_ui.components.ComponentDescriptor.emits`
set, and vice-versa.

The stylesheet is the projection of the registry. Drift in either direction is
a test failure — the printout tells the author which side to fix:

* **CSS → registry orphan.** A class in the CSS but not in any ``emits``. Either
  add it to the owning descriptor (as an element/variant/size/modifier or via
  ``extra_emits``), or delete the stale rule.
* **Registry → CSS orphan.** A class the registry promises but that no partial
  defines. Either add the CSS, or trim the descriptor.

See ``docs/PLAN-css-scope-and-layer.md § Sprint 4`` and
``docs/DESIGN-css-registry-projection.md § Decision 4``.
"""

import re
from pathlib import Path

from chirp_ui.components import _AUTO_TRIMS, COMPONENTS

REPO_ROOT = Path(__file__).resolve().parent.parent
PARTIALS_DIR = REPO_ROOT / "src" / "chirp_ui" / "templates" / "css" / "partials"

# Matches a class selector token: `.chirpui-<ident>` where <ident> is a BEM-ish
# run of word chars / hyphens / double-underscores. Stop at any selector
# terminator so we don't greedily swallow following selectors.
_CLASS_RE = re.compile(r"\.(chirpui-[A-Za-z0-9_-]+)")

# Strip CSS comments before scanning. Comments occasionally contain example
# selectors that aren't actually emitted by any component (e.g. documentation
# snippets inside rule-body comments).
_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def _classes_in_partial(text: str) -> set[str]:
    stripped = _COMMENT_RE.sub("", text)
    return set(_CLASS_RE.findall(stripped))


def _all_css_classes() -> tuple[set[str], dict[str, set[str]]]:
    """Return (union of classes, per-partial mapping) across every partial."""
    union: set[str] = set()
    per_partial: dict[str, set[str]] = {}
    for path in sorted(PARTIALS_DIR.glob("*.css")):
        classes = _classes_in_partial(path.read_text(encoding="utf-8"))
        per_partial[path.name] = classes
        union |= classes
    return union, per_partial


def _all_registry_emits() -> tuple[set[str], dict[str, set[str]]]:
    union: set[str] = set()
    per_block: dict[str, set[str]] = {}
    for name, desc in COMPONENTS.items():
        emits = set(desc.emits)
        per_block[name] = emits
        union |= emits
    return union, per_block


def test_css_classes_are_declared_by_registry() -> None:
    """Every class in the shipped CSS must be in some descriptor's ``emits``."""
    css_classes, per_partial = _all_css_classes()
    registry_classes, _ = _all_registry_emits()

    orphans = css_classes - registry_classes
    if not orphans:
        return

    # Attach first-seen partial to each orphan so the failure message points
    # the author at the file to edit.
    first_seen: dict[str, str] = {}
    for partial_name, classes in per_partial.items():
        for cls in classes & orphans:
            first_seen.setdefault(cls, partial_name)

    lines = [
        f"{len(orphans)} CSS classes have no owning ComponentDescriptor:",
        "  (add to an existing descriptor's elements/variants/sizes/modifiers,",
        "   add to extra_emits, or delete the stale rule)",
        "",
    ]
    lines.extend(f"  .{cls}  <- {first_seen.get(cls, '??')}" for cls in sorted(orphans))
    raise AssertionError("\n".join(lines))


def test_registry_emits_are_defined_in_css() -> None:
    """Every class a descriptor promises must exist in some partial."""
    css_classes, _ = _all_css_classes()
    registry_classes, per_block = _all_registry_emits()

    orphans = registry_classes - css_classes
    if not orphans:
        return

    # Attach descriptor(s) that promise each orphan class.
    owners: dict[str, list[str]] = {}
    for block_name, emits in per_block.items():
        for cls in emits & orphans:
            owners.setdefault(cls, []).append(block_name)

    lines = [
        f"{len(orphans)} descriptor emits have no matching CSS rule:",
        "  (add the CSS, trim the descriptor, or move to extra_emits if",
        "   intentionally declared but style-less)",
        "",
    ]
    lines.extend(
        f"  .{cls}  <- {', '.join(sorted(owners.get(cls, ['??'])))}" for cls in sorted(orphans)
    )
    raise AssertionError("\n".join(lines))


def test_emits_is_derived_from_grammar() -> None:
    """Sanity check: the property derives block/elements/variants/sizes/modifiers.

    Grammar-derived classes appear in ``emits`` unless explicitly listed in
    :data:`_AUTO_TRIMS` for that block (drift reconciliation).
    """
    for name, desc in COMPONENTS.items():
        emits = desc.emits
        trims = _AUTO_TRIMS.get(desc.block, frozenset())

        expected: list[tuple[str, str]] = [(f"chirpui-{desc.block}", "block")]
        expected.extend((f"chirpui-{desc.block}__{e}", e) for e in desc.elements)
        expected.extend((f"chirpui-{desc.block}--{v}", v) for v in desc.variants if v)
        expected.extend((f"chirpui-{desc.block}--{s}", s) for s in desc.sizes if s)
        expected.extend((f"chirpui-{desc.block}--{m}", m) for m in desc.modifiers if m)
        expected.extend((x, x) for x in desc.extra_emits)

        for cls, tag in expected:
            if cls in trims:
                continue
            assert cls in emits, (name, tag)


def test_streaming_family_classes_are_typed_descriptors() -> None:
    """Streaming/SSE state classes should not live in auto reconciliation maps."""
    from chirp_ui.components import _AUTO_EXTRAS

    assert not {"streaming-bubble", "streaming-block", "streaming", "sse-retry"} & set(_AUTO_EXTRAS)

    streaming_bubble = COMPONENTS["streaming_bubble"]
    assert streaming_bubble.variants == ("thinking", "error")
    assert streaming_bubble.elements == ("thinking",)

    assert COMPONENTS["streaming-block"].modifiers == ("active",)
    assert COMPONENTS["streaming"].variants == ("error",)
    assert COMPONENTS["sse-retry"].modifiers == ("loading",)
