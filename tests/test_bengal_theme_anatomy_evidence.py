from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "BENGAL-THEME-ANATOMY.md"
DESIGN = ROOT / "docs" / "DESIGN-interactive-anatomy.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _ledger() -> str:
    return _text().split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_bengal_theme_anatomy_doc_applies_evidence_ledger() -> None:
    ledger = _ledger()

    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in ledger
    assert "docs/tests contract for packaged Bengal theme chrome" in ledger
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


def test_bengal_theme_anatomy_sources_include_page_actions() -> None:
    text = _text()

    for source in [
        "src/bengal_themes/chirp_theme/templates/partials/page-actions.html",
        "src/bengal_themes/chirp_theme/assets/js/enhancements/action-bar.js",
    ]:
        assert source in text

    section = text.split("## Page Actions Popover", 1)[1].split("## Mobile Navigation", 1)[0]
    for hook in [
        "`.chirp-theme-page-actions__trigger`",
        "`.chirp-theme-page-actions__menu[popover]`",
        '`data-action="copy-url"`',
        '`data-action="copy-llm-txt"`',
        '`data-ai="<assistant-id>"`',
        '`rel="noopener noreferrer"`',
    ]:
        assert hook in section


def test_bengal_theme_ledger_covers_theme_owned_surfaces_and_runtime() -> None:
    ledger = _ledger()

    for surface in [
        "Theme menu",
        "search modal",
        "inline search",
        "page actions popover",
        "mobile navigation",
        "docs navigation",
        "TOC",
        "Bengal content tabs",
    ]:
        assert surface in ledger

    for runtime in [
        "`core/theme.js`",
        "`core/search.js`",
        "`enhancements/action-bar.js`",
        "`enhancements/mobile-nav.js`",
        "`enhancements/tabs.js`",
        "`enhancements/toc.js`",
        "Bengal-generated index artifacts",
    ]:
        assert runtime in ledger


def test_bengal_theme_ledger_preserves_boundaries_and_security_claims() -> None:
    ledger = _ledger()

    for boundary in [
        "not a Chirp UI registry component API",
        "must not be conflated with Chirp UI route tabs",
        "no Chirp UI component runtime or manifest projection is implied",
        "should not be promoted into registry APIs without a separate",
        "TOC raw HTML fallback is limited to Bengal-provided already-rendered markup",
        "reads explicit `data-action`, `data-url`, and `data-ai` hooks",
    ]:
        assert boundary in ledger


def test_bengal_theme_ledger_names_executable_proof_and_residual_risk() -> None:
    ledger = _ledger()

    for proof in [
        "`tests/test_bengal_theme_package.py`",
        "`tests/browser/test_bengal_docs_chrome.py`",
        "`tests/test_docs_site.py`",
        "responsive chrome",
        "page actions popover",
        "no document horizontal overflow",
    ]:
        assert proof in ledger

    assert "no manual screen-reader or assistive-technology proof is claimed" in ledger


def test_bengal_theme_ledger_matches_design_ledger_fields() -> None:
    """Family-specific ledgers should not silently drift from the design contract."""
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    bengal_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in bengal_ledger
