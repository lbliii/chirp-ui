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


def test_application_chrome_plan_distinguishes_recipe_proof_from_consumers() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "Current evidence log:" in text
    for evidence in [
        "Dense object chrome showcase recipes",
        "Rail-to-drawer showcase recipe and browser fixture",
        "Application chrome gauntlet families",
        "Bengal docs chrome",
    ]:
        assert evidence in text

    assert "Counts As Real Consumer?" in text
    assert "not enough for `application_chrome`" in text
    assert "not enough for a stable shell API" in text
    assert "Open consumer evidence required before composite work" in text
    assert "one filesystem-routed Chirp app" in text
    assert "one second app or packaged integration" in text
