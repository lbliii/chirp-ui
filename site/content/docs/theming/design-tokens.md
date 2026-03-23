---
title: Design tokens
description: Spacing, semantic aliases, elevation, and token precedence
draft: false
weight: 31
lang: en
type: doc
keywords: [chirp-ui, tokens, css]
icon: sliders
---

# Design tokens

`chirpui.css` defines **`--chirpui-*` variables** in three conceptual tiers:

1. **Core primitives** — spacing, radius, typography, color foundations, motion, shadows.
2. **Semantic tokens** — interaction/state and theme-aware aliases.
3. **Component aliases** — optional defaults mapping to semantic/core tokens.

## Spacing scale

Core steps include `--chirpui-spacing-xs` through `--chirpui-spacing-3xl`. Prefer **semantic aliases** for intent:

| Token | Typical role |
|-------|----------------|
| `--chirpui-space-inline-gap` | Tight inline adjacency |
| `--chirpui-space-control-gap` | Button/control groups |
| `--chirpui-space-stack-gap` | Default vertical rhythm |
| `--chirpui-space-section-gap` | Section header/body |
| `--chirpui-space-page-gap` | Page-level stacks |
| `--chirpui-space-card-padding` | Card inset |

## Precedence

1. `:root` defaults  
2. `[data-theme="light"|"dark"|"system"]`  
3. `[data-style="default"|"neumorphic"]`  
4. Capability overrides in `@supports` (e.g. `oklch`, `color-mix`)

## Page header tokens

Override `--chirpui-page-header-*` to tune `page_header` without touching BEM classes — see the full table in [TOKENS.md](https://github.com/lbliii/chirp-ui/blob/main/docs/TOKENS.md).

## Related

- [Typography](./typography.md)
- [Creating themes](./creating-themes.md)
