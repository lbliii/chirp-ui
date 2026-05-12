import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC_SHOWCASE = REPO_ROOT / "examples" / "static-showcase" / "index.html"
DOC = REPO_ROOT / "docs" / "STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"

LEGACY_HELPER_RE = re.compile(
    r"chirpui-(?:clamp-[23]|display|focus-ring|font-[^ ]+|list-reset|m[bt]-[^ ]+|"
    r"measure-[^ ]+|min-w-0|placeholder-inline|prose-[^ ]+|scroll-x|text-muted|"
    r"truncate|ui-[^ ]+|visually-hidden)"
)


def _legacy_helper_classes(text: str) -> Counter[str]:
    classes: list[str] = []
    for match in re.finditer(r'class="([^"]*)"', text):
        classes.extend(
            cls for cls in match.group(1).split() if LEGACY_HELPER_RE.fullmatch(cls)
        )
    return Counter(classes)


def test_static_showcase_only_keeps_visually_hidden_helper_contracts() -> None:
    helpers = _legacy_helper_classes(STATIC_SHOWCASE.read_text(encoding="utf-8"))

    assert set(helpers) == {"chirpui-visually-hidden"}
    assert helpers["chirpui-visually-hidden"] == 102


def test_static_showcase_legacy_helper_triage_doc_matches_inventory() -> None:
    text = DOC.read_text(encoding="utf-8")

    for required in [
        "102 legacy helper class",
        "`chirpui-visually-hidden` | 102 | component contract",
        "Header note copy",
        "Settings-row labels",
        "Do not introduce typography or spacing helpers",
    ]:
        assert required in text

    assert "STATIC-SHOWCASE-LEGACY-HELPER-TRIAGE.md" in INDEX.read_text(
        encoding="utf-8"
    )
