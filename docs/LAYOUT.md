# Layout Guide

How chirp-ui layouts work: horizontal overflow, vertical fill, and grid vs frame primitives. For the broader authoring vocabulary, see [PRIMITIVES.md](PRIMITIVES.md).

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

## Content containment (inside cards, surfaces, bentos)

Layout primitives solve the *cell* — the cell is the right width. Containment solves the *content inside the cell* — long URLs, wide tables, hardcoded-width inputs, API keys, filenames that punch past the cell edge.

### What's handled automatically

- **`.chirpui-card`** and **`.chirpui-panel`** use `overflow: clip`. Content cannot visually escape.
- **`.chirpui-surface`** and **`.chirpui-callout`** apply `min-width: 0` and `overflow-wrap: break-word` — long words break instead of widening the surface.
- **`.chirpui-field__input`** (all inputs/textareas/selects rendered by `field_wrapper`) uses `width: 100%; max-width: 100%; min-width: 0` — form controls cannot overflow their parent.
- **Links inside cards and surfaces** use `overflow-wrap: anywhere` — long URLs break mid-string.
- **Code blocks** (`.chirpui-code-block`, prose `<pre>`) scroll horizontally via `overflow-x: auto` and use `overscroll-behavior: contain` so scroll doesn't chain to the page.
- **Media elements** (`<img>`, `<video>`, `<canvas>`, `<iframe>`, `<embed>`, `<object>`, `<svg>`) have a zero-specificity `:where()` reset — `max-width: 100%` and `height: auto` where applicable — so raw media dropped anywhere can't widen its parent.
- **`<pre>` and `<table>` inside `.chirpui-card__body` / `.chirpui-surface` / `.chirpui-callout`** automatically scroll horizontally (`display: block` + `overflow-x: auto` on tables). No manual wrapping needed for the common case.
- **`prefers-reduced-motion: reduce`** is honored globally — animations/transitions collapse to 0.01ms across the whole CSS. Per-component `@media` blocks still override for bespoke handling.
- **Native form controls** (checkboxes, radios, range, progress) pick up `accent-color: var(--chirpui-accent)` at `:root`.

### Legacy containment helpers

These helpers remain available for narrow compatibility cases. They are not the preferred growth path for new layout vocabulary.

| Helper | Use for |
|---------|---------|
| **`.chirpui-scroll-x`** | Wide tables, dense toolbars, horizontal strips that should scroll locally instead of widening the page. Wrap `<table>` in `<div class="chirpui-scroll-x">`. |
| **`.chirpui-truncate`** | Single-line labels that must hard-stop with an ellipsis (file names in a tight bento cell). Requires a bounded parent. |
| **`.chirpui-clamp-2`** / **`.chirpui-clamp-3`** | Multi-line descriptions that must cap at 2 or 3 lines with an ellipsis. |
| **`.chirpui-min-w-0`** | Ad-hoc flex children that need to shrink below content width. |

### Rules of thumb

- **Prefer break-word over clip.** Clipping hides content; wrapping keeps it readable. Only use `overflow: clip` on outer frames (card, panel) where inner scroll/popover content doesn't need to escape.
- **Surfaces don't clip.** A surface inside a bento cell is allowed to host popovers, tooltips, and overflow menus that visually escape. Containment happens via `min-width: 0` + `overflow-wrap`, not by clipping.
- **Raw `<input>` tags outside `field_wrapper`** need `max-width: 100%; min-width: 0` added by hand, or they can overflow narrow cells.
- **Wide prose tables** (outside the code-block treatment) need explicit wrapping: `<div class="chirpui-scroll-x"><table>…</table></div>`.

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
| `sidebar-start` | Fixed-width left rail + fluid main content |
| `sidebar-end` | Fluid main content + fixed-width right sidebar |

**Tokens:** `--chirpui-frame-gap`, `--chirpui-frame-balanced-columns`, `--chirpui-frame-hero-columns`, `--chirpui-frame-sidebar-width`.

`sidebar-start` and `sidebar-end` both use `--chirpui-frame-sidebar-width`.
Use `sidebar-start` for workspace shells where navigation appears before the
content and the content should expand into the remaining row. Use `sidebar-end`
for detail pages where secondary context sits after the main content.

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

- [PRIMITIVES.md](PRIMITIVES.md) — blessed primitives and legacy helper boundary
- [LAYOUT-PRESETS.md](LAYOUT-PRESETS.md) — preset names, aliases, breakpoint tokens
- [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md) — common layout footguns and how to avoid them
- [UI-LAYERS.md](UI-LAYERS.md) — app shell vs page chrome vs surface chrome
