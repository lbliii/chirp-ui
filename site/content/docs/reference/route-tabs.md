---
title: Route tabs
description: tab_is_active and URL matching
draft: false
weight: 49
lang: en
type: doc
keywords: [chirp-ui, route_tabs, navigation]
icon: tabs
---

# Route tabs

## `tab_is_active`

Registered as a **template global** when the app supports **`template_global`** (Chirp).

```python
def tab_is_active(tab: dict | object, current_path: str) -> bool:
    ...
```

Each **tab** must provide:

- **`href`** (required) — URL path for the tab.
- **`match`** (optional) — `"exact"` (default) or `"prefix"`.

### Matching rules

- **`exact`** — `current_path == href`
- **`prefix`** — `current_path == href` **or** `current_path.startswith(href + "/")`

Use **`prefix`** for nested routes that should keep a parent tab highlighted.

## Templates

Import **`route_tabs`** / **`render_route_tabs`** from `chirpui/route_tabs.html` and pass **`current_path`** from the request (Chirp exposes this in page context).

## Related

- [Components: Tabs](../components/tabs.md)
- [App shell](../app-shell/_index.md)
