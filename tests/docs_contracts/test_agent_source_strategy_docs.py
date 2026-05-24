from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"
SOURCE_MAP = ROOT / "docs" / "agents" / "agent-source-map.md"


def test_agent_source_inventory_includes_strategy_and_evidence_sources() -> None:
    text = INVENTORY.read_text(encoding="utf-8")

    for row in [
        "| `manifest-derived` | `src/chirp_ui/find.py` |",
        "| `docs-derived` | `docs/decisions/design-system-research.md` |",
        "| `docs-derived` | `docs/safety/public-surface-stabilization.md` |",
        "| `docs-derived` | `docs/decisions/interactive-anatomy.md` |",
        "| `docs-derived` | `docs/screens/` |",
        "promotion-ledger boundaries",
        "| `docs-derived` | `docs/reference-implementations/playbook.md` |",
        "| `docs-derived` | `docs/reference-implementations/README.md` |",
        "| `docs-derived` | `docs/reference-implementations/PROOF-ANALYSIS.md` |",
        "| `docs-derived` | `docs/reference-implementations/RECIPE-GUIDANCE.md` |",
        "| `docs-derived` | `tests/browser/test_page_actions_candidate.py` |",
        "| `docs-derived` | `tests/browser/test_dense_reference_data_reference.py` |",
        "| `docs-derived` | `tests/test_shell_response_targets.py` |",
        "| `docs-derived` | `tests/test_find_cli.py` |",
    ]:
        assert row in text

    for phrase in [
        "python -m chirp_ui find --details",
        "maturity, authoring, role, macro, template, runtime requirements, slots",
        "Screen archetype selection, profile pairing, fixture proof, promotion-ledger boundaries, and agent guidance",
        "Evidence labels, promotion rules, recipe-only boundaries",
        "Interactive anatomy contract and evidence ledger fields",
        "Reference implementation evidence ladder",
        "Index of reference implementation briefs",
        "Source-only proof-analysis decisions",
        "Source-only recipe guidance",
        "Browser proof for private page-action reference fixtures",
        "Browser proof for private dense-reference fixtures",
        "Server proof for shell response ownership reference contracts",
        "CLI proof for agent discovery reference contracts",
        "| `source-only` |",
    ]:
        assert phrase in text


def test_agent_source_map_routes_strategy_sources_without_new_artifacts() -> None:
    text = SOURCE_MAP.read_text(encoding="utf-8")

    for row in [
        "| `src/chirp_ui/find.py` | `manifest-derived` | Local human/agent discovery through `python -m chirp_ui find --details` |",
        "| `docs/decisions/design-system-research.md` | `docs-derived` |",
        "| `docs/safety/public-surface-stabilization.md` | `docs-derived` |",
        "| `docs/decisions/interactive-anatomy.md` | `docs-derived` |",
        "| `docs/screens/` | `docs-derived` |",
        "promotion-ledger boundaries",
        "| `docs/reference-implementations/playbook.md` | `docs-derived` |",
        "| `docs/reference-implementations/README.md` | `docs-derived` |",
        "| `docs/reference-implementations/PROOF-ANALYSIS.md` | `docs-derived` |",
        "| `docs/reference-implementations/RECIPE-GUIDANCE.md` | `docs-derived` |",
        "| `tests/browser/test_page_actions_candidate.py` | `docs-derived` |",
        "| `tests/browser/test_dense_reference_data_reference.py` | `docs-derived` |",
        "| `tests/test_shell_response_targets.py` | `docs-derived` |",
        "| `tests/test_find_cli.py` | `docs-derived` |",
    ]:
        assert row in text

    for phrase in [
        "not a generated artifact",
        "Screen archetype selection, profile pairing, fixture proof, promotion-ledger boundaries, and agent guidance for complete product situations",
        "Research ledger and categorical positioning; not copyable snippet source.",
        "Evidence labels, promotion gates, recipe-only boundaries, and compatibility policy.",
        "Evidence ledger and stop-and-ask boundaries for behavior-bearing promotions.",
        "Reference implementation evidence ladder and public-API stop boundaries.",
        "Source-only proof-analysis ledger for reference fixture decisions",
        "Source-only recipe guidance for current-primitive decisions",
        "Browser proof for private page-action fixtures; source-only evidence, never copyable snippets.",
        "Browser proof for private dense-reference fixtures; source-only evidence, never copyable snippets.",
        "Server proof for response ownership; source-only evidence, never copyable snippets.",
        "CLI proof for registry discovery; source-only evidence, never copyable snippets.",
        "not copyable snippet source.",
    ]:
        assert phrase in text
