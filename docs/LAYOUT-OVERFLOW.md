# Layout overflow (horizontal scroll)

How Chirp UI keeps the app shell from growing sideways, and how to build pages that stay inside the main column.

## Shell contract

The scrollable region is `#main` / `.chirpui-app-shell__main`. It is a grid child with **`min-width: 0`** so the `1fr` main track can shrink next to the sidebar, and **`overflow-x: clip`** so stray overflow does not create a horizontal scrollbar on the page. Vertical scrolling stays on this element (`overflow-y: auto`).

Wide content is still supported: put it in a **child** with **`overflow-x: auto`** (tables, code blocks, dense toolbars). The page column clips; the child scrolls horizontally.

## Primitives (preferred)

| Situation | Use |
|-----------|-----|
| Responsive columns | `grid()` + `block()` from `chirpui/layout.html` — `chirpui-block` sets **`min-width: 0`** on grid children. |
| Chips, tags, variable-length rows | `cluster()` — **`flex-wrap: wrap`** by default. |
| LED-style indicators in a row | `indicator_row()` — wraps by default; use **`indicator_row(nowrap=true)`** for a deliberate single-line strip. |

## Custom CSS grids

If you use raw `display: grid` (e.g. `repeat(3, 1fr)`):

- Give grid items **`min-width: 0`** (or reuse **`chirpui-block`** classes) so flex/grid descendants can shrink.
- Prefer **`minmax(0, 1fr)`** instead of bare **`1fr`** for tracks when content can be wider than the cell.

## Related CSS in `chirpui.css`

- App shell grid and **`.chirpui-app-shell__main`** — scrollport and `min-width: 0`.
- **`.chirpui-grid`** / **`.chirpui-block`** — layout primitives.
- **`.chirpui-cluster`** — wrapping horizontal clusters.
- **`.chirpui-ascii-indicator-row`** — wrapping indicator rows; **`--nowrap`** modifier for single line.

See also [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md).
