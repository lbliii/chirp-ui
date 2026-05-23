from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "DRAWER-TRAY-ANATOMY.md"
DESIGN = ROOT / "docs" / "DESIGN-interactive-anatomy.md"


def _ledger() -> str:
    text = DOC.read_text(encoding="utf-8")
    return text.split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_drawer_tray_anatomy_doc_applies_evidence_ledger() -> None:
    ledger = _ledger()

    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in ledger
    assert "docs/tests contract for the rendered drawer/tray family" in ledger
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


def test_drawer_tray_ledger_covers_surfaces_and_runtime_contracts() -> None:
    ledger = _ledger()

    for surface in [
        "`drawer` plus `drawer_trigger`",
        "`tray` plus `tray_trigger`",
    ]:
        assert surface in ledger

    for contract in [
        "Native `<dialog>` opened with `showModal()`",
        '`form method="dialog"`',
        "`chirpuiDialogTarget()`",
        '`Alpine.store("trays")`',
        "`data-tray-id`",
        "`x-trap.inert.noscroll`",
        "`chirpui:tray-closed`",
    ]:
        assert contract in ledger


def test_drawer_tray_ledger_preserves_focus_security_and_overflow_boundaries() -> None:
    ledger = _ledger()

    for contract in [
        "Escape closes the dialog",
        "store initialization and persistence behavior across boosted navigation",
        "phone and tablet widths",
        "tray ids stay in escaped `data-tray-id` attributes",
        "out of Alpine JavaScript string literals",
        "known hit-target anomaly with the app-shell topbar",
    ]:
        assert contract in ledger


def test_drawer_tray_ledger_names_executable_proof_and_residual_risk() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_components.py`",
        "`tests/browser/test_drawer.py`",
        "`tests/browser/test_tray.py`",
        "`tests/browser/test_alpine_lifecycle.py`",
    ]:
        assert proof in ledger

    assert "no manual screen-reader or assistive-technology proof is claimed" in ledger


def test_drawer_tray_ledger_matches_design_ledger_fields() -> None:
    """Family-specific ledgers should not silently drift from the design contract."""
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    drawer_tray_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in drawer_tray_ledger
