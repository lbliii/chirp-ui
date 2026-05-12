import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_TEMPLATES = REPO_ROOT / "examples" / "component-showcase" / "templates"
BASE = SHOWCASE_TEMPLATES / "base.html"

HIGH_VISIBILITY_TEMPLATES = [
    SHOWCASE_TEMPLATES / "showcase" / "navigation.html",
    SHOWCASE_TEMPLATES / "showcase" / "dashboard.html",
    SHOWCASE_TEMPLATES / "showcase" / "islands.html",
    SHOWCASE_TEMPLATES / "showcase" / "ui.html",
]

LEGACY_CLASS_RE = re.compile(
    r'class="[^"]*chirpui-'
    r"(?:display|text-muted|font-[^\" ]+|mt-[^\" ]+|mb-[^\" ]+|ui-[^\" ]+|scroll-x)"
)


def test_high_visibility_showcase_templates_use_local_copy_chrome() -> None:
    for template in HIGH_VISIBILITY_TEMPLATES:
        text = template.read_text(encoding="utf-8")
        assert not LEGACY_CLASS_RE.search(text), template


def test_component_showcase_defines_local_copy_chrome() -> None:
    text = BASE.read_text(encoding="utf-8")

    for required in [
        ".showcase-copy",
        ".showcase-copy--spaced",
        ".showcase-copy--section",
        ".showcase-copy--rhythm",
    ]:
        assert required in text
