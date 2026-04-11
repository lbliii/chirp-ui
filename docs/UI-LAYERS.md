# UI layers & terms

Authoritative site copy lives in **`site/content/docs/app-shell/ui-layers.md`**. This file is the same reference for repo-wide search (CLAUDE, IDE).

## Glossary

| Term | Meaning |
|------|---------|
| **App shell** | Persistent layout: `chirpui/app_shell_layout.html` or `app_shell()` + `shell_outlet()` (topbar, sidebar, `#main`). |
| **Page content** | `#page-content` — swapped on boosted navigation (`hx-select`); provided by `app_shell_layout.html` or `shell_outlet()`. |
| **Page chrome** | Inside `#page-content`: tabs, headers, route toolbars. |
| **Shell actions** | `shell_actions_bar` in `#chirp-shell-actions`; Chirp `ShellActions`. |
| **Shell regions** | Stable ids for HTMX OOB: see `chirp.shell_regions` in Chirp. |
| **Surface chrome** | Component frame (card/panel/bento border and padding) — not the app shell. |

Do **not** use “chrome” alone for the global frame; say **app shell** or name the region.

## Page fragment targets

`chirpui.css` styles these IDs with flex-column + gap. **Do not add layout utility classes** (e.g. `chirpui-stack--lg`) to these elements — the CSS-by-ID rules already handle spacing.

| ID | CSS | Purpose |
|----|-----|---------|
| `#page-root` | `flex-direction: column; gap: spacing-lg` | Outermost page wrapper inside `#page-content`. Route-tabs target this for sub-page swaps. |
| `#page-content` | `flex-direction: column; gap: spacing-md` | Swapped on boosted nav (`hx-select`). Direct child of `#main`. |
| `#page-content-inner` | `flex-direction: column; gap: spacing-md` | Optional inner wrapper below route-tabs. |

## Surface chrome (dashboards & data tiles)

Use this vocabulary when building analytics-style UIs inside `#page-content`:

| Building block | Macros / CSS | Typical use |
|----------------|--------------|-------------|
| **Widget frame** | `card`, `metric_card`, `animated_stat_card`, `config_card` | Title row, body, optional `header_actions`; pass `attrs_map={"id": "…"}` on `card` (and composites that forward it) so `hx-target="#…"` does not need an extra wrapper. |
| **Section grouping** | `section`, `surface` | Muted/elevated backgrounds behind a block of widgets; `section` adds `section_header`. |
| **Toolbar / filters** | `filter_bar`, `action_strip`, `filter_chip` | Page- or region-level controls (often **page chrome** if they sit under `page_header`). |
| **HTMX-safe swap root** | `fragment_island` / `safe_region` | Wrap a widget or region that updates in place so app-shell `hx-boost` / `hx-select` does not steal the swap. See [DND-FRAGMENT-ISLAND.md](./DND-FRAGMENT-ISLAND.md). |

**App shell** (`app_shell_layout`) is separate: sidebar, topbar, `#main`. **Surface chrome** is everything that *looks like a card or panel* around chart/table/KPI content.

## Chirp imports

```python
from chirp.shell_regions import (
    DOCUMENT_TITLE_ELEMENT_ID,
    SHELL_ACTIONS_TARGET,
    SHELL_ELEMENT_IDS,
)
```

## See also

- [SHELL-TABS-CONTRACT.md](./SHELL-TABS-CONTRACT.md) — sections, route tabs, and OOB handoffs
- [LAYOUT-OVERFLOW.md](./LAYOUT-OVERFLOW.md)
- [COMPONENT-OPTIONS.md](./COMPONENT-OPTIONS.md) — panel / surface wording
