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

| Template | Role |
|----------|------|
| `sidebar.html` | App nav rail; `shell_brand_link`, `shell_boosted_link` |
| `navbar.html` | Top bar; `navbar_link`, `navbar_dropdown` |
| `nav_tree.html` | Hierarchical explorer |
| `nav_link.html` | Styled link primitive |
| `breadcrumbs.html` | Path trail |
| `pagination.html` | Page controls |
| `command_palette.html` | ⌘K-style launcher |
| `search_header.html` | Search chrome |

## App shell

Sidebars and navbars are composed inside [app shell layouts](../app-shell/_index.md). Use [Route tabs](./tabs.md) for section switching inside a route.

## HTMX

Boosted links and `hx-*` attributes work with `shell_boosted_link` patterns — see [OOB updates](../app-shell/oob-updates.md).

## Related

- [Shell regions](../app-shell/shell-regions.md)
