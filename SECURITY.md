# chirp-ui Security

## `| safe` Usage Audit

chirp-ui templates use `| safe` in specific contexts. This document classifies each occurrence and explains the risk model.

### Classification

| Template | Count | Pattern | Classification | Notes |
|----------|-------|---------|----------------|-------|
| `forms.html` | 6 | `{{ attrs \| safe }}` | **Needs guard** | `attrs` is a raw string escape hatch for HTMX/data attributes. Callers must not pass user-controlled content. Prefer `attrs_map` (dict) which goes through `html_attrs` and is escaped. |
| `dnd.html` | 6 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern — `attrs` from `html_attrs` filter. When `attrs` is a dict, `html_attrs` escapes keys/values. When `attrs` is a raw string, it passes through unescaped. |
| `fragment_island.html` | 2 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `sortable_list.html` | 1 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `wizard_form.html` | 1 | `{{ attrs \| safe }}` | **Needs guard** | Same pattern. |
| `layout.html` | 1 | `{{ meta \| safe }}` | **Low** | Meta line (e.g. config path). Typically internal, not user-facing. Callers should not pass untrusted content. |
| `streaming.html` | 1 | `{{ content \| markdown \| safe }}` | **Low** | Markdown output is pre-sanitized by Kida's markdown filter. Content should be from trusted sources. |

### `html_attrs` Filter Behavior

- **Mapping input**: Keys and values are escaped via `html.escape()`. Safe for structured attrs (e.g. `{"hx-post": "/x", "data-id": "123"}`).
- **Raw string input**: Passed through unescaped. Intended for legacy escape hatches (e.g. `attrs='hx-get="/q" hx-target="#r"'`). **Callers must not pass user-controlled or untrusted strings.**

### Recommendations

1. **Prefer `attrs_map`** over `attrs` when passing HTMX or data attributes. `attrs_map` is escaped.
2. **Never pass user input** to `attrs` or `meta` without sanitization.
3. **Streaming content**: Ensure `content` in `streaming.html` comes from trusted sources (e.g. server-generated markdown, not raw user input without sanitization).

### XSS Vector Tests

See `tests/test_filters.py` — `TestHtmlAttrsXss` verifies that:
- Mapping input escapes event handlers, script tags, and encoded payloads.
- Raw string input is documented as pass-through (caller responsibility).
