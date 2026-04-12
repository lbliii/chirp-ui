from __future__ import annotations

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui"
CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
TRANSITIONS_CSS_PATH = (
    Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui-transitions.css"
)
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples/component-showcase/templates"


TARGET_PREFIXES = (
    "chirpui-frame",
    "chirpui-app-shell",
    "chirpui-route-tab",
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
    "chirpui-chat-layout",
    "chirpui-page-fill",
    "chirpui-site-shell",
    "chirpui-site-header",
    "chirpui-site-footer",
    "chirpui-site-nav",
    "chirpui-band",
    "chirpui-feature-section",
    "chirpui-feature-stack",
)

EXAMPLE_LAYOUT_PREFIXES = (
    "chirpui-action-strip",
    "chirpui-cluster",
    "chirpui-flow",
    "chirpui-frame",
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

    Covers additional classes that are emitted dynamically (via Kida ``{{ }}``
    expressions) and therefore missed by the static template class scanner.
    These supplement the descriptor-driven test below.
    """
    css_classes = _extract_css_defined_classes()
    required: list[str] = [
        "chirpui-chat-layout--fill",
        "chirpui-app-shell__main--fill",
        "chirpui-page-fill",
        "chirpui-chat-layout__messages-body",
    ]
    missing = [cls for cls in required if cls not in css_classes]
    assert not missing, "Required dynamic BEM classes missing from CSS: " + ", ".join(missing)


def test_component_descriptor_elements_and_modifiers_exist_in_css() -> None:
    """Elements and modifiers declared in COMPONENTS must have CSS definitions.

    Block root classes (e.g. ``.chirpui-confirm``) are not enforced because
    some components style only via modifier selectors (e.g.
    ``.chirpui-confirm--danger``).  Variants and sizes have their own test.
    """
    from chirp_ui.components import COMPONENTS

    css_classes = _extract_css_defined_classes()
    missing: list[str] = []
    for _name, desc in sorted(COMPONENTS.items()):
        for m in desc.modifiers:
            if m:
                expected = f"chirpui-{desc.block}--{m}"
                if expected not in css_classes:
                    missing.append(expected)
        for e in desc.elements:
            expected = f"chirpui-{desc.block}__{e}"
            if expected not in css_classes:
                missing.append(expected)
    assert not missing, (
        f"Component element/modifier classes missing from CSS ({len(missing)}): "
        + ", ".join(missing[:20])
        + ("..." if len(missing) > 20 else "")
    )


def test_component_descriptor_key_variants_exist_in_css() -> None:
    """Non-default variant and size modifiers for high-traffic components must have CSS.

    Checks a curated set of components where every declared variant/size is
    expected to have an explicit CSS rule. Components whose variants are
    purely validation fallbacks (many ASCII components) are not included.
    """
    from chirp_ui.components import COMPONENTS

    enforced = {
        "btn",
        "alert",
        "badge",
        "surface",
        "toast",
        "overlay",
        "hero",
        "aura_tone",
        "tooltip",
        "status-indicator",
        "neon",
        "site-header",
        "band",
        "feature-section",
    }
    css_classes = _extract_css_defined_classes()
    missing: list[str] = []
    for name in sorted(enforced):
        desc = COMPONENTS.get(name)
        if desc is None:
            continue
        for v in desc.variants:
            if v and v != "default":
                expected = f"chirpui-{desc.block}--{v}"
                if expected not in css_classes:
                    missing.append(expected)
    assert not missing, (
        f"Key component variant/size classes missing from CSS ({len(missing)}): "
        + ", ".join(missing[:20])
        + ("..." if len(missing) > 20 else "")
    )


def test_token_catalog_covers_css() -> None:
    """Every token in TOKEN_CATALOG must exist in chirpui.css."""
    from chirp_ui.tokens import TOKEN_CATALOG, extract_css_tokens

    css_tokens = extract_css_tokens()
    catalog_names = set(TOKEN_CATALOG)
    missing_from_css = sorted(catalog_names - css_tokens)
    assert not missing_from_css, (
        f"TOKEN_CATALOG has {len(missing_from_css)} entries not in CSS: "
        + ", ".join(missing_from_css[:10])
    )
