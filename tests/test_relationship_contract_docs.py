from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIPS = REPO_ROOT / "docs" / "RELATIONSHIP-CONTRACTS.md"
PLAN = REPO_ROOT / "docs" / "plans" / "PLAN-relationship-contracts.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
LAYOUT = REPO_ROOT / "docs" / "LAYOUT.md"
PRIMITIVES = REPO_ROOT / "docs" / "PRIMITIVES.md"


def test_relationship_contracts_define_parent_ownership_model() -> None:
    text = RELATIONSHIPS.read_text(encoding="utf-8")

    for required in [
        "Status: active design contract",
        "children own their internal shape; parents own the relationship",
        "Relationship Types",
        "Ownership Rules",
        "Current Contract Matrix",
        "Known Gaps",
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
    relationship_link = "[RELATIONSHIP-CONTRACTS.md](RELATIONSHIP-CONTRACTS.md)"
    plan_link = "[PLAN-relationship-contracts.md](plans/PLAN-relationship-contracts.md)"

    assert relationship_link in INDEX.read_text(encoding="utf-8")
    assert relationship_link in LAYOUT.read_text(encoding="utf-8")
    assert relationship_link in PRIMITIVES.read_text(encoding="utf-8")
    assert plan_link in INDEX.read_text(encoding="utf-8")
    assert plan_link in RELATIONSHIPS.read_text(encoding="utf-8")


def test_relationship_rollout_plan_sets_scope_proof_and_not_now_boundaries() -> None:
    text = PLAN.read_text(encoding="utf-8")

    for required in [
        "Status: in-flight",
        "No new public macro parameters",
        "No manifest schema change",
        "Current Accepted Slices",
        "Next 10 Tasks",
        "Parity Matrix",
        "Steward Notes",
        "Required Proof Per Slice",
        "Not Now",
        "Public `relationship=` macro params",
        "New descriptor fields",
        "`chirpui-manifest@6` projection",
        "Global `[data-chirpui-*]` relationship rules",
    ]:
        assert required in text
