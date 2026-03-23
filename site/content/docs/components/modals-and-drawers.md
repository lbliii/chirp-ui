---
title: Modals and drawers
description: modal, drawer, tray, confirm, popover, tooltip
draft: false
weight: 14
lang: en
type: doc
keywords: [chirp-ui, modal, drawer, tray]
icon: bounding-box
---

# Modals and drawers

Overlay UI for focused tasks and transient panels.

| Template | Role |
|----------|------|
| `modal.html` / `modal_overlay.html` | Dialog centered in viewport |
| `drawer.html` | Edge sheet (often right) |
| `tray.html` | Bottom / compact tray |
| `confirm.html` | Destructive or high-friction confirmation |
| `popover.html` | Anchored floating panel |
| `tooltip.html` | Small hint; variant registry `tooltip` (placement) |

## Sizes

`modal` uses `SIZE_REGISTRY["modal"]`: `small`, `medium`, `large`.

## Alpine

Dropdowns, modals, and trays typically use Alpine for open/close. Chirp injects Alpine; see [Alpine integration](../concepts/alpine-integration.md).

## Related

- [Alerts](./alerts-and-feedback.md) — toast for async feedback after close
- [HTMX patterns](../guides/htmx-patterns.md) — swapping modal content
