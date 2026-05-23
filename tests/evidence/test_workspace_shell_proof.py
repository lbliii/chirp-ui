from tests.helpers import REPO_ROOT

PROOF = REPO_ROOT / "docs" / "WORKSPACE-SHELL-PROOF.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
BASELINE = REPO_ROOT / "examples/component-showcase/templates/showcase/operations_shell.html"
WORKSPACE = (
    REPO_ROOT / "examples/component-showcase/templates/showcase/operations_shell_workspace.html"
)
SUPPORT = REPO_ROOT / "examples/component-showcase/templates/showcase/support_shell.html"


def test_workspace_shell_proof_names_comparison_surfaces() -> None:
    text = PROOF.read_text(encoding="utf-8")

    for required in [
        "Status: promotion proof",
        "/operations-shell",
        "/operations-shell-workspace",
        "same operations data",
        "registry-cited primitives",
        "Do not promote layout-affinity fields into the manifest yet",
    ]:
        assert required in text

    assert "[WORKSPACE-SHELL-PROOF.md](WORKSPACE-SHELL-PROOF.md)" in INDEX.read_text(
        encoding="utf-8"
    )


def test_operations_workspace_variant_uses_dense_primitives_not_page_owned_shell() -> None:
    baseline = BASELINE.read_text(encoding="utf-8")
    workspace = WORKSPACE.read_text(encoding="utf-8")

    assert 'class="ops-shell-workspace"' in baseline
    assert "ops-shell-rail-link" in baseline
    assert "ops-shell-card-grid" in baseline

    for promoted in [
        "filter_rail(",
        "filter_rail_item(",
        "metric_strip(",
        "metric_item(",
        "result_collection(",
        "result_card(",
        "inspector_panel(",
    ]:
        assert promoted in workspace

    for page_owned in [
        'class="ops-shell-workspace"',
        "ops-shell-rail-link",
        "ops-shell-card-grid",
    ]:
        assert page_owned not in workspace


def test_support_shell_uses_dense_primitives_not_page_owned_inner_shapes() -> None:
    support = SUPPORT.read_text(encoding="utf-8")

    for promoted in [
        "filter_rail(",
        "filter_rail_item(",
        "metric_strip(",
        "metric_item(",
        "result_collection(",
        "result_card(",
        "inspector_panel(",
    ]:
        assert promoted in support

    for page_owned in [
        "support-shell-rail-link",
        "support-shell-card-grid",
        "{% call card(",
        'from "chirpui/card.html" import card',
    ]:
        assert page_owned not in support
