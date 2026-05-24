from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
ROADMAP = ROOT / "docs" / "strategy" / "roadmap-pre-1.0.md"
PLANS = ROOT / "docs" / "plans"

EXPECTED_ACTIVE_PLANS = [
    "PLAN-application-chrome-system.md",
    "PLAN-bengal-chirpui-library-contract.md",
    "PLAN-chirp-theme-content-parity.md",
    "PLAN-css-scope-and-layer.md",
    "PLAN-page-actions-primitive.md",
    "PLAN-pre-1.0-productization-saga.md",
    "PLAN-visual-taste-floor-saga.md",
]


def test_active_plans_are_mapped_to_roadmap_workstreams() -> None:
    """Every live plan should be anchored to the current roadmap, not free-floating."""
    roadmap = ROADMAP.read_text(encoding="utf-8")
    active_plans = sorted(path.name for path in PLANS.glob("PLAN-*.md"))

    missing = [name for name in active_plans if name not in roadmap]
    assert not missing, "active plans missing roadmap workstream mapping: " + ", ".join(missing)


def test_active_plan_count_stays_intentional() -> None:
    """Planning cleanup should keep live plans bounded and force explicit review on growth."""
    active_plans = sorted(path.name for path in PLANS.glob("PLAN-*.md"))

    assert active_plans == EXPECTED_ACTIVE_PLANS
    assert len(active_plans) <= 7


def test_archived_plans_do_not_claim_active_or_draft_status() -> None:
    """Archived plans may mention history, but their status line must not be active/draft."""
    offenders: list[str] = []
    for path in sorted((PLANS / "done").glob("PLAN-*.md")):
        for line in path.read_text(encoding="utf-8").splitlines()[:8]:
            normalized = line.strip().lower().strip("*")
            if normalized in {"status: active", "status: draft"}:
                offenders.append(path.name)
                break

    assert not offenders, "archived plans with active/draft status: " + ", ".join(offenders)


def test_active_plans_expose_next_work_marker() -> None:
    """Live plans should point agents at remaining work, not only historical design."""
    accepted_markers = (
        "## Residual Work",
        "## Next Slice",
        "## Next Batches",
        "## Ranked Backlog",
        "## Recommended Execution Order",
        "## Sprint Structure",
        "## Open items",
        "## Ranked Waves",
    )
    missing: list[str] = []

    for path in sorted(PLANS.glob("PLAN-*.md")):
        text = path.read_text(encoding="utf-8")
        if not any(marker in text for marker in accepted_markers):
            missing.append(path.name)

    assert not missing, "active plans missing a next-work marker: " + ", ".join(missing)


def test_roadmap_records_application_chrome_reference_implementation_gate() -> None:
    """High-level roadmap should not route completed chrome investigations into fixture churn."""
    text = ROADMAP.read_text(encoding="utf-8")
    section = text.split("### 5a. Application Chrome System", 1)[1].split(
        "### 5b. Bengal-Driven Component Maturation", 1
    )[0]
    normalized = " ".join(section.split())

    for signal in [
        "Current promotion queue:",
        "Private evidence is complete for page actions, linked nav/sidebar semantics,",
        "shell response/OOB routing, and compact header/page hero comparison",
        "Scenario-complete proof also exists for dense reference/data pages and agent discovery",
        "The next work there is proof analysis",
        "before proposing a data-grid, reference-page macro, manifest schema change",
        "not waiting for a userbase or adding another artificial fixture",
        "REFERENCE-IMPLEMENTATION-PLAYBOOK.md",
        "reference-implementations/README.md",
        "reference-implementations/PROOF-ANALYSIS.md",
        "guidance, more reference evidence, or a stop-and-ask API plan",
        "reference-implementations/RECIPE-GUIDANCE.md",
        "keep current primitives and teach the recipe",
        "second scenario-complete non-Bengal reference implementation",
        "third scenario-complete hand-written route family",
        "`application_chrome()`",
        "`docs_shell`",
        "`catalog_shell`",
        "`compact_page_header`",
        "`page_actions`",
        "shell response helper APIs",
    ]:
        assert signal in normalized

    bengal_section = text.split("### 5b. Bengal-Driven Component Maturation", 1)[1].split(
        "### 6. CSS Scope Hardening", 1
    )[0]
    bengal_normalized = " ".join(bengal_section.split())
    assert "Treat private fixtures as proof of current composition" in bengal_normalized
    assert "not as promotion evidence by themselves" in bengal_normalized


def test_productization_saga_records_application_chrome_queue_status() -> None:
    """The saga should send future slices toward reference implementation evidence or explicit API planning."""
    text = (PLANS / "PLAN-pre-1.0-productization-saga.md").read_text(encoding="utf-8")
    section = text.split("### 6. Application Chrome Adoption", 1)[1].split(
        "### 7. Bengal And chirp-theme Integration", 1
    )[0]
    normalized = " ".join(section.split())

    for signal in [
        "Current application-chrome queue:",
        "Private fixtures now prove current composition for page actions",
        "linked",
        "nav/sidebar",
        "compact headers/page heroes",
        "shell response/OOB branching",
        "Dense reference/data and agent-discovery proof now exist too",
        "Their next slice is proof analysis against current primitives",
        "not another brief",
        "not an immediate data-grid, reference-page macro, manifest schema",
        "deliberately built reference implementation repetition",
        "second scenario-complete non-Bengal page-action",
        "linked-branch",
        "compact docs/reference/catalog",
        "third scenario-complete hand-written route family outside `mount_pages()`",
        "Do not spend more productization slices creating artificial chrome fixtures",
        "unless they test a new failure mode",
        "docs/reference-implementations/PROOF-ANALYSIS.md",
        "recipe guidance, more independent reference evidence",
        "docs/reference-implementations/RECIPE-GUIDANCE.md",
        "keeps the surface on current primitives",
        "stop and ask for an explicit public API/design plan",
    ]:
        assert signal in normalized


def test_application_chrome_plan_links_reference_scenario_queue() -> None:
    text = (PLANS / "PLAN-application-chrome-system.md").read_text(encoding="utf-8")
    section = text.split("Reference scenario queue:", 1)[1].split(
        "Disqualifiers for promotion evidence:", 1
    )[0]

    for link in [
        "../REFERENCE-IMPLEMENTATION-PLAYBOOK.md",
        "../reference-implementations/README.md",
        "../reference-implementations/PAGE-ACTIONS-AI-REFERENCE.md",
        "../reference-implementations/LINKED-NAV-CATALOG-REFERENCE.md",
        "../reference-implementations/COMPACT-HEADER-REFERENCE.md",
        "../reference-implementations/SHELL-RESPONSE-REFERENCE.md",
        "../reference-implementations/DENSE-REFERENCE-DATA-REFERENCE.md",
        "../reference-implementations/AGENT-DISCOVERY-REFERENCE.md",
    ]:
        assert link in section


def test_navigation_contract_records_application_chrome_current_status() -> None:
    """Canonical navigation docs should keep app chrome recipe-first until reference implementations repeat gaps."""
    text = (ROOT / "docs" / "patterns" / "navigation.md").read_text(encoding="utf-8")
    section = text.split("## Application Chrome System", 1)[1].split("## ARIA And Semantics", 1)[0]
    normalized = " ".join(section.split())

    for signal in [
        "Current promotion status:",
        "Private evidence is complete for page actions, linked nav/sidebar semantics,",
        "shell response/OOB branching, and compact header/page hero comparison",
        "do not count as the second scenario-complete reference implementation",
        "deliberately built or identified non-Bengal page-action",
        "linked-branch",
        "compact docs/reference/catalog reference implementation",
        "third",
        "hand-written route family outside `mount_pages()`",
        "`application_chrome()`",
        "`docs_shell`",
        "`catalog_shell`",
        "`compact_page_header`",
        "`page_actions`",
        "shell response helper APIs",
    ]:
        assert signal in normalized
