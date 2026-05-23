from tests.helpers import REPO_ROOT

RECIPE = REPO_ROOT / "docs" / "WORKSPACE-SHELL-RECIPES.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
PRIMITIVES = REPO_ROOT / "docs" / "PRIMITIVES.md"
SITE_PATTERN = REPO_ROOT / "site" / "content" / "docs" / "patterns" / "workspace-shells.md"


def test_workspace_shell_recipe_documents_agent_surface() -> None:
    text = RECIPE.read_text(encoding="utf-8")

    for required in [
        "Status: experimental, agent-facing",
        "Search Workspace",
        "Operations Workspace",
        "Support Queue",
        "Admin Workspace",
        "HTMX Boundary",
        "Agent Checklist",
        "workspace_shell",
        "filter_rail",
        "result_collection",
        "result_card",
        "metric_strip",
        "inspector_panel",
    ]:
        assert required in text


def test_workspace_shell_recipe_is_linked_from_canonical_guides() -> None:
    assert "[WORKSPACE-SHELL-RECIPES.md](WORKSPACE-SHELL-RECIPES.md)" in INDEX.read_text(
        encoding="utf-8"
    )
    primitives = PRIMITIVES.read_text(encoding="utf-8")
    assert "Dense workspace primitives" in primitives
    assert "filter_rail" in primitives
    assert "inspector_panel" in primitives


def test_workspace_shell_published_bridge_points_to_durable_source() -> None:
    text = SITE_PATTERN.read_text(encoding="utf-8")

    assert "type: doc" in text
    assert "docs/WORKSPACE-SHELL-RECIPES.md" in text
    assert "workspace_shell" in text
    assert "filter_rail" in text
    assert "inspector_panel" in text
