from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "components" / "context-menu-anatomy.md"
DESIGN = ROOT / "docs" / "decisions" / "interactive-anatomy.md"
PLAN = ROOT / "docs" / "plans" / "PLAN-component-maturity-gap-sweep.md"
INDEX = ROOT / "docs" / "INDEX.md"
SOURCE_INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _ledger() -> str:
    return _text().split("## Evidence Ledger", 1)[1].split("## Implementation Gate", 1)[0]


def test_context_menu_anatomy_is_preimplementation_source_only() -> None:
    text = _text()
    normalized = _normalized(text)

    for signal in [
        "**Status:** design contract, not shipped",
        "Chirp UI does not ship a context-menu macro yet.",
        "The API is intentionally not approved.",
        "Do not publish `context_menu(...)`, `context_menu_trigger(...)`, or",
        "`chirpui-context-menu*` app markup until render tests and browser tests prove",
    ]:
        assert signal in text
    for signal in [
        "pre- implementation contract",
        "pre-implementation docs/tests contract, not descriptor or manifest metadata",
    ]:
        assert signal in normalized


def test_context_menu_anatomy_preserves_dropdown_and_payload_boundaries() -> None:
    text = _text()
    normalized = _normalized(text)

    for signal in [
        "`row_actions(...)` or `dropdown_menu(...)` for visible action affordances.",
        "`dropdown_select(...)` for command/filter selection.",
        "Reusing `dropdown_menu(...)` as a fake context menu.",
        "rendered into escaped DOM attributes and read by named Alpine code",
    ]:
        assert signal in text
    for signal in [
        "not primary navigation, not a replacement for visible row actions, and not a general dropdown trigger style",
        "not interpolated into inline JavaScript object literals",
    ]:
        assert signal in normalized


def test_context_menu_anatomy_covers_trigger_keyboard_focus_and_positioning() -> None:
    text = _text()
    normalized = _normalized(text)

    for signal in [
        "open on the native `contextmenu` event",
        "`ContextMenu` or `Shift+F10`",
        "Open moves focus into the first enabled item.",
        "ArrowDown and ArrowUp move among enabled items and wrap.",
        "Home and End move to first and last enabled item.",
        "Enter and Space activate the focused item.",
        "Escape closes the menu and returns focus to the owning element.",
        "Tab closes the menu and allows normal document focus movement.",
        "use roving `tabindex`",
        "Pointer-opened menus position from the event coordinates.",
        "must stay inside the visual viewport",
        "no document-level horizontal overflow",
    ]:
        assert signal in text
    assert "Keyboard-opened menus position from the owning element rectangle." in normalized


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
        "strict-undefined item tests",
        "escaping tests for `data-*` payloads",
        "browser tests for pointer open",
        "keyboard open",
        "roving focus",
        "Escape",
        "outside click",
        "resize flip",
        "overflow containment",
        "No assistive-technology proof is claimed.",
    ]:
        assert proof in ledger

    for deferred in [
        "Submenus",
        "Checkbox/radio menu items",
        "Typeahead search",
        "A global context-menu manager",
    ]:
        assert deferred in _text()


def test_context_menu_source_is_indexed_but_not_marked_shipped() -> None:
    plan = PLAN.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    inventory = SOURCE_INVENTORY.read_text(encoding="utf-8")
    plan_normalized = _normalized(plan)

    assert "components/context-menu-anatomy.md" in index
    assert "docs/components/context-menu-anatomy.md" in inventory
    assert "source-only" in inventory
    assert "Context-menu anatomy is now drafted as a source-only design contract" in plan_normalized
    assert "no public context-menu macro or classes are shipped yet" in plan_normalized
    assert (
        "Implement `context_menu` only after accepting the source-only anatomy" in plan_normalized
    )
