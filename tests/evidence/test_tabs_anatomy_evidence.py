from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "TABS-ANATOMY.md"
DESIGN = ROOT / "docs" / "DESIGN-interactive-anatomy.md"


def _ledger() -> str:
    text = DOC.read_text(encoding="utf-8")
    return text.split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_tabs_anatomy_doc_applies_evidence_ledger() -> None:
    ledger = _ledger()

    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in ledger
    assert "docs/tests contract for the rendered tabs family" in ledger
    assert "not descriptor or manifest" in ledger
    assert "metadata" in ledger

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


def test_tabs_ledger_preserves_semantic_boundaries() -> None:
    ledger = _ledger()

    for boundary in [
        "`tabs` plus `tab` for in-place htmx tab widgets",
        "`tabs_container`, `tab_button`, and `tab_panel`",
        "`render_route_tabs`, compatibility alias `route_tabs`",
        "ARIA tab widget semantics",
        "ARIA tab/panel semantics",
        "Navigation semantics",
        "route tabs are not ARIA tab widgets",
        "Route tabs must continue to avoid ARIA tab-widget claims",
    ]:
        assert boundary in ledger


def test_tabs_ledger_covers_htmx_alpine_and_layout_contracts() -> None:
    ledger = _ledger()

    for contract in [
        '`hx-boost="false"`',
        '`hx-select="unset"`',
        '`hx-push-url="false"`',
        '`hx-push-url="true"`',
        "`chirpuiTabs()`",
        "`chirpui:tab-changed`",
        "`tab_is_active`",
        "`#page-root`",
        "`#page-content-inner`",
    ]:
        assert contract in ledger


def test_tabs_ledger_preserves_keyboard_and_security_boundaries() -> None:
    ledger = _ledger()

    for contract in [
        "no roving-arrow tablist keyboard model is published",
        "keyboard navigation is browser link navigation",
        "escaped `data-tab-id`",
        "templates must not interpolate tab ids into Alpine JavaScript string literals",
        "dict-like and dataclass item shapes",
    ]:
        assert contract in ledger


def test_tabs_ledger_names_executable_proof_and_residual_risk() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_components.py`",
        "`tests/test_route_tabs.py`",
        "`tests/browser/test_tabs.py`",
        "`tests/browser/test_alpine_lifecycle.py`",
        "browser shell tests",
    ]:
        assert proof in ledger

    assert "no manual screen-reader or assistive-technology proof is claimed" in ledger


def test_tabs_ledger_matches_design_ledger_fields() -> None:
    """Family-specific ledgers should not silently drift from the design contract."""
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    tabs_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in tabs_ledger
