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

Two families of tab components plus a page-level layout wrapper.

1. **URL-driven** -- `route_tabs.html` with `render_route_tabs` for navigation that matches the current path. Each tab loads a new URL.
2. **Client panels** -- `tabs.html` (htmx-powered) and `tabs_panels.html` (Alpine.js) for panel switching without full navigation.
3. **Page layout** -- `tabbed_page_layout.html` wraps page chrome around HTMX targets for multi-section pages.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `tabs.html` | `tabs`, `tab` | htmx-powered tab switching |
| `tabs_panels.html` | `tabs_container`, `tab`, `tab_panel` | Client-side Alpine.js panel switching |
| `route_tabs.html` | `render_route_tabs`, `route_tabs` | URL-driven navigation tabs |
| `tabbed_page_layout.html` | `tabbed_page_layout` | Full page layout with route tabs |

## tabs / tab (htmx)

Tab bar where each tab fires an htmx request to swap content into a target container.

```text
{% from "chirpui/tabs.html" import tabs, tab %}

{% call tabs(active="overview") %}
  {{ tab("overview", "Overview", url="/tabs/overview", hx_target="#content", active=true) }}
  {{ tab("details", "Details", url="/tabs/details", hx_target="#content") }}
{% end %}

<div id="content">... loaded via htmx ...</div>
```

### tabs params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `active` | `str` | `none` | Currently active tab ID (for reference) |
| `cls` | `str` | `""` | Extra CSS classes |

### tab params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | required | Unique tab identifier |
| `label` | `str` | required | Tab display text |
| `url` | `str` | `none` | URL for htmx fetch |
| `hx_target` | `str` | `none` | htmx target selector (enables htmx attributes) |
| `hx_swap` | `str` | `"innerHTML"` | htmx swap strategy |
| `active` | `bool` | `false` | Whether this tab is active |
| `cls` | `str` | `""` | Extra CSS classes |

When `hx_target` is set, the tab renders with `hx-boost="false"`, `hx-select="unset"`, `hx-get`, `hx-target`, `hx-swap`, and `hx-push-url="false"`.

## tabs_container / tab / tab_panel (Alpine.js)

Client-side panel switching using Alpine.js `x-data` and `x-show`. No server requests.

```text
{% from "chirpui/tabs_panels.html" import tabs_container, tab, tab_panel %}

{% call tabs_container(active="overview") %}
  {{ tab("overview", "Overview", active=true) }}
  {{ tab("details", "Details") }}
  {% call tab_panel("overview", active=true) %}
    Overview content here.
  {% end %}
  {% call tab_panel("details") %}
    Details content here.
  {% end %}
{% end %}
```

### tabs_container params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `active` | `str` | `none` | Initially active tab ID |

### tab params (panels)

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | required | Unique tab identifier |
| `label` | `str` | required | Tab display text |
| `active` | `bool` | `false` | Initial active state |

Tabs use `@click` to set `active` and dispatch `chirpui:tab-changed`.

### tab_panel params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | required | Panel identifier (matches tab `id`) |
| `active` | `bool` | `false` | Initial visibility |

Panels use `x-show` with `x-transition` and `x-cloak`.

## render_route_tabs

URL-driven navigation tabs with `aria-current="page"`. Uses htmx for boosted swaps that target `#page-root`.

```text
{% from "chirpui/route_tabs.html" import render_route_tabs %}

{{ render_route_tabs(
    tab_items=[
        {"label": "Overview", "href": "/project/overview"},
        {"label": "Settings", "href": "/project/settings", "icon": "gear"},
        {"label": "Members", "href": "/project/members", "badge": "5"},
    ],
    current_path=request.path,
    target="#main"
) }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `tab_items` | `list[dict]` | required | Tab definitions: `{label, href, icon?, badge?, match?}` |
| `current_path` | `str` | required | Current URL path for active detection |
| `target` | `str` | `"#main"` | htmx target selector |
| `is_active` | `callable` | `none` | Custom active-check function (defaults to `tab_is_active` template global) |

Each tab item supports:
- `label` -- display text (required)
- `href` -- URL (required)
- `icon` -- optional leading icon
- `badge` -- optional trailing badge
- `match` -- `"exact"` or `"prefix"` for active detection

`route_tabs(tabs, current_path, ...)` is an alias for `render_route_tabs`.

## tabbed_page_layout

Full page layout that combines `container`, `stack`, and `render_route_tabs`. Supports both block-based (extends) and macro-based (call) usage.

**Block-based usage (recommended):**

```text
{% extends "chirpui/tabbed_page_layout.html" %}

{% block page_header %}{{ page_header("Project") }}{% end %}
{% block page_toolbar %}{% end %}
{% block page_content %}
  ... page body ...
{% end %}
```

**Macro-based usage:**

```text
{% from "chirpui/tabbed_page_layout.html" import tabbed_page_layout %}

{% call tabbed_page_layout(tab_items=tabs, current_path=request.path) %}
  {% slot page_header %}{{ page_header("Project") }}{% end %}
  {% slot page_content %}... page body ...{% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `tab_items` | `list[dict]` | `none` | Tab definitions for `render_route_tabs` |
| `tabs` | `list[dict]` | `none` | Alias for `tab_items` |
| `current_path` | `str` | `"/"` | Current URL path |
| `tab_target` | `str` | `"#main"` | htmx target for tab navigation |

**Blocks/Slots:** `page_header`, `page_toolbar`, `page_content`.

The layout renders `<div id="page-root">` at the outermost level so `hx-select="#page-root"` preserves the container structure during boosted swaps.

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-tabs` | Tab bar / container |
| `chirpui-tab` | Individual tab link |
| `chirpui-tab--active` | Active tab |
| `chirpui-tabs__tab` | Panel tab button |
| `chirpui-tabs__tab--active` | Active panel tab |
| `chirpui-tab-panel` | Panel content area |
| `chirpui-route-tabs` | Route tabs nav |
| `chirpui-route-tab` | Route tab link |
| `chirpui-route-tab--active` | Active route tab |
| `chirpui-route-tab__icon` | Tab icon |
| `chirpui-route-tab__badge` | Tab badge |

## Related

- [App shell](../app-shell/_index.md) -- where tabs often live
- [Route tabs reference](../reference/route-tabs.md)
