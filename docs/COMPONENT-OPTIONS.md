# chirp-ui Component Options Reference

Valid variant, size, and option values for chirp-ui components. When **strict mode** is enabled (e.g. `app.debug=True` with Chirp's `use_chirp_ui`), invalid values log warnings and fall back to defaults.

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
| arrow, migrate, config | ▸ |
| wizard, diamond, settings | ◇ |
| gear | ⚙ |
| bullet | ● |
| star | ★ |
| spark | ✦ |
| logs | ⟳ |
| cloud | ☁ |
| sources | ⊞ |
| chain | ⛓ |
| link | ⟶ |
| alert | ↑ |
| dots | ⋯ |

Unknown names pass through unchanged. Use `{{ "custom" | icon }}` in templates when needed.

---

## Components with Variants

| Component | Param | Valid values | Default |
|-----------|-------|--------------|---------|
| **alert** | `variant` | info, success, warning, error | info |
| **badge** | `variant` | primary, success, warning, error, muted, info | — |
| **surface** | `variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke | default |
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
| `shell_outlet_attrs` | Standard hx-boost/hx-target/hx-swap/hx-select attributes for main |
| `shell_region` | Persistent region container (id for OOB updates) |
| `safe_region` | HTMX-safe mutation region; `hx-disinherit` to avoid inherited shell attributes |
| `fragment_island` | Alias for `safe_region`; use either |

## JavaScript Dependencies

Interactive components require **Alpine.js** (loaded before chirp-ui components). Use `chirpui.js` for theme/style init only.

| Template / Component | Required JS | Notes |
|---------------------|-------------|-------|
| `dropdown_menu.html` | Alpine.js | `x-data`, `x-show`, `@click.outside`, `x-transition` |
| `modal.html` | Alpine.js (optional) | `modal_trigger` uses `@click`; native `<dialog>` for modal |
| `modal_overlay.html` | Alpine.js | Overlay behavior |
| `tray.html` | Alpine.js | Slide-in panel |
| `tabs_panels.html` | Alpine.js | Tab switching |
| `theme_toggle.html` | Alpine.js | Theme/style persistence |
| `copy_button.html` | Alpine.js | Copy-to-clipboard |
| `forms.html` (masked_field, phone_field, money_field) | Alpine.js + @alpinejs/mask | `x-mask`, `x-mask:dynamic` |
| `chirpui.js` | — | Pre-paint theme/style init only |

**Static path:** Include `chirpui.css` and `chirpui.js` from `chirp_ui.static_path()`. Use `use_chirp_ui(app)` with Chirp for automatic registration.

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
| `sticky_header` | Adds chirpui-table-wrap--sticky for sticky thead |
| `actions_header` | Adds empty th for row actions column |

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
| `cols` | `2`, `3`, `4`, or omitted for auto-fit |
| `gap` | `sm`, `md`, `lg` |
| `cls` | Optional additional classes |

Use `grid()` for two-dimensional layout rhythm. Prefer `gap="md"` for page content and `gap="sm"` for denser internal layouts.

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

Use `panel()` when a region needs its own chrome and scroll behavior inside a larger page or workspace. This is the preferred primitive for activity rails, file explorers, and inspector panes.

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

Use `file_tree()` for CMS and IDE-like explorer rails where you want panel chrome and tree behavior together. For raw tree markup without panel chrome, keep using `nav_tree()`.

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
| `detail` | Right column; rendered as `<code>` when contains "dori " (command), else plain text |
| `status_variant` | Override badge variant: success, error, muted, primary |

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

## Usage Notes

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

{% from "chirpui/toast.html" import toast %}
{{ toast("Done!", variant="success") }}
```

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

```html
{% from "chirpui/donut.html" import donut %}
{{ donut(value=75, max=100, label="75%") }}
{{ donut(value=3, max=5, label="3/5", variant="success") }}
```

---

## Sidebar

Sidebar navigation for dashboards and app shells. Use `sidebar`, `sidebar_section`, `sidebar_link`, and `sidebar_toggle` from `chirpui/sidebar.html`.

### Macros

| Macro | Params | Description |
|-------|--------|-------------|
| `sidebar` | `cls` | Container with header, nav, footer slots |
| `sidebar_section` | `title`, `collapsible`, `cls` | Section group; `collapsible=true` uses details/summary |
| `sidebar_link` | `href`, `label`, `icon`, `active`, `cls` | Nav link; `icon` recommended for collapsible mode |
| `sidebar_toggle` | `cls` | Toggle button for icon-only collapsed state |

### Usage

```html
{% from "chirpui/sidebar.html" import sidebar, sidebar_section, sidebar_link %}
{% call sidebar() %}
  {% call sidebar_section("Navigate") %}
    {{ sidebar_link("/", "Home", icon="◉", active=cp == "/") }}
    {{ sidebar_link("/skills", "Skills", icon="✦", active=cp.startswith("/skills")) }}
  {% end %}
  {% call sidebar_section("Settings") %}
    {{ sidebar_link("/settings", "Config", icon="◇", active=cp.startswith("/settings")) }}
  {% end %}
{% end %}
```

### app_shell

Full-page shell with topbar, sidebar, and main content. Params: `brand`, `brand_url`, `sidebar_collapsible`, `topbar_variant`, `sidebar_variant`, `cls`.

| Param | Valid values | Default |
|-------|--------------|---------|
| `topbar_variant` | default, glass, gradient | default |
| `sidebar_variant` | default, glass, muted | default |

Glass variants use `backdrop-filter`; gradient topbar uses `--chirpui-gradient-subtle`.

### Collapsible sidebar

Enable via `app_shell(sidebar_collapsible=true)` or override `{% block sidebar_collapsible %}true{% end %}` in `app_shell_layout`. Collapsed mode shows icons only; provide `icon` for each `sidebar_link`.

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
