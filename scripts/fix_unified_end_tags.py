"""Replace bare ``{% end %}`` closers with explicit Kida end tags.

Uses the Kida parser's ``_unified_end_closures`` metadata (same signal as
``kida check --strict``). Run from repo root::

    python scripts/fix_unified_end_tags.py
    python scripts/fix_unified_end_tags.py --check
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from kida import Environment, FileSystemLoader
from kida.lexer import Lexer
from kida.parser import Parser

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui"
END_TAG_RE = re.compile(r"\{%-?\s*(end)\s*-?%\}")
# Kida accepts unified {% end %} for slots and try/fallback blocks.
_SKIP_EXPLICIT = frozenset({"slot", "try"})


def _explicit_close(block_type: str) -> str:
    if block_type == "block":
        return "{% endblock %}"
    return f"{{% end{block_type} %}}"


def _fix_file(path: Path) -> int:
    source = path.read_text(encoding="utf-8")
    env = Environment(loader=FileSystemLoader("."))
    lexer = Lexer(source, env._lexer_config)
    tokens = list(lexer.tokenize())
    sparser = Parser(
        tokens,
        name=path.name,
        filename=str(path),
        source=source,
        autoescape=True,
    )
    sparser.parse()
    closures = sparser._unified_end_closures
    if not closures:
        return 0

    lines = source.splitlines(keepends=True)
    fixes = 0
    for lineno, col_offset, closing in reversed(closures):
        if closing in _SKIP_EXPLICIT:
            continue
        line = lines[lineno - 1]
        for match in END_TAG_RE.finditer(line):
            if match.start(1) == col_offset:
                want = _explicit_close(closing)
                lines[lineno - 1] = line[: match.start()] + want + line[match.end() :]
                fixes += 1
                break
        else:
            print(
                f"fix-unified-end: no match {path}:{lineno}:{col_offset}",
                file=sys.stderr,
            )

    if fixes:
        path.write_text("".join(lines), encoding="utf-8")
    return fixes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Template directory to fix (default: templates/chirpui)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report files that would change without writing",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f"fix-unified-end: not a directory: {root}", file=sys.stderr)
        return 2

    total = 0
    changed_files = 0
    for path in sorted(root.rglob("*.html")):
        if args.check:
            before = path.read_text(encoding="utf-8")
            fixes = _fix_file(path)
            if fixes:
                path.write_text(before, encoding="utf-8")
        else:
            fixes = _fix_file(path)
        if fixes:
            changed_files += 1
            total += fixes
            action = "would fix" if args.check else "fixed"
            print(f"{action} {fixes} tag(s) in {path.relative_to(REPO_ROOT)}")

    if args.check and total:
        print(f"{changed_files} file(s) would change ({total} tag(s))", file=sys.stderr)
        return 1

    print(f"fixed {total} tag(s) across {changed_files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
