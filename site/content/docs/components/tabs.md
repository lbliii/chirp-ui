---
title: Tabs anatomy
description: Rendered anatomy and behavior contracts for htmx tabs, tab panels, and route tabs
draft: false
weight: 26
lang: en
type: doc
keywords: [chirp-ui, tabs, route tabs, htmx, alpine, anatomy]
search_keywords:
  - tab
  - tabs
  - tab panel
  - tabbed
  - route tabs
  - segmented control
  - tab bar
  - tab navigation
category: components
---

# Tabs anatomy

Chirp UI ships three tab-like contracts:

- `tabs(...)` and `tab(...)` from `chirpui/tabs.html`
- `tabs_container(...)`, `tab_button(...)`, and `tab_panel(...)` from `chirpui/tabs_panels.html`
- `render_route_tabs(...)` and `route_tabs(...)` from `chirpui/route_tabs.html`

Route tabs are URL-backed navigation links with `role="navigation"` and
`aria-current="page"`. They are not ARIA tab widgets. Client-side tab panels
use the `chirpuiTabs()` Alpine controller and escaped `data-tab-id` attributes.

The full rendered contract, ARIA roles, htmx behavior, Alpine behavior, route
tab semantics, and proof locations live in the canonical source guide:
[`docs/components/tabs-anatomy.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/components/tabs-anatomy.md?plain=1).
