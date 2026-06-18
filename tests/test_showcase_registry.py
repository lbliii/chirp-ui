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


def _parse_app_routes() -> list[tuple[str, list[str]]]:
    text = APP_PY.read_text(encoding="utf-8")
    routes: list[tuple[str, list[str]]] = []
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
