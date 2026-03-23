---
title: Components
description: Layout, UI, forms, streaming, and dashboard components
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, components, layout, cards, forms, modal]
category: components
---

# Components

chirp-ui ships many Kida templates under `chirpui/`. Import with `{% from "chirpui/...." import ... %}` and compose with `{% call %}`.

## Reference by category

| Topic | Page |
|-------|------|
| **Layout** | [Layout](./layout.md) — container, grid, frame, stack, cluster, block, headers |
| **Cards** | [Cards](./cards.md) — card, glow, spotlight, index, config |
| **Buttons** | [Buttons](./buttons.md) — btn, icon, shimmer, ripple, pulsing, split, copy |
| **Modals & drawers** | [Modals and drawers](./modals-and-drawers.md) — modal, drawer, tray, confirm, popover, tooltip |
| **Alerts** | [Alerts and feedback](./alerts-and-feedback.md) — alert, toast, empty, skeleton, spinner, progress |
| **Navigation** | [Navigation](./navigation.md) — sidebar, navbar, breadcrumbs, pagination, command palette |
| **Tabs** | [Tabs](./tabs.md) — route_tabs, tabs, tabbed layout |
| **Forms** | [Forms](./forms.md) — fields, fieldset, form_actions |
| **Tables & data** | [Tables and data](./tables-and-data.md) — table, description_list, tree, sortable |
| **Charts & stats** | [Charts and stats](./charts-and-stats.md) — bar, donut, stat, metric grid |
| **Headers** | [Headers](./headers.md) — page, section, entity, document, profile |
| **Status** | [Status indicators](./status-indicators.md) — badge, status, live, notification dot |
| **Media** | [Avatars and media](./avatars-and-media.md) — avatar, media object, video, carousel |
| **Social & chat** | [Social and chat](./social-and-chat.md) — messages, chat input, typing |
| **Streaming** | [Streaming](./streaming.md) — SSE / LLM blocks |
| **ASCII** | [ASCII kit](./ascii-kit.md) — retro terminal components |
| **Effects** | [Effects](./effects.md) — backgrounds, particles, ambient |
| **Typography FX** | [Typography effects](./typography-effects.md) — gradient, glitch, neon, typewriter |
| **Type-aware** | [Type-aware rendering](./type-aware-rendering.md) — `description_item`, `value_type` |

## Live examples

Run the component showcase locally (see [README](https://github.com/lbliii/chirp-ui#usage)) or browse the **[Showcase](/showcase/)** on this site after build.

## Mutation helpers

For server-driven dashboards:

- `fragment_island`, `fragment_island_with_result` — isolated targets; see [HTMX patterns](../guides/htmx-patterns.md).

```html
{% from "chirpui/fragment_island.html" import poll_trigger %}

<div id="collection-status"></div>
{{ poll_trigger("/collections/status?refresh=1", "#collection-status", delay="1s") }}
```

## Related

- [Concepts](../concepts/_index.md)
- [Guides](../guides/_index.md)
- [Reference](../reference/_index.md)
