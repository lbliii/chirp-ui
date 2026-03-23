---
title: Headers
description: page_header, section_header, entity_header, document_header, profile_header
draft: false
weight: 21
lang: en
type: doc
keywords: [chirp-ui, header, entity]
icon: text-align-left
---

# Headers

| Template | Role |
|----------|------|
| `layout.html` | `page_header`, `section_header`, `section_header_inline` |
| `entity_header.html` | Dashboard-grade entity title + metadata + actions |
| `document_header.html` | Document-style title row |
| `profile_header.html` | Profile / user header |
| `search_header.html` | Search-first chrome |

## Variants

`page_header` and `section_header` have registry entries (`page_header`, `section_header`).

## Layout

Headers include flex rules so title columns shrink safely — pair with [Layout overflow](../guides/layout-overflow.md) for long titles.

## Related

- [Navigation](./navigation.md)
