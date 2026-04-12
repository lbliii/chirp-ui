# UI layers & terms

Authoritative site copy lives in **`site/content/docs/app-shell/ui-layers.md`**. This file is the same reference for repo-wide search (CLAUDE, IDE).

## Glossary

| Term | Meaning |
|------|---------|
| **App shell** | Persistent layout: `chirpui/app_shell_layout.html` or `app_shell()` + `shell_outlet()` (topbar, sidebar, `#main`). The document owns vertical scroll by default; `#main` is the persistent swap boundary. |
| **Page content** | `#page-content` — swapped on boosted navigation (`hx-select`); provided by `app_shell_layout.html` or `shell_outlet()`. |
| **Page chrome** | Inside `#page-content`: tabs, headers, route toolbars. |
| **Shell actions** | `shell_actions_bar` in `#chirp-shell-actions`; Chirp `ShellActions`. |
| **Shell regions** | Stable ids for HTMX OOB: see `chirp.shell_regions` in Chirp. |
| **Marketing site shell** | Full-page scroll layout: `site_shell()` + `site_header()` + `site_footer()`. Use for landing pages, docs homes, marketing sites. Counterpart to **app shell** — same document-scroll philosophy, no sidebar. |
| **Surface chrome** | Component frame (card/panel/bento border and padding) — not the app shell. |
| **Navigation domain** | The author-facing boundary declared in Chirp `_layout.html` via `{# domain: name #}`. `swap_attrs()` uses shared domain ancestry to choose the right swap target. |

Do **not** use "chrome" alone for the global frame; say **app shell**, **site shell**, or name the region.

## Chirp `mount_pages` layouts

Filesystem `_layout.html` files that extend `chirpui/app_shell_layout.html` should declare `{# target: body #}`, an explicit **`{# domain: ... #}`**, and **`{# outlet: main #}`** so Chirp can both resolve route-aware navigation and match `HX-Target: #main` on boosted requests.

Minimal pattern:

```html
{# target: body #}
{# domain: workspace #}
{# shell: workspace #}
{# outlet: main #}
{% extends "chirpui/app_shell_layout.html" %}
```

The server then wraps the page with the full shell (including `#page-content` for `hx-select`). Without `{# outlet: main #}`, `main` may not match any layout and the response can omit `#page-content`, which breaks shell swaps. See Chirp’s **filesystem routing** guide (Layouts / persistent app shell).

## Page fragment targets

`chirpui.css` styles these IDs with flex-column + gap. **Do not add layout utility classes** (e.g. `chirpui-stack--lg`) to these elements — the CSS-by-ID rules already handle spacing.

| ID | CSS | Purpose |
|----|-----|---------|
| `#page-root` | `flex-direction: column; gap: spacing-lg` | Outermost page wrapper inside `#page-content`. Route-tabs target this for sub-page swaps. |
| `#page-content` | `flex-direction: column; gap: spacing-md` | Swapped on boosted nav (`hx-select`). Direct child of `#main`; not the primary page scrollport in default shell mode. |
| `#page-content-inner` | `flex-direction: column; gap: spacing-md` | Optional inner wrapper below route-tabs. |

## Surface chrome (dashboards & data tiles)

Use this vocabulary when building analytics-style UIs inside `#page-content`:

| Building block | Macros / CSS | Typical use |
|----------------|--------------|-------------|
| **Widget frame** | `card`, `metric_card`, `animated_stat_card`, `config_card` | Title row, body, optional `header_actions`; pass `attrs_map={"id": "…"}` on `card` (and composites that forward it) so `hx-target="#…"` does not need an extra wrapper. |
| **Section grouping** | `section`, `surface` | Muted/elevated backgrounds behind a block of widgets; `section` adds `section_header`. |
| **Toolbar / filters** | `filter_bar`, `action_strip`, `filter_chip` | Page- or region-level controls (often **page chrome** if they sit under `page_header`). |
| **HTMX-safe swap root** | `fragment_island` / `safe_region` | Wrap a widget or region that updates in place so app-shell `hx-boost` / `hx-select` does not steal the swap. See [DND-FRAGMENT-ISLAND.md](./DND-FRAGMENT-ISLAND.md). |

**App shell** (`app_shell_layout`) is separate: sidebar, sticky topbar, and the persistent `#main` outlet. **Surface chrome** is everything that *looks like a card or panel* around chart/table/KPI content.

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
