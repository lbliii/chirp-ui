from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PRIMITIVES = REPO_ROOT / "docs" / "PRIMITIVES.md"
ANTI_FOOTGUNS = REPO_ROOT / "docs" / "ANTI-FOOTGUNS.md"
PUBLIC_SURFACE = REPO_ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"


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
