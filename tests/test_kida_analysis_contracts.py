"""Contracts backed by Kida's static analysis APIs."""

import re
from pathlib import Path

from kida.analysis import EscapeAuditFinding, audit_escaping
from kida.lexer import Lexer
from kida.parser import Parser

TEMPLATES_DIR = Path("src/chirp_ui/templates/chirpui")
BARE_SAFE_RE = re.compile(r"\|\s*safe(?!\s*\()")


def _template_escape_findings() -> list[tuple[str, EscapeAuditFinding]]:
    findings: list[tuple[str, EscapeAuditFinding]] = []
    for path in sorted(TEMPLATES_DIR.glob("*.html")):
        source = path.read_text(encoding="utf-8")
        tokens = list(Lexer(source).tokenize())
        ast = Parser(tokens, name=f"chirpui/{path.name}", source=source).parse()
        findings.extend(
            (path.name, finding) for finding in audit_escaping(ast, include_output_sites=False)
        )
    return findings


def test_safe_filter_sites_explain_trust_boundary() -> None:
    """Every `| safe` in shipped macros must document why escaping is bypassed."""
    safe_sites = [
        (template, finding)
        for template, finding in _template_escape_findings()
        if finding.kind == "safe-filter"
    ]

    assert safe_sites, "escape audit should cover at least one trusted-markup site"

    missing_reason = [
        f"{template}:{finding.lineno} {finding.expression}"
        for template, finding in safe_sites
        if finding.suggestion
    ]
    assert missing_reason == []


def test_templates_do_not_disable_autoescape() -> None:
    disabled = [
        f"{template}:{finding.lineno}"
        for template, finding in _template_escape_findings()
        if finding.kind == "autoescape-disabled"
    ]
    assert disabled == []


def test_template_source_does_not_use_bare_safe_filter() -> None:
    bare_safe_sites: list[str] = []
    for path in sorted(TEMPLATES_DIR.glob("*.html")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if BARE_SAFE_RE.search(line):
                bare_safe_sites.append(f"{path.name}:{line_no}")

    assert bare_safe_sites == []
