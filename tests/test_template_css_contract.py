from __future__ import annotations

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui"
CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"


TARGET_PREFIXES = (
    "chirpui-app-shell",
    "chirpui-sidebar",
    "chirpui-action-strip",
    "chirpui-filter-bar",
    "chirpui-command-bar",
    "chirpui-search-header",
    "chirpui-selection-bar",
)


def _extract_template_classes() -> set[str]:
    class_attr_pattern = re.compile(
        r"""\bclass\s*=\s*(["'])(.*?)\1""",
        re.IGNORECASE | re.DOTALL,
    )
    class_name_pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_-]*")
    classes: set[str] = set()

    for template_file in TEMPLATES_DIR.rglob("*.html"):
        content = template_file.read_text(encoding="utf-8")
        content = re.sub(r"\{#.*?#\}", "", content, flags=re.DOTALL)
        for match in class_attr_pattern.finditer(content):
            class_attr_value = match.group(2)
            # Skip dynamic class attributes to avoid Kida false positives.
            if "{{" in class_attr_value or "{%" in class_attr_value:
                continue
            for class_match in class_name_pattern.finditer(class_attr_value):
                classes.add(class_match.group(0))
    return classes


def _extract_css_defined_classes() -> set[str]:
    class_selector_pattern = re.compile(r"\.([a-zA-Z_][a-zA-Z0-9_-]*)")
    content = CSS_PATH.read_text(encoding="utf-8")
    return {match.group(1) for match in class_selector_pattern.finditer(content)}


def test_target_template_classes_exist_in_css() -> None:
    template_classes = _extract_template_classes()
    css_classes = _extract_css_defined_classes()
    missing = sorted(
        class_name
        for class_name in template_classes
        if class_name.startswith(TARGET_PREFIXES) and class_name not in css_classes
    )
    assert not missing, "Shell/sidebar template classes missing CSS definitions: " + ", ".join(
        missing
    )
