# ChirpUI Layout & Widget Brainstorm

A design exploration for more polished, less clunky layout widgets. Inspired by feedback on settings/config pages (DORI, etc.) where current primitives feel functional but generic.

---

## 1. Page & Section Headers

### Current pain
- `page_header` and `section_header` are nearly identical (h1 vs h2)
- Flat layout: title left, actions right — no visual hierarchy beyond font size
- Config path / breadcrumb / meta info often floats awkwardly below

### Ideas

| Widget | Description |
|--------|-------------|
| **page_hero** (exists) | Use `page_hero(variant="minimal")` for settings — softer, less editorial |
| **page_header_with_meta** | Single macro: title + subtitle + meta line (e.g. config path) + actions. Meta gets `chirpui-text-muted chirpui-font-sm` and sits between title and actions |
| **section_header_inline** | Compact variant: h2 + actions on one line, no subtitle slot — for dense forms |
| **header_divider** | Optional thin accent line under header to separate from content |
| **breadcrumb_header** | Page header with integrated breadcrumb above title (Dori / Home / Settings) |

---

## 2. Config / Key-Value Cards

### Current pain
- `chirpui-card` with empty `chirpui-card__media` looks unfinished
- `chirpui-dl chirpui-dl--horizontal` is clear but monotonous
- All cards look the same; no visual differentiation for "Logs" vs "ACP" vs "Sources"

### Ideas

| Widget | Description |
|--------|-------------|
| **config_card** | Purpose-built: icon/badge in header, key-value pairs with semantic styling. No empty media — icon goes in header or as small accent |
| **config_card_compact** | Single-column stacked layout for 1–2 items; no card chrome, just a subtle surface |
| **stat_card** | For numeric config (retention_days, max_entries): large number, small label, optional sparkline/trend |
| **status_card** | For boolean-ish config (enabled, configured): green/red dot + label, compact |
| **key_value_row** | Inline `term: value` with copy button, monospace value — for URLs, paths |
| **config_section** | Group of related keys under a heading; uses `surface--muted` but with tighter padding and optional collapsible |

### Semantic value display
- `(not set)` → muted, italic, or a subtle "—" with tooltip
- URLs → monospace, truncate with ellipsis, copy-on-click
- Booleans → Yes/No as badges (success/muted) or mini toggle visual
- Numbers → right-align, optional unit suffix

---

## 3. Forms & Inline Actions

### Current pain
- "Set config value" form: two fields + button feels like a generic form block
- Section header + form + result div is a lot of structure for a simple action
- Actions section with single button feels orphaned

### Ideas

| Widget | Description |
|--------|-------------|
| **inline_form** | Key + value inputs side-by-side, submit inline (no separate section). Like a command bar: `[key▾] [value________] [Set]` |
| **key_value_form** | Semantic: `key` field with optional dropdown of known keys (acp.endpoint, etc.), `value` field, primary button. Single row on desktop |
| **action_bar** | Horizontal strip of actions (Validate, Reset, etc.) — no section header, just `chirpui-flow` in a subtle surface. Replaces "Actions" section |
| **form_in_card** | Form wrapped in a card with optional title — elevates the form without full surface |
| **floating_label_field** | Label animates/floats on focus (Material-style) — reduces vertical space |
| **compact_field_row** | Label left, input right, same row — for settings where space matters |

---

## 4. Card Variants & Layout

### Current pain
- `chirpui-card__media` is always present; empty div adds visual dead space
- Cards in a 2-col grid can feel samey
- No "feature" or "highlight" card for important config

### Ideas

| Widget | Description |
|--------|-------------|
| **card_no_media** | Card variant that omits media block entirely when not used — or collapse media height to 0 when empty |
| **card_icon_header** | Icon in header (left of title) instead of media — Logs ⟳, ACP ◇, Cursor ☁, Sources ⊞ |
| **card_accent_border** | Left border accent (4px) in theme color — quick way to differentiate sections |
| **card_grid_auto** | Grid with `auto-fill` / `minmax()` so cards size naturally; 1–4 cols based on viewport |
| **card_aside** | Narrow card (e.g. 200px) for sidebar-style config summary |
| **config_dashboard** | Composite: page header + inline form + grid of config cards + action bar. One macro to rule them all for settings pages |

---

## 5. Description List Enhancements

### Current pain
- `chirpui-dl--horizontal` is term left, detail right — works but is plain
- No copy button, no truncation for long values
- No type-aware styling (url, bool, number)

### Ideas

| Widget | Description |
|--------|-------------|
| **description_list_compact** | Tighter line-height, smaller font for terms |
| **description_list_stacked_cards** | Each row is a mini card (term + value) — good for 2–4 items |
| **detail_copyable** | `dd` with copy icon on hover — for endpoints, paths, IDs |
| **detail_truncate** | Long values get `text-overflow: ellipsis` + tooltip or expand-on-click |
| **detail_badge** | For enum/status values, render as `chirpui-badge` instead of plain text |
| **key_value_inline** | `term: value` on one line, comma-separated for very compact display |

---

## 6. Surface & Section Choreography

### Current pain
- `chirpui-surface chirpui-surface--muted` + `section_header` + content is repeated
- Feels boxy; sections don't breathe

### Ideas

| Widget | Description |
|--------|-------------|
| **section** | Composite: optional surface variant + section header + slot. One macro instead of manual nesting |
| **section_divider** | `<hr>` with consistent styling between sections |
| **section_collapsible** | `details`/`summary` with section_header as summary — for "Advanced" or rarely-used config |
| **surface_inset** | Surface with negative margin or inset shadow — creates depth without full box |
| **striped_sections** | Alternating surface/default for adjacent sections — reduces boxiness |

---

## 7. Micro-interactions & Polish

| Idea | Description |
|------|-------------|
| **focus_ring** | Consistent, visible focus styles on all interactive elements (already important for a11y) |
| **hover_lift** | Subtle `transform: translateY(-1px)` + shadow on card hover — already possible via CSS |
| **loading_skeleton** | For config cards that load async — use `skeleton(variant="card")` |
| **success_toast** | After "Set" or "Validate" — `toast("Saved", variant="success")` for feedback |
| **empty_state_inline** | For config sections with no values — "No overrides" with optional "Add" link |

---

## 8. Suggested Implementation Order

1. **Quick wins (CSS only)**
   - Collapse `chirpui-card__media` when empty (0 height, no layout shift)
   - Add `config_card` or `card_icon_header` — icon in header, no media
   - `section` composite macro to reduce boilerplate

2. **Config-specific**
   - `config_card` with semantic value rendering (badge for bool, monospace for URL)
   - `inline_form` or `key_value_form` for "Set config value"
   - `action_bar` for Validate / Migrate / etc.

3. **Layout refinements**
   - `page_header_with_meta` for config path
   - `description_list` enhancements (copyable, truncate, badge)

4. **Nice-to-have**
   - `config_dashboard` composite
   - `section_collapsible`
   - Hover/polish micro-interactions

---

## 9. Design References (for inspiration)

- **Linear** — Clean settings, minimal chrome, good use of muted surfaces
- **Vercel Dashboard** — Config as key-value with copy, status indicators
- **Raycast** — Dense but readable, good typography hierarchy
- **GitHub Settings** — Sectioned, collapsible, action bars
- **Stripe Dashboard** — Cards with accent borders, clear primary actions

---

## 10. Open Questions

- Should `page_header` and `section_header` share more implementation (e.g. one macro with `level` param)?
- Is a `config_*` namespace too specific, or should these be generic (`key_value_card`, etc.)?
- How much should ChirpUI assume about HTMX (e.g. `hx-post` on forms) vs stay presentation-only?
