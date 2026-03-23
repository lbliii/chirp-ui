---
title: Alerts and feedback
description: alert, toast, callout, empty, skeleton, spinner, progress
draft: false
weight: 15
lang: en
type: doc
keywords: [chirp-ui, alert, toast, skeleton]
icon: bell-ringing
---

# Alerts and feedback

| Template | Role |
|----------|------|
| `alert.html` | Inline status message (`VARIANT_REGISTRY["alert"]`) |
| `toast.html` | Transient notifications (`toast` variants) |
| `callout.html` | Prose-adjacent emphasis |
| `empty.html`, `empty_panel_state.html` | Zero-data states |
| `skeleton.html` | Loading placeholders (`skeleton` variants) |
| `spinner.html` | Indeterminate busy |
| `progress.html` | Determinate progress (`progress-bar` variants/sizes) |

## Toast container

Use `toast_container` where htmx or Alpine injects new toasts. Pair with server events or `HX-Trigger` headers in Chirp routes.

## Related

- [Status indicators](./status-indicators.md) — badges and live dots
- [Security](../guides/security.md) — never pass untrusted HTML into alerts
