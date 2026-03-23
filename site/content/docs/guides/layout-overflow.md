---
title: Layout overflow
description: Keep the app shell from growing sideways
draft: false
weight: 36
lang: en
type: doc
keywords: [chirp-ui, layout, overflow, scroll]
icon: arrows-out
---

# Layout overflow

How chirp-ui keeps the app shell from growing sideways, and how to build pages that stay inside the main column.

## Shell contract

The scrollable region is `#main` / `.chirpui-app-shell__main`. It is a grid child with **`min-width: 0`** so the `1fr` main track can shrink next to the sidebar, and **`overflow-x: clip`** so stray overflow does not create a horizontal scrollbar on the page. Vertical scrolling stays on this element (`overflow-y: auto`).

Wide content is still supported: put it in a **child** with **`overflow-x: auto`** (tables, code blocks, dense toolbars).

## Primitives

| Situation | Use |
|-----------|-----|
| Responsive columns | `grid()` from `chirpui/layout.html`. Direct grid children get **`min-width: 0`**. Use **`block()`** when you need **`span=`** or bento rows. |
| Chips / variable rows | `cluster()` — wraps by default. |
| LED-style indicators | `indicator_row()` — wraps; use **`nowrap=true`** for a single-line strip. |
| Title + actions | **`page_header`**, **`section_header`**, **`entity_header`** include CSS so the title column shrinks. For ad hoc rows, add **`chirpui-min-w-0`**. |

## Custom grids

If you use raw `display: grid`:

- Give items **`min-width: 0`** (or **`chirpui-block`**).
- Prefer **`minmax(0, 1fr)`** for tracks when content can exceed the cell.

## Fixed columns: presets + `block(span=…)`

Use **`grid(..., preset="bento-211")`**, **`thirds`**, or **`detail-two`** for known column ratios. **`block(span=2)`** spans two tracks; **`span="full"`** is full width.

See [Layout presets](./layout-presets.md) and [Grids and frames](./grids-and-frames.md).

## Related

- [Vertical layout](./vertical-layout.md)
- [Pitfalls](./pitfalls.md)
