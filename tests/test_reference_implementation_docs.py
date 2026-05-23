from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "docs" / "REFERENCE-IMPLEMENTATION-PLAYBOOK.md"
INDEX = ROOT / "docs" / "INDEX.md"
PAGE_ACTIONS = ROOT / "docs" / "reference-implementations" / "PAGE-ACTIONS-AI-REFERENCE.md"
LINKED_NAV = ROOT / "docs" / "reference-implementations" / "LINKED-NAV-CATALOG-REFERENCE.md"


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


def test_page_actions_reference_brief_keeps_api_unauthorized() -> None:
    text = PAGE_ACTIONS.read_text(encoding="utf-8")

    for primitive in [
        "`page_header` actions",
        "`page_hero` actions",
        "`dropdown_menu`",
        "`share_menu`",
        "`action_bar`",
        "`copy_btn`",
    ]:
        assert primitive in text

    for proof in [
        "Browser proof at 320, 390, 768, and 1024 widths",
        "Long command labels stay contained",
        "Copy feedback works for known text",
        "External assistant links use safe external-link attributes",
        "No Bengal `.chirp-theme-*` selectors are used",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize `page_actions()`",
        "copy/fetch runtime helpers",
        "descriptor changes",
        "CSS",
        "manifest updates",
        "generated component",
        "public page-actions API",
    ]:
        assert boundary in text


def test_linked_nav_reference_brief_forces_existing_primitives_first() -> None:
    text = LINKED_NAV.read_text(encoding="utf-8")

    for primitive in [
        "`sidebar`",
        "`sidebar_section`",
        "`sidebar_link`",
        "`nav_tree(branch_mode=\"linked\")`",
        "`drawer`",
        "`drawer_trigger`",
    ]:
        assert primitive in text

    for proof in [
        "Parent branches render as anchors",
        "Closed branch children are omitted",
        "Active child links render current-page state",
        "Count badges are visible",
        "Long labels stay contained",
        "Drawer opens, closes with Escape",
        "no document-level horizontal overflow at 320px",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize new `nav_tree` parameters",
        "sidebar branch macros",
        "emitted classes",
        "CSS",
        "manifest updates",
        "`docs_sidebar`",
        "`catalog_sidebar`",
        "`docs_shell`",
        "ARIA tree claims",
    ]:
        assert boundary in text
