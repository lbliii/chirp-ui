---
title: Filters
description: Template filters and color registration API
draft: false
weight: 46
lang: en
type: doc
keywords: [chirp-ui, filters, bem, html_attrs]
icon: funnel
---

# Filters

Register with **`chirp_ui.register_filters(app)`** (or **`use_chirp_ui(app)`**). The following are registered as **template filters**:

| Filter | Signature | Role |
|--------|-----------|------|
| `bem` | `(block, variant="", modifier="", cls="")` | Build `chirpui-{block}` BEM classes. |
| `field_errors` | `(errors, field_name)` | List of error strings for one field. |
| `html_attrs` | `(value)` | Mapping → escaped attrs; raw string → pass-through `Markup`. |
| `icon` | `(name)` | Resolve icon name to glyph (see icon registry). |
| `validate_variant` | `(value, allowed, default="")` | Validate against an explicit tuple. |
| `validate_variant_block` | `(value, block, default="")` | Validate using `VARIANT_REGISTRY[block]`. |
| `validate_size` | `(value, block, default="")` | Validate using `SIZE_REGISTRY[block]`. |
| `value_type` | `(value)` | Python value → CSS type name for `description_item`. |
| `sanitize_color` | `(value)` | Safe CSS color string or `None`. |
| `contrast_text` | `(css_color)` | `white` or `#1a1a1a` for text on hex background. |
| `resolve_color` | `(value)` | Named colors + safe CSS validation. |

## Python API (not a template filter)

- **`register_colors(mapping)`** — register semantic names for **`resolve_color`**. Call from application startup or per-request setup.

## Template global

- **`tab_is_active(tab, current_path)`** — registered via **`template_global`** when available. See [Route tabs](./route-tabs.md).

## `html_attrs` edge cases

- **`None` / `False`** → empty.
- **Mapping** → keys and values escaped.
- **Raw string** starting with space → returned as-is (leading space convention).
- **Otherwise** → prefixed with a single leading space for concatenation.

## Related

- [Validation](./validation.md)
- [Security](../guides/security.md)
