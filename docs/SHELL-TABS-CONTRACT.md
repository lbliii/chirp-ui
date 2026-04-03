# Shell, sections, and route tabs — contract checklist

Use this when building a Chirp app with chirp-ui’s app shell and subsection navigation.

## Layers

| Layer | Responsibility |
|-------|------------------|
| **App shell** | `app_shell` / layout: sidebar, topbar, `#main`. Persists across boosted navigation. |
| **Page content** | `#page-content` — selected via `hx-select` on boosted requests. |
| **Page chrome** | Inside `#page-content`: route tabs, page header, toolbars. |

Stable fragment targets (`#page-root`, `#page-content-inner`) are documented in [UI-LAYERS.md](./UI-LAYERS.md).

## Delivery modes (quick reference)

| Delivery | Template usage | Swap target | Layout chain | OOB |
|----------|----------------|-------------|--------------|-----|
| Full page (browser nav) | All layouts nested | `body` (full doc) | Root to deepest | N/A |
| Boosted nav (`hx-boost`) | Layouts from `hx-select` target down | `#page-content` | Mid-chain | Sidebar, title, breadcrumbs |
| Route tab click | Page chrome + content | `#page-root` | Innermost only | Title, breadcrumbs |
| Fragment endpoint | Named block only | Caller's `hx-target` | None | Per response |
| SSE / EventStream | Fragment yields | Caller's `hx-target` | None | Per event |

## Chirp: sections and metadata

1. **`register_section(Section(...))`** before `mount_pages()` — define `id`, `label`, `tab_items`, `breadcrumb_prefix`, `active_prefixes`.
2. **`TabItem`** fields: `label`, `href`, optional `icon`, `badge`, `match` (`"exact"` default or `"prefix"` for nested URLs). Same information flows to templates as `tab_items` / `route_tabs` dicts.
3. **Each page** `_meta.py`: set `section="<id>"` so shell context resolves tabs and breadcrumbs for that route family.
4. **`app.check()`** — run in CI; it warns on unknown `meta.section`, missing tab routes, duplicate tab hrefs in a section, section coverage (`active_prefixes` vs `meta.section`), and other hypermedia contracts.

## chirp-ui: route tabs

1. **`render_route_tabs`** / **`tab_is_active`** — register via `use_chirp_ui(app)`; tabs are `role="navigation"` links, not ARIA `tablist`.
2. **Tab dict shape**: `{ label, href, icon?, badge?, match? }`. Prefix matching follows `tab_is_active` in `chirp_ui/route_tabs.py`.
3. **Targets** — default `hx-target="#page-root"` so subsection navigation swaps page chrome + inner content without reloading the app shell.
4. **Boost** — route tab links use `hx-boost="false"` so they do not inherit the shell’s boosted `hx-select`; see component source.

## OOB handoffs

When a response must update sidebar, breadcrumbs, document title, or the tab strip without a full page load, use **`register_oob_region`** (or Chirp’s shell OOB helpers) with stable `target_id`s aligned to your layout. Fragment responses that change the current section should include matching OOB swaps so chrome stays consistent.

## Reliability tips

- Keep **one source of truth** for tab definitions: `Section.tab_items` (`TabItem`), not a parallel app-only model.
- After adding routes, run **`app.check()`** and fix section / tab href warnings.
- Prefer **prefix** `match` when a tab represents a URL subtree (e.g. `/settings` for `/settings/wizard`).
