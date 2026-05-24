from tests.helpers import REPO_ROOT

RELATIONSHIPS = REPO_ROOT / "docs" / "fundamentals" / "relationship-contracts.md"
PLAN = REPO_ROOT / "docs" / "plans" / "done" / "PLAN-relationship-contracts.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
LAYOUT = REPO_ROOT / "docs" / "fundamentals" / "layout.md"
PRIMITIVES = REPO_ROOT / "docs" / "fundamentals" / "primitives.md"


def test_relationship_contracts_define_parent_ownership_model() -> None:
    text = RELATIONSHIPS.read_text(encoding="utf-8")

    for required in [
        "Status: active design contract",
        "children own their internal shape; parents own the relationship",
        "Relationship Types",
        "Ownership Rules",
        "Current Contract Matrix",
        "Known Gaps",
        "Registry And Manifest Decision",
        "External Takeaways",
        "Agent Checklist",
        "Inset",
        "Sibling rhythm",
        "Attached",
        "Grouped",
        "Separated",
        "Region",
        "Pressure",
        "Local overflow",
    ]:
        assert required in text


def test_relationship_contracts_name_current_and_gap_surfaces() -> None:
    text = RELATIONSHIPS.read_text(encoding="utf-8")

    for surface in [
        "`stack()`",
        "`cluster()`",
        "`form()`",
        "`command_bar` / `filter_bar`",
        "`workspace_shell`",
        "field wrappers",
        "`fieldset`",
        "`modal` / `drawer` / `tray`",
        "navigation primitives",
    ]:
        assert surface in text


def test_relationship_contracts_are_discoverable_from_core_docs() -> None:
    relationship_link = "[RELATIONSHIP-CONTRACTS.md](fundamentals/relationship-contracts.md)"
    relationship_link_from_fundamentals = "[RELATIONSHIP-CONTRACTS.md](relationship-contracts.md)"
    plan_link = "[PLAN-relationship-contracts.md](plans/done/PLAN-relationship-contracts.md)"

    assert relationship_link in INDEX.read_text(encoding="utf-8")
    assert relationship_link_from_fundamentals in LAYOUT.read_text(encoding="utf-8")
    assert relationship_link_from_fundamentals in PRIMITIVES.read_text(encoding="utf-8")
    assert plan_link in INDEX.read_text(encoding="utf-8")
    assert (
        "[PLAN-relationship-contracts.md](../plans/done/PLAN-relationship-contracts.md)"
        in RELATIONSHIPS.read_text(encoding="utf-8")
    )


def test_relationship_rollout_plan_sets_scope_proof_and_not_now_boundaries() -> None:
    text = PLAN.read_text(encoding="utf-8")

    for required in [
        "Status: shipped",
        "No new public macro parameters",
        "No manifest schema change",
        "Current Accepted Slices",
        "Remaining Follow-Ups",
        "Parity Matrix",
        "Objective Decisions",
        "Steward Notes",
        "Required Proof Per Slice",
        "Not Now",
        "Public `relationship=` macro params",
        "New descriptor fields",
        "`chirpui-manifest@6` projection",
        "Global `[data-chirpui-*]` relationship rules",
        "Descriptor/manifest projection remains deferred",
        "lbliii/emdashCSS",
    ]:
        assert required in text
