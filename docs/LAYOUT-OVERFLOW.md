# Layout overflow (horizontal scroll)

How Chirp UI keeps the app shell from growing sideways, and how to build pages that stay inside the main column.

## Shell contract

For **vertical fill** (full-height routes with inner scroll), see **`docs/LAYOUT-VERTICAL.md`**.

The scrollable region is `#main` / `.chirpui-app-shell__main`. It is a grid child with **`min-width: 0`** so the `1fr` main track can shrink next to the sidebar, and **`overflow-x: clip`** so stray overflow does not create a horizontal scrollbar on the page. Vertical scrolling stays on this element (`overflow-y: auto`).

Wide content is still supported: put it in a **child** with **`overflow-x: auto`** (tables, code blocks, dense toolbars). The page column clips; the child scrolls horizontally.

## Primitives (preferred)

| Situation | Use |
|-----------|-----|
| Responsive columns | `grid()` + `block()` from `chirpui/layout.html` — `chirpui-block` sets **`min-width: 0`** on grid children. For explicit hero/sidebar columns use **`frame()`** — see [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md). |
| Chips, tags, variable-length rows | `cluster()` — **`flex-wrap: wrap`** by default. |
| LED-style indicators in a row | `indicator_row()` — wraps by default; use **`indicator_row(nowrap=true)`** for a deliberate single-line strip. |

## Custom CSS grids

If you use raw `display: grid` (e.g. `repeat(3, 1fr)`):

- Give grid items **`min-width: 0`** (or reuse **`chirpui-block`** classes) so flex/grid descendants can shrink.
- Prefer **`minmax(0, 1fr)`** instead of bare **`1fr`** for tracks when content can be wider than the cell.

## Fixed columns: `grid()` presets + `block(span=…)`

The default **`chirpui-grid`** uses **auto-fit** columns (`--chirpui-grid-min`). For a **known column ratio** (dashboard / bento), use **`grid()`** from **`chirpui/layout.html`** with a **`preset`**:

| `preset` value | Tracks (wide) | Typical use |
|----------------|---------------|-------------|
| **`bento-211`** | `minmax(0, 2fr) minmax(0, 1fr) minmax(0, 1fr)` | One wide + two narrow cards; breakpoints at 64rem and 48rem. |
| **`thirds`** | Three equal `minmax(0, 1fr)` | Three equal columns; stacks at 48rem. |

**`block(span=2)`** spans **two grid tracks** (not “half the page” unless tracks are equal). **`block(span="full")`** is **`grid-column: 1 / -1`** (full row). Example: first row = stats `span=2` + abilities; second row = BST **`span="full"`** so the BST card uses the full width instead of leaving empty cells.

**`chirpui-bento`** / **`bento_grid()`** is a separate component: equal columns **or** inline `style="repeat(n, 1fr)"`, with **default card chrome** (border, padding). Use **`grid()` + preset** when you need **asymmetric `fr` tracks** or you are wrapping content in **`surface()`** yourself.

## Related CSS in `chirpui.css`

- App shell grid and **`.chirpui-app-shell__main`** — scrollport and `min-width: 0`.
- **`.chirpui-grid`** / **`.chirpui-grid--preset-bento-211`** / **`.chirpui-grid--preset-thirds`** / **`.chirpui-block`** — layout primitives and fixed-track presets.
- **`.chirpui-cluster`** — wrapping horizontal clusters.
- **`.chirpui-ascii-indicator-row`** — wrapping indicator rows; **`--nowrap`** modifier for single line.

See also [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md).
