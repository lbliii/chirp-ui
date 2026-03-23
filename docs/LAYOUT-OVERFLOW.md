# Layout overflow (horizontal scroll)

How Chirp UI keeps the app shell from growing sideways, and how to build pages that stay inside the main column.

## Shell contract

For **vertical fill** (full-height routes with inner scroll), see **`docs/LAYOUT-VERTICAL.md`**.

The scrollable region is `#main` / `.chirpui-app-shell__main`. It is a grid child with **`min-width: 0`** so the `1fr` main track can shrink next to the sidebar, and **`overflow-x: clip`** so stray overflow does not create a horizontal scrollbar on the page. Vertical scrolling stays on this element (`overflow-y: auto`).

Wide content is still supported: put it in a **child** with **`overflow-x: auto`** (tables, code blocks, dense toolbars). The page column clips; the child scrolls horizontally.

## Primitives (preferred)

| Situation | Use |
|-----------|-----|
| Responsive columns | `grid()` from `chirpui/layout.html`. **`.chirpui-grid > *`** sets **`min-width: 0`** so arbitrary cell markup does not overflow tracks (same effect as **`chirpui-block`**). Use **`block()`** when you need **`span=`** (bento rows) or an explicit cell wrapper. Use **`preset="bento-211"`** or **`preset="thirds"`** for fixed `fr` tracks (see *Fixed columns* below). Use **`items="start"`** (or **`end`** / **`center`**) when row cells have unequal heights and you want to avoid default **`stretch`** leaving empty space in short cells. For explicit hero/sidebar columns use **`frame()`** — see [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md). |
| Chips, tags, variable-length rows | `cluster()` — **`flex-wrap: wrap`** by default. |
| LED-style indicators in a row | `indicator_row()` — wraps by default; use **`indicator_row(nowrap=true)`** for a deliberate single-line strip. |
| Flex row (title + actions) | **`page_header`**, **`section_header`**, and **`entity_header`** ship CSS so the **title column** can shrink and wrap. For ad hoc flex rows, add **`chirpui-min-w-0`** on the flex child that should absorb overflow. |

## Custom CSS grids

If you use raw `display: grid` (e.g. `repeat(3, 1fr)`):

- Give grid items **`min-width: 0`** (or reuse **`chirpui-block`** classes) so flex/grid descendants can shrink.
- Prefer **`minmax(0, 1fr)`** instead of bare **`1fr`** for tracks when content can be wider than the cell.

## Fixed columns: `grid()` presets + `block(span=…)`

Canonical names, **aliases**, and breakpoint tokens are summarized in **[LAYOUT-PRESETS.md](LAYOUT-PRESETS.md)**.

The default **`chirpui-grid`** uses **auto-fit** columns (`--chirpui-grid-min`). For a **known column ratio** (dashboard / bento), use **`grid()`** from **`chirpui/layout.html`** with a **`preset`**:

| `preset` value | Tracks (wide) | Typical use |
|----------------|---------------|-------------|
| **`bento-211`** | `minmax(0, 2fr) minmax(0, 1fr) minmax(0, 1fr)` | One wide + two narrow cards; breakpoints at 64rem and 48rem. |
| **`thirds`** | Three equal `minmax(0, 1fr)` | Three equal columns; stacks at 48rem. |
| **`detail-two`** | `minmax(0, 1fr) minmax(0, 1.35fr)` | Two unequal columns (e.g. prose + sidebar card); stacks at **52rem**. Optional **`detail_single=true`** on `grid()` for a single full-width column when only one cell is shown. Surfaces/callouts in cells stretch to row height; pair evolution sprite rows with **`cluster(..., cls="chirpui-cluster--detail-two-sprites")`**. |

**`block(span=2)`** spans **two grid tracks** (not “half the page” unless tracks are equal). **`block(span="full")`** is **`grid-column: 1 / -1`** (full row). Example: first row = stats `span=2` + abilities; second row = BST **`span="full"`** so the BST card uses the full width instead of leaving empty cells.

**`chirpui-bento`** / **`bento_grid()`** is a separate component: equal columns **or** inline `style="repeat(n, 1fr)"`, with **default surface chrome** (card border, padding). Use **`grid()` + preset** when you need **asymmetric `fr` tracks** or you are wrapping content in **`surface()`** yourself.

## Related CSS in `chirpui.css`

- App shell grid and **`.chirpui-app-shell__main`** — scrollport and `min-width: 0`.
- **`.chirpui-grid`** (including **`.chirpui-grid > *` { `min-width: 0` }**) / **`.chirpui-grid--preset-bento-211`** / **`.chirpui-grid--preset-thirds`** / **`.chirpui-grid--preset-detail-two`** / **`.chirpui-grid--items-*`** / **`.chirpui-block`** / **`.chirpui-min-w-0`** — layout primitives, shrink-safe cells, fixed-track presets, optional row alignment, and a **`min-width: 0`** utility for custom flex markup.
- **`.chirpui-cluster`** — wrapping horizontal clusters.
- **`.chirpui-ascii-indicator-row`** — wrapping indicator rows; **`--nowrap`** modifier for single line.

See also [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md).
