import tomllib

from tests.helpers import REPO_ROOT

PYPROJECT = REPO_ROOT / "pyproject.toml"
DOC = REPO_ROOT / "docs" / "safety" / "verification.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"


def test_verify_generated_task_groups_generated_artifact_checks() -> None:
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    tasks = data["tool"]["poe"]["tasks"]

    assert tasks["verify-generated"]["sequence"] == [
        "build-css-check",
        "build-manifest-check",
        "build-docs-check",
        "build-component-index-check",
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
    assert tasks["test-browser-chrome"]["sequence"] == [
        "docs-build-all",
        "test-browser-chrome-check",
    ]
    assert tasks["test-browser-chrome-check"]["cmd"].startswith(
        "pytest tests/browser/test_rail_to_tray_chrome.py"
    )
    assert (
        "tests/browser/test_application_chrome_gauntlet.py"
        in tasks["test-browser-chrome-check"]["cmd"]
    )
    assert "tests/browser/test_bengal_docs_chrome.py" in tasks["test-browser-chrome-check"]["cmd"]
    assert tasks["ci-browser"]["sequence"] == ["test-browser"]
    assert coverage["fail_under"] == 80


def test_verification_doc_names_locked_environment_and_kida_failure() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "uv run poe verify-generated",
        "uv run poe build-css-check",
        "uv run poe build-manifest-check",
        "uv run poe build-docs-check",
        "uv run poe build-component-index-check",
        "make release-preflight",
        "uv run python -m chirp_ui.manifest --json",
        "Kida Mismatch Failure",
        "locked project environment",
        "Gate Policy",
        "uv run poe test-cov",
        "uv run poe ci-browser",
        "uv run poe test-browser-chrome",
        "Bengal docs chrome",
        "fail_under = 80",
        "Browser tests stay outside",
    ]:
        assert required in text


def test_verification_doc_routes_browser_sensitive_proof() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "## Proof Routing",
        "Registry, manifest schema, generated CSS, generated component docs",
        "uv run poe verify-generated",
        "Kida macros, escaping, structured attrs, HTMX attributes",
        "uv run poe test-js",
        "Token, CSS partial, cascade layer, or scope behavior",
        "Dialog, focus, overflow, htmx lifecycle, Alpine lifecycle, responsive layout",
        "uv run poe ci-browser",
        "Application chrome rail/tray, command focus, route-tab scroll, badge stability",
        "uv run poe test-browser-chrome",
        "Search shells, facet rails, scoped counts, and responsive command surfaces",
        "320px, 390px, 768px, 1024px, and desktop width",
        "uv run poe docs-build-all",
        "Theme packages, Bengal templates, packaged assets",
    ]:
        assert required in text


def test_verification_doc_is_indexed() -> None:
    assert "[VERIFICATION.md](safety/verification.md)" in INDEX.read_text(encoding="utf-8")
