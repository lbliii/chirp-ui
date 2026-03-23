---
title: Color system
description: Palettes, resolve_color, register_colors, and contrast_text
draft: false
weight: 33
lang: en
type: doc
keywords: [chirp-ui, color, css]
icon: palette
---

# Color system

## Filters

| Filter | Role |
|--------|------|
| `sanitize_color(value)` | Returns the string if it matches a safe CSS color pattern, else `None`. |
| `resolve_color(value)` | Looks up named colors from `register_colors`, then validates as a safe color. |
| `register_colors(mapping)` | Registers semantic names (e.g. domain-specific labels) for `resolve_color`. |
| `contrast_text(css_color)` | Returns `white` or `#1a1a1a` for readable text on solid hex backgrounds. |

Named colors use a **contextvar** map — safe for concurrent requests when used per-request.

## Usage in templates

```text
{{ "primary" | resolve_color }}
```

For chips and badges that accept custom colors, prefer **`attrs_map`** + resolved colors over raw user strings.

## CSS

Theme colors live under `:root` and `data-theme` overrides in `chirpui.css`. Use **`color-mix()`** and semantic surface tokens where possible.

## Related

- [Filters](../reference/filters.md)
- [Security](../guides/security.md)
