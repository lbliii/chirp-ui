---
title: Security
description: "| safe", html_attrs, and XSS considerations
draft: false
weight: 44
lang: en
type: doc
keywords: [chirp-ui, security, xss, html_attrs]
icon: shield
---

# Security

## `| safe`

chirp-ui uses `| safe` only where outputs are trusted or pre-escaped. **`attrs`** string escape hatches in several macros pass through raw HTML — **never** pass user-controlled strings.

### Audit table

| Template | Count | Pattern | Classification | Notes |
|----------|-------|---------|----------------|-------|
| `forms.html` | 6 | `{{ attrs \| safe }}` | **Needs guard** | `attrs` is a raw string escape hatch for HTMX/data attributes. Callers must not pass user-controlled content. Prefer `attrs_map` (dict) which goes through `html_attrs` and is escaped. |
| `dnd.html` | 6 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern — `attrs` from `html_attrs` filter. When `attrs` is a dict, `html_attrs` escapes keys/values. When `attrs` is a raw string, it passes through unescaped. |
| `fragment_island.html` | 2 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `sortable_list.html` | 1 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `wizard_form.html` | 1 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `layout.html` | 1 | `{{ meta \| safe }}` | **Low** | Meta line (e.g. config path). Typically internal, not user-facing. Callers should not pass untrusted content. |
| `streaming.html` | 1 | `{{ content \| markdown \| safe }}` | **Low** | Markdown output is pre-sanitized by Kida's markdown filter. Content should be from trusted sources. |

## `html_attrs`

The `html_attrs` filter accepts several input types and handles each differently:

- **`None` / `False`** — returns an empty string (no attributes rendered).
- **Mapping input** (dict) — keys and values are escaped via `html.escape()`. Safe for structured attrs (e.g. `{"hx-post": "/x", "data-id": "123"}`). Prefer **`attrs_map`** / dicts for HTMX attributes.
- **Raw string starting with a space** — passed through as-is (already formatted).
- **Other raw string** — prefixed with a space, then passed through unescaped. Intended for legacy escape hatches (e.g. `attrs='hx-get="/q" hx-target="#r"'`). **Callers must not pass user-controlled or untrusted strings.**

## Recommendations

1. Prefer **`attrs_map`** over raw **`attrs`** strings.
2. Never pass user input to **`attrs`** or **`meta`** without sanitization.
3. Streaming markdown content should be from **trusted** sources.

## Tests

`tests/test_filters.py` includes **`TestHtmlAttrsXss`** which verifies that:

- Mapping input escapes event handlers, script tags, and encoded payloads.
- Raw string input is documented as pass-through (caller responsibility).

## Related

- [Filters](../reference/filters.md)
