from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "components" / "context-menu-anatomy.md"
DESIGN = ROOT / "docs" / "decisions" / "interactive-anatomy.md"
INDEX = ROOT / "docs" / "INDEX.md"
SOURCE_INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _ledger() -> str:
    return _text().split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_context_menu_anatomy_is_shipped_contract() -> None:
    text = _text()
    normalized = _normalized(text)

    assert "**Status:** shipped contract" in text
    assert "Import from `chirpui/context_menu.html`:" in text
    assert "docs/tests contract for the rendered context menu family" in normalized


def test_context_menu_anatomy_preserves_dropdown_and_payload_boundaries() -> None:
    text = _text()
    normalized = _normalized(text)

    for signal in [
        "`row_actions(...)` or `dropdown_menu(...)` for visible action affordances.",
        "`dropdown_select(...)` for command/filter selection.",
        "Do not reuse `dropdown_menu(...)` as a fake context menu.",
        "rendered into escaped DOM attributes and read by named Alpine code",
    ]:
        assert signal in text
    assert "not interpolated into Alpine JavaScript object literals" in normalized


def test_context_menu_anatomy_covers_trigger_keyboard_focus_and_positioning() -> None:
    text = _text()
    normalized = _normalized(text)

    for signal in [
        "native `contextmenu` event",
        "`ContextMenu` or Shift+F10",
        "ArrowDown and ArrowUp move among items via roving tabindex",
        "Home and End move to first and last item",
        "Escape closes the menu and returns focus to the trigger",
        "Disabled items stay focusable with `aria-disabled=\"true\"`",
        "clamps the panel to the viewport on open",
    ]:
        assert signal in text
    assert "positions from the trigger rectangle" in normalized


def test_context_menu_ledger_matches_interactive_anatomy_fields() -> None:
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    context_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in context_ledger


def test_context_menu_ledger_names_required_proof_and_deferred_scope() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_components.py`",
        "`tests/browser/test_context_menu_gauntlet.py`",
        "no manual screen-reader or assistive-technology proof is claimed",
    ]:
        assert proof in ledger

    for deferred in [
        "Submenus",
        "checkbox/radio items",
        "typeahead search remain out of scope for v1",
    ]:
        assert deferred in _text()


def test_context_menu_source_is_indexed_as_shipped_contract() -> None:
    index = INDEX.read_text(encoding="utf-8")
    inventory = SOURCE_INVENTORY.read_text(encoding="utf-8")

    assert "components/context-menu-anatomy.md" in index
    assert "shipped contract" in index
    assert "docs/components/context-menu-anatomy.md" in inventory
    assert "shipped contract" in inventory
