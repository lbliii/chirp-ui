from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "docs" / "REFERENCE-IMPLEMENTATION-PLAYBOOK.md"
INDEX = ROOT / "docs" / "INDEX.md"
REFERENCE_INDEX = ROOT / "docs" / "reference-implementations" / "README.md"
PROOF_ANALYSIS = ROOT / "docs" / "reference-implementations" / "PROOF-ANALYSIS.md"
PAGE_ACTIONS = ROOT / "docs" / "reference-implementations" / "PAGE-ACTIONS-AI-REFERENCE.md"
LINKED_NAV = ROOT / "docs" / "reference-implementations" / "LINKED-NAV-CATALOG-REFERENCE.md"
COMPACT_HEADER = ROOT / "docs" / "reference-implementations" / "COMPACT-HEADER-REFERENCE.md"
SHELL_RESPONSE = ROOT / "docs" / "reference-implementations" / "SHELL-RESPONSE-REFERENCE.md"
DENSE_REFERENCE = (
    ROOT / "docs" / "reference-implementations" / "DENSE-REFERENCE-DATA-REFERENCE.md"
)
AGENT_DISCOVERY = ROOT / "docs" / "reference-implementations" / "AGENT-DISCOVERY-REFERENCE.md"


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
    text = INDEX.read_text(encoding="utf-8")

    assert "[REFERENCE-IMPLEMENTATION-PLAYBOOK.md](REFERENCE-IMPLEMENTATION-PLAYBOOK.md)" in text
    assert "[reference-implementations/README.md](reference-implementations/README.md)" in text


def test_reference_implementation_index_links_all_briefs() -> None:
    text = REFERENCE_INDEX.read_text(encoding="utf-8")

    for brief in [
        "PROOF-ANALYSIS.md",
        "PAGE-ACTIONS-AI-REFERENCE.md",
        "LINKED-NAV-CATALOG-REFERENCE.md",
        "COMPACT-HEADER-REFERENCE.md",
        "SHELL-RESPONSE-REFERENCE.md",
        "DENSE-REFERENCE-DATA-REFERENCE.md",
        "AGENT-DISCOVERY-REFERENCE.md",
    ]:
        assert f"[{brief}]({brief})" in text

    for boundary in [
        "They are not public API plans.",
        "Use [PROOF-ANALYSIS.md](PROOF-ANALYSIS.md)",
        "Do not add public APIs from a reference brief.",
        "Do not count market research as promotion proof.",
        "Do not count Bengal as the second independent reference.",
    ]:
        assert boundary in text


def test_reference_proof_analysis_keeps_public_api_closed() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")

    for decision in [
        "Status: active proof-analysis ledger",
        "not a public API plan",
        "Existing primitives working in one private fixture means recipe guidance",
        "Promotion requires two independent scenario-complete references",
        "Response-helper promotion also requires owner clarity",
    ]:
        assert decision in text

    for candidate in [
        "Page actions",
        "Linked navigation",
        "Compact headers",
        "Shell response/OOB",
        "Dense reference/data pages",
        "Agent discovery",
    ]:
        assert f"| {candidate} |" in text

    for boundary in [
        "No `page_actions()` macro.",
        "No new `nav_tree` parameters",
        "No `compact_page_header`",
        "No visual shell macro",
        "No data-grid engine",
        "No manifest schema changes",
    ]:
        assert boundary in text


def test_reference_proof_analysis_records_dense_reference_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Dense Reference/Data Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "/dense-reference-data-reference",
        "tests/browser/test_dense_reference_data_reference.py",
        "`resource_index`, `resource_card`, `filter_rail`",
        "`table`, `params_table`, `card`, `badge`, and",
        "Long module, member, and parameter names stay inside the document",
        "320,",
        "768,",
        "1280 widths",
        "Filter counts currently read like navigation badges",
        "Copyable anchors and route-local reference actions were not exercised",
    ]:
        assert proof in section

    for decision in [
        "keep dense reference/data pages recipe-first",
        "evidence against immediate data-grid",
        "virtualized table",
        "reference-page macro",
        "JavaScript layout runtime",
        "another independent dense reference if a specific gap repeats",
    ]:
        assert decision in normalized


def test_reference_proof_analysis_records_agent_discovery_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Agent Discovery Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "tests/test_find_cli.py",
        "docs/AGENT-SOURCE-INVENTORY.md",
        "docs/AGENT-SOURCE-MAP.md",
        "`python -m chirp_ui find --details`",
        "`python -m chirp_ui find --role=pattern --details`",
        "`build_manifest()`",
        "component name, category, maturity, authoring",
        "`page_header`",
        "`page_hero`",
        "`resource-index`",
        "`filter-rail`",
        "copyable-curated snippets",
    ]:
        assert proof in section

    for boundary in [
        "Unpromoted proposal names such as `page-actions`",
        "`compact-page-header`",
        "`reference-page`",
        "`data-grid` are absent",
        "keep the manifest schema and descriptor fields closed",
        "without a copied-source workflow",
        "new CLI command",
        "MCP/server tool",
        "manifest expansion",
        "schema change should wait for repeated tasks",
    ]:
        assert boundary in normalized


def test_reference_proof_analysis_records_page_actions_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Page Actions Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "/page-actions-candidate",
        "tests/browser/test_page_actions_candidate.py",
        "`page_header`, `page_hero`, `dropdown_menu`",
        "`share_menu`, `action_bar`, and `copy_btn`",
        "Title-adjacent actions fit inside",
        "copy URL, open LLM text, copy known prompt text",
        "external assistant handoff commands",
        "Long command labels stay inside the dropdown",
        "Copy feedback for known text works",
    ]:
        assert proof in normalized

    for decision in [
        "Ownership is split",
        "canonical URL, prompt text, AI handoff",
        "did not exercise fetched LLM text",
        "not a semantic AI handoff contract",
        "keep page actions in investigation",
        "blocks an immediate `page_actions()` macro",
        "descriptor, CSS, manifest",
        "second non-Bengal reference",
        "title-adjacent URL/LLM/AI command ownership gap",
    ]:
        assert decision in normalized


def test_reference_proof_analysis_records_linked_navigation_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Linked Navigation Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "/linked-nav-candidate",
        "tests/browser/test_linked_nav_candidate.py",
        "`sidebar`, `sidebar_section`, `sidebar_link`",
        '`nav_tree(branch_mode="linked")`',
        "`drawer`, and `drawer_trigger`",
        "Parent branches render as route anchors",
        "children remain server-owned",
        "`open=true`",
        "Active child state, badges/counts, no-href groups",
        "Drawer fallback opens, closes with Escape",
    ]:
        assert proof in normalized

    for decision in [
        "Active-descendant parent emphasis is still a recipe convention",
        "Counts are visually useful",
        "structured navigation metadata contract",
        "Sidebar-to-drawer fallback requires app-owned duplication",
        "keep linked navigation as recipe/browser-proofed composition",
        "block new `nav_tree` parameters",
        "`docs_sidebar`",
        "`catalog_sidebar`",
        "`docs_shell`",
        "ARIA tree claims",
        "same active-descendant/count/fallback gap repeats",
    ]:
        assert decision in normalized


def test_reference_proof_analysis_records_compact_header_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Compact Header Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "/compact-header-candidate",
        "tests/browser/test_compact_header_candidate.py",
        '`page_header(variant="compact")`',
        '`page_hero(variant="minimal")`',
        "`search_header`, `entity_header`",
        "`document_header`, and `route_tabs`",
        "dense titles, subtitles, metadata, actions",
        "Filled `page_hero` optional regions remain available",
        "Empty `page_hero` optional regions",
        "Route tabs stay link-native",
    ]:
        assert proof in normalized

    for decision in [
        "choice between `page_header`, `page_hero`, `search_header`",
        "under-documented for dense docs and reference pages",
        "Empty optional-region behavior is still a contract to clarify",
        "did not prove a second independent compact docs/reference/catalog",
        "keep compact headers recipe-first",
        "blocks `compact_page_header`",
        "`docs_header`",
        "`catalog_header`",
        "new `page_hero` parameters",
        "slot changes",
        "generated options",
        "header-choice guidance",
    ]:
        assert decision in normalized


def test_reference_proof_analysis_records_shell_response_decision() -> None:
    text = PROOF_ANALYSIS.read_text(encoding="utf-8")
    section = text.split("## Shell Response/OOB Analysis", 1)[1]
    normalized = " ".join(section.split())

    for proof in [
        "tests/test_shell_response_targets.py",
        "tests/browser/test_consumer_shell_actions_oob.py",
        "`HX-Target` branching",
        "`shell_outlet_attrs`",
        "`route_tabs`",
        "shell-actions OOB replacement",
        "filesystem `mount_pages()` comparison",
        "Normal requests, `HX-Request` without target",
        "`HX-Target: main`",
        "`HX-Target: page-root`",
        "Workspace and admin route families",
        "boosted shell navigation",
    ]:
        assert proof in normalized

    for decision in [
        "repeat target classification and shell OOB inclusion decisions",
        "Chirp routing, Chirp UI, or app-local recipe helpers",
        "response ownership, not visual shell composition",
        "keep shell response/OOB route-local and recipe-first",
        "blocks a public `chirp_ui` helper",
        "visual shell macro",
        "new HTMX protocol",
        "third independent hand-written route family outside `mount_pages()`",
        "owner decision before implementation",
    ]:
        assert decision in normalized


def test_reference_implementation_index_tracks_current_proof_routes() -> None:
    text = REFERENCE_INDEX.read_text(encoding="utf-8")

    for route_or_surface in [
        "/page-actions-candidate",
        "/linked-nav-candidate",
        "/compact-header-candidate",
        "/dense-reference-data-reference",
        "Consumer workspace/admin route families",
        "`python -m chirp_ui find --details`",
    ]:
        assert route_or_surface in text

    for proof_file in [
        "tests/browser/test_page_actions_candidate.py",
        "tests/browser/test_linked_nav_candidate.py",
        "tests/browser/test_compact_header_candidate.py",
        "tests/browser/test_dense_reference_data_reference.py",
        "tests/test_shell_response_targets.py",
        "tests/browser/test_consumer_shell_actions_oob.py",
        "tests/test_find_cli.py",
    ]:
        assert proof_file in text

    for implementation_marker in [
        'data-reference-implementation="page-actions-ai"',
        'data-reference-implementation="linked-nav-catalog"',
        'data-reference-implementation="compact-header-reference"',
        'data-reference-implementation="dense-reference-data"',
        'data-public-api="false"',
    ]:
        assert implementation_marker in text


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


def test_agent_discovery_reference_brief_keeps_manifest_schema_closed() -> None:
    text = AGENT_DISCOVERY.read_text(encoding="utf-8")

    for surface in [
        "`python -m chirp_ui find --details`",
        "`python -m chirp_ui find --maturity=experimental --details`",
        "`python -m chirp_ui find --role=pattern --details`",
        "`build_manifest()`",
        "`docs/AGENT-SOURCE-INVENTORY.md`",
        "`docs/AGENT-SOURCE-MAP.md`",
        "`docs/REGISTRY-DISCOVERY.md`",
        "`docs/COMPONENT-OPTIONS.md`",
    ]:
        assert surface in text

    for proof in [
        "Search by job, category, maturity, authoring, and role",
        "Details expose macro, template, runtime requirements, slots",
        "source-only versus copyable-curated",
        "not presented as preferred stable APIs",
        "valid existing primitive or a documented not-now boundary",
    ]:
        assert proof in text

    for boundary in [
        "does not authorize manifest schema changes",
        "new descriptor fields",
        "new CLI commands",
        "MCP/server tooling",
        "public extension protocols",
        "generated component option changes",
        "copied-source installation",
    ]:
        assert boundary in text
