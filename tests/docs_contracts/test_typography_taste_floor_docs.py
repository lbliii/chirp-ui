from tests.helpers import REPO_ROOT

ROOT = REPO_ROOT
PLAN = ROOT / "docs" / "plans" / "PLAN-visual-taste-floor-saga.md"
RESEARCH = ROOT / "docs" / "decisions" / "typography-rhythm-taste-floor.md"
INDEX = ROOT / "docs" / "INDEX.md"
ROADMAP = ROOT / "docs" / "strategy" / "roadmap-pre-1.0.md"
INVENTORY = ROOT / "docs" / "agents" / "agent-source-inventory.md"
SOURCE_MAP = ROOT / "docs" / "agents" / "agent-source-map.md"


def test_typography_research_records_external_and_local_evidence() -> None:
    text = RESEARCH.read_text(encoding="utf-8")

    for phrase in [
        "Status: research-backed planning input",
        "This record captures the typography research",
        "It does not add public tokens, macro parameters",
        "Material 3 typography",
        "Fluent 2 typography",
        "Carbon typography",
        "Atlassian typography",
        "Primer typography",
        "GOV.UK layout/type scale",
        "USWDS typography",
        "WCAG text spacing",
        "Current Chirp UI typography has useful foundations",
        "UI and prose scales are named by size rather than role.",
        "viewport-driven `clamp()` values",
    ]:
        assert phrase in text


def test_typography_research_keeps_roles_recipe_only() -> None:
    text = RESEARCH.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "These names are planning vocabulary only",
        "They do not authorize public token names or macros",
        "Stop and ask before adding public typography role tokens",
        "New utility classes for type roles.",
        "New font dependency or bundled web font.",
        "Manifest schema for type roles.",
    ]:
        assert phrase in normalized

    for role_family in [
        "Structure",
        "Reading",
        "Metadata",
        "Controls",
        "State",
        "Data",
        "Technical",
        "Expressive",
    ]:
        assert f"| {role_family} |" in text


def test_visual_taste_plan_tracks_typography_next_phase() -> None:
    text = PLAN.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for phrase in [
        "Typography roles",
        "docs/decisions/typography-rhythm-taste-floor.md",
        "Epic 5a. Typography And Rhythm Taste Floor",
        "Audit current CSS partials, theme packs, examples, and golden screens",
        "Draft a recipe-only role matrix",
        "Stop and ask before changing public token defaults",
        "Run the typography and rhythm audit before promoting visual patterns.",
        "Typography roles are screen-proven before becoming public token vocabulary.",
    ]:
        assert phrase in normalized


def test_typography_research_is_indexed_and_mapped() -> None:
    index_text = INDEX.read_text(encoding="utf-8")
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    inventory_text = INVENTORY.read_text(encoding="utf-8")
    source_map_text = SOURCE_MAP.read_text(encoding="utf-8")

    assert "decisions/typography-rhythm-taste-floor.md" in index_text
    assert "Typography role and rhythm research" in index_text

    assert "docs/decisions/typography-rhythm-taste-floor.md" in roadmap_text
    assert "Typography improvements are role-backed and screen-proven" in roadmap_text

    for text in [inventory_text, source_map_text]:
        assert "docs/decisions/typography-rhythm-taste-floor.md" in text
        assert "planning input" in text
        assert "not public token vocabulary" in text
