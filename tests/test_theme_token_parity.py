import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_THEME = ROOT / "docs" / "APP-THEME.md"
TOKENS = ROOT / "docs" / "TOKENS.md"
SHOWCASE = ROOT / "examples" / "design-system-gap-showcase" / "index.html"


class _TokenJobParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.jobs: list[str] = []
        self.profiles: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if attr_map.get("data-token-job"):
            self.jobs.append(attr_map["data-token-job"] or "")
        if attr_map.get("data-theme-profile"):
            self.profiles.add(attr_map["data-theme-profile"] or "")


def _app_theme_jobs() -> list[str]:
    text = APP_THEME.read_text(encoding="utf-8")
    rows = re.findall(r"^\| ([A-Z][^|]+) \| `--chirpui-", text, flags=re.MULTILINE)
    return [row.strip().lower() for row in rows]


def test_app_theme_first_token_jobs_match_visual_audit_explorer() -> None:
    parser = _TokenJobParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))

    assert parser.jobs == _app_theme_jobs()


def test_token_docs_name_all_visual_theme_profiles() -> None:
    parser = _TokenJobParser()
    parser.feed(SHOWCASE.read_text(encoding="utf-8"))
    docs_text = APP_THEME.read_text(encoding="utf-8") + "\n" + TOKENS.read_text(encoding="utf-8")

    for profile in parser.profiles:
        assert profile in docs_text


def test_visual_audit_stays_in_public_token_namespace() -> None:
    text = SHOWCASE.read_text(encoding="utf-8")

    assert "--chirp-theme-" not in text
    assert "--chirp_theme-" not in text


def test_app_theme_docs_define_override_escalation_ladder() -> None:
    text = APP_THEME.read_text(encoding="utf-8")

    for required in [
        "## Override Escalation Ladder",
        "Public token",
        "Semantic alias",
        "App override",
        "Token proposal",
        "@layer app.overrides",
        "Do not skip directly to component selectors",
    ]:
        assert required in text
