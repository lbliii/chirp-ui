from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
PLAN = ROOT / "docs" / "plans" / "PLAN-page-actions-primitive.md"
INDEX = ROOT / "docs" / "INDEX.md"
ROADMAP = ROOT / "docs" / "ROADMAP-pre-1.0.md"
APP_CHROME_PLAN = ROOT / "docs" / "plans" / "PLAN-application-chrome-system.md"


def test_page_actions_primitive_plan_is_active_but_no_api_authorized() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "Status: active investigation, no public API authorized" in text
    assert "This plan does not authorize `page_actions()`" in text
    for forbidden in [
        "descriptor",
        "emitted classes",
        "CSS",
        "JavaScript runtime",
        "manifest changes",
        "generated docs",
    ]:
        assert forbidden in text

    assert "Do not add `page_actions()` in this investigation slice." in text
    assert "Do not move Bengal `.chirp-theme-page-actions*` selectors into `chirpui-*`" in text
    assert "Do not use this candidate to justify `application_chrome()`" in text


def test_page_actions_plan_records_existing_primitives_tried() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Existing Primitives Tried", 1)[1].split(
        "## Reference Evidence Scan", 1
    )[0]

    for surface in [
        "`page_hero` actions slot",
        "`dropdown_menu`",
        "`share_menu`",
        "`action_bar`",
        "Bengal `page_actions` partial",
    ]:
        assert f"| {surface} |" in section

    for gap in [
        "Does not define command anatomy",
        "not a page-command surface",
        "not a title-adjacent overflow/popover surface",
        "not a registry-owned Chirp UI contract",
    ]:
        assert gap in section


def test_page_actions_reference_implementation_scan_keeps_promotion_gate_unmet() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Reference Evidence Scan", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    assert "Current scan result: the promotion gate is not satisfied" in section
    assert "only qualifying implementation context" in section

    for evidence in [
        "Bengal docs/reference page actions",
        "Forum site pattern detail page",
        "Component showcase social/layout examples",
        "Product/media pattern docs",
        "Existing `share_menu` component",
    ]:
        assert f"| {evidence} |" in section

    for boundary in [
        "Partial",
        "No | Social/forum actions prove `share_menu` and `action_bar`",
        "No | Showcase examples are useful visual/API proof",
        "No | Recipe prose does not prove",
        "No | It remains the compatibility/social sharing surface",
    ]:
        assert boundary in section


def test_page_actions_reference_implementation_scan_names_remaining_evidence_needed() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Implementation evidence still needed:", 1)[1].split(
        "## Non-Bengal Reference Candidate Scan", 1
    )[0]

    for requirement in [
        "one non-Bengal scenario-complete app, example, or packaged integration",
        "copy URL plus at least one non-social page",
        "`page_hero` actions, `dropdown_menu`, `share_menu`, and",
        "`action_bar` were tried or considered",
        "page-local command anatomy",
        "rather than social sharing, generic dropdown actions, or shell composition",
        "browser proof for trigger placement, popover containment, keyboard/focus",
    ]:
        assert requirement in section


def test_page_actions_non_bengal_candidate_scan_keeps_promotion_unmet() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Non-Bengal Reference Candidate Scan", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    assert "Scan date: 2026-05-23" in section
    assert "no existing non-Bengal page qualifies as the second reference" in section
    assert "scenario-complete first-party" in section

    for candidate in [
        "Component showcase Streaming & AI page",
        "Component showcase catalog/detail routes",
        "Forum site pattern detail page",
        "Product/media pattern pages",
        "Bengal docs/reference pages",
    ]:
        assert f"| {candidate} |" in section

    for decision in [
        "Best candidate for a private fixture",
        "there is no LLM text or AI handoff need",
        "Confirms the social/action-bar boundary",
        "Pattern prose is not reference implementation evidence",
        "Still the only qualifying implementation context",
    ]:
        assert decision in section


def test_page_actions_candidate_fixture_rule_tries_existing_primitives_first() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Candidate fixture rule:", 1)[1].split("## Private Candidate Fixture", 1)[
        0
    ]

    for requirement in [
        "Streaming & AI page family",
        "copy current URL plus open/copy transcript, prompt, or LLM sample text",
        "Use existing `page_header` actions, `dropdown_menu`, `share_menu`,",
        "`action_bar`, and `copy_button` before sketching any new macro",
        "If those primitives suffice, close the candidate as no-new-API evidence",
        "record the exact missing anatomy",
        "external link safety",
        "keyboard/focus",
        "responsive containment",
        "Keep the fixture private/copyable",
        "not Bengal-specific",
    ]:
        assert requirement in section


def test_page_actions_plan_records_private_candidate_fixture_without_api_promotion() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Private Candidate Fixture", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    assert "Status: implemented as test evidence only, no public API authorized." in section
    for fixture_ref in [
        "route: `/page-actions-candidate`",
        "tests/browser/templates/page_actions_candidate_page.html",
        "tests/browser/test_page_actions_candidate.py",
    ]:
        assert fixture_ref in section

    for proof in [
        "page-local tools in `page_header` actions",
        "existing `dropdown_menu` and `share_menu`",
        "`action_bar` and `copy_button`",
        "open prompt text and copy",
        "outside Bengal theme selectors",
        "without document-level horizontal overflow",
        "long non-social dropdown command",
        "without a new page-actions primitive",
    ]:
        assert proof in section

    for boundary in [
        "It does not prove that `page_actions()` should exist.",
        "does not provide URL/LLM text/AI handoff semantics as one owned",
        "does not add a descriptor, macro, emitted class, CSS partial",
        "runtime controller",
        "does not count as qualifying implementation evidence",
    ]:
        assert boundary in section


def test_page_actions_plan_fixture_decision_keeps_next_slice_analytical() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Fixture decision:", 1)[1].split("## Fixture Analysis", 1)[0]

    for decision in [
        "Do existing primitives render the candidate shape?",
        "Yes, as a private fixture.",
        "Is there enough evidence for public API promotion?",
        "No.",
        "Is the next slice implementation or analysis?",
        "Analysis: inspect fixture behavior",
        "A second independent reference implementation that repeats copy URL plus non-social page commands",
    ]:
        assert decision in section


def test_page_actions_plan_fixture_analysis_classifies_gap_without_promotion() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Fixture Analysis", 1)[1].split("## Candidate Contract Shape", 1)[0]

    assert "Analysis date: 2026-05-23" in section
    assert "keep page actions in investigation" in section
    assert "does not prove a public `page_actions()` API gap" in section

    for behavior in [
        "Title-adjacent placement",
        "Grouped non-social commands",
        "Social/canonical URL share",
        "Known-text copy",
        "Visible local actions",
        "Responsive containment",
    ]:
        assert f"| {behavior} |" in section

    for outcome in [
        "`page_header` actions can hold `dropdown_menu` and `share_menu`",
        "`dropdown_menu` can expose open prompt text",
        "`share_menu` covers copy/social URL affordances",
        "`copy_button` copies a known prompt string",
        "`action_bar` covers inline visible actions",
        "Browser proof covers 320, 390, 768, and 1024 widths",
    ]:
        assert outcome in section

    for classification in [
        "Real gap: there is no single owned contract",
        "page URL, LLM text fetch/copy",
        "Not yet a promotion gap",
        "one artificial non-Bengal",
        "build or",
        "scenario-complete reference implementation",
    ]:
        assert classification in section


def test_page_actions_plan_fixture_analysis_next_slices_stay_private_until_second_reference_implementation() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Next-slice options from this analysis:", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    for slice_name in [
        "Fixture gap notes",
        "Private behavior stress",
        "Reference implementation design",
        "Public API proposal",
    ]:
        assert f"| {slice_name} |" in section

    for boundary in [
        "Low; docs/test only.",
        "Closed for the current private fixture",
        "still not API proof",
        "Low; evidence gathering.",
        "High; stop and ask first.",
        "only after a second reference implementation repeats the gap",
    ]:
        assert boundary in section

    for stress_result in [
        "Private behavior stress result:",
        "prompt text route",
        "`copy_button` feedback",
        "long dropdown command visibility",
        "menu containment at",
        "320px",
        "strengthens the existing-primitives recipe",
        "not the public",
        "API case",
        "after a second reference implementation exists",
    ]:
        assert stress_result in section


def test_page_actions_plan_real_reference_implementation_search_finds_no_second_reference_implementation() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Reference Evidence Search", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    assert "Search date: 2026-05-23" in section
    assert "no second qualifying scenario-complete non-Bengal reference" in section
    assert "Page actions should remain in" in section

    for scope in [
        "`docs/`",
        "`examples/`",
        "`tests/browser/templates/`",
        "`tests/browser/app.py`",
        "`src/chirp_ui/templates/`",
        "excluded Bengal theme templates",
    ]:
        assert scope in section

    for criterion in [
        "page or object header placement",
        "copy current/canonical URL",
        "at least one non-social page command",
        "LLM text, prompt/transcript, AI handoff",
        "`page_header`, `page_hero`, `dropdown_menu`,",
        "`share_menu`, `action_bar`, and `copy_button`",
    ]:
        assert criterion in section


def test_page_actions_plan_real_reference_implementation_search_records_near_misses() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Reference Evidence Search", 1)[1].split("Decision after search:", 1)[0]

    for candidate in [
        "Private `/page-actions-candidate` fixture",
        "Dense object chrome browser fixture",
        "Application chrome route fixtures",
        "Gauntlet command surfaces",
        "Forum site patterns",
        "Product/media pattern pages",
        "Streaming showcase page",
    ]:
        assert f"| {candidate} |" in section

    for reason in [
        "Artificial evidence fixture, not a scenario-complete reference implementation",
        "not copy URL plus LLM/prompt/AI handoff semantics",
        "not page-local copy/LLM actions",
        "Browser stress evidence only",
        "Confirms the social/action boundary",
        "Pattern prose and visual recipes",
        "does not place copy URL plus non-social commands",
    ]:
        assert reason in section


def test_page_actions_plan_real_reference_implementation_search_keeps_api_closed_and_routes_next_slice() -> (
    None
):
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Decision after search:", 1)[1].split("## Candidate Contract Shape", 1)[0]

    for decision in [
        "Keep `page_actions()` unauthorized.",
        "Keep the private fixture as regression and evidence",
        "Do not count forum/social",
        "dense object command menus",
        "gauntlet stress cases",
        "recipe prose",
        "should not be a public page-actions API",
        "build a scenario-complete external-pattern-backed reference",
        "next readiness queue candidate",
    ]:
        assert decision in section


def test_page_actions_plan_defines_candidate_contract_without_implementation() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Candidate Contract Shape", 1)[1].split("## Open Design Questions", 1)[
        0
    ]

    for contract in [
        "Trigger, native popover/menu panel",
        "copy URL, open LLM text, copy LLM text, and external AI handoff",
        "structured data or explicit slots, not raw JavaScript strings",
        "named Chirp UI runtime module, not inline scripts",
        "normal template escaping and attribute helpers",
        "Escape/light dismiss",
        "phone, tablet, and desktop widths",
    ]:
        assert contract in section


def test_page_actions_plan_has_promotion_gate_and_collateral() -> None:
    text = PLAN.read_text(encoding="utf-8")
    gate = text.split("## Promotion Gate", 1)[1].split("## Not Now", 1)[0]

    for requirement in [
        "Bengal plus one additional independent reference implementation",
        "`page_hero` actions, `dropdown_menu`,",
        "`share_menu`, and `action_bar`",
        "macro parameters, slots, action item shape, event hooks",
        "escaping, and strict undefined behavior",
        "copy success and failure states",
        '`rel="noopener noreferrer"`',
        "descriptor, macro, CSS partial, generated CSS",
        "manifest, generated component options, docs, examples",
        "changelog",
    ]:
        assert requirement in gate


def test_page_actions_plan_has_non_authorizing_api_sketch() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Non-Authorizing API Sketch", 1)[1].split(
        "## Proof Matrix For Promotion", 1
    )[0]

    assert "evaluation input only" in section
    assert "Do not copy it into templates, generated docs, examples, or downstream code" in section
    assert '{% from "chirpui/page_actions.html" import page_actions %}' in section
    assert "Provisional macro shape:" in section

    for parameter in [
        "`title`",
        "`label`",
        "`url`",
        "`llm_text_url`",
        "`actions`",
        "`id`",
        "`placement`",
        "`cls` / `attrs_map`",
    ]:
        assert f"| {parameter} |" in section


def test_page_actions_plan_defines_action_item_schema_and_slots() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Non-Authorizing API Sketch", 1)[1].split(
        "## Proof Matrix For Promotion", 1
    )[0]

    for item_type in [
        "`copy-url`",
        "`open-url`",
        "`copy-text-url`",
        "`ai-handoff`",
        "`custom-link`",
        "`custom-button`",
        "`separator`",
    ]:
        assert item_type in section

    for field in [
        "`type`",
        "`label`",
        "`url`",
        "`href`",
        "`assistant`",
        "`icon`",
        "`method`",
        "`attrs_map`",
    ]:
        assert f"| {field} |" in section

    for slot in ["`trigger`", "`header`", "`actions`", "`footer`"]:
        assert f"| {slot} |" in section


def test_page_actions_plan_pins_runtime_and_existing_surface_boundaries() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("## Non-Authorizing API Sketch", 1)[1].split(
        "## Proof Matrix For Promotion", 1
    )[0]

    for runtime_boundary in [
        "Use native `[popover]`",
        "named Chirp UI runtime controller",
        "`chirpui:page-action-copy`",
        "`chirpui:page-action-error`",
        "No inline scripts",
        "no label-based behavior inference",
    ]:
        assert runtime_boundary in section

    for coexistence in [
        "`share_menu` remains the social-share compatibility surface",
        "`dropdown_menu` remains a generic command/select/split menu family",
        "page URL, LLM text, AI handoff",
    ]:
        assert coexistence in section


def test_page_actions_plan_has_promotion_proof_matrix() -> None:
    text = PLAN.read_text(encoding="utf-8")
    matrix = text.split("## Proof Matrix For Promotion", 1)[1].split("## Promotion Gate", 1)[0]

    for proof_area in [
        "Registry and manifest",
        "Template anatomy",
        "Escaping and security",
        "Runtime",
        "Keyboard and focus",
        "Responsive and overflow",
        "CSS and tokens",
        "Docs and examples",
    ]:
        assert f"| {proof_area} |" in matrix

    for requirement in [
        "manifest projection tests",
        "empty action list",
        '`rel="noopener noreferrer"`',
        "fetch failure",
        "focus return",
        "320, 390, 768, 1024, and desktop widths",
        "no theme-only selectors",
        "migration note for `share_menu` boundaries",
    ]:
        assert requirement in matrix


def test_page_actions_plan_has_real_reference_implementation_evidence_intake() -> None:
    text = PLAN.read_text(encoding="utf-8")
    section = text.split("Reference implementation evidence intake:", 1)[1].split(
        "## Candidate Contract Shape", 1
    )[0]

    for field in [
        "Implementation identity",
        "Existing primitives tried",
        "Repeated gap",
        "Proof",
        "Boundary",
        "Decision",
    ]:
        assert f"| {field} |" in section

    for requirement in [
        "Scenario-complete non-Bengal app, package, or docs/reference route family",
        "private fixtures and pattern prose do not qualify",
        "`page_header` or `page_hero` actions",
        "`dropdown_menu`, `share_menu`, `action_bar`, and `copy_button`",
        "copy current URL",
        "fetch/copy LLM text",
        "AI handoff",
        "Browser or server proof",
        "no-authorization note for `page_actions()`",
        "stop and ask for an explicit public API/design plan",
    ]:
        assert requirement in section

    for disqualifier in [
        "private `/page-actions-candidate` fixture by itself",
        "Bengal page actions by themselves",
        "social sharing that `share_menu` already covers",
        "dense object command menus without URL/LLM/AI semantics",
        "copy buttons for known local text without page-level command grouping",
        "visual preference for title-adjacent actions without a repeated behavior gap",
    ]:
        assert disqualifier in section


def test_page_actions_plan_is_indexed_and_roadmapped() -> None:
    assert "[PLAN-page-actions-primitive.md](plans/PLAN-page-actions-primitive.md)" in (
        INDEX.read_text(encoding="utf-8")
    )
    roadmap = ROADMAP.read_text(encoding="utf-8")
    assert "docs/plans/PLAN-page-actions-primitive.md" in roadmap
    assert "before any registry-owned page-actions macro or runtime is proposed" in roadmap


def test_application_chrome_plan_points_to_page_actions_investigation() -> None:
    text = APP_CHROME_PLAN.read_text(encoding="utf-8")

    assert "Page actions primitive" in text
    assert "Candidate for next investigation" in text
    assert "Bengal page actions repeat copy URL, LLM text, and AI handoff hooks" in text
