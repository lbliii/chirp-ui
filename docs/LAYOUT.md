# Layout Guide

How chirp-ui layouts work: horizontal overflow, vertical fill, and grid vs frame primitives.

---

## Horizontal overflow

The app shell main column (`.chirpui-app-shell__main`) uses **`min-width: 0`** and **`overflow-x: clip`**. If the page scrolls sideways, something inside the content is wider than the column.

Wide content is still supported: put it in a child with **`overflow-x: auto`** (tables, code blocks, dense toolbars). The page column clips; the child scrolls horizontally.

### Layout primitives

| Situation | Use |
|-----------|-----|
| Responsive columns | `grid()` — `.chirpui-grid > *` sets `min-width: 0` automatically. Use `block()` when you need `span=`. Use `preset=` for fixed tracks (see *Grid presets* below). |
| Chips, tags, variable-length rows | `cluster()` — `flex-wrap: wrap` by default. |
| LED-style indicators | `indicator_row()` — wraps by default; `nowrap=true` for single line. |
| Flex row (title + actions) | `page_header`, `section_header`, `entity_header` harden the title column. For ad hoc flex rows, add `chirpui-min-w-0` on the shrinking child. |

### Custom CSS grids

If you use raw `display: grid` (e.g. `repeat(3, 1fr)`):

- Give grid items **`min-width: 0`** (or reuse `chirpui-block` classes).
- Prefer **`minmax(0, 1fr)`** instead of bare `1fr` when content can be wider than the cell.

---

## Vertical fill (full-height main)

How the app shell handles the block axis (height).

### Two modes

| Mode | Scroll owner | Typical use |
|------|-------------|-------------|
| **Default** | Document / page | Long-form content, lists, docs |
| **Fill** | Inner panels below `#main` | Chat, maps, split editors |

Default mode uses browser-native document scrolling. **Fill mode** makes `#main` a bounded flex column so a single child can stretch to the bottom of the shell.

### Opt in to fill mode

1. In layouts extending `app_shell_layout.html`:

   ```kida
   {% block main_shell_class %} chirpui-app-shell__main--fill{% end %}
   ```

   If you build a custom shell with `app_shell()`, wrap routed content with `shell_outlet()` so the same `#page-content` fill contract exists.

2. Wrap your route body in a single root with `chirpui-page-fill`:

   ```html
   <div class="chirpui-page-fill my-page-root">...</div>
   ```

### Chat layout

Use `chat_layout(..., fill=true)` for the `--fill` modifier. If the messages slot has a wrapper, add `chirpui-chat-layout__messages-body` so it receives `flex: 1; min-height: 0`.

### Why `min-height: 0` matters

Flex/grid children default to `min-height: auto`, which prevents shrinking and breaks nested scroll. Any flex child that should scroll internally needs `min-height: 0`.

### HTMX and fill mode sync

`app_shell_layout.html` auto-syncs fill mode on `htmx:afterSettle`: it checks whether `#page-content` contains a direct child with `.chirpui-page-fill` and toggles `chirpui-app-shell__main--fill` on `#main` accordingly.

---

## Flow grids vs frame layouts

chirp-ui separates two layout problems so templates stay predictable.

### Flow grid (`grid()`)

**Use for:** repeating siblings that should wrap — cards, metric tiles, form rows.

**Mechanism:** `repeat(auto-fit, minmax(...))` with `--chirpui-grid-min`. The `cols=2|3|4` parameter scales the minimum track width (it does not force a fixed column count).

### Grid presets

For a known column ratio, use `grid(preset=...)`:

| `preset` | Tracks (wide) | Use |
|----------|---------------|-----|
| `bento-211` | `2fr 1fr 1fr` | One wide + two narrow cards |
| `thirds` | Three equal `1fr` | Three equal columns |
| `detail-two` | `1fr 1.35fr` | Two unequal columns (prose + sidebar) |

`block(span=2)` spans two tracks. `block(span="full")` is `grid-column: 1 / -1`. Use `items="start"` when row cells have unequal heights. Use `detail_single=true` for a single full-width column.

Canonical names, aliases, and breakpoint tokens: [LAYOUT-PRESETS.md](LAYOUT-PRESETS.md).

### Frame (`frame()`)

**Use for:** page regions with a fixed structure — hero, main + sidebar, two equal columns.

**Mechanism:** explicit `grid-template-columns` per variant.

| `variant` | Purpose |
|-----------|---------|
| `balanced` | Two equal columns (`1fr / 1fr`) |
| `hero` | Media + copy; second column slightly wider |
| `sidebar-end` | Fluid main + fixed-width sidebar |

**Tokens:** `--chirpui-frame-gap`, `--chirpui-frame-balanced-columns`, `--chirpui-frame-hero-columns`, `--chirpui-frame-sidebar-width`.

### Anti-patterns

- Do **not** use `grid(cols=2)` for a hero or app shell — use `frame()`.
- Do **not** use `frame()` for an unknown number of wrapping cards — use `grid()`.

### Macro reference

| Macro | CSS base | Role |
|-------|----------|------|
| `grid()` | `chirpui-grid` | Auto-fit flow (+ optional presets) |
| `frame()` | `chirpui-frame` | Explicit structural columns |
| `stack()` | `chirpui-stack` | Vertical flex gap |
| `block()` | `chirpui-block` | Grid cell; `min-width: 0` |

---

## See also

- [LAYOUT-PRESETS.md](LAYOUT-PRESETS.md) — preset names, aliases, breakpoint tokens
- [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md) — common layout footguns and how to avoid them
- [UI-LAYERS.md](UI-LAYERS.md) — app shell vs page chrome vs surface chrome
