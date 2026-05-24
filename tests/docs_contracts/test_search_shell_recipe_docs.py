from tests.helpers import REPO_ROOT

RECIPE = REPO_ROOT / "docs" / "patterns" / "search-shell-recipes.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
HTMX = REPO_ROOT / "docs" / "components" / "htmx-patterns.md"
RESPONSIVE = REPO_ROOT / "docs" / "fundamentals" / "responsive.md"
AFFINITY = REPO_ROOT / "docs" / "decisions" / "layout-affinity.md"
SITE_PATTERN = REPO_ROOT / "site" / "content" / "docs" / "patterns" / "search-shells.md"


def test_search_shell_recipe_documents_contract_surfaces() -> None:
    text = RECIPE.read_text(encoding="utf-8")

    for required in [
        "Status: recipe contract",
        "Progressive Enhancement",
        "Scoped Counts",
        "Responsive Command Surface",
        "Facet Rails",
        "Pending And Settling Feedback",
        "Dense Result Items",
        "Proof Checklist",
        "data-chirpui-role",
        "Promotion to public macros requires a separate registry/API plan",
    ]:
        assert required in text


def test_search_shell_recipe_is_linked_from_canonical_guides() -> None:
    assert "[SEARCH-SHELL-RECIPES.md](patterns/search-shell-recipes.md)" in INDEX.read_text(
        encoding="utf-8"
    )
    assert "[SEARCH-SHELL-RECIPES.md](../patterns/search-shell-recipes.md)" in HTMX.read_text(
        encoding="utf-8"
    )
    assert "Dense Search Shells" in RESPONSIVE.read_text(encoding="utf-8")
    assert "[DESIGN-layout-affinity.md](../decisions/layout-affinity.md)" in RECIPE.read_text(
        encoding="utf-8"
    )
    assert "does not redefine the vocabulary or promote descriptor/manifest fields" in (
        RECIPE.read_text(encoding="utf-8")
    )
    assert "Status: proposed recipe-first contract" in AFFINITY.read_text(encoding="utf-8")


def test_search_shell_published_bridge_points_to_durable_sources() -> None:
    text = SITE_PATTERN.read_text(encoding="utf-8")

    assert "type: doc" in text
    assert "docs/patterns/search-shell-recipes.md" in text
    assert "docs/components/htmx-patterns.md" in text
    assert "docs/decisions/layout-affinity.md" in text
    assert "Layout Affinity](../layout-affinity/)" in text
    assert "Do not add a published-only search-shell API here" in text
