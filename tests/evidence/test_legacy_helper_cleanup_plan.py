from tests.helpers import REPO_ROOT

PLAN = REPO_ROOT / "docs" / "plans" / "done" / "PLAN-legacy-helper-cleanup-pre-1.0.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
ROADMAP = REPO_ROOT / "docs" / "strategy" / "roadmap-pre-1.0.md"
PRIMITIVE_PLAN = REPO_ROOT / "docs" / "plans" / "done" / "PLAN-primitive-vocabulary-hardening.md"


def test_legacy_helper_cleanup_plan_records_scope_and_safety() -> None:
    text = PLAN.read_text(encoding="utf-8")

    for required in [
        "Do not delete public legacy helper classes in this phase.",
        "No helper vocabulary growth.",
        "Make The Visual Audit Helper-Free",
        "Clean High-Visibility Showcase Templates",
        "Triage The Static Showcase",
        "Pre-1.0 Decision Gate",
        "`mt-sm`, `mt-md`, `mb-md`",
        "`visually-hidden`, `focus-ring`, `list-reset`",
        "uv run poe verify-generated",
        "uv run poe check",
    ]:
        assert required in text


def test_legacy_helper_cleanup_plan_is_linked_from_planning_docs() -> None:
    plan_link = "PLAN-legacy-helper-cleanup-pre-1.0.md"

    assert plan_link in INDEX.read_text(encoding="utf-8")
    assert plan_link in ROADMAP.read_text(encoding="utf-8")
    assert plan_link in PRIMITIVE_PLAN.read_text(encoding="utf-8")
