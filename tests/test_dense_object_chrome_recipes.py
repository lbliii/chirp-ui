from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = (
    ROOT
    / "examples"
    / "component-showcase"
    / "templates"
    / "showcase"
    / "_dense_object_chrome.html"
)
NAV_DOC = ROOT / "docs" / "NAVIGATION.md"
PLAN = ROOT / "docs" / "plans" / "PLAN-dense-object-chrome-next.md"


def test_dense_object_chrome_showcase_exports_two_recipe_shapes() -> None:
    text = RECIPE.read_text(encoding="utf-8")

    assert "{% def dense_project_object_chrome() %}" in text
    assert "{% def dense_settings_object_chrome() %}" in text
    for required in [
        "command_palette_trigger",
        "primary_nav",
        "breadcrumbs",
        "inline_counter",
        "route_tabs",
        "badge_loading",
        "badge_expected",
    ]:
        assert required in text


def test_dense_object_chrome_stays_recipe_level_until_browser_proof_repeats() -> None:
    recipe = RECIPE.read_text(encoding="utf-8")
    docs = NAV_DOC.read_text(encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")

    assert "{% def object_chrome" not in recipe
    assert "{% def workspace_header" not in recipe
    assert "dense object chrome recipes" in docs
    assert "remain recipe-level ideas" in docs
    assert "Do not add a public `object_chrome()` or `workspace_header()`" in plan
