# chirp-ui Component Options Reference

Valid variant, size, and option values for chirp-ui components. When **strict mode** is enabled (e.g. `app.debug=True` with Chirp's `use_chirp_ui`), invalid values log warnings and fall back to defaults.

Prefer composition primitives and component slots over legacy helper-class chains when authoring templates. See [Primitive Vocabulary](PRIMITIVES.md) for the blessed primitive set and the compatibility-helper boundary.

See [Strict mode](#strict-mode) for setup.

---

## Slot Reference

| Component | Slot name | Purpose | Required? |
|-----------|-----------|---------|------------|
| `page_header` | `actions` | Model selectors, badges, toggles — content outside the slot is the body | No |
| `document_header` | `actions` | Document-level actions like Save, Preview, Compare | No |
| `section_header` | `actions` | Section-level buttons (Refresh, Auto-detect) | No |
| `section_header_inline` | default (unnamed) | Compact actions on one line with title | No |
| `hero` | `action` | Primary CTA button | No |
| `file_tree` | `header`, `actions`, `footer` | Explorer search/filter, toolbar actions, footer summary | No |
| `page_hero` | `eyebrow`, `actions`, `metadata`, `footer` | Hero sub-regions | No |
| `alert` | `actions` | Alert action buttons | No |
| `sidebar` | `header`, `footer`, default (nav) | Sidebar regions | No |
| `composer_shell` | `header`, `identity`, `fields`, `toolbar`, `body`, `preview`, `status`, `actions` | Structured authoring form regions | No |
| `token_input` | `tokens`, `input`, `results` | App-owned autocomplete token picker regions | No |
| `rendered_content` | default (unnamed) | Rendered prose/content wrapper | No |
| `chip_group` | default (unnamed) | Facet, tag, or metadata chips | No |
| `card` | `header_actions`, `media`, `body_actions`, default | Card regions | No |
| `resource_card` | `badges`, `subtitle`, `footer`, default | Resource card regions | No |
| `confirm_dialog` | `form_content` | Hidden fields when `confirm_url` set | No |

**Note:** `section_header_inline` uses the **default** slot (not `actions`). This will be unified in a future release; use `section_header(variant="inline")` for the named `actions` slot.

## Macro Slot Context

Components that use `{% slot %}` (e.g. `form`, `card`, `card_link`, `resource_index`, `resource_card`, `field_wrapper`) render slot content in the **caller's context**. Page variables passed to the handler (e.g. `selected_tags`, `q`) are available inside macro slots without `| default()`.

```html
{% call form("/search", method="get") %}
  {{ search_bar("q", value=q, variant="with-button", placeholder="Search...") }}
  {% if selected_tags %}
    {{ hidden_field("tags", value=selected_tags | join(",")) }}
  {% end %}
{% end %}
```

**search_bar** — Composite search input with layout variants. Use inside a form.

| Param | Description |
|-------|-------------|
| `variant` | `solo` (input only, for live search), `with-button` (input + compact submit), `with-icon` (input with ⌕ prefix) |
| `button_label` | Submit button text when `variant="with-button"` (default: "Search") |
| `button_icon` | Icon for button or prefix when `variant="with-icon"` (default: "⌕") |
| `search_sync` | When `search_url`/`search_target` set, defaults to `this:replace` for live search. Override or pass `""` to disable. |

With `with-button`, the input flexes to fill space; the button stays compact. Live search with `search_url`/`search_target` uses `hx-sync="this:replace"` by default to prevent stale results when typing rapidly.

Use `| default()` for optional variables that may be unset on first load (e.g. `selected_tags | default([])` when the handler may omit the key). Variables used inside macro slots must be in the page context — Chirp passes handler context through to `render_block()`.

---

## Icon registry

Components that accept an `icon` param (e.g. `section`, `card`, `btn`, `alert`, `badge`) resolve **semantic names** via the `icon` filter. Use names for consistency; raw glyphs still work.

```html
{% call section("System status", icon="status") %}
{% call section("Validation", icon="validate") %}
{{ btn("Refresh", icon="refresh") }}
{{ config_card(title="Logs", icon="logs") }}
```

| Name | Glyph |
|------|-------|
| status, validate, run | ◎ |
| home | ◉ |
| shortcut | ⌘ |
| skills | ✦ |
| add | + |
| refresh | ↻ |
| search | ⌕ |
| reply | ↩ |
| comment, watch | ◉ |
| share | ↗ |
| up, arrow-up, vote-up | ▲ |
| down, arrow-down, vote-down | ▼ |
| follow, star | ★ |
| report, alert | ↑ |
| arrow, migrate, config | ▸ |
| wizard, diamond, settings | ◇ |
| gear | ⚙ |
| bullet | ● |
| spark | ✦ |
| logs | ⟳ |
| cloud | ☁ |
| sources | ⊞ |
| chain | ⛓ |
| link | ⟶ |
| dots | ⋯ |

Unknown names pass through unchanged. Use `{{ "custom" | icon }}` in templates when needed.

---

## Components with Variants

| Component | Param | Valid values | Default |
|-----------|-------|--------------|---------|
| **alert** | `variant` | info, success, warning, error | info |
| **badge** | `variant` | primary, success, warning, error, muted, info | — |
| **surface** | `variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke | default |
| **aura** | `tone` | accent, warm, cool, muted, primary | accent |
| **aura** | `spread` | sm, md, lg | md |
| **aura** | `mirror` | false, true (horizontal flip of the halo; e.g. column on the left) | false |
| **toast** | `variant` | info, success, warning, error | info |
| **hero** | `background` | solid, muted, gradient, mesh, animated-gradient | solid |
| **page_hero** | `variant` | editorial, minimal | editorial |
| **page_hero** | `background` | solid, muted, gradient | solid |
| **description_list** | `variant` | stacked, horizontal | stacked |
| **description_item** | `type` | bool, url, number, unset | — |
| **action_strip** | `surface_variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke | muted |
| **action_strip** | `density` | sm, md | md |
| **action_strip** | `wrap` | wrap, scroll, collapse | wrap |
| **skeleton** | `variant` | *(empty)*, avatar, text, card | *(empty)* |
| **confirm** | `variant` | default, danger | default |
| **confirm_dialog** | `hx_target`, `hx_swap`, `hx_select`, `hx_push_url` | HTMX params for confirm form (when `confirm_url` set) | — |
| **overlay** | `variant` | dark, gradient-bottom, gradient-top | dark |
| **progress_bar** | `variant` | gold, radiant, success, watched | gold |
| **progress_bar** | `size` | sm, md, lg | md |
| **bar_chart** | `variant` | gold, radiant, success, muted | gold |
| **bar_chart** | `size` | sm, md, lg | md |
| **donut** | `variant` | gold, success, muted | gold |
| **donut** | `size` | sm, md, lg | md |
| **btn** | `variant` | *(empty)*, default, primary, ghost, danger, success, warning | *(empty)* |
| **btn** | `size` | `sm` or omitted | omitted |
| **logo** | `variant` | text, image, both | both |
| **logo** | `size` | sm, md, lg | md |
| **logo** | `align` | start, center, end | center |
| **page_header** | `variant` | default, compact | default |
| **section_header** | `variant` | default, inline | default |
| **message_bubble** | `role` | default, user, assistant, system | default |
| **message_bubble** | `align` | left, right | left |

---

## Shell Frame and Safe Regions

| Component | Description |
|-----------|-------------|
| `shell_outlet` | Main content swap target; wraps content in `#page-content` for hx-select |
| `shell_outlet_attrs` | Standard hx-boost/hx-target/hx-swap/hx-select attributes (now built into `<main>` in `app_shell_layout.html`) |
| `shell_region` | Persistent region container (id for OOB updates) |
| `safe_region` | HTMX-safe mutation region; `hx-disinherit` to avoid inherited shell attributes |
| `fragment_island` | Alias for `safe_region`; use either |

## JavaScript Dependencies

Interactive components require **Alpine.js**. With Chirp, `use_chirp_ui(app)`
auto-enables Alpine injection and also injects `chirpui-alpine.js`, which
registers chirp-ui's named Alpine controllers. `chirpui.js` remains the
pre-paint theme/style initializer only.

| Template / Component | Required JS | Notes |
|---------------------|-------------|-------|
| `dropdown_menu.html` | Alpine.js + `chirpui-alpine.js` | Uses `chirpuiDropdown()` / `chirpuiDropdownSelect()` |
| `modal.html` | Alpine.js + `chirpui-alpine.js` | `modal_trigger` uses `chirpuiDialogTarget()`; native `<dialog>` remains the dialog surface |
| `modal_overlay.html` | Alpine.js | Overlay behavior |
| `tray.html` | Alpine.js | Slide-in panel |
| `tabs_panels.html` | Alpine.js | Tab switching |
| `theme_toggle.html` | Alpine.js + `chirpui-alpine.js` | Theme/style persistence via named controllers |
| `copy_button.html` | Alpine.js + `chirpui-alpine.js` | Copy-to-clipboard via `chirpuiCopy()` |
| `forms.html` (masked_field, phone_field, money_field) | Alpine.js + @alpinejs/mask | `x-mask`, `x-mask:dynamic` |
| `chirpui.js` | — | Pre-paint theme/style init only |
| `chirpui-alpine.js` | Alpine.js | Named controller runtime for chirp-ui behavior API |

**Static path:** Include `chirpui.css`, `chirpui.js`, and `chirpui-alpine.js`
from `chirp_ui.static_path()`. With Chirp, prefer `use_chirp_ui(app)` so the
runtime is injected automatically and stays aligned with Chirp's Alpine
bootstrap. In standalone setups, load `chirpui-alpine.js` before the Alpine
core script.

---

## Fragment Island and DnD Primitives

| Component | Description |
|-----------|-------------|
| `fragment_island` | Alias for `safe_region`; HTMX-safe mutation region |
| `dnd_list`, `dnd_item`, `dnd_handle`, `dnd_drop_indicator` | Row drag-drop primitives |
| `dnd_board`, `dnd_column`, `dnd_card` | Kanban board primitives |

See [DND-FRAGMENT-ISLAND.md](DND-FRAGMENT-ISLAND.md) for cookbook examples and anti-footgun guidance.

---

## Dashboard Primitives

Dashboard-grade interaction components. See [DASHBOARD-MATURITY-CONTRACT.md](DASHBOARD-MATURITY-CONTRACT.md) for usage principles.

| Component | Description |
|-----------|-------------|
| `inline_edit_field_display` | Display block with Edit trigger; swap target for HTMX |
| `inline_edit_field_form` | Edit form with save/cancel; HTMX swap target |
| `row_actions` | Kebab dropdown for table row actions (uses dropdown_menu) |
| `status_with_hint` | Badge + tooltip for status with details |
| `entity_header` | Title + meta + actions for entity detail pages |

### inline_edit_field

```html
{% from "chirpui/inline_edit_field.html" import inline_edit_field_display, inline_edit_field_form %}
{{ inline_edit_field_display(value=item.name, edit_url="/items/1/edit-name", swap_id="name-field") }}
{{ inline_edit_field_form(name="name", value=item.name, save_url="/items/1/save-name", cancel_url="/items/1", swap_id="name-field") }}
```

Uses `hx-sync` internally: form aborts when Cancel link fires; Cancel aborts when form submits; Edit trigger uses `this:replace` for rapid clicks.

### row_actions

```html
{% from "chirpui/row_actions.html" import row_actions %}
{{ row_actions(items=[{"label": "Edit", "href": "/edit"}, {"label": "Delete", "href": "/del", "variant": "danger"}]) }}
```

### confirm_dialog (HTMX)

When `confirm_url` is set, add `hx_target`, `hx_swap`, `hx_select`, `hx_push_url` for HTMX form submission. Use `{% slot form_content %}` for hidden fields (e.g. entity id):

```html
{% from "chirpui/confirm.html" import confirm_dialog, confirm_trigger %}
{% call confirm_dialog("del-dlg", title="Delete?", message="Cannot be undone.", confirm_label="Delete",
   variant="danger", confirm_url="/items/1", confirm_method="DELETE",
   hx_target="#main", hx_swap="innerHTML", hx_select="#page-content", hx_push_url="/items") %}
{% slot form_content %}<input type="hidden" name="id" value="123">{% end %}
{% end %}
{{ confirm_trigger("del-dlg", label="Delete") }}
```

### table enhancements

| Param | Description |
|-------|-------------|
| `rows` | List of tuples/lists — data-driven mode, alignment applies to all cells automatically |
| `sticky_header` | Adds chirpui-table-wrap--sticky for sticky thead |
| `actions_header` | Adds empty th for row actions column |

Data-driven tables (alignment flows to headers and body cells):

```html
{{ table(headers=["Name", "Status", "Count"],
         rows=[("Alice", "Active", "42"), ("Bob", "Idle", "7")],
         align=["left", "center", "right"]) }}
```

Slot-based tables (alignment auto-inherited by `row()` via `provide`/`consume`):

```html
{% call table(headers=["Name", "Count"], align=["left", "right"]) %}
  {{ row("Alice", "42") }}
  {{ row("Bob", "7") }}
{% end %}
```

> **Deprecated:** `aligned_row(cells, align)` still works but is no longer needed — `row()` inside `table(align=...)` inherits alignment automatically. `aligned_row` will be removed in 0.3.0.

---

## Card

Use `card(title="...", icon="⟳")` for config/settings cards. The `icon` renders in the header; no media block is needed. Empty `chirpui-card__media` is hidden via CSS.

```html
{% from "chirpui/card.html" import card %}
{% call card(title="Logs", icon="⟳") %}
  ...
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Card header title |
| `icon` | Icon character in header (avoids empty media) |
| `subtitle` | Optional subtitle under title |
| `variant` | Optional: feature, media, horizontal, stats |
| `border_variant` | Optional: gradient (gradient border via background-clip) |
| `header_variant` | Optional: gradient (gradient in header strip) |
| `attrs` | Raw extra attributes on the outer `<article>` / `<details>` (same pattern as `surface`) |
| `attrs_map` | Mapping for extra attributes; use e.g. `{"id": "kpi-users"}` for `hx-target` on dashboard widgets |

**Slots:** `header_actions`, `media`, `body_actions` (for list cards), default (body).

### resource_card

Opinionated list/index card for app resources. Prefer this when a card represents a browseable thing such as a skill, chain, thread, task, playlist, project, or user.

```html
{% from "chirpui/card.html" import resource_card %}
{% call resource_card("/skills/doc-help", "doc-help", description="Draft docs from code", top_meta="builtin") %}
  {% slot subtitle %}<code>::help</code>{% end %}
  {% slot footer %}<span class="chirpui-badge chirpui-badge--muted">docs</span>{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `href` | Primary destination for the resource |
| `title` | Resource title |
| `description` | Optional summary paragraph in the card body |
| `top_meta` | Optional compact meta row above the title |
| `top_meta_href` | Optional href for `top_meta` when `link_mode="main"` |
| `top_meta_title` | Optional tooltip/title for the top meta row |
| `link_mode` | `all` for full-card link, `main` when footer/meta need independent links |
| `cls` | Optional additional classes |

**Slots:** `badges`, `subtitle`, `footer`, default (extra body content).

---

## Layout (layout.html)

### page_header

Place model selectors, badges, and toggles in `{% slot actions %}`. Content outside the slot is the body.

```html
{% from "chirpui/layout.html" import page_header %}
{% call page_header("Ollama Chat", variant="compact") %}
{% slot actions %}
  <select>...</select>
  <span class="chirpui-badge">llama3</span>
{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Page title (h1) |
| `subtitle` | Optional subtitle |
| `meta` | Optional meta line (e.g. config path) — muted, below subtitle |
| `breadcrumb_items` | Optional list of `{label, href?}` for breadcrumbs above title |
| `variant` | `default` or `compact` — compact for dense header bars |

### shell_actions_bar

Canonical renderer for route-scoped shell actions resolved by Chirp. Use it in
persistent shells and target the containing element with `id="chirp-shell-actions"`
or another stable id that matches `shell_actions.target`.

```html
{% from "chirpui/shell_actions.html" import shell_actions_bar %}
<div id="chirp-shell-actions">
  {{ shell_actions_bar(shell_actions) }}
</div>
```

The renderer expects a resolved action object with `primary`, `controls`, and
`overflow` zones. `overflow` items render as a compact dropdown in the top bar.

### container

Responsive page-width wrapper. `padding=true` keeps the standard container gutter; set `padding=false` only when a nested surface or blade owns the edge spacing.

### grid

Responsive layout grid for cards and sections.

| Param | Description |
|-------|-------------|
| `cols` | `2`, `3`, `4`, or omitted for auto-fit (scales minimum track width, not a fixed column count) |
| `gap` | `sm`, `md`, `lg` |
| `preset` | `bento-211` or `thirds` for fixed-track dashboard cells (with `block()` spans) |
| `cls` | Optional additional classes |

Use `grid()` for **flow** — repeating items that wrap. Prefer `gap="md"` for page content and `gap="sm"` for denser internal layouts. For hero / sidebar **regions** with explicit columns, use `frame()` and see [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md).

### frame

Structural two-column layouts (explicit `grid-template-columns`). Pass **two direct children** in the default slot (e.g. media + copy).

| Param | Description |
|-------|-------------|
| `variant` | `balanced` (default), `hero`, `sidebar-end` |
| `gap` | `sm`, `md`, `lg` |
| `cls` | Optional additional classes |

Override tracks per page with CSS variables on the element (e.g. `--chirpui-frame-hero-columns`). Full detail: [LAYOUT-GRIDS-AND-FRAMES.md](LAYOUT-GRIDS-AND-FRAMES.md).

### stack

Vertical layout primitive.

| Param | Description |
|-------|-------------|
| `gap` | `xs`, `sm`, `md`, `lg`, `xl` |
| `cls` | Optional additional classes |

Use `stack()` for most page and component vertical rhythm. `gap="lg"` is the default page-level cadence; `sm` and `xs` are for denser local groupings.

### cluster

Wrapping inline layout primitive for badges, aliases, chips, and compact action groups.

| Param | Description |
|-------|-------------|
| `gap` | `xs`, `sm`, `md`, `lg` |
| `cls` | Optional additional classes |

Use `cluster()` when content should wrap horizontally but remain visually grouped. This is the preferred primitive for badge/tag rows; `chirpui-flow` remains as the compatibility utility class.

### layer

Overlapping card deck layout — children overlap with negative margin and slight rotation, hover straightens and elevates. Inspired by emdashCSS's "layer" pattern.

```html
{% from "chirpui/layout.html" import layer %}
{% call layer(direction="center", overlap="md", angle="subtle") %}
  <div class="chirpui-card">Card 1</div>
  <div class="chirpui-card">Card 2</div>
  <div class="chirpui-card">Card 3</div>
{% end %}
```

| Param | Description |
|-------|-------------|
| `direction` | `left` (default), `center`, `right` — horizontal alignment of the deck |
| `overlap` | `sm` (-1.5rem), `md` (-3rem), `lg` (-5rem) — how much cards overlap |
| `angle` | `none`, `subtle` (default, ~2deg), `moderate` (~4deg) — idle rotation on non-first cards |
| `hover` | `true` (default) — hover straightens card and raises z-index |
| `cls` | Optional additional classes |

Children alternate tilt direction (even children rotate opposite) for a natural "fanned" look. All transforms respect `prefers-reduced-motion` — rotation is disabled, only a subtle scale remains on hover.

Override overlap and angle via CSS custom properties: `--chirpui-layer-overlap-sm`, `--chirpui-layer-overlap-md`, `--chirpui-layer-overlap-lg`, `--chirpui-layer-angle-subtle`, `--chirpui-layer-angle-moderate`.

### Container modifiers

CSS-only classes that propagate non-inheritable properties to direct children. Inspired by emdashCSS's `c-*` prefix pattern (e.g. `.c-rounded-11 > *`). Use on any parent element — works with `grid()`, `cluster()`, `layer()`, or plain `<div>`.

```html
{% call grid(cols=3, gap="md") %}
  {# All cards get rounded corners without passing to each macro #}
  <div class="chirpui-children--rounded-lg">
    {{ card("A") }}
    {{ card("B") }}
    {{ card("C") }}
  </div>
{% end %}
```

| Class | Effect on `> *` |
|-------|-----------------|
| `chirpui-children--rounded` | `border-radius: var(--chirpui-radius)` |
| `chirpui-children--rounded-sm` | `border-radius: var(--chirpui-radius-sm)` |
| `chirpui-children--rounded-lg` | `border-radius: var(--chirpui-radius-lg)` |
| `chirpui-children--rounded-xl` | `border-radius: var(--chirpui-radius-xl)` |
| `chirpui-children--rounded-full` | `border-radius: 9999px` (pill/circle) |
| `chirpui-children--equal` | `flex: 1` (uniform sizing in flex contexts) |
| `chirpui-children--clip` | `min-width: 0; overflow: hidden` (prevent blowout) |

**Design note:** This is intentionally a small set covering non-inheritable CSS properties only. For semantic context propagation (variants, density), use `provide`/`consume`. For inheritable theming, use `--chirpui-*` custom properties.

### section

Composite: surface + section_header + content. Reduces boilerplate. Use `{% slot actions %}` for section-level buttons (Refresh, Auto-detect, Run validation).

```html
{% from "chirpui/layout.html" import section %}
{% from "chirpui/button.html" import btn %}
{% call section("Setup targets", icon="◎", surface_variant="muted") %}
{% slot actions %}{{ btn("Refresh", attrs_map={"hx-get": "/status", "hx-target": "#targets"}) }}{% end %}
<div id="targets">...</div>
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Section heading (h2) |
| `subtitle` | Optional subtitle below title |
| `icon` | Optional ASCII/Unicode icon left of title (aligns with card, entity_header) |
| `surface_variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke (default: muted) |
| `full_width` | If true, wraps in `chirpui-blade` for edge-to-edge layout (breaks out of container) |
| `parallax` | If true with full_width, adds subtle scroll-driven animation (Chrome 115+); respects prefers-reduced-motion |

**surface_variant usage (semantic convention):** Surface variants convey **section role**, not visual rhythm. The eye should scan hierarchy without reading a word.

| Variant | Role | Use for |
|---------|------|---------|
| `elevated` | Look here first | Health checks, system status, version info, dashboard stats |
| `accent` | Do this | Primary action area: validation, run buttons, auto-detect. Max one per page. |
| `default` | Fill this in | Form input, neutral workspace: config forms, search, compare inputs |
| `muted` | Reference | Background grouping, locations, catalogs, secondary detail |

**When to skip:** Pages with 0–1 sections, or pages where cards already provide grouping (skill detail, collection detail), do not need surface_variant differentiation. Don't wrap content in a section just to apply a variant.

Glass, frosted, smoke need a colored background behind to show blur.

### section_header_inline

Compact header for dense forms: h2 + actions on one line, no subtitle. Params: `title`, `icon` (optional), `cls`.

### section_collapsible

`details`/`summary` with section_header as summary. For "Advanced" config blocks.

### panel

Reusable titled pane for inspectors, activity feeds, file trees, and embedded side surfaces.

```html
{% from "chirpui/panel.html" import panel %}
{% call panel(title="Tool Activity", subtitle="Inspector rail", scroll_body=true) %}
  {% slot actions %}{{ btn("Clear", variant="ghost", size="sm") }}{% end %}
  <div>Activity rows...</div>
  {% slot footer %}<span class="chirpui-text-muted chirpui-ui-sm">Connected</span>{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Optional panel title |
| `subtitle` | Optional supporting line below title |
| `surface_variant` | Surface styling for the panel shell; same values as `surface` |
| `scroll_body` | Makes the body region independently scrollable |
| `cls` | Optional additional classes |

**Slots:** `actions`, default (body), `footer`.

Use `panel()` when a region needs its own **surface chrome** (frame + scroll) inside a larger page or workspace. This is the preferred primitive for activity rails, file explorers, and inspector panes.

### file_tree

Workbench-oriented file explorer that composes `panel()` and `nav_tree()` into one reusable primitive.

```html
{% from "chirpui/file_tree.html" import file_tree %}
{% call file_tree(items=items, title="Files", show_icons=true) %}
  {% slot actions %}{{ btn("Refresh", variant="ghost", size="sm") }}{% end %}
  {% slot header %}<input type="search" placeholder="Filter files">{% end %}
  {% slot footer %}<span class="chirpui-text-muted chirpui-ui-sm">12 files</span>{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `items` | Tree items using the same shape as `nav_tree` (`title`, `href`, `children`, `active`, `open`, optional `icon`) |
| `title` | Optional explorer title |
| `subtitle` | Optional supporting line below the title |
| `show_icons` | Renders `item.icon` values when present |
| `surface_variant` | Surface styling for the outer panel |
| `scroll_body` | Makes the explorer body independently scrollable |
| `cls` | Optional additional classes |

**Slots:** `header`, `actions`, `footer`.

Use `file_tree()` for CMS and IDE-like explorer rails where you want **panel** surface chrome and tree behavior together. For raw tree markup without that frame, keep using `nav_tree()`.

### split_layout

Generic two-pane work surface for explorer/content, editor/preview, and content/inspector compositions.

```html
{% from "chirpui/split_layout.html" import split_layout %}
{% call split_layout(ratio="sidebar") %}
  {% slot primary %}<nav>Tree</nav>{% end %}
  {% slot secondary %}<main>Editor</main>{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `direction` | `horizontal` (default) or `vertical` |
| `ratio` | `sidebar`, `balanced`, `wide-primary`, `wide-secondary` |
| `gap` | `sm`, `md`, `lg` |
| `cls` | Optional additional classes |

**Slots:** `primary`, `secondary`.

V1 is CSS-only and non-resizable. Prefer `ratio="sidebar"` for file trees and `wide-primary` for editor/preview layouts where the main surface should dominate.

### workspace_shell

Opinionated workbench composite for IDE-like and CMS-authoring pages inside an existing app shell.

```html
{% from "chirpui/workspace_shell.html" import workspace_shell %}
{% call workspace_shell("Authoring", subtitle="Edit and preview", sidebar_title="Files",
    show_inspector=true, inspector_title="Preview") %}
  {% slot toolbar %}{{ btn("Save", variant="primary", size="sm") }}{% end %}
  {% slot sidebar %}<nav>Tree</nav>{% end %}
  <textarea></textarea>
  {% slot inspector %}<div>Preview</div>{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Optional workspace title |
| `subtitle` | Optional workspace subtitle |
| `sidebar_title` | Optional title for the sidebar panel |
| `show_inspector` | Enables the right-hand inspector split |
| `inspector_title` | Optional title for the inspector panel |
| `sidebar_surface_variant` | Surface styling for the sidebar panel |
| `inspector_surface_variant` | Surface styling for the inspector panel |
| `cls` | Optional additional classes |

**Slots:** `toolbar`, `sidebar`, default (main surface), `inspector`.

Use `workspace_shell()` when you want one canonical composite for file tree + editor, file tree + viewer, or authoring + preview pages. It composes `panel()` and `split_layout()` for you.

### document_header

Document-oriented header for editor, preview, and detail surfaces inside a larger workspace.

```html
{% from "chirpui/document_header.html" import document_header %}
{% call document_header("README.md", subtitle="Skill guide", path="docs/README.md",
    provenance="Forked from builtin/doc-help", status="Draft") %}
  {% slot actions %}{{ btn("Save", variant="primary", size="sm") }}{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Document title |
| `subtitle` | Optional supporting line below the title |
| `meta` | Optional `page_header` meta line |
| `breadcrumb_items` | Optional breadcrumbs passed through to `page_header` |
| `eyebrow` | Optional small uppercase context label above the header |
| `path` | Optional file/path pill |
| `provenance` | Optional source/fork detail |
| `status` | Optional inline status chip |
| `meta_items` | Optional additional small metadata items |
| `cls` | Optional additional classes |

**Slots:** `actions`.

Use `document_header()` when a surface needs document/file context without taking over app-shell title or breadcrumb regions.

### empty_panel_state

Compact empty-state wrapper for pane bodies and unloaded workbench surfaces.

```html
{% from "chirpui/empty_panel_state.html" import empty_panel_state %}
{% call empty_panel_state(title="No file selected", icon="docs") %}
  <p>Select a file from the explorer to start editing.</p>
  {% slot action %}{{ btn("Browse", variant="primary", size="sm") }}{% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `icon` | Optional icon or glyph |
| `title` | Empty-state title |
| `illustration` | Optional richer illustration markup |
| `action_label` | CTA label when using built-in link action |
| `action_href` | CTA destination when using built-in link action |
| `code` | Optional code/query pill |
| `suggestions` | Optional list of suggestions |
| `search_hint` | Optional search guidance line |
| `compact` | Applies the panel-friendly compact treatment (default: `true`) |
| `cls` | Optional additional classes |

**Slots:** default body, `action`.

Use `empty_panel_state()` for side rails, editor placeholders, and inspector panes where the full `empty_state()` treatment is too roomy.

---

## Navigation

### logo

Reusable brand mark component for nav and app-shell brand areas.

```html
{% from "chirpui/logo.html" import logo %}

{{ logo(text="ChirpUI", variant="text") }}
{{ logo(image_src="/static/brand.svg", image_alt="ChirpUI", variant="image") }}
{{ logo(text="ChirpUI", image_src="/static/brand.svg", href="/", variant="both", size="md") }}
```

| Param | Description |
|-------|-------------|
| `text` | Brand label text. |
| `image_src` | Logo image URL/path. |
| `image_alt` | Image alt text. Recommended for image-only logos. |
| `href` | Optional link wrapper. When omitted, renders non-link root. |
| `variant` | `text`, `image`, `both` (default: `both`). |
| `size` | `sm`, `md`, `lg` (default: `md`). |
| `align` | `start`, `center`, `end` (default: `center`). |
| `cls` | Additional classes for custom styling. |

Accessibility notes:
- If `variant="both"`, prefer `image_alt=""` (default) to avoid duplicate announcements.
- If `variant="image"` and `image_alt` is empty, provide `text`; it is rendered as visually hidden fallback label.

Use logo directly in navigation components:

```html
{% from "chirpui/navbar.html" import navbar, navbar_link %}
{% from "chirpui/logo.html" import logo %}
{% call navbar(brand_url="/", use_slots=true, brand_slot=true) %}
  {% slot brand %}{{ logo(text="ChirpUI", image_src="/static/brand.svg", variant="both") }}{% end %}
  {{ navbar_link("/docs", "Docs") }}
{% end %}
```

---

## Forms

### key_value_form

Inline key + value inputs + submit. For "Set config value" etc.

```html
{% from "chirpui/forms.html" import key_value_form %}
{{ key_value_form("/config/set", attrs_map={"hx-post": "/config/set", "hx-target": "#result", "hx-swap": "innerHTML"},
                 key_placeholder="e.g. acp.endpoint", value_placeholder="e.g. https://...") }}
```

| Param | Description |
|-------|-------------|
| `action` | Form action URL |
| `key_options` | Optional list of `{value, label}` for datalist suggestions |
| `attrs_map` | Preferred structured attrs (`{"hx-post": "...", "hx-target": "#..."}`) |
| `attrs` | Legacy raw attr string escape hatch |

---

## Config Components

### action_strip

Canonical action container for list/index pages. Distinct from `action_bar` (social actions).

Recommended inner zones:
- `.chirpui-action-strip__primary`: leading area (usually search)
- `.chirpui-action-strip__controls`: filter/sort/toggle controls
- `.chirpui-action-strip__actions`: trailing CTA buttons

Recommended usage:

```html
{% from "chirpui/action_strip.html" import action_strip %}
{% from "chirpui/forms.html" import search_bar %}
{% from "chirpui/button.html" import btn %}

{% call action_strip(surface_variant="muted", density="sm", wrap="wrap") %}
  <div class="chirpui-action-strip__primary">
    <form>{{ search_bar("q", variant="with-button", placeholder="Search...") }}</form>
  </div>
  <div class="chirpui-action-strip__controls">
    {{ btn("Filters", variant="default", size="sm") }}
  </div>
  <div class="chirpui-action-strip__actions">
    {{ btn("Create", variant="primary", size="sm") }}
  </div>
{% end %}
```

| Param | Description |
|-------|-------------|
| `surface_variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke |
| `density` | `sm`, `md` |
| `wrap` | `wrap` (default), `scroll` (single-row horizontal scroll), `collapse` (compact controls) |
| `sticky` | `true` for sticky toolbar behavior |

### Action Container Variants

**`filter_bar` vs `filter_chips`:** two different patterns—do not confuse the template names.

| Template | Macro(s) | Use when |
|----------|-----------|----------|
| `chirpui/filter_bar.html` | `filter_bar` | **Form-backed** filter toolbar: GET/POST to an action URL, `action_strip` zones (search, selects, export). Fits `resource_index`, data tables, admin lists. |
| `chirpui/filter_chips.html` | `filter_group`, `filter_chip` | **Chip / pill** faceted navigation: `role="radiogroup"`, optional `resolve_color` / `register_colors`, HTMX `hx-target` / `hx-select`. Fits taxonomy toggles (e.g. Pokémon types), tag filters without a wrapping form. |
| `chirpui/chip_group.html` | `chip_group`, `chip` | **Display chips** for tags, facets, world traits, and compact metadata where a radiogroup/form contract would be too strong. |

#### filter_bar

Filter-first composite (`action_strip` + `form`) for searchable lists and tables.
Use the same inner zone classes as `action_strip`.

```html
{% from "chirpui/filter_bar.html" import filter_bar %}
{% from "chirpui/forms.html" import search_bar %}

{% call filter_bar("/skills", attrs_map={"id": "skills_filters"}) %}
  <div class="chirpui-action-strip__primary">
    {{ search_bar("q", variant="solo", placeholder="Search skills...") }}
  </div>
  <div class="chirpui-action-strip__controls">
    <select class="chirpui-field__input" name="role"><option>All</option></select>
  </div>
  <div class="chirpui-action-strip__actions">
    <button class="chirpui-btn chirpui-btn--secondary" type="submit">Export</button>
  </div>
{% end %}
```

#### filter_chips

Chip-style faceted filters: a `filter_group` wrapper (`role="radiogroup"`) and `filter_chip` pills that reuse badge styling and scoped `--chirpui-badge-color`. Pass semantic colors via `color=` after `chirp_ui.register_colors({...})`, or a literal hex/rgb string. Optional HTMX on each chip link.

```html
{% from "chirpui/filter_chips.html" import filter_group, filter_chip %}

{% call filter_group(name="Type", value=current_type) %}
  {{ filter_chip("All", href="/?q=" ~ search, active=not current_type,
      hx_target="#main", hx_push_url=true, hx_select="#main") }}
  {% for t in types %}
    {{ filter_chip(t, color=t, href="/?type=" ~ t ~ "&q=" ~ search,
        active=(current_type == t), hx_target="#main", hx_push_url=true, hx_select="#main") }}
  {% endfor %}
{% end %}
```

| Param | `filter_group` | `filter_chip` |
|-------|----------------|---------------|
| Core | `name` (→ `aria-label`), optional `cls` | `label`, `href`, `active`, `color`, `cls` |
| HTMX | — | `hx_target`, `hx_push_url`, `hx_swap`, `hx_select` |

See also: **Badge** (`color`, `fill`) and filters **`resolve_color`**, **`register_colors`** in `chirp_ui`.

#### chip_group

Display-only chip clusters for tags, facets, and compact metadata. Use
`filter_chips` when the chips are a single-choice filter control; use
`chip_group` when they are simple links or labels.

```html
{% from "chirpui/chip_group.html" import chip_group, chip %}

{% call chip_group(label="Traits") %}
  {{ chip("Urban", href="/facets/urban", color="#78c850") }}
  {{ chip("Quiet", muted=true) }}
{% end %}
```

#### command_bar

Action-first composite for command-heavy pages (bulk actions, create/export, workspace controls).
Use the same inner zone classes as `action_strip`.

```html
{% from "chirpui/command_bar.html" import command_bar %}
{% from "chirpui/button.html" import btn %}

{% call command_bar(surface_variant="default", density="sm") %}
  <div class="chirpui-action-strip__controls">
    {{ btn("Bulk edit", variant="default", size="sm") }}
  </div>
  <div class="chirpui-action-strip__actions">
    {{ btn("Create", variant="primary", size="sm") }}
  </div>
{% end %}
```

#### search_header

Search-first page header composite (`page_header` + `action_strip` + `search_bar`).
Pass optional controls in the default slot; the macro places them inside the controls zone for you.

```html
{% from "chirpui/search_header.html" import search_header %}
{% from "chirpui/button.html" import btn %}
{% call search_header("Skills", "/skills", query=q, subtitle="Search and filter skills") %}
  {{ btn("Sort", variant="default", size="sm") }}
  {{ btn("View", variant="default", size="sm") }}
{% end %}
```

#### resource_index

High-level browse/index composite that wraps `search_header`, optional `filter_bar`, optional `selection_bar`, optional filter/tray panel, and either results or an empty state.

```html
{% from "chirpui/resource_index.html" import resource_index %}
{% from "chirpui/card.html" import resource_card %}
{% call resource_index(
  "Skills",
  "/skills",
  query=q,
  subtitle="Browse installed skills",
  filter_action="/skills",
  filter_label="Tag filters",
  selected_count=selected_tags | length,
  has_results=skills | length > 0,
  results_layout="grid",
  results_cols=2
) %}
  {% slot toolbar_controls %}{{ btn("Filters", variant="default", size="sm") }}{% end %}
  {% slot selection %}<a class="chirpui-badge chirpui-badge--primary">python x</a>{% end %}
  {% for skill in skills %}
    {{ resource_card("/skill/" ~ skill.name, skill.name, description=skill.description or "—") }}
  {% end %}
{% end %}
```

| Param | Description |
|-------|-------------|
| `title`, `subtitle` | Discovery page header |
| `search_action`, `query`, `search_name` | Search form configuration |
| `filter_action` | Enables the filter bar when provided |
| `filter_label` | Leading summary label in the filter bar |
| `filter_state_name`, `filter_state_value` | Hidden state preserved through search submissions |
| `selected_count`, `selected_label`, `selected_aria_label` | Applied-filter/selection bar configuration |
| `results_layout` | `stack` or `grid` |
| `results_cols`, `results_gap` | Result wrapper layout options |
| `has_results`, `empty_title`, `empty_icon`, `empty_hint`, `empty_message` | Empty-state behavior |
| `mutation_result_id` | Optional. Id for a result div rendered at the start of the results block. Use when forms in the results target a mutation result; keeps target co-located. |

**Slots:** `toolbar_controls`, `filter_primary`, `filter_controls`, `filter_actions`, `selection`, `filters_panel`, default (results).

**Mutation targets:** If the default slot (results) loads via HTMX and contains forms that target a result div, use `mutation_result_id` or put that div **inside** the results content, not in `filters_panel`. Otherwise the target may be missing when the form fires.

#### selection_bar

Stateful bulk-actions bar shown when rows/items are selected. Renders nothing when `count <= 0`.

```html
{% from "chirpui/selection_bar.html" import selection_bar %}
{% call selection_bar(count=3, live_region=true) %}
  <a class="chirpui-btn chirpui-btn--sm chirpui-btn--secondary">Export selected</a>
  <a class="chirpui-btn chirpui-btn--sm chirpui-btn--secondary">Clear</a>
{% end %}
```

### config_card

Key-value card for settings. Icon in header, no media. Uses `description_list` with type-aware styling.

```html
{% from "chirpui/config_card.html" import config_card %}
{{ config_card(title="Logs", icon="⟳", items=[
    {"term": "retention_days", "detail": "14", "type": "number"},
    {"term": "enabled", "detail": "Yes", "type": "bool"},
]) }}
```

Item `type`: `bool` (badge), `url` (monospace+truncate), `number` (right-align), `unset` (muted italic).

Also accepts `cls`, `attrs`, and `attrs_map` — forwarded to `card` (use `attrs_map={"id": "…"}` for `hx-target` on the widget root).

### config_dashboard

Composite for full settings pages: page_header + key_value_form + grid of config_cards + action_strip. Slots: `header_actions`, `form_result`, `config_cards`, `action_strip`.

Spacing guidance:

- Put result fragments in `.chirpui-result-slot` or `.chirpui-result-slot--sm` instead of ad hoc margin utilities.
- Use `.chirpui-measure-sm|md|lg` on forms and narrow content blocks that need a maximum readable width.
- Prefer `stack()` or `cluster()` before adding inline `style="gap: ..."` overrides.

### metric_grid and metric_card

Use these for dashboard KPIs and overview decks instead of hand-assembling a grid of generic cards around `stat()`.

```html
{% from "chirpui/metric_grid.html" import metric_grid, metric_card %}
{% call metric_grid() %}
  {{ metric_card(value=128, label="Open tasks", icon="status", href="/tasks", hint="Assigned to your team") }}
  {{ metric_card(value="99.9%", label="Uptime", icon="status", trend="+0.2% this week") }}
{% end %}
```

| Macro | Param | Description |
|-------|-------|-------------|
| `metric_grid` | `cols`, `gap`, `cls` | Responsive wrapper for metric cards |
| `metric_card` | `value`, `label`, `icon` | Core KPI content |
| `metric_card` | `trend`, `hint` | Optional supporting context |
| `metric_card` | `href` | Optional clickable KPI destination |
| `metric_card` | `icon_bg`, `footer_label`, `footer_href`, `cls` | Icon badge tint, optional footer link, extra classes |
| `metric_card` | `attrs`, `attrs_map` | Forwarded to the outer `card` or `<a>` (e.g. `id` for HTMX) |

---

## Description List

### description_item type

| Type | Rendering |
|------|-----------|
| `bool` | Badge (success/muted) |
| `url` | Monospace, truncate |
| `number` | Right-align |
| `unset` | Muted italic |

### description_list compact

`compact=true` for tighter line-height and smaller terms.

### settings_row_list and settings_row

Three-column field set for setup targets, health checks, validation summaries. Use when you have label + status badge + detail (e.g. command or path).

```html
{% from "chirpui/settings_row.html" import settings_row_list, settings_row %}
{% call settings_row_list() %}
{{ settings_row("Cursor IDE", status="Configured", detail="dori setup cursor") }}
{{ settings_row("Skills directory", status="ok", detail="/path/to/skills") }}
{{ settings_row("Config", status="error", detail="File not found", status_variant="error") }}
{% end %}
```

| Param | Description |
|-------|-------------|
| `label` | Row label (left column) |
| `status` | Badge text (middle); variant inferred: ok/configured→success, error/issues→error, else muted |
| `detail` | Right column; always rendered in monospace (`chirpui-font-mono`) |
| `status_variant` | Override badge variant: success, error, muted, primary |

### install_snippet

Pre-formatted install command with copy-to-clipboard button. Replaces the pattern of inline Alpine + SVG duplicated across marketing pages.

```html
{% from "chirpui/code.html" import install_snippet %}
{{ install_snippet("uv add bengal-chirp") }}
{{ install_snippet("pip install kida-templates", label="pip", prompt="%") }}
```

| Param | Default | Description |
|-------|---------|-------------|
| `command` | *(required)* | Shell command text (auto-escaped in `data-copy-text`) |
| `label` | `"install"` | Small-caps label above the command; empty string hides it |
| `prompt` | `"$"` | Shell prompt prefix |
| `id` | `none` | Optional id on the `<pre>` element |
| `cls` | `""` | Extra classes on wrapper |

Uses `x-data="chirpuiCopy()"` — register via `Alpine.safeData` in your Chirp app.

### filter_row

Lightweight inline filter form for 2-3 controls. Use instead of `filter_bar` when you don't need the full action strip toolbar chrome.

```html
{% from "chirpui/filter_bar.html" import filter_row %}
{% call filter_row("/history/filter",
    attrs_map={"hx-target": "#results", "hx-swap": "innerHTML",
                "hx-trigger": "change delay:200ms from:input"}) %}
    <label for="f-skill">Skill</label>
    {{ text_field("skill", value=q, size="sm") }}
{% end %}
```

| Param | Default | Description |
|-------|---------|-------------|
| `action` | `none` | Form action URL; omit for JS-only forms |
| `method` | `"get"` | HTTP method |
| `attrs_map` | `none` | Dict of HTML/HTMX attributes (passed through `html_attrs`) |
| `gap` | `"sm"` | Cluster gap size |
| `cls` | `""` | Extra classes |

### tag_browse (tray + badges + actions)

Composite for the common tag-filtered listing pattern. Provides three macros designed to plug into `resource_index` slots.

```html
{% from "chirpui/tag_browse.html" import tag_browse_tray, tag_selection_badges, tag_filter_actions %}

{% slot filters_panel %}
{{ tag_browse_tray("my-filters", "Filter by tags", all_tags, selected_tags, tag_toggle_url, clear_url) }}
{% end %}
{% slot selection %}
{{ tag_selection_badges(selected_tags, tag_toggle_url, clear_url) }}
{% end %}
{% slot filter_actions %}
{{ tag_filter_actions(selected_tags, clear_url) }}
{% end %}
```

| Macro | Key Params | Description |
|-------|-----------|-------------|
| `tag_browse_tray` | `id`, `title`, `tags`, `selected_tags`, `tag_toggle_url`, `clear_url` | Slide-out tray with tag picker; selected tags get `badge--primary` |
| `tag_selection_badges` | `selected_tags`, `tag_toggle_url`, `clear_url` | Badge row of selected tags with remove (×) links |
| `tag_filter_actions` | `selected_tags`, `clear_url` | "Clear all" badge, hidden when no tags selected |

`tag_toggle_url` is a callable: `tag_toggle_url(tag) → URL string`. All links use `route_link_attrs` for boost-aware navigation.

### config_row_list and config_row_* (toggle, select, editable)

Two-column field set for config dashboards with interactive controls. Use inside `card` or `section` for editable config sections.

```html
{% from "chirpui/config_row.html" import config_row_list, config_row_toggle, config_row_select, config_row_editable %}
{% call config_row_list() %}
{{ config_row_toggle("acp.enabled", "ACP enabled", checked=config.acp.enabled,
    form_action="/config/set", attrs_map={"hx-post": "/config/set", "hx-target": "#result", "hx-swap": "innerHTML"}) }}
{{ config_row_select("logs.level", "Log level", options=[{"value": "info", "label": "Info"}, {"value": "debug", "label": "Debug"}],
    selected=config.logs.level, form_action="/config/set", attrs_map={...}) }}
{{ config_row_editable("endpoint", config.acp.endpoint, edit_url="/config/edit/acp.endpoint", swap_id="acp-endpoint") }}
{% end %}
```

| Macro | Param | Description |
|-------|-------|-------------|
| `config_row_list` | `cls` | Container grid; slot for rows |
| `config_row_toggle` | `name`, `label`, `checked` | Config key, label, initial state |
| `config_row_toggle` | `form_action`, `attrs_map` | When both set, wrap in HTMX form (submit on change) |
| `config_row_select` | `name`, `label`, `options`, `selected` | Options: `[{value, label}, ...]` |
| `config_row_select` | `form_action`, `attrs_map` | HTMX form wrapper when provided |
| `config_row_editable` | `term`, `value`, `edit_url` | Display + Edit trigger; edit_url handler returns `inline_edit_field_form` |
| `config_row_editable` | `swap_id`, `edit_label` | Swap target id; Edit button label |

Toggle with HTMX sends `key` + `value` (true/false). Select sends `key` + `value` (selected option). The edit_url handler returns `inline_edit_field_form` with save/cancel URLs.

---

## Spacing Utilities

These helpers exist for lightweight markup where a dedicated component would be overkill.

| Class | Purpose |
|-------|---------|
| `chirpui-flow` | Wrapping inline cluster utility |
| `chirpui-inline` | Non-wrapping inline group |
| `chirpui-measure-sm|md|lg` | Readable max-width utilities |
| `chirpui-result-slot` | Standard margin before streamed/results content |
| `chirpui-result-slot--sm` | Compact result spacing |
| `chirpui-placeholder-inline` | Inline placeholder row for loading/thinking states |

---

## OOB Helpers

`chirpui/oob.html` provides macros for composing htmx out-of-band swap fragments.

### `oob_fragment(id, swap, tag, cls)`

Wraps any block content with `hx-swap-oob`. Pairs with Chirp's `Fragment()` and `OOB()` returns.

```html
{% from "chirpui/oob.html" import oob_fragment %}
{% call oob_fragment("sidebar-stats", swap="innerHTML") %}
    <p>Updated stats</p>
{% end %}
```

| Param | Default | Description |
|-------|---------|-------------|
| `id` | — | Target element ID |
| `swap` | `"true"` | OOB swap strategy (`true` = outerHTML, `innerHTML`, `beforeend`, etc.) |
| `tag` | `"div"` | HTML tag for the wrapper |

### `oob_toast(message, variant, dismissible, container_id)`

Shorthand for sending a toast notification from any htmx response.

```html
{% from "chirpui/oob.html" import oob_toast %}
{{ oob_toast("Item saved!", variant="success") }}
```

### `counter_badge(id, count, variant, max_count, oob)`

Small numeric pill for notification counts, cart items, etc. Hidden when `count=0`.

```html
{% from "chirpui/oob.html" import counter_badge %}
{{ counter_badge("inbox-count", count=5) }}
{{ counter_badge("inbox-count", count=12, variant="danger", oob=true) }}
```

| Param | Default | Description |
|-------|---------|-------------|
| `id` | — | Element ID (OOB target) |
| `count` | `0` | Number to display |
| `variant` | `""` | `""`, `warning`, `danger` |
| `max_count` | `99` | Overflow threshold (displays `99+` above) |
| `oob` | `false` | Emit `hx-swap-oob="true"` |

---

## Suspense (Deferred Loading)

`chirpui/suspense.html` provides skeleton-to-content swap macros that pair with Chirp's `Suspense(defer_map={})` return type. The server renders the shell immediately, then sends deferred blocks as OOB swaps that replace the skeleton placeholders.

```jinja
{% from "chirpui/suspense.html" import suspense_slot, suspense_group %}

{# Default skeleton placeholder #}
{{ suspense_slot("user-profile") }}

{# Skeleton variant (card, text, etc.) #}
{{ suspense_slot("sidebar-nav", skeleton_variant="text", lines=5) }}

{# Custom placeholder via call block #}
{% call suspense_slot("dashboard-stats") %}
    <p>Loading stats...</p>
{% end %}

{# Group — marks parent busy until all slots resolve #}
{% call suspense_group() %}
    {{ suspense_slot("panel-a", skeleton_variant="card") }}
    {{ suspense_slot("panel-b", skeleton_variant="card") }}
{% end %}
```

### `suspense_slot`

| Param | Default | Description |
|-------|---------|-------------|
| `id` | *(required)* | Element ID — OOB swap target |
| `skeleton_variant` | `""` | Skeleton type (`"text"`, `"card"`, etc.) |
| `lines` | `1` | Line count for text skeleton |
| `width` | `none` | Custom skeleton width |
| `height` | `none` | Custom skeleton height |
| `cls` | `""` | Extra CSS classes |

When called without a `{% call %}` block and no `skeleton_variant`, renders a default block skeleton (`100%` × `3rem`).

### `suspense_group`

| Param | Default | Description |
|-------|---------|-------------|
| `cls` | `""` | Extra CSS classes |

Wraps child slots in a container with `aria-busy="true"`. Remove the group (or swap its content) once all deferred slots resolve.

**Provides:** `_suspense_busy = "true"` — child slots can consume this to coordinate rendering while the group is busy. Use `consume("_suspense_busy", "false")` in custom slot content to detect whether the slot is inside an active group.

---

## Navigation Progress

`chirpui/nav_progress.html` provides a CSS-only fixed progress bar at the top of the viewport. It animates automatically when htmx adds `htmx-request` to `<body>` during navigation requests. Use this in layouts that don't use `app_shell` (which has its own built-in loading bar).

```jinja
{% from "chirpui/nav_progress.html" import nav_progress %}

{{ nav_progress() }}
```

### `nav_progress`

| Param | Default | Description |
|-------|---------|-------------|
| `cls` | `""` | Extra CSS classes |

The bar is `position: fixed`, `z-index: 9999`, and uses `aria-hidden="true"` (purely decorative). It respects `prefers-reduced-motion` by skipping the animation and showing a static full-width bar instead.

---

## Streaming

`chirpui/streaming.html` provides components for LLM chat interfaces and SSE-driven UIs: message bubbles with role and state awareness, streaming blocks with animated cursors, copy buttons, and model cards.

```jinja
{% from "chirpui/streaming.html" import streaming_bubble, streaming_block, copy_btn, model_card %}

{# Basic assistant bubble with streaming cursor #}
{% call streaming_bubble() %}
    <p>Generating response...</p>
{% end %}

{# User message (no cursor) #}
{% call streaming_bubble(role="user", streaming=false) %}
    <p>What is the meaning of life?</p>
{% end %}

{# Thinking state — pulsing indicator + aria-busy #}
{% call streaming_bubble(state="thinking") %}{% end %}

{# Error state — alert semantics + error styling #}
{% call streaming_bubble(state="error", streaming=false) %}
    <p>Connection lost. Please retry.</p>
    {{ sse_retry("/api/stream/123") }}
{% end %}

{# SSE-connected bubble #}
{% call streaming_bubble(sse_connect="/api/stream/123") %}{% end %}
```

### `streaming_bubble`

| Param | Default | Description |
|-------|---------|-------------|
| `role` | `"assistant"` | Message role: `assistant`, `user`, `system`, `default` |
| `state` | `""` | State variant: `""` / `"content"` (default), `"thinking"`, `"error"` |
| `streaming` | `true` | Show animated cursor |
| `sse_swap_target` | `false` | Add `sse-swap` attributes to the inner block |
| `sse_connect` | `none` | SSE endpoint URL (adds `hx-ext="sse"` + `sse-connect`) |
| `sse_close` | `"done"` | SSE close event name |
| `cls` | `""` | Extra CSS classes |

**State variants:**

| `state` | CSS class | Aria | Visual |
|---------|-----------|------|--------|
| `""` / `"content"` | *(base)* | current behavior | Normal message body |
| `"thinking"` | `chirpui-streaming-bubble--thinking` | `aria-busy="true"` | Pulsing dots animation (replaces streaming cursor) |
| `"error"` | `chirpui-streaming-bubble--error` | `role="alert"` | Error border + background |

**Role-aware aria-label:** The `aria-label` is set per role — `"assistant response"`, `"user message"`, `"system message"`, or `"message"` for default.

**Provides:** `_streaming_role` — children in the slot can consume the bubble's role via `consume("_streaming_role", "assistant")`. Explicit params on children always win.

### `streaming_block`

| Param | Default | Description |
|-------|---------|-------------|
| `streaming` | `false` | Show animated cursor |
| `sse_swap_target` | `false` | Add `sse-swap` attributes |
| `cls` | `""` | Extra CSS classes |

Low-level streaming container with `aria-live="polite"`. Use `streaming_bubble` for message-level semantics; use `streaming_block` when you need just the cursor and live region without a message wrapper.

### `copy_btn`

| Param | Default | Description |
|-------|---------|-------------|
| `label` | `"Copy"` | Button text |
| `copy_text` | `""` | Text to copy to clipboard |
| `cls` | `""` | Extra CSS classes |

Clipboard copy button using Alpine.js. Shows "Copied!" feedback for 1.5s after click.

### `model_card`

| Param | Default | Description |
|-------|---------|-------------|
| `title` | *(required)* | Model name displayed in header |
| `badge` | `none` | Optional badge text (e.g. version label) |
| `footer` | `none` | Footer content (rendered as safe HTML) |
| `sse_connect` | `none` | SSE endpoint URL |
| `sse_close` | `"done"` | SSE close event name |
| `sse_streaming` | `false` | Wrap slot in active streaming block |
| `cls` | `""` | Extra CSS classes |

Card-style wrapper for model comparison UIs. When `sse_streaming=true`, the body gets an active streaming block with cursor and `sse-swap="fragment"`.

---

## SSE Status

`chirpui/sse_status.html` provides connection status indicators and retry controls for SSE-driven streaming UIs. Pair with `streaming_bubble`/`streaming_block` from `chirpui/streaming.html`.

```jinja
{% from "chirpui/sse_status.html" import sse_status, sse_retry %}

{# Connection indicator #}
{{ sse_status("connected") }}
{{ sse_status("error", label="Connection lost") }}

{# Retry button — re-fetches the SSE endpoint #}
{{ sse_retry("/api/stream/123") }}
{{ sse_retry("/api/stream/123", label="Reconnect", method="post") }}

{# Retry auto-disables when parent provides connected state #}
{% provide _sse_state = "connected" %}
    {{ sse_retry("/api/stream/123") }}  {# rendered with disabled + aria-disabled #}
{% end %}
```

### `sse_status`

| Param | Default | Description |
|-------|---------|-------------|
| `state` | `"connected"` | One of `connected`, `disconnected`, `error` |
| `label` | *(auto)* | Display text (defaults to state name) |
| `cls` | `""` | Extra CSS classes |

Renders a colored dot + label with `role="status"` and `aria-live="polite"`.

### `sse_retry`

| Param | Default | Description |
|-------|---------|-------------|
| `url` | *(required)* | SSE endpoint URL to re-fetch |
| `label` | `"Retry"` | Button text |
| `method` | `"get"` | htmx method (`get`, `post`) |
| `target` | `"closest [hx-ext]"` | htmx swap target |
| `swap` | `"outerHTML"` | htmx swap strategy |
| `cls` | `""` | Extra CSS classes |

Renders a small button (`chirpui-btn--sm`) that triggers an htmx request to reconnect. Uses Alpine.js for loading state feedback — shows "Retrying…" with `aria-busy` during the request.

**Consumes:** `_sse_state` — when a parent provides `_sse_state = "connected"`, the retry button renders with `disabled` and `aria-disabled="true"`. Use `{% provide _sse_state = "..." %}` to wrap SSE sections and coordinate retry availability.

---

## Form Accessibility

All field macros include built-in accessibility for validation:

| Feature | Attribute | Where |
|---------|-----------|-------|
| Field OOB target | `id="field-{name}"` | Wrapper div |
| Error description | `aria-describedby="errors-{name}"` | Input control |
| Error container | `id="errors-{name}" role="alert" aria-live="polite"` | Always in DOM |
| Invalid state | `aria-invalid="true"` | Input when errors present |

### `field_wrapper` params

| Param | Default | Description |
|-------|---------|-------------|
| `field_id` | `"field-{name}"` | Override wrapper ID (for repeated/nested fields) |
| `oob` | `false` | Emit `hx-swap-oob="true"` for per-field OOB validation |

### `form_error_summary(errors, id, oob)`

Alert-style error summary for form tops. Lists field count with anchor links to `#field-{name}`.

```html
{% from "chirpui/forms.html" import form_error_summary %}
{% call form("/save", hx_post="/save", hx_target="#my-form") %}
    {{ form_error_summary(errors) }}
    {{ text_field("email", errors=errors, label="Email") }}
{% end %}
```

| Param | Default | Description |
|-------|---------|-------------|
| `errors` | — | Dict of `{field_name: [messages]}` |
| `id` | `"form-errors"` | Element ID (OOB target) |
| `oob` | `false` | Emit `hx-swap-oob="true"` |

---

## Usage Notes

### HTMX Attributes (`build_hx_attrs`)

Components with htmx support (btn, form, tabs, etc.) accept named `hx_*` parameters directly. Internally, templates use `build_hx_attrs` to convert these to HTML attributes:

```html
{# Template author: use build_hx_attrs in macros instead of individual {% if hx_* %} blocks #}
{{ build_hx_attrs(hx_post="/save", hx_target="#result") | html_attrs }}
{# → hx-post="/save" hx-target="#result" #}
```

`build_hx_attrs` converts underscores to hyphens in keys (`hx_post` → `hx-post`). `None` values are preserved in the dict but skipped by `html_attrs`, so unset params produce no output. It is registered as a **template global** (called as a function, not a filter).

**Component consumers** use the named params directly — no need to call `build_hx_attrs`:

```html
{{ btn("Save", hx_post="/save", hx_target="#result") }}
{% call form("/items", hx_post="/items", hx_target="#list", hx_swap="innerHTML") %}
  ...
{% end %}
```

### Structured Attributes (recommended)

All core form/button helpers now support both:
- `attrs_map` for structured, escaped attributes (recommended),
- `attrs` for legacy raw strings (escape hatch).

```html
{{ btn("Save", attrs_map={"hx-post": "/save", "hx-target": "#result"}) }}
{% call form("/search", attrs_map={"id": "search_form", "hx-get": "/search", "hx-target": "#results"}) %}
  {{ search_bar("q", variant="with-button") }}
{% end %}
```

Forms with `hx-post`/`hx-put`/`hx-patch`/`hx-delete` (via params or `attrs_map`) reset on successful response by default. Use `hx_reset_on_success=false` to opt out. See [htmx reset user input](https://htmx.org/examples/reset-user-input/).

For forms with htmx, add `hx_sync="this:replace"` (or via `attrs_map`) to prevent double-submit. See [htmx synchronization](https://htmx.org/docs/#synchronization).

### BEM-based components (alert, badge)

These use the `bem` filter internally. Pass `variant` directly; validation runs automatically when strict mode is on.

```html
{% from "chirpui/alert.html" import alert %}
{% call alert(variant="success") %}Saved.{% end %}
```

### Inline-variant components (surface, hero, toast, etc.)

These use `validate_variant` at macro top. Invalid values fall back to the default and log a warning in strict mode.

```html
{% from "chirpui/surface.html" import surface %}
{% call surface(variant="muted") %}...{% end %}
{# Optional: style= (inline CSS; overrides variant background), attrs / attrs_map #}
{% call surface(variant="default", padding=false, full_width=true, style="background: …") %}…{% end %}

{% from "chirpui/toast.html" import toast %}
{{ toast("Done!", variant="success") }}
```

### Aura (dimensional halo)

Wrapper for **any** block: a blurred, token-driven chromatic layer sits **behind** the child (via `::before`); the slot renders inside `chirpui-aura__content` above it. Pair with `surface(variant="glass")` for marketing panels, cards, or bento cells. Does not consume the inner surface’s `::before`/`::after`, so `chirpui-surface--cornered` on the child still works.

```html
{% from "chirpui/aura.html" import aura %}
{% from "chirpui/surface.html" import surface %}
{% call aura(tone="accent", spread="md") %}
  {% call surface(variant="glass") %}…{% end %}
{% end %}
{% call aura(tone="warm", spread="lg", mirror=true) %}…{% end %}
```

`prefers-reduced-transparency` softens the effect in CSS.

Apps that already shipped a local halo (e.g. `::before` on a marketing wrapper) can delete that CSS and wrap the same content with `aura()` after upgrading to chirp-ui **0.3.1+**.

### Skeleton variant

Use `""` (empty) for the default block, or `avatar`, `text`, `card` for structured placeholders.

```html
{% from "chirpui/skeleton.html" import skeleton %}
{{ skeleton() }}
{{ skeleton(variant="avatar") }}
{{ skeleton(variant="text", lines=3) }}
```

### Progress bar

Both `variant` (color style) and `size` are validated.

```html
{% from "chirpui/progress.html" import progress_bar %}
{{ progress_bar(75, variant="gold", size="md") }}
```

### Bar chart

CSS-only horizontal bar chart. Items: `{label, value, href?}`. Optional `href` makes the label a link.

```html
{% from "chirpui/bar_chart.html" import bar_chart %}
{{ bar_chart(items=[{"label": "A", "value": 42}, {"label": "B", "value": 18}]) }}
{{ bar_chart(items=tag_counts, max=10, show_value=true, variant="gold") }}
```

### Donut chart

CSS-only donut using conic-gradient. For success rate, completion, etc.

- **text** — overrides center display (replaces the default percentage)
- **caption** — small text below the value (e.g. "Uptime", "Tasks")
- **label** — deprecated alias for `text` (backwards-compatible)

```html
{% from "chirpui/donut.html" import donut %}
{{ donut(value=75, max=100) }}
{{ donut(value=3, max=5, text="3/5", variant="success") }}
{{ donut(value=40, max=100, caption="Uptime") }}
```

---

## Sidebar

Sidebar navigation for dashboards and app shells. Use `sidebar`, `sidebar_section`, `sidebar_link`, and `sidebar_toggle` from `chirpui/sidebar.html`.

### Macros

| Macro | Params | Description |
|-------|--------|-------------|
| `sidebar` | `cls` | Container with header, nav, footer slots |
| `sidebar_section` | `title`, `collapsible`, `cls` | Section group; `collapsible=true` uses details/summary |
| `sidebar_link` | `href`, `label`, `icon`, `active`, `match`, `boost`, `cls`, `badge` | Nav link; `icon` recommended for collapsible mode; `badge` renders counts/status outside the label |
| `sidebar_toggle` | `cls` | Toggle button for icon-only collapsed state |

### Active state

Two approaches:

- **`match=`** (recommended) — Automatic path comparison using `current_path` from the template context. `match="exact"` activates when `current_path == href`. `match="prefix"` activates when `current_path` starts with `href` (or equals it). Chirp auto-injects `current_path` for `Template(...)` and `Page(...)` returns; no manual `nav=` threading needed.
- **`active=`** (explicit) — Pass a boolean directly. Use when active state depends on something other than the URL path (e.g. `active=is_admin`).

When `match=` is set, it takes precedence over `active=`. Both emit `aria-current="page"` on active links.

**Client-side sync:** `app_shell_layout.html` includes a built-in script that updates sidebar and navbar active classes after htmx history navigation (`htmx:pushedIntoHistory`, `htmx:replacedInHistory`). This covers the case where `hx-boost` swaps `#main` but leaves the sidebar DOM untouched.

### Usage

```html
{% from "chirpui/sidebar.html" import sidebar, sidebar_section, sidebar_link %}
{% call sidebar() %}
  {% call sidebar_section("Navigate") %}
    {{ sidebar_link("/", "Home", icon="◉", match="exact") }}
    {{ sidebar_link("/skills", "Skills", icon="✦", match="prefix", badge=3) }}
  {% end %}
  {% call sidebar_section("Settings") %}
    {{ sidebar_link("/settings", "Config", icon="◇", match="prefix") }}
  {% end %}
{% end %}
```

Legacy `active=` still works for backward compatibility:

```html
{{ sidebar_link("/admin", "Admin", icon="⚙", active=is_admin) }}
```

## Navigation and PBP Metadata

Use `primary_nav` for broad top-level app or section navigation. Use
`route_tabs` only for local views of one object/workspace; use `nav_tree` with
`branch_mode="linked"` for server-controlled site maps where parent nodes are
route links first.

```html
{% from "chirpui/primary_nav.html" import primary_nav %}

{{ primary_nav([
  {"label": "World", "href": "/world", "match": "prefix"},
  {"divider": true},
  {"label": "Inbox", "href": "/inbox", "badge": unread_count},
], current_path=current_path) }}
```

For compact forum/PBP metadata:

- `inline_counter(mark, value, label)` renders small count triples without folding the label into a string.
- `latest_line(label, href, title, actor=none, actor_href=none, meta=none, detail=none)` renders a latest-activity jump with optional tooltip detail.
- `linked_avatar_stack(items, max_visible=4, total=none)` renders cast/avatar faces as direct links while preserving the avatar-stack shape.
- `rendered_content(compact=false)` wraps rendered post/prose content without bypassing escaping; sanitize/mark safe upstream when content is already trusted.
- `composer_shell()` and `token_input()` provide authoring structure for app-owned editors and autocomplete. ChirpUI supplies the regions; the app owns the behavior.

### app_shell

Full-page shell with topbar, sidebar, and main content. Params: `brand`, `brand_url`, `sidebar_collapsible`, `topbar_variant`, `sidebar_variant`, `cls`.

Below `48rem`, `app_shell` collapses to a single-column layout and turns its
sidebar slot into a horizontally scrollable navigation strip. This keeps forum,
dashboard, and workspace pages from losing main-content width on phones while
preserving persistent navigation.

| Param | Valid values | Default |
|-------|--------------|---------|
| `topbar_variant` | default, glass, gradient | default |
| `sidebar_variant` | default, glass, muted | default |

Glass variants use `backdrop-filter`; gradient topbar uses `--chirpui-gradient-subtle`.

### Collapsible sidebar

Enable via `app_shell(sidebar_collapsible=true)`. `app_shell_layout.html` keeps the sidebar non-collapsible by default; use a custom shell if a layout-based app needs the collapsible variant. Collapsed mode shows icons only; provide `icon` for each `sidebar_link`.

### Tokens

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-sidebar-active-bg` | Active link background | 10% accent tint |
| `--chirpui-sidebar-active-color` | Active link text | `var(--chirpui-accent)` |
| `--chirpui-sidebar-section-gap` | Gap between sections | `var(--chirpui-spacing-md)` |
| `--chirpui-sidebar-link-gap` | Gap between links | `var(--chirpui-spacing-xs)` |
| `--chirpui-sidebar-collapsed-width` | Width when collapsed | `4rem` |

### Gradient tokens

| Token | Purpose |
|-------|---------|
| `--chirpui-gradient-subtle` | Subtle 135deg gradient (bg-subtle to accent tint) |
| `--chirpui-gradient-accent` | Accent gradient (light to darker accent) |
| `--chirpui-gradient-border` | Gradient for borders (accent to example) |
| `--chirpui-gradient-split` | Hard-stop 50/50 split (surface | bg-subtle) |
| `--chirpui-gradient-mesh` | Simulated mesh (radial overlays, BBC-style ambient) |

---

## Strict Mode

**With Chirp:** Strict mode follows `app.debug` by default. Override with `strict=True` or `strict=False`:

```python
from chirp import App, use_chirp_ui
import chirp_ui

app = App(...)
use_chirp_ui(app, prefix="/static", strict=True)   # always validate
use_chirp_ui(app, prefix="/static", strict=False)  # never validate
use_chirp_ui(app, prefix="/static")                # strict=app.debug (from chirp)
```

**Standalone (Kida only):** Call `chirp_ui.set_strict(True)` before rendering:

```python
import chirp_ui
chirp_ui.set_strict(True)
# ... render templates
```

Invalid icon names also log warnings (pass-through unchanged).

---

## Filters

- **`bem(block, variant="", modifier="", cls="")`** — Builds BEM class string; validates `variant` against `VARIANT_REGISTRY` when strict.
- **`icon(name)`** — Resolves icon name to glyph; validates against `ICON_REGISTRY` when strict.
- **`validate_variant(value, allowed, default="")`** — Returns `value` if in `allowed`, else `default`. Logs warning when strict and invalid.

For custom components with inline variants:

```html
{% set variant = variant | validate_variant(("a","b","c"), "a") %}
```

---

## Typography

chirp-ui uses separate **UI** and **Prose** typography scales. Override `--chirpui-ui-*` and `--chirpui-prose-*` tokens to tune component vs. document typography. See [docs/TYPOGRAPHY.md](TYPOGRAPHY.md) for token reference and override examples.

## Tokens, Motion, and Elevation

For the full token contract (tiering, theme precedence, motion, state, and elevation mapping), see [docs/TOKENS.md](TOKENS.md).

## Theme and Style Presets

chirp-ui uses a two-axis model:

- `data-theme="light|dark|system"` controls color mode.
- `data-style="default|neumorphic"` controls artistic preset.

Example:

```html
<html data-theme="system" data-style="neumorphic">
```

Runtime controls are available in `chirpui/theme_toggle.html`:

```html
{% from "chirpui/theme_toggle.html" import theme_toggle, style_toggle, style_select %}
{{ theme_toggle() }}
{{ style_toggle() }}
{{ style_select() }}
```

---

## Error Boundaries (kida ≥ 0.4.0)

Kida 0.4.0 adds native `{% try %}` / `{% fallback %}` blocks that catch render-time exceptions and provide fallback content instead of crashing the page.

### Syntax

```html
{% try %}
    {{ some_expression_that_might_fail }}
    {% slot %}
{% fallback error %}
    <p>Render error: {{ error.message }}</p>
{% end %}
```

The `error` variable is optional. When provided, it exposes: `message`, `type`, `template`, `line`.

### Where chirp-ui uses error boundaries

| Component | Fallback strategy |
|-----------|-------------------|
| `suspense_slot` | Default skeleton placeholder |
| `oob_fragment` | Empty content (OOB swap still arrives with correct `id`) |
| `streaming_bubble` / `streaming_block` | Error-state div with "Content unavailable" message |
| `safe_region` / `fragment_island` | Empty content (wrapper `div` with `id` preserved) |

### Tier guide for component authors

| Tier | When to use | Fallback pattern |
|------|-------------|-----------------|
| **OOB-critical** | OOB swaps, toasts, live regions | Empty content — the swap still lands, preventing stale UI |
| **Visible** | Suspense slots, loading states | Default skeleton — user sees a placeholder, not a crash |
| **Slot guards** | Arbitrary `{% slot %}` content | Omit the slot region — parent structure stays intact |

### When NOT to use error boundaries

- **Argument evaluation** — `{% try %}` only catches errors inside its body. If the caller passes `{{ toast(undefined_var.bad) }}`, the error happens at the call site, not inside the macro.
- **Development** — Consider leaving boundaries off in dev/test so errors surface immediately. Use `set_strict()` for this.

---

## Scoped Slots (kida ≥ 0.4.0)

Scoped slots let a component expose variables back to the caller's slot content — an inversion-of-control pattern where the parent decides how to render child-provided data.

### Syntax

**In the component (def)** — expose variables with `let:name=expr`:

```html
{% def data_list(items) %}
<ul>
    {% for item in items %}
    <li>{% slot row let:item=item, let:index=loop.index0 %}{{ item }}{% end %}</li>
    {% end %}
</ul>
{% end %}
```

**In the caller** — declare which bindings to receive with `let:name`:

```html
{% call data_list(items=users) %}
    {% slot row let:item, let:index %}
        <strong>{{ index + 1 }}.</strong> {{ item.name }}
    {% end %}
{% end %}
```

### When to use scoped slots vs provide/consume

| Pattern | Use when | Example |
|---------|----------|---------|
| **Scoped slots** | Parent needs data back from the child to template each item | Iterator components, render-prop patterns |
| **Provide/consume** | Deep context propagation across macro boundaries | Theme variant flowing from `card` → nested `alert`, form density flowing from `form` → `field_wrapper` |

chirp-ui currently uses provide/consume for all 33 context propagation sites. This is correct — those are deep cross-macro patterns, not parent-templates-child-data patterns. Scoped slots are available for future components (e.g. a `data_table` where the caller templates each row cell).

---

## Partial Evaluator (kida ≥ 0.4.0)

Kida 0.4.0 includes an opt-in two-phase partial evaluator that performs compile-time optimizations:

- **Constant folding** — static expressions reduced at compile time
- **Filter inlining** — pure built-in filters evaluated at compile time
- **Dead branch elimination** — `{% if false %}` blocks removed
- **Loop unrolling** — `{% for x in [1, 2, 3] %}` with static iterables expanded

### Enabling

The partial evaluator is controlled by the `Environment` constructor, which Chirp owns:

```python
from kida import Environment

env = Environment(
    loader=...,
    partial_eval=True,  # Enable compile-time optimization
)
```

chirp-ui templates are compatible with the partial evaluator but do not require it. No code changes are needed — the optimizer is transparent to template authors.

### When to enable

- **Production builds** — measurable render speedup for templates with static content
- **Development** — leave off (default) to keep compile times fast and error messages clear

---

## Marketing Kit

Components for full-page scroll sites — landing pages, docs homes, marketing sites. The marketing kit is the scrolling-page counterpart to `app_shell`: instead of a sidebar + fixed topbar, you get a sticky header, flowing content bands, and a footer.

### Imports

```html
{% from "chirpui/site_shell.html" import site_shell %}
{% from "chirpui/site_header.html" import site_header, site_nav_link %}
{% from "chirpui/site_footer.html" import site_footer, footer_column, footer_link %}
{% from "chirpui/band.html" import band %}
{% from "chirpui/feature_section.html" import feature_section, feature_stack %}
```

### Slot Reference

| Component | Slot | Purpose | Required? |
|-----------|------|---------|-----------|
| `site_shell` | `header` | Sticky top region (place `site_header` here) | No |
| `site_shell` | default | Page content | Yes |
| `site_shell` | `footer` | Footer region (place `site_footer` here) | No |
| `site_header` | `brand` | Logo / brand name (wrapped in `<a>`) | No |
| `site_header` | `nav` | Primary navigation links | No |
| `site_header` | `nav_end` | Right-side links when `layout="center-brand"` | No |
| `site_header` | `tools` | Utility buttons (theme toggle, CTA) | No |
| `site_footer` | `brand` | Footer brand / tagline | No |
| `site_footer` | default | Footer columns (`footer_column`) | No |
| `site_footer` | `rule` | Decorative divider between columns and colophon | No |
| `site_footer` | `colophon` | Copyright / fine print | No |
| `band` | `header` | Section header (e.g. `section_header()`) | No |
| `band` | default | Band content | Yes |
| `feature_section` | `eyebrow` | Small label above title | No |
| `feature_section` | `title` | Feature heading | No |
| `feature_section` | default | Body / description | Yes |
| `feature_section` | `actions` | CTA buttons | No |
| `feature_section` | `media` | Screenshot, code snippet, illustration | No |
| `feature_stack` | default | Consecutive `feature_section` calls | Yes |

### site_shell

Full-page scroll container. Creates an `isolation: isolate` stacking context so sticky headers always sit above content, regardless of child z-indices.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `ambient` | bool | `false` | Adds ambient glow background layer |
| `cls` | str | `""` | Extra CSS classes |

### site_header

Sticky top navigation bar with layout + surface axes.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `brand_url` | str | `"/"` | Brand link href |
| `layout` | str | `"start"` | `start`, `center-brand`, `center-nav`, `split` |
| `variant` | str | `"glass"` | `glass`, `solid`, `transparent` |
| `sticky` | bool | `true` | Sticky positioning |
| `current_path` | str | `""` | Current URL path for nav link active matching |
| `cls` | str | `""` | Extra CSS classes |

**Layout variants:**
- **`start`** — `[brand] [nav...] [spacer] [tools]` (default)
- **`center-brand`** — `[nav left] [brand] [nav right | tools]`
- **`center-nav`** — `[brand] [nav centered] [tools]`
- **`split`** — `[brand + nav] [spacer] [tools]`

**Surface variants:** `glass` (backdrop blur), `solid` (opaque), `transparent` (hero overlap)

### site_nav_link

Navigation link for use inside `site_header`'s `nav` slot. Reads `current_path` from the parent header via provide/consume.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `href` | str | required | Link destination |
| `label` | str | required | Display text |
| `glyph` | str | `""` | Prefix icon/emoji |
| `external` | bool | `false` | Adds `rel="noopener noreferrer"` |
| `match` | str | `""` | `"exact"` or `"prefix"` for active state |
| `active` | bool | `false` | Force active state |
| `cls` | str | `""` | Extra CSS classes |

### site_footer

Multi-section footer with brand, link columns, rule, and colophon.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `layout` | str | `"columns"` | `columns`, `centered`, `simple` |
| `cls` | str | `""` | Extra CSS classes |

**Layout variants:**
- **`columns`** — brand left + N link columns (fat footer)
- **`centered`** — stacked, center-aligned
- **`simple`** — single row: brand left, links right

### footer_column / footer_link

Sub-components for structuring `site_footer` content.

**`footer_column`**: `title` (str), `cls` (str). Default slot holds `footer_link` calls.

**`footer_link`**: `href` (str), `label` (str), `glyph` (str), `external` (bool), `cls` (str).

### band

Full-bleed marketing section panel with width control and pattern overlay.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | str | `"default"` | `default`, `elevated`, `accent`, `glass`, `gradient` |
| `width` | str | `"inset"` | `inset`, `bleed`, `contained` |
| `pattern` | str | `""` | Pattern overlay: `dots-sm`, `dots-md`, `grid`, `crosshatch`, `diag` |
| `cls` | str | `""` | Extra CSS classes |

**Width variants:** `inset` (rounded, slightly wider), `bleed` (viewport-wide bg), `contained` (no breakout)

### feature_section

Two-column copy + media grid for product features.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `layout` | str | `"split"` | `split`, `balanced`, `media-dominant`, `stacked` |
| `variant` | str | `"default"` | `default`, `muted`, `halo` |
| `reverse` | bool | `false` | Flip column order (zigzag patterns) |
| `cls` | str | `""` | Extra CSS classes |

**Layout variants:** `split` (55/45), `balanced` (50/50), `media-dominant` (40/60), `stacked` (single column)

**Surface variants:** `default` (transparent), `muted` (subtle bg), `halo` (glow behind media)

### feature_stack

Wrapper for consecutive `feature_section` calls with consistent vertical spacing.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cls` | str | `""` | Extra CSS classes |

### Bento Extensions

CSS-only extensions to existing `surface` and `frame` components for dashboard-style tile grids.

| Class | Purpose |
|-------|---------|
| `chirpui-surface--bento` | Hover lift + flex height equalization on surfaces |
| `chirpui-frame--bento` | Consistent gap and min-height for bento frames |
| `chirpui-block--wide` | Span 2 grid columns |
| `chirpui-block--tall` | Span 2 grid rows |
| `chirpui-surface__eyebrow` | Small-caps label above title |
| `chirpui-surface__title` | Large heading inside surface |
| `chirpui-surface__lede` | Subtitle / summary text |
| `chirpui-surface__body` | Body text region |

Use with `grid(preset="bento-211")` or custom CSS grid layouts. Pair `surface--bento` tiles inside a `frame--bento` for consistent dashboard aesthetics.

---

## When to Use: Decision Trees

### Overlays: modal vs tray vs drawer vs popover vs tooltip

1. **Does the user need to confirm or input data?**
   - Yes → Is it blocking (must respond before continuing)?
     - Yes → **`modal`** — centered dialog, focus-trapped, backdrop
     - No → **`tray`** — slide-out panel, page stays interactive
   - No → continue
2. **Is it persistent navigation or a tool panel?**
   - Yes → **`drawer`** — side panel with header/close, typically right-aligned
3. **Is it contextual info triggered by hover/focus on a specific element?**
   - Short text (1–2 lines) → **`tooltip`** — pure CSS, no interactivity inside
   - Rich content or interactive → **`popover`** — Alpine-powered, click to toggle
4. **Is it an overlay for media or preview?**
   - Yes → **`overlay`** — dark/gradient backdrop for fullscreen media

### Cards: card vs resource\_card vs config\_card vs metric\_card vs glow\_card

1. **Is it a CRUD resource with badges, subtitle, and list context?**
   - Yes → **`resource_card`** — has `badges`, `subtitle`, `footer` slots; use inside `resource_index`
2. **Is it a settings/config entry point?**
   - Yes → **`config_card`** — title + icon, links to config dashboard
3. **Is it a numeric KPI or metric?**
   - Yes → **`stat`** or **`animated_stat_card`** — value + label + optional trend
4. **Is it a marketing/hero decorative card?**
   - Yes → **`glow_card`** / **`spotlight_card`** — mouse-tracking effects, use inside hero sections
5. **General content container?**
   - Yes → **`card`** — flexible container with `header_actions`, `media`, `body_actions` slots

### Filters: filter\_bar vs filter\_chips vs filter\_row

1. **Is it a full toolbar with search + actions for a list/table?**
   - Yes → **`filter_bar`** — wraps `action_strip`, includes form structure
2. **Is it a set of togglable facet pills (e.g., status: active/inactive)?**
   - Yes → **`filter_chips`** — `filter_group` + `filter_chip`, HTMX-powered, supports `register_colors`
3. **Is it 2–3 inline controls inside a compact row?**
   - Yes → **`filter_row`** (from `filter_bar.html`) — lightweight cluster form with HTMX

### Layout: frame vs grid vs stack vs cluster vs block vs layer

1. **Do you need named column regions (hero + sidebar, content + aside)?**
   - Yes → **`frame`** — CSS grid with named areas, `preset=` for common ratios
2. **Do you need a repeating auto-fit grid of equal items?**
   - Yes → **`grid`** — CSS grid with `min=` column width, `preset=` for bento layouts
3. **Do you need vertical stacking with consistent gaps?**
   - Yes → **`stack`** — flexbox column, `gap=` for spacing
4. **Do you need horizontal wrapping items (tags, buttons, breadcrumbs)?**
   - Yes → **`cluster`** — flexbox row with wrap, `gap=` and `justify=`
5. **Do you need a single cell inside a grid that spans columns/rows?**
   - Yes → **`block`** — grid child with `span=` for bento cells
6. **Do you need overlapping layers (background + content + overlay)?**
   - Yes → **`layer`** — CSS grid stacking with `z-index` control

---

## Context Propagation Reference

Components use `{% provide %}` / `consume()` to pass state through slot boundaries without explicit props.

| Provider | Key | Consumers | Effect |
|----------|-----|-----------|--------|
| `surface` | `_surface_variant` | `badge`, `callout`, `divider`, `settings_row`, `status`, `timeline` | Child inherits surface variant for color-matching |
| `card` | `_card_variant` | `alert`, `badge`, `divider`, `settings_row` | Child inherits card variant |
| `hero_effects` | `_hero_variant` | `constellation`, `holy_light`, `meteor`, `particle_bg`, `rune_field`, `spotlight_card`, `symbol_rain` | Effect children match hero color scheme |
| `command_bar`, `filter_bar` | `_bar_density` | `button`, `icon_btn` | Buttons shrink to bar density |
| `command_bar`, `filter_bar` | `_bar_surface` | *(reserved)* | Surface variant for bar children |
| `suspense` | `_suspense_busy` | `button`, `icon_btn` | Buttons disable while slot is loading |
| `streaming` | `_streaming_role` | `copy_button` | Copy button adapts to streaming context |
| `forms` | `_form_density` | `forms` (field wrappers) | Fields inherit form density |
| `table` | `_table_align` | `table` (rows) | Row cells inherit column alignment |
| `accordion` | `_accordion_name` | `accordion` (items) | Items share radio-group name |
| `navbar` | `_nav_current_path` | `navbar` (links) | Links highlight when matching current path |
| `sidebar` | `_nav_current_path` | `sidebar` (links) | Same as navbar |
| `site_header` | `_site_nav_current_path` | `site_header` (links) | Marketing nav active state |

**Rule:** Explicit params always win over consumed values. Consuming a key that was never provided returns the default (usually `""`).

---

## All Components (A–Z)

Auto-generated reference for every chirp-ui template. See topic sections above for in-depth usage.

### accordion

**File:** `chirpui/accordion.html`

chirp-ui: Accordion component

**Macros:**
  - `accordion(name="accordion", cls="")`
  - `accordion_item(title, open=false, name="", cls="")`

**Context:** Provides: `_accordion_name`. Consumes: `_accordion_name`.


### action_bar

**File:** `chirpui/action_bar.html`

chirp-ui: Action Bar component

**Macros:**
  - `action_bar(cls="")`
  - `action_bar_item(icon, label, count=none, href=none, active=false, cls="")`


### animated_counter

**File:** `chirpui/animated_counter.html`

chirp-ui: Animated Counter

**Macros:**
  - `animated_counter(value, label="", prefix="", suffix="", variant="", cls="")`


### animated_stat_card

**File:** `chirpui/animated_stat_card.html`

chirp-ui: Animated Stat Card

**Macros:**
  - `animated_stat_card(value, label="", prefix="", suffix="", trend="", trend_direction="", effect="...)`


### app_layout

**File:** `chirpui/app_layout.html`

chirp-ui: App layout — extends chirp boost with CSS and toast.


### app_shell

**File:** `chirpui/app_shell.html`

chirp-ui: App Shell component

**Macros:**
  - `app_shell(brand="", brand_url="/", brand_slot=false, brand_boost=true, sidebar_collapsi...)`


### app_shell_layout

**File:** `chirpui/app_shell_layout.html`

chirp-ui: App shell layout — extends chirp shell with ChirpUI structure


### ascii_7seg

**File:** `chirpui/ascii_7seg.html`

chirp-ui: ASCII 7-Segment Display

**Macros:**
  - `ascii_7seg(text, label=none, variant="", cls="")`


### ascii_badge

**File:** `chirpui/ascii_badge.html`

chirp-ui: ASCII Badge

**Macros:**
  - `ascii_badge(text="", glyph="", variant="", frame="", cls="")`


### ascii_border

**File:** `chirpui/ascii_border.html`

chirp-ui: ASCII Border

**Macros:**
  - `ascii_border(variant="", glyph="", cls="")`


### ascii_breaker_panel

**File:** `chirpui/ascii_breaker_panel.html`

chirp-ui: ASCII Breaker Panel

**Macros:**
  - `breaker_panel(title=none, variant="double", size="", master=none, cls="")`
  - `breaker(name, label=none, checked=false, variant="", disabled=false)`


### ascii_card

**File:** `chirpui/ascii_card.html`

chirp-ui: ASCII Card

**Macros:**
  - `ascii_card(title=none, variant="", glyph="", cls="")`


### ascii_checkbox

**File:** `chirpui/ascii_checkbox.html`

chirp-ui: ASCII Checkbox

**Macros:**
  - `ascii_checkbox(name, label=none, checked=false, variant="", disabled=false, cls="")`
  - `ascii_checkbox_group(legend=none, cls="")`


### ascii_divider

**File:** `chirpui/ascii_divider.html`

chirp-ui: ASCII Divider

**Macros:**
  - `ascii_divider(glyph="", variant="", cls="")`


### ascii_empty

**File:** `chirpui/ascii_empty.html`

chirp-ui: ASCII Empty State component

**Macros:**
  - `ascii_empty(glyph="◇", heading="Nothing here", description="", variant="", cls="")`


### ascii_error

**File:** `chirpui/ascii_error.html`

chirp-ui: ASCII Error Page

**Macros:**
  - `ascii_error(code="404", heading="", description="", cls="")`


### ascii_fader

**File:** `chirpui/ascii_fader.html`

chirp-ui: ASCII Fader / Slider

**Macros:**
  - `ascii_fader(name, value=0, label=none, variant="", cls="")`
  - `fader_bank(title=none, cls="")`


### ascii_icon

**File:** `chirpui/ascii_icon.html`

chirp-ui: ASCII Icon component

**Macros:**
  - `ascii_icon(char, animation="none", size="md", cls="")`


### ascii_indicator

**File:** `chirpui/ascii_indicator.html`

chirp-ui: ASCII Indicator Light

**Macros:**
  - `indicator(label=none, variant="success", blink=false, glyph="square", cls="")`
  - `indicator_row(cls="", nowrap=false)`


### ascii_knob

**File:** `chirpui/ascii_knob.html`

chirp-ui: ASCII Knob / Rotary Selector

**Macros:**
  - `ascii_knob(name, options, selected=none, label=none, variant="", cls="")`


### ascii_modal

**File:** `chirpui/ascii_modal.html`

chirp-ui: ASCII Modal

**Macros:**
  - `ascii_modal(id, title=none, variant="", cls="")`
  - `ascii_modal_trigger(target, label="Open", cls="")`


### ascii_progress

**File:** `chirpui/ascii_progress.html`

chirp-ui: ASCII Progress

**Macros:**
  - `ascii_progress(value=0, label="", variant="", width=20, cls="")`


### ascii_radio

**File:** `chirpui/ascii_radio.html`

chirp-ui: ASCII Radio

**Macros:**
  - `ascii_radio(name, value, label=none, checked=false, disabled=false, cls="")`
  - `ascii_radio_group(name=none, legend=none, layout="vertical", variant="", cls="")`


### ascii_skeleton

**File:** `chirpui/ascii_skeleton.html`

chirp-ui: ASCII Skeleton

**Macros:**
  - `ascii_skeleton(variant="", lines=1, width="", cls="")`


### ascii_sparkline

**File:** `chirpui/ascii_sparkline.html`

chirp-ui: ASCII Sparkline

**Macros:**
  - `ascii_sparkline(values=[], variant="", cls="")`


### ascii_spinner

**File:** `chirpui/ascii_spinner.html`

chirp-ui: ASCII Spinner component

**Macros:**
  - `ascii_spinner(charset="braille", size="md", label="", cls="")`


### ascii_split_flap

**File:** `chirpui/ascii_split_flap.html`

chirp-ui: ASCII Split-Flap Display

**Macros:**
  - `split_flap(text, variant="", animate=true, cls="")`
  - `split_flap_row(cells, cls="")`
  - `split_flap_board(title=none, variant="", cls="")`


### ascii_stepper

**File:** `chirpui/ascii_stepper.html`

chirp-ui: ASCII Stepper

**Macros:**
  - `ascii_stepper(steps, current=0, variant="", cls="")`


### ascii_table

**File:** `chirpui/ascii_table.html`

chirp-ui: ASCII Table

**Macros:**
  - `ascii_table(headers=none, variant="single", align=none, compact=false, striped=false, sti...)`
  - `ascii_row(*cells, align=none)`


### ascii_tabs

**File:** `chirpui/ascii_tabs.html`

chirp-ui: ASCII Tabs

**Macros:**
  - `ascii_tabs(variant="", cls="")`
  - `ascii_tab(id, label, url=none, hx_target=none, hx_swap="innerHTML", active=false, cls="")`


### ascii_ticker

**File:** `chirpui/ascii_ticker.html`

chirp-ui: ASCII Ticker

**Macros:**
  - `ascii_ticker(text, variant="", speed="", cls="")`


### ascii_tile_btn

**File:** `chirpui/ascii_tile_btn.html`

chirp-ui: ASCII Tile Button

**Macros:**
  - `tile_btn(glyph="■", label=none, variant="", lit=false, toggle=false, name=none, disabl...)`
  - `tile_grid(cols=4, cls="")`


### ascii_toggle

**File:** `chirpui/ascii_toggle.html`

chirp-ui: ASCII Toggle

**Macros:**
  - `ascii_toggle(name, checked=false, label=none, variant="", size="", disabled=false, cls="")`
  - `ascii_switch(name, checked=false, label=none, variant="", size="", disabled=false, cls="")`


### ascii_vu_meter

**File:** `chirpui/ascii_vu_meter.html`

chirp-ui: ASCII VU Meter

**Macros:**
  - `ascii_vu_meter(name=none, value=0, label=none, variant="", width=20, peak=false, animate=fal...)`
  - `vu_meter_stack(title=none, cls="")`


### aurora

**File:** `chirpui/aurora.html`

chirp-ui: Aurora Background

**Macros:**
  - `aurora(variant="", cls="")`


### auth

**File:** `chirpui/auth.html`

chirp-ui: Auth form compositions

**Macros:**
  - `login_form(action="/login", username_name="username", password_name="password", csrf=non...)`
  - `signup_form(action="/signup", username_name="username", email_name="email", password_name...)`


### avatar

**File:** `chirpui/avatar.html`

chirp-ui: Avatar component

**Macros:**
  - `avatar(src=none, initials=none, alt="", size="md", status=none, cls="")`


### avatar_stack

**File:** `chirpui/avatar_stack.html`

chirp-ui: Avatar Stack component

**Macros:**
  - `avatar_stack(max_visible=4, total=none, cls="")`


### badge

**File:** `chirpui/badge.html`

chirp-ui: Badge component

**Macros:**
  - `badge(text, variant="primary", icon=none, cls="", color=none, fill="subtle", href=none)`

**Context:** Consumes: `_card_variant`, `_surface_variant`.


### bento_grid

**File:** `chirpui/bento_grid.html`

chirp-ui: Bento Grid

**Macros:**
  - `bento_grid(cols=3, cls="")`
  - `bento_item(span=none, span_row=false, cls="")`


### border_beam

**File:** `chirpui/border_beam.html`

chirp-ui: Border Beam

**Macros:**
  - `border_beam(variant="", cls="", attrs="", attrs_map=none)`


### breadcrumbs

**File:** `chirpui/breadcrumbs.html`

chirp-ui: Breadcrumbs component

**Macros:**
  - `breadcrumbs(items, cls="")`


### calendar

**File:** `chirpui/calendar.html`

chirp-ui: Calendar component

**Macros:**
  - `calendar(weeks, month_label, prev_url=none, next_url=none, cls="")`


### callout

**File:** `chirpui/callout.html`

chirp-ui: Callout component

**Macros:**
  - `callout(variant="info", title=none, icon=none, cls="")`

**Context:** Consumes: `_surface_variant`.


### carousel

**File:** `chirpui/carousel.html`

chirp-ui: Carousel component

**Macros:**
  - `carousel(variant="compact", slide_count=0, show_dots=false, cls="")`
  - `carousel_slide(id, cls="")`


### channel_card

**File:** `chirpui/channel_card.html`

chirp-ui: Channel Card component

**Macros:**
  - `channel_card(href, name, avatar_src=none, avatar_initials=none, subscribers=none, cls="", ...)`


### chapter_list

**File:** `chirpui/chapter_list.html`

chirp-ui: Chapter List component

**Macros:**
  - `chapter_list(summary="Chapters", open=false, cls="")`
  - `chapter_item(title, timestamp, href=none, cls="")`


### chat_input

**File:** `chirpui/chat_input.html`

chirp-ui: Chat Input component

**Macros:**
  - `chat_input(action="", name="message", placeholder="Type a message...", rows=2, maxlength...)`


### chat_layout

**File:** `chirpui/chat_layout.html`

chirp-ui: Chat Layout component

**Macros:**
  - `chat_layout(show_activity=false, cls="", fill=false)`


### collapse

**File:** `chirpui/collapse.html`

chirp-ui: Collapse component

**Macros:**
  - `collapse(trigger, open=false, cls="")`


### command_palette

**File:** `chirpui/command_palette.html`

chirp-ui: Command Palette component

**Macros:**
  - `command_palette(id="command-palette", search_url="/search", placeholder="Search...")`
  - `command_palette_trigger(target="command-palette", label="Search", cls="")`


### comment

**File:** `chirpui/comment.html`

chirp-ui: Comment component

**Macros:**
  - `comment(author, time=none, href=none, avatar_src=none, avatar_initials=none, replies_...)`
  - `comment_thread(cls="")`


### confetti

**File:** `chirpui/confetti.html`

chirp-ui: Confetti

**Macros:**
  - `confetti(count=40, event="confetti", cls="")`
  - `confetti_trigger(label, event="confetti", tag="button", cls="")`


### config_dashboard

**File:** `chirpui/config_dashboard.html`

chirp-ui: Config Dashboard composite

**Macros:**
  - `config_dashboard(title, subtitle=none, meta=none, breadcrumb_items=none, form_action=none, for...)`


### constellation

**File:** `chirpui/constellation.html`

chirp-ui: Constellation

**Macros:**
  - `constellation(density="", variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### conversation_item

**File:** `chirpui/conversation_item.html`

chirp-ui: Conversation Item component

**Macros:**
  - `conversation_item(href, name, preview, time=none, unread=none, muted=false, cls="")`


### conversation_list

**File:** `chirpui/conversation_list.html`

chirp-ui: Conversation List component

**Macros:**
  - `conversation_list(cls="")`


### copy_button

**File:** `chirpui/copy_button.html`

chirp-ui: Copy button

**Macros:**
  - `copy_button(text, label="Copy")`

**Context:** Consumes: `_streaming_role`.


### description_list

**File:** `chirpui/description_list.html`

chirp-ui: Description list component

**Macros:**
  - `description_list(items=none, variant="stacked", compact=false, relaxed=false, hoverable=false,...)`
  - `description_item(term, detail, type=none, icon=none, cls="")`


### divider

**File:** `chirpui/divider.html`

chirp-ui: Divider component

**Macros:**
  - `divider(text=none, horizontal=false, variant="", cls="")`

**Context:** Consumes: `_card_variant`, `_surface_variant`.


### dnd

**File:** `chirpui/dnd.html`

chirp-ui: Drag-drop primitives

**Macros:**
  - `dnd_list(cls="", attrs="")`
  - `dnd_item(cls="", attrs="")`
  - `dnd_handle(cls="", attrs="")`
  - `dnd_drop_indicator(cls="", attrs="")`
  - `dnd_board(cls="", attrs="")`
  - `dnd_column(title=none, cls="", attrs="")`
  - `dnd_card(cls="", attrs="")`


### dock

**File:** `chirpui/dock.html`

chirp-ui: Floating Dock

**Macros:**
  - `dock(items=none, variant="", size="", cls="")`


### drawer

**File:** `chirpui/drawer.html`

chirp-ui: Drawer component

**Macros:**
  - `drawer(id, title=none, side="right", cls="")`
  - `drawer_trigger(target, label="Open", cls="")`


### dropdown

**File:** `chirpui/dropdown.html`

chirp-ui: Dropdown component

**Macros:**
  - `dropdown(label, cls="")`


### dropdown_menu

**File:** `chirpui/dropdown_menu.html`

chirp-ui: Dropdown menu (items-based)

**Macros:**
  - `dropdown_menu(trigger, items, id="chirpui-dropdown")`
  - `dropdown_select(trigger_label, items, selected=none, id="chirpui-dropdown-select")`
  - `dropdown_split(primary_label, primary_href=none, primary_action=none, items=[], icon=none)`


### empty

**File:** `chirpui/empty.html`

chirp-ui: Empty State component

**Macros:**
  - `empty_state(icon=none, title="No items", illustration=none, action_label=none, action_hre...)`


### entity_header

**File:** `chirpui/entity_header.html`

chirp-ui: Entity header (dashboard-grade)

**Macros:**
  - `entity_header(title, meta=none, icon=none, cls="")`


### fragment_island

**File:** `chirpui/fragment_island.html`

chirp-ui: Safe region / Fragment island primitives

**Macros:**
  - `poll_trigger(url, target, delay=none, swap="innerHTML", select=none, cls="chirpui-sr-only"...)`
  - `safe_region(id, hx_target=none, hx_swap=none, hx_select=none, cls="", attrs="")`
  - `fragment_island(id, hx_target=none, hx_swap=none, hx_select=none, cls="", attrs="")`
  - `fragment_island_with_result(id, mutation_result_id, hx_target=none, hx_swap=none, hx_select=none, cls="",...)`


### glitch_text

**File:** `chirpui/glitch_text.html`

chirp-ui: Glitch Text Effect

**Macros:**
  - `glitch_text(text, variant="", tag="span", cls="")`


### glow_card

**File:** `chirpui/glow_card.html`

chirp-ui: Glow Card

**Macros:**
  - `glow_card(variant="", cls="", attrs="", attrs_map=none)`


### gradient_text

**File:** `chirpui/gradient_text.html`

chirp-ui: Gradient Text

**Macros:**
  - `gradient_text(text, animated=false, tag="span", cls="")`


### grain

**File:** `chirpui/grain.html`

chirp-ui: Grain Overlay

**Macros:**
  - `grain(variant="", animated=false, cls="", attrs="", attrs_map=none)`


### hero

**File:** `chirpui/hero.html`

chirp-ui: Hero component

**Macros:**
  - `hero(title=none, subtitle=none, background="solid", cls="")`
  - `page_hero(title=none, subtitle=none, variant="editorial", background="solid", cls="")`


### hero_effects

**File:** `chirpui/hero_effects.html`

chirp-ui: Hero Effects

**Macros:**
  - `hero_effects(effect="particles", variant="", cls="")`

**Context:** Provides: `_hero_variant`.


### holy_light

**File:** `chirpui/holy_light.html`

chirp-ui: Holy Light

**Macros:**
  - `holy_light(intensity="", variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### icon_btn

**File:** `chirpui/icon_btn.html`

chirp-ui: Icon Button

**Macros:**
  - `icon_btn(icon, variant="", size="", href=none, aria_label="", disabled=false, type="bu...)`

**Context:** Consumes: `_bar_density`, `_suspense_busy`.


### index_card

**File:** `chirpui/index_card.html`

chirp-ui: Index card component

**Macros:**
  - `index_card(href, title, description=none, badge=none, cls="")`


### infinite_scroll

**File:** `chirpui/infinite_scroll.html`

chirp-ui: Infinite Scroll component

**Macros:**
  - `infinite_scroll(load_url, target="this", swap="beforeend", loading_html=none, cls="")`


### islands

**File:** `chirpui/islands.html`

chirp-ui: Framework-agnostic island mount wrappers

**Macros:**
  - `island_root(name, props=none, mount_id=none, version="1", src=none, primitive=none, cls="...)`


### label_overline

**File:** `chirpui/label_overline.html`

chirp-ui: Small caps / overline label for cards and dense panels.

**Macros:**
  - `label_overline(text, section=false, tag="span", cls="")`


### link

**File:** `chirpui/link.html`

chirp-ui: Link component

**Macros:**
  - `link(text, href, external=false, cls="")`


### list

**File:** `chirpui/list.html`

chirp-ui: List component

**Macros:**
  - `list_group(items=none, linked=false, bordered=false, cls="")`
  - `list_item(cls="")`


### live_badge

**File:** `chirpui/live_badge.html`

chirp-ui: Live Badge component

**Macros:**
  - `live_badge(viewers=none, cls="")`


### marquee

**File:** `chirpui/marquee.html`

chirp-ui: Marquee

**Macros:**
  - `marquee(items=none, speed="", reverse=false, pause_on_hover=true, cls="")`


### media_object

**File:** `chirpui/media_object.html`

chirp-ui: Media Object layout primitive

**Macros:**
  - `media_object(align="start", cls="", use_slots=false)`
  - `media_object_media(cls="")`
  - `media_object_body(cls="")`
  - `media_object_actions(cls="")`


### mention

**File:** `chirpui/mention.html`

chirp-ui: Mention component

**Macros:**
  - `mention(username, href=none, cls="")`


### message_bubble

**File:** `chirpui/message_bubble.html`

chirp-ui: Message Bubble component

**Macros:**
  - `message_bubble(align="left", role="default", status=none, cls="")`


### message_thread

**File:** `chirpui/message_thread.html`

chirp-ui: Message Thread component

**Macros:**
  - `message_thread(cls="")`


### meteor

**File:** `chirpui/meteor.html`

chirp-ui: Meteor Effect

**Macros:**
  - `meteor(count=4, variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### modal

**File:** `chirpui/modal.html`

chirp-ui: Modal component

**Macros:**
  - `modal(id, title=none, size="md", cls="")`
  - `modal_trigger(target, label="Open", cls="")`


### modal_overlay

**File:** `chirpui/modal_overlay.html`

chirp-ui: Modal overlay (div-based, for apps that prefer overlay over native dialog)

**Macros:**
  - `modal_overlay_trigger(id, label, variant="", icon=none)`
  - `modal_overlay(id, title)`


### nav_link

**File:** `chirpui/nav_link.html`

chirp-ui: SPA-style link for content areas

**Macros:**
  - `nav_link(href, label="", cls="")`


### nav_tree

**File:** `chirpui/nav_tree.html`

chirp-ui: Nav tree component

Use `branch_mode="disclosure"` (the default) for docs/file-explorer sidebars
where branch rows are expand/collapse controls. Use `branch_mode="linked"` for
site-map or world-map navigation where parent locations are route links first;
in linked mode, child lists render only when the server marks the item
`open=true`.

Item shape: `{title, href?, children?, active?, open?, icon?, badge?, muted?}`.
`badge` renders in a separate count/status region, and `active`, `branch`,
`child`, `open`, and `muted` emit item-level state hooks for app overrides.

**Macros:**
  - `nav_tree_item_content(item, show_icons=false)`
  - `nav_tree(items, show_icons=false, branch_mode="disclosure", cls="")`
  - `nav_tree_items(items, show_icons, branch_mode="disclosure")`


### neon_text

**File:** `chirpui/neon_text.html`

chirp-ui: Neon Text

**Macros:**
  - `neon_text(text, color="cyan", animation="", tag="span", cls="")`


### notification_dot

**File:** `chirpui/notification_dot.html`

chirp-ui: Notification Dot

**Macros:**
  - `notification_dot(variant="", size="", count=none, cls="")`


### number_ticker

**File:** `chirpui/number_ticker.html`

chirp-ui: Number Ticker

**Macros:**
  - `number_ticker(value, variant="", size="", prefix="", suffix="", cls="")`


### orbit

**File:** `chirpui/orbit.html`

chirp-ui: Orbit

**Macros:**
  - `orbit(items=[], size="", speed="", reverse=false, cls="")`


### overlay

**File:** `chirpui/overlay.html`

chirp-ui: Overlay component

**Macros:**
  - `overlay(variant="dark", cls="")`


### pagination

**File:** `chirpui/pagination.html`

chirp-ui: Pagination component

**Macros:**
  - `pagination(current, total, url_pattern, hx_target=none, hx_push_url=false, hx_swap="inne...)`


### params_table

**File:** `chirpui/params_table.html`

chirp-ui: Params table component

**Macros:**
  - `params_table(rows, title=none, columns=none, cls="")`


### particle_bg

**File:** `chirpui/particle_bg.html`

chirp-ui: Particle Background

**Macros:**
  - `particle_bg(count=8, variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### playlist

**File:** `chirpui/playlist.html`

chirp-ui: Playlist component

**Macros:**
  - `playlist(title=none, cls="")`
  - `playlist_item(href, title, duration=none, active=false, cls="")`


### popover

**File:** `chirpui/popover.html`

chirp-ui: Popover component

**Macros:**
  - `popover(trigger_label, cls="")`


### post_card

**File:** `chirpui/post_card.html`

chirp-ui: Post Card component

**Macros:**
  - `post_card(name=none, handle=none, time=none, href=none, cls="")`
  - `post_card_header(name, handle=none, time=none, href=none, cls="")`
  - `post_card_body(cls="")`
  - `post_card_media(cls="")`
  - `post_card_actions(cls="")`


### profile_header

**File:** `chirpui/profile_header.html`

chirp-ui: Profile Header component

**Macros:**
  - `profile_header(name=none, cover_url=none, href=none, cls="", use_slots=false)`
  - `profile_header_avatar(cls="")`
  - `profile_header_info(name, href=none, cls="")`
  - `profile_header_stats(cls="")`
  - `profile_header_action(cls="")`


### pulsing_button

**File:** `chirpui/pulsing_button.html`

chirp-ui: Pulsing Button

**Macros:**
  - `pulsing_button(text, variant="", icon=none, href=none, cls="", type="button", disabled=false)`


### reaction_pill

**File:** `chirpui/reaction_pill.html`

chirp-ui: Reaction Pill component

**Macros:**
  - `reaction_pill(emoji, count=1, active=false, cls="")`
  - `message_reactions(cls="")`


### reveal_on_scroll

**File:** `chirpui/reveal_on_scroll.html`

chirp-ui: Reveal on scroll — animate content when it enters the viewport

**Macros:**
  - `reveal_on_scroll(cls="")`


### ripple_button

**File:** `chirpui/ripple_button.html`

chirp-ui: Ripple Button

**Macros:**
  - `ripple_button(text, variant="", size="", icon=none, cls="")`


### route_tabs

**File:** `chirpui/route_tabs.html`

chirp-ui: Route-backed subsection tabs

Use `route_tabs` for local views of one object, workspace, or subsection. For
broad cross-feature navigation, prefer `primary_nav`, `sidebar`, `nav_tree`, or
an app-level section tree so tab semantics do not imply a single local context.
Below `40rem`, route tabs become a horizontal scroll strip instead of wrapping
into several rows.

**Macros:**
  - `render_route_tabs(tab_items, current_path, target="#page-root", is_active=none)`
  - `route_tabs(tabs, current_path, target="#page-root", is_active=none)`


### rune_field

**File:** `chirpui/rune_field.html`

chirp-ui: Rune Field

**Macros:**
  - `rune_field(variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### scanline

**File:** `chirpui/scanline.html`

chirp-ui: Scanline Overlay

**Macros:**
  - `scanline(variant="", cls="")`


### segmented_control

**File:** `chirpui/segmented_control.html`

chirp-ui: Segmented Control

**Macros:**
  - `segmented_control(items, name="segmented", size="", cls="")`


### share_menu

**File:** `chirpui/share_menu.html`

chirp-ui: Share Menu component

**Macros:**
  - `share_menu(label="Share", share_url=none, cls="")`


### shell_frame

**File:** `chirpui/shell_frame.html`

chirp-ui: Shell frame primitives — persistent-region + swap-boundary contract

**Macros:**
  - `shell_outlet_attrs(target="#main", swap="innerHTML", select="#page-content")`
  - `shell_outlet(id="page-content", cls="", attrs="", include_boost_attrs=true, target="#main"...)`
  - `shell_region(id, cls="")`
  - `shell_runtime_script()`


### shimmer_button

**File:** `chirpui/shimmer_button.html`

chirp-ui: Shimmer Button

**Macros:**
  - `shimmer_button(text, variant="", size="", icon=none, href=none, cls="", type="button", attrs...)`


### signature

**File:** `chirpui/signature.html`

chirp-ui: Signature component

**Macros:**
  - `signature(text, language=none, cls="")`


### sortable_list

**File:** `chirpui/sortable_list.html`

chirp-ui: Sortable list macros

**Macros:**
  - `sortable_list(cls="", attrs="")`
  - `sortable_item(cls="", attrs="")`


### sparkle

**File:** `chirpui/sparkle.html`

chirp-ui: Sparkle

**Macros:**
  - `sparkle(count=6, variant="", cls="")`


### spinner

**File:** `chirpui/spinner.html`

chirp-ui: Spinner component

**Macros:**
  - `spinner(size="md", cls="")`
  - `spinner_thinking(size="md", cls="")`


### split_button

**File:** `chirpui/split_button.html`

chirp-ui: Split button component

**Macros:**
  - `split_button(primary_label, primary_href=none, primary_submit=false, variant="primary", cl...)`


### split_panel

**File:** `chirpui/split_panel.html`

chirp-ui: Split Panel

**Macros:**
  - `split_panel(direction="horizontal", default_split=50, min_split=10, max_split=90, cls="")`


### spotlight_card

**File:** `chirpui/spotlight_card.html`

chirp-ui: Spotlight Card

**Macros:**
  - `spotlight_card(variant="", cls="", attrs="", attrs_map=none)`

**Context:** Consumes: `_hero_variant`.


### stat

**File:** `chirpui/stat.html`

chirp-ui: Stat component

**Macros:**
  - `stat(value, label, icon=none, cls="")`


### state_primitives

**File:** `chirpui/state_primitives.html`

chirp-ui: No-build high-state primitive wrappers.

**Macros:**
  - `state_sync(state_key, query_param=none, initial="", mount_id=none, cls="")`
  - `action_queue(action_id, mount_id=none, cls="")`
  - `draft_store(draft_key, mount_id=none, cls="")`
  - `error_boundary(boundary_id, mount_id=none, cls="")`
  - `grid_state(state_key, columns, mount_id=none, cls="")`
  - `wizard_state(state_key, steps, mount_id=none, cls="")`
  - `upload_state(state_key, endpoint, mount_id=none, cls="")`


### status

**File:** `chirpui/status.html`

chirp-ui: Status Indicator component

**Macros:**
  - `status_indicator(label, variant="", icon=none, pulse=false, cls="", color=none)`

**Context:** Consumes: `_surface_variant`.


### status_with_hint

**File:** `chirpui/status_with_hint.html`

chirp-ui: Status with hint (badge + tooltip/popover)

**Macros:**
  - `status_with_hint(text, variant="primary", hint=none, icon=none, cls="")`


### stepper

**File:** `chirpui/stepper.html`

chirp-ui: Stepper component

**Macros:**
  - `stepper(steps, current=1, cls="")`


### symbol_rain

**File:** `chirpui/symbol_rain.html`

chirp-ui: Symbol Rain

**Macros:**
  - `symbol_rain(count=6, variant="", cls="")`

**Context:** Consumes: `_hero_variant`.


### tabbed_page_layout

**File:** `chirpui/tabbed_page_layout.html`

chirp-ui: Tabbed page layout macro

**Macros:**
  - `tabbed_page_layout(tab_items=none, tabs=none, current_path="/", tab_target="#page-root")`


### table

**File:** `chirpui/table.html`

chirp-ui: Table component

**Macros:**
  - `table(headers=none, rows=none, sortable=false, sort_url=none, hx_target=none, strip...)`
  - `row(*cells)`
  - `aligned_row(cells, align)`
  - `table_empty(message="No data available", icon="◇")`

**Context:** Provides: `_table_align`. Consumes: `_table_align`.


### tabs

**File:** `chirpui/tabs.html`

chirp-ui: Tabs component

**Macros:**
  - `tabs(active=none, cls="")`
  - `tab(id, label, url=none, hx_target=none, hx_swap="innerHTML", active=false, cls="")`


### tabs_panels

**File:** `chirpui/tabs_panels.html`

chirp-ui: Tab panels (button-based, client-side switching)

**Macros:**
  - `tab(id, label, active=false)`
  - `tab_panel(id, active=false)`
  - `tabs_container(active=none)`


### tag_input

**File:** `chirpui/tag_input.html`

chirp-ui: Tag input component

**Macros:**
  - `tag_input(name, tags=[], label=none, add_url=none, remove_url=none, placeholder="Add ta...)`


### text_reveal

**File:** `chirpui/text_reveal.html`

chirp-ui: Text Reveal

**Macros:**
  - `text_reveal(text, variant="", tag="span", cls="")`


### timeline

**File:** `chirpui/timeline.html`

chirp-ui: Timeline component

**Macros:**
  - `timeline(items=none, hoverable=false, cls="")`
  - `timeline_item(title, date, content=none, icon=none, avatar=none, variant="", time=none, hre...)`

**Context:** Consumes: `_surface_variant`.


### tooltip

**File:** `chirpui/tooltip.html`

chirp-ui: Tooltip macro

**Macros:**
  - `tooltip(content=none, hint=none, position="top", cls="")`


### tray

**File:** `chirpui/tray.html`

chirp-ui: Tray (slide-out panel)

**Macros:**
  - `tray_trigger(id, label, icon=none)`
  - `tray(id, title, position="right")`


### tree_view

**File:** `chirpui/tree_view.html`

chirp-ui: Tree view component

**Macros:**
  - `tree_view(nodes, cls="")`


### trending_tag

**File:** `chirpui/trending_tag.html`

chirp-ui: Trending Tag component

**Macros:**
  - `trending_tag(tag, href=none, count=none, trend=none, cls="")`


### typewriter

**File:** `chirpui/typewriter.html`

chirp-ui: Typewriter Effect

**Macros:**
  - `typewriter(text, speed="", cursor=true, delay="", tag="span", cls="")`


### typing_indicator

**File:** `chirpui/typing_indicator.html`

chirp-ui: Typing Indicator component

**Macros:**
  - `typing_indicator(cls="")`


### video_card

**File:** `chirpui/video_card.html`

chirp-ui: Video Card component

**Macros:**
  - `video_card(href, thumbnail, duration, title, channel=none, channel_href=none, views=none...)`


### video_thumbnail

**File:** `chirpui/video_thumbnail.html`

chirp-ui: Video Thumbnail component

**Macros:**
  - `video_thumbnail(href=none, src="", alt="", duration=none, watched_pct=none, cls="")`


### wizard_form

**File:** `chirpui/wizard_form.html`

chirp-ui: Wizard form component

**Macros:**
  - `wizard_form(id, steps, current=1, cls="", attrs="")`


### wobble

**File:** `chirpui/wobble.html`

chirp-ui: Wobble / Jello / Rubber-band / Bounce-in

**Macros:**
  - `wobble(trigger="load", cls="")`
  - `jello(trigger="load", cls="")`
  - `rubber_band(trigger="load", cls="")`
  - `bounce_in(cls="")`

---

<!-- chirpui:generated:start -->
## API Reference (generated)

> Generated from `src/chirp_ui/manifest.json` by `scripts/build_component_options.py`.
> Do not edit this section directly — edit the descriptor in `chirp_ui.components`
> or the template's `{#- chirp-ui: ... -#}` doc-block and re-run `poe build-docs`.
> Hand-authored narrative guides above are the source of truth for intent and
> idioms; this section is the projection of the registry for agent grounding.

**Maturity taxonomy:** `stable` = documented public surface suitable for normal app use;
`experimental` = public but still settling; `legacy` = supported compatibility surface
with a preferred replacement; `internal` = infrastructure for Chirp UI composition, not
recommended as an app-level building block.

**Authoring hints:** `preferred` = reach for this first in new app templates;
`available` = public surface, but not the first-choice composition vocabulary;
`compatibility` = retained for existing code or narrow escape hatches; `internal` =
not for app-level authoring.

### `accordion`

Accordion component

- **Template:** `chirpui/accordion.html`
- **Macro:** `accordion`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Provides:** `_accordion_name`

| Param | Required | Default |
|-------|----------|---------|
| `name` | no | (has default) |
| `cls` | no | (has default) |

### `action-bar`

Action Bar component

- **Template:** `chirpui/action_bar.html`
- **Macro:** `action_bar`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `action-strip`

Action Strip component

- **Template:** `chirpui/action_strip.html`
- **Macro:** `action_strip`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `collapse`, `scroll`, `sm`, `sticky`

| Param | Required | Default |
|-------|----------|---------|
| `surface_variant` | no | (has default) |
| `density` | no | (has default) |
| `wrap` | no | (has default) |
| `sticky` | no | (has default) |
| `role` | no | (has default) |
| `aria_label` | no | (has default) |
| `cls` | no | (has default) |

### `actions`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `alert`

Alert component

- **Template:** `chirpui/alert.html`
- **Macro:** `alert`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`, `actions`, `header_actions`
- **Variants:** `error`, `info`, `success`, `warning`
- **Consumes:** `_card_variant`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `dismissible` | no | (has default) |
| `icon` | no | (has default) |
| `title` | no | (has default) |
| `cls` | no | (has default) |
| `collapsible` | no | (has default) |
| `open` | no | (has default) |

### `ambient`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ambient-root`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `animated-counter`

Animated Counter

- **Template:** `chirpui/animated_counter.html`
- **Macro:** `animated_counter`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `default`, `mono`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `label` | no | (has default) |
| `prefix` | no | (has default) |
| `suffix` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `animated-stat-card`

Animated Stat Card

- **Template:** `chirpui/animated_stat_card.html`
- **Macro:** `animated_stat_card`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `label` | no | (has default) |
| `prefix` | no | (has default) |
| `suffix` | no | (has default) |
| `trend` | no | (has default) |
| `trend_direction` | no | (has default) |
| `effect` | no | (has default) |
| `cls` | no | (has default) |

### `answer-card`

Forum and social pattern assets

- **Template:** `chirpui/forum_patterns.html`
- **Macro:** `answer_card`
- **Category:** `social`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header_actions`
- **Composes:** `badge`, `btn`, `card`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `accepted` | no | (has default) |
| `closed` | no | (has default) |
| `author` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `(default)` | `card` | `(default)` |

### `app-shell`

App Shell component

- **Template:** `chirpui/app_shell.html`
- **Macro:** `app_shell`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`, `htmx`
- **Slots:** `(default)`, `brand`, `sidebar`, `topbar`, `topbar_end`
- **Modifiers:** `sidebar-collapsed`, `sidebar-collapsible`

| Param | Required | Default |
|-------|----------|---------|
| `brand` | no | (has default) |
| `brand_url` | no | (has default) |
| `brand_slot` | no | (has default) |
| `brand_boost` | no | (has default) |
| `sidebar_collapsible` | no | (has default) |
| `topbar_variant` | no | (has default) |
| `sidebar_variant` | no | (has default) |
| `shell_actions` | no | (has default) |
| `cls` | no | (has default) |

### `ascii`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-7seg`

ASCII 7-Segment Display

- **Template:** `chirpui/ascii_7seg.html`
- **Macro:** `ascii_7seg`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `error`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-badge`

ASCII Badge

- **Template:** `chirpui/ascii_badge.html`
- **Macro:** `ascii_badge`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `error`, `muted`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `text` | no | (has default) |
| `glyph` | no | (has default) |
| `variant` | no | (has default) |
| `frame` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-border`

ASCII Border

- **Template:** `chirpui/ascii_border.html`
- **Macro:** `ascii_border`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `double`, `heavy`, `rounded`, `single`, `spin`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `glyph` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-breaker-panel`

ASCII Breaker Panel

- **Template:** `chirpui/ascii_breaker_panel.html`
- **Macro:** `breaker_panel`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `sm`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `master` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-card`

ASCII Card

- **Template:** `chirpui/ascii_card.html`
- **Macro:** `ascii_card`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `double`, `heavy`, `rounded`, `single`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `variant` | no | (has default) |
| `glyph` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-checkbox`

ASCII Checkbox

- **Template:** `chirpui/ascii_checkbox.html`
- **Macro:** `ascii_checkbox`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `default`, `success`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `label` | no | (has default) |
| `checked` | no | (has default) |
| `variant` | no | (has default) |
| `disabled` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-checkbox-group`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-divider`

ASCII Divider

- **Template:** `chirpui/ascii_divider.html`
- **Macro:** `ascii_divider`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `dots`, `double`, `heavy`, `single`, `spin`, `spin-drift`, `spin-reverse`

| Param | Required | Default |
|-------|----------|---------|
| `glyph` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-empty`

ASCII Empty State component

- **Template:** `chirpui/ascii_empty.html`
- **Macro:** `ascii_empty`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `muted`

| Param | Required | Default |
|-------|----------|---------|
| `glyph` | no | (has default) |
| `heading` | no | (has default) |
| `description` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-error`

ASCII Error Page

- **Template:** `chirpui/ascii_error.html`
- **Macro:** `ascii_error`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `code` | no | (has default) |
| `heading` | no | (has default) |
| `description` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-fader`

ASCII Fader / Slider

- **Template:** `chirpui/ascii_fader.html`
- **Macro:** `ascii_fader`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `default`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `value` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-fader-bank`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-fill`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-fill-hover`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-indicator`

ASCII Indicator Light

- **Template:** `chirpui/ascii_indicator.html`
- **Macro:** `indicator`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `accent`, `error`, `muted`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `blink` | no | (has default) |
| `glyph` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-indicator-row`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-knob`

ASCII Knob / Rotary Selector

- **Template:** `chirpui/ascii_knob.html`
- **Macro:** `ascii_knob`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `options` | yes | — |
| `selected` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-modal`

ASCII Modal

- **Template:** `chirpui/ascii_modal.html`
- **Macro:** `ascii_modal`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`
- **Variants:** `(default)`, `double`, `heavy`, `single`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-modal-trigger`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-progress`

ASCII Progress

- **Template:** `chirpui/ascii_progress.html`
- **Macro:** `ascii_progress`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `value` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `width` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-radio`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-radio-group`

ASCII Radio

- **Template:** `chirpui/ascii_radio.html`
- **Macro:** `ascii_radio_group`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `name` | no | (has default) |
| `legend` | no | (has default) |
| `layout` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-skeleton`

ASCII Skeleton

- **Template:** `chirpui/ascii_skeleton.html`
- **Macro:** `ascii_skeleton`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `avatar`, `card`, `heading`, `text`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `lines` | no | (has default) |
| `width` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-sparkline`

ASCII Sparkline

- **Template:** `chirpui/ascii_sparkline.html`
- **Macro:** `ascii_sparkline`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `gradient`, `muted`

| Param | Required | Default |
|-------|----------|---------|
| `values` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-spinner`

ASCII Spinner component

- **Template:** `chirpui/ascii_spinner.html`
- **Macro:** `ascii_spinner`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `arrows`, `blocks`, `box`, `braille`, `dots`

| Param | Required | Default |
|-------|----------|---------|
| `charset` | no | (has default) |
| `size` | no | (has default) |
| `label` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-stepper`

ASCII Stepper

- **Template:** `chirpui/ascii_stepper.html`
- **Macro:** `ascii_stepper`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `success`

| Param | Required | Default |
|-------|----------|---------|
| `steps` | yes | — |
| `current` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-switch`

ASCII Toggle

- **Template:** `chirpui/ascii_toggle.html`
- **Macro:** `ascii_switch`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `default`, `success`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `checked` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `disabled` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-tab`

ASCII Tabs

- **Template:** `chirpui/ascii_tabs.html`
- **Macro:** `ascii_tab`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Variants:** `(default)`, `accent`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `label` | yes | — |
| `url` | no | (has default) |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-table`

ASCII Table

- **Template:** `chirpui/ascii_table.html`
- **Macro:** `ascii_table`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `double`, `heavy`, `rounded`, `single`

| Param | Required | Default |
|-------|----------|---------|
| `headers` | no | (has default) |
| `variant` | no | (has default) |
| `align` | no | (has default) |
| `compact` | no | (has default) |
| `striped` | no | (has default) |
| `sticky_header` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-tabs`

ASCII Tabs

- **Template:** `chirpui/ascii_tabs.html`
- **Macro:** `ascii_tabs`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-ticker`

ASCII Ticker

- **Template:** `chirpui/ascii_ticker.html`
- **Macro:** `ascii_ticker`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `error`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `speed` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-tile-btn`

ASCII Tile Button

- **Template:** `chirpui/ascii_tile_btn.html`
- **Macro:** `tile_btn`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `default`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `glyph` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `lit` | no | (has default) |
| `toggle` | no | (has default) |
| `name` | no | (has default) |
| `disabled` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-tile-grid`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `ascii-toggle`

ASCII Toggle

- **Template:** `chirpui/ascii_toggle.html`
- **Macro:** `ascii_toggle`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `default`, `success`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `checked` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `disabled` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-vu`

ASCII VU Meter

- **Template:** `chirpui/ascii_vu_meter.html`
- **Macro:** `ascii_vu_meter`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `default`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `name` | no | (has default) |
| `value` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `width` | no | (has default) |
| `peak` | no | (has default) |
| `animate` | no | (has default) |
| `cls` | no | (has default) |

### `ascii-vu-stack`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `aura`

Aura — chromatic halo behind stacked content (glass surfaces, cards, etc.)

- **Template:** `chirpui/aura.html`
- **Macro:** `aura`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Sizes:** `lg`, `md`, `sm`
- **Modifiers:** `mirror`

| Param | Required | Default |
|-------|----------|---------|
| `tone` | no | (has default) |
| `spread` | no | (has default) |
| `mirror` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `aura_tone`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `accent`, `cool`, `muted`, `primary`, `warm`

### `aurora`

Aurora Background

- **Template:** `chirpui/aurora.html`
- **Macro:** `aurora`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `intense`, `subtle`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `avatar`

Avatar component

- **Template:** `chirpui/avatar.html`
- **Macro:** `avatar`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Sizes:** `(default)`, `lg`, `sm`
- **Modifiers:** `offline`, `online`

| Param | Required | Default |
|-------|----------|---------|
| `src` | no | (has default) |
| `initials` | no | (has default) |
| `alt` | no | (has default) |
| `size` | no | (has default) |
| `status` | no | (has default) |
| `decorative` | no | (has default) |
| `cls` | no | (has default) |

### `avatar-stack`

Avatar Stack component

- **Template:** `chirpui/avatar_stack.html`
- **Macro:** `avatar_stack`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `max_visible` | no | (has default) |
| `total` | no | (has default) |
| `cls` | no | (has default) |

### `badge`

Badge component

- **Template:** `chirpui/badge.html`
- **Macro:** `badge`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `custom`, `custom-solid`, `error`, `info`, `muted`, `primary`, `success`, `warning`
- **Consumes:** `_card_variant`, `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `icon` | no | (has default) |
| `cls` | no | (has default) |
| `color` | no | (has default) |
| `fill` | no | (has default) |
| `href` | no | (has default) |

### `band`

Band component

- **Template:** `chirpui/band.html`
- **Macro:** `band`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header`
- **Variants:** `accent`, `default`, `elevated`, `glass`, `gradient`
- **Modifiers:** `bleed`, `contained`, `inset`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `width` | no | (has default) |
| `pattern` | no | (has default) |
| `cls` | no | (has default) |

### `bar-chart`

Bar Chart component

- **Template:** `chirpui/bar_chart.html`
- **Macro:** `bar_chart`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `gold`, `muted`, `radiant`, `success`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `max` | no | (has default) |
| `show_value` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `bento`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `bg-pattern`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `blade`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `block`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `border-beam`

Border Beam

- **Template:** `chirpui/border_beam.html`
- **Macro:** `border_beam`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `success`, `warning`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `bounce-in`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `breadcrumbs`

Breadcrumbs component

- **Template:** `chirpui/breadcrumbs.html`
- **Macro:** `breadcrumbs`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `cls` | no | (has default) |

### `btn`

Button component. Use chirpui-btn with variants. Supports loading state for htmx.

- **Template:** `chirpui/button.html`
- **Macro:** `btn`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`
- **Variants:** `(default)`, `danger`, `ghost`, `primary`, `success`, `warning`
- **Sizes:** `(default)`, `lg`, `md`, `sm`
- **Modifiers:** `loading`
- **Consumes:** `_bar_density`, `_suspense_busy`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `loading` | no | (has default) |
| `type` | no | (has default) |
| `href` | no | (has default) |
| `icon` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |
| `hx` | no | (has default) |
| `hx_get` | no | (has default) |
| `hx_post` | no | (has default) |
| `hx_put` | no | (has default) |
| `hx_patch` | no | (has default) |
| `hx_delete` | no | (has default) |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |
| `hx_trigger` | no | (has default) |
| `hx_include` | no | (has default) |
| `hx_select` | no | (has default) |
| `hx_ext` | no | (has default) |
| `hx_vals` | no | (has default) |
| `disabled` | no | (has default) |
| `data_action` | no | (has default) |
| `aria_label` | no | (has default) |

### `btn-group`

- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `bulk-bar`

- **Category:** `control`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `calendar`

Calendar component

- **Template:** `chirpui/calendar.html`
- **Macro:** `calendar`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `weeks` | yes | — |
| `month_label` | yes | — |
| `prev_url` | no | (has default) |
| `next_url` | no | (has default) |
| `cls` | no | (has default) |

### `callout`

Callout component

- **Template:** `chirpui/callout.html`
- **Macro:** `callout`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header_actions`
- **Modifiers:** `error`, `info`, `neutral`, `on-accent`, `on-muted`, `success`, `warning`
- **Consumes:** `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `title` | no | (has default) |
| `icon` | no | (has default) |
| `cls` | no | (has default) |

### `card`

Card component

- **Template:** `chirpui/card.html`
- **Macro:** `card`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `body_actions`, `footer`, `header_actions`, `media`
- **Modifiers:** `collapsible`, `gradient-border`, `gradient-header`, `hoverable`, `link`, `linked`
- **Provides:** `_card_variant`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `footer` | no | (has default) |
| `collapsible` | no | (has default) |
| `open` | no | (has default) |
| `variant` | no | (has default) |
| `icon` | no | (has default) |
| `border_variant` | no | (has default) |
| `header_variant` | no | (has default) |
| `cls` | no | (has default) |
| `hoverable` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `carousel`

Carousel component

- **Template:** `chirpui/carousel.html`
- **Macro:** `carousel`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `compact`, `page`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `slide_count` | no | (has default) |
| `show_dots` | no | (has default) |
| `cls` | no | (has default) |

### `catalog-rail`

Media pattern assets

- **Template:** `chirpui/media_patterns.html`
- **Macro:** `catalog_rail`
- **Category:** `media`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `actions`
- **Composes:** `carousel`, `title-card`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `items` | yes | — |
| `subtitle` | no | (has default) |
| `artwork` | no | (has default) |
| `variant` | no | (has default) |
| `show_dots` | no | (has default) |
| `cls` | no | (has default) |

### `channel-card`

Channel Card component

- **Template:** `chirpui/channel_card.html`
- **Macro:** `channel_card`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `body`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `name` | yes | — |
| `avatar_src` | no | (has default) |
| `avatar_initials` | no | (has default) |
| `subscribers` | no | (has default) |
| `cls` | no | (has default) |
| `use_slots` | no | (has default) |

### `chapter-item`

Chapter List component

- **Template:** `chirpui/chapter_list.html`
- **Macro:** `chapter_item`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `timestamp` | yes | — |
| `href` | no | (has default) |
| `cls` | no | (has default) |

### `chapter-list`

Chapter List component

- **Template:** `chirpui/chapter_list.html`
- **Macro:** `chapter_list`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `summary_actions`

| Param | Required | Default |
|-------|----------|---------|
| `summary` | no | (has default) |
| `open` | no | (has default) |
| `cls` | no | (has default) |

### `chat-input`

Chat Input component

- **Template:** `chirpui/chat_input.html`
- **Macro:** `chat_input`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `action` | no | (has default) |
| `name` | no | (has default) |
| `placeholder` | no | (has default) |
| `rows` | no | (has default) |
| `maxlength` | no | (has default) |
| `cls` | no | (has default) |

### `chat-layout`

Chat Layout component

- **Template:** `chirpui/chat_layout.html`
- **Macro:** `chat_layout`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `activity`, `input`, `messages`
- **Modifiers:** `fill`

| Param | Required | Default |
|-------|----------|---------|
| `show_activity` | no | (has default) |
| `cls` | no | (has default) |
| `fill` | no | (has default) |

### `children`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `chip`

Chip group

- **Template:** `chirpui/chip_group.html`
- **Macro:** `chip`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `custom`, `muted`, `selected`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `href` | no | (has default) |
| `selected` | no | (has default) |
| `muted` | no | (has default) |
| `color` | no | (has default) |
| `cls` | no | (has default) |

### `chip-group`

Chip group

- **Template:** `chirpui/chip_group.html`
- **Macro:** `chip_group`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `label` | no | (has default) |
| `cls` | no | (has default) |

### `clamp-2`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `clamp-3`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `click-jello`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `click-wobble`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `cluster`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `code`

- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `code-block`

- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `code-block-wrapper`

- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `collapse`

Collapse component

- **Template:** `chirpui/collapse.html`
- **Macro:** `collapse`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header_actions`

| Param | Required | Default |
|-------|----------|---------|
| `trigger` | yes | — |
| `open` | no | (has default) |
| `cls` | no | (has default) |

### `command-bar`

- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `command-palette`

Command Palette component

- **Template:** `chirpui/command_palette.html`
- **Macro:** `command_palette`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`, `htmx`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `id` | no | (has default) |
| `search_url` | no | (has default) |
| `placeholder` | no | (has default) |

### `comment`

Comment component

- **Template:** `chirpui/comment.html`
- **Macro:** `comment`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`

| Param | Required | Default |
|-------|----------|---------|
| `author` | yes | — |
| `time` | no | (has default) |
| `href` | no | (has default) |
| `avatar_src` | no | (has default) |
| `avatar_initials` | no | (has default) |
| `replies_url` | no | (has default) |
| `replies_count` | no | (has default) |
| `cls` | no | (has default) |

### `comment-thread`

- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `composer-shell`

Composer shell

- **Template:** `chirpui/composer_shell.html`
- **Macro:** `composer_shell`
- **Category:** `form`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`, `body`, `fields`, `header`, `identity`, `preview`, `status`, `toolbar`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `confetti`

Confetti

- **Template:** `chirpui/confetti.html`
- **Macro:** `confetti`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Variants:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `event` | no | (has default) |
| `cls` | no | (has default) |

### `config-row`

Config row — label | control (toggle, select, editable)

- **Template:** `chirpui/config_row.html`
- **Macro:** `config_row_toggle`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `label` | yes | — |
| `checked` | no | (has default) |
| `form_action` | no | (has default) |
| `attrs_map` | no | (has default) |
| `errors` | no | (has default) |
| `cls` | no | (has default) |
| `swap_id` | no | (has default) |
| `oob` | no | (has default) |

### `config-row-list`

- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `confirm`

Confirm dialog component

- **Template:** `chirpui/confirm.html`
- **Macro:** `confirm_dialog`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `form_content`, `header_actions`, `message`
- **Variants:** `danger`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | yes | — |
| `message` | no | (has default) |
| `confirm_label` | no | (has default) |
| `cancel_label` | no | (has default) |
| `variant` | no | (has default) |
| `confirm_url` | no | (has default) |
| `confirm_method` | no | (has default) |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |
| `hx_select` | no | (has default) |
| `hx_push_url` | no | (has default) |
| `cls` | no | (has default) |

### `constellation`

Constellation

- **Template:** `chirpui/constellation.html`
- **Macro:** `constellation`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `cool`, `default`, `mono`, `warm`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `density` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `container`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `conversation-item`

Conversation Item component

- **Template:** `chirpui/conversation_item.html`
- **Macro:** `conversation_item`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`
- **Modifiers:** `muted`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `name` | yes | — |
| `preview` | yes | — |
| `time` | no | (has default) |
| `unread` | no | (has default) |
| `muted` | no | (has default) |
| `cls` | no | (has default) |

### `conversation-list`

Conversation List component

- **Template:** `chirpui/conversation_list.html`
- **Macro:** `conversation_list`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `copy-btn`

Copy button

- **Template:** `chirpui/copy_button.html`
- **Macro:** `copy_button`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Variants:** `(default)`, `assistant`, `system`, `user`
- **Consumes:** `_streaming_role`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `label` | no | (has default) |

### `counter-badge`

- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `cta-band`

CTA Band

- **Template:** `chirpui/cta_band.html`
- **Macro:** `cta_band`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`
- **Composes:** `band`, `btn`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `body` | no | (has default) |
| `primary_label` | no | (has default) |
| `primary_href` | no | (has default) |
| `secondary_label` | no | (has default) |
| `secondary_href` | no | (has default) |
| `variant` | no | (has default) |
| `width` | no | (has default) |
| `cls` | no | (has default) |

### `description_list`

Description list component

- **Template:** `chirpui/description_list.html`
- **Macro:** `description_list`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header`
- **Variants:** `horizontal`, `stacked`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `variant` | no | (has default) |
| `compact` | no | (has default) |
| `relaxed` | no | (has default) |
| `hoverable` | no | (has default) |
| `divided` | no | (has default) |
| `term_width` | no | (has default) |
| `detail_align` | no | (has default) |
| `cls` | no | (has default) |

### `detail-header`

Detail header

- **Template:** `chirpui/detail_header.html`
- **Macro:** `detail_header`
- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `actions`, `aside`, `badges`, `media`, `meta`
- **Composes:** `badge`, `btn`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `summary` | no | (has default) |
| `eyebrow` | no | (has default) |
| `cls` | no | (has default) |

### `display`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `divider`

Divider component

- **Template:** `chirpui/divider.html`
- **Macro:** `divider`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `accent`, `dotted`, `error`, `fade`, `horizontal`, `primary`, `success`, `warning`
- **Consumes:** `_card_variant`, `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `text` | no | (has default) |
| `horizontal` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `dl`

- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `dnd`

Drag-drop primitives

- **Template:** `chirpui/dnd.html`
- **Macro:** `dnd_list`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `board`, `row`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |

### `dock`

Floating Dock

- **Template:** `chirpui/dock.html`
- **Macro:** `dock`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `default`, `glass`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `document-header`

Document header

- **Template:** `chirpui/document_header.html`
- **Macro:** `document_header`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`
- **Composes:** `page_header`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `subtitle` | no | (has default) |
| `meta` | no | (has default) |
| `breadcrumb_items` | no | (has default) |
| `eyebrow` | no | (has default) |
| `path` | no | (has default) |
| `provenance` | no | (has default) |
| `status` | no | (has default) |
| `meta_items` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `actions` | `page_header` | `actions` |

### `donut`

Donut Chart component

- **Template:** `chirpui/donut.html`
- **Macro:** `donut`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `gold`, `muted`, `success`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `max` | no | (has default) |
| `text` | no | (has default) |
| `caption` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `drawer`

Drawer component

- **Template:** `chirpui/drawer.html`
- **Macro:** `drawer`
- **Category:** `overlay`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`, `header_actions`
- **Variants:** `left`, `right`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | no | (has default) |
| `side` | no | (has default) |
| `cls` | no | (has default) |

### `dropdown`

Dropdown component

- **Template:** `chirpui/dropdown.html`
- **Macro:** `dropdown`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `cls` | no | (has default) |

### `dropdown__item`

Dropdown menu (items-based)

- **Template:** `chirpui/dropdown_menu.html`
- **Macro:** `dropdown_menu`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Variants:** `danger`, `default`, `muted`

| Param | Required | Default |
|-------|----------|---------|
| `trigger` | yes | — |
| `items` | yes | — |
| `id` | no | (has default) |

### `empty-panel-state`

Empty panel state

- **Template:** `chirpui/empty_panel_state.html`
- **Macro:** `empty_panel_state`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `action`, `actions`
- **Composes:** `empty-state`
- **Modifiers:** `compact`

| Param | Required | Default |
|-------|----------|---------|
| `icon` | no | (has default) |
| `title` | no | (has default) |
| `illustration` | no | (has default) |
| `action_label` | no | (has default) |
| `action_href` | no | (has default) |
| `code` | no | (has default) |
| `suggestions` | no | (has default) |
| `search_hint` | no | (has default) |
| `compact` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `(default)` | `empty-state` | `(default)` |
| `action` | `empty-state` | `action` |
| `actions` | `empty-state` | `actions` |

### `empty-state`

Empty State component

- **Template:** `chirpui/empty.html`
- **Macro:** `empty_state`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `action`, `actions`

| Param | Required | Default |
|-------|----------|---------|
| `icon` | no | (has default) |
| `title` | no | (has default) |
| `illustration` | no | (has default) |
| `action_label` | no | (has default) |
| `action_href` | no | (has default) |
| `code` | no | (has default) |
| `suggestions` | no | (has default) |
| `search_hint` | no | (has default) |
| `cls` | no | (has default) |

### `entity-header`

Entity header (dashboard-grade)

- **Template:** `chirpui/entity_header.html`
- **Macro:** `entity_header`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `meta` | no | (has default) |
| `icon` | no | (has default) |
| `cls` | no | (has default) |

### `facet-chip`

Facet chip

- **Template:** `chirpui/facet_chip.html`
- **Macro:** `facet_chip`
- **Category:** `control`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Composes:** `chip`
- **Modifiers:** `custom`, `muted`, `removable`, `selected`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `href` | no | (has default) |
| `count` | no | (has default) |
| `selected` | no | (has default) |
| `muted` | no | (has default) |
| `color` | no | (has default) |
| `remove_href` | no | (has default) |
| `remove_label` | no | (has default) |
| `cls` | no | (has default) |

### `feature-section`

Feature Section component

- **Template:** `chirpui/feature_section.html`
- **Macro:** `feature_section`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `eyebrow`, `media`, `title`
- **Variants:** `balanced`, `halo`, `media-dominant`, `muted`, `split`, `stacked`
- **Modifiers:** `reverse`

| Param | Required | Default |
|-------|----------|---------|
| `layout` | no | (has default) |
| `variant` | no | (has default) |
| `reverse` | no | (has default) |
| `cls` | no | (has default) |

### `feature-stack`

Feature Section component

- **Template:** `chirpui/feature_section.html`
- **Macro:** `feature_stack`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `field`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `field_wrapper`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`
- **Variants:** `checkbox`, `dense`, `error`, `radio`, `radio-horizontal`, `range`, `toggle`
- **Consumes:** `_form_density`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `label` | no | (has default) |
| `errors` | no | (has default) |
| `required` | no | (has default) |
| `hint` | no | (has default) |
| `modifier` | no | (has default) |
| `field_id` | no | (has default) |
| `oob` | no | (has default) |

### `fieldset`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `fieldset`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `legend` | no | (has default) |
| `cls` | no | (has default) |

### `file-tree`

File tree

- **Template:** `chirpui/file_tree.html`
- **Macro:** `file_tree`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`, `footer`, `header`
- **Composes:** `nav-tree`, `panel`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `show_icons` | no | (has default) |
| `branch_mode` | no | (has default) |
| `surface_variant` | no | (has default) |
| `scroll_body` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `actions` | `panel` | `actions` |
| `footer` | `panel` | `footer` |
| `header` | `nav-tree` | `header` |

### `filter-bar`

- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `filter-group`

Filter chips — radiogroup + pill chips (named colors / HTMX)

- **Template:** `chirpui/filter_chips.html`
- **Macro:** `filter_group`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `param` | no | (has default) |
| `value` | no | (has default) |
| `cls` | no | (has default) |

### `filter-row`

Filter Bar composite

- **Template:** `chirpui/filter_bar.html`
- **Macro:** `filter_row`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `action` | no | (has default) |
| `method` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |
| `gap` | no | (has default) |
| `cls` | no | (has default) |

### `flow`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `focus-ring`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-2xl`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-base`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-lg`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-medium`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-mono`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-sm`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-xl`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `font-xs`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `form-actions`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `form_actions`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `end`

| Param | Required | Default |
|-------|----------|---------|
| `align` | no | (has default) |
| `cls` | no | (has default) |

### `form-error-summary`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `form_error_summary`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`

| Param | Required | Default |
|-------|----------|---------|
| `errors` | yes | — |
| `id` | no | (has default) |
| `oob` | no | (has default) |

### `fragment-island`

Safe region / Fragment island primitives

- **Template:** `chirpui/fragment_island.html`
- **Macro:** `fragment_island`
- **Category:** `infrastructure`
- **Maturity:** `internal`
- **Role:** `infrastructure`
- **Authoring:** `internal`
- **Requires:** `htmx`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |
| `hx_select` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |

### `frame`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `glitch`

Glitch Text Effect

- **Template:** `chirpui/glitch_text.html`
- **Macro:** `glitch_text`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `intense`, `subtle`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `glow-card`

Glow Card

- **Template:** `chirpui/glow_card.html`
- **Macro:** `glow_card`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `muted`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `gradient-text`

Gradient Text

- **Template:** `chirpui/gradient_text.html`
- **Macro:** `gradient_text`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Modifiers:** `animated`, `rainbow`, `secondary`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `animated` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `grain`

Grain Overlay

- **Template:** `chirpui/grain.html`
- **Macro:** `grain`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `heavy`, `subtle`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `animated` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `grid`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `hero`

Hero component

- **Template:** `chirpui/hero.html`
- **Macro:** `hero`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `action`, `actions`
- **Variants:** `animated-gradient`, `gradient`, `mesh`, `muted`, `solid`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `background` | no | (has default) |
| `cls` | no | (has default) |

### `hero-effects`

Hero Effects

- **Template:** `chirpui/hero_effects.html`
- **Macro:** `hero_effects`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Provides:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `effect` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `holy-light`

Holy Light

- **Template:** `chirpui/holy_light.html`
- **Macro:** `holy_light`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `default`, `gold`, `holy`, `silver`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `intensity` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `hover-jello`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `hover-rubber`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `hover-wobble`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `icon-btn`

Icon Button

- **Template:** `chirpui/icon_btn.html`
- **Macro:** `icon_btn`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Variants:** `(default)`, `danger`, `default`, `ghost`, `primary`
- **Sizes:** `(default)`, `lg`, `md`, `sm`
- **Consumes:** `_bar_density`, `_suspense_busy`

| Param | Required | Default |
|-------|----------|---------|
| `icon` | yes | — |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `href` | no | (has default) |
| `aria_label` | no | (has default) |
| `disabled` | no | (has default) |
| `type` | no | (has default) |
| `cls` | no | (has default) |
| `hx` | no | (has default) |
| `hx_get` | no | (has default) |
| `hx_post` | no | (has default) |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |

### `index-card`

Index card component

- **Template:** `chirpui/index_card.html`
- **Macro:** `index_card`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `title` | yes | — |
| `description` | no | (has default) |
| `badge` | no | (has default) |
| `cls` | no | (has default) |

### `infinite-scroll`

Infinite Scroll component

- **Template:** `chirpui/infinite_scroll.html`
- **Macro:** `infinite_scroll`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`, `loading`

| Param | Required | Default |
|-------|----------|---------|
| `load_url` | yes | — |
| `target` | no | (has default) |
| `swap` | no | (has default) |
| `loading_html` | no | (has default) |
| `cls` | no | (has default) |

### `inline`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `inline-counter`

Inline counter

- **Template:** `chirpui/inline_counter.html`
- **Macro:** `inline_counter`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `mark` | yes | — |
| `value` | yes | — |
| `label` | yes | — |
| `title` | no | (has default) |
| `cls` | no | (has default) |

### `inline-edit`

Inline edit field

- **Template:** `chirpui/inline_edit_field.html`
- **Macro:** `inline_edit_field_display`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Variants:** `display`, `edit`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `edit_url` | yes | — |
| `swap_target` | no | (has default) |
| `swap_id` | no | (has default) |
| `edit_label` | no | (has default) |
| `edit_icon` | no | (has default) |
| `cls` | no | (has default) |

### `input-group`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `input_group`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `prefix`, `suffix`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `prefix` | no | (has default) |
| `suffix` | no | (has default) |
| `value` | no | (has default) |
| `label` | no | (has default) |
| `errors` | no | (has default) |
| `type` | no | (has default) |
| `required` | no | (has default) |
| `placeholder` | no | (has default) |
| `hint` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |

### `install-snippet`

Code macros

- **Template:** `chirpui/code.html`
- **Macro:** `install_snippet`
- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `command` | yes | — |
| `label` | no | (has default) |
| `prompt` | no | (has default) |
| `id` | no | (has default) |
| `cls` | no | (has default) |

### `jello`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `key-value-form`

- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `label-overline`

Small caps / overline label for cards and dense panels.

- **Template:** `chirpui/label_overline.html`
- **Macro:** `label_overline`
- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `section`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `section` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `latest-line`

Latest line

- **Template:** `chirpui/latest_line.html`
- **Macro:** `latest_line`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `href` | yes | — |
| `title` | yes | — |
| `actor` | no | (has default) |
| `actor_href` | no | (has default) |
| `meta` | no | (has default) |
| `detail` | no | (has default) |
| `cls` | no | (has default) |

### `layer`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `lifecycle-showcase`

Marketing pattern assets

- **Template:** `chirpui/marketing_patterns.html`
- **Macro:** `lifecycle_showcase`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `link`

Link component

- **Template:** `chirpui/link.html`
- **Macro:** `link`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `href` | yes | — |
| `external` | no | (has default) |
| `cls` | no | (has default) |

### `list`

List component

- **Template:** `chirpui/list.html`
- **Macro:** `list_group`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `bordered`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `linked` | no | (has default) |
| `bordered` | no | (has default) |
| `cls` | no | (has default) |

### `list-reset`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `live-badge`

Live Badge component

- **Template:** `chirpui/live_badge.html`
- **Macro:** `live_badge`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `viewers` | no | (has default) |
| `cls` | no | (has default) |

### `live-event-card`

Media pattern assets

- **Template:** `chirpui/media_patterns.html`
- **Macro:** `live_event_card`
- **Category:** `media`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Composes:** `badge`, `btn`, `media-object`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `state` | yes | — |
| `time` | yes | — |
| `href` | no | (has default) |
| `restriction` | no | (has default) |
| `state_variant` | no | (has default) |
| `cls` | no | (has default) |

### `logo`

Logo component

- **Template:** `chirpui/logo.html`
- **Macro:** `logo`
- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `center`, `end`, `image`, `lg`, `md`, `sm`, `start`, `text`

| Param | Required | Default |
|-------|----------|---------|
| `text` | no | (has default) |
| `image_src` | no | (has default) |
| `image_alt` | no | (has default) |
| `href` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `align` | no | (has default) |
| `cls` | no | (has default) |

### `logo-cloud`

Logo Cloud

- **Template:** `chirpui/logo_cloud.html`
- **Macro:** `logo_cloud`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `monochrome`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `label` | no | (has default) |
| `monochrome` | no | (has default) |
| `cls` | no | (has default) |

### `marquee`

Marquee

- **Template:** `chirpui/marquee.html`
- **Macro:** `marquee`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `default`, `reverse`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `speed` | no | (has default) |
| `reverse` | no | (has default) |
| `pause_on_hover` | no | (has default) |
| `cls` | no | (has default) |

### `mb-md`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `measure-lg`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `measure-md`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `measure-sm`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `media-hero-shelf`

Media pattern assets

- **Template:** `chirpui/media_patterns.html`
- **Macro:** `media_hero_shelf`
- **Category:** `media`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Composes:** `carousel`, `title-card`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `artwork` | no | (has default) |
| `cls` | no | (has default) |

### `media-object`

Media Object layout primitive

- **Template:** `chirpui/media_object.html`
- **Macro:** `media_object`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `media`
- **Modifiers:** `align-center`

| Param | Required | Default |
|-------|----------|---------|
| `align` | no | (has default) |
| `cls` | no | (has default) |
| `use_slots` | no | (has default) |

### `mention`

Mention component

- **Template:** `chirpui/mention.html`
- **Macro:** `mention`
- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `username` | yes | — |
| `href` | no | (has default) |
| `cls` | no | (has default) |

### `message-reactions`

- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `message-thread`

Message Thread component

- **Template:** `chirpui/message_thread.html`
- **Macro:** `message_thread`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `message_bubble`

Message Bubble component

- **Template:** `chirpui/message_bubble.html`
- **Macro:** `message_bubble`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `assistant`, `default`, `system`, `user`

| Param | Required | Default |
|-------|----------|---------|
| `align` | no | (has default) |
| `role` | no | (has default) |
| `status` | no | (has default) |
| `cls` | no | (has default) |

### `meteor`

Meteor Effect

- **Template:** `chirpui/meteor.html`
- **Macro:** `meteor`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `muted`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `metric-card`

Metric grid/card

- **Template:** `chirpui/metric_grid.html`
- **Macro:** `metric_card`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `label` | yes | — |
| `icon` | no | (has default) |
| `trend` | no | (has default) |
| `trend_direction` | no | (has default) |
| `hint` | no | (has default) |
| `href` | no | (has default) |
| `icon_bg` | no | (has default) |
| `footer_label` | no | (has default) |
| `footer_href` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `metric-grid`

Metric grid/card

- **Template:** `chirpui/metric_grid.html`
- **Macro:** `metric_grid`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cols` | no | (has default) |
| `gap` | no | (has default) |
| `cls` | no | (has default) |

### `min-w-0`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `modal`

Modal component

- **Template:** `chirpui/modal.html`
- **Macro:** `modal`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`, `footer`, `header_actions`
- **Sizes:** `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `model-card`

- **Category:** `data-display`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `moderation-queue-item`

Forum and social pattern assets

- **Template:** `chirpui/forum_patterns.html`
- **Macro:** `moderation_queue_item`
- **Category:** `social`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `actions`
- **Composes:** `badge`, `btn`, `resource-card`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `title` | yes | — |
| `reason` | yes | — |
| `state` | no | (has default) |
| `state_variant` | no | (has default) |
| `target` | no | (has default) |
| `actor` | no | (has default) |
| `cls` | no | (has default) |

### `mt-md`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `mt-sm`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `nav-progress`

Navigation progress bar

- **Template:** `chirpui/nav_progress.html`
- **Macro:** `nav_progress`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `nav-tree`

Nav tree component

- **Template:** `chirpui/nav_tree.html`
- **Macro:** `nav_tree`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header`
- **Modifiers:** `linked-branches`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `show_icons` | no | (has default) |
| `branch_mode` | no | (has default) |
| `cls` | no | (has default) |

### `navbar`

Navbar component

- **Template:** `chirpui/navbar.html`
- **Macro:** `navbar`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `brand`, `end`
- **Modifiers:** `sticky`
- **Provides:** `_nav_current_path`

| Param | Required | Default |
|-------|----------|---------|
| `brand` | no | (has default) |
| `brand_url` | no | (has default) |
| `cls` | no | (has default) |
| `use_slots` | no | (has default) |
| `brand_slot` | no | (has default) |
| `current_path` | no | (has default) |

### `navbar-dropdown`

Navbar component

- **Template:** `chirpui/navbar.html`
- **Macro:** `navbar_dropdown`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Consumes:** `_nav_current_path`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `active` | no | (has default) |
| `match` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |

### `neon`

Neon Text

- **Template:** `chirpui/neon_text.html`
- **Macro:** `neon_text`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `blue`, `cyan`, `green`, `magenta`, `orange`, `red`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `color` | no | (has default) |
| `animation` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `notification-dot`

Notification Dot

- **Template:** `chirpui/notification_dot.html`
- **Macro:** `notification_dot`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `default`, `error`, `success`, `warning`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `count` | no | (has default) |
| `aria_label` | no | (has default) |
| `cls` | no | (has default) |

### `number-scale`

- **Category:** `form`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `number-ticker`

Number Ticker

- **Template:** `chirpui/number_ticker.html`
- **Macro:** `number_ticker`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `default`, `mono`
- **Sizes:** `(default)`, `lg`, `md`, `sm`, `xl`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `prefix` | no | (has default) |
| `suffix` | no | (has default) |
| `cls` | no | (has default) |

### `orbit`

Orbit

- **Template:** `chirpui/orbit.html`
- **Macro:** `orbit`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `lg`, `sm`, `xl`
- **Sizes:** `(default)`, `lg`, `sm`, `xl`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `size` | no | (has default) |
| `speed` | no | (has default) |
| `reverse` | no | (has default) |
| `cls` | no | (has default) |

### `overlay`

Overlay component

- **Template:** `chirpui/overlay.html`
- **Macro:** `overlay`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `dark`, `gradient-bottom`, `gradient-top`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `page-fill`

- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `page_header`

Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block.

- **Template:** `chirpui/layout.html`
- **Macro:** `page_header`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`
- **Variants:** `compact`, `default`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `subtitle` | no | (has default) |
| `meta` | no | (has default) |
| `breadcrumb_items` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `page_hero`

Hero component

- **Template:** `chirpui/hero.html`
- **Macro:** `page_hero`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `eyebrow`, `footer`, `metadata`
- **Variants:** `editorial`, `minimal`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `variant` | no | (has default) |
| `background` | no | (has default) |
| `cls` | no | (has default) |

### `pagination`

Pagination component

- **Template:** `chirpui/pagination.html`
- **Macro:** `pagination`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`

| Param | Required | Default |
|-------|----------|---------|
| `current` | yes | — |
| `total` | yes | — |
| `url_pattern` | yes | — |
| `hx_target` | no | (has default) |
| `hx_push_url` | no | (has default) |
| `hx_swap` | no | (has default) |
| `hx_select` | no | (has default) |
| `window` | no | (has default) |
| `cls` | no | (has default) |

### `panel`

Panel component

- **Template:** `chirpui/panel.html`
- **Macro:** `panel`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `footer`
- **Provides:** `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `surface_variant` | no | (has default) |
| `scroll_body` | no | (has default) |
| `cls` | no | (has default) |

### `params-table`

Params table component

- **Template:** `chirpui/params_table.html`
- **Macro:** `params_table`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `rows` | yes | — |
| `title` | no | (has default) |
| `columns` | no | (has default) |
| `cls` | no | (has default) |

### `particle-bg`

Particle Background

- **Template:** `chirpui/particle_bg.html`
- **Macro:** `particle_bg`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `muted`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `placeholder-inline`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `playlist`

Playlist component

- **Template:** `chirpui/playlist.html`
- **Macro:** `playlist`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `header_actions`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `cls` | no | (has default) |

### `playlist-item`

Playlist component

- **Template:** `chirpui/playlist.html`
- **Macro:** `playlist_item`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `active`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `title` | yes | — |
| `duration` | no | (has default) |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `popover`

Popover component

- **Template:** `chirpui/popover.html`
- **Macro:** `popover`
- **Category:** `overlay`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header`

| Param | Required | Default |
|-------|----------|---------|
| `trigger_label` | yes | — |
| `cls` | no | (has default) |

### `post-card`

Post Card component

- **Template:** `chirpui/post_card.html`
- **Macro:** `post_card`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `actions`, `avatar`, `media`

| Param | Required | Default |
|-------|----------|---------|
| `name` | no | (has default) |
| `handle` | no | (has default) |
| `time` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |

### `primary-nav`

Primary navigation

- **Template:** `chirpui/primary_nav.html`
- **Macro:** `primary_nav`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `current_path` | no | (has default) |
| `aria_label` | no | (has default) |
| `cls` | no | (has default) |

### `profile-header`

Profile Header component

- **Template:** `chirpui/profile_header.html`
- **Macro:** `profile_header`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `action`, `actions`, `avatar`, `bio`, `stats`

| Param | Required | Default |
|-------|----------|---------|
| `name` | no | (has default) |
| `cover_url` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |
| `use_slots` | no | (has default) |

### `progress`

- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `progress-bar`

Progress Bar component

- **Template:** `chirpui/progress.html`
- **Macro:** `progress_bar`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `custom`, `gold`, `radiant`, `success`, `watched`
- **Sizes:** `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `max` | no | (has default) |
| `label` | no | (has default) |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |
| `color` | no | (has default) |

### `prose`

- **Category:** `typography`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `prose-lg`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `prose-sm`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `pulsing-btn`

Pulsing Button

- **Template:** `chirpui/pulsing_button.html`
- **Macro:** `pulsing_button`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `danger`, `default`, `primary`, `success`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `icon` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |
| `type` | no | (has default) |
| `disabled` | no | (has default) |

### `reaction-pill`

Reaction Pill component

- **Template:** `chirpui/reaction_pill.html`
- **Macro:** `reaction_pill`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `active`, `disabled`

| Param | Required | Default |
|-------|----------|---------|
| `emoji` | yes | — |
| `count` | no | (has default) |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `rendered-content`

Rendered content

- **Template:** `chirpui/rendered_content.html`
- **Macro:** `rendered_content`
- **Category:** `typography`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `compact`

| Param | Required | Default |
|-------|----------|---------|
| `compact` | no | (has default) |
| `cls` | no | (has default) |

### `resource-card`

- **Category:** `data-display`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `resource-index`

Resource Index composite

- **Template:** `chirpui/resource_index.html`
- **Macro:** `resource_index`
- **Category:** `composite`
- **Maturity:** `stable`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `(default)`, `empty`, `filter_actions`, `filter_controls`, `filter_primary`, `filters_panel`, `selection`, `toolbar_controls`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `search_action` | yes | — |
| `query` | no | (has default) |
| `subtitle` | no | (has default) |
| `search_name` | no | (has default) |
| `search_placeholder` | no | (has default) |
| `button_label` | no | (has default) |
| `button_icon` | no | (has default) |
| `search_method` | no | (has default) |
| `filter_action` | no | (has default) |
| `filter_method` | no | (has default) |
| `filter_surface_variant` | no | (has default) |
| `filter_density` | no | (has default) |
| `filter_label` | no | (has default) |
| `filter_state_name` | no | (has default) |
| `filter_state_value` | no | (has default) |
| `selected_count` | no | (has default) |
| `selected_label` | no | (has default) |
| `selected_aria_label` | no | (has default) |
| `results_title` | no | (has default) |
| `results_subtitle` | no | (has default) |
| `results_layout` | no | (has default) |
| `results_cols` | no | (has default) |
| `results_gap` | no | (has default) |
| `has_results` | no | (has default) |
| `empty_title` | no | (has default) |
| `empty_icon` | no | (has default) |
| `empty_hint` | no | (has default) |
| `empty_message` | no | (has default) |
| `mutation_result_id` | no | (has default) |
| `cls` | no | (has default) |

### `result-slot`

- **Category:** `feedback`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `reveal-on-scroll`

Reveal on scroll — animate content when it enters the viewport

- **Template:** `chirpui/reveal_on_scroll.html`
- **Macro:** `reveal_on_scroll`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `ripple-btn`

Ripple Button

- **Template:** `chirpui/ripple_button.html`
- **Macro:** `ripple_button`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Variants:** `(default)`, `default`, `primary`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `icon` | no | (has default) |
| `cls` | no | (has default) |

### `route-tab`

Route-backed subsection tabs

- **Template:** `chirpui/route_tabs.html`
- **Macro:** `render_route_tabs`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`

| Param | Required | Default |
|-------|----------|---------|
| `tab_items` | yes | — |
| `current_path` | yes | — |
| `target` | no | (has default) |
| `is_active` | no | (has default) |

### `route-tabs`

- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `row-actions`

Row actions (kebab menu)

- **Template:** `chirpui/row_actions.html`
- **Macro:** `row_actions`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `id` | no | (has default) |

### `rubber-band`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `rune-field`

Rune Field

- **Template:** `chirpui/rune_field.html`
- **Macro:** `rune_field`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `arcane`, `default`, `ember`, `frost`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `scanline`

Scanline Overlay

- **Template:** `chirpui/scanline.html`
- **Macro:** `scanline`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `crt`, `heavy`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `scroll-x`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `search-bar`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `search_bar`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Modifiers:** `with-icon`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `value` | no | (has default) |
| `variant` | no | (has default) |
| `label` | no | (has default) |
| `search_url` | no | (has default) |
| `search_target` | no | (has default) |
| `search_trigger` | no | (has default) |
| `search_include` | no | (has default) |
| `search_sync` | no | (has default) |
| `placeholder` | no | (has default) |
| `button_label` | no | (has default) |
| `button_icon` | no | (has default) |
| `errors` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |
| `search_attrs_map` | no | (has default) |
| `search_hx_select` | no | (has default) |

### `search-header`

Search Header composite

- **Template:** `chirpui/search_header.html`
- **Macro:** `search_header`
- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `form_action` | yes | — |
| `query` | no | (has default) |
| `search_name` | no | (has default) |
| `subtitle` | no | (has default) |
| `meta` | no | (has default) |
| `breadcrumb_items` | no | (has default) |
| `form_method` | no | (has default) |
| `form_attrs` | no | (has default) |
| `form_attrs_unsafe` | no | (has default) |
| `form_attrs_map` | no | (has default) |
| `search_placeholder` | no | (has default) |
| `button_label` | no | (has default) |
| `button_icon` | no | (has default) |
| `surface_variant` | no | (has default) |
| `density` | no | (has default) |
| `wrap` | no | (has default) |
| `sticky` | no | (has default) |
| `cls` | no | (has default) |

### `section-collapsible`

Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block.

- **Template:** `chirpui/layout.html`
- **Macro:** `section_collapsible`
- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Composes:** `section_header`, `surface`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `open` | no | (has default) |
| `surface_variant` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `(default)` | `surface` | `(default)` |

### `section_header`

Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block.

- **Template:** `chirpui/layout.html`
- **Macro:** `section_header`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`
- **Variants:** `default`, `inline`

| Param | Required | Default |
|-------|----------|---------|
| `title` | yes | — |
| `subtitle` | no | (has default) |
| `icon` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `segmented`

Segmented Control

- **Template:** `chirpui/segmented_control.html`
- **Macro:** `segmented_control`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `items` | yes | — |
| `name` | no | (has default) |
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `selection-bar`

Selection Bar

- **Template:** `chirpui/selection_bar.html`
- **Macro:** `selection_bar`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `label` | no | (has default) |
| `live_region` | no | (has default) |
| `aria_label` | no | (has default) |
| `cls` | no | (has default) |

### `settings-row`

Settings row — label | status badge | detail

- **Template:** `chirpui/settings_row.html`
- **Macro:** `settings_row`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `status` | no | (has default) |
| `detail` | no | (has default) |
| `status_variant` | no | (has default) |
| `cls` | no | (has default) |

### `settings-row-list`

Settings row — label | status badge | detail

- **Template:** `chirpui/settings_row.html`
- **Macro:** `settings_row_list`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `divided`, `hoverable`, `relaxed`
- **Consumes:** `_card_variant`, `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `hoverable` | no | (has default) |
| `divided` | no | (has default) |
| `relaxed` | no | (has default) |
| `cls` | no | (has default) |

### `shell-action-form`

- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `shell-actions`

Shell actions renderer

- **Template:** `chirpui/shell_actions.html`
- **Macro:** `shell_actions_bar`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `shell_actions` | yes | — |
| `cls` | no | (has default) |

### `shell-section`

- **Category:** `layout`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `shimmer-btn`

Shimmer Button

- **Template:** `chirpui/shimmer_button.html`
- **Macro:** `shimmer_button`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `default`, `primary`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `size` | no | (has default) |
| `icon` | no | (has default) |
| `href` | no | (has default) |
| `cls` | no | (has default) |
| `type` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |
| `disabled` | no | (has default) |

### `sidebar`

Sidebar component

- **Template:** `chirpui/sidebar.html`
- **Macro:** `sidebar`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header`
- **Provides:** `_nav_current_path`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |
| `current_path` | no | (has default) |

### `sidebar-toggle`

Sidebar component

- **Template:** `chirpui/sidebar.html`
- **Macro:** `sidebar_toggle`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `signature`

Signature component

- **Template:** `chirpui/signature.html`
- **Macro:** `signature`
- **Category:** `content`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `language` | no | (has default) |
| `cls` | no | (has default) |

### `site-footer`

Site Footer component

- **Template:** `chirpui/site_footer.html`
- **Macro:** `site_footer`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `brand`, `colophon`, `rule`
- **Variants:** `centered`, `columns`, `simple`

| Param | Required | Default |
|-------|----------|---------|
| `layout` | no | (has default) |
| `cls` | no | (has default) |

### `site-header`

Site Header component

- **Template:** `chirpui/site_header.html`
- **Macro:** `site_header`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `brand`, `nav`, `nav_end`, `tools`
- **Variants:** `glass`, `solid`, `transparent`
- **Modifiers:** `sticky`
- **Provides:** `_site_nav_current_path`

| Param | Required | Default |
|-------|----------|---------|
| `brand_url` | no | (has default) |
| `layout` | no | (has default) |
| `variant` | no | (has default) |
| `sticky` | no | (has default) |
| `current_path` | no | (has default) |
| `cls` | no | (has default) |

### `site-nav-link`

Site Header component

- **Template:** `chirpui/site_header.html`
- **Macro:** `site_nav_link`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Consumes:** `_site_nav_current_path`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `label` | yes | — |
| `glyph` | no | (has default) |
| `external` | no | (has default) |
| `match` | no | (has default) |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `site-shell`

Site Shell component

- **Template:** `chirpui/site_shell.html`
- **Macro:** `site_shell`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header`

| Param | Required | Default |
|-------|----------|---------|
| `ambient` | no | (has default) |
| `cls` | no | (has default) |

### `skeleton`

Skeleton component

- **Template:** `chirpui/skeleton.html`
- **Macro:** `skeleton`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `avatar`, `card`, `text`

| Param | Required | Default |
|-------|----------|---------|
| `width` | no | (has default) |
| `height` | no | (has default) |
| `variant` | no | (has default) |
| `lines` | no | (has default) |
| `cls` | no | (has default) |

### `sortable`

Sortable list macros

- **Template:** `chirpui/sortable_list.html`
- **Macro:** `sortable_list`
- **Category:** `interactive`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |

### `sparkle`

Sparkle

- **Template:** `chirpui/sparkle.html`
- **Macro:** `sparkle`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `gold`, `rainbow`, `white`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `spinner`

Spinner component

- **Template:** `chirpui/spinner.html`
- **Macro:** `spinner`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

| Param | Required | Default |
|-------|----------|---------|
| `size` | no | (has default) |
| `cls` | no | (has default) |

### `spinner-thinking`

- **Category:** `feedback`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `split-btn`

Split button component

- **Template:** `chirpui/split_button.html`
- **Macro:** `split_button`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `header`

| Param | Required | Default |
|-------|----------|---------|
| `primary_label` | yes | — |
| `primary_href` | no | (has default) |
| `primary_submit` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `split-flap`

ASCII Split-Flap Display

- **Template:** `chirpui/ascii_split_flap.html`
- **Macro:** `split_flap`
- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `amber`, `default`, `green`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `animate` | no | (has default) |
| `cls` | no | (has default) |

### `split-flap-board`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `split-flap-row`

- **Category:** `ascii`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `split-layout`

Split layout

- **Template:** `chirpui/split_layout.html`
- **Macro:** `split_layout`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `primary`, `secondary`
- **Variants:** `balanced`, `horizontal`, `sidebar`, `vertical`, `wide-primary`, `wide-secondary`
- **Modifiers:** `gap-lg`, `gap-md`, `gap-sm`

| Param | Required | Default |
|-------|----------|---------|
| `direction` | no | (has default) |
| `ratio` | no | (has default) |
| `gap` | no | (has default) |
| `cls` | no | (has default) |

### `split-panel`

Split Panel

- **Template:** `chirpui/split_panel.html`
- **Macro:** `split_panel`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `left`, `right`
- **Modifiers:** `dragging`, `vertical`

| Param | Required | Default |
|-------|----------|---------|
| `direction` | no | (has default) |
| `default_split` | no | (has default) |
| `min_split` | no | (has default) |
| `max_split` | no | (has default) |
| `cls` | no | (has default) |

### `spotlight-card`

Spotlight Card

- **Template:** `chirpui/spotlight_card.html`
- **Macro:** `spotlight_card`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `sse-retry`

- **Category:** `feedback`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`
- **Modifiers:** `loading`

### `sse-status`

SSE connection status and error recovery

- **Template:** `chirpui/sse_status.html`
- **Macro:** `sse_status`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Modifiers:** `connected`, `disconnected`, `error`

| Param | Required | Default |
|-------|----------|---------|
| `state` | no | (has default) |
| `label` | no | (has default) |
| `cls` | no | (has default) |

### `stack`

- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `preferred`

### `star-rating`

- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

### `stat`

Stat component

- **Template:** `chirpui/stat.html`
- **Macro:** `stat`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `value` | yes | — |
| `label` | yes | — |
| `icon` | no | (has default) |
| `cls` | no | (has default) |

### `status-indicator`

Status Indicator component

- **Template:** `chirpui/status.html`
- **Macro:** `status_indicator`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `custom`, `default`, `error`, `info`, `primary`, `success`, `warning`
- **Consumes:** `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `label` | yes | — |
| `variant` | no | (has default) |
| `icon` | no | (has default) |
| `pulse` | no | (has default) |
| `cls` | no | (has default) |
| `color` | no | (has default) |

### `stepper`

Stepper component

- **Template:** `chirpui/stepper.html`
- **Macro:** `stepper`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `steps` | yes | — |
| `current` | no | (has default) |
| `cls` | no | (has default) |

### `story-card`

Story Card

- **Template:** `chirpui/story_card.html`
- **Macro:** `story_card`
- **Category:** `marketing`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `(default)`, `footer`, `logo`, `metric`
- **Modifiers:** `link`

| Param | Required | Default |
|-------|----------|---------|
| `customer` | yes | — |
| `outcome` | yes | — |
| `summary` | no | (has default) |
| `href` | no | (has default) |
| `metric` | no | (has default) |
| `logo_src` | no | (has default) |
| `logo_alt` | no | (has default) |
| `cta_label` | no | (has default) |
| `cls` | no | (has default) |

### `streaming`

- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`
- **Variants:** `error`

### `streaming-block`

- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`
- **Modifiers:** `active`

### `streaming_bubble`

Streaming and AI components

- **Template:** `chirpui/streaming.html`
- **Macro:** `streaming_bubble`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`
- **Variants:** `error`, `thinking`
- **Provides:** `_streaming_role`

| Param | Required | Default |
|-------|----------|---------|
| `role` | no | (has default) |
| `state` | no | (has default) |
| `streaming` | no | (has default) |
| `sse_swap_target` | no | (has default) |
| `sse_connect` | no | (has default) |
| `sse_close` | no | (has default) |
| `cls` | no | (has default) |

### `surface`

Surface component

- **Template:** `chirpui/surface.html`
- **Macro:** `surface`
- **Category:** `container`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `accent`, `default`, `elevated`, `frosted`, `glass`, `gradient-accent`, `gradient-border`, `gradient-mesh`, `gradient-subtle`, `muted`, `smoke`
- **Modifiers:** `bento`, `full`, `no-padding`
- **Provides:** `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `variant` | no | (has default) |
| `full_width` | no | (has default) |
| `padding` | no | (has default) |
| `cls` | no | (has default) |
| `style` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |
| `attrs_map` | no | (has default) |

### `suspense-group`

- **Category:** `feedback`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `suspense-slot`

Suspense components

- **Template:** `chirpui/suspense.html`
- **Macro:** `suspense_slot`
- **Category:** `infrastructure`
- **Maturity:** `internal`
- **Role:** `infrastructure`
- **Authoring:** `internal`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `skeleton_variant` | no | (has default) |
| `lines` | no | (has default) |
| `width` | no | (has default) |
| `height` | no | (has default) |
| `cls` | no | (has default) |

### `symbol-rain`

Symbol Rain

- **Template:** `chirpui/symbol_rain.html`
- **Macro:** `symbol_rain`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `(default)`, `accent`, `default`, `gold`, `muted`
- **Consumes:** `_hero_variant`

| Param | Required | Default |
|-------|----------|---------|
| `count` | no | (has default) |
| `variant` | no | (has default) |
| `cls` | no | (has default) |

### `tab`

Tabs component

- **Template:** `chirpui/tabs.html`
- **Macro:** `tab`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Modifiers:** `active`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `label` | yes | — |
| `url` | no | (has default) |
| `hx_target` | no | (has default) |
| `hx_swap` | no | (has default) |
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `tab-panel`

- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `table`

Table component

- **Template:** `chirpui/table.html`
- **Macro:** `table`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`, `caption`
- **Modifiers:** `compact`, `striped`
- **Provides:** `_table_align`

| Param | Required | Default |
|-------|----------|---------|
| `headers` | no | (has default) |
| `rows` | no | (has default) |
| `sortable` | no | (has default) |
| `sort_url` | no | (has default) |
| `hx_target` | no | (has default) |
| `striped` | no | (has default) |
| `sticky_header` | no | (has default) |
| `actions_header` | no | (has default) |
| `align` | no | (has default) |
| `widths` | no | (has default) |
| `compact` | no | (has default) |
| `cls` | no | (has default) |

### `table-wrap`

Table component

- **Template:** `chirpui/table.html`
- **Macro:** `table`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`, `caption`
- **Modifiers:** `sticky`
- **Provides:** `_table_align`

| Param | Required | Default |
|-------|----------|---------|
| `headers` | no | (has default) |
| `rows` | no | (has default) |
| `sortable` | no | (has default) |
| `sort_url` | no | (has default) |
| `hx_target` | no | (has default) |
| `striped` | no | (has default) |
| `sticky_header` | no | (has default) |
| `actions_header` | no | (has default) |
| `align` | no | (has default) |
| `widths` | no | (has default) |
| `compact` | no | (has default) |
| `cls` | no | (has default) |

### `tabs`

Tabs component

- **Template:** `chirpui/tabs.html`
- **Macro:** `tabs`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `active` | no | (has default) |
| `cls` | no | (has default) |

### `tag`

Tag input component

- **Template:** `chirpui/tag_input.html`
- **Macro:** `tag_input`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `tags` | no | (has default) |
| `label` | no | (has default) |
| `add_url` | no | (has default) |
| `remove_url` | no | (has default) |
| `placeholder` | no | (has default) |
| `cls` | no | (has default) |

### `tag-browse`

Tag browse — tray + selection badges for tag-filtered listings

- **Template:** `chirpui/tag_browse.html`
- **Macro:** `tag_browse_tray`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | yes | — |
| `tags` | yes | — |
| `selected_tags` | yes | — |
| `tag_toggle_url` | yes | — |
| `clear_url` | yes | — |
| `position` | no | (has default) |
| `hint` | no | (has default) |

### `tag-input`

Tag input component

- **Template:** `chirpui/tag_input.html`
- **Macro:** `tag_input`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `tags` | no | (has default) |
| `label` | no | (has default) |
| `add_url` | no | (has default) |
| `remove_url` | no | (has default) |
| `placeholder` | no | (has default) |
| `cls` | no | (has default) |

### `text-muted`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `text-reveal`

Text Reveal

- **Template:** `chirpui/text_reveal.html`
- **Macro:** `text_reveal`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `default`, `gradient`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `variant` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `texture`

- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `theme-toggle`

Theme + style toggles

- **Template:** `chirpui/theme_toggle.html`
- **Macro:** `theme_toggle`
- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`

### `thread-reader-layout`

Thread reader layout

- **Template:** `chirpui/thread_reader_layout.html`
- **Macro:** `thread_reader_layout`
- **Category:** `social`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `attention_nav`, `composer`, `header`, `local_nav`, `posts`
- **Composes:** `answer-card`, `btn`, `detail-header`, `facet-chip`

| Param | Required | Default |
|-------|----------|---------|
| `label` | no | (has default) |
| `cls` | no | (has default) |

### `thumbs`

- **Category:** `control`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Sizes:** `(default)`, `lg`, `md`, `sm`

### `timeline`

Timeline component

- **Template:** `chirpui/timeline.html`
- **Macro:** `timeline`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Modifiers:** `hoverable`, `on-accent`, `on-muted`
- **Consumes:** `_surface_variant`

| Param | Required | Default |
|-------|----------|---------|
| `items` | no | (has default) |
| `hoverable` | no | (has default) |
| `link_mode` | no | (has default) |
| `cls` | no | (has default) |

### `title-card`

Media pattern assets

- **Template:** `chirpui/media_patterns.html`
- **Macro:** `title_card`
- **Category:** `media`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `actions`
- **Composes:** `badge`, `btn`, `video-thumbnail`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `title` | yes | — |
| `artwork` | no | (has default) |
| `alt` | no | (has default) |
| `duration` | no | (has default) |
| `meta` | no | (has default) |
| `summary` | no | (has default) |
| `state` | no | (has default) |
| `state_variant` | no | (has default) |
| `primary_label` | no | (has default) |
| `secondary_label` | no | (has default) |
| `secondary_href` | no | (has default) |
| `cls` | no | (has default) |

### `toast`

Toast component

- **Template:** `chirpui/toast.html`
- **Macro:** `toast`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`, `htmx`
- **Variants:** `error`, `info`, `success`, `warning`

| Param | Required | Default |
|-------|----------|---------|
| `message` | yes | — |
| `variant` | no | (has default) |
| `id` | no | (has default) |
| `dismissible` | no | (has default) |
| `oob` | no | (has default) |
| `container_id` | no | (has default) |
| `cls` | no | (has default) |

### `toast-container`

- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `primitive`
- **Authoring:** `available`

### `toggle`

- **Category:** `control`
- **Maturity:** `experimental`
- **Role:** `primitive`
- **Authoring:** `available`

### `toggle-wrap`

Form field macros

- **Template:** `chirpui/forms.html`
- **Macro:** `toggle_field`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Variants:** `(default)`, `accent`, `danger`, `lg`, `sm`, `success`

| Param | Required | Default |
|-------|----------|---------|
| `name` | yes | — |
| `checked` | no | (has default) |
| `label` | no | (has default) |
| `errors` | no | (has default) |
| `size` | no | (has default) |
| `variant` | no | (has default) |
| `label_inside` | no | (has default) |

### `token-input`

Token input

- **Template:** `chirpui/token_input.html`
- **Macro:** `token_input`
- **Category:** `form`
- **Maturity:** `experimental`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `input`, `results`, `tokens`

| Param | Required | Default |
|-------|----------|---------|
| `label` | no | (has default) |
| `input_id` | no | (has default) |
| `placeholder` | no | (has default) |
| `cls` | no | (has default) |

### `tooltip`

Tooltip macro

- **Template:** `chirpui/tooltip.html`
- **Macro:** `tooltip`
- **Category:** `navigation`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `bottom`, `left`, `right`, `top`
- **Modifiers:** `block`

| Param | Required | Default |
|-------|----------|---------|
| `content` | no | (has default) |
| `hint` | no | (has default) |
| `position` | no | (has default) |
| `block` | no | (has default) |
| `cls` | no | (has default) |

### `topic-card`

Forum and social pattern assets

- **Template:** `chirpui/forum_patterns.html`
- **Macro:** `topic_card`
- **Category:** `social`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `badges`
- **Composes:** `badge`, `resource-card`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `title` | yes | — |
| `description` | no | (has default) |
| `category` | no | (has default) |
| `state` | no | (has default) |
| `state_variant` | no | (has default) |
| `replies` | no | (has default) |
| `views` | no | (has default) |
| `latest_label` | no | (has default) |
| `latest_href` | no | (has default) |
| `actor` | no | (has default) |
| `meta` | no | (has default) |
| `cls` | no | (has default) |

### `tray`

Tray (slide-out panel)

- **Template:** `chirpui/tray.html`
- **Macro:** `tray`
- **Category:** `overlay`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `alpine`
- **Slots:** `(default)`
- **Variants:** `bottom`, `left`, `right`
- **Modifiers:** `closed`, `open`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `title` | yes | — |
| `position` | no | (has default) |

### `tree`

Tree view component

- **Template:** `chirpui/tree_view.html`
- **Macro:** `tree_view`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `nodes` | yes | — |
| `cls` | no | (has default) |

### `trending-tag`

Trending Tag component

- **Template:** `chirpui/trending_tag.html`
- **Macro:** `trending_tag`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Modifiers:** `up`

| Param | Required | Default |
|-------|----------|---------|
| `tag` | yes | — |
| `href` | no | (has default) |
| `count` | no | (has default) |
| `trend` | no | (has default) |
| `cls` | no | (has default) |

### `truncate`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `typewriter`

Typewriter Effect

- **Template:** `chirpui/typewriter.html`
- **Macro:** `typewriter`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Variants:** `(default)`, `fast`, `slow`

| Param | Required | Default |
|-------|----------|---------|
| `text` | yes | — |
| `speed` | no | (has default) |
| `cursor` | no | (has default) |
| `delay` | no | (has default) |
| `tag` | no | (has default) |
| `cls` | no | (has default) |

### `typing-indicator`

Typing Indicator component

- **Template:** `chirpui/typing_indicator.html`
- **Macro:** `typing_indicator`
- **Category:** `feedback`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `ui-base`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-bold`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-label`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-lg`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-medium`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-meta`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-normal`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-semibold`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-sm`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-title`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-xl`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `ui-xs`

- **Category:** `typography`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `video-card`

Video Card component

- **Template:** `chirpui/video_card.html`
- **Macro:** `video_card`
- **Category:** `data-display`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `actions`

| Param | Required | Default |
|-------|----------|---------|
| `href` | yes | — |
| `thumbnail` | yes | — |
| `duration` | yes | — |
| `title` | yes | — |
| `channel` | no | (has default) |
| `channel_href` | no | (has default) |
| `views` | no | (has default) |
| `date` | no | (has default) |
| `cls` | no | (has default) |

### `video-thumbnail`

Video Thumbnail component

- **Template:** `chirpui/video_thumbnail.html`
- **Macro:** `video_thumbnail`
- **Category:** `media`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`

| Param | Required | Default |
|-------|----------|---------|
| `href` | no | (has default) |
| `src` | no | (has default) |
| `alt` | no | (has default) |
| `duration` | no | (has default) |
| `watched_pct` | no | (has default) |
| `cls` | no | (has default) |

### `visually-hidden`

- **Category:** `layout`
- **Maturity:** `legacy`
- **Role:** `primitive`
- **Authoring:** `compatibility`

### `watch-companion-layout`

Media pattern assets

- **Template:** `chirpui/media_patterns.html`
- **Macro:** `watch_companion_layout`
- **Category:** `media`
- **Maturity:** `experimental`
- **Role:** `pattern`
- **Authoring:** `available`
- **Slots:** `companion`, `player`

| Param | Required | Default |
|-------|----------|---------|
| `cls` | no | (has default) |

### `wizard-form`

Wizard form component

- **Template:** `chirpui/wizard_form.html`
- **Macro:** `wizard_form`
- **Category:** `form`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Requires:** `htmx`
- **Slots:** `(default)`

| Param | Required | Default |
|-------|----------|---------|
| `id` | yes | — |
| `steps` | yes | — |
| `current` | no | (has default) |
| `cls` | no | (has default) |
| `attrs` | no | (has default) |
| `attrs_unsafe` | no | (has default) |

### `wobble`

Wobble / Jello / Rubber-band / Bounce-in

- **Template:** `chirpui/wobble.html`
- **Macro:** `wobble`
- **Category:** `effect`
- **Maturity:** `experimental`
- **Role:** `effect`
- **Authoring:** `available`
- **Slots:** `(default)`
- **Variants:** `bounce-in`, `jello`, `rubber-band`, `wobble`

| Param | Required | Default |
|-------|----------|---------|
| `trigger` | no | (has default) |
| `cls` | no | (has default) |

### `workspace-shell`

Workspace shell

- **Template:** `chirpui/workspace_shell.html`
- **Macro:** `workspace_shell`
- **Category:** `layout`
- **Maturity:** `stable`
- **Role:** `component`
- **Authoring:** `available`
- **Slots:** `(default)`, `inspector`, `sidebar`, `toolbar`
- **Composes:** `panel`, `split-layout`

| Param | Required | Default |
|-------|----------|---------|
| `title` | no | (has default) |
| `subtitle` | no | (has default) |
| `sidebar_title` | no | (has default) |
| `show_inspector` | no | (has default) |
| `inspector_title` | no | (has default) |
| `sidebar_surface_variant` | no | (has default) |
| `inspector_surface_variant` | no | (has default) |
| `cls` | no | (has default) |

| Slot | Target | Target slot |
|------|--------|-------------|
| `inspector` | `panel` | `(default)` |
| `sidebar` | `panel` | `(default)` |
<!-- chirpui:generated:end -->
