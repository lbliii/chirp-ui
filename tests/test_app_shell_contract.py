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
    assert 'data-chirp-scroll="auto"' in text
    assert "data-chirpui-shell-topbar" in text
    assert "shell_outlet(include_boost_attrs=false)" in text
    assert "shell_outlet_attrs()" in text
