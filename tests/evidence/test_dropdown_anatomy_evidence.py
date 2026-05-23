from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "DROPDOWN-ANATOMY.md"
DESIGN = ROOT / "docs" / "DESIGN-interactive-anatomy.md"


def _ledger() -> str:
    text = DOC.read_text(encoding="utf-8")
    return text.split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_dropdown_anatomy_doc_applies_evidence_ledger() -> None:
    ledger = _ledger()

    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in ledger
    assert "docs/tests contract for the rendered dropdown family" in ledger
    assert "not descriptor or" in ledger
    assert "manifest metadata" in ledger

    for field in [
        "Surface",
        "Label",
        "Anatomy",
        "Native semantics",
        "Keyboard",
        "Focus",
        "Runtime",
        "Motion",
        "Responsive and overflow",
        "Security and escaping",
        "Performance",
        "Proof",
        "Residual risk",
    ]:
        assert f"| {field} |" in ledger


def test_dropdown_anatomy_ledger_covers_dropdown_surfaces_and_runtime() -> None:
    ledger = _ledger()

    for surface in [
        "`dropdown_menu` command menu",
        "`dropdown_select` combobox/listbox selection surface",
        "`dropdown_split` primary action plus command menu",
    ]:
        assert surface in ledger

    for contract in [
        "`chirpuiDropdown()`",
        "`chirpuiDropdownSelect()`",
        "`x-id`",
        "`x-show`",
        "`x-cloak`",
        "`x-transition`",
        "`route_link_attrs()`",
    ]:
        assert contract in ledger


def test_dropdown_anatomy_ledger_preserves_keyboard_and_payload_boundaries() -> None:
    ledger = _ledger()

    for contract in [
        "roving-arrow menu navigation is not yet published",
        "ArrowDown, ArrowUp, and Enter",
        "Selection returns focus to the trigger",
        "templates must not interpolate server values into Alpine JavaScript object literals",
        "escaped `data-label`, `data-href`, and `data-action`",
        "escaped `data-label` and `data-value`",
    ]:
        assert contract in ledger


def test_dropdown_anatomy_ledger_names_executable_proof_and_residual_risk() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_components.py`",
        "`tests/browser/test_dropdowns.py`",
        "gauntlet browser tests",
    ]:
        assert proof in ledger

    assert "no manual screen-reader or assistive-technology proof is claimed" in ledger


def test_dropdown_anatomy_ledger_matches_design_ledger_fields() -> None:
    """Family-specific ledgers should not silently drift from the design contract."""
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    dropdown_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in dropdown_ledger
