import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
DOC = REPO_ROOT / "docs" / "VERIFICATION.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"


def test_verify_generated_task_groups_generated_artifact_checks() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    tasks = data["tool"]["poe"]["tasks"]

    assert tasks["verify-generated"]["sequence"] == [
        "build-css-check",
        "build-manifest-check",
        "build-docs-check",
    ]
    assert "verify-generated" in tasks["ci"]["sequence"]
    assert "verify-generated" in tasks["check"]["sequence"]


def test_verification_gate_policy_matches_poe_tasks() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    tasks = data["tool"]["poe"]["tasks"]
    coverage = data["tool"]["coverage"]["report"]

    assert "test-js" in tasks["ci"]["sequence"]
    assert "test-cov" not in tasks["ci"]["sequence"]
    assert "test-browser" not in tasks["ci"]["sequence"]
    assert tasks["ci-browser"]["sequence"] == ["test-browser"]
    assert coverage["fail_under"] == 80


def test_verification_doc_names_locked_environment_and_kida_failure() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "uv run poe verify-generated",
        "uv run poe build-css-check",
        "uv run poe build-manifest-check",
        "uv run poe build-docs-check",
        "make release-preflight",
        "uv run python -m chirp_ui.manifest --json",
        "Kida Mismatch Failure",
        "locked project environment",
        "Gate Policy",
        "uv run poe test-cov",
        "uv run poe ci-browser",
        "fail_under = 80",
        "Browser tests stay outside",
    ]:
        assert required in text


def test_verification_doc_is_indexed() -> None:
    assert "[VERIFICATION.md](VERIFICATION.md)" in INDEX.read_text(encoding="utf-8")
