from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "agents" / "registry-discovery.md"
INDEX = ROOT / "docs" / "INDEX.md"
INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"
SOURCE_MAP = ROOT / "docs" / "agents" / "agent-source-map.md"


def test_registry_discovery_doc_separates_app_and_component_mcp_layers() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "Chirp's Milo-backed MCP server (`chirp --mcp`)",
        "`check`, `diff`, `routes`",
        "Chirp UI's manifest MCP server (`chirp-ui mcp`)",
        "`find_components`, `get_component`, `list_categories`",
        "load or validate a Chirp application",
        "https://lbliii.github.io/chirp/docs/reference/cli/",
    ]:
        assert required in text


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
        "[PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md)",
        "[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md)",
    ]:
        assert required in text


def test_registry_discovery_doc_is_indexed_and_agent_sourced() -> None:
    link = "[REGISTRY-DISCOVERY.md](agents/registry-discovery.md)"

    assert link in INDEX.read_text(encoding="utf-8")
    assert "| `docs-derived` | `docs/agents/registry-discovery.md` |" in INVENTORY.read_text(
        encoding="utf-8"
    )
    assert "| `docs/agents/registry-discovery.md` | `docs-derived` |" in SOURCE_MAP.read_text(
        encoding="utf-8"
    )
