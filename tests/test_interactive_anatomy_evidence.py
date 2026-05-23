from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANATOMY = ROOT / "docs" / "DESIGN-interactive-anatomy.md"
PUBLIC_SURFACE = ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"
INDEX = ROOT / "docs" / "INDEX.md"


def test_interactive_anatomy_doc_defines_evidence_ledger() -> None:
    text = ANATOMY.read_text(encoding="utf-8")
    ledger = text.split("## Evidence Ledger", 1)[1].split("## Projection Decision", 1)[0]

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

    for boundary in [
        "docs/tests contract, not descriptor or manifest metadata",
        "prefer native HTML before ARIA",
        "Do not claim screen-reader or assistive-technology proof unless it was manually",
        "Automated render/browser proof",
    ]:
        assert boundary in ledger


def test_public_surface_promotions_route_behavioral_work_through_ledger() -> None:
    text = PUBLIC_SURFACE.read_text(encoding="utf-8")
    promotion = text.split("## Promotion Rule", 1)[1].split("## Proof Tracks", 1)[0]

    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in promotion
    for required in [
        "Interactive, shell-adjacent, theme-hook, and behavior-bearing promotions",
        "native semantics",
        "keyboard",
        "focus",
        "runtime",
        "security/escaping",
        "residual risk",
    ]:
        assert required in promotion


def test_interactive_anatomy_design_doc_is_indexed() -> None:
    assert "[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md)" in (
        INDEX.read_text(encoding="utf-8")
    )
