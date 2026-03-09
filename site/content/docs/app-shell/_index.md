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

See [Chirp's chirp-ui guide](https://lbliii.github.io/chirp/docs/guides/chirp-ui/) for full app-shell patterns and htmx integration.
