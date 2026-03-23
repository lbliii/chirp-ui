---
title: Grids and frames
description: When to use grid() vs frame() vs flow
draft: false
weight: 38
lang: en
type: doc
keywords: [chirp-ui, grid, frame]
icon: frame-corners
---

# Grids and frames

chirp-ui separates **flow grids** from **frame layouts** so templates stay predictable.

## Flow grid (`grid()`)

**Use for:** repeating siblings that wrap — cards, metrics, form rows, filter chips.

**Mechanism:** `repeat(auto-fit, minmax(…))` with `--chirpui-grid-min`. The `cols=` parameter tunes minimum track width, not a fixed column count on all viewports.

**Presets:** `bento-211`, `thirds`, `detail-two` select fixed tracks for dashboard cells. Use **`items="start"`** when row cells have unequal heights.

## Frame (`frame()`)

**Use for:** fixed regions — hero (media + copy), main + sidebar, two equal columns.

**Variants:**

| `variant` | Purpose |
|-----------|---------|
| `balanced` | Two equal columns |
| `hero` | Media + copy |
| `sidebar-end` | Fluid main + fixed sidebar |

**Tokens:** `--chirpui-frame-gap`, `--chirpui-frame-balanced-columns`, `--chirpui-frame-hero-columns`, `--chirpui-frame-sidebar-width`.

## Overflow

`.chirpui-frame > *` sets **`min-width: 0`**. For flow grids, use **`block()`** when needed. See [Layout overflow](./layout-overflow.md).

## Anti-patterns

- Do **not** use `grid(cols=2)` for a hero — use **`frame()`** or app CSS.
- Do **not** use `frame()` for an unknown number of wrapping cards — use **`grid()`**.

## Related

- [Layout presets](./layout-presets.md)
