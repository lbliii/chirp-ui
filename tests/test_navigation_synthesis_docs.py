from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS_DOC = ROOT / "docs" / "DENSE-NAVIGATION-SYNTHESIS.md"
RECIPES_DOC = ROOT / "docs" / "DENSE-NAVIGATION-RECIPES.md"
NAVIGATION_DOC = ROOT / "docs" / "NAVIGATION.md"
INDEX_DOC = ROOT / "docs" / "INDEX.md"


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
