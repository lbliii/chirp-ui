"""Tests for the registry-backed blocks gallery generator."""

from __future__ import annotations

import json
from pathlib import Path

from chirp_ui.blocks_gallery import (
    GALLERY_SCHEMA,
    build_gallery,
    copy_snippet_for,
    extract_usage_snippet,
    is_public_component,
    to_json_gallery,
)
from chirp_ui.manifest import build_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]
GALLERY_PATH = REPO_ROOT / "examples" / "component-showcase" / "generated" / "blocks_gallery.json"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_blocks_gallery.py"


def test_extract_usage_snippet_from_doc_block() -> None:
    description = (
        "Accordion component\n\n"
        "    Usage:\n"
        "        {% from \"chirpui/accordion.html\" import accordion %}\n"
        "        {{ accordion() }}\n"
    )
    snippet = extract_usage_snippet(description)
    assert 'from "chirpui/accordion.html"' in snippet
    assert "accordion" in snippet


def test_copy_snippet_falls_back_to_import_and_call() -> None:
    manifest = build_manifest()
    entry = manifest["components"]["badge"]
    snippet = copy_snippet_for("badge", entry)
    assert 'from "chirpui/' in snippet
    assert "badge" in snippet


def test_build_gallery_covers_public_components() -> None:
    manifest = build_manifest()
    public_names = {
        name
        for name, entry in manifest["components"].items()
        if is_public_component(entry)
    }
    gallery = build_gallery(with_previews=False)
    assert gallery["schema"] == GALLERY_SCHEMA
    assert {block["name"] for block in gallery["blocks"]} == public_names
    assert gallery["stats"]["blocks"] == len(public_names)


def test_build_gallery_renders_some_live_previews() -> None:
    gallery = build_gallery(with_previews=True)
    assert gallery["stats"]["previews_rendered"] > 50


def test_committed_blocks_gallery_is_fresh() -> None:
    assert GALLERY_PATH.is_file(), (
        f"Missing {GALLERY_PATH.relative_to(REPO_ROOT)}. Run: poe build-blocks-gallery"
    )
    current = GALLERY_PATH.read_text(encoding="utf-8")
    generated = to_json_gallery(build_gallery(with_previews=True))
    assert current == generated, (
        f"{GALLERY_PATH.relative_to(REPO_ROOT)} is stale relative to the registry.\n"
        "Run: poe build-blocks-gallery"
    )


def test_build_script_check_mode() -> None:
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_gallery_json_is_valid_and_complete() -> None:
    payload = json.loads(GALLERY_PATH.read_text(encoding="utf-8"))
    assert payload["schema"] == GALLERY_SCHEMA
    assert payload["blocks"]
    first = payload["blocks"][0]
    assert {"name", "category", "copy_snippet", "preview_html", "summary"} <= set(first)
