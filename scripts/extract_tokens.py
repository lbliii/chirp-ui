#!/usr/bin/env python3
"""Extract --chirpui-* custom property declarations from chirpui.css.

Produces a Python dict literal suitable for pasting into tokens.py.
Deduplicates (same property may appear in :root, [data-theme], @media, etc.)
and categorizes by prefix heuristics.

Usage:
    uv run python scripts/extract_tokens.py
"""

import re
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parents[1] / "src/chirp_ui/templates/chirpui.css"

PROP_RE = re.compile(r"^\s*(--chirpui-[a-z0-9-]+)\s*:", re.MULTILINE)

CATEGORY_PREFIXES: list[tuple[str, str]] = [
    ("--chirpui-spacing", "spacing"),
    ("--chirpui-space-", "spacing"),
    ("--chirpui-measure-", "spacing"),
    ("--chirpui-radius", "radius"),
    ("--chirpui-font-", "typography"),
    ("--chirpui-ui-", "typography"),
    ("--chirpui-prose-", "typography"),
    ("--chirpui-line-height-", "typography"),
    ("--chirpui-ascii-font", "typography"),
    ("--chirpui-motion-", "motion"),
    ("--chirpui-ease-", "motion"),
    ("--chirpui-duration-", "motion"),
    ("--chirpui-easing-", "motion"),
    ("--chirpui-shadow-", "elevation"),
    ("--chirpui-sidebar-", "layout"),
    ("--chirpui-container-", "layout"),
    ("--chirpui-grid-", "layout"),
    ("--chirpui-shell-", "layout"),
    ("--chirpui-panel-", "layout"),
    ("--chirpui-alert-", "component"),
    ("--chirpui-badge-", "component"),
    ("--chirpui-btn-", "component"),
    ("--chirpui-card-", "component"),
    ("--chirpui-modal-", "component"),
    ("--chirpui-toast-", "component"),
    ("--chirpui-tab-", "component"),
    ("--chirpui-tooltip-", "component"),
    ("--chirpui-dropdown-", "component"),
    ("--chirpui-surface-", "component"),
    ("--chirpui-aura-", "component"),
    ("--chirpui-hero-", "component"),
    ("--chirpui-progress-", "component"),
    ("--chirpui-skeleton-", "component"),
    ("--chirpui-chat-", "component"),
    ("--chirpui-dnd-", "component"),
    ("--chirpui-streaming-", "component"),
    ("--chirpui-code-", "component"),
    ("--chirpui-form-", "component"),
    ("--chirpui-filter-", "component"),
    ("--chirpui-ascii-", "component"),
    ("--chirpui-accent", "color"),
    ("--chirpui-bg", "color"),
    ("--chirpui-fg", "color"),
    ("--chirpui-border", "color"),
    ("--chirpui-muted", "color"),
    ("--chirpui-text-", "color"),
    ("--chirpui-link-", "color"),
    ("--chirpui-success", "color"),
    ("--chirpui-warning", "color"),
    ("--chirpui-error", "color"),
    ("--chirpui-info", "color"),
    ("--chirpui-danger", "color"),
]

SCOPE_PREFIXES: list[tuple[str, str]] = [
    ("--chirpui-btn-", "btn"),
    ("--chirpui-card-", "card"),
    ("--chirpui-badge-", "badge"),
    ("--chirpui-alert-", "alert"),
    ("--chirpui-modal-", "modal"),
    ("--chirpui-toast-", "toast"),
    ("--chirpui-tab-", "tab"),
    ("--chirpui-tooltip-", "tooltip"),
    ("--chirpui-dropdown-", "dropdown"),
    ("--chirpui-surface-", "surface"),
    ("--chirpui-aura-", "aura"),
    ("--chirpui-hero-", "hero"),
    ("--chirpui-sidebar-", "sidebar"),
    ("--chirpui-shell-", "app-shell"),
    ("--chirpui-panel-", "panel"),
    ("--chirpui-progress-", "progress-bar"),
    ("--chirpui-skeleton-", "skeleton"),
    ("--chirpui-chat-", "chat-layout"),
    ("--chirpui-dnd-", "dnd"),
    ("--chirpui-streaming-", "streaming"),
    ("--chirpui-code-", "code"),
    ("--chirpui-form-", "form"),
    ("--chirpui-filter-", "filter"),
    ("--chirpui-ascii-", "ascii"),
]


def categorize(prop: str) -> str:
    for prefix, cat in CATEGORY_PREFIXES:
        if prop.startswith(prefix):
            return cat
    return "color"


def scope_of(prop: str) -> str:
    for prefix, scope in SCOPE_PREFIXES:
        if prop.startswith(prefix):
            return scope
    return "global"


def main() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    props: set[str] = set()
    for m in PROP_RE.finditer(css):
        props.add(m.group(1))

    by_category: dict[str, list[str]] = {}
    for prop in sorted(props):
        cat = categorize(prop)
        by_category.setdefault(cat, []).append(prop)

    print(f"# Extracted {len(props)} unique --chirpui-* custom properties\n")
    print("TOKEN_CATALOG: dict[str, TokenDef] = {")
    for cat in sorted(by_category):
        print(f"    # -- {cat} ---")
        for prop in by_category[cat]:
            scope = scope_of(prop)
            scope_arg = f', scope="{scope}"' if scope != "global" else ""
            print(f'    "{prop}": TokenDef("{prop}", "{cat}"{scope_arg}),')
    print("}")
    print(f"\n# Total: {len(props)} tokens across {len(by_category)} categories")
    for cat in sorted(by_category):
        print(f"#   {cat}: {len(by_category[cat])}")


if __name__ == "__main__":
    main()
