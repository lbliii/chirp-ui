> **Consolidated:** This content has been merged into [LAYOUT.md](LAYOUT.md). This file is kept for existing links.

# Flow grids vs frame layouts

chirp-ui separates **two layout problems** so templates stay predictable.

For **`grid()`** fixed-track **presets**, **aliases**, and layout breakpoints, see **[LAYOUT-PRESETS.md](LAYOUT-PRESETS.md)**.

## Flow grid (`grid()`)

**Use for:** repeating siblings that should wrap — cards, metric tiles, form rows, filter chips.

**Mechanism:** `repeat(auto-fit, minmax(…))` with `--chirpui-grid-min`. The `cols=2|3|4` parameter **does not** mean “always N columns”; it scales the minimum track width so you tend to get more columns on wide viewports.

**Also:** `preset="bento-211"`, **`thirds`**, or **`detail-two`** on `grid()` selects **fixed** column tracks for dashboard-style cells (with `block()` for spans). Use **`detail_single=true`** with **`detail-two`** when only one column of content exists. That is still a **grid** primitive, not `frame()`. Optional **`items="start"`** / **`end`** / **`center`** sets **`align-items`** on the grid (default is **`stretch`**).

**Tokens:** `--chirpui-grid-min` (and optional overrides on a wrapper).

## Frame (`frame()`)

**Use for:** page regions with a **fixed structure** — hero (media + copy), main + sidebar, two equal columns.

**Mechanism:** explicit `grid-template-columns` per variant. Put **two direct children** in the default slot (or more if you customize via CSS).

**Variants:**

| `variant`        | Purpose                                      |
|------------------|----------------------------------------------|
| `balanced`       | Two equal columns (`1fr` / `1fr`)          |
| `hero`           | Media + copy; second column slightly wider  |
| `sidebar-end`    | Fluid main + fixed-width sidebar column     |

**Tokens:** `--chirpui-frame-gap`, `--chirpui-frame-balanced-columns`, `--chirpui-frame-hero-columns`, `--chirpui-frame-sidebar-width` (defaults align with `--chirpui-split-sidebar-width`).

**Example:**

```html
{% from "chirpui/layout.html" import frame, stack %}

{% call frame(variant="hero", gap="lg") %}
  <div class="my-hero-media">…</div>
  <div class="my-hero-copy">{% call stack(gap="md") %}…{% end %}</div>
{% end %}
```

Override columns for one page:

```html
<div class="chirpui-frame chirpui-frame--hero" style="--chirpui-frame-hero-columns: minmax(0, 1fr) minmax(0, 2fr)">
  …
</div>
```

## Overflow

Grid and frame children need **`min-width: 0`** so nested flex/grid can shrink. `.chirpui-frame > *` sets this; for flow grids, wrap cells in **`block()`** when needed. See [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md).

## Anti-patterns

- Do **not** use `grid(cols=2)` for a hero or app shell — use **`frame()`** or app-specific CSS.
- Do **not** use `frame()` for an unknown number of wrapping cards — use **`grid()`**.

## Macro reference

| Macro        | CSS base        | Role                          |
|-------------|-----------------|-------------------------------|
| `grid()`    | `chirpui-grid`  | Auto-fit flow (+ optional presets) |
| `frame()`   | `chirpui-frame` | Explicit structural columns   |
| `stack()`   | `chirpui-stack` | Vertical flex gap             |
| `block()`   | `chirpui-block` | Grid cell; `min-width: 0`     |
