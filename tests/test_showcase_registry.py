"""Ratchet: showcase page routes and registry entries stay in sync."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_DIR = REPO_ROOT / "examples" / "component-showcase"
APP_PY = SHOWCASE_DIR / "app.py"
BASE_HTML = SHOWCASE_DIR / "templates" / "base.html"

sys.path.insert(0, str(SHOWCASE_DIR))

from showcase.registry import PAGES, index_cards, nav_sections, page_by_path  # noqa: E402

ROUTE_RE = re.compile(
    r'@app\.route\("([^"]+)"(?:,\s*template="[^"]+")?(?:,\s*methods=\[([^\]]+)\])?\)'
)
ROUTE_SOURCES = (
    APP_PY,
    SHOWCASE_DIR / "routes" / "components.py",
    SHOWCASE_DIR / "routes" / "demos.py",
    SHOWCASE_DIR / "routes" / "shells.py",
    SHOWCASE_DIR / "routes" / "screens.py",
)


def _parse_app_routes() -> list[tuple[str, list[str]]]:
    routes: list[tuple[str, list[str]]] = []
    for source in ROUTE_SOURCES:
        text = source.read_text(encoding="utf-8")
        for match in ROUTE_RE.finditer(text):
            path = match.group(1)
            methods_raw = match.group(2)
            if methods_raw:
                methods = [item.strip().strip("\"'") for item in methods_raw.split(",")]
            else:
                methods = ["GET"]
            routes.append((path, methods))
    return routes


def test_registry_covers_every_app_route() -> None:
    registry = page_by_path()
    missing = [path for path, _methods in _parse_app_routes() if path not in registry]
    assert not missing, f"Routes missing registry entries: {missing}"


def test_registry_has_no_orphan_paths() -> None:
    route_paths = {path for path, _methods in _parse_app_routes()}
    orphans = [page.path for page in PAGES if page.path not in route_paths]
    assert not orphans, f"Registry paths without @app.route handlers: {orphans}"


def test_hidden_endpoints_are_flagged() -> None:
    registry = page_by_path()
    hidden_fragment_paths = {
        "/toast",
        "/demo/submit",
        "/demo/stream",
        "/composer/send",
        "/composer/abort",
        "/composer/dismiss/{file_id}",
        "/layout/dir",
        "/forms/demo",
        "/ui/tab/{name}",
        "/islands/remount",
        "/streaming/demo",
        "/streaming/retry",
        "/data/table",
        "/data/bulk-bar",
        "/data/export",
        "/animation/swap-demo",
        "/calendar/{year}/{month}",
        "/theme-packs/preview/{name}/{mode}",
    }
    for path, methods in _parse_app_routes():
        page = registry[path]
        if "POST" in methods:
            assert page.hidden, f"POST route should be hidden: {path}"
        if path in hidden_fragment_paths:
            assert page.hidden, f"Fragment/SSE route should be hidden: {path}"


def test_sidebar_is_registry_driven() -> None:
    base = BASE_HTML.read_text(encoding="utf-8")
    assert "showcase_nav_sections" in base
    assert 'sidebar_link("/", "Home"' not in base
    assert "{% for page in pages %}" in base


def test_index_cards_match_legacy_destinations() -> None:
    cards = index_cards()
    assert [page.path for page in cards] == [
        "/navigation",
        "/layout",
        "/chrome",
        "/shell-actions",
        "/sections",
        "/carousel",
        "/cards",
        "/forms",
        "/appearance-tone",
        "/theme-packs",
        "/ui",
        "/islands",
        "/message-turn",
        "/composer",
        "/streaming",
        "/data-display",
        "/data",
        "/effects",
        "/typography",
        "/ascii-primitives",
        "/buttons",
        "/dashboard",
        "/animation",
        "/ascii",
        "/messenger",
        "/social",
        "/video",
    ]


def test_nav_sections_preserve_sidebar_groups() -> None:
    sections = nav_sections()
    assert [name for name, _pages in sections] == [
        "Core",
        "Components",
        "Data",
        "Effects",
        "ASCII",
        "Rich",
    ]
    core_paths = [page.path for page in sections[0][1]]
    assert core_paths == ["/", "/demo"]
    data_paths = [page.path for page in sections[2][1]]
    assert "/catalog-shell" in data_paths
    assert "/screen-command-center" not in data_paths


def test_search_index_serializes_visible_pages() -> None:
    sys.path.insert(0, str(SHOWCASE_DIR))
    from showcase.search import filter_search_index, search_index

    index = search_index()
    assert len(index) <= 55
    assert all({"path", "title", "section", "description", "tags"} <= set(entry) for entry in index)
    catalog = [
        entry for entry in filter_search_index("catalog") if entry["path"] == "/catalog-shell"
    ]
    streaming = [entry for entry in filter_search_index("stream") if entry["path"] == "/streaming"]
    assert catalog
    assert streaming


SHELL_CSS_DIR = SHOWCASE_DIR / "templates" / "showcase" / "_css"
SHELL_CSS_PREFIXES = ("catalog-shell-", "ops-shell-", "support-shell-")
SHELL_TEMPLATE_INCLUDES = {
    "showcase/catalog_shell.html": "showcase/_css/catalog_shell.css.html",
    "showcase/operations_shell.html": "showcase/_css/ops_shell.css.html",
    "showcase/operations_shell_workspace.html": "showcase/_css/ops_shell.css.html",
    "showcase/support_shell.html": "showcase/_css/support_shell.css.html",
}
GALLERY_TEMPLATES = (
    "showcase/forms.html",
    "showcase/ui.html",
    "showcase/cards.html",
    "index.html",
)


def _style_block(text: str) -> str:
    match = re.search(r"<style>(.*?)</style>", text, flags=re.DOTALL)
    return match.group(1) if match else ""


def test_base_html_style_block_is_showcase_copy_only() -> None:
    """Gallery pages must not download catalog/ops/support shell CSS (#269)."""
    base = BASE_HTML.read_text(encoding="utf-8")
    style = _style_block(base)
    assert style
    assert "showcase-copy" in style
    for prefix in SHELL_CSS_PREFIXES:
        assert prefix not in style, f"base.html still defines {prefix}* rules"
    style_lines = len(style.splitlines())
    assert style_lines < 400, f"base.html style block should be <400 lines, got {style_lines}"


def test_shell_css_partials_are_scoped() -> None:
    for partial in SHELL_CSS_DIR.glob("*.css.html"):
        content = partial.read_text(encoding="utf-8")
        assert content.startswith("<style>")
        assert content.endswith("</style>\n")
        assert any(prefix in content for prefix in SHELL_CSS_PREFIXES)


def test_shell_recipe_templates_include_scoped_css() -> None:
    templates_dir = SHOWCASE_DIR / "templates"
    for rel_path, include_path in SHELL_TEMPLATE_INCLUDES.items():
        template = (templates_dir / rel_path).read_text(encoding="utf-8")
        assert include_path in template, f"{rel_path} must include {include_path}"


def test_gallery_templates_do_not_include_shell_css() -> None:
    templates_dir = SHOWCASE_DIR / "templates"
    for rel_path in GALLERY_TEMPLATES:
        template = (templates_dir / rel_path).read_text(encoding="utf-8")
        for include_path in SHELL_TEMPLATE_INCLUDES.values():
            assert include_path not in template, f"{rel_path} must not include {include_path}"
