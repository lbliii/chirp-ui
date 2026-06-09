import importlib.util
import os
import re
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE_SCRIPT = REPO_ROOT / "scripts" / "docs_site.py"
PYPROJECT = REPO_ROOT / "pyproject.toml"
THEME_BASE_TEMPLATE = (
    REPO_ROOT / "src" / "bengal_themes" / "chirp_theme" / "templates" / "base.html"
)
THEME_AUTODOC_MEMBERS = (
    REPO_ROOT
    / "src"
    / "bengal_themes"
    / "chirp_theme"
    / "templates"
    / "autodoc"
    / "partials"
    / "members.html"
)
FONTS_CONFIG = REPO_ROOT / "site" / "config" / "_default" / "fonts.yaml"
SITE_PUBLIC = REPO_ROOT / "site" / "public"
API_FILTERS_PAGE = SITE_PUBLIC / "api" / "filters" / "index.html"
VALID_SEARCH_PRELOAD_MODES = {"smart", "immediate", "lazy"}
AGENT_SOURCE_INVENTORY = REPO_ROOT / "docs" / "agents" / "agent-source-inventory.md"
AGENT_SOURCE_MAP = REPO_ROOT / "docs" / "agents" / "agent-source-map.md"
AGENT_CURATED_SNIPPETS = REPO_ROOT / "docs" / "agents" / "agent-curated-snippets.md"
PATTERN_DOCS = {
    "navigation.md": "docs/patterns/navigation.md",
    "search-shells.md": "docs/patterns/search-shell-recipes.md",
    "workspace-shells.md": "docs/patterns/workspace-shell-recipes.md",
    "layout-affinity.md": "docs/decisions/layout-affinity.md",
    "product-pages.md": "docs/patterns/product-page-patterns.md",
    "media-sites.md": "docs/patterns/media-site-patterns.md",
    "forums.md": "docs/patterns/forum-site-patterns.md",
}
NAVIGATION_PATTERN_COLLATERAL = [
    "docs/patterns/dense-navigation-recipes.md",
    "docs/plans/PLAN-application-chrome-system.md",
]
COMPONENT_DOCS = {
    "appearance-tone.md": "docs/components/appearance-tone.md",
    "dropdowns.md": "docs/components/dropdown-anatomy.md",
    "drawers-trays.md": "docs/components/drawer-tray-anatomy.md",
    "modals.md": "docs/components/modal-anatomy.md",
    "tabs.md": "docs/components/tabs-anatomy.md",
}
THEME_DOCS = {
    "bengal-theme-controls.md": "docs/theming/bengal-theme-anatomy.md",
    "chirp-theme.md": "docs/theming/chirp-theme.md",
}
DOCS_IA_MIGRATION = REPO_ROOT / "docs" / "agents" / "docs-ia-migration.md"
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


def test_docs_index_uses_chirpui_card_markup_for_cards() -> None:
    text = DOCS_INDEX.read_text(encoding="utf-8")

    assert "API Reference" not in text
    assert 'href="./components/"' in text
    assert '<div class="chirpui-grid' in text
    assert 'class="chirpui-card' in text
    assert "card-grid" not in text
    assert ":::{cards}" not in text
    assert ":::{card} Component Reference" not in text


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
    assert "current application chrome status" in matrix
    assert "reference-implementation promotion gate" in matrix
    assert "no published-only application chrome API" in matrix
    assert "This page is a published bridge" in text
    assert "Do not add a published-only application chrome API here" in text
    assert "docs/patterns/visual-audit-showcase.md" in text
    assert "## Current Status" in text
    assert "Private evidence is complete for page actions" in text
    assert "linked nav/sidebar semantics" in text
    assert "shell response/OOB branching" in text
    assert "compact header/page hero comparison" in text
    assert "deliberately built reference implementation" in text
    assert "third" in text
    assert "hand-written route family outside `mount_pages()`" in text
    assert "`application_chrome()`" in text
    assert "`page_actions`" in text
    assert "shell response helper APIs" in text


def test_layout_affinity_published_page_marks_prototype_contract() -> None:
    text = (REPO_ROOT / "site" / "content" / "docs" / "patterns" / "layout-affinity.md").read_text(
        encoding="utf-8"
    )

    for required in [
        "type: doc",
        "docs/decisions/layout-affinity.md",
        "docs/patterns/layout-affinity-resolver-authoring.md",
        "prototype",
        "parent-scoped",
        "layout_resolver",
        "layout_parts",
        "Prototype recipe attributes",
        "Not yet descriptor API",
        "Not yet manifest contract",
        "Allowed only where documented parent resolvers consume them",
        "not part of the current manifest contract",
        "not promoted",
        "Broad descendant selectors are",
        "Authoring changes follow `docs/patterns/layout-affinity-resolver-authoring.md`",
    ]:
        assert required in text


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

    assert "docs/agents/agent-curated-snippets.md" in inventory
    assert "[AGENT-CURATED-SNIPPETS.md](agents/agent-curated-snippets.md)" in index
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
    assert "docs/agents/agent-source-inventory.md" in text
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


def _built_html_pages() -> list[Path]:
    """Built index pages to assert head-meta correctness against (skip if unbuilt)."""
    candidates = [SITE_PUBLIC / "index.html", SITE_PUBLIC / "search" / "index.html"]
    return [path for path in candidates if path.is_file()]


def test_base_template_links_fonts_css_when_display_font_configured() -> None:
    """#135 — fonts.css must be linked, gated on a fonts-configured check, with
    the above-the-fold Outfit weights preloaded as woff2 (font-display:swap is in
    the generated stylesheet)."""
    template = THEME_BASE_TEMPLATE.read_text(encoding="utf-8")

    # The gate keys off the configured display font (fonts.yaml: fonts.display).
    assert "config?.fonts?.display" in template
    # Generated stylesheet is linked so var(--font-display) resolves to Outfit.
    assert "asset_url('fonts.css')" in template
    # 400 (body/headings) and 600 (section labels) are above the fold — preload both.
    assert 'rel="preload"' in template
    assert 'as="font"' in template
    assert 'type="font/woff2"' in template
    assert "asset_url('fonts/outfit-400.woff2')" in template
    assert "asset_url('fonts/outfit-600.woff2')" in template
    # crossorigin is required for font preloads to be reused by the @font-face fetch.
    fonts_block = template[template.index("config?.fonts?.display") :]
    fonts_block = fonts_block[: fonts_block.index("{% end %}")]
    for line in fonts_block.splitlines():
        if 'rel="preload"' in line and 'as="font"' in line:
            assert "crossorigin" in line, line


def test_fonts_config_defines_a_display_font() -> None:
    """The fonts gate is only meaningful while a display font is configured."""
    text = FONTS_CONFIG.read_text(encoding="utf-8")

    # fonts.display: "Outfit:400,600,700" — the weights the preloads/stylesheet serve.
    assert "display:" in text
    assert "Outfit" in text


def test_base_template_reads_real_search_preload_config_path() -> None:
    """#139 — the meta must read search.lunr.preload (not the non-existent
    config.search_preload) so it never leaks a stringified ConfigSection."""
    template = THEME_BASE_TEMPLATE.read_text(encoding="utf-8")

    assert "config.search?.lunr?.preload ?? 'smart'" in template
    # The old mis-keyed path is gone for good.
    assert "config.search_preload" not in template


def test_built_pages_link_fonts_css() -> None:
    """#135 — every built page links fonts.css while a display font is configured."""
    pages = _built_html_pages()
    if not pages:
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert "fonts.css" in html, f"fonts.css not linked in {page}"
        assert re.search(r'rel="preload"[^>]*as="font"[^>]*type="font/woff2"', html), (
            f"no woff2 font preload in {page}"
        )


def test_built_pages_render_clean_search_preload_meta() -> None:
    """#139 — bengal:search_preload renders one of the three valid modes with no
    stringified config object, on every page including /search."""
    pages = _built_html_pages()
    if not pages:
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    pattern = re.compile(r'<meta\s+name="bengal:search_preload"\s+content="([^"]*)"', re.IGNORECASE)
    for page in pages:
        html = page.read_text(encoding="utf-8")
        match = pattern.search(html)
        assert match is not None, f"bengal:search_preload meta missing in {page}"
        value = match.group(1)
        assert "ConfigSection" not in value, f"stringified config leaked in {page}: {value!r}"
        assert value in VALID_SEARCH_PRELOAD_MODES, f"invalid preload mode in {page}: {value!r}"


def test_autodoc_members_read_signature_and_params_from_metadata() -> None:
    """#158 — member detail must read the Bengal extractor's real field paths.

    Bengal's Python extractor emits a member's signature/params under
    `member.metadata.*` (signature -> metadata.signature, parameters ->
    metadata.args). The previous template gated the signature on the
    non-existent top-level `member.signature` and looked for
    `metadata.parameters`/`metadata.args` without remapping the arg dicts'
    `docstring` key to params_table's `description` column, so on real data
    zero signatures and zero params tables rendered.
    """
    template = THEME_AUTODOC_MEMBERS.read_text(encoding="utf-8")

    # Signature/params are sourced from metadata, not the (absent) top-level keys.
    assert "member_meta?.signature" in template
    assert "member_meta?.args" in template
    # The arg dicts' per-param prose (`docstring`) is remapped to the
    # params_table `description` column, or it would render blank.
    assert 'arg.get("docstring"' in template
    assert "params_table(member_param_rows" in template
    # Member-level flags surfaced from metadata (not only the page hero).
    assert "member_meta?.is_async" in template
    assert "member_meta?.is_property" in template
    assert "member_meta?.is_classmethod" in template
    assert "member_meta?.is_staticmethod" in template
    # Deprecation notice is a DocElement-level field, not a metadata flag.
    assert "member?.deprecated" in template


def test_built_api_filters_renders_typed_params_tables() -> None:
    """#158 — a parametered member on /api/filters/ must emit a params table.

    `bem`, `validate_variant`, and friends in chirp_ui.filters have typed
    parameters; after the field-path fix the rebuilt page must surface them as
    chirpui-params-table elements (name/type/default/description). Skipped when
    the site is unbuilt — the Gate rebuilds the site before verification.
    """
    if not API_FILTERS_PAGE.is_file():
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    html = API_FILTERS_PAGE.read_text(encoding="utf-8")

    # The page documents parametered filters, so at least one member's
    # parameters must render as a chirpui-params-table.
    assert html.count("chirpui-params-table") > 0, (
        "no chirpui-params-table on /api/filters/ — member params are not "
        "being read from member.metadata.args (see #158)"
    )
    # And the typed signature itself must be surfaced as a code block.
    assert "chirp-theme-reference-member__signature" in html, (
        "no member signature rendered on /api/filters/ — signature is not being "
        "read from member.metadata.signature (see #158)"
    )
