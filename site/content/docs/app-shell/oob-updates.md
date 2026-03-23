---
title: OOB updates
description: HTMX out-of-band swaps for shell chrome
draft: false
weight: 42
lang: en
type: doc
keywords: [chirp-ui, htmx, oob]
icon: arrows-split
---

# OOB updates

When building **app-shell** navigation with htmx, you may need to update **sidebar**, **breadcrumbs**, or **title** regions outside the main content swap.

## Pattern

Return **multiple fragments** in one response using htmx **out-of-band** swaps (`hx-swap-oob`) for shell elements, while the primary swap targets **`#page-content`** or your boosted region.

## View Transitions

Include **`chirpui-transitions.css`** and follow comments in that file — certain shell nodes may need **`view-transition-name: none`** to avoid duplicate transition names during OOB swaps.

## Chirp

Chirp’s app-shell examples and the **chirp-app-shell-oob** skill cover AST-driven OOB updates — align your route responses with the shell IDs your layout exposes.

## Related

- [App shell](./_index.md)
- [HTMX patterns](../guides/htmx-patterns.md)
