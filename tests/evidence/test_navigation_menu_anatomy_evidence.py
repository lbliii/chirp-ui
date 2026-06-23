from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "components" / "navigation-menu-anatomy.md"
DESIGN = ROOT / "docs" / "decisions" / "interactive-anatomy.md"
INDEX = ROOT / "docs" / "INDEX.md"
SOURCE_INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _ledger() -> str:
    return _text().split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_navigation_menu_anatomy_is_experimental_contract() -> None:
    text = _text()
    assert "**Status:** anatomy contract (experimental surface)" in text
    assert "Import from `chirpui/navigation_menu.html`:" in text
    assert "`experimental` rendered macro contract" in text


def test_navigation_menu_anatomy_preserves_navigation_boundaries() -> None:
    text = _text()
    for signal in [
        "distinct from `menubar` application commands",
        "`dropdown_menu` compact triggers",
        "`route_tabs`",
        "`nav_tree` for docs sidebars",
    ]:
        assert signal in text


def test_navigation_menu_anatomy_covers_keyboard_and_mobile_fallback() -> None:
    text = " ".join(_text().split())
    for signal in [
        "ArrowDown, Enter, or Space opens the flyout",
        "Escape closes the open flyout",
        "Click outside closes the open flyout",
        "wraps instead of forcing horizontal page overflow",
        "drawer or tray fallback",
    ]:
        assert signal in text


def test_navigation_menu_ledger_matches_interactive_anatomy_fields() -> None:
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    navigation_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in navigation_ledger


def test_navigation_menu_anatomy_is_indexed_for_agents() -> None:
    index = INDEX.read_text(encoding="utf-8")
    inventory = SOURCE_INVENTORY.read_text(encoding="utf-8")
    assert "components/navigation-menu-anatomy.md" in index
    assert "Navigation menu flyout anatomy" in index
    assert "docs/components/navigation-menu-anatomy.md" in inventory
