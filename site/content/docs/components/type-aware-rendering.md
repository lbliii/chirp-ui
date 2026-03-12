---
title: Type-aware value rendering
description: Auto-detect Python types and apply CSS variants in description lists
draft: false
weight: 25
lang: en
type: doc
keywords: [chirp-ui, description_list, value_type, Path, bool, type-aware]
category: components
---

# Type-aware value rendering

ChirpUI's `description_item` macro automatically detects Python types and applies the right CSS variant. Pass raw values from your handlers—no string conversion needed.

## How it works

When you call `description_item(term, detail)` without `type=`, the macro applies the `value_type` filter to infer the type:

| Python type | CSS variant | Rendering |
|-------------|-------------|-----------|
| `bool` | `--bool` | Yes/No badge (success/muted) |
| `int`, `float` | `--number` | Right-aligned, monospace-friendly |
| `Path`, `PurePath` | `--path` | Mono font, ellipsis, nowrap |
| `None` | `--unset` | Muted, italic |
| `str` | `""` | No extra class (plain text) |

Explicit `type=` overrides auto-detection. Use it when you need a specific variant (e.g. `type="url"`) even when the value is a string.

## Usage

### Pass raw types from handlers

```python
# In your page handler:
return {
    "workspace_root": workspace_root,  # Path, not str(workspace_root)
    "project_initialized": project_initialized,  # bool, not "Yes"/"No"
}
```

### In templates

```kida
{% from "chirpui/description_list.html" import description_item %}

{{ description_item("Workspace path", workspace_root) }}
{{ description_item("Project initialized", project_initialized) }}
```

No `type=` needed. The macro detects `Path` and `bool` and applies the right class and rendering.

### With items list

```kida
{% set items = [
    {"term": "Workspace", "detail": workspace_root},
    {"term": "Ready", "detail": True},
] %}
{{ description_list(items=items) }}
```

Type is auto-detected from each item's `detail` when `type` is omitted.

### Override when needed

```kida
{{ description_item("Config URL", config_url, type="url") }}
```

Use `type=` when the value is a string but you want a specific variant (e.g. URL styling).

## Supported types

| Type | value_type returns | Notes |
|------|--------------------|-------|
| `None` | `"unset"` | Muted, italic |
| `bool` | `"bool"` | Renders Yes/No badge |
| `int`, `float` | `"number"` | Right-aligned |
| `Path`, `PurePath` | `"path"` | Mono font, ellipsis |
| `str` | `""` | No variant |
| `type="url"` | Explicit | Same styling as path |

## Kida `typeof` filter

For generic type names (e.g. debugging), you can use Kida's `typeof` filter:

```kida
{{ value | typeof }}
```

Returns `"bool"`, `"int"`, `"float"`, `"path"`, `"list"`, `"dict"`, `"none"`, or `"str"` (with `bool` checked before `int`).

## Best practices

1. **Pass raw types** — Avoid `str()` in handlers for Path and bool. Let templates handle display.
2. **Use `description_item`** — For key-value pairs, prefer the macro over hand-written markup so type-aware styling applies.
3. **Override when needed** — Use `type="url"` for URLs that arrive as strings.
