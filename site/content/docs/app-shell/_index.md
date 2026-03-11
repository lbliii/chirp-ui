---
title: App Shell
description: Sidebar, breadcrumbs, command palette, and layout patterns
draft: false
weight: 40
lang: en
type: doc
keywords: [chirp-ui, app shell, sidebar, breadcrumbs, layout]
category: app-shell
---

# App Shell

**Quick start:** Extend `chirpui/app_shell_layout.html` and fill the blocks. No manual HTML boilerplate.

```html
{% extends "chirpui/app_shell_layout.html" %}
{% block brand %}My App{% end %}
{% block sidebar %}
  {% from "chirpui/sidebar.html" import sidebar, sidebar_link, sidebar_section %}
  {% call sidebar() %}
    {% call sidebar_section("Main") %}
      {{ sidebar_link("/", "Home") }}
      {{ sidebar_link("/items", "Items") }}
    {% end %}
  {% end %}
{% end %}
```

## Components

- **sidebar** — Collapsible navigation with sections
- **breadcrumbs** — Path navigation
- **command_palette** — Cmd+K search
- **toast_container** — Toast notifications
- **shell_actions** — Route-scoped topbar actions that update automatically on navigation

### shell_actions

Route-scoped topbar actions (buttons, links, menus) that update automatically
when navigating via htmx boost (sidebar) or tab clicks (hx-target #main or #page-root).

When extending `chirpui/app_shell_layout.html`, `shell_actions` is provided by
the layout chain from Chirp's merged `_context.py` results. When using the
`app_shell()` macro, pass it explicitly:

```html
{% call app_shell(brand="My App", shell_actions=shell_actions | default(none)) %}
  ...
{% end %}
```

The rendering macro is `shell_actions_bar(shell_actions)` from
`chirpui/shell_actions.html`. See [Chirp's app-shell guide](https://lbliii.github.io/chirp/docs/guides/app-shell/#shell-actions)
for the full cascade/override pattern (primary, controls, overflow zones;
`remove=`; `mode="replace"`).

**Design:** Prefer shell_actions for actions that apply across the whole section (e.g. "New Chain" on Discover). Page-level action strips are better for actions that only apply to the current tab. Avoid duplicating the same action in both.

**Tabbed layout:** Tabs are topmost. Put title, action strips, and content underneath (inside page_content). Order: Tabs → Title → Actions → Content.

### route_tabs and tabbed_page_layout

For route-backed subsection tabs (e.g. Workspace → Analytics, Events, Logs), use `route_tabs` from `chirpui/route_tabs.html`:

```html
{% from "chirpui/route_tabs.html" import route_tabs %}
{{ route_tabs(tabs, current_path, target="#page-root") }}
```

Tab items: `{label, href, icon?, badge?, match?}`. `match`: `"exact"` or `"prefix"`. ChirpUI registers `tab_is_active` as a template global via `use_chirp_ui()`.

For the full tabbed layout structure (container → #page-root → route-tabs + page-content-inner), use `tabbed_page_layout` from `chirpui/tabbed_page_layout.html`:

```html
{% from "chirpui/tabbed_page_layout.html" import tabbed_page_layout %}
{% call tabbed_page_layout(tabs=route_tabs, current_path=current_path) %}
  {% slot page_header %}{{ page_header("Section Title") }}{% end %}
  {% slot page_toolbar %}{% end %}
  {% slot page_content %}...{% end %}
{% end %}
```

See [Chirp's chirp-ui guide](https://lbliii.github.io/chirp/docs/guides/chirp-ui/) for full app-shell patterns and htmx integration.

### HTMX fragment targets

ChirpUI registers three fragment targets via `use_chirp_ui()`. When an HTMX request includes `HX-Target`, Chirp uses the registry to choose which template block to render:

| Target | Block | Use case |
|--------|-------|----------|
| `#main` | `page_root` | Sidebar navigation (full content + tabs) |
| `#page-root` | `page_root_inner` | Tab clicks (tabs + content) |
| `#page-content-inner` | `page_content` | Narrow content swaps |

Sidebar links use `hx-target="#main"` by default. Section tab links use `hx-target="#page-root"`. For custom targets, use `app.register_fragment_target("target-id", fragment_block="block_name")` before `mount_pages()`. Set `triggers_shell_update=False` for narrow content swaps that should not update the topbar (e.g. inline form results).

### Polling shell regions

Use `poll_trigger()` from `chirpui/fragment_island.html` when a shell region
needs a delayed or load-triggered refresh without visible UI chrome:

```html
{% from "chirpui/fragment_island.html" import poll_trigger %}

<div id="shell-status"></div>
{{ poll_trigger("/status/summary", "#shell-status") }}
{{ poll_trigger("/status/summary?refresh=1", "#shell-status", delay="2s") }}
```

This keeps the polling markup consistent with the rest of the app-shell and
avoids repeating hidden `hx-get` button boilerplate across templates.
