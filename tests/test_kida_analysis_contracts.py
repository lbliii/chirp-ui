"""Contracts backed by Kida's static analysis APIs."""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from kida.analysis import (
    EscapeAuditFinding,
    PrivacyFinding,
    audit_escaping,
    check_context_contract,
    lint_privacy,
)
from kida.analysis.dependencies import DependencyWalker
from kida.lexer import Lexer
from kida.nodes import Block, Def, FromImport, Import, Node
from kida.parser import Parser

from chirp_ui._macro_introspect import macros_in_template

TEMPLATES_DIR = Path("src/chirp_ui/templates/chirpui")
SHOWCASE_TEMPLATES_DIR = Path("examples/component-showcase/templates")
PRIVACY_LINT_DIRS = (
    SHOWCASE_TEMPLATES_DIR,
    Path("src/bengal_themes/chirp_theme/templates"),
)
BARE_SAFE_RE = re.compile(r"\|\s*safe(?!\s*\()")
ALLOWED_PRIVACY_FINDINGS = frozenset(
    {
        (
            "K-PRI-001",
            "examples/component-showcase/templates/showcase/_form_demo.html",
            "email",
        ),
        (
            "K-PRI-001",
            "examples/component-showcase/templates/showcase/forms.html",
            "password_field",
        ),
    }
)
SHOWCASE_PAGE_CONTEXTS = {
    "index.html": {"current_path"},
    "showcase/animation.html": {"current_path"},
    "showcase/ascii.html": {"current_path"},
    "showcase/ascii_primitives.html": {"current_path"},
    "showcase/buttons.html": {"current_path"},
    "showcase/calendar.html": {"current_path", "month_label", "next_url", "prev_url", "weeks"},
    "showcase/cards.html": {"current_path"},
    "showcase/carousel.html": {"current_path"},
    "showcase/chrome.html": {"current_path"},
    "showcase/dashboard.html": {"current_path"},
    "showcase/data-display.html": {"current_path"},
    "showcase/data.html": {
        "current_path",
        "density",
        "end_row",
        "page",
        "q",
        "query_string",
        "role",
        "rows",
        "sort_col",
        "sort_dir",
        "start_row",
        "total_pages",
        "total_rows",
    },
    "showcase/demo.html": {"current_path"},
    "showcase/effects.html": {"current_path"},
    "showcase/forms.html": {"current_path"},
    "showcase/htmx.html": {"current_path"},
    "showcase/islands.html": {"current_path"},
    "showcase/islands_grid_state.html": {"current_path"},
    "showcase/islands_upload_state.html": {"current_path"},
    "showcase/islands_wizard_state.html": {"current_path"},
    "showcase/layout.html": {"current_path", "direction"},
    "showcase/messenger.html": {"current_path"},
    "showcase/navigation.html": {"current_path"},
    "showcase/sections.html": {"current_path"},
    "showcase/shell_actions.html": {"current_path", "shell_actions"},
    "showcase/social.html": {"current_path"},
    "showcase/streaming.html": {"current_path"},
    "showcase/typography.html": {"current_path"},
    "showcase/ui.html": {"current_path"},
    "showcase/video.html": {"current_path"},
}
KIDA_DEF_METADATA_PARITY = {
    "button.html": "btn",
    "card.html": "card",
    "layout.html": "page_header",
    "navbar.html": "navbar",
    "route_tabs.html": "render_route_tabs",
}


@dataclass(frozen=True, slots=True)
class StaticTemplateContract:
    name: str
    ast: Node

    def depends_on(self) -> frozenset[str]:
        return frozenset(DependencyWalker().analyze(self.ast))

    def list_defs(self) -> list[str]:
        return [node.name for node in _walk_nodes(self.ast) if isinstance(node, Def)]

    def list_blocks(self) -> list[str]:
        return [node.name for node in _walk_nodes(self.ast) if isinstance(node, Block)]


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


def _parse_template(path: Path):
    source = path.read_text(encoding="utf-8")
    tokens = list(Lexer(source).tokenize())
    return Parser(tokens, name=path.as_posix(), source=source).parse()


def _walk_nodes(node: Node):
    yield node
    for child in node.iter_child_nodes():
        yield from _walk_nodes(child)


def _imported_names(ast: Node) -> set[str]:
    names: set[str] = set()
    for node in _walk_nodes(ast):
        if isinstance(node, FromImport):
            names.update(alias or name for name, alias in node.names)
        elif isinstance(node, Import):
            names.add(node.alias or "imported_template")
    return names


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


def test_examples_and_theme_templates_pass_privacy_lint() -> None:
    findings: list[tuple[Path, PrivacyFinding]] = []
    for root in PRIVACY_LINT_DIRS:
        for path in sorted(root.rglob("*.html")):
            ast = _parse_template(path)
            findings.extend((path, finding) for finding in lint_privacy(ast))

    unreviewed = [
        f"{finding.code} {path}:{finding.lineno or '?'} {finding.path or ''}".strip()
        for path, finding in findings
        if (finding.code, path.as_posix(), finding.path) not in ALLOWED_PRIVACY_FINDINGS
    ]
    assert unreviewed == []


def test_showcase_page_templates_match_route_context_contracts() -> None:
    missing_context: list[str] = []
    for template_name, provided in SHOWCASE_PAGE_CONTEXTS.items():
        path = SHOWCASE_TEMPLATES_DIR / template_name
        ast = _parse_template(path)
        template = StaticTemplateContract(name=template_name, ast=ast)
        issues = check_context_contract(
            template,
            provided,
            globals=_imported_names(ast) | {"caller"},
        )
        missing_context.extend(
            f"{template_name}: {issue.path}" for issue in issues if issue.code == "K-CTX-001"
        )

    assert missing_context == []


def test_kida_def_metadata_matches_chirp_macro_introspection(env) -> None:
    """Probe Kida's public def metadata before replacing Chirp's parser wrapper."""
    mismatches: list[str] = []
    for template_name, macro_name in KIDA_DEF_METADATA_PARITY.items():
        template = env.get_template(f"chirpui/{template_name}")
        kida_meta = template.def_metadata()[macro_name]
        chirp_meta = macros_in_template(template_name)[macro_name]

        kida_params = [(p.name, p.has_default, p.is_required) for p in kida_meta.params]
        chirp_params = [(p.name, p.has_default, p.is_required) for p in chirp_meta.params]
        if kida_params != chirp_params:
            mismatches.append(f"{template_name}:{macro_name} params")

        kida_slots = set(kida_meta.slots)
        if kida_meta.has_default_slot:
            kida_slots.add("")
        if kida_slots != set(chirp_meta.slots):
            mismatches.append(f"{template_name}:{macro_name} slots")

    assert mismatches == []


def test_escape_audit_script_prints_review_report() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/escape_audit.py"],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "# chirp-ui Kida Escape Audit" in result.stdout
    assert "attrs_unsafe trust boundary" in result.stdout
