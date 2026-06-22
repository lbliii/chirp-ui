"""Static Kida template contracts for the showcase proof loop (#306, #307).

Kida 0.9.x does not implement Jinja-style ``{{ super() }}`` — child blocks fully
replace parent blocks. Shared markup must use ``{% include %}``.

Chirp fragment routes must return templates that define the named block passed to
``Fragment(template, block_name, ...)``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_TEMPLATES = REPO_ROOT / "examples" / "component-showcase" / "templates"
CHIRPUI_TEMPLATES = REPO_ROOT / "src" / "chirp_ui" / "templates"
SHOWCASE_ROUTES = REPO_ROOT / "examples" / "component-showcase" / "routes"
SHOWCASE_APP = REPO_ROOT / "examples" / "component-showcase" / "app.py"

KIDA_COMMENT_RE = re.compile(r"\{#.*?#\}", re.DOTALL)
SUPER_PATTERNS = (
    re.compile(r"\{\{\s*super\s*\(\s*\)\s*\}\}"),
    re.compile(r"\{\{\s*super\s*\}\}"),
    re.compile(r"(?<![\w.])super\s*\(\s*\)"),
    re.compile(r"\{%-?\s*block\b[^%]*\{\{\s*super\b"),
)
FRAGMENT_CALL_RE = re.compile(
    r"""\bFragment\s*\(\s*["']([^"']+)["']\s*,\s*["']([^"']+)["']""",
)


def _html_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.html"))


def _strip_kida_comments(text: str) -> str:
    return KIDA_COMMENT_RE.sub("", text)


def _super_violations(path: Path) -> list[str]:
    source = _strip_kida_comments(path.read_text(encoding="utf-8"))
    hits: list[str] = []
    for pattern in SUPER_PATTERNS:
        for match in pattern.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            hits.append(f"{path.relative_to(REPO_ROOT)}:{line}: {match.group(0)!r}")
    return hits


def _block_names_in_template(path: Path) -> set[str]:
    source = path.read_text(encoding="utf-8")
    return {
        match.group(1)
        for match in re.finditer(r"\{%-?\s*block\s+([A-Za-z_][\w]*)", source)
    }


def _showcase_fragment_calls() -> list[tuple[str, str, Path]]:
    route_files = sorted(SHOWCASE_ROUTES.glob("*.py"))
    sources = [(path, path.read_text(encoding="utf-8")) for path in route_files]
    sources.append((SHOWCASE_APP, SHOWCASE_APP.read_text(encoding="utf-8")))
    calls: list[tuple[str, str, Path]] = []
    for path, source in sources:
        for template, block in FRAGMENT_CALL_RE.findall(source):
            calls.append((template, block, path))
    return calls


def _resolve_showcase_template(template: str) -> Path:
    return SHOWCASE_TEMPLATES / template


@pytest.mark.parametrize(
    "templates_root",
    [SHOWCASE_TEMPLATES, CHIRPUI_TEMPLATES],
    ids=["showcase", "chirpui"],
)
def test_kida_templates_forbid_super(templates_root: Path) -> None:
    """#306 — Kida block inheritance is override-only; super() 500s at render time."""
    violations: list[str] = []
    for path in _html_files(templates_root):
        violations.extend(_super_violations(path))
    assert not violations, (
        "Kida does not implement super()/super — use {% include %} for shared markup:\n"
        + "\n".join(violations)
    )


def test_showcase_fragment_blocks_exist_in_templates() -> None:
    """#307 — every Fragment(template, block) must define {% block block %} in that template."""
    missing: list[str] = []
    for template, block, route_file in _showcase_fragment_calls():
        template_path = _resolve_showcase_template(template)
        if not template_path.is_file():
            missing.append(
                f"{route_file.relative_to(REPO_ROOT)}: Fragment({template!r}, {block!r}) "
                f"→ missing template {template_path.relative_to(REPO_ROOT)}"
            )
            continue
        block_names = _block_names_in_template(template_path)
        if block not in block_names:
            missing.append(
                f"{route_file.relative_to(REPO_ROOT)}: Fragment({template!r}, {block!r}) "
                f"→ {template_path.relative_to(REPO_ROOT)} has blocks "
                f"{sorted(block_names)!r}, not {block!r}"
            )
    assert not missing, "Showcase fragment routes need matching template blocks:\n" + "\n".join(
        missing
    )
