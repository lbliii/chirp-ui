---
title: Build a dashboard
description: Grid, cards, stats, charts, and filters
draft: false
weight: 56
lang: en
type: doc
keywords: [chirp-ui, tutorial, dashboard]
icon: presentation-chart
---

# Build a dashboard

This walkthrough ties together layout, data display, and toolbar patterns. Adapt routes and handlers to your Chirp app.

## 1. Page shell

Use **`app_shell_layout`** (or your app’s base layout) with **`page_header`** for title + primary action.

## 2. Layout grid

Use **`grid(..., preset="bento-211")`** or **`thirds`** with **`block(span=...)`** for metric rows. See [Layout presets](../guides/layout-presets.md).

## 3. Metric tiles

Compose **`metric_grid`** / **`stat`** / **`animated_stat_card`** for KPIs. See [Charts and stats](../components/charts-and-stats.md).

## 4. Charts

Add **`bar_chart`** or **`donut`** for summaries; ensure chart wrappers use **`overflow-x: auto`** on small screens — [Layout overflow](../guides/layout-overflow.md).

## 5. Filters

Use **`filter_bar`** for toolbars with forms; use **`filter_chips`** for faceted rows — see project docs for **filter_bar vs filter_chips**.

## 6. Polish

Apply [Dashboard patterns](../guides/dashboard-patterns.md) for action hierarchy and confirmations.

## Related

- [Components: Layout](../components/layout.md)
- [Pitfalls](../guides/pitfalls.md)
