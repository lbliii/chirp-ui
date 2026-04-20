"""Doc-block coverage gate — every chirp-ui template must carry a description.

Sprint 4 of the agent-grounding-depth epic: agents reading the manifest get
the component's purpose in natural language. The gate is hard from day 1 —
all 195 bundled templates already carry a ``{#- chirp-ui: ... -#}`` block
at the time of Sprint 4 (verified 2026-04-20), so there is no grandfather
allow-list to maintain.

Policy summary (see ``AGENTS.md`` and ``CLAUDE.md``):

* **Syntax**: ``{#- chirp-ui: Title\\n  Body…\\n-#}`` at the top of the
  template file, before any ``{% def %}`` or ``{% from %}``.
* **One block per file**, documenting every macro in that file.
* **Both whitespace-trim markers accepted**: ``{#- … -#}`` is the
  canonical form; ``{# … #}`` also parses.
"""

from __future__ import annotations

from pathlib import Path

from chirp_ui._macro_introspect import description_from_template

_TEMPLATES_DIR = Path(__file__).parent.parent / "src" / "chirp_ui" / "templates" / "chirpui"


def _all_template_names() -> list[str]:
    return sorted(p.name for p in _TEMPLATES_DIR.glob("*.html"))


def test_every_template_has_doc_block() -> None:
    """Every bundled template must surface a non-empty description.

    New templates: add a ``{#- chirp-ui: ... -#}`` block at the top of the
    file. See ``CLAUDE.md § Adding a component`` for the checklist.
    """
    missing = [name for name in _all_template_names() if not description_from_template(name)]
    assert not missing, (
        "templates without a {#- chirp-ui: ... -#} doc-block:\n"
        + "\n".join(f"  {name}" for name in missing)
        + "\nAdd a leading doc-block per AGENTS.md § Done criteria."
    )


def test_description_first_line_is_title() -> None:
    """Sanity: non-empty first line is present (title/headline of the block)."""
    bad = []
    for name in _all_template_names():
        desc = description_from_template(name)
        first_line = desc.splitlines()[0] if desc else ""
        if not first_line.strip():
            bad.append(name)
    assert not bad, "templates whose doc-block has an empty first line:\n" + "\n".join(
        f"  {n}" for n in bad
    )


def test_description_extraction_is_cached() -> None:
    """Repeat calls must hit the cache — keeps manifest builds cheap."""
    description_from_template.cache_clear()
    description_from_template("card.html")
    info_first = description_from_template.cache_info()
    description_from_template("card.html")
    info_second = description_from_template.cache_info()
    assert info_second.hits > info_first.hits


def test_description_present_in_manifest_for_canonical_components() -> None:
    """Spot-check: high-traffic components surface the doc-block title in the manifest."""
    from chirp_ui.manifest import build_manifest

    m = build_manifest()
    # Each first-line title is the literal opener of its doc-block.
    assert m["components"]["card"]["description"].startswith("Card component")
    assert m["components"]["btn"]["description"].startswith("Button component")
    assert m["components"]["alert"]["description"].startswith("Alert component")
    assert m["components"]["modal"]["description"].startswith("Modal component")
    assert m["components"]["metric-card"]["description"].startswith("Metric grid/card")


def test_components_without_template_have_empty_description() -> None:
    """``category=auto`` descriptors (no template) must emit ``description: \"\"`` — not error."""
    from chirp_ui.components import COMPONENTS
    from chirp_ui.manifest import build_manifest

    m = build_manifest()
    for name, entry in m["components"].items():
        if not COMPONENTS[name].template:
            assert entry["description"] == "", (
                f"{name}: description should be '' when there is no template"
            )


def test_components_with_description_stat_matches_count() -> None:
    """``stats.components_with_description`` equals the count of non-empty descriptions."""
    from chirp_ui.manifest import build_manifest

    m = build_manifest()
    expected = sum(1 for e in m["components"].values() if e["description"])
    assert m["stats"]["components_with_description"] == expected
    # Sanity floor — most descriptors with a template should carry a block.
    assert m["stats"]["components_with_description"] > 150
