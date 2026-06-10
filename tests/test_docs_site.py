import importlib.util
import json
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
FONTS_CSS = REPO_ROOT / "site" / "assets" / "fonts.css"
SITE_PUBLIC = REPO_ROOT / "site" / "public"
API_FILTERS_PAGE = SITE_PUBLIC / "api" / "filters" / "index.html"
SITE_CONTENT = REPO_ROOT / "site" / "content"
MENU_CONFIG = REPO_ROOT / "site" / "config" / "_default" / "menu.yaml"
# #145 — every shipped template family needs live content so its route renders
# instead of 404ing. Each tuple is (section dir, the type/template token its
# _index.md must declare so Bengal resolves the family list template).
DOGFOOD_FAMILIES = {
    "blog": "type: blog",
    "tutorial": "type: tutorial",
    "changelog": "type: changelog",
    "authors": "template: authors/list.html",
    "resume": "template: resume/list.html",
}
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

# #165/#166 — on-site reference so users never leave for GitHub.
THEME_TEMPLATES = REPO_ROOT / "src" / "bengal_themes" / "chirp_theme" / "templates"
SEARCH_PAGE_TEMPLATE = THEME_TEMPLATES / "search.html"
SHORTCODES_DIR = THEME_TEMPLATES / "shortcodes"
DIRECTIVES_DIR = THEME_TEMPLATES / "directives"
REFERENCE_DIR = SITE_CONTENT / "docs" / "reference"
COMPONENTS_INDEX = SITE_CONTENT / "docs" / "components" / "_index.md"
MANIFEST_JSON = REPO_ROOT / "src" / "chirp_ui" / "manifest.json"
# The Markdown directive name differs from its template filename for child-cards.
DIRECTIVE_TEMPLATE_TO_NAME = {"child_cards": "child-cards"}


def _shipped_shortcode_names() -> set[str]:
    return {p.stem for p in SHORTCODES_DIR.glob("*.html")}


def _shipped_directive_names() -> set[str]:
    return {DIRECTIVE_TEMPLATE_TO_NAME.get(p.stem, p.stem) for p in DIRECTIVES_DIR.glob("*.html")}


def _manifest_public_categories() -> set[str]:
    manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    return {
        comp.get("category")
        for comp in manifest["components"].values()
        if comp.get("authoring") != "internal" and comp.get("category")
    }


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


def test_fonts_css_declares_font_faces_for_all_weights() -> None:
    """#135 — the generated stylesheet must define @font-face for 400/600/700 with
    font-display:swap so the preloaded woff2 weights actually resolve to Outfit.

    base.html links this file (gated on config.fonts.display) and preloads the
    400/600 woff2; this guards the other half of the contract — that the linked
    stylesheet wires those weights to the Outfit family with swap behavior.
    """
    css = FONTS_CSS.read_text(encoding="utf-8")

    assert css.count("@font-face") >= 3, (
        "fonts.css must declare at least 3 @font-face blocks (#135)"
    )
    assert "font-family: 'Outfit'" in css or 'font-family: "Outfit"' in css
    for weight in (400, 600, 700):
        assert f"font-weight: {weight}" in css, f"no @font-face for Outfit {weight} (#135)"
    # swap keeps text visible during the woff2 fetch (no invisible-text FOIT).
    assert css.count("font-display: swap") >= 3, (
        "every @font-face must use font-display:swap (#135)"
    )
    # The stylesheet serves woff2 only (the .ttf duplicates were dropped — see below).
    assert ".woff2" in css
    assert ".ttf" not in css


def test_fonts_dir_ships_woff2_only_no_ttf_duplicates() -> None:
    """#135 — the unused .ttf duplicates were removed; only woff2 weights ship.

    fonts.css references woff2 only, so the .ttf copies were dead weight in the
    build. This fails if a .ttf font sneaks back into the source fonts dir.
    """
    fonts_dir = REPO_ROOT / "site" / "assets" / "fonts"
    ttf = sorted(p.name for p in fonts_dir.glob("*.ttf"))
    assert not ttf, f"unused .ttf font duplicates shipped in site/assets/fonts: {ttf} (#135)"
    woff2 = sorted(p.name for p in fonts_dir.glob("*.woff2"))
    assert woff2, "expected woff2 Outfit weights in site/assets/fonts (#135)"


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


def _render_autodoc_members(theme_env, element: dict) -> str:
    """Render the theme's autodoc members partial against a fabricated element.

    Uses the ``theme_env`` fixture (theme + chirp_ui loader roots, conftest
    filter stubs, ``markdownify`` stub) so the members -> returns/raises ->
    chirpui macro chain renders without a real Chirp/Bengal app.
    """
    template = theme_env.get_template("autodoc/partials/members.html")
    return template.render(element=element)


def test_autodoc_member_returns_and_raises_render_in_accordion_body(theme_env) -> None:
    """#158 — a member with return/raises detail emits Returns/Raises blocks.

    Mirrors Bengal's Python extractor shape: the return type lives under
    ``member.metadata.returns``, the return prose under
    ``member.metadata.parsed_doc.returns``, and the exception list under
    ``member.metadata.parsed_doc.raises`` (a list of ``{type, description}``).
    ``register_colors`` on /api/filters/ documents ``Raises ValueError``; the
    rebuilt member body must surface a structured Raises block, and a
    return-annotated member must surface a Returns block — inside each member's
    accordion body, after the params table.
    """
    element = {
        "children": [
            {
                "name": "register_colors",
                "element_type": "function",
                "metadata": {
                    "signature": "register_colors(colors: dict) -> None",
                    "args": [
                        {
                            "name": "colors",
                            "type": "dict",
                            "default": "",
                            "docstring": "Mapping of name to color value.",
                        }
                    ],
                    "returns": "None",
                    "parsed_doc": {
                        "returns": "Nothing.",
                        "raises": [
                            {
                                "type": "ValueError",
                                "description": "If a registered color is invalid.",
                            }
                        ],
                    },
                },
            },
            {
                "name": "resolve_color",
                "element_type": "function",
                "metadata": {
                    "signature": "resolve_color(name: str) -> str",
                    "args": [
                        {
                            "name": "name",
                            "type": "str",
                            "default": "",
                            "docstring": "Registered color name.",
                        }
                    ],
                    "returns": "str",
                    "parsed_doc": {"returns": "The resolved CSS color string."},
                },
            },
        ]
    }

    html = _render_autodoc_members(theme_env, element)

    # The raising member surfaces a structured Raises block naming the exception.
    assert "chirp-theme-reference-raises" in html, (
        "raising member did not emit a Raises block (#158)"
    )
    assert "ValueError" in html
    # The return-annotated member surfaces a Returns block.
    assert "chirp-theme-reference-returns" in html, (
        "return-annotated member did not emit a Returns block (#158)"
    )


def test_autodoc_member_without_return_or_raises_emits_no_blocks(theme_env) -> None:
    """#158 — members with no return/raises detail must not emit empty blocks.

    Strict-undefined guards (``member.metadata.get(...)``) gate the includes, so
    a bare member renders neither a Returns nor a Raises callout.
    """
    element = {
        "children": [
            {
                "name": "noop",
                "element_type": "function",
                "metadata": {
                    "signature": "noop()",
                    "args": [],
                    "parsed_doc": {},
                },
            }
        ]
    }

    html = _render_autodoc_members(theme_env, element)

    assert "chirp-theme-reference-returns" not in html
    assert "chirp-theme-reference-raises" not in html


def test_autodoc_members_template_renders_returns_and_raises_partials() -> None:
    """#158 — the members partial wires the shared returns/raises partials.

    Source-level guard so the wiring cannot silently regress: each member's
    accordion body includes the returns.html / raises.html partials, guarded on
    the member's own metadata (strict-undefined ``.get`` access), and the
    "intentionally NOT wired here" note is gone.
    """
    template = THEME_AUTODOC_MEMBERS.read_text(encoding="utf-8")

    assert 'include "autodoc/partials/returns.html"' in template
    assert 'include "autodoc/partials/raises.html"' in template
    # Read from the member's own metadata, per the Bengal extractor field paths.
    assert 'member_meta.get("returns")' in template
    assert 'member_meta.get("parsed_doc")' in template
    assert 'member_parsed_doc.get("returns")' in template
    assert 'member_parsed_doc.get("raises")' in template
    # The stale "not wired here" note must be removed.
    assert "intentionally NOT wired here" not in template


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


# ---------------------------------------------------------------------------
# #145 — dogfood content for every shipped template family
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("section", "type_token"), sorted(DOGFOOD_FAMILIES.items()))
def test_dogfood_family_has_section_index_with_resolving_type(
    section: str, type_token: str
) -> None:
    """#145 — each family has a real section index that resolves its list template.

    blog/tutorial/changelog resolve via Bengal's content-type strategies
    (``type: <family>``); authors/resume have no strategy and resolve by section
    auto-detection, so their index pins the template explicitly. Either way the
    section must exist or the route 404s.
    """
    index = SITE_CONTENT / section / "_index.md"
    assert index.is_file(), f"missing {section}/_index.md — /{section}/ would 404 (#145)"

    text = index.read_text(encoding="utf-8")
    assert type_token in text, (
        f"{section}/_index.md must declare `{type_token}` so Bengal resolves "
        f"{section}/list.html (#145)"
    )
    # Non-placeholder: a real title and prose body, not an empty stub.
    assert "title:" in text
    body = text.split("---", 2)[-1].strip()
    assert len(body) > 40, f"{section}/_index.md has placeholder/empty body (#145)"


@pytest.mark.parametrize("section", sorted(DOGFOOD_FAMILIES))
def test_dogfood_family_has_child_content(section: str) -> None:
    """#145 — each family ships at least one child page so the list is non-empty."""
    children = [p for p in (SITE_CONTENT / section).glob("*.md") if p.name != "_index.md"]
    assert children, f"{section}/ has no child pages — its list would render empty (#145)"


def test_dogfood_blog_post_dogfoods_lazy_features() -> None:
    """#145/#149 — one blog post exercises a mermaid fence and a markdown table.

    This seeds content for the lazy-feature wiring (#149): the mermaid block and
    table exist in source so a built page proves the loaders once they are wired.
    """
    posts = list((SITE_CONTENT / "blog").glob("*.md"))
    text = "\n".join(p.read_text(encoding="utf-8") for p in posts)

    assert "```mermaid" in text, "no mermaid code-fence in any blog post (#145/#149)"
    # A GitHub-flavored markdown table needs a header separator row.
    assert re.search(r"^\|[\s\-:|]+\|\s*$", text, flags=re.MULTILINE), (
        "no markdown table in any blog post (#145/#149)"
    )


def test_dogfood_families_are_wired_into_menu_config() -> None:
    """#145 — the families are reachable from navigation via the real menu.yaml.

    The footer menu (rendered by the theme) names each family; the top nav also
    auto-discovers the sections, but the explicit menu makes the wiring durable.
    """
    text = MENU_CONFIG.read_text(encoding="utf-8")
    for section in DOGFOOD_FAMILIES:
        assert f"/{section}/" in text, f"/{section}/ not wired into menu.yaml (#145)"


@pytest.mark.parametrize("section", sorted(DOGFOOD_FAMILIES))
def test_built_dogfood_family_route_renders_non_placeholder(section: str) -> None:
    """#145 — each family route builds to a 200-equivalent page with real content.

    Skipped when the site is unbuilt; the Gate rebuilds the site before
    verification. A built index.html is the static-site analogue of a 200.
    """
    page = SITE_PUBLIC / section / "index.html"
    if not page.is_file():
        pytest.skip("site/public not built; Gate rebuilds the site before verification")

    html = page.read_text(encoding="utf-8")
    # Not the Bengal emergency fallback page (which means the template crashed).
    assert "fallback-notice" not in html, f"/{section}/ rendered the fallback page (#145)"
    # Real chrome + content rendered, not an empty body.
    assert "<title" in html
    assert len(html) > 2000, f"/{section}/ index.html looks like a placeholder (#145)"


# ---------------------------------------------------------------------------
# #165/#166 — on-site shortcode/directive reference + component catalog
# ---------------------------------------------------------------------------


def test_reference_section_pages_exist_as_docs() -> None:
    """#165 — the reference section ships an index plus shortcode/directive pages."""
    index = REFERENCE_DIR / "_index.md"
    shortcodes = REFERENCE_DIR / "shortcodes.md"
    directives = REFERENCE_DIR / "directives.md"

    for page in (index, shortcodes, directives):
        assert page.is_file(), f"missing reference page: {page} (#165)"
        assert "type: doc" in page.read_text(encoding="utf-8"), page


def test_shortcodes_reference_documents_every_shipped_shortcode() -> None:
    """#165 — every shipped shortcode template has an on-site reference entry.

    Test-guarded sync: adding a shortcode template without documenting it here
    fails, so the reference never silently drifts from what the theme ships.
    """
    text = (REFERENCE_DIR / "shortcodes.md").read_text(encoding="utf-8")
    shipped = _shipped_shortcode_names()

    assert shipped, "no shortcode templates found — wrong path?"
    for name in shipped:
        assert name in text, f"shortcode '{name}' is shipped but not in shortcodes.md (#165)"

    # component_specimen and the admonition family are first-class (issue ask).
    assert "component_specimen" in text
    for inline in ("tip", "warning", "danger"):
        assert inline in text

    # A rendered example, not only a syntax dump: live shortcode invocations
    # (no comment-escape) must appear on the page.
    assert "{{< component_specimen" in text
    assert "{{< tip" in text


def test_directives_reference_documents_every_shipped_directive() -> None:
    """#165 — every shipped directive template has an on-site reference entry."""
    text = (REFERENCE_DIR / "directives.md").read_text(encoding="utf-8")
    shipped = _shipped_directive_names()

    assert shipped, "no directive templates found — wrong path?"
    for name in shipped:
        assert name in text, f"directive '{name}' is shipped but not in directives.md (#165)"

    # admonition is documented as a first-class authoring feature (issue ask),
    # and a live rendered directive (not just a code fence) must appear.
    assert "admonition" in text
    assert ":::{tip}" in text
    assert ":::{cards}" in text


def test_reference_section_is_wired_into_menu_config() -> None:
    """#165 — the reference section is reachable from the real menu.yaml."""
    text = MENU_CONFIG.read_text(encoding="utf-8")
    assert "/docs/reference/" in text, "/docs/reference/ not wired into menu.yaml (#165)"


def test_components_index_is_an_onsite_catalog_not_a_github_pointer() -> None:
    """#166 — the component catalog lives on-site, not behind a GitHub README.

    The old index punted to a GitHub README anchor and `python examples/...app.py`
    to see examples; the rebuilt catalog must keep visitors on the site.
    """
    text = COMPONENTS_INDEX.read_text(encoding="utf-8")

    # No off-site / local-app pointers for seeing examples.
    assert "github.com/lbliii/chirp-ui#usage" not in text
    assert "examples/component-showcase/app.py" not in text
    assert "localhost:8000" not in text

    # On-site equivalents are present: the showcase, live specimen pages, and the
    # generated API reference.
    assert "/showcase/" in text
    assert "/api/" in text
    assert "./controls/" in text


def test_components_catalog_covers_every_manifest_category() -> None:
    """#166 — the catalog stays in sync with the manifest (test-guarded).

    Every public component category in manifest.json must be named in the
    catalog, so a new category cannot ship without a home in the docs.
    """
    text = COMPONENTS_INDEX.read_text(encoding="utf-8").lower()
    categories = _manifest_public_categories()

    assert categories, "no public categories found in manifest.json"
    for category in categories:
        # Catalog headings use spaced labels (e.g. "data display"); match the
        # manifest's hyphenated category either form.
        spaced = category.replace("-", " ")
        assert category in text or spaced in text, (
            f"manifest category '{category}' has no home in components/_index.md (#166)"
        )


class _NoscriptPage:
    """Minimal page stand-in for the noscript fallback render tests (#171)."""

    def __init__(self, title: str, href: str) -> None:
        self.title = title
        self.href = href


class _NoscriptSection:
    """Minimal section stand-in carrying regular_pages for the noscript loop."""

    def __init__(self, title: str, pages: list) -> None:
        self.title = title
        self.name = title
        self.regular_pages = pages
        self.pages = pages


class _NoscriptSite:
    """Fake `site` exposing sections + a flat page list for noscript rendering."""

    def __init__(self, sections: list, pages: list) -> None:
        self.sections = sections
        self.regular_pages = pages
        self.pages = pages


def _absolute_url_stub(value: object) -> str:
    """Base-prefix passthrough mirroring Bengal's `absolute_url` filter."""
    text = str(value)
    return ("/base" + text) if text.startswith("/") else text


def _extract_noscript_block(template_text: str) -> str:
    """Pull the <noscript>...</noscript> fragment out of a template source.

    The full search.html extends base.html and pulls in the whole shell
    (navbar, hero, globals like current_lang()), which is too much context for
    a unit test. The server-side fallback we care about lives entirely inside a
    single <noscript> block of plain kida, so we render *that* fragment through
    the real engine — if the loop, the `?.` access, or the `absolute_url`
    pipeline regresses, this test fails.
    """
    match = re.search(r"<noscript>.*?</noscript>", template_text, re.DOTALL)
    assert match, "search.html no longer contains a <noscript> fallback block (#171)"
    return match.group(0)


def _render_search_noscript(site: _NoscriptSite) -> str:
    """Render the real search.html <noscript> fragment with fake site data."""
    kida = pytest.importorskip("kida")
    noscript = _extract_noscript_block(SEARCH_PAGE_TEMPLATE.read_text(encoding="utf-8"))
    env = kida.Environment(autoescape=True)
    # absolute_url is a Bengal-provided filter; the passthrough is enough to
    # prove links are emitted and run through the pipeline.
    env.update_filters({"absolute_url": _absolute_url_stub})
    return env.from_string(noscript).render(site=site)


def test_search_page_noscript_renders_indexed_page_links() -> None:
    """#171 — /search renders a real, server-side list of indexed pages with JS off.

    Renders the actual <noscript> fragment from search.html via the kida engine
    with fake site data and asserts it emits a search-page__noscript-list with
    anchors to each page (not a dead input over an empty state).
    """
    site = _NoscriptSite(
        sections=[
            _NoscriptSection("Guides", [_NoscriptPage("Installation", "/docs/install/")]),
            _NoscriptSection("API Reference", [_NoscriptPage("filters", "/api/filters/")]),
        ],
        pages=[_NoscriptPage("Installation", "/docs/install/")],
    )

    html = _render_search_noscript(site)

    # Grouped list container is present.
    assert "search-page__noscript-list" in html, (
        "noscript fallback did not render a search-page__noscript-list (#171)"
    )
    # Section headings render from site data.
    assert "Guides" in html
    assert "API Reference" in html
    # Real anchors to indexed pages, run through absolute_url.
    assert '<a href="/base/docs/install/">Installation</a>' in html
    assert '<a href="/base/api/filters/">filters</a>' in html


def test_search_page_noscript_falls_back_to_flat_page_list() -> None:
    """#171 — with no sections, the noscript block lists site.pages directly."""
    site = _NoscriptSite(
        sections=[],
        pages=[_NoscriptPage("Quickstart", "/docs/quickstart/")],
    )

    html = _render_search_noscript(site)

    assert "search-page__noscript-list" in html
    assert '<a href="/base/docs/quickstart/">Quickstart</a>' in html


# ---------------------------------------------------------------------------
# #153 — adoption quickstart: applying chirp-theme to a Bengal site
# ---------------------------------------------------------------------------


def test_install_doc_documents_chirp_theme_adoption() -> None:
    """#153 — the install doc walks a Bengal user through adopting chirp-theme.

    The get-started page must name the theme, state the minimum Bengal version,
    explain the ``library_asset_tags`` requirement, and show setting
    ``theme.name: "chirp-theme"`` — the four facts a new adopter needs and the
    acceptance criteria for #153.
    """
    text = INSTALL_DOC.read_text(encoding="utf-8")

    # Names the theme and shows wiring it into a Bengal site config.
    assert "chirp-theme" in text
    assert 'name: "chirp-theme"' in text
    # States the minimum Bengal version.
    assert "0.3.3" in text
    assert ">=0.3.3" in text or ">= 0.3.3" in text
    # Names the library_asset_tags requirement (why >=0.3.3 is needed).
    assert "library_asset_tags" in text
    # The README links to the adoption path, so the entry point is discoverable.
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "chirp-theme" in readme
    assert "get-started/installation" in readme


# ---------------------------------------------------------------------------
# #167 — /docs/ landing destinations get an icon per card
# ---------------------------------------------------------------------------


def test_docs_index_cards_carry_an_icon_each() -> None:
    """#167 — every destination card on /docs/ leads with an icon.

    The landing keeps raw ``chirpui-card`` markup (guarded by
    ``test_docs_index_uses_chirpui_card_markup_for_cards``), so the icons are
    inline ``chirpui-card__icon`` spans wrapping a shipped Phosphor SVG — one per
    card, not the directive form. There are seven destination cards (five Learn,
    two Reference), so there must be at least seven icon spans, each with an
    accessible-hidden inline ``<svg>``.
    """
    text = DOCS_INDEX.read_text(encoding="utf-8")

    card_count = text.count('class="chirpui-card chirp-theme-directive-card"')
    icon_spans = text.count('class="chirpui-card__icon"')
    assert card_count >= 7, f"expected the documented destination cards, found {card_count}"
    assert icon_spans >= card_count, (
        f"only {icon_spans} icon spans for {card_count} cards — every /docs/ "
        f"destination card must lead with an icon (#167)"
    )
    # Icons are decorative (the title is the label) and rendered as inline SVG.
    assert '<span class="chirpui-card__icon" aria-hidden="true"><svg' in text
