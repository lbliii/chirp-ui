---
title: HTMX patterns
description: Fragment islands, forms in boosted layouts, sortable lists
draft: false
weight: 40
lang: en
type: doc
keywords: [chirp-ui, htmx, fragment, island]
icon: arrows-clockwise
---

# HTMX patterns

## Fragment island

Wrap mutation regions with **`fragment_island()`** so inherited `hx-select` / `hx-target` from the app shell does not break local swaps.

- **`id`** (required) — stable root id; must match **`hx-target="#id"`** on mutating requests.
- The island applies **`hx-disinherit="hx-select hx-target hx-swap"`** on children.

Use **`fragment_island_with_result()`** when forms need a co-located result div in the same subtree.

## Forms inside boosted layouts

When `#main` inherits **`hx-select="#page-content"`**:

1. **`hx-select="unset"`** on the form — `hx-disinherit` alone is not enough for the form element.
2. **`hx-swap="innerHTML transition:false"`** — avoids View Transition flash on every submit.

**Complete pattern:**

```html
<form hx-post="/endpoint"
      hx-target="#my-island"
      hx-swap="innerHTML transition:false"
      hx-select="unset"
      hx-disinherit="hx-select">
```

## Sortable lists

Pair **`sortable_list`** / **`sortable_item`** with **`fragment_island`** for drag-and-drop + HTMX — see `chirpui/dnd.html` and repo **[DND-FRAGMENT-ISLAND.md](https://github.com/lbliii/chirp-ui/blob/main/docs/DND-FRAGMENT-ISLAND.md)**.

## Related

- [Pitfalls](./pitfalls.md)
- [Wizard forms](./wizard-forms.md)
