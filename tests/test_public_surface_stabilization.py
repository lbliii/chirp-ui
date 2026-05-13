from pathlib import Path

from chirp_ui.manifest import build_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
SHOWCASE = REPO_ROOT / "examples" / "design-system-gap-showcase" / "index.html"
COMPONENT_TESTS = REPO_ROOT / "tests" / "test_components.py"


def test_public_surface_stabilization_doc_records_current_slice() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "Promote to stable",
        "Keep experimental",
        "`logo-cloud` | Promote to stable",
        "`story-card` | Promote to stable",
        "`cta-band` | Promote to stable",
        "`ascii-badge` | Keep experimental",
        "`ascii-progress` | Keep experimental",
        "`ascii-table` | Keep experimental",
        "`ascii-toggle` | Keep experimental",
        "no private theme token namespace",
    ]:
        assert required in text


def test_public_surface_stabilization_doc_is_indexed() -> None:
    assert "[PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md)" in (
        INDEX.read_text(encoding="utf-8")
    )


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
    tests = COMPONENT_TESTS.read_text(encoding="utf-8")
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
