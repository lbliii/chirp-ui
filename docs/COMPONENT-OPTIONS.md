# chirp-ui Component Options Reference

Valid variant, size, and option values for chirp-ui components. When **strict mode** is enabled (e.g. `app.debug=True` with Chirp's `use_chirp_ui`), invalid values log warnings and fall back to defaults.

See [Strict mode](#strict-mode) for setup.

---

## Macro Slot Context

Components that use `{% slot %}` (e.g. `form`, `card`, `card_link`, `field_wrapper`) render slot content in the **caller's context**. Page variables passed to the handler (e.g. `selected_tags`, `q`) are available inside macro slots without `| default()`.

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

With `with-button`, the input flexes to fill space; the button stays compact.

Use `| default()` for optional variables that may be unset on first load (e.g. `selected_tags | default([])` when the handler may omit the key). Variables used inside macro slots must be in the page context — Chirp passes handler context through to `render_block()`.

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
| **logo** | `variant` | text, image, both | both |
| **logo** | `size` | sm, md, lg | md |
| **logo** | `align` | start, center, end | center |

---

## Fragment Island and DnD Primitives

| Component | Description |
|-----------|-------------|
| `fragment_island` | HTMX-safe mutation region; wraps content with `hx-disinherit` to avoid inherited shell attributes |
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

---

## Layout (layout.html)

### page_header

| Param | Description |
|-------|-------------|
| `title` | Page title (h1) |
| `subtitle` | Optional subtitle |
| `meta` | Optional meta line (e.g. config path) — muted, below subtitle |
| `breadcrumb_items` | Optional list of `{label, href?}` for breadcrumbs above title |

### section

Composite: surface + section_header + content. Reduces boilerplate.

```html
{% from "chirpui/layout.html" import section %}
{% call section("Set config value", surface_variant="muted") %}
  ...
{% end %}
```

| Param | Description |
|-------|-------------|
| `title` | Section heading (h2) |
| `subtitle` | Optional |
| `surface_variant` | default, muted, elevated, accent, gradient-subtle, gradient-accent, gradient-border, gradient-mesh, glass, frosted, smoke (default: muted) |
| `full_width` | If true, wraps in `chirpui-blade` for edge-to-edge layout (breaks out of container) |
| `parallax` | If true with full_width, adds subtle scroll-driven animation (Chrome 115+); respects prefers-reduced-motion |

### section_header_inline

Compact header for dense forms: h2 + actions on one line, no subtitle.

### section_collapsible

`details`/`summary` with section_header as summary. For "Advanced" config blocks.

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
Optional controls/actions are passed in the default slot using action-strip zone classes.

```html
{% from "chirpui/search_header.html" import search_header %}
{{ search_header("Skills", "/skills", query=q, subtitle="Search and filter skills") }}
```

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

---

## Filters

- **`bem(block, variant="", modifier="", cls="")`** — Builds BEM class string; validates `variant` against `VARIANT_REGISTRY` when strict.
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
