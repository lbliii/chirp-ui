"""Registry-backed blocks gallery — copy-paste snippets and live previews.

Generates the manifest-driven blocks catalog consumed by the component
showcase and freshness-gated in CI (``scripts/build_blocks_gallery.py``).
"""

from __future__ import annotations

import json
import re
import textwrap
from typing import Any

from kida import Environment

from chirp_ui.manifest import SCHEMA, build_manifest
from chirp_ui.preview_env import make_preview_env

GALLERY_SCHEMA = "chirpui-blocks-gallery@1"

_PREVIEW_KEYS = frozenset({"preview_html", "preview_error"})

_USAGE_RE = re.compile(r"(?:^|\n)\s*Usage:\s*\n", re.MULTILINE)
_TRAILING_SECTION_RE = re.compile(r"^\s*(Notes|See also|Parameters):", re.MULTILINE)
_PSEUDO_FROM_RE = re.compile(r'^from\s+(".+"\s+import\s+.+)$')
_PSEUDO_CALL_RE = re.compile(r"^call\s+(.+)$")
_PSEUDO_END_RE = re.compile(r"^end$")
_PSEUDO_SLOT_RE = re.compile(r"^slot(?:\s+(\w+))?$")
_PSEUDO_MACRO_CALL_RE = re.compile(r"^([a-z_][\w]*)\s*\(")
_VISUAL_PREVIEW_RE = re.compile(r'class="chirpui-(?!stack\b)[\w-]+')


def is_public_component(entry: dict[str, Any]) -> bool:
    """Return whether a manifest entry belongs in the public blocks gallery."""
    return entry.get("maturity") != "internal" and entry.get("authoring") != "internal"


def summary_line(description: str) -> str:
    """Return the first non-empty line of a template doc-block."""
    for raw in description.splitlines():
        line = raw.strip()
        if line:
            return line
    return ""


def extract_usage_snippet(description: str) -> str:
    """Extract the Usage example from a template doc-block, if present."""
    if not description:
        return ""
    match = _USAGE_RE.search(description)
    if not match:
        return ""
    snippet = description[match.end() :]
    trailing = _TRAILING_SECTION_RE.search(snippet)
    if trailing:
        snippet = snippet[: trailing.start()]
    lines = [line.rstrip() for line in snippet.splitlines()]
    return textwrap.dedent("\n".join(lines)).strip()


def _classify_pseudo_line(stripped: str) -> tuple[str, str | None]:
    """Classify one Usage line for pseudo-syntax normalization."""
    if not stripped:
        return "blank", None
    if stripped.startswith(("{%", "{{", "{#")):
        return "kida", stripped
    from_match = _PSEUDO_FROM_RE.match(stripped)
    if from_match:
        return "from", "{% from " + from_match.group(1) + " %}"
    call_match = _PSEUDO_CALL_RE.match(stripped)
    if call_match:
        return "call", call_match.group(1)
    if _PSEUDO_END_RE.match(stripped):
        return "end", None
    slot_match = _PSEUDO_SLOT_RE.match(stripped)
    if slot_match:
        slot_name = slot_match.group(1)
        if slot_name:
            return "slot", "{% slot " + slot_name + " %}"
        return "slot", "{% slot %}"
    if _PSEUDO_MACRO_CALL_RE.match(stripped):
        return "macro", "{{ " + stripped + " }}"
    return "text", stripped


def normalize_usage_snippet(snippet: str) -> str:
    """Convert template doc-block pseudo-syntax into valid Kida."""
    parsed: list[tuple[int, str, str | None, str]] = []
    for line in snippet.splitlines():
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        kind, payload = _classify_pseudo_line(stripped)
        parsed.append((indent, kind, payload, stripped))

    leaf_calls: set[int] = set()
    for index, (indent, kind, _payload, _stripped) in enumerate(parsed):
        if kind != "call":
            continue
        next_index = index + 1
        while next_index < len(parsed) and parsed[next_index][1] == "blank":
            next_index += 1
        if next_index >= len(parsed) or parsed[next_index][0] <= indent:
            leaf_calls.add(index)

    output: list[str] = []
    for index, (indent, kind, payload, _stripped) in enumerate(parsed):
        pad = " " * indent
        if kind == "blank":
            output.append("")
        elif kind == "from":
            assert payload is not None
            output.append(pad + payload)
        elif kind == "call":
            assert payload is not None
            if index in leaf_calls:
                output.append(pad + "{% call " + payload + " %}{% end %}")
            else:
                output.append(pad + "{% call " + payload + " %}")
        elif kind == "end":
            output.append(pad + "{% end %}")
        elif kind in {"slot", "kida", "macro", "text"}:
            assert payload is not None
            output.append(pad + payload)
    return "\n".join(output).strip()


def is_visual_preview(html: str | None) -> bool:
    """Return whether rendered preview HTML contains a chirp-ui component."""
    return bool(html and _VISUAL_PREVIEW_RE.search(html))


def fallback_copy_snippet(name: str, entry: dict[str, Any]) -> str:
    """Synthesize a minimal import + call when the doc-block has no Usage section."""
    macro = entry.get("macro") or name.replace("-", "_")
    template = entry.get("template") or f"{macro}.html"
    slots = entry.get("slots") or []
    import_line = f'{{% from "chirpui/{template}" import {macro} %}}'
    if "" in slots:
        return f"{import_line}\n\n{{% call {macro}() %}}\n  Content\n{{% end %}}"
    if slots:
        slot_name = slots[0]
        slot_arg = f'"{slot_name}"' if slot_name else '""'
        return f"{import_line}\n\n{{% call {macro}({slot_arg}) %}}\n  Content\n{{% end %}}"
    return f"{import_line}\n\n{{{{ {macro}() }}}}"


def copy_snippet_for(name: str, entry: dict[str, Any]) -> str:
    """Return the copy-paste Kida snippet for one manifest component."""
    usage = extract_usage_snippet(entry.get("description") or "")
    if usage:
        return normalize_usage_snippet(usage)
    return fallback_copy_snippet(name, entry)


def render_preview_html(env: Environment, snippet: str) -> tuple[str | None, str | None]:
    """Try to render a usage snippet; return ``(html, error)``."""
    wrapped = (
        '{% from "chirpui/layout.html" import stack %}\n'
        "{% call stack() %}\n"
        f"{snippet}\n"
        "{% end %}"
    )
    try:
        template = env.from_string(wrapped, name="blocks-gallery-preview")
        rendered = template.render().strip()
        return (rendered or None), None
    except Exception as exc:
        return None, str(exc)


def preview_snippet_for(
    name: str,
    entry: dict[str, Any],
    env: Environment,
    snippet: str,
) -> tuple[str | None, str | None]:
    """Render a snippet, falling back to a synthesized import/call when needed."""
    preview_html, preview_error = render_preview_html(env, snippet)
    if is_visual_preview(preview_html):
        return preview_html, None

    fallback = fallback_copy_snippet(name, entry)
    if fallback == snippet:
        return preview_html, preview_error

    fallback_html, fallback_error = render_preview_html(env, fallback)
    if is_visual_preview(fallback_html):
        return fallback_html, None
    if preview_html:
        return preview_html, preview_error
    return fallback_html, fallback_error or preview_error


def build_block_entry(
    name: str,
    entry: dict[str, Any],
    *,
    env: Environment | None = None,
) -> dict[str, Any]:
    """Build one gallery record for a manifest component."""
    snippet = copy_snippet_for(name, entry)
    preview_html: str | None = None
    preview_error: str | None = None
    if env is not None:
        preview_html, preview_error = preview_snippet_for(name, entry, env, snippet)
    return {
        "name": name,
        "category": entry.get("category") or "",
        "maturity": entry.get("maturity") or "",
        "authoring": entry.get("authoring") or "",
        "role": entry.get("role") or "",
        "block": entry.get("block") or name,
        "macro": entry.get("macro") or "",
        "template": entry.get("template") or "",
        "summary": summary_line(entry.get("description") or ""),
        "copy_snippet": snippet,
        "preview_html": preview_html,
        "preview_error": preview_error,
    }


def build_gallery(*, with_previews: bool = True) -> dict[str, Any]:
    """Build the full blocks gallery payload from the live registry projection."""
    manifest = build_manifest()
    env = make_preview_env() if with_previews else None
    blocks = [
        build_block_entry(name, entry, env=env)
        for name, entry in sorted(manifest.get("components", {}).items())
        if is_public_component(entry)
    ]
    categories = sorted({block["category"] for block in blocks if block["category"]})
    preview_ok = sum(1 for block in blocks if is_visual_preview(block.get("preview_html")))
    return {
        "schema": GALLERY_SCHEMA,
        "manifest_schema": manifest.get("schema", SCHEMA),
        "version": manifest.get("version", ""),
        "generated_from": "src/chirp_ui/manifest.json",
        "stats": {
            "blocks": len(blocks),
            "categories": len(categories),
            "previews_rendered": preview_ok,
        },
        "categories": categories,
        "blocks": blocks,
    }


def gallery_check_payload(gallery: dict[str, Any]) -> dict[str, Any]:
    """Return a platform-stable gallery payload for CI freshness checks.

    Live preview HTML/error strings can differ across OS/Python builds; the
    gate compares manifest-derived metadata and copy snippets only.
    """
    payload = json.loads(json.dumps(gallery))
    stats = dict(payload.get("stats") or {})
    stats.pop("previews_rendered", None)
    payload["stats"] = stats
    payload["blocks"] = [
        {key: value for key, value in block.items() if key not in _PREVIEW_KEYS}
        for block in payload.get("blocks") or []
    ]
    return payload


def to_json_gallery(gallery: dict[str, Any], *, indent: int = 2) -> str:
    """Serialize a gallery payload to canonical JSON."""
    text = json.dumps(gallery, indent=indent, ensure_ascii=True)
    if not text.endswith("\n"):
        text += "\n"
    return text


def to_json_gallery_check(gallery: dict[str, Any], *, indent: int = 2) -> str:
    """Serialize the freshness-gate view of a gallery payload."""
    return to_json_gallery(gallery_check_payload(gallery), indent=indent)
