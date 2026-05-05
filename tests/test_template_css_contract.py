import json
import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui"
CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"
TRANSITIONS_CSS_PATH = (
    Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui-transitions.css"
)
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples/component-showcase/templates"
MANIFEST_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/manifest.json"


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

SHOWCASE_TEMPLATE_PACKS = {
    # These files expose macro groups whose shipped classes are registry-backed
    # by CSS-only descriptors or by the nested components they compose.
    "ascii_icon.html",
    "auth.html",
    "bento_grid.html",
    "command_bar.html",
    "config_card.html",
    "config_dashboard.html",
    "islands.html",
    "modal_overlay.html",
    "nav_link.html",
    "oob.html",
    "share_menu.html",
    "shell_frame.html",
    "state_primitives.html",
    "status_with_hint.html",
    "tabbed_page_layout.html",
}

STABLE_COMPONENT_SHOWCASE_DEFERRALS = {
    # These are stable but have focused docs/browser coverage elsewhere; keep
    # them explicit so new stable components cannot silently skip the showcase.
    "copy-btn",
    "empty-panel-state",
    "latest-line",
    "panel",
    "rendered-content",
    "tag-browse",
}


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


def _extract_showcase_imports() -> set[str]:
    import_pattern = re.compile(
        r"""\{%\s*(?:from|include)\s+["']chirpui/([^"']+)["']""",
        re.IGNORECASE,
    )
    imports: set[str] = set()
    for template_file in EXAMPLES_DIR.rglob("*.html"):
        imports.update(import_pattern.findall(template_file.read_text(encoding="utf-8")))
    return imports


def _manifest_components() -> dict[str, dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return manifest["components"]


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


def test_example_static_chirpui_classes_exist_in_css() -> None:
    template_classes = _extract_template_classes(EXAMPLES_DIR)
    css_classes = _extract_css_defined_classes()
    missing = sorted(
        class_name
        for class_name in template_classes
        if class_name.startswith("chirpui-") and class_name not in css_classes
    )
    assert not missing, "Example templates reference missing chirpui-* CSS classes: " + ", ".join(
        missing
    )


def test_showcase_imported_templates_are_manifest_backed() -> None:
    components = _manifest_components()
    manifest_templates = {
        str(entry["template"]) for entry in components.values() if entry.get("template")
    }
    imported_templates = _extract_showcase_imports()
    missing = sorted(imported_templates - manifest_templates - SHOWCASE_TEMPLATE_PACKS)
    assert not missing, (
        "Showcase imports chirpui templates that are not in manifest.json and not "
        "documented as macro packs: " + ", ".join(missing)
    )


def test_stable_templated_components_have_showcase_coverage() -> None:
    components = _manifest_components()
    imported_templates = _extract_showcase_imports()
    missing = sorted(
        name
        for name, entry in components.items()
        if entry["maturity"] == "stable"
        and entry["role"] == "component"
        and entry.get("template")
        and entry["template"] not in imported_templates
        and name not in STABLE_COMPONENT_SHOWCASE_DEFERRALS
    )
    assert not missing, (
        "Stable templated components need showcase coverage or an explicit deferral: "
        + ", ".join(missing)
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
