"""Accuracy ratchets for cross-repository integration guidance."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHIRP_UI_GUIDE = "https://lbliii.github.io/chirp/docs/build-apps/ui-extensions/chirp-ui/"
STALE_CHIRP_UI_GUIDE = "https://lbliii.github.io/chirp/docs/guides/chirp-ui/"


def test_kida_starlette_guidance_uses_shipped_adapter_name() -> None:
    integration_docs = ROOT / "docs" / "integration"

    for path in integration_docs.glob("*.md"):
        assert "KidaStarlette" not in path.read_text(encoding="utf-8"), path


def test_chirp_ui_guide_links_use_current_documentation_path() -> None:
    roots = (ROOT / "docs", ROOT / "site" / "content", ROOT / "examples")
    markdown_files = (path for root in roots for path in root.rglob("*.md"))

    for path in markdown_files:
        assert STALE_CHIRP_UI_GUIDE not in path.read_text(encoding="utf-8"), path

    capability_matrix = (ROOT / "docs" / "integration" / "capability-matrix.md").read_text(
        encoding="utf-8"
    )
    upgrade_pitch = capability_matrix.split("## Upgrade pitch", 1)[1].split("\n## ", 1)[0]
    assert CHIRP_UI_GUIDE in upgrade_pitch


def test_kida_overlap_audit_is_indexed() -> None:
    docs_index = (ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8")

    assert "integration/kida-overlap-audit.md" in docs_index


def test_django_safe_wrapper_names_its_trust_boundary() -> None:
    django_guide = (ROOT / "docs" / "integration" / "django.md").read_text(encoding="utf-8")
    overlap_audit = (ROOT / "docs" / "integration" / "kida-overlap-audit.md").read_text(
        encoding="utf-8"
    )

    assert "These are narrow trust boundaries" in django_guide
    assert "Never pass" in django_guide
    assert "never request data" in overlap_audit
    assert "user-authored HTML" in overlap_audit
