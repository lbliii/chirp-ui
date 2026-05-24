from chirp_ui.components import COMPONENTS
from tests.helpers import REPO_ROOT

PRIMITIVES = REPO_ROOT / "docs" / "fundamentals" / "primitives.md"
ANTI_FOOTGUNS = REPO_ROOT / "docs" / "safety" / "anti-footguns.md"
PUBLIC_SURFACE = REPO_ROOT / "docs" / "safety" / "public-surface-stabilization.md"
PRIMITIVE_PLAN = REPO_ROOT / "docs" / "plans" / "done" / "PLAN-primitive-vocabulary-hardening.md"


def test_primitive_docs_record_spacing_shortcut_deprecation_boundary() -> None:
    text = PRIMITIVES.read_text(encoding="utf-8")

    for required in [
        "Spacing shortcuts are **deprecate later** candidates.",
        "New first-party examples",
        "`mt-sm`, `mt-md`, or `mb-md`",
        "STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md",
        "only `visually-hidden` remains",
    ]:
        assert required in text


def test_anti_footguns_names_deprecate_later_spacing_shortcuts() -> None:
    text = ANTI_FOOTGUNS.read_text(encoding="utf-8")

    assert ".chirpui-mt-sm" in text
    assert ".chirpui-mt-md" in text
    assert ".chirpui-mb-md" in text
    assert "deprecate-later spacing shortcuts" in text


def test_public_surface_policy_separates_preferred_and_compatibility() -> None:
    text = PUBLIC_SURFACE.read_text(encoding="utf-8")

    for required in [
        "Legacy Helper Authoring Policy",
        "1.0 Helper Decision Gate",
        "No helper removal is approved by this document alone.",
        "`authoring=compatibility`",
        "`find --authoring preferred` should not include utility-like typography",
        "`mt-sm`, `mt-md`, and `mb-md` are deprecate-later candidates",
        "Zero first-party usage outside legacy examples.",
        "`visually-hidden`, `focus-ring`, and `list-reset` stay narrow",
    ]:
        assert required in text


def test_primitive_plan_names_every_legacy_primitive_decision() -> None:
    """The residual primitive plan is the human-readable companion to the manifest ratchet."""
    text = PRIMITIVE_PLAN.read_text(encoding="utf-8")
    legacy_primitives = {
        name
        for name, desc in COMPONENTS.items()
        if desc.resolved_role == "primitive" and desc.resolved_maturity == "legacy"
    }

    missing = [name for name in sorted(legacy_primitives) if f"`{name}`" not in text]
    assert not missing, "legacy primitives missing plan decisions: " + ", ".join(missing)
