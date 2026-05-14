from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS_DOC = ROOT / "docs" / "DENSE-NAVIGATION-SYNTHESIS.md"
RECIPES_DOC = ROOT / "docs" / "DENSE-NAVIGATION-RECIPES.md"
NAVIGATION_DOC = ROOT / "docs" / "NAVIGATION.md"
INDEX_DOC = ROOT / "docs" / "INDEX.md"
DENSE_OBJECT_PLAN = ROOT / "docs" / "plans" / "done" / "PLAN-dense-object-chrome-next.md"
APPLICATION_CHROME_PLAN = ROOT / "docs" / "plans" / "PLAN-application-chrome-system.md"


def test_dense_navigation_synthesis_records_api_decisions() -> None:
    text = SYNTHESIS_DOC.read_text()

    assert "Dense navigation does not need a product-specific mega-header" in text
    assert "Sidebar Badge Parity" in text
    assert "scope_switcher" in text
    assert "saved_view_strip" in text
    assert "dense_nav_frame" in text
    assert "github_header" in text
    assert "DENSE-NAVIGATION-RECIPES.md" in text
    assert "If those answers are not concrete, keep the pattern as a documented recipe." in text


def test_dense_navigation_guides_are_linked_from_navigation_docs() -> None:
    navigation = NAVIGATION_DOC.read_text()
    index = INDEX_DOC.read_text()

    assert "DENSE-NAVIGATION-SYNTHESIS.md" in navigation
    assert "DENSE-NAVIGATION-RECIPES.md" in navigation
    assert "DENSE-NAVIGATION-SYNTHESIS.md" in index
    assert "DENSE-NAVIGATION-RECIPES.md" in index
    assert "PLAN-application-chrome-system.md" in navigation
    assert "PLAN-application-chrome-system.md" in index


def test_application_chrome_plan_keeps_recipe_first_system_boundary() -> None:
    plan = APPLICATION_CHROME_PLAN.read_text()
    navigation = NAVIGATION_DOC.read_text()

    for rock in [
        "Chrome Layer Model",
        "Rail And Tray Design Contracts",
        "Modern Visual Rhythm",
        "Responsive Chrome Gauntlet",
        "Recipe First, Composite Later",
    ]:
        assert f"| {rock} |" in plan

    for layer in [
        "Product rail",
        "Secondary rail",
        "Object context",
        "Local routes",
        "Overlay chrome",
    ]:
        assert f"| {layer} |" in plan

    for deferred in [
        "application_chrome()",
        "object_chrome()",
        "workspace_header()",
        "dense_nav_frame()",
    ]:
        assert deferred in plan

    assert "Application chrome is the umbrella" in navigation
    assert "Use this decision table for rail and overlay navigation" in navigation


def test_dense_object_browser_proof_is_recorded_before_composite_promotion() -> None:
    navigation = NAVIGATION_DOC.read_text()
    plan = DENSE_OBJECT_PLAN.read_text()
    index = INDEX_DOC.read_text()

    for required in [
        "Browser proof covers the same composition",
        "route tabs scroll instead of wrapping into a tall block",
        "command triggers open named palettes and focus search",
    ]:
        assert required in navigation

    assert "Phase 5 accepted: browser proof covers desktop, tablet, and phone widths" in plan
    assert "Phase 4 remains not-now until repeated app usage" in plan
    assert "composite-decision backlog after browser proof" in index


def test_dense_navigation_recipes_keep_layer_model_and_promotion_boundary() -> None:
    text = RECIPES_DOC.read_text()

    for layer in [
        "App identity",
        "Scope",
        "Command jump",
        "Broad navigation",
        "Object context",
        "Local route views",
        "Page tools",
        "Attention",
    ]:
        assert f"| {layer} |" in text

    for required in [
        "Object Page Console",
        "Composite Promotion Boundary",
        "showcase example is evidence for documentation",
        "not enough evidence for a new stable macro",
        "At least two recipes repeat the same shape.",
        "Until then, keep the shape as a recipe.",
    ]:
        assert required in text
