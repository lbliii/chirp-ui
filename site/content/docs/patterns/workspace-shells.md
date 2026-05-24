---
title: Workspace Shell Recipes
description: Dense app workspace recipes for search, operations, support, and admin surfaces.
type: doc
---

# Workspace Shell Recipes

Use `workspace_shell` for dense multi-region app surfaces, then fill it with
registry-cited primitives instead of page-owned shell grids.

| Need | Primitive |
|---|---|
| Command/search surface | `command_bar` |
| Filters | `filter_bar` |
| Sidebar rail | `filter_rail`, `filter_rail_item` |
| Results | `result_collection`, `result_card` |
| Readouts | `metric_strip`, `metric_item` |
| Selected object | `inspector_panel` |

## Agent Checklist

- Start with `workspace_shell` for multi-region app workspaces.
- Use `filter_rail` for sidebar navigation or filters.
- Use `result_collection` and `result_card` for dense search results.
- Use `metric_strip` for operational readouts.
- Use `inspector_panel` for selected-object details.
- Keep app-local classes for domain copy and data styling only.

The durable authoring source is
[`docs/patterns/workspace-shell-recipes.md`](https://github.com/llane/chirp-ui/blob/main/docs/patterns/workspace-shell-recipes.md).
