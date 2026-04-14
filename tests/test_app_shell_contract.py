"""Smoke checks for Chirp UI app shell HTMX contract (no Chirp runtime required)."""

from pathlib import Path

APP_SHELL = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "chirp_ui"
    / "templates"
    / "chirpui"
    / "app_shell_layout.html"
)
APP_SHELL_MACRO = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "chirp_ui"
    / "templates"
    / "chirpui"
    / "app_shell.html"
)


def test_app_shell_layout_has_main_and_page_content_contract() -> None:
    text = APP_SHELL.read_text(encoding="utf-8")
    assert 'id="main"' in text
    assert 'data-chirp-scroll="auto"' in text
    assert "data-chirpui-shell-topbar" in text
    assert "shell_outlet(include_boost_attrs=false)" in text
    assert "shell_outlet_attrs()" in text
    assert "shell_runtime_script()" in text


def test_app_shell_macro_shares_shell_runtime_markers() -> None:
    text = APP_SHELL_MACRO.read_text(encoding="utf-8")
    assert 'id="main"' in text
    assert 'data-chirp-scroll="auto"' in text
    assert "data-chirpui-shell-topbar" in text
    assert "shell_runtime_script()" in text
