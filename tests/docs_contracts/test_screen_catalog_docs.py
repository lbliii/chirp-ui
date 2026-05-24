from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
SCREENS = ROOT / "docs" / "screens"
PLAN = ROOT / "docs" / "plans" / "PLAN-visual-taste-floor-saga.md"
SHOWCASE_APP = ROOT / "examples" / "component-showcase" / "app.py"
INDEX = ROOT / "docs" / "INDEX.md"

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
    assert "[Screen Archetype Matrix](archetype-matrix.md)" in readme
    assert "[Screen Entry Template](entry-template.md)" in readme


def test_screen_archetype_matrix_names_canonical_product_situations() -> None:
    matrix = (SCREENS / "archetype-matrix.md").read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")

    assert "Status: recipe catalog expansion" in matrix
    assert "The matrix is recipe-only." in matrix
    assert "screens/archetype-matrix.md" in index
    assert "screens/entry-template.md" in index

    for archetype in [
        "`command-center`",
        "`review-queue`",
        "`agent-run-monitor`",
        "`product-docs-home`",
        "`settings-detail`",
        "`data-index-detail`",
        "`setup-flow`",
        "`dashboard-overview`",
    ]:
        assert archetype in matrix

    for phrase in [
        "Choose the closest archetype and profile from the matrix.",
        "planned recipe target",
        "record the missing relationship as evidence",
        "does not authorize",
        "public screen macro",
        "utility classes for spacing, layout, or text alignment",
    ]:
        assert phrase in matrix


def test_screen_entry_template_preserves_recipe_first_contract() -> None:
    template = (SCREENS / "entry-template.md").read_text(encoding="utf-8")

    for heading in [
        "## Use When",
        "## Do Not Use When",
        "## Composition Map",
        "## Typography Role Map",
        "## Data Shape",
        "## Required States",
        "## Agent Guidance",
        "## Proof Checklist",
        "## Extraction Candidates",
    ]:
        assert heading in template

    for phrase in [
        "planned recipe target | golden screen fixture",
        "do not authorize public",
        "docs/decisions/typography-role-matrix.md",
        "data-screen-archetype",
        "Stop and ask before adding public vocabulary",
    ]:
        assert phrase in template


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
        assert "## Typography Role Map" in text
        assert "docs/decisions/typography-role-matrix.md" in text
        assert "## Extraction Candidates" in text
        assert "Do not" in text


def test_screen_docs_map_recipe_only_typography_roles() -> None:
    readme = (SCREENS / "README.md").read_text(encoding="utf-8")
    assert "docs/decisions/typography-role-matrix.md" in readme
    assert "not public token names or utility classes" in readme

    expected_roles = {
        "command-center.md": [
            "`page-title`",
            "`panel-title`",
            "`object-title`",
            "`dense-body`",
            "`metadata`",
            "`metric`",
            "`status-label`",
        ],
        "review-queue.md": [
            "`page-title`",
            "`panel-title`",
            "`object-title`",
            "`dense-body`",
            "`metadata`",
            "`metric`",
            "`status-label`",
        ],
        "agent-run-monitor.md": [
            "`page-title`",
            "`panel-title`",
            "`object-title`",
            "`dense-body`",
            "`metadata`",
            "`metric`",
            "`status-label`",
            "`log-line`",
        ],
        "product-docs-home.md": [
            "`hero-display`",
            "`proof-copy`",
            "`panel-title`",
            "`object-title`",
            "`metadata`",
            "`metric`",
            "`status-label`",
        ],
    }

    for filename, roles in expected_roles.items():
        text = (SCREENS / filename).read_text(encoding="utf-8")
        for role in roles:
            assert role in text


def test_screen_catalog_does_not_authorize_public_screen_macros() -> None:
    readme = (SCREENS / "README.md").read_text(encoding="utf-8")
    assert "remain not-now" in readme

    for filename in SCREEN_DOCS:
        path = SCREENS / filename
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
