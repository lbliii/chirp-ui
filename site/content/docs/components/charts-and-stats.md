---
title: Charts and stats
description: bar_chart, donut, stat, metric_grid, animated cards
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, charts, stats]
icon: chart-bar
---

# Charts and stats

CSS-only charts, stat blocks, animated counters, and metric card grids for dashboards and KPI displays. No JavaScript required for bar charts and donuts.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `stat.html` | `stat` | Simple value + label pair |
| `animated_stat_card.html` | `animated_stat_card` | Stat card with animated counter and trend |
| `bar_chart.html` | `bar_chart` | CSS-only horizontal bar chart |
| `donut.html` | `donut` | CSS-only donut chart (conic-gradient) |
| `metric_grid.html` | `metric_grid`, `metric_card` | Dashboard KPI grid with trend indicators |
| `animated_counter.html` | `animated_counter` | Counter that animates from 0 to target |
| `number_ticker.html` | `number_ticker` | CSS-animated number using `@property` and `counter()` |

## stat

Simple label + value pair for followers, views, KPIs.

```text
{% from "chirpui/stat.html" import stat %}

{{ stat(value="1.2K", label="Followers") }}
{{ stat(value="42", label="Videos", icon="play") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `str` | required | Display value |
| `label` | `str` | required | Description label |
| `icon` | `str` | `none` | Optional icon (passed through `| icon`) |
| `cls` | `str` | `""` | Extra CSS classes |

## animated_stat_card

Composite card combining `animated_counter` with an optional trend indicator.

```text
{% from "chirpui/animated_stat_card.html" import animated_stat_card %}

{{ animated_stat_card(1250, label="Active Users", trend="+12%", trend_direction="up") }}
{{ animated_stat_card(48, label="Revenue", prefix="$", suffix="M", effect="beam") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `int/str` | required | Target number |
| `label` | `str` | `""` | Description label |
| `prefix` | `str` | `""` | Text before value (e.g. `"$"`) |
| `suffix` | `str` | `""` | Text after value (e.g. `"M"`) |
| `trend` | `str` | `""` | Trend text (e.g. `"+12%"`) |
| `trend_direction` | `str` | `""` | `"up"`, `"down"`, or empty for neutral |
| `effect` | `str` | `""` | Visual effect name |
| `cls` | `str` | `""` | Extra CSS classes |

## bar_chart

CSS-only horizontal bar chart. Items are `{label, value}` dicts with optional `href`.

```text
{% from "chirpui/bar_chart.html" import bar_chart %}

{{ bar_chart(items=[
    {"label": "create-rule", "value": 42},
    {"label": "debug-agent", "value": 18},
    {"label": "review-pr", "value": 7},
], max=50) }}

{{ bar_chart(items=tag_counts, variant="success", size="sm", show_value=false) }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `items` | `list[dict]` | required | `{label, value}` or `{label, value, href}` |
| `max` | `int` | `none` | Scale maximum (auto-detected from values if omitted) |
| `show_value` | `bool` | `true` | Show numeric value after each bar |
| `variant` | `str` | `"gold"` | `"gold"`, `"radiant"`, `"success"`, `"muted"` |
| `size` | `str` | `"md"` | `"sm"`, `"md"`, `"lg"` |
| `cls` | `str` | `""` | Extra CSS classes |

## donut

CSS-only donut chart using `conic-gradient`. Shows a percentage or fraction.

```text
{% from "chirpui/donut.html" import donut %}

{{ donut(value=75, max=100, label="75%") }}
{{ donut(value=3, max=5, label="3/5", variant="success") }}
{{ donut(value=42, max=100, size="lg") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `int/float` | required | Current value |
| `max` | `int/float` | `100` | Maximum value |
| `label` | `str` | `none` | Center label (defaults to percentage) |
| `variant` | `str` | `"gold"` | `"gold"`, `"success"`, `"muted"` |
| `size` | `str` | `"md"` | `"sm"`, `"md"`, `"lg"` |
| `cls` | `str` | `""` | Extra CSS classes |

## metric_grid / metric_card

Dashboard KPI grid. `metric_grid` is a wrapper around `grid()`, and `metric_card` renders a stat card with optional trend, hint, icon badge, and link.

```text
{% from "chirpui/metric_grid.html" import metric_grid, metric_card %}

{% call metric_grid(cols=3, gap="md") %}
  {{ metric_card(value="1,234", label="Users", trend="+12%", trend_direction="up", icon="users") }}
  {{ metric_card(value="$48K", label="Revenue", hint="MRR", href="/revenue") }}
  {{ metric_card(value="99.9%", label="Uptime", icon="check", icon_bg="success") }}
{% end %}
```

### metric_grid params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cols` | `int` | `3` | Grid columns |
| `gap` | `str` | `"md"` | Grid gap size |
| `cls` | `str` | `""` | Extra CSS classes |

### metric_card params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `str` | required | Display value |
| `label` | `str` | required | Description label |
| `icon` | `str` | `none` | Icon (inline or badge) |
| `trend` | `str` | `none` | Trend text |
| `trend_direction` | `str` | `""` | `"up"`, `"down"`, or neutral |
| `hint` | `str` | `none` | Explanatory hint text |
| `href` | `str` | `none` | Makes the card a link |
| `icon_bg` | `str` | `""` | Background variant for icon badge |
| `footer_label` | `str` | `none` | Footer link text |
| `footer_href` | `str` | `none` | Footer link URL |
| `cls` | `str` | `""` | Extra CSS classes |
| `attrs` | `str` | `""` | Extra HTML attributes |
| `attrs_map` | `dict` | `none` | Extra HTML attributes map |

## animated_counter

Counter that animates from 0 to the target value on page load using CSS `@property`.

```text
{% from "chirpui/animated_counter.html" import animated_counter %}

{{ animated_counter(1250, label="Active Users") }}
{{ animated_counter(99, prefix="$", suffix="M", label="Revenue", variant="mono") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `int` | required | Target number |
| `label` | `str` | `""` | Description label |
| `prefix` | `str` | `""` | Text before value |
| `suffix` | `str` | `""` | Text after value |
| `variant` | `str` | `""` | `""`, `"default"`, or `"mono"` |
| `cls` | `str` | `""` | Extra CSS classes |

## number_ticker

Inline CSS-animated number using `@property` and `counter()`. Similar to `animated_counter` but renders as a `<span>` for inline use.

```text
{% from "chirpui/number_ticker.html" import number_ticker %}

{{ number_ticker(1250) }}
{{ number_ticker(99, prefix="$", suffix="+", variant="mono", size="xl") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `value` | `int` | required | Target number |
| `variant` | `str` | `""` | `""`, `"default"`, or `"mono"` |
| `size` | `str` | `""` | `"sm"`, `"md"`, `"lg"`, `"xl"` |
| `prefix` | `str` | `""` | Text before value |
| `suffix` | `str` | `""` | Text after value |
| `cls` | `str` | `""` | Extra CSS classes |

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-stat` | Stat wrapper |
| `chirpui-stat__value` | Value display |
| `chirpui-stat__label` | Label text |
| `chirpui-animated-stat-card` | Animated stat card |
| `chirpui-animated-stat-card__trend--up/down` | Trend direction |
| `chirpui-bar-chart` | Bar chart wrapper |
| `chirpui-bar-chart--gold/radiant/success/muted` | Color variant |
| `chirpui-bar-chart--sm/md/lg` | Size variant |
| `chirpui-donut` | Donut chart wrapper |
| `chirpui-donut--gold/success/muted` | Color variant |
| `chirpui-metric-grid` | Metric grid layout |
| `chirpui-metric-card` | Metric card |
| `chirpui-metric-card__trend--up/down/neutral` | Trend arrow direction |
| `chirpui-animated-counter` | Animated counter |
| `chirpui-number-ticker` | Number ticker |

## Tokens

Charts respect `--chirpui-*` color custom properties. Use [Color system](../theming/color-system.md) for semantic colors.

## Related

- [Dashboard patterns](../guides/dashboard-patterns.md)
- [Tables and data](./tables-and-data.md)
