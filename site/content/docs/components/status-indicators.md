---
title: Status indicators
description: badge, status, live_badge, notification_dot
draft: false
weight: 22
lang: en
type: doc
keywords: [chirp-ui, badge, status]
icon: circle-wavy
---

# Status indicators

| Template | Role |
|----------|------|
| `badge.html` | Small labels (`badge` variants; includes custom chip colors via `resolve_color`) |
| `status.html` / `status_with_hint.html` | Status line + hint |
| `live_badge.html` | Live / realtime affordance |
| `notification_dot.html` | Pulsing dot (`notification-dot` sizes) |
| `progress.html` | Determinate bar (`progress-bar`) |

## Colors

Use `resolve_color` / `register_colors` for semantic palettes — see [Color system](../theming/color-system.md).

## Related

- [Alerts](./alerts-and-feedback.md)
