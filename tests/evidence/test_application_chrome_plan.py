from tests.helpers import REPO_ROOT

PLAN = REPO_ROOT / "docs" / "plans" / "PLAN-application-chrome-system.md"


def test_application_chrome_plan_has_composite_evaluation_docket() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "### 5. Composite Evaluation Docket" in text
    assert "Evaluation docket:" in text
    for candidate in ["`object_header`", "`chrome_frame`", "`workspace_shell`"]:
        assert candidate in text

    for field in [
        "Evidence Required",
        "Accept If",
        "Reject If",
        "Collateral If Accepted",
        "Existing primitives tried:",
        "Missing contract:",
        "Not-now spillover:",
    ]:
        assert field in text


def test_application_chrome_plan_keeps_recipe_first_boundary() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "This is a system plan, not a request to add `application_chrome()`" in text
    assert "No `application_chrome()`" in text
    assert "two independent reference implementations" in text
    assert "utility classes for density, hiding, spacing, alignment, or overflow" in text


def test_application_chrome_plan_has_release_readiness_ledger() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "## Release Readiness Ledger" in text
    for slice_name in [
        "Docs bridge",
        "Rail-to-tray recipe",
        "Chrome gauntlet",
        "Rhythm audit",
        "Bengal parity",
        "Composite promotion",
    ]:
        assert slice_name in text

    for proof in [
        "`uv run poe build-docs-check`",
        "browser proof at 320, 390, 768, 1024, and 1280",
        "command focus, route-tab scroll, badges, and overflow",
        "full component contract proof",
        "remaining browser/environment gap",
    ]:
        assert proof in text


def test_application_chrome_plan_distinguishes_recipe_proof_from_reference_implementations() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")

    assert "Current evidence log:" in text
    for evidence in [
        "Dense object chrome showcase recipes",
        "Rail-to-drawer showcase recipe and browser fixture",
        "Application chrome gauntlet families",
        "Bengal docs chrome",
    ]:
        assert evidence in text

    assert "Counts As Reference Implementation?" in text
    assert "not enough for `application_chrome`" in text
    assert "not enough for a stable shell API" in text
    assert "Open implementation evidence still required before composite work" in text
    assert "one production or copyable filesystem-routed Chirp app" in text
    assert "one additional app or packaged integration" in text


def test_application_chrome_plan_synthesizes_anatomy_ledgers() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "## Evidence-Ledger Synthesis: Shell Primitive Readiness" in text
    assert "They do not authorize a shell macro by themselves" in text
    assert "not ready for a generic `application_chrome()`" in text

    for ledger in [
        "[MODAL-ANATOMY.md](../components/modal-anatomy.md)",
        "[DROPDOWN-ANATOMY.md](../components/dropdown-anatomy.md)",
        "[DRAWER-TRAY-ANATOMY.md](../components/drawer-tray-anatomy.md)",
        "[TABS-ANATOMY.md](../components/tabs-anatomy.md)",
        "[BENGAL-THEME-ANATOMY.md](../theming/bengal-theme-anatomy.md)",
    ]:
        assert ledger in text

    for boundary in [
        "Native dialogs and store-backed overlays intentionally have different event models",
        "Menu/split roving-arrow navigation is not published",
        "app-shell topbar hit-target anomaly",
        "Route tabs are navigation, not ARIA tab widgets",
        "Theme selectors are not registry APIs",
    ]:
        assert boundary in text


def test_application_chrome_plan_identifies_narrow_next_candidates() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Cross-ledger primitive candidates:", 1)[1].split(
        "Promotion gate for the next implementation slice:", 1
    )[0]

    for candidate in [
        "Page actions primitive",
        "Linked nav-tree/sidebar semantics",
        "Shell response/OOB helper",
        "Compact page header",
        "Generic application shell macro",
        "Catalog/docs shell macro",
    ]:
        assert f"| {candidate} |" in section

    for decision in [
        "Candidate for next investigation",
        "Candidate for recipe/helper evaluation",
        "Deferred",
        "the repeated pain is response ownership and smaller contracts",
        "product-specific information architecture",
    ]:
        assert decision in section


def test_application_chrome_plan_has_next_slice_promotion_gate() -> None:
    text = PLAN.read_text(encoding="utf-8")
    gate = text.split("Promotion gate for the next implementation slice:", 1)[1].split(
        "## Linked Nav-Tree/Sidebar Semantics Investigation", 1
    )[0]

    for requirement in [
        "choose one narrow candidate, not a mega-shell",
        "name the reference implementations and existing primitives tried",
        "write the registry/API contract before touching descriptors or macros",
        "rendered anatomy, escaping, keyboard/focus, HTMX/Alpine boundaries",
        "docs/examples/generated outputs only if a public API is actually promoted",
    ]:
        assert requirement in gate


def test_application_chrome_plan_has_linked_nav_investigation_boundary() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Linked Nav-Tree/Sidebar Semantics Investigation", 1)[1].split(
        "## Shell Response/OOB Helper Investigation", 1
    )[0]

    assert "Status: active investigation inside this plan, no public API authorized." in section
    assert "does not authorize new `nav_tree` parameters" in section
    assert "or a docs-shell macro" in section

    for forbidden in [
        "new sidebar macros",
        "emitted classes",
        "CSS",
        "manifest changes",
        "generated",
        "docs",
    ]:
        assert forbidden in section

    for surface in [
        "`sidebar` / `sidebar_section` / `sidebar_link`",
        '`nav_tree(branch_mode="disclosure")`',
        '`nav_tree(branch_mode="linked")`',
        "Bengal docs nav partials",
        "Rail-to-drawer recipe",
    ]:
        assert f"| {surface} |" in section


def test_application_chrome_plan_linked_nav_reference_implementation_scan_is_not_enough() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Linked Nav-Tree/Sidebar Semantics Investigation", 1)[1].split(
        "### Linked Nav Reference Evidence Search", 1
    )[0]

    for evidence in [
        "Bengal docs navigation",
        "Rail-to-drawer recipe",
        "Knowledge workspace recipe",
        "Filesystem app-shell fixture",
        "Generic docs recipes",
    ]:
        assert f"| {evidence} |" in section

    for boundary in [
        "Partial | Packaged-theme pressure",
        "Partial | Good responsive proof for existing primitives",
        "No | Recipe evidence only",
        "No | Proves sidebar shell navigation, not linked branch hierarchy",
        "No | Prose guidance is not implementation repetition",
    ]:
        assert boundary in section


def test_application_chrome_plan_linked_nav_real_reference_implementation_search_keeps_api_closed() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Linked Nav Reference Evidence Search", 1)[1].split(
        "Candidate contract questions:", 1
    )[0]

    assert "Search date: 2026-05-23" in section
    assert "no second qualifying non-Bengal linked-branch reference implementation" in section
    assert "remain in" in section
    assert "investigation" in section

    for forbidden in [
        "`nav_tree` parameters",
        "sidebar branch macros",
        "CSS",
        "manifest",
        "generated docs",
        "docs-shell",
    ]:
        assert forbidden in section

    for scope in [
        "`docs/`",
        "`examples/`",
        "`tests/browser/templates/`",
        "`tests/browser/app.py`",
        "`src/chirp_ui/templates/`",
        "excluded Bengal theme templates",
    ]:
        assert scope in section


def test_application_chrome_plan_linked_nav_search_names_qualifying_criteria() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Linked Nav Reference Evidence Search", 1)[1].split(
        "Search findings:", 1
    )[0]

    for criterion in [
        "scenario-complete app, packaged integration, or",
        "`sidebar`, `sidebar_section`, `sidebar_link`, and",
        '`nav_tree(branch_mode="linked")`',
        "parent",
        "route links",
        "server-owned open state",
        "active descendants",
        "child rows",
        "compact branch/leaf rhythm",
        "badge/count metadata",
        "mobile fallback",
        "without using Bengal selectors",
    ]:
        assert criterion in section


def test_application_chrome_plan_linked_nav_search_records_near_misses() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Linked Nav Reference Evidence Search", 1)[1].split(
        "Decision after search:", 1
    )[0]

    for candidate in [
        "Bengal docs navigation",
        "Rail-to-drawer recipe",
        "Application chrome gauntlet",
        "General gauntlet linkability rooms",
        "Component showcase navigation page",
        "Filesystem/app chrome fixtures",
        "Forum/product/media pattern docs",
    ]:
        assert f"| {candidate} |" in section

    for reason in [
        "Original pressure only",
        "Recipe/fixture evidence",
        "Browser stress evidence only",
        "Component stress proof",
        "Showcase examples are not implementation repetition",
        "not hierarchical linked branch semantics",
        "Prose/pattern evidence only",
    ]:
        assert reason in section


def test_application_chrome_plan_linked_nav_search_routes_next_slice_to_private_fixture() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Decision after search:", 1)[1].split("### Private Linked Nav Fixture", 1)[
        0
    ]

    for decision in [
        "Keep linked nav-tree/sidebar semantics unauthorized",
        '`nav_tree(branch_mode="linked")` as the current',
        "Do not add `docs_sidebar`, `catalog_sidebar`, sidebar branch macros",
        "new",
        "branch metadata",
        "scenario-complete first-party reference",
        '`sidebar` and `nav_tree(branch_mode="linked")`',
        "active descendants",
        "child-count metadata",
        "compact",
        "mobile fallback",
    ]:
        assert decision in section


def test_application_chrome_plan_records_private_linked_nav_fixture_without_api_promotion() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Private Linked Nav Fixture", 1)[1].split(
        "Candidate contract questions:", 1
    )[0]

    assert "Status: implemented as test evidence only, no public API authorized." in section
    for fixture_ref in [
        "route: `/linked-nav-candidate`",
        "tests/browser/templates/linked_nav_candidate_page.html",
        "tests/browser/test_linked_nav_candidate.py",
    ]:
        assert fixture_ref in section

    for proof in [
        "`sidebar`, `sidebar_section`, and `sidebar_link`",
        '`nav_tree(branch_mode="linked")`',
        "`drawer` and `drawer_trigger`",
        "Linked branch parents render as route links",
        "not native disclosure summaries",
        "server marks a branch `open=true`",
        "closed",
        "children are omitted",
        "Active child links",
        "no-href groups",
        "branch badges",
        "long child labels",
        "phone drawer fallback",
        "focus",
        "return",
        "without document-level horizontal",
        "overflow",
    ]:
        assert proof in section

    for boundary in [
        "does not authorize new `nav_tree` parameters",
        "sidebar branch macros",
        "emitted classes",
        "CSS",
        "manifest changes",
        "generated docs",
        "docs-shell",
        "does not prove that active descendants",
        "does not count as qualifying implementation evidence",
    ]:
        assert boundary in section


def test_application_chrome_plan_private_linked_nav_fixture_decision_keeps_next_slice_analytical() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Fixture decision:", 1)[1].split("### Linked Nav Fixture Analysis", 1)[0]

    for decision in [
        "Do existing primitives render the linked-sidebar candidate shape?",
        "Yes, as a private fixture.",
        "Is there enough evidence for public API promotion?",
        "No.",
        "What remains to analyze?",
        "active descendants, count metadata, compact rhythm, and mobile fallback",
        "What would unlock promotion?",
        "A second independent reference implementation that repeats the same linked-branch gap",
    ]:
        assert decision in section


def test_application_chrome_plan_linked_nav_fixture_analysis_classifies_gap_without_promotion() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Linked Nav Fixture Analysis", 1)[1].split(
        "Candidate contract questions:", 1
    )[0]

    assert "Analysis date: 2026-05-23" in section
    assert "keep linked nav-tree/sidebar semantics in investigation" in section
    assert "does not prove a public `nav_tree` or `sidebar` API gap" in section

    for behavior in [
        "Sidebar integration",
        "Branch parent links",
        "Active child state",
        "Count metadata",
        "No-href grouping",
        "Long labels and overflow",
        "Mobile fallback",
    ]:
        assert f"| {behavior} |" in section

    for outcome in [
        "`sidebar`, `sidebar_section`, and `sidebar_link` can host",
        "Linked branch parents render as anchors",
        'Active children render `aria-current="page"`',
        "Branch badges render visible counts",
        "Branches without `href` render as text",
        "Long child labels stay contained",
        "phone-width containment and a phone drawer fallback",
    ]:
        assert outcome in section

    for classification in [
        "Real gap: Chirp UI does not automatically derive active-descendant",
        "richer child-count metadata",
        "mobile fallback policy",
        "Not yet a promotion gap",
        "private fixture is still artificial",
        "existing composition renders the candidate without new API or CSS",
    ]:
        assert classification in section


def test_application_chrome_plan_linked_nav_fixture_analysis_next_slices_stay_private_until_second_reference_implementation() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Next-slice options from this analysis:", 1)[1].split(
        "### Private Linked Nav Mobile Fallback Stress", 1
    )[0]

    for slice_name in [
        "Private mobile fallback stress",
        "Fixture gap notes",
        "Reference evidence research",
        "Public API proposal",
    ]:
        assert f"| {slice_name} |" in section

    for boundary in [
        "Closed; private evidence only.",
        "Low; docs/test only.",
        "Low; evidence gathering.",
        "High; stop and ask first.",
        "Done: same linked tree now composes in a phone drawer fallback",
    ]:
        assert boundary in section


def test_application_chrome_plan_records_private_linked_nav_mobile_fallback_stress() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Private Linked Nav Mobile Fallback Stress", 1)[1].split(
        "Candidate contract questions:", 1
    )[0]
    normalized = " ".join(section.split())

    assert "Status: implemented as private browser evidence, no public API authorized." in section
    for fixture_ref in [
        "tests/browser/templates/linked_nav_candidate_page.html",
        "tests/browser/test_linked_nav_candidate.py",
        "`drawer` and",
        "`drawer_trigger`",
    ]:
        assert fixture_ref in section

    for proof in [
        "hide the persistent sidebar at phone width",
        "drawer trigger",
        "without adding a shell/sidebar macro",
        '`nav_tree(branch_mode="linked")` keeps the same linked branch behavior',
        "branch parents remain anchors",
        "no `<summary>` disclosure",
        'active children keep `aria-current="page"`',
        "closed branch",
        "children remain omitted",
        "inside the open drawer at 320px",
        "without",
        "document-level horizontal overflow",
        "closes with Escape",
        "returns focus to the trigger",
    ]:
        assert proof in normalized

    for decision in [
        "closes the private mobile fallback stress slice",
        "weakens the case for an immediate public linked-sidebar primitive",
        "remaining gap is policy and repetition",
        "another independent reference implementation must repeat",
        "before promotion is justified",
    ]:
        assert decision in normalized


def test_application_chrome_plan_records_private_linked_nav_gap_notes() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Private Linked Nav Gap Notes", 1)[1].split(
        "Candidate contract questions:", 1
    )[0]
    normalized = " ".join(section.split())

    assert "Status: recorded as investigation notes only, no public API authorized." in section
    assert "desktop sidebar and phone drawer contexts" in normalized

    for gap in [
        "Active-descendant parent state",
        "Rich count metadata",
        "Compact branch/leaf rhythm",
        "Responsive fallback policy",
    ]:
        assert f"| {gap} |" in section

    for boundary in [
        "Do not add `active_descendant` until a second reference implementation",
        "Do not add `child_count` or `child_count_label`",
        "Treat rhythm as CSS/recipe evidence, not a macro parameter.",
        "Do not add a shell-owned responsive policy",
        "Start with `sidebar`, `sidebar_section`, `sidebar_link`,",
        '`nav_tree(branch_mode="linked")`, `drawer`, and `drawer_trigger`',
        "Mark branches `open=true` server-side",
        "Use badges for visible counts first",
        "Record the exact repeated boilerplate before proposing a public primitive.",
    ]:
        assert boundary in normalized


def test_application_chrome_plan_linked_nav_promotion_gate_and_not_now() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Linked Nav-Tree/Sidebar Semantics Investigation", 1)[1].split(
        "## Shell Response/OOB Helper Investigation", 1
    )[0]

    gate = section.split("Promotion gate:", 1)[1].split("Not now:", 1)[0]
    for requirement in [
        "Bengal plus one additional independent reference implementation",
        "`sidebar`, `sidebar_section`,",
        '`sidebar_link`, and `nav_tree(branch_mode="linked")`',
        '`nav_tree(branch_mode="linked")`',
        "item schema, active/open semantics, ARIA",
        "badge/count behavior",
        "compact branch/leaf rhythm",
        "strict undefined",
        "phone drawer fallback",
        "descriptor/manifest impact",
    ]:
        assert requirement in gate

    not_now = section.split("Not now:", 1)[1]
    for boundary in [
        "Do not add a `docs_sidebar`, `catalog_sidebar`, or `docs_shell` macro.",
        "Do not move Bengal `.chirp-theme-docs-nav*` selectors into `chirpui-*`",
        "Do not add nav-tree descriptor/schema changes without a separate API plan.",
        "Do not make linked branch navigation an ARIA tree",
        "Do not count recipe prose as a reference implementation.",
    ]:
        assert boundary in not_now


def test_application_chrome_plan_has_shell_response_helper_investigation_boundary() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Shell Response/OOB Helper Investigation", 1)[1].split(
        "## Compact Page Header/Page Hero Investigation", 1
    )[0]

    assert "Status: active investigation inside this plan, no public API authorized." in section
    assert "not a visual shell problem" in section
    assert "response-shape" in section
    assert "selection across persistent shell navigation" in section
    assert "does not authorize a public `chirp_ui` helper" in section
    assert "or a new HTMX protocol" in section

    for forbidden in [
        "a shell macro",
        "new component descriptors",
        "emitted classes",
        "CSS",
        "manifest changes",
        "generated",
        "docs",
    ]:
        assert forbidden in section

    for surface in [
        "[SHELL-TABS-CONTRACT.md](../components/shell-tabs-contract.md) route-local helpers",
        "Filesystem mounted pages with `mount_pages()`",
        "`shell_outlet_attrs()` and shell OOB regions",
        "`route_tabs`",
        "`fragment_island` / `safe_region` patterns",
        "Workspace/admin route fixtures",
    ]:
        assert f"| {surface} |" in section


def test_application_chrome_plan_shell_response_reference_implementation_scan_routes_helper_to_chirp_not_visual_shell() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Shell Response/OOB Helper Investigation", 1)[1].split(
        "Promotion gate:", 1
    )[0]

    for evidence in [
        "Filesystem mounted app fixture",
        "Manual route references from Wave 1/Wave 2",
        "Workspace/admin browser fixtures",
        "Bengal docs chrome",
        "Published recipe prose",
    ]:
        assert f"| {evidence} |" in section

    for boundary in [
        "Covered | This path should prefer `mount_pages()`",
        "Partial | Repeated internal pressure",
        "Partial | Good regression evidence",
        "No | It proves theme shell pressure",
        "No | Prose guidance is necessary collateral",
    ]:
        assert boundary in section

    for question in [
        "Is the owner Chirp routing/framework, `chirp_ui`, or app-local recipe code?",
        "named around response ownership, not application",
        "return booleans, an enum, or a decision object",
        "`main`, `page-root`, `page-content-inner`, `chirp-shell-actions`",
        "no `HX-Request`, missing `HX-Target`, boosted shell navigation",
        "filesystem pages and manual routes share a contract",
    ]:
        assert question in section


def test_application_chrome_plan_shell_response_promotion_gate_and_not_now() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Shell Response/OOB Helper Investigation", 1)[1].split(
        "## Compact Page Header/Page Hero Investigation", 1
    )[0]

    gate = section.split("Promotion gate:", 1)[1].split("Not now:", 1)[0]
    for requirement in [
        "Three route families repeat the same branching",
        "outside filesystem mounted pages",
        "named around response ownership",
        "Chirp routing,",
        "`chirp_ui`,",
        "no `HX-Request`, missing `HX-Target`, `HX-Target: main`,",
        "`HX-Target: page-root`, local fragment targets, and OOB shell actions",
        "without",
        "changing template contracts",
        "no descriptor, manifest, CSS, generated options, or",
        "component docs change",
    ]:
        assert requirement in gate

    not_now = section.split("Not now:", 1)[1]
    for boundary in [
        "Do not add a public `chirp_ui` shell response helper from this plan slice.",
        "Do not add `application_chrome()`, `chrome_frame()`, or another visual macro",
        "Do not move routing decisions into component templates.",
        "Do not create a new HTMX convention",
        "Do not replace the filesystem mounted page-shell contract",
        "Do not count Bengal theme chrome as proof",
    ]:
        assert boundary in not_now


def test_application_chrome_plan_records_shell_response_route_local_gap_notes() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Shell Response Route-Local Gap Notes", 1)[1].split(
        "## Compact Page Header/Page Hero Investigation", 1
    )[0]
    normalized = " ".join(section.split())

    assert "Status: recorded as route-local evidence only, no public API authorized." in section

    for request_shape in [
        "normal full-page request",
        "`HX-Request` without `HX-Target`",
        "`HX-Target: main`",
        "`HX-Target: page-root`",
        "local target such as `page-content-inner`",
    ]:
        assert f"| {request_shape} |" in section

    for decision in [
        "Keep `_is_hx_target()` and `_include_shell_actions_oob()` as fixture-local",
        "documented [SHELL-TABS-CONTRACT.md](../components/shell-tabs-contract.md)",
        "Do not promote a public helper from two manual fixture route families",
        "close to Chirp routing/page composition",
        "third scenario-complete route reference",
        "Do not add descriptor, manifest, CSS, generated component options, or macro",
        "third hand-written route family",
        "outside `mount_pages()`",
        "repeats the same `HX-Target` branching and OOB",
    ]:
        assert decision in normalized


def test_application_chrome_plan_tracks_current_reference_proof_status() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Reference implementation proof status:", 1)[1].split(
        "Disqualifiers for promotion evidence:", 1
    )[0]

    for proof in [
        "/page-actions-candidate",
        "tests/browser/test_page_actions_candidate.py",
        "/linked-nav-candidate",
        "tests/browser/test_linked_nav_candidate.py",
        "/compact-header-candidate",
        "tests/browser/test_compact_header_candidate.py",
        "tests/test_shell_response_targets.py",
        "/dense-reference-data-reference",
        "tests/browser/test_dense_reference_data_reference.py",
        "tests/test_find_cli.py",
    ]:
        assert proof in section

    for boundary in [
        "No `page_actions()` macro",
        "No new `nav_tree` parameters",
        "No `compact_page_header`",
        "No visual shell macro",
        "No data-grid engine",
        "No manifest schema changes",
    ]:
        assert boundary in section


def test_application_chrome_plan_has_compact_header_investigation_boundary() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Compact Page Header/Page Hero Investigation", 1)[1].split(
        "## Promotion Readiness Queue", 1
    )[0]

    assert "Status: active investigation inside this plan, no public API authorized." in section
    assert "header anatomy and optional-region" in section
    assert "not a docs-shell problem" in section
    assert "does not authorize new `page_hero` parameters" in section
    assert "or a docs/catalog shell macro" in section

    for forbidden in [
        "a new compact",
        "slot changes",
        "emitted classes",
        "CSS",
        "manifest changes",
        "generated",
        "docs",
    ]:
        assert forbidden in section

    for surface in [
        '`page_header(variant="compact")`',
        '`page_hero(variant="minimal")`',
        "`search_header` / `resource_index`",
        "`document_header` / `entity_header`",
        "Bengal docs hero/header treatment",
        "Header relationship CSS/browser proof",
    ]:
        assert f"| {surface} |" in section


def test_application_chrome_plan_compact_header_reference_implementation_scan_is_not_enough() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Compact Page Header/Page Hero Investigation", 1)[1].split(
        "Promotion gate:", 1
    )[0]

    for evidence in [
        "Bengal docs/API/catalog pages",
        "Application chrome route fixtures",
        "Catalog/resource recipes",
        "Forum/media pattern pages",
        "Private compact-header candidate fixture",
        "Generated docs prose",
    ]:
        assert f"| {evidence} |" in section

    for boundary in [
        "Partial | Packaged-theme pressure",
        "No | Proves existing compact app headers",
        "Partial | Good dense-header evidence",
        "No | Pattern evidence is not repeated app pressure",
        "No | Artificial browser evidence",
        "No | Prose can guide the contract",
    ]:
        assert boundary in section

    for question in [
        "Should `page_hero` omit empty named-slot wrappers",
        "compact hero/header, an extension of",
        "Which optional regions are contractually meaningful",
        "Should page actions live in the header primitive",
        "semantic heading level, landmarks, breadcrumbs, and route tabs",
        "remains Bengal theme-specific",
    ]:
        assert question in section


def test_application_chrome_plan_compact_header_promotion_gate_and_not_now() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Compact Page Header/Page Hero Investigation", 1)[1].split(
        "## Promotion Readiness Queue", 1
    )[0]

    gate = section.split("Promotion gate:", 1)[1].split("Not now:", 1)[0]
    for requirement in [
        "Bengal plus one additional independent reference implementation",
        '`page_header(variant="compact")`',
        '`page_hero(variant="minimal")`',
        "`search_header`, and `entity_header`",
        "owned regions, heading semantics, optional slot",
        "action placement, metadata/footer behavior",
        "empty slots, filled eyebrow/actions/metadata/content/footer",
        "strict",
        "undefined",
        "descriptor/manifest parity",
        "long titles, long actions",
        "route-tab",
        "proximity",
        "generated component",
        "options",
    ]:
        assert requirement in gate

    not_now = section.split("Not now:", 1)[1]
    for boundary in [
        "Do not add a `compact_page_header`, `docs_header`, `catalog_header`, or",
        "Do not change `page_hero` markup, slot wrappers, descriptor metadata, or CSS",
        "Do not move Bengal `.chirp-theme-*` header selectors into `chirpui-*`",
        "Do not solve page actions by hiding them inside a generic hero contract",
        "Do not count recipe prose or visual preference as implementation repetition.",
    ]:
        assert boundary in not_now


def test_application_chrome_plan_records_private_compact_header_candidate_fixture() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Private Compact Header Candidate Fixture", 1)[1].split(
        "## Promotion Readiness Queue", 1
    )[0]
    normalized = " ".join(section.split())

    assert "Status: implemented as browser evidence only, no public API authorized." in section
    for fixture_ref in [
        "route: `/compact-header-candidate`",
        "tests/browser/templates/compact_header_candidate_page.html",
        "tests/browser/test_compact_header_candidate.py",
    ]:
        assert fixture_ref in section

    for primitive in [
        '`page_header(variant="compact")`',
        '`page_hero(variant="minimal")`',
        "`search_header`",
        "`entity_header`",
        "`document_header`",
    ]:
        assert primitive in section

    for proof in [
        "long title, subtitle, metadata, and page actions",
        "without document-level horizontal overflow",
        "phone, tablet, and desktop widths",
        "filled eyebrow, actions, metadata, content, and footer regions",
        "Empty `page_hero` eyebrow, actions, metadata, and footer wrappers collapse",
        "search-first, object-detail, and document-detail header needs",
        "without a new docs/catalog header macro",
    ]:
        assert proof in normalized

    for boundary in [
        "`page_hero` still emits its structural content wrapper",
        "does not count as a second scenario-complete compact-docs or compact-reference implementation",
        "separate public API/design plan",
        "Prefer better guidance for choosing",
        "Do not add `compact_page_header`, `docs_header`, `catalog_header`,",
        "new `page_hero` parameters, markup changes, CSS, descriptor",
        "scenario-complete non-Bengal compact docs, reference, or catalog page",
    ]:
        assert boundary in normalized


def test_application_chrome_plan_has_promotion_readiness_queue() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Promotion Readiness Queue", 1)[1].split("## Ranked Backlog", 1)[0]

    assert "Status: decision queue for future implementation slices" in section
    assert "no public API" in section
    assert "start with `application_chrome()`" in section
    assert "whole-frame macro" in section

    for column in [
        "Candidate",
        "Current Readiness",
        "Primary Blocker",
        "Next Slice",
        "Promotion Bias",
    ]:
        assert column in section

    for candidate in [
        "Page actions primitive",
        "Linked nav-tree/sidebar semantics",
        "Shell response/OOB helper",
        "Compact page header / `page_hero` maturation",
        "Generic application shell macro",
        "Catalog/docs shell macro",
    ]:
        assert f"| {candidate} |" in section


def test_application_chrome_plan_promotion_queue_ranks_candidates_by_blocker() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Promotion Readiness Queue", 1)[1].split(
        "Evidence ladder for any queue item:", 1
    )[0]

    for blocker in [
        "Bengal plus private `/page-actions-candidate` prove current composition",
        "no second scenario-complete reference implementation repeats copy URL / LLM text / AI handoff pressure",
        "Bengal plus private `/linked-nav-candidate` prove desktop/phone composition",
        "no second scenario-complete reference implementation repeats the linked-branch gap",
        "Filesystem pages already solve the best adoption path",
        "two manual route fixture families remain only partial evidence",
        "Bengal plus private `/compact-header-candidate` prove current header composition",
        "no second scenario-complete compact docs/reference/catalog implementation",
        "Existing primitives compose real fixtures",
        "Product-specific information architecture is doing the work",
    ]:
        assert blocker in section

    for next_slice in [
        "non-Bengal page-action reference implementation",
        "`page_header`, `page_hero`, `dropdown_menu`, `share_menu`, and `action_bar`",
        "non-Bengal linked-branch reference implementation",
        '`sidebar`, `nav_tree(branch_mode="linked")`, `drawer`, and `drawer_trigger`',
        "third hand-written route family outside `mount_pages()`",
        "`HX-Target` branching and shell-actions OOB",
        "non-Bengal dense-header reference implementation",
        "`page_header`, `page_hero`, `search_header`, `entity_header`, and `document_header`",
        "recipe/browser gauntlets only",
        "implementation pressure for smaller contracts",
    ]:
        assert next_slice in section

    for bias in [
        "Promote a page-local command primitive only if the second independent reference implementation repeats the same gap",
        "Prefer extending hierarchical navigation over a docs/sidebar shell macro only after implementation repetition",
        "Prefer Chirp routing or app-local recipe",
        "Prefer omitting/collapsing optional regions",
        "Reject until two independent reference implementations repeat the same missing owned layer",
        "Reject until a reusable shell-owned contract is separable",
    ]:
        assert bias in section


def test_application_chrome_plan_promotion_queue_has_evidence_ladder_and_stop_rule() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Promotion Readiness Queue", 1)[1].split("## Ranked Backlog", 1)[0]

    for ladder_step in [
        "Recipe pressure",
        "Partial implementation",
        "Promotion candidate",
        "Public API proposal",
        "Shipped contract",
    ]:
        assert ladder_step in section

    for rule in [
        "may add docs, scans, fixtures, or",
        "private examples with tests",
        "changes public macro/API",
        "descriptor metadata",
        "emitted",
        "CSS",
        "manifest",
        "generated component options",
        "runtime behavior",
        "stop and ask before implementing",
        "cannot name two independent reference implementations",
        "continue recipes and browser",
    ]:
        assert rule in section


def test_application_chrome_plan_has_real_reference_implementation_evidence_intake() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Reference implementation evidence intake:", 1)[1].split(
        "Next implementation rule:", 1
    )[0]

    for field in [
        "Implementation identity",
        "Existing primitives tried",
        "Repeated gap",
        "Proof",
        "Promotion boundary",
        "Next decision",
    ]:
        assert f"| {field} |" in section

    for requirement in [
        "App/theme/package name",
        "Bengal, private fixture, recipe prose, or scenario-complete non-Bengal reference usage",
        "Exact Chirp UI primitives used",
        "smallest behavior current primitives cannot express",
        "Render, server, or browser test",
        "no public API, descriptor, CSS, manifest, generated docs, or runtime change",
        "keep as recipe evidence",
        "stop and ask for a public API/design plan",
    ]:
        assert requirement in section

    for disqualifier in [
        "artificial/private fixtures without scenario completeness",
        "recipe prose, pattern docs, or visual preference without rendered usage",
        "Bengal-only selectors or page-context fallbacks",
        "stress tests that prove current primitives work",
        "a proposed API sketch without two independent reference implementations",
    ]:
        assert disqualifier in section


def test_application_chrome_plan_records_post_fixture_reference_evidence_scan() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("### Post-Fixture Repository Reference Evidence Scan", 1)[1].split(
        "Next implementation rule:", 1
    )[0]
    normalized = " ".join(section.split())

    assert "Scan date: 2026-05-23" in section
    assert "no new qualifying scenario-complete non-Bengal reference implementation" in section
    assert "no public API, descriptor, CSS, manifest, generated docs" in normalized
    assert "runtime changes authorized" in normalized

    for scope in [
        "`docs/`",
        "`examples/`",
        "`tests/browser/templates/`",
        "`tests/browser/app.py`",
        "`tests/fixtures/`",
        "`src/chirp_ui/templates/`",
        "excluded Bengal theme templates and the private candidate fixtures",
    ]:
        assert scope in section

    for candidate in [
        "Page actions primitive",
        "Linked nav-tree/sidebar semantics",
        "Shell response/OOB helper",
        "Compact header / `page_hero` maturation",
        "Generic application/docs/catalog shell",
    ]:
        assert f"| {candidate} |" in section

    for decision in [
        "No second scenario-complete copy URL / LLM text / AI handoff reference implementation",
        "keep `page_actions()` unauthorized",
        "No second scenario-complete linked-branch sidebar reference implementation",
        "keep sidebar/nav-tree API unchanged",
        "No third scenario-complete hand-written route family outside `mount_pages()`",
        "keep helpers fixture-local",
        "No second scenario-complete compact docs/reference/catalog implementation",
        "do not change `page_hero` markup or add compact header macros",
        "Keep mega-shell APIs deferred",
    ]:
        assert decision in normalized

    for next_count in [
        "a scenario-complete app/package/theme route family",
        "not a showcase or private fixture",
        "explicit use of the current primitives",
        "a named repeated gap",
        "focused proof",
        "explicit stop-and-ask point",
    ]:
        assert next_count in normalized
