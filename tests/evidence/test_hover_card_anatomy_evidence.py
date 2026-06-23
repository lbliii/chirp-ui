from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
DOC = ROOT / "docs" / "components" / "hover-card-anatomy.md"
DESIGN = ROOT / "docs" / "decisions" / "interactive-anatomy.md"
INDEX = ROOT / "docs" / "INDEX.md"
SOURCE_INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def _ledger() -> str:
    return _text().split("## Evidence Ledger", 1)[1].split("## Proof", 1)[0]


def test_hover_card_anatomy_is_shipped_contract() -> None:
    text = _text()
    assert "**Status:** shipped contract" in text
    assert "Import from `chirpui/hover_card.html`:" in text
    assert "`stable` rendered macro contract" in text


def test_hover_card_anatomy_covers_delay_focus_and_motion() -> None:
    text = " ".join(_text().split())
    for signal in [
        "Pointer enter on the root or content schedules open after `openDelay`",
        "Escape dismisses immediately through `dismiss()`",
        "prefers-reduced-motion: reduce",
        "menuAlignment()",
    ]:
        assert signal in text


def test_hover_card_ledger_matches_interactive_anatomy_fields() -> None:
    design_ledger = DESIGN.read_text(encoding="utf-8").split("## Evidence Ledger", 1)[1]
    hover_ledger = _ledger()

    fields = [
        line.split("|")[1].strip()
        for line in design_ledger.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required answer" not in line
    ]

    assert fields
    for field in fields:
        assert f"| {field} |" in hover_ledger


def test_hover_card_anatomy_is_indexed_for_agents() -> None:
    index = INDEX.read_text(encoding="utf-8")
    inventory = SOURCE_INVENTORY.read_text(encoding="utf-8")
    assert "components/hover-card-anatomy.md" in index
    assert "Shipped hover card anatomy" in index
    assert "docs/components/hover-card-anatomy.md" in inventory
