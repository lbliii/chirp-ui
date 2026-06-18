"""Ratchet: modular showcase app layout stays importable and thin."""

from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_DIR = REPO_ROOT / "examples" / "component-showcase"
APP_PY = SHOWCASE_DIR / "app.py"

ROUTE_MODULES = (
    "routes.components",
    "routes.demos",
    "routes.shells",
    "routes.screens",
)
FIXTURE_MODULES = (
    "fixtures.catalog",
    "fixtures.ops",
    "fixtures.support",
    "fixtures.roster",
)


@pytest.fixture(scope="module", autouse=True)
def _showcase_path() -> None:
    path = str(SHOWCASE_DIR)
    if path not in sys.path:
        sys.path.insert(0, path)


def test_app_py_is_thin_entrypoint() -> None:
    line_count = len(APP_PY.read_text(encoding="utf-8").splitlines())
    assert line_count <= 200, f"app.py should be <=200 lines, got {line_count}"


def test_route_and_fixture_modules_import_cleanly() -> None:
    for module_name in (*ROUTE_MODULES, *FIXTURE_MODULES, "showcase.helpers"):
        importlib.import_module(module_name)


def test_route_modules_do_not_import_each_other() -> None:
    importers: dict[str, set[str]] = {}
    for module_name in ROUTE_MODULES:
        module = importlib.import_module(module_name)
        sources = {
            node.module
            for node in ast.walk(ast.parse(Path(module.__file__).read_text(encoding="utf-8")))
            if isinstance(node, ast.ImportFrom) and node.module
        }
        importers[module_name] = sources

    for module_name, sources in importers.items():
        for other in ROUTE_MODULES:
            if other == module_name:
                continue
            assert other not in sources, f"{module_name} imports sibling route module {other}"


def test_helpers_live_in_showcase_package() -> None:
    helpers = importlib.import_module("showcase.helpers")
    assert hasattr(helpers, "page")
    assert hasattr(helpers, "query_list")
    assert hasattr(helpers, "SHOWCASE_PALETTE_BOOST_ATTRS")
