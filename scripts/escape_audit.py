"""Print a Kida-backed escape audit for shipped chirp-ui macros.

The report is intentionally read-only: it gives reviewers a stable inventory
of trusted-markup boundaries without mutating generated artifacts.

Usage
-----
From the repo root::

    python scripts/escape_audit.py
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from kida.analysis import audit_escaping
from kida.lexer import Lexer
from kida.parser import Parser

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = REPO_ROOT / "src" / "chirp_ui" / "templates" / "chirpui"


@dataclass(frozen=True, slots=True)
class AuditRow:
    template: str
    line: int
    kind: str
    expression: str
    message: str


def _markdown_cell(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def collect_rows() -> list[AuditRow]:
    rows: list[AuditRow] = []
    for path in sorted(TEMPLATE_ROOT.glob("*.html")):
        source = path.read_text(encoding="utf-8")
        tokens = list(Lexer(source).tokenize())
        ast = Parser(tokens, name=f"chirpui/{path.name}", source=source).parse()
        rows.extend(
            AuditRow(
                template=path.name,
                line=finding.lineno or 0,
                kind=finding.kind,
                expression=finding.expression or "",
                message=finding.message,
            )
            for finding in audit_escaping(ast, include_output_sites=False)
        )
    return sorted(rows, key=lambda row: (row.template, row.line, row.kind, row.expression))


def render_markdown(rows: list[AuditRow]) -> str:
    lines = [
        "# chirp-ui Kida Escape Audit",
        "",
        "| Template | Line | Kind | Expression | Message |",
        "|---|---:|---|---|---|",
    ]
    lines.extend(
        "| "
        + " | ".join(
            (
                _markdown_cell(row.template),
                _markdown_cell(row.line),
                _markdown_cell(row.kind),
                _markdown_cell(row.expression),
                _markdown_cell(row.message),
            )
        )
        + " |"
        for row in rows
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    sys.stdout.write(render_markdown(collect_rows()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
