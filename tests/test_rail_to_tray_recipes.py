from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = (
    ROOT
    / "examples"
    / "component-showcase"
    / "templates"
    / "showcase"
    / "_rail_to_tray_chrome.html"
)
SHOWCASE_NAV = (
    ROOT / "examples" / "component-showcase" / "templates" / "showcase" / "navigation.html"
)
NAV_DOC = ROOT / "docs" / "NAVIGATION.md"
RECIPES_DOC = ROOT / "docs" / "DENSE-NAVIGATION-RECIPES.md"


def test_rail_to_tray_showcase_exports_copyable_recipe() -> None:
    text = RECIPE.read_text(encoding="utf-8")

    assert "{% def rail_to_tray_chrome() %}" in text
    for required in [
        "nav_tree",
        "drawer_trigger",
        "drawer(",
        "command_palette_trigger",
        "route_tabs",
        "badge_loading",
        "badge_expected",
        "appchrome-rail-recipe__mobile-trigger",
    ]:
        assert required in text


def test_rail_to_tray_recipe_is_reachable_from_showcase_and_docs() -> None:
    showcase = SHOWCASE_NAV.read_text(encoding="utf-8")
    navigation = NAV_DOC.read_text(encoding="utf-8")
    recipes = RECIPES_DOC.read_text(encoding="utf-8")

    assert "_rail_to_tray_chrome.html" in showcase
    assert "Rail To Drawer Navigation" in showcase
    assert "rail-to-drawer application chrome recipe" in navigation
    assert "## Rail To Drawer Application Chrome" in recipes
    assert "examples/component-showcase/templates/showcase/_rail_to_tray_chrome.html" in recipes


def test_rail_to_tray_recipe_keeps_composite_api_out_of_scope() -> None:
    text = RECIPE.read_text(encoding="utf-8")
    recipes = RECIPES_DOC.read_text(encoding="utf-8")

    assert "{% def application_chrome" not in text
    assert "{% def workspace_shell" not in text
    assert "a generic `application_chrome()` macro" in recipes
    assert "product-specific shell clones" in recipes
