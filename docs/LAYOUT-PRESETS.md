# `grid()` fixed-track presets

`grid()` defaults to **auto-fit** columns (`repeat(auto-fit, minmax(…))`). A **`preset`** switches to **fixed `grid-template-columns`** for dashboards and detail rows. **Aliases** share the same CSS classes as the canonical names (see table).

## Breakpoints (canonical)

| Token | Value | Used in |
|-------|--------|---------|
| **`--chirpui-layout-bp-sm`** | `48rem` | `thirds`, `bento-211` final stack; `frame()` stack |
| **`--chirpui-layout-bp-md`** | `52rem` | `detail-two` stack |
| **`--chirpui-layout-bp-lg`** | `64rem` | `bento-211` first narrowing |

**Note:** `@media (max-width: …)` uses the same **literal** `rem` values (CSS custom properties are not used inside media queries for broad compatibility). Keep literals in sync with `:root` tokens in `chirpui.css`.

## Preset table

| Canonical `preset` | Aliases | Tracks (wide) | Collapses | Notes |
|--------------------|---------|---------------|-----------|--------|
| **`bento-211`** | **`split-2-1-1`** | `2fr` + `1fr` + `1fr` | → 2 cols at **lg**; → 1 col at **sm** | Use **`block(span=2)`**, **`span="full"`**. |
| **`thirds`** | **`split-thirds`**, **`three-equal`** | three `1fr` | → 1 col at **sm** | Equal three-up. |
| **`detail-two`** | **`split-1-1.35`** | `1fr` + `1.35fr` | → 1 col at **md** | Optional **`detail_single=true`** or use **`detail-two-single`** when only one column of content. Includes stretch + cluster helpers for detail rows. |
| **`detail-two-single`** | **`split-1-1.35-single`** | one `1fr` | (already single) | Same as **`detail-two`** + single column; no **`detail_single`** needed. |

## Parameters

| Parameter | Applies to | Purpose |
|-----------|------------|---------|
| **`gap`** | all | `sm` / `md` / `lg` |
| **`items`** | all | `start` / `end` / `center` — **`align-items`** (default **stretch**) |
| **`detail_single`** | **`detail-two`** / **`split-1-1.35`** only | Force one full-width column. Ignored if **`preset`** is already **`detail-two-single`**. |

## `block()` spans

- **`span=2`** — two tracks (meaning depends on preset).
- **`span="full"`** — `grid-column: 1 / -1` (full row).

## Related

- [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md) — overflow/shrink-safe grids.
- [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md) — `grid()` vs `frame()` vs `bento_grid()`.
- `chirpui/bento_grid.html` — **equal** columns + card chrome; **not** the same as **`preset="bento-211"`**.
