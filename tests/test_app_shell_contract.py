"""Smoke checks for Chirp UI app shell HTMX contract (no Chirp runtime required)."""

from __future__ import annotations

from pathlib import Path

APP_SHELL = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "chirp_ui"
    / "templates"
    / "chirpui"
    / "app_shell_layout.html"
)


def test_app_shell_layout_has_main_and_page_content_contract() -> None:
    text = APP_SHELL.read_text(encoding="utf-8")
    assert 'id="main"' in text
    assert 'id="page-content"' in text
    assert 'hx-boost="true"' in text
    assert 'hx-target="#main"' in text
    assert 'hx-swap="innerHTML"' in text
    assert 'hx-select="#page-content"' in text
