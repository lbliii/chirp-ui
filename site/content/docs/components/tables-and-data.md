---
title: Tables and data
description: table, description_list, params_table, tree_view, sortable_list
draft: false
weight: 19
lang: en
type: doc
keywords: [chirp-ui, table, tree]
icon: table
---

# Tables and data

| Template | Role |
|----------|------|
| `table.html` | `table`, `row`, `aligned_row`, `table_empty` |
| `description_list.html` | Key/value lists; variants `stacked` / `horizontal`; use with [type-aware rendering](./type-aware-rendering.md) |
| `params_table.html` | Parameter rows for settings |
| `tree_view.html` | Hierarchical data |
| `sortable_list.html` | Drag reorder + HTMX (see [HTMX patterns](../guides/htmx-patterns.md)) |
| `dnd.html` | Drag-and-drop primitives |

## Dense tables

Wrap wide tables in a child with `overflow-x: auto` — see [Layout overflow](../guides/layout-overflow.md).

## Related

- [Charts](./charts-and-stats.md)
