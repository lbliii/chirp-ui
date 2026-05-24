from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "components" / "modal-anatomy.md"
DESIGN = ROOT / "docs" / "decisions" / "interactive-anatomy.md"


def _ledger() -> str:
    text = DOC.read_text(encoding="utf-8")
    return text.split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_modal_anatomy_doc_applies_evidence_ledger() -> None:
    ledger = _ledger()

    assert "[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md)" in ledger
    assert "docs/tests contract for the rendered modal family" in ledger
    assert "not descriptor or manifest metadata" in ledger

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


def test_modal_anatomy_ledger_covers_all_modal_family_surfaces() -> None:
    ledger = _ledger()

    for surface in [
        "`modal` plus `modal_trigger`",
        "`confirm_dialog` plus `confirm_trigger`",
        "`modal_overlay` plus `modal_overlay_trigger`",
    ]:
        assert surface in ledger

    for contract in [
        "Native `<dialog>` opened with `showModal()`",
        '`form method="dialog"`',
        "`x-trap.inert.noscroll`",
        "`chirpuiDialogTarget()`",
        '`hx-disinherit="hx-select hx-target hx-swap"`',
        '`Alpine.store("modals")`',
    ]:
        assert contract in ledger


def test_modal_anatomy_ledger_names_executable_proof_and_residual_risk() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_components.py`",
        "`tests/browser/test_modals.py`",
        "`tests/browser/test_alpine_lifecycle.py`",
    ]:
        assert proof in ledger

    assert "no manual screen-reader or assistive-technology proof is claimed" in ledger


def test_modal_anatomy_ledger_matches_design_ledger_fields() -> None:
    """Family-specific ledgers should not silently drift from the design contract."""
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    modal_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in modal_ledger
