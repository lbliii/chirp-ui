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

## CSS custom property tokens

Theme colors are defined as CSS custom properties under `:root` with `light-dark()` for automatic light/dark support. The `[data-theme="light"]` and `[data-theme="dark"]` selectors provide explicit overrides.

| Token | Role |
|-------|------|
| `--chirpui-accent` | Primary interactive color (links, buttons, focus rings) |
| `--chirpui-primary` | Brand primary — distinct from accent for decorative use |
| `--chirpui-success` | Positive actions and states |
| `--chirpui-warning` | Caution states |
| `--chirpui-error` | Error / danger states |
| `--chirpui-info` | Informational — aliases `--chirpui-accent` by default |
| `--chirpui-text` | Base text color |
| `--chirpui-text-muted` | Secondary / dimmed text |
| `--chirpui-surface` | Card and panel backgrounds |
| `--chirpui-surface-alt` | Alternate surface (striped rows, sidebar) |
| `--chirpui-border` | Default border color |
| `--chirpui-bg` | Page background |

To override the theme globally, set `data-theme` on `<html>` or set tokens directly under a custom `[data-theme]` selector.

### color-mix() pattern

Derived shades are built with `color-mix()` and generic shade modifiers so themes only need to override base tokens:

```text
--chirpui-accent-hover: color-mix(in srgb, var(--chirpui-accent) var(--chirpui-shade-hover), black);
--chirpui-accent-light: color-mix(in srgb, var(--chirpui-accent) var(--chirpui-shade-light), white);
--chirpui-primary-muted: color-mix(in srgb, var(--chirpui-primary) var(--chirpui-shade-muted), white);
--chirpui-focus-ring:    color-mix(in srgb, var(--chirpui-accent) 30%, transparent);
```

Override `--chirpui-shade-hover`, `--chirpui-shade-muted`, etc. to tune all derived shades at once without touching individual colors.

## Filters

| Filter | Role |
|--------|------|
| `sanitize_color(value)` | Returns the string if it matches a safe CSS color pattern, else `None`. |
| `resolve_color(value)` | Looks up named colors from `register_colors`, then validates as a safe color. |
| `register_colors(mapping)` | Registers semantic names (e.g. domain-specific labels) for `resolve_color`. |
| `contrast_text(css_color)` | Returns `white` or `#1a1a1a` for readable text on solid hex backgrounds. |

## register_colors and concurrency

`register_colors` stores its mapping in a Python **`ContextVar`**, so each async request gets its own copy. This is safe for concurrent use in threaded or async Chirp handlers — one request's colors never leak into another.

### Example: registering colors in a Chirp handler

```python
from chirp_ui.filters import register_colors

@app.before_request
async def set_domain_colors():
    register_colors({
        "fire":    "#ef4444",
        "water":   "#3b82f6",
        "grass":   "#22c55e",
        "electric": "#facc15",
    })
```

Templates can then use the registered names directly:

```text
{{ type_name | resolve_color }}
```

## Usage in templates

```text
{{ "primary" | resolve_color }}
```

For chips and badges that accept custom colors, prefer **`attrs_map`** + resolved colors over raw user strings.

## Related

- [Filters](../reference/filters.md)
- [Security](../guides/security.md)
