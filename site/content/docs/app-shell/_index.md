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
when navigating between pages via htmx boost.

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

See [Chirp's chirp-ui guide](https://lbliii.github.io/chirp/docs/guides/chirp-ui/) for full app-shell patterns and htmx integration.

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
