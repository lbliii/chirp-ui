from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "PUBLIC-SURFACE-STABILIZATION.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"


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
