---
title: Layout presets
description: grid() presets, aliases, and breakpoints
draft: false
weight: 37
lang: en
type: doc
keywords: [chirp-ui, grid, preset]
icon: grid-four
---

# Layout presets

`grid()` defaults to **auto-fit** columns. A **`preset`** switches to **fixed** `grid-template-columns` for dashboards and detail rows.

## Breakpoints

| Token | Value | Used in |
|-------|--------|---------|
| `--chirpui-layout-bp-sm` | `48rem` | `thirds`, `bento-211` stack; `frame()` stack |
| `--chirpui-layout-bp-md` | `52rem` | `detail-two` stack |
| `--chirpui-layout-bp-lg` | `64rem` | `bento-211` first narrowing |

Media queries use literal `rem` values (not custom properties inside `@media`).

## Preset table

| Canonical `preset` | Aliases | Tracks (wide) | Collapses |
|--------------------|---------|---------------|-----------|
| `bento-211` | `split-2-1-1` | `2fr` + `1fr` + `1fr` | → 2 cols at lg; → 1 at sm |
| `thirds` | `split-thirds`, `three-equal` | three `1fr` | → 1 col at sm |
| `detail-two` | `split-1-1.35` | `1fr` + `1.35fr` | → 1 col at md |
| `detail-two-single` | `split-1-1.35-single` | one `1fr` | already single |

## `block()` spans

- **`span=2`** — two tracks.
- **`span="full"`** — `grid-column: 1 / -1`.

## Related

- [Layout overflow](./layout-overflow.md)
- [Components: Layout](../components/layout.md)
