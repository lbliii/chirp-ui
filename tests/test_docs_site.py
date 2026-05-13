import importlib.util
import os
import re
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE_SCRIPT = REPO_ROOT / "scripts" / "docs_site.py"
PYPROJECT = REPO_ROOT / "pyproject.toml"
AGENT_SOURCE_INVENTORY = REPO_ROOT / "docs" / "AGENT-SOURCE-INVENTORY.md"
AGENT_SOURCE_MAP = REPO_ROOT / "docs" / "AGENT-SOURCE-MAP.md"
AGENT_CURATED_SNIPPETS = REPO_ROOT / "docs" / "AGENT-CURATED-SNIPPETS.md"
PATTERN_DOCS = {
    "navigation.md": "docs/NAVIGATION.md",
    "product-pages.md": "docs/PRODUCT-PAGE-PATTERNS.md",
    "media-sites.md": "docs/MEDIA-SITE-PATTERNS.md",
    "forums.md": "docs/FORUM-SITE-PATTERNS.md",
}
NAVIGATION_PATTERN_COLLATERAL = [
    "docs/DENSE-NAVIGATION-RECIPES.md",
    "docs/plans/PLAN-application-chrome-system.md",
]
COMPONENT_DOCS = {
    "appearance-tone.md": "docs/APPEARANCE-TONE.md",
    "dropdowns.md": "docs/DROPDOWN-ANATOMY.md",
    "drawers-trays.md": "docs/DRAWER-TRAY-ANATOMY.md",
    "modals.md": "docs/MODAL-ANATOMY.md",
    "tabs.md": "docs/TABS-ANATOMY.md",
}
THEME_DOCS = {
    "bengal-theme-controls.md": "docs/BENGAL-THEME-ANATOMY.md",
    "chirp-theme.md": "docs/CHIRP-THEME.md",
}
DOCS_IA_MIGRATION = REPO_ROOT / "docs" / "DOCS-IA-MIGRATION.md"
DOCS_INDEX = REPO_ROOT / "site" / "content" / "docs" / "_index.md"
INSTALL_DOC = REPO_ROOT / "site" / "content" / "docs" / "get-started" / "installation.md"
SOURCE_ELIGIBILITY = {
    "source-only",
    "candidate-review",
    "copyable-curated",
    "excluded",
}
FORBIDDEN_SNIPPET_PREFIXES = (
    "examples/static-showcase/",
    "site/public/",
    "tests/browser/",
    "site/content/",
)
BENGAL_OWNED_OUTPUTS = {
    "site/public/llms.txt",
    "site/public/agent.json",
    "site/public/index.json",
    "site/public/search-index.json",
    "site/public/**/*.json page projections",
    "site/public/**/*.md page projections",
    "site/public/sitemap.xml",
    "site/public/robots.txt",
}
FORBIDDEN_OUTPUT_NAMES = (
    "llms.txt",
    "llms-full.txt",
    "agent.json",
    "index.json",
    "search-index.json",
    "sitemap.xml",
    "robots.txt",
)


def _load_docs_site_module():
    spec = importlib.util.spec_from_file_location("chirp_ui_docs_site", DOCS_SITE_SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_markdown_table(text: str, heading: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError as exc:
        raise AssertionError(f"Missing markdown heading: {heading}") from exc

    table_lines: list[str] = []
    for line in lines[start + 1 :]:
        if not line.strip():
            if table_lines:
                break
            continue
        if not line.startswith("|"):
            if table_lines:
                break
            continue
        table_lines.append(line)

    assert len(table_lines) >= 3, f"Expected a markdown table after {heading}"
    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        rows.append(dict(zip(headers, cells, strict=True)))
    return rows


def _inventory_source_path(raw: str) -> str:
    return raw.split(" as ", 1)[0].split("#", 1)[0].strip()


def _plain_cell(value: str) -> str:
    return value.replace("`", "")


def test_build_bengal_env_prepends_workspace_repo(monkeypatch, tmp_path: Path) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setenv("PYTHONPATH", "existing-path")

    env = module._build_bengal_env()

    assert env["PYTHONPATH"] == str(workspace_bengal) + os.pathsep + "existing-path"


def test_install_doc_version_example_matches_project_metadata() -> None:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    text = INSTALL_DOC.read_text(encoding="utf-8")

    assert f'print(chirp_ui.__version__)  # e.g. "{project["version"]}"' in text
    assert "0.2.2" not in text


def test_docs_index_uses_site_directives_for_cards() -> None:
    text = DOCS_INDEX.read_text(encoding="utf-8")

    assert "API Reference" not in text
    assert ":link: ./components/" in text
    assert '<div class="chirpui-grid' not in text
    assert 'class="chirpui-card' not in text
    assert ":::{cards}" in text
    assert ":::{card} Component Reference" in text


def test_ensure_workspace_bengal_accepts_workspace_checkout(monkeypatch, tmp_path: Path) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setattr(
        module,
        "_resolve_bengal_origin",
        lambda _env: workspace_bengal / "bengal" / "__init__.py",
    )

    module._ensure_workspace_bengal({})


def test_ensure_workspace_bengal_rejects_site_packages(monkeypatch, tmp_path: Path, capsys) -> None:
    module = _load_docs_site_module()
    workspace_bengal = tmp_path / "b-stack" / "bengal"
    workspace_bengal.mkdir(parents=True)

    monkeypatch.setattr(module, "_WORKSPACE_BENGAL", workspace_bengal)
    monkeypatch.setattr(
        module,
        "_resolve_bengal_origin",
        lambda _env: (
            tmp_path / ".venv" / "lib" / "python3.14" / "site-packages" / "bengal" / "__init__.py"
        ),
    )

    with pytest.raises(SystemExit, match="1"):
        module._ensure_workspace_bengal({})

    stderr = capsys.readouterr().err
    assert "installed Bengal package" in stderr
    assert "uv run poe docs-serve" in stderr


def test_pattern_docs_are_published_site_sources() -> None:
    """The Bengal-published docs should expose the shipped 0.7 pattern families."""
    pattern_dir = REPO_ROOT / "site" / "content" / "docs" / "patterns"

    assert (pattern_dir / "_index.md").is_file()
    for filename, canonical_doc in PATTERN_DOCS.items():
        text = (pattern_dir / filename).read_text(encoding="utf-8")

        assert "type: doc" in text
        assert canonical_doc in text


def test_navigation_pattern_publishes_application_chrome_sources() -> None:
    text = (REPO_ROOT / "site" / "content" / "docs" / "patterns" / "navigation.md").read_text(
        encoding="utf-8"
    )
    matrix = DOCS_IA_MIGRATION.read_text(encoding="utf-8")

    for source in NAVIGATION_PATTERN_COLLATERAL:
        assert source in text
        assert source in matrix

    assert "Application chrome remains recipe-first" in text
    assert "recipe-first application chrome status" in matrix


def test_component_docs_are_published_site_sources() -> None:
    """Published component docs should point at canonical repository guides."""
    component_dir = REPO_ROOT / "site" / "content" / "docs" / "components"

    assert (component_dir / "_index.md").is_file()
    for filename, canonical_doc in COMPONENT_DOCS.items():
        text = (component_dir / filename).read_text(encoding="utf-8")

        assert "type: doc" in text
        assert canonical_doc in text


def test_theme_docs_are_published_site_sources() -> None:
    """Published theme docs should point at canonical repository guides."""
    theming_dir = REPO_ROOT / "site" / "content" / "docs" / "theming"

    assert (theming_dir / "_index.md").is_file()
    for filename, canonical_doc in THEME_DOCS.items():
        text = (theming_dir / filename).read_text(encoding="utf-8")

        assert "type: doc" in text
        assert canonical_doc in text


def test_docs_ia_migration_covers_all_published_docs_pages() -> None:
    """Sprint 4's IA matrix should name every published docs page source."""
    text = DOCS_IA_MIGRATION.read_text(encoding="utf-8")
    published_docs = sorted((REPO_ROOT / "site" / "content" / "docs").rglob("*.md"))

    assert published_docs
    for path in published_docs:
        rel = path.relative_to(REPO_ROOT).as_posix()
        assert rel in text


def test_docs_ia_migration_names_target_sections_and_endpoint_sources() -> None:
    """The IA matrix should pin the planned public sections and LLM provenance."""
    text = DOCS_IA_MIGRATION.read_text(encoding="utf-8")

    for section in (
        "Get Started",
        "Fundamentals",
        "Design System",
        "Components",
        "Patterns",
        "Integrations",
        "Agent Manifest",
        "Theming",
    ):
        assert f"| {section} |" in text

    for provenance in ("manifest-derived", "docs-derived", "example-derived"):
        assert provenance in text


def test_agent_source_inventory_paths_exist_and_name_provenance() -> None:
    """Sprint 6 source inventory should point at real source files/directories."""
    text = AGENT_SOURCE_INVENTORY.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text, "## Source Inventory")

    assert rows
    assert {row["Provenance"] for row in rows} >= {
        "manifest-derived",
        "docs-derived",
        "example-derived",
    }

    for row in rows:
        source = _inventory_source_path(row["Source"])
        eligibility = row["Snippet eligibility"]

        assert eligibility in SOURCE_ELIGIBILITY
        path = REPO_ROOT / source
        if source.endswith("/"):
            assert path.is_dir(), source
        else:
            assert path.is_file(), source


def test_agent_source_inventory_excludes_non_public_snippet_sources() -> None:
    """Copyable snippet sources must not come from generated/static/test surfaces."""
    text = AGENT_SOURCE_INVENTORY.read_text(encoding="utf-8")
    inventory_rows = _parse_markdown_table(text, "## Source Inventory")
    exclusion_rows = _parse_markdown_table(text, "## Snippet Exclusions")
    exclusions = {_plain_cell(row["Source or pattern"]) for row in exclusion_rows}

    for forbidden in (
        "examples/static-showcase/",
        "site/public/",
        "tests/browser/",
        "site/content/docs/ as snippets",
        "sc-*",
        "docs-*",
        "inline <script>",
        "attrs_unsafe",
        "raw chirpui-* class-heavy markup",
        "raw appearance/tone modifier classes",
    ):
        assert forbidden in exclusions

    for row in inventory_rows:
        if row["Snippet eligibility"] != "copyable-curated":
            continue
        source = _inventory_source_path(row["Source"])
        assert not source.startswith(FORBIDDEN_SNIPPET_PREFIXES), source


def test_agent_source_inventory_keeps_current_examples_review_gated() -> None:
    """Dynamic showcase templates are candidate sources, not automatic snippets."""
    text = AGENT_SOURCE_INVENTORY.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text, "## Source Inventory")
    candidates = [
        row
        for row in rows
        if row["Source"].startswith("examples/component-showcase/templates/showcase/")
    ]

    assert candidates
    assert {row["Snippet eligibility"] for row in candidates} == {"candidate-review"}
    assert "No `candidate-review` source is approved for automatic snippet extraction." in text


def test_agent_source_inventory_defines_copyable_snippet_review_gate() -> None:
    text = AGENT_SOURCE_INVENTORY.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text, "## Snippet Review Gate")

    gates = {row["Gate"] for row in rows}
    assert gates == {
        "Exact source path",
        "Macro-first shape",
        "Exclusion scan",
        "Runnable proof",
        "Provenance note",
    }
    assert "copyable-curated" in text
    assert "raw appearance/tone modifier classes" in text


def test_agent_curated_snippets_are_indexed_and_macro_first() -> None:
    inventory = AGENT_SOURCE_INVENTORY.read_text(encoding="utf-8")
    index = (REPO_ROOT / "docs" / "INDEX.md").read_text(encoding="utf-8")
    snippets = AGENT_CURATED_SNIPPETS.read_text(encoding="utf-8")

    assert "docs/AGENT-CURATED-SNIPPETS.md" in inventory
    assert "[AGENT-CURATED-SNIPPETS.md](AGENT-CURATED-SNIPPETS.md)" in index
    assert "Eligibility: `copyable-curated`" in snippets
    assert 'from "chirpui/card.html" import card' in snippets
    assert 'appearance="outlined"' in snippets
    assert 'tone="primary"' in snippets

    code_blocks = "\n".join(
        match.group(1) for match in re.finditer(r"```jinja\n(.*?)\n```", snippets, flags=re.S)
    )
    assert code_blocks
    for forbidden in [
        'class="chirpui-',
        "sc-",
        "docs-",
        "<script",
        "attrs_unsafe",
        "chirpui-card--",
    ]:
        assert forbidden not in code_blocks


def test_agent_source_map_names_generated_output_ownership() -> None:
    """Sprint 6 source map should preserve Bengal-owned output boundaries."""
    text = AGENT_SOURCE_MAP.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text, "## Generated Output Map")

    outputs = {_plain_cell(row["Generated output"]): row for row in rows}
    assert set(outputs) >= BENGAL_OWNED_OUTPUTS

    for output in BENGAL_OWNED_OUTPUTS:
        row = outputs[output]
        assert row["Owner"] == "Bengal"
        assert "docs-build-all" in row["Produced by"]

    manifest = outputs["site/public/chirpui.manifest.json"]
    assert manifest["Owner"] == "Chirp UI"
    assert "python -m chirp_ui.manifest --json" in manifest["Produced by"]

    showcase = outputs["site/public/showcase/index.html"]
    assert showcase["Owner"] == "Chirp UI assembly"
    assert "not a copyable snippet source" in showcase["Agent use"]


def test_agent_source_map_inputs_exist_and_reference_inventory() -> None:
    """Source inputs in the source map should point at real repo paths."""
    text = AGENT_SOURCE_MAP.read_text(encoding="utf-8")
    rows = _parse_markdown_table(text, "## Source Input Map")

    assert rows
    assert "docs/AGENT-SOURCE-INVENTORY.md" in text
    for row in rows:
        source = _inventory_source_path(row["Source input"].replace("*.html", ""))
        path = REPO_ROOT / source
        if row["Source input"].endswith("/"):
            assert path.is_dir(), row["Source input"]
        elif "*" not in row["Source input"]:
            assert path.is_file(), row["Source input"]


def test_agent_source_map_rejects_new_overlapping_artifact_names() -> None:
    """The source map should keep future Chirp artifacts distinct from Bengal outputs."""
    text = AGENT_SOURCE_MAP.read_text(encoding="utf-8")
    pyproject = PYPROJECT.read_text(encoding="utf-8")

    assert "No new Chirp-owned agent artifact is needed for Sprint 6." in text
    assert "site/public/chirpui.manifest.json" in text
    for name in FORBIDDEN_OUTPUT_NAMES:
        assert f"- `{name}`" in text

    assert "chirpui.agent.json" not in pyproject


def test_docs_build_tasks_do_not_override_ssg_agent_artifacts() -> None:
    """Bengal owns llms.txt and agent.json; Chirp UI should enrich sources only."""
    pyproject = PYPROJECT.read_text(encoding="utf-8")

    assert "build_llm_endpoints" not in pyproject
    assert "docs-emit-llm" not in pyproject
    assert "docs-llm-endpoints" not in pyproject
