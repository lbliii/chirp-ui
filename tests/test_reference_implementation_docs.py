from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "docs" / "REFERENCE-IMPLEMENTATION-PLAYBOOK.md"
INDEX = ROOT / "docs" / "INDEX.md"


def test_reference_implementation_playbook_defines_evidence_ladder() -> None:
    text = PLAYBOOK.read_text(encoding="utf-8")

    assert "does not authorize public macro/API changes" in text
    for level in [
        "Market proxy",
        "Recipe proof",
        "Private fixture",
        "Scenario-complete reference",
        "Promotion candidate",
    ]:
        assert f"| {level} |" in text

    for boundary in [
        "Requirements input only.",
        "Regression proof, not enough alone.",
        "Qualifying implementation evidence.",
        "Stop and ask for public API/design approval.",
    ]:
        assert boundary in text


def test_reference_implementation_playbook_names_priority_candidates() -> None:
    text = PLAYBOOK.read_text(encoding="utf-8")

    for candidate in [
        "Page actions",
        "Linked navigation",
        "Compact header",
        "Shell response/OOB",
        "Dense reference/data pages",
        "Agent discovery",
    ]:
        assert f"| {candidate} |" in text

    for primitive in [
        "`page_header`, `page_hero`, `dropdown_menu`, `share_menu`, `action_bar`, `copy_btn`",
        "`sidebar`, `sidebar_section`, `sidebar_link`, `nav_tree(branch_mode=\"linked\")`",
        "`page_header(variant=\"compact\")`, `page_hero(variant=\"minimal\")`",
        "`resource_index`, `resource_card`, `filter_rail`, `filter_bar`, `table`",
        "`python -m chirp_ui find --details`",
    ]:
        assert primitive in text


def test_reference_implementation_playbook_is_indexed() -> None:
    assert "[REFERENCE-IMPLEMENTATION-PLAYBOOK.md](REFERENCE-IMPLEMENTATION-PLAYBOOK.md)" in (
        INDEX.read_text(encoding="utf-8")
    )
