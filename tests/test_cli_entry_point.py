"""Tests for the installed ``chirp-ui`` console script entry point."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_chirp_ui_console_script_is_on_path_after_install() -> None:
    script = shutil.which("chirp-ui")
    assert script, "chirp-ui console script not found on PATH after install"


def test_chirp_ui_find_via_console_script() -> None:
    result = subprocess.run(
        ["chirp-ui", "find", "badge", "--category=feedback"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "badge" in result.stdout


def test_chirp_ui_help_via_module_matches_console_script() -> None:
    module = subprocess.run(
        [sys.executable, "-m", "chirp_ui", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    console = subprocess.run(
        ["chirp-ui", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert module.returncode == 0
    assert console.returncode == 0
    assert "find" in module.stdout
    assert module.stdout == console.stdout
