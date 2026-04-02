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

Small visual cues for state, labels, live presence, and notifications. Supports semantic variants and custom colors via `resolve_color`.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `badge.html` | `badge` | Small label with semantic variant or custom color |
| `status.html` | `status_indicator` | Dot or icon + label status line |
| `status_with_hint.html` | `status_with_hint` | Badge with tooltip hint |
| `live_badge.html` | `live_badge` | "LIVE" pill with optional viewer count |
| `notification_dot.html` | `notification_dot` | Pulsing dot overlay for any element |
| `trending_tag.html` | `trending_tag` | Hashtag with count and trend indicator |

## badge

Small status label with semantic variants, custom colors, optional icon, and link support. Custom colors use `resolve_color` and `contrast_text` for accessible fills.

```text
{% from "chirpui/badge.html" import badge %}

{{ badge("Active", variant="success") }}
{{ badge("Grass", color="#78c850") }}
{{ badge("Fire", color="fire", fill="solid") }}
{{ badge("Tag", href="/tags/x", icon="tag") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | `str` | required | Badge label |
| `variant` | `str` | `"primary"` | Validated against `badge` registry |
| `icon` | `str` | `none` | Leading icon (passed through `| icon`) |
| `cls` | `str` | `""` | Extra CSS classes |
| `color` | `str` | `none` | Custom color (hex or registered name) |
| `fill` | `str` | `"subtle"` | `"subtle"` (tinted bg) or `"solid"` (filled bg, auto contrast text) |
| `href` | `str` | `none` | Renders as `<a>` link instead of `<span>` |

When `color` is set, the badge uses `--chirpui-badge-color` custom property. With `fill="solid"`, `--chirpui-badge-text` is auto-calculated for contrast.

## status_indicator

Visual status with a colored dot (or icon) and label. Supports custom colors and a pulsing animation.

```text
{% from "chirpui/status.html" import status_indicator %}

{{ status_indicator("Running", variant="success") }}
{{ status_indicator("Pending", variant="warning", pulse=true) }}
{{ status_indicator("Live", color="#78c850") }}
{{ status_indicator("Error", variant="error", icon="!") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `label` | `str` | required | Status text |
| `variant` | `str` | `"default"` | Validated against `status-indicator` registry |
| `icon` | `str` | `none` | Replaces the dot with a custom icon |
| `pulse` | `bool` | `false` | Adds pulsing animation |
| `cls` | `str` | `""` | Extra CSS classes |
| `color` | `str` | `none` | Custom color (uses `--chirpui-status-color`) |

## status_with_hint

Badge with an optional tooltip for extra context. Wraps `badge` inside `tooltip` when `hint` is provided.

```text
{% from "chirpui/status_with_hint.html" import status_with_hint %}

{{ status_with_hint("Active", variant="success", hint="Last active 2 hours ago") }}
{{ status_with_hint("Pending", variant="warning", hint="Waiting for approval", icon="clock") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `text` | `str` | required | Badge label |
| `variant` | `str` | `"primary"` | Badge variant |
| `hint` | `str` | `none` | Tooltip text (no tooltip if omitted) |
| `icon` | `str` | `none` | Badge icon |
| `cls` | `str` | `""` | Extra CSS classes |

## live_badge

"LIVE" pill with a pulsing red dot and optional viewer count.

```text
{% from "chirpui/live_badge.html" import live_badge %}

{{ live_badge() }}
{{ live_badge(viewers="2.4K") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `viewers` | `str` | `none` | Viewer count display |
| `cls` | `str` | `""` | Extra CSS classes |

## notification_dot

Wraps any element with a pulsing notification indicator. Optionally shows a count inside the dot.

```text
{% from "chirpui/notification_dot.html" import notification_dot %}

{% call notification_dot(variant="error") %}
  <button>Inbox</button>
{% end %}

{% call notification_dot(variant="success", count=3, size="lg") %}
  <span>Messages</span>
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `variant` | `str` | `""` | `"default"`, `"error"`, `"success"`, `"warning"` |
| `size` | `str` | `""` | `"sm"`, `"md"`, `"lg"` |
| `count` | `int` | `none` | Number inside the dot |
| `cls` | `str` | `""` | Extra CSS classes |

The default slot wraps the target element.

## trending_tag

Hashtag pill with optional post count and trend direction arrow.

```text
{% from "chirpui/trending_tag.html" import trending_tag %}

{{ trending_tag(tag="python", href="/tag/python", count="12.5K") }}
{{ trending_tag(tag="webdev", count="8.2K", trend="up") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `tag` | `str` | required | Tag name (rendered with `#` prefix) |
| `href` | `str` | `none` | Link URL (renders as `<a>`) |
| `count` | `str` | `none` | Post/usage count |
| `trend` | `str` | `none` | Trend modifier class (e.g. `"up"`) |
| `cls` | `str` | `""` | Extra CSS classes |

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-badge` | Badge element |
| `chirpui-badge--primary/success/warning/error/muted` | Semantic variants |
| `chirpui-badge--custom` | Custom color (subtle fill) |
| `chirpui-badge--custom-solid` | Custom color (solid fill) |
| `chirpui-status-indicator` | Status wrapper |
| `chirpui-status-indicator__dot` | Status dot |
| `chirpui-status-indicator--pulse` | Pulsing animation |
| `chirpui-live-badge` | Live badge |
| `chirpui-live-badge__dot` | Pulsing red dot |
| `chirpui-notification-dot` | Notification wrapper |
| `chirpui-notification-dot__ping` | Ping animation |
| `chirpui-notification-dot--error/success/warning` | Variant colors |
| `chirpui-trending-tag` | Trending tag pill |

## Colors

Use `resolve_color` / `register_colors` for semantic palettes. See [Color system](../theming/color-system.md).

## Related

- [Alerts and feedback](./alerts-and-feedback.md)
