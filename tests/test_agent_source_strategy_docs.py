from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "AGENT-SOURCE-INVENTORY.md"
SOURCE_MAP = ROOT / "docs" / "AGENT-SOURCE-MAP.md"


def test_agent_source_inventory_includes_strategy_and_evidence_sources() -> None:
    text = INVENTORY.read_text(encoding="utf-8")

    for row in [
        "| `manifest-derived` | `src/chirp_ui/find.py` |",
        "| `docs-derived` | `docs/DESIGN-SYSTEM-RESEARCH.md` |",
        "| `docs-derived` | `docs/PUBLIC-SURFACE-STABILIZATION.md` |",
        "| `docs-derived` | `docs/DESIGN-interactive-anatomy.md` |",
        "| `docs-derived` | `docs/REFERENCE-IMPLEMENTATION-PLAYBOOK.md` |",
        "| `docs-derived` | `docs/reference-implementations/README.md` |",
    ]:
        assert row in text

    for phrase in [
        "python -m chirp_ui find --details",
        "maturity, authoring, role, macro, template, runtime requirements, slots",
        "Evidence labels, promotion rules, recipe-only boundaries",
        "Interactive anatomy contract and evidence ledger fields",
        "Reference implementation evidence ladder",
        "Index of reference implementation briefs",
        "| `source-only` |",
    ]:
        assert phrase in text


def test_agent_source_map_routes_strategy_sources_without_new_artifacts() -> None:
    text = SOURCE_MAP.read_text(encoding="utf-8")

    for row in [
        "| `src/chirp_ui/find.py` | `manifest-derived` | Local human/agent discovery through `python -m chirp_ui find --details` |",
        "| `docs/DESIGN-SYSTEM-RESEARCH.md` | `docs-derived` |",
        "| `docs/PUBLIC-SURFACE-STABILIZATION.md` | `docs-derived` |",
        "| `docs/DESIGN-interactive-anatomy.md` | `docs-derived` |",
        "| `docs/REFERENCE-IMPLEMENTATION-PLAYBOOK.md` | `docs-derived` |",
        "| `docs/reference-implementations/README.md` | `docs-derived` |",
    ]:
        assert row in text

    for phrase in [
        "not a generated artifact",
        "Research ledger and categorical positioning; not copyable snippet source.",
        "Evidence labels, promotion gates, recipe-only boundaries, and compatibility policy.",
        "Evidence ledger and stop-and-ask boundaries for behavior-bearing promotions.",
        "Reference implementation evidence ladder and public-API stop boundaries.",
        "not copyable snippet source.",
    ]:
        assert phrase in text
