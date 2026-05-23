from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "docs" / "REFERENCE-IMPLEMENTATION-PLAYBOOK.md"
INDEX = ROOT / "docs" / "INDEX.md"
PAGE_ACTIONS = ROOT / "docs" / "reference-implementations" / "PAGE-ACTIONS-AI-REFERENCE.md"
LINKED_NAV = ROOT / "docs" / "reference-implementations" / "LINKED-NAV-CATALOG-REFERENCE.md"
COMPACT_HEADER = ROOT / "docs" / "reference-implementations" / "COMPACT-HEADER-REFERENCE.md"
SHELL_RESPONSE = ROOT / "docs" / "reference-implementations" / "SHELL-RESPONSE-REFERENCE.md"
DENSE_REFERENCE = (
    ROOT / "docs" / "reference-implementations" / "DENSE-REFERENCE-DATA-REFERENCE.md"
)


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
        "manifest",
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
        "manifest",
        "`docs_sidebar`",
        "`catalog_sidebar`",
        "`docs_shell`",
        "ARIA tree claims",
    ]:
        assert boundary in text


def test_compact_header_reference_brief_blocks_premature_header_api() -> None:
    text = COMPACT_HEADER.read_text(encoding="utf-8")

    for primitive in [
        '`page_header(variant="compact")`',
        '`page_hero(variant="minimal")`',
        "`search_header`",
        "`entity_header`",
        "`document_header`",
        "`route_tabs`",
    ]:
        assert primitive in text

    for proof in [
        "Long titles and action labels wrap without overlap",
        "Empty `page_hero` optional regions collapse",
        "Route tabs stay near page identity",
        "Browser proof covers phone, tablet, and desktop widths",
        "No document-level horizontal overflow",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize `compact_page_header`",
        "`docs_header`",
        "`catalog_header`",
        "`docs_shell`",
        "new `page_hero` parameters",
        "slot changes",
        "markup changes",
        "CSS",
        "descriptor changes",
        "manifest updates",
    ]:
        assert boundary in text


def test_shell_response_reference_brief_keeps_problem_non_visual() -> None:
    text = SHELL_RESPONSE.read_text(encoding="utf-8")

    for primitive in [
        "`HX-Target` branching",
        "`shell_outlet_attrs`",
        "`route_tabs`",
        "`fragment_island`",
        "`safe_region`",
        "shell actions OOB replacement",
        "`mount_pages()`",
    ]:
        assert primitive in text

    for proof in [
        "No `HX-Request` returns the full page response",
        "`HX-Request` without `HX-Target`",
        "`HX-Target: main` returns shell-owned content",
        "`HX-Target: page-root` returns only page-root",
        "Local fragment targets return local content",
        "singleton `#main`, `#page-content`, and `#page-root`",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize a public `chirp_ui` helper",
        "Chirp routing API",
        "visual shell macro",
        "component descriptor",
        "emitted classes",
        "CSS",
        "manifest",
        "new HTMX protocol",
    ]:
        assert boundary in text


def test_dense_reference_data_brief_avoids_grid_engine_jump() -> None:
    text = DENSE_REFERENCE.read_text(encoding="utf-8")

    for primitive in [
        "`resource_index`",
        "`resource_card`",
        "`filter_rail`",
        "`filter_bar`",
        "`search_header`",
        "`table`",
        "`params_table`",
        "`card`",
        "`badge`",
        "`callout`",
    ]:
        assert primitive in text

    for proof in [
        "Filter and search controls stay reachable",
        "Long module, function, parameter, and type names wrap without overflow",
        "Empty, loading, and error states",
        "without introducing a heavy grid engine",
        "Browser proof covers 320, 768, and 1280 widths",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize a data-grid engine",
        "virtualized table",
        "reference-page macro",
        "new filter-count API",
        "emitted classes",
        "CSS",
        "descriptor changes",
        "manifest updates",
        "JavaScript layout runtime",
    ]:
        assert boundary in text
