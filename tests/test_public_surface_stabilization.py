from pathlib import Path

from chirp_ui.manifest import build_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
DESIGN_RESEARCH = REPO_ROOT / "docs" / "DESIGN-SYSTEM-RESEARCH.md"
SHOWCASE = REPO_ROOT / "examples" / "design-system-gap-showcase" / "index.html"
COMPONENT_TESTS = REPO_ROOT / "tests" / "test_components.py"
ASCII_TESTS = REPO_ROOT / "tests" / "test_ascii_components.py"


def test_public_surface_stabilization_doc_records_current_slice() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "Promote to stable",
        "Keep experimental",
        "`logo-cloud` | Promote to stable",
        "`story-card` | Promote to stable",
        "`cta-band` | Promote to stable",
        "`ascii-badge` | Promote to stable",
        "`ascii-toggle` | Promote to stable",
        "`ascii-progress` | Promote to stable",
        "`ascii-table` | Promote to stable",
        "no private theme token namespace",
    ]:
        assert required in text


def test_public_surface_doc_defines_evidence_labels() -> None:
    """Maturity and research labels should stay explicit for humans and agents."""
    text = DOC.read_text(encoding="utf-8")
    section = text.split("## Evidence Labels", 1)[1].split("## Current Slice", 1)[0]

    for label in [
        "`stable`",
        "`experimental`",
        "`recipe-only`",
        "`compatibility`",
        "`research`",
    ]:
        assert f"| {label} |" in section

    for contract in [
        "`maturity=stable`",
        "`maturity=experimental`",
        "`authoring=preferred`",
        "`authoring=compatibility`",
        "python -m chirp_ui find --maturity=experimental",
        "No registry change unless a later implementation plan promotes it.",
    ]:
        assert contract in section


def test_public_surface_stabilization_doc_is_indexed() -> None:
    assert "[PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md)" in (
        INDEX.read_text(encoding="utf-8")
    )


def test_design_system_research_points_to_public_surface_labels() -> None:
    """Research direction should route maturity labels through the canonical doc."""
    text = DESIGN_RESEARCH.read_text(encoding="utf-8")

    assert "[PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md)" in text
    assert "evidence-label glossary" in text


def test_design_system_research_has_component_parity_matrix() -> None:
    """External comparison should stay framed as strategy input, not API proof."""
    text = DESIGN_RESEARCH.read_text(encoding="utf-8")
    section = text.split("## Component/Feature/Primitive Parity Matrix", 1)[1].split(
        "## Core Findings", 1
    )[0]

    for source in [
        "[shadcn/ui components](https://ui.shadcn.com/docs/components)",
        "[shadcn/ui blocks](https://ui.shadcn.com/blocks)",
        "[Material Design 3 components](https://m3.material.io/components)",
        "[Carbon components overview](https://carbondesignsystem.com/components/overview/components/)",
        "[Shopify Polaris components](https://polaris.shopify.com/components)",
        "[Atlassian components](https://atlassian.design/components)",
    ]:
        assert source in text

    for column in [
        "Chirp UI Today",
        "shadcn/ui",
        "Material Design 3",
        "Carbon",
        "Shopify Polaris",
        "Atlassian Design System",
        "Chirp UI Strategy",
    ]:
        assert column in section

    for surface in [
        "Distribution and discovery",
        "Layout primitives",
        "App/site shell",
        "Navigation hierarchy",
        "Page header and actions",
        "Dense data and object browsing",
        "Agent/readiness metadata",
    ]:
        assert f"| {surface} |" in section

    for boundary in [
        "requirements proxy, not promotion evidence",
        "not chase raw component count",
        "copied-source/Tailwind model conflicts",
        "contract maturity, not more names",
        "components, docs, generated CSS, manifests, tests, and agents all agree",
    ]:
        assert boundary in section


def test_every_experimental_public_template_has_disposition() -> None:
    """New experimental public macros must get a pre-1.0 disposition row."""
    text = DOC.read_text(encoding="utf-8")
    manifest = build_manifest()
    missing: list[str] = []
    for name, entry in sorted(manifest["components"].items()):
        if entry["template"] and entry["maturity"] == "experimental":
            row_prefix = f"| `{name}` | "
            if row_prefix not in text:
                missing.append(name)

    assert not missing, "missing public-surface dispositions: " + ", ".join(missing)


def test_promoted_public_surface_rows_have_manifest_test_and_showcase_proof() -> None:
    """Promoting an experimental component to stable requires collateral proof."""
    text = DOC.read_text(encoding="utf-8")
    tests = COMPONENT_TESTS.read_text(encoding="utf-8") + ASCII_TESTS.read_text(encoding="utf-8")
    showcase = SHOWCASE.read_text(encoding="utf-8")
    manifest = build_manifest()["components"]
    promoted = [
        line.split("|")[1].strip().strip("`")
        for line in text.splitlines()
        if "| Promote to stable |" in line and line.startswith("| `")
    ]

    assert promoted
    for name in promoted:
        css_class = f"chirpui-{name}"
        assert manifest[name]["maturity"] == "stable"
        assert css_class in tests, name
        assert css_class in showcase, name


def test_recipe_only_rows_remain_pattern_role_and_not_preferred() -> None:
    """Recipe-only decisions should not leak into preferred component vocabulary."""
    text = DOC.read_text(encoding="utf-8")
    manifest = build_manifest()["components"]
    recipe_only = [
        line.split("|")[1].strip().strip("`")
        for line in text.splitlines()
        if "| Recipe-only |" in line and line.startswith("| `")
    ]

    assert recipe_only
    for name in recipe_only:
        entry = manifest[name]
        assert entry["role"] == "pattern", name
        assert entry["maturity"] == "experimental", name
        assert entry["authoring"] != "preferred", name


def test_experimental_disposition_tracks_have_required_proof_rows() -> None:
    """The inventory's track labels should be backed by proof guidance."""
    text = DOC.read_text(encoding="utf-8")
    proof_section = text.split("## Proof Tracks", 1)[1].split("## Next Batches", 1)[0]
    inventory = text.split("## Experimental Disposition Inventory", 1)[1].split(
        "## Legacy Helper Authoring Policy", 1
    )[0]
    proof_tracks = {
        line.split("|")[1].strip()
        for line in proof_section.splitlines()
        if line.startswith("| ") and not line.startswith("| ---") and "Required proof" not in line
    }
    inventory_tracks = {
        line.split("|")[3].strip().split(";", 1)[0].rstrip(".")
        for line in inventory.splitlines()
        if line.startswith("| `")
    }

    assert inventory_tracks <= proof_tracks


def test_public_surface_closure_batches_cover_open_decision_families() -> None:
    text = DOC.read_text(encoding="utf-8")
    section = text.split("## Closure Batches", 1)[1].split("## Next Batches", 1)[0]

    for batch in [
        "ASCII/TUI controls",
        "Marketing patterns",
        "Motion/effects",
        "Form and controls",
        "Recipe-only patterns",
    ]:
        assert f"| {batch} |" in section

    for proof in [
        "ARIA, keyboard, reduced-motion, render, and browser proof",
        "responsive pattern docs and visual audit coverage",
        "reduced-motion and visual/browser proof",
        "focus, keyboard, invalid-state, overflow, and render proof",
        "pattern-role and non-preferred",
    ]:
        assert proof in section
