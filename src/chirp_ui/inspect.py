"""Design system introspection — dump the chirp-ui API surface.

Usage::

    python -m chirp_ui.inspect              # JSON report
    python -m chirp_ui.inspect --summary    # compact table
    python -m chirp_ui.inspect --tokens     # token catalog only
    python -m chirp_ui.inspect --components # component descriptors only
"""

import argparse
import json
import sys

from chirp_ui.components import COMPONENTS, design_system_report
from chirp_ui.tokens import TOKEN_CATALOG


def _print_summary() -> None:
    report = design_system_report()
    stats = report["stats"]
    print("chirp-ui design system surface")
    print("=" * 40)
    print(f"Components: {stats['total_components']}")
    print(f"Tokens:     {stats['total_tokens']}")
    print()
    print("Component categories:")
    for cat, count in sorted(stats["component_categories"].items()):
        print(f"  {cat:20s} {count:3d}")
    print()
    print("Token categories:")
    for cat, count in sorted(stats["token_categories"].items()):
        print(f"  {cat:20s} {count:3d}")


def _print_components() -> None:
    for name, desc in sorted(COMPONENTS.items()):
        parts = [f"  block: {desc.block}"]
        if desc.variants:
            parts.append(f"  variants: {', '.join(v or '(empty)' for v in desc.variants)}")
        if desc.sizes:
            parts.append(f"  sizes: {', '.join(s or '(empty)' for s in desc.sizes)}")
        if desc.modifiers:
            parts.append(f"  modifiers: {', '.join(desc.modifiers)}")
        if desc.elements:
            parts.append(f"  elements: {', '.join(desc.elements)}")
        if desc.slots:
            parts.append(f"  slots: {', '.join(s or '(default)' for s in desc.slots)}")
        if desc.tokens:
            parts.append(f"  tokens: {', '.join(desc.tokens)}")
        if desc.template:
            parts.append(f"  template: {desc.template}")
        if desc.category:
            parts.append(f"  category: {desc.category}")
        print(f"{name}:")
        print("\n".join(parts))
        print()


def _print_tokens() -> None:
    by_category: dict[str, list[str]] = {}
    for name, tdef in sorted(TOKEN_CATALOG.items()):
        by_category.setdefault(tdef.category, []).append(
            f"  {name}" + (f" [{tdef.scope}]" if tdef.scope != "global" else "")
        )
    for cat in sorted(by_category):
        print(f"{cat} ({len(by_category[cat])}):")
        for line in by_category[cat]:
            print(line)
        print()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="chirp-ui-inspect",
        description="Inspect the chirp-ui design system surface.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--summary", action="store_true", help="compact summary table")
    group.add_argument("--components", action="store_true", help="component descriptors only")
    group.add_argument("--tokens", action="store_true", help="token catalog only")
    group.add_argument("--json", action="store_true", help="full JSON report (default)")
    args = parser.parse_args(argv)

    if args.summary:
        _print_summary()
    elif args.components:
        _print_components()
    elif args.tokens:
        _print_tokens()
    else:
        report = design_system_report()
        json.dump(report, sys.stdout, indent=2, default=str)
        print()


if __name__ == "__main__":
    main()
