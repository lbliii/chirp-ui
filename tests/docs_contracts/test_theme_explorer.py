"""Contract: live theme explorer matches token-job taxonomy (#213)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SHOWCASE_DIR = REPO / "examples" / "component-showcase"
sys.path.insert(0, str(SHOWCASE_DIR))

from showcase.theme_explorer import TOKEN_JOBS, list_token_jobs  # noqa: E402

APP_THEME = REPO / "docs" / "theming" / "app-theme.md"
TEMPLATE = SHOWCASE_DIR / "templates" / "showcase" / "theme-explorer.html"


def _app_theme_jobs() -> list[str]:
    text = APP_THEME.read_text(encoding="utf-8")
    rows = re.findall(r"^\| ([A-Z][^|]+) \| `--chirpui-", text, flags=re.MULTILINE)
    return [row.strip().lower() for row in rows]


def test_theme_explorer_token_jobs_match_app_theme_table() -> None:
    jobs = [job.id for job in list_token_jobs()]
    assert jobs == _app_theme_jobs()


def test_theme_explorer_template_declares_token_jobs() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    assert 'data-token-job="{{ job.id }}"' in html
    assert "{% for job in board_sections %}" in html
    assert "{{ token.name }}" in html
    assert len(TOKEN_JOBS) == 10


def test_theme_explorer_stays_in_public_token_namespace() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    assert "--chirp-theme-" not in html
    assert "--chirp_theme-" not in html
