from __future__ import annotations

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui"
CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
TRANSITIONS_CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui-transitions.css"
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples/component-showcase/templates"


TARGET_PREFIXES = (
    "chirpui-app-shell",
    "chirpui-sidebar",
    "chirpui-action-strip",
    "chirpui-config-row",
    "chirpui-filter-bar",
    "chirpui-command-bar",
    "chirpui-resource-index",
    "chirpui-resource-card",
    "chirpui-search-header",
    "chirpui-selection-bar",
    "chirpui-entity-header",
    "chirpui-inline-edit",
    "chirpui-metric-card",
    "chirpui-metric-grid",
    "chirpui-row-actions",
)

EXAMPLE_LAYOUT_PREFIXES = (
    "chirpui-action-strip",
    "chirpui-cluster",
    "chirpui-flow",
    "chirpui-grid",
    "chirpui-inline",
    "chirpui-mb-",
    "chirpui-measure",
    "chirpui-metric-",
    "chirpui-mt-",
    "chirpui-resource-",
    "chirpui-result-slot",
    "chirpui-stack",
)


def _extract_template_classes(base_dir: Path) -> set[str]:
    class_attr_pattern = re.compile(
        r"""\bclass\s*=\s*(["'])(.*?)\1""",
        re.IGNORECASE | re.DOTALL,
    )
    class_name_pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_-]*")
    classes: set[str] = set()

    for template_file in base_dir.rglob("*.html"):
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
    if TRANSITIONS_CSS_PATH.exists():
        content += TRANSITIONS_CSS_PATH.read_text(encoding="utf-8")
    return {match.group(1) for match in class_selector_pattern.finditer(content)}


def test_target_template_classes_exist_in_css() -> None:
    template_classes = _extract_template_classes(TEMPLATES_DIR)
    css_classes = _extract_css_defined_classes()
    missing = sorted(
        class_name
        for class_name in template_classes
        if class_name.startswith(TARGET_PREFIXES) and class_name not in css_classes
    )
    assert not missing, "Shell/sidebar template classes missing CSS definitions: " + ", ".join(
        missing
    )


def test_example_chirpui_classes_exist_in_css() -> None:
    template_classes = _extract_template_classes(EXAMPLES_DIR)
    css_classes = _extract_css_defined_classes()
    missing = sorted(
        class_name
        for class_name in template_classes
        if class_name.startswith(EXAMPLE_LAYOUT_PREFIXES) and class_name not in css_classes
    )
    assert not missing, "Example templates reference missing spacing/layout classes: " + ", ".join(
        missing
    )


def test_dynamic_bem_modifiers_used_in_templates_exist_in_css() -> None:
    """Dynamic BEM modifiers used in button, modal, dropdown, forms exist in CSS.

    Covers the blocks we enforce validate_variant/validate_size for.
    Some variants use base styling (no explicit modifier class in CSS).
    """
    css_classes = _extract_css_defined_classes()
    # Subset of VARIANT_REGISTRY/SIZE_REGISTRY that have explicit CSS
    required: list[str] = [
        "chirpui-btn--primary",
        "chirpui-btn--danger",
        "chirpui-btn--ghost",
        "chirpui-btn--sm",
        "chirpui-modal--small",
        "chirpui-modal--large",
        "chirpui-dropdown__item--danger",
        "chirpui-star-rating--sm",
        "chirpui-star-rating--lg",
        "chirpui-thumbs--sm",
        "chirpui-thumbs--lg",
        "chirpui-segmented--sm",
    ]
    missing = [cls for cls in required if cls not in css_classes]
    assert not missing, "Required dynamic BEM classes missing from CSS: " + ", ".join(missing)
