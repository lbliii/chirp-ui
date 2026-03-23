---
title: Layout
description: container, grid, frame, stack, cluster, block, section headers
draft: false
weight: 11
lang: en
type: doc
keywords: [chirp-ui, layout, grid, frame, stack]
icon: grid-four
---

# Layout

Import from `chirpui/layout.html`.

## Overview

| Macro | Role |
|-------|------|
| `container()` | Max-width page wrapper with horizontal padding |
| `grid()` | Responsive flow grid; optional **presets** (`bento-211`, `thirds`, `detail-two`) |
| `frame()` | Fixed column structures (hero, balanced, sidebar-end) |
| `stack()` | Vertical flex column with gap |
| `cluster()` | Horizontal flex row that wraps |
| `block()` | Grid cell with `min-width: 0`; supports `span=` |
| `page_header()`, `section_header()` | Title rows with actions |
| `section()`, `section_collapsible()` | Grouped content regions |

## Basic usage

```text
{% from "chirpui/layout.html" import container, grid, block %}
{% call container() %}
  {% call grid(cols=2) %}
    {% call block() %}…{% end %}
    {% call block() %}…{% end %}
  {% end %}
{% end %}
```

## Grid presets

Use `preset="bento-211"` or `preset="thirds"` for fixed dashboard tracks. See [Layout presets](../guides/layout-presets.md) and [Grids and frames](../guides/grids-and-frames.md).

## CSS classes

- `chirpui-grid`, `chirpui-grid--preset-*`
- `chirpui-frame`, `chirpui-frame--*`
- `chirpui-stack`, `chirpui-cluster`, `chirpui-block`
- `chirpui-page-header`, `chirpui-section-header`

## Related

- [Layout overflow](../guides/layout-overflow.md)
- [Vertical layout](../guides/vertical-layout.md)
- [Charts and stats](./charts-and-stats.md) — `bento_grid()` vs `grid()` presets
