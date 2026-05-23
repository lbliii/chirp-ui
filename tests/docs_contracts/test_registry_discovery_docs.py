from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "REGISTRY-DISCOVERY.md"
INDEX = ROOT / "docs" / "INDEX.md"
INVENTORY = ROOT / "docs" / "AGENT-SOURCE-INVENTORY.md"
SOURCE_MAP = ROOT / "docs" / "AGENT-SOURCE-MAP.md"


def test_registry_discovery_doc_covers_cli_audits_and_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "python -m chirp_ui find metric",
        "python -m chirp_ui find --authoring=preferred",
        "python -m chirp_ui find --maturity=experimental",
        "python -m chirp_ui find --role=pattern --maturity=experimental --details",
        "python -m chirp_ui find token-input --details",
        "Preferred primitives",
        "Experimental public surfaces",
        "Recipe-first patterns",
        "Compatibility helpers",
        "find is discovery, not validation",
        "find --details is local CLI output, not a generated artifact",
        "chirpui-manifest@5",
    ]:
        assert required in text


def test_registry_discovery_doc_covers_python_helpers_and_labels() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "components_by_authoring",
        "components_by_maturity",
        "components_by_role",
        "detailed_search",
        "preferred_components",
        "`maturity`",
        "`authoring`",
        "`role`",
        "`category`",
        "Do not infer `recipe-only` from a name alone.",
        "[PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md)",
        "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)",
    ]:
        assert required in text


def test_registry_discovery_doc_is_indexed_and_agent_sourced() -> None:
    link = "[REGISTRY-DISCOVERY.md](REGISTRY-DISCOVERY.md)"

    assert link in INDEX.read_text(encoding="utf-8")
    assert "| `docs-derived` | `docs/REGISTRY-DISCOVERY.md` |" in INVENTORY.read_text(
        encoding="utf-8"
    )
    assert "| `docs/REGISTRY-DISCOVERY.md` | `docs-derived` |" in SOURCE_MAP.read_text(
        encoding="utf-8"
    )
