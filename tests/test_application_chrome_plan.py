from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
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
    assert "two real consuming apps" in text
    assert "utility classes for density, hiding, spacing, alignment, or overflow" in text
