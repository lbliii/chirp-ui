---
title: Tabs
description: route_tabs, tabs, tabs_panels, tabbed_page_layout
draft: false
weight: 17
lang: en
type: doc
keywords: [chirp-ui, tabs, route_tabs]
icon: tabs
---

# Tabs

Two families:

1. **URL-driven** — `route_tabs.html` with `render_route_tabs` for navigation that matches the current path.
2. **Client panels** — `tabs.html` / `tabs_panels.html` for panel switching without full navigation.

`tabbed_page_layout.html` wraps page chrome around HTMX targets for multi-section pages.

## Route tabs

Use `tab_is_active` (template global from Chirp registration) to style the active tab. See [Route tabs reference](../reference/route-tabs.md).

## Related

- [App shell](../app-shell/_index.md) — where tabs often live
- [Tabs vs panels](https://github.com/lbliii/chirp-ui/blob/main/docs/COMPONENT-OPTIONS.md) in repo docs for import paths
