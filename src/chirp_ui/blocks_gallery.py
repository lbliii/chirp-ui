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
        return usage
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
        preview_html, preview_error = render_preview_html(env, snippet)
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
    preview_ok = sum(1 for block in blocks if block.get("preview_html"))
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
