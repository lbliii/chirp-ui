import re

from tests.helpers import REPO_ROOT
from tests.layout_affinity_contract import ALLOWED_SOURCE_VALUES, RESOLVER_MATRIX

RFC = REPO_ROOT / "docs" / "DESIGN-layout-affinity.md"
AUTHORING = REPO_ROOT / "docs" / "LAYOUT-AFFINITY-RESOLVER-AUTHORING.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
PRIMITIVES = REPO_ROOT / "docs" / "PRIMITIVES.md"
PLAN = REPO_ROOT / "docs" / "plans" / "done" / "PLAN-layout-affinity-rollout.md"
BROWSER_PROOF = REPO_ROOT / "tests" / "browser" / "test_catalog_shell_recipe.py"
SOURCE_GLOBS = (
    "src/chirp_ui/templates/chirpui/**/*.html",
    "examples/component-showcase/templates/**/*.html",
)

ATTR_RE = re.compile(r'\b(data-chirpui-(?:role|pressure|affinity|rhythm))="([^"]*)"')


def test_layout_affinity_rfc_defines_recipe_first_contract() -> None:
    text = RFC.read_text(encoding="utf-8")

    for required in [
        "Status: proposed recipe-first contract",
        "data-chirpui-role",
        "data-chirpui-pressure",
        "data-chirpui-affinity",
        "Status Block",
        "Prototype recipe attributes",
        "Not yet descriptor API",
        "Not yet manifest contract",
        "Allowed only where documented parent resolvers consume them",
        "Authoring Vocabulary Contract",
        "Prototype-supported values currently emitted in source templates",
        "Resolver Model",
        "LAYOUT-AFFINITY-RESOLVER-AUTHORING.md",
        "First Prototype",
        "Second Prototype",
        "filter_bar",
        "Third Prototype",
        "card",
        "component-owned internal layout-affinity contract",
        "Micro-Resolver Prototype",
        "not promoted",
        "Workspace Shell Resolver",
        "workspace_shell",
        "inspector/workspace resolver",
        "Payoff Experiment",
        "operations workspace shell",
        "support queue shell",
        "repeats the same",
        "does not promote",
        "operations shell remains the baseline page-owned version",
        "Boilerplate Comparison",
        "Structural owner",
        "Operations shell",
        "Operations shell workspace variant",
        "Support shell",
        "/operations-shell-workspace",
        "Decision: keep `/operations-shell` as the baseline route",
        "For Agents",
        "Descriptor And Manifest Readiness",
        "layout_resolver",
        "layout_parts",
        "chirpui-manifest@6",
        "HTML/CSS contracts only",
        "Agent Contract",
        "No utility classes",
        "No public macro params until repeated use proves the vocabulary",
    ]:
        assert required in text


def test_layout_affinity_rfc_is_discoverable_from_docs_index_and_primitives() -> None:
    assert "[DESIGN-layout-affinity.md](DESIGN-layout-affinity.md)" in INDEX.read_text(
        encoding="utf-8"
    )
    assert "[DESIGN-layout-affinity.md](DESIGN-layout-affinity.md)" in PRIMITIVES.read_text(
        encoding="utf-8"
    )
    plan_link = "[PLAN-layout-affinity-rollout.md](plans/done/PLAN-layout-affinity-rollout.md)"
    authoring_link = (
        "[LAYOUT-AFFINITY-RESOLVER-AUTHORING.md](LAYOUT-AFFINITY-RESOLVER-AUTHORING.md)"
    )
    assert plan_link in INDEX.read_text(encoding="utf-8")
    assert plan_link in PRIMITIVES.read_text(encoding="utf-8")
    assert plan_link in RFC.read_text(encoding="utf-8")
    assert authoring_link in INDEX.read_text(encoding="utf-8")
    assert authoring_link in PRIMITIVES.read_text(encoding="utf-8")
    assert authoring_link in RFC.read_text(encoding="utf-8")


def test_layout_affinity_resolver_authoring_guide_sets_safe_authoring_contract() -> None:
    text = AUTHORING.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    for required in [
        "Status: prototype authoring guide",
        "Prototype recipe attributes",
        "Not yet descriptor API",
        "Not yet manifest contract",
        "Allowed only where documented parent resolvers consume them",
        "layout_resolver",
        "layout_parts",
        "not descriptor fields, macro parameters, manifest keys, or public Python API",
        "Pick the parent owner",
        "Pick the scope",
        "Use only documented vocabulary",
        "Write CSS in the owning partial",
        "Prove selector boundaries",
        "Prove browser behavior",
        "direct-children",
        "component-owned part classes",
        "broad descendant selectors",
        "Current Resolver Matrix",
        "`command_bar`",
        "`filter_bar`",
        "`card`",
        "`frame`",
        "`stack` and `cluster` are intentionally absent",
        "Manifest tests continue to prove no `layout_resolver`, `layout_parts`, or",
        "Promotion to descriptor fields or `chirpui-manifest@6` is a separate public API",
    ]:
        assert required in text or required in normalized

    for forbidden_example in [
        '.chirpui-command-bar [data-chirpui-pressure~="flex"]',
        '.chirpui-card :scope [data-chirpui-pressure~="compress"]',
        '.chirpui-stack > [data-chirpui-affinity~="fill"]',
    ]:
        assert forbidden_example in text


def test_layout_affinity_source_values_stay_in_documented_vocabulary() -> None:
    offenders: list[str] = []

    for pattern in SOURCE_GLOBS:
        for path in sorted(REPO_ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8")
            for attr, raw_value in ATTR_RE.findall(text):
                offenders.extend(
                    f"{path.relative_to(REPO_ROOT)}: {attr}={value!r}"
                    for value in raw_value.split()
                    if value not in ALLOWED_SOURCE_VALUES[attr]
                )

    assert not offenders, "undocumented layout-affinity source values: " + "; ".join(offenders)


def test_layout_affinity_rfc_lists_every_allowed_source_value() -> None:
    text = RFC.read_text(encoding="utf-8")

    for attr, values in ALLOWED_SOURCE_VALUES.items():
        assert f"`{attr}`" in text
        for value in values:
            assert f"`{value}`" in text


def test_layout_affinity_resolver_matrix_has_docs_css_and_browser_proof() -> None:
    docs = RFC.read_text(encoding="utf-8") + "\n" + PLAN.read_text(encoding="utf-8")
    browser = BROWSER_PROOF.read_text(encoding="utf-8")

    for resolver, proof in RESOLVER_MATRIX.items():
        assert proof["css"].is_file(), resolver
        css = proof["css"].read_text(encoding="utf-8")
        assert "data-chirpui-" in css, resolver
        for docs_term in proof["docs"]:
            assert docs_term in docs, f"{resolver} missing docs term {docs_term!r}"
        assert proof["browser"] in browser, resolver
