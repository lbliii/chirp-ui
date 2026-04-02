---
title: Navigation
description: sidebar, navbar, nav_tree, breadcrumbs, pagination, command_palette
draft: false
weight: 16
lang: en
type: doc
keywords: [chirp-ui, sidebar, navbar, breadcrumbs]
icon: navigation-arrow
---

# Navigation

Navigation components handle app-level wayfinding: sidebars, top bars, trees, breadcrumbs, pagination, command palettes, docks, and more. Most emit HTMX attributes for SPA-style transitions out of the box.

## Quick reference

| Template | Primary macro | Role |
|----------|--------------|------|
| `sidebar.html` | `sidebar()` | Vertical app nav rail |
| `navbar.html` | `navbar()` | Horizontal top bar |
| `nav_link.html` | `nav_link()` | SPA-style HTMX link primitive |
| `nav_tree.html` | `nav_tree()` | Hierarchical doc/settings nav |
| `breadcrumbs.html` | `breadcrumbs()` | Path trail |
| `pagination.html` | `pagination()` | HTMX page controls |
| `command_palette.html` | `command_palette()` | Cmd+K search overlay |
| `command_bar.html` | `command_bar()` | Dense action cluster bar |
| `dock.html` | `dock()` | macOS-style floating dock |
| `tree_view.html` | `tree_view()` | Hierarchical data display |

---

## Sidebar

Vertical sidebar with header, nav, and footer slots. Boosted links use `hx-select="#page-root"` to keep the page wrapper intact during SPA navigation.

### Macros

```text
sidebar(cls="")
sidebar_section(title="", collapsible=false, cls="")
sidebar_link(href, label, icon="", active=false, match="", boost=true, cls="")
shell_brand_link(href="/", cls="", boost=true)
shell_boosted_link(href, cls="", boost=true)
sidebar_toggle(cls="")
```

### Key parameters

| Param | On | Description |
|-------|----|-------------|
| `match` | `sidebar_link` | `"exact"` or `"prefix"` -- auto-compares `current_path` to `href` |
| `active` | `sidebar_link` | Explicit boolean override (skips `match` logic) |
| `icon` | `sidebar_link` | Passed through the `icon` filter |
| `collapsible` | `sidebar_section` | Wraps section in `<details>` for expand/collapse |
| `boost` | `sidebar_link`, `shell_brand_link`, `shell_boosted_link` | Emit HTMX boost attributes (default `true`) |

### Slots

- **`sidebar`**: `header`, default (nav content), `footer`
- **`shell_brand_link`**: default (brand HTML)
- **`shell_boosted_link`**: default (link HTML)

### Example

```text
{% from "chirpui/sidebar.html" import sidebar, sidebar_link, sidebar_section, shell_brand_link %}

{% call sidebar() %}
    {% slot header %}
        {% call shell_brand_link("/") %}My App{% end %}
    {% end %}
    {% call sidebar_section("Main", collapsible=true) %}
        {{ sidebar_link("/", "Home", icon="home", match="exact") }}
        {{ sidebar_link("/dashboard", "Dashboard", icon="grid", match="prefix") }}
    {% end %}
    {% slot footer %}<span>v1.0</span>{% end %}
{% end %}
```

---

## Navbar

Horizontal top navigation bar with brand, links, and optional right-aligned end section. Add `cls="chirpui-navbar--sticky"` for sticky positioning.

### Macros

```text
navbar(brand=none, brand_url="/", cls="", use_slots=false, brand_slot=false)
navbar_link(href, label, active=false, match="", cls="")
navbar_end(cls="")
navbar_dropdown(label, active=false, match="", href="", cls="")
```

### Key parameters

| Param | On | Description |
|-------|----|-------------|
| `brand` | `navbar` | Text brand name |
| `brand_slot` | `navbar` | Use a named `brand` slot instead of text (requires `use_slots=true`) |
| `use_slots` | `navbar` | Enable named slots (`end`, `brand`) for structured layout |
| `match` | `navbar_link`, `navbar_dropdown` | `"exact"` or `"prefix"` path matching |

### Example

```text
{% from "chirpui/navbar.html" import navbar, navbar_link, navbar_end %}

{% call navbar(brand="My App", brand_url="/", use_slots=true) %}
    {{ navbar_link("/docs", "Docs", match="prefix") }}
    {{ navbar_link("/about", "About", match="exact") }}
    {% slot end %}
        {{ btn("Login", href="/login") }}
    {% end %}
{% end %}
```

With a brand slot (logo component):

```text
{% call navbar(brand_url="/", use_slots=true, brand_slot=true) %}
    {% slot brand %}
        {{ logo(text="My App", image_src="/static/logo.svg", variant="both") }}
    {% end %}
    {{ navbar_link("/docs", "Docs", match="prefix") }}
{% end %}
```

---

## Nav link

A single SPA-style HTMX link. Emits `hx-boost`, `hx-target="#main"`, `hx-swap="innerHTML transition:true"`, and `hx-select="#page-content"`. Use for pagination links, interlinked content pages, or anywhere you want smooth in-shell transitions without a full reload.

### Macro

```text
nav_link(href, label="", cls="")
```

When `label` is empty, the default slot is used instead.

### Example

```text
{% from "chirpui/nav_link.html" import nav_link %}

{{ nav_link("/page-2", "Next page") }}

{% call nav_link("/details") %}View details &rarr;{% end %}
```

---

## Nav tree

Hierarchical navigation built on native `<details>` elements. Suited for docs sidebars, admin panels, and settings trees.

### Macro

```text
nav_tree(items, show_icons=false, cls="")
```

### Data format

`items` is a list of dicts. Each item can have:

| Key | Type | Description |
|-----|------|-------------|
| `title` | str | Display text |
| `href` | str | Link target (optional -- omit for non-link headings) |
| `children` | list | Nested items (triggers `<details>` expand/collapse) |
| `active` | bool | Marks as current page and auto-opens parent |
| `open` | bool | Force parent `<details>` open without active styling |
| `icon` | str | Icon name (requires `show_icons=true`) |

Slots: `header` (version selector, search, etc.).

### Example

```text
{% from "chirpui/nav_tree.html" import nav_tree %}

{% call nav_tree(items=[
    {"title": "Getting Started", "href": "/docs/start", "active": true},
    {"title": "API", "children": [
        {"title": "Routes", "href": "/docs/api/routes"},
        {"title": "Models", "href": "/docs/api/models"},
    ]},
], show_icons=false) %}
    {% slot header %}<input type="search" placeholder="Filter...">{% end %}
{% end %}
```

---

## Breadcrumbs

Navigation trail. The last item (no `href`) renders as the current page.

### Macro

```text
breadcrumbs(items, cls="")
```

`items` is a list of `{"label": str, "href": str?}`. Omit `href` on the final item.

### Example

```text
{% from "chirpui/breadcrumbs.html" import breadcrumbs %}

{{ breadcrumbs([
    {"label": "Home", "href": "/"},
    {"label": "Docs", "href": "/docs"},
    {"label": "Navigation"},
]) }}
```

---

## Pagination

HTMX-powered page navigation with windowed page numbers and ellipsis.

### Macro

```text
pagination(current, total, url_pattern, hx_target=none, hx_push_url=false,
           hx_swap="innerHTML", hx_select=none, window=2, cls="")
```

### Key parameters

| Param | Description |
|-------|-------------|
| `current` | Current page number (1-based) |
| `total` | Total number of pages |
| `url_pattern` | URL template with `{page}` placeholder (e.g. `"/items?page={page}"`) |
| `hx_target` | HTMX target selector; when set, links use `hx-get` instead of plain navigation |
| `hx_push_url` | Push URL to browser history on HTMX swap |
| `hx_select` | Narrow the swapped content to a selector |
| `window` | Number of page links to show on each side of current (default `2`) |

### Example

```text
{% from "chirpui/pagination.html" import pagination %}

{{ pagination(current=3, total=10, url_pattern="/items?page={page}",
              hx_target="#item-list", hx_push_url=true) }}
```

---

## Command palette

Cmd+K search overlay using native `<dialog>`. Results load via HTMX into the results container with a 200ms debounce.

### Macros

```text
command_palette(id="command-palette", search_url="/search", placeholder="Search...")
command_palette_trigger(target="command-palette", label="Search", cls="")
```

### Key parameters

| Param | On | Description |
|-------|----|-------------|
| `search_url` | `command_palette` | Endpoint that receives `?q=` queries via `hx-get` |
| `id` | `command_palette` | Dialog element ID (also used for results container) |
| `target` | `command_palette_trigger` | ID of the `command_palette` dialog to open |

### Example

```text
{% from "chirpui/command_palette.html" import command_palette, command_palette_trigger %}

{{ command_palette_trigger() }}
{{ command_palette(search_url="/api/search") }}
```

---

## Command bar

Dense action cluster bar built on `action_strip` with `role="toolbar"` semantics. Use for create/export/bulk-action toolbars.

### Macro

```text
command_bar(surface_variant="default", density="sm", wrap="wrap",
            sticky=false, aria_label="Command bar", cls="")
```

### Key parameters

| Param | Description |
|-------|-------------|
| `surface_variant` | Surface styling variant (passed to `action_strip`) |
| `density` | Spacing density (`"sm"`, etc.) |
| `sticky` | Pin bar to top on scroll |

### Example

```text
{% from "chirpui/command_bar.html" import command_bar %}

{% call command_bar(sticky=true) %}
    {{ btn("New", variant="primary") }}
    {{ btn("Export", variant="ghost") }}
    {{ btn("Delete", variant="danger") }}
{% end %}
```

---

## Dock

macOS-style floating dock with icon magnification on hover. Items can be links or buttons.

### Macro

```text
dock(items=none, variant="", size="", cls="")
```

### Key parameters

| Param | Description |
|-------|-------------|
| `items` | List of `{"icon", "label", "href?", "active?"}` -- when omitted, uses default slot |
| `variant` | `""` (default) or `"glass"` |
| `size` | `""`, `"sm"`, `"md"`, or `"lg"` |

### Example

```text
{% from "chirpui/dock.html" import dock %}

{{ dock(items=[
    {"icon": "home", "label": "Home", "href": "/"},
    {"icon": "search", "label": "Search", "href": "/search"},
    {"icon": "settings", "label": "Settings", "active": true},
], variant="glass", size="lg") }}
```

---

## Tree view

Hierarchical data display using native `<details>/<summary>` for expand/collapse. Unlike `nav_tree`, this is for displaying data hierarchies rather than navigation.

### Macro

```text
tree_view(nodes, cls="")
```

`nodes` is a list of `{"id", "label", "children"}` where `children` is a list of the same structure.

### Example

```text
{% from "chirpui/tree_view.html" import tree_view %}

{{ tree_view(nodes=[
    {"id": "1", "label": "src/", "children": [
        {"id": "1a", "label": "app.py", "children": []},
        {"id": "1b", "label": "models/", "children": [
            {"id": "1b1", "label": "user.py", "children": []},
        ]},
    ]},
    {"id": "2", "label": "tests/", "children": []},
]) }}
```

---

## Active state matching

Both `sidebar_link` and `navbar_link` support automatic active state via the `match` parameter. This requires `current_path` in the template context.

| Value | Behavior |
|-------|----------|
| `"exact"` | Active when `current_path == href` |
| `"prefix"` | Active when `current_path` starts with `href` |
| *(empty)* | Use `active=true/false` for manual control |

## App shell integration

Sidebars and navbars are composed inside [app shell layouts](../app-shell/_index.md). Boosted links (`shell_brand_link`, `shell_boosted_link`, `sidebar_link` with `boost=true`) emit `hx-select="#page-root"` targeting `#main` -- pages must render a `<div id="page-root">` wrapper. See [OOB updates](../app-shell/oob-updates.md) for swap details.

Use [Route tabs](./tabs.md) for section switching within a route. See [Shell regions](../app-shell/shell-regions.md) for placement guidance.
