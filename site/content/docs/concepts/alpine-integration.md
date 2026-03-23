---
title: Alpine integration
description: How chirp-ui uses Alpine.js with Chirp
draft: false
weight: 50
lang: en
type: doc
keywords: [chirp-ui, alpine, htmx, chirp]
icon: lightning
---

# Alpine integration

Interactive chirp-ui pieces (dropdowns, modals, trays, tabs, inline state) use **Alpine.js** via `x-data` and related attributes. **Chirp** injects Alpine when `alpine=True` on the app config; `use_chirp_ui(app)` enables Alpine by default for convenience.

## Ownership

- **Chirp** owns Alpine script injection and lifecycle.
- **chirp-ui** does not ship inline `<script>` blocks in macros — only attributes and optional `chirpui.js` for theme/style bootstrapping.

## Named components

For htmx-safe behavior across full loads and boosted navigation, register Alpine data with **`Alpine.safeData`** (provided by Chirp) for named component factories.

## Events

Some components dispatch **custom events** for coordination (open/close, selection). See [Alpine magics](https://github.com/lbliii/chirp-ui/blob/main/docs/ALPINE-MAGICS.md) in the repository for a concise list.

## htmx + Alpine

When a fragment swaps in new HTML, ensure Alpine **initializes** on the new nodes (Chirp’s integration handles common cases). For complex islands, prefer `fragment_island` patterns in [HTMX patterns](../guides/htmx-patterns.md).
