from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
SCREENS = ROOT / "docs" / "screens"
PLAN = ROOT / "docs" / "plans" / "PLAN-visual-taste-floor-saga.md"
SHOWCASE_APP = ROOT / "examples" / "component-showcase" / "app.py"

SCREEN_DOCS = {
    "command-center.md": {
        "route": "/screen-command-center",
        "profile": "atlas",
        "archetype": "command-center",
        "template": "examples/component-showcase/templates/showcase/operations_shell.html",
    },
    "review-queue.md": {
        "route": "/screen-review-queue",
        "profile": "sage",
        "archetype": "review-queue",
        "template": "examples/component-showcase/templates/showcase/support_shell.html",
    },
    "agent-run-monitor.md": {
        "route": "/screen-agent-run-monitor",
        "profile": "signal",
        "archetype": "agent-run-monitor",
        "template": "examples/component-showcase/templates/showcase/screen_agent_run_monitor.html",
    },
    "product-docs-home.md": {
        "route": "/screen-product-docs-home",
        "profile": "ember",
        "archetype": "product-docs-home",
        "template": "examples/component-showcase/templates/showcase/screen_product_docs_home.html",
    },
}


def test_screen_catalog_indexes_all_golden_screens() -> None:
    readme = (SCREENS / "README.md").read_text(encoding="utf-8")

    for filename, metadata in SCREEN_DOCS.items():
        assert filename in readme
        assert metadata["route"] in readme
        assert metadata["profile"] in readme

    assert "Screen entries are recipes, not public macros." in readme
    assert "Choose a screen archetype before choosing individual components." in readme


def test_screen_docs_pin_fixture_routes_profiles_and_proof() -> None:
    app_text = SHOWCASE_APP.read_text(encoding="utf-8")

    for filename, metadata in SCREEN_DOCS.items():
        text = (SCREENS / filename).read_text(encoding="utf-8")
        assert metadata["route"] in text
        assert metadata["route"] in app_text
        assert f"Profile: `{metadata['profile']}" in text
        assert metadata["template"] in text
        assert "tests/test_data_integration.py" in text
        assert "tests/browser/test_golden_screen_fixtures.py" in text
        assert "## Agent Guidance" in text
        assert "## Extraction Candidates" in text
        assert "Do not" in text


def test_screen_catalog_does_not_authorize_public_screen_macros() -> None:
    readme = (SCREENS / "README.md").read_text(encoding="utf-8")
    assert "remain not-now" in readme

    for path in sorted(SCREENS.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        assert "Status: golden screen fixture" in text
        assert "public API work" in normalized


def test_visual_taste_floor_plan_records_golden_screen_progress() -> None:
    text = PLAN.read_text(encoding="utf-8")

    assert "## Current Progress" in text
    for phrase in [
        "Milestone 1 inventory is complete",
        "Command Center and Review Queue fixtures are implemented",
        "Agent Run Monitor and Product/Docs Home fixtures are implemented",
        "The initial screen catalog is published under `docs/screens/`",
    ]:
        assert phrase in text
