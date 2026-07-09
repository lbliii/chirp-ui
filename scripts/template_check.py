"""Strict Kida template verification for chirp-ui partials.

``kida check`` alone cannot validate chirp-ui templates: component macros rely on
filters and globals registered at Chirp runtime (``use_chirp_ui`` /
``make_preview_env``). This script mirrors ``kida check <dir> --strict`` with
those stubs wired so parse/load resolution matches production.

Usage (from repo root)::

    python scripts/template_check.py
    python scripts/template_check.py --root src/chirp_ui/templates/chirpui
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kida import Environment, FileSystemLoader
from kida.exceptions import TemplateSyntaxError
from kida.lexer import Lexer
from kida.parser import Parser

from chirp_ui.preview_env import make_preview_env

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui"
TEMPLATE_GLOBS = ("*.html", "*.kida")
# Slots and try/fallback only support unified {% end %} in practice.
_SKIP_STRICT = frozenset({"slot", "try"})


def _iter_templates(root: Path) -> list[Path]:
    seen: set[Path] = set()
    for glob in TEMPLATE_GLOBS:
        for path in root.rglob(glob):
            seen.add(path)
    return sorted(seen)


def _explicit_close_suggestion(block_type: str) -> str:
    if block_type == "block":
        return "{% endblock %}"
    return f"{{% end{block_type} %}}"


def _make_check_env(loader_root: Path) -> Environment:
    """Preview stubs with a loader root that resolves chirpui/ import paths."""
    env = make_preview_env()
    wired = Environment(
        loader=FileSystemLoader(str(loader_root)),
        autoescape=env.autoescape,
    )
    wired.update_filters(env.filters)
    for name, value in env.globals.items():
        wired.add_global(name, value)
    return wired


def _template_loader_root(check_root: Path) -> Path:
    """Return the FileSystemLoader root that resolves ``chirpui/…`` imports."""
    if check_root.name == "chirpui" and (check_root.parent / "chirpui").is_dir():
        return check_root.parent
    return check_root


def _template_name(check_root: Path, path: Path) -> str:
    rel = path.relative_to(check_root).as_posix()
    if check_root.name == "chirpui":
        return f"chirpui/{rel}"
    return rel


def run_check(check_root: Path) -> int:
    root = check_root.resolve()
    if not root.is_dir():
        print(f"template-check: not a directory: {root}", file=sys.stderr)
        return 2

    loader_root = _template_loader_root(root)
    env = _make_check_env(loader_root)

    errors = 0
    strict_warnings = 0
    failed_loads: set[str] = set()

    for path in _iter_templates(root):
        rel = _template_name(root, path)
        try:
            tpl = env.get_template(rel)
        except Exception as exc:
            print(f"{rel}: {exc}", file=sys.stderr)
            errors += 1
            failed_loads.add(rel)
            continue

        try:
            source = path.read_text(encoding="utf-8")
            lexer = Lexer(source, env._lexer_config)
            tokens = list(lexer.tokenize())
            should_escape = env.select_autoescape(rel)
            sparser = Parser(
                tokens,
                name=rel,
                filename=str(path),
                source=source,
                autoescape=should_escape,
            )
            sparser.parse()
        except OSError as exc:
            print(f"{rel}: {exc}", file=sys.stderr)
            errors += 1
            continue
        except TemplateSyntaxError as exc:
            print(f"{rel}: {exc}", file=sys.stderr)
            errors += 1
            continue

        for lineno, _col, closing in sparser._unified_end_closures:
            if closing in _SKIP_STRICT:
                continue
            want = _explicit_close_suggestion(closing)
            print(
                f"{rel}:{lineno}: strict: unified {{% end %}} closes '{closing}' — prefer {want}",
                file=sys.stderr,
            )
            strict_warnings += 1

        _ = tpl  # load succeeded; keep for future validate-calls wiring

    if strict_warnings:
        print(
            f"template-check: strict: {strict_warnings} unified {{% end %}} tag(s)",
            file=sys.stderr,
        )
        errors += strict_warnings

    if errors:
        print(f"template-check: {errors} problem(s)", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Directory of chirp-ui templates to verify (default: templates/chirpui)",
    )
    args = parser.parse_args(argv)
    return run_check(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
