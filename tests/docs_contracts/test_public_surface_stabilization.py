from chirp_ui.manifest import build_manifest
from tests.helpers import REPO_ROOT

DOC = REPO_ROOT / "docs" / "safety" / "public-surface-stabilization.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
DESIGN_RESEARCH = REPO_ROOT / "docs" / "decisions" / "design-system-research.md"
SHOWCASE = REPO_ROOT / "examples" / "design-system-gap-showcase" / "index.html"
COMPONENT_TESTS = REPO_ROOT / "tests" / "test_components.py"
ASCII_TESTS = REPO_ROOT / "tests" / "test_ascii_components.py"

# #203 maturity honesty — proof corpus the stable-composition-wrapper rule reads.
# Concatenated source of every test we accept as "more than a class-string"
# proof (a11y attribute / slot-forward render / browser gauntlet). Hygiene
# assertion (4c) below fails if a named proof test goes missing from this corpus.
PROOF_TEST_CORPUS_FILES = (
    REPO_ROOT / "tests" / "test_components.py",
    REPO_ROOT / "tests" / "test_elbysodic_primitives.py",
    REPO_ROOT / "tests" / "test_manifest_signatures.py",
    REPO_ROOT / "tests" / "browser" / "test_gauntlet.py",
    REPO_ROOT / "tests" / "browser" / "test_compact_header_candidate.py",
)

# #203 maturity honesty — the justified-allowlist escape (path B) for the
# structural composes-rule. A `stable` component that composes other registry
# components (non-empty ``composes``) is a composition wrapper and must carry the
# same proof collateral as any stable promotion. Each entry names the asserting
# proof test (a11y attribute / slot-forward render) that defends it. ``cta-band``
# is intentionally ABSENT — it is a documented "Promote to stable" doc row
# (path A) whose collateral the existing
# ``test_promoted_public_surface_rows_have_manifest_test_and_showcase_proof``
# already enforces. See docs/safety/public-surface-stabilization.md
# § Stable Composition Wrappers.
STABLE_COMPOSERS_WITH_PROOF: dict[str, str] = {
    "document-header": "test_document_header_yielded_actions_slot",
    "empty-panel-state": "test_empty_panel_state_actions_slot",
    "file-tree": "test_file_tree_forwards_branch_mode_to_nav_tree",
    "saved-view-strip": "test_saved_view_strip_renders_selected_views",
    "scope-switcher": "test_scope_switcher_renders_dropdown_scope_control",
}


def _promoted_to_stable_rows(text: str) -> list[str]:
    """Component names from the doc's ``| Promote to stable |`` rows."""
    return [
        line.split("|")[1].strip().strip("`")
        for line in text.splitlines()
        if "| Promote to stable |" in line and line.startswith("| `")
    ]


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
    assert "[PUBLIC-SURFACE-STABILIZATION.md](safety/public-surface-stabilization.md)" in (
        INDEX.read_text(encoding="utf-8")
    )


def test_design_system_research_points_to_public_surface_labels() -> None:
    """Research direction should route maturity labels through the canonical doc."""
    text = DESIGN_RESEARCH.read_text(encoding="utf-8")

    assert "[PUBLIC-SURFACE-STABILIZATION.md](../safety/public-surface-stabilization.md)" in text
    assert "evidence-label glossary" in text


def test_design_system_research_routes_reference_proof_to_analysis_ledger() -> None:
    """Market research should feed proof analysis, not direct public API promotion."""
    text = DESIGN_RESEARCH.read_text(encoding="utf-8")
    section = text.split("### Evidence Model Without A Userbase", 1)[1].split(
        "### Wave 5: Bengal-Driven Primitive Maturation", 1
    )[0]
    normalized = " ".join(section.split())

    for required in [
        "Scenario-complete non-Bengal reference implementations",
        "Browser, render, server, escaping, and generated-output tests",
        "`docs/reference-implementations/PROOF-ANALYSIS.md`",
        "source-only ledger",
        "recipe guidance",
        "another independent reference",
        "stop-and-ask public API plan",
        "`docs/reference-implementations/RECIPE-GUIDANCE.md`",
        "source-only authoring layer",
        "keep current primitives and teach the recipe",
        "Explicit stop-and-ask before any public macro/API",
    ]:
        assert required in normalized


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
    promoted = _promoted_to_stable_rows(text)

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


def test_no_thin_composition_wrapper_is_stable_without_proof() -> None:
    """#203 maturity honesty — a stable composition wrapper must carry proof.

    The objective "thin composition-wrapper" signal is the first-class
    ``composes`` descriptor field (manifest-projected, round-trip-pinned by
    ``test_manifest.py``). Any component that ships ``maturity=stable`` while
    composing other registry components must be proof-backed via EITHER:

    * (A) a documented ``| Promote to stable |`` row in this doc — whose
      manifest+render+showcase collateral
      ``test_promoted_public_surface_rows_have_manifest_test_and_showcase_proof``
      already enforces; OR
    * (B) a ``STABLE_COMPOSERS_WITH_PROOF`` allowlist entry naming an asserting
      proof test (a11y attribute / slot-forward render / browser gauntlet).

    This catches the CLASS: ``data_table`` shipped ``stable`` with
    ``composes=("filter-row","table","pagination")`` and neither (A) nor (B)
    before #200 demoted it — this test would have flagged it as a violator. It
    provably does NOT fire on complete/low-feature primitives
    (``table``/``table-wrap``/``calendar``/``bar_chart``/``donut``) or the ASCII
    set, all of which have empty ``composes``.
    """
    text = DOC.read_text(encoding="utf-8")
    components = build_manifest()["components"]
    promoted = set(_promoted_to_stable_rows(text))

    stable_composers = sorted(
        name
        for name, entry in components.items()
        if entry["maturity"] == "stable" and entry["composes"]
    )

    # (1)-(3): every stable composer is path A (doc row) OR path B (allowlist).
    violators = [
        name
        for name in stable_composers
        if name not in promoted and name not in STABLE_COMPOSERS_WITH_PROOF
    ]
    assert not violators, (
        "stable component(s) compose other registry components but carry no "
        "promotion proof: "
        + ", ".join(violators)
        + ". Fix each by adding a `Promote to stable` doc row with proof, adding "
        "a STABLE_COMPOSERS_WITH_PROOF allowlist entry naming its proof test, or "
        "demoting it to experimental."
    )

    # (4a) no stale allowlist keys — every entry is still stable-with-composes.
    stale_keys = [name for name in STABLE_COMPOSERS_WITH_PROOF if name not in stable_composers]
    assert not stale_keys, (
        "STABLE_COMPOSERS_WITH_PROOF has stale entries no longer stable-with-composes: "
        + ", ".join(stale_keys)
    )

    # (4b) no overlap — a stable composer has exactly one canonical proof source.
    overlap = sorted(set(STABLE_COMPOSERS_WITH_PROOF) & promoted)
    assert not overlap, (
        "stable composer(s) are BOTH a `Promote to stable` doc row and an "
        "allowlist entry; keep exactly one proof source per component: " + ", ".join(overlap)
    )

    # (4c) each named proof-test identifier still exists in the proof corpus, so
    # deleting the proof breaks this gate (the allowlist cannot rot into a hollow
    # justification).
    corpus = "".join(path.read_text(encoding="utf-8") for path in PROOF_TEST_CORPUS_FILES)
    missing_proof = [
        f"{name} -> {test_id}"
        for name, test_id in STABLE_COMPOSERS_WITH_PROOF.items()
        if test_id not in corpus
    ]
    assert not missing_proof, (
        "STABLE_COMPOSERS_WITH_PROOF names proof test(s) absent from the proof corpus: "
        + ", ".join(missing_proof)
    )
