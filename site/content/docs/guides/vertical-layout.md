---
title: Vertical layout
description: Full-height main and inner scroll regions
draft: false
weight: 39
lang: en
type: doc
keywords: [chirp-ui, layout, flex, chat]
icon: arrows-vertical
---

# Vertical layout

Two modes for the **block axis** (height):

| Mode | `#main` scroll | Typical use |
|------|----------------|-------------|
| **Default** | Yes (`overflow-y: auto`) | Long content, lists, docs |
| **Fill** | No (`overflow: hidden`); inner scroll | Chat, maps, split editors |

## Fill mode

1. On layouts extending `chirpui/app_shell_layout.html`, append **`chirpui-app-shell__main--fill`** via `{% block main_shell_class %}`.
2. Wrap route body in a direct child of `#page-content` with class **`chirpui-page-fill`**.

## Chat layout

Use **`{% call chat_layout(..., fill=true) %}`** so the root gets **`chirpui-chat-layout--fill`**. Messages wrappers may need **`chirpui-chat-layout__messages-body`** for flex + scroll.

## Why `min-height: 0`

Flex/grid children default to `min-height: auto`, which can block shrinking. Any region that should scroll internally needs **`min-height: 0`** (or an ancestor with `overflow: hidden`).

## HTMX

`app_shell_layout.html` can sync **`chirpui-app-shell__main--fill`** after boosted navigation when `#page-content` contains **`chirpui-page-fill`**.

## Related

- [Layout overflow](./layout-overflow.md)
- [App shell](../app-shell/_index.md)
