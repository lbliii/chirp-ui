from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS_DOC = ROOT / "docs" / "DENSE-NAVIGATION-SYNTHESIS.md"
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
    assert "If those answers are not concrete, keep the pattern as a documented recipe." in text


def test_dense_navigation_synthesis_is_linked_from_navigation_docs() -> None:
    navigation = NAVIGATION_DOC.read_text()
    index = INDEX_DOC.read_text()

    assert "DENSE-NAVIGATION-SYNTHESIS.md" in navigation
    assert "DENSE-NAVIGATION-SYNTHESIS.md" in index
