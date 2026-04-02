---
title: Layout
description: container, grid, frame, stack, cluster, block, section headers
draft: false
weight: 11
lang: en
type: doc
keywords: [chirp-ui, layout, grid, frame, stack]
icon: grid-four
---

# Layout

Layout primitives handle page structure, content flow, and sectioning. Core primitives live in `chirpui/layout.html`. Specialized layouts -- split panes, bento grids, panels, heroes, dividers, and collapsibles -- each have their own template.

## Quick reference

| Template | Macro | Description |
|----------|-------|-------------|
| `layout.html` | `container` | Max-width wrapper with horizontal padding |
| `layout.html` | `grid` | Responsive flow grid with optional presets |
| `layout.html` | `frame` | Fixed column structures (hero, sidebar, balanced) |
| `layout.html` | `stack` | Vertical flex column |
| `layout.html` | `cluster` | Horizontal flex row that wraps |
| `layout.html` | `block` | Grid cell with `min-width: 0`; supports `span` |
| `layout.html` | `page_header` | Full-width page title with breadcrumbs and actions |
| `layout.html` | `section_header` | Section title with optional icon and actions |
| `layout.html` | `section` | Composite surface + section header |
| `layout.html` | `section_collapsible` | Collapsible section with details/summary |
| `split_layout.html` | `split_layout` | Two-pane layout with ratio presets |
| `split_panel.html` | `split_panel` | Resizable split panel (Alpine.js) |
| `bento_grid.html` | `bento_grid` | Asymmetric showcase grid |
| `bento_grid.html` | `bento_item` | Grid item with span control |
| `panel.html` | `panel` | Titled pane with header, body, footer |
| `hero.html` | `hero` | Full-width hero section |
| `hero.html` | `page_hero` | Enhanced hero with eyebrow, actions, metadata |
| `divider.html` | `divider` | Visual separator with optional text |
| `collapse.html` | `collapse` | Expand/collapse via details/summary |
| `app_layout.html` | _(extends)_ | Base layout extending Chirp boost |

---

## Core primitives

These macros compose together to build any page structure. Import them from a single template:

```text
{% from "chirpui/layout.html" import container, grid, frame, stack, cluster, block %}
```

### container

Responsive max-width wrapper with horizontal padding.

**Signature:**

```text
container(max_width="72rem", padding=true, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_width` | string | `"72rem"` | CSS max-width value |
| `padding` | bool | `true` | Apply horizontal padding |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% call container(max_width="60rem") %}
  <p>Narrower content area.</p>
{% end %}
```

### grid

Flow grid using `repeat(auto-fit, minmax(...))` by default. Pass `cols` for a simple column count, or `preset` for fixed dashboard tracks.

**Signature:**

```text
grid(cols=none, gap=none, preset=none, items=none, detail_single=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cols` | int | `none` | Column count (2, 3, or 4) for auto-fit sizing |
| `gap` | string | `none` | Gap size: `"sm"`, `"md"`, or `"lg"` |
| `preset` | string | `none` | Fixed-track preset (see table below) |
| `items` | string | `none` | Align items: `"start"`, `"end"`, `"center"` |
| `detail_single` | bool | `false` | Force single column (only for `detail-two` / `split-1-1.35`) |
| `cls` | string | `""` | Extra CSS classes |

**Grid presets:**

| Canonical | Aliases | Tracks (wide) | Collapse |
|-----------|---------|---------------|----------|
| `bento-211` | `split-2-1-1` | `2fr 1fr 1fr` | 2 cols at lg, 1 at sm |
| `thirds` | `split-thirds`, `three-equal` | `1fr 1fr 1fr` | 1 col at sm |
| `detail-two` | `split-1-1.35` | `1fr 1.35fr` | 1 col at md |
| `detail-two-single` | `split-1-1.35-single` | `1fr` | Already single |

**Examples:**

```text
{# Simple two-column grid #}
{% call grid(cols=2, gap="md") %}
  {% call block() %}Left{% end %}
  {% call block() %}Right{% end %}
{% end %}

{# Dashboard preset with spanning block #}
{% call grid(preset="bento-211") %}
  {% call block(span=2) %}Wide card{% end %}
  {% call block() %}Stat{% end %}
  {% call block() %}Stat{% end %}
{% end %}

{# Detail layout with unequal cell heights #}
{% call grid(preset="detail-two", items="start") %}
  {% call block() %}Sidebar{% end %}
  {% call block() %}Main content{% end %}
{% end %}
```

### frame

Explicit two-column structure for hero layouts, sidebars, or balanced splits. Unlike `grid()`, `frame()` uses fixed `grid-template-columns` and expects exactly two direct children.

**Signature:**

```text
frame(variant="balanced", gap=none, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `variant` | string | `"balanced"` | Column structure: `"balanced"`, `"hero"`, `"sidebar-end"` |
| `gap` | string | `none` | Gap size: `"sm"`, `"md"`, or `"lg"` |
| `cls` | string | `""` | Extra CSS classes |

**Examples:**

```text
{# Balanced two-column #}
{% call frame() %}
  <div>Left column</div>
  <div>Right column</div>
{% end %}

{# Hero with wide primary #}
{% call frame(variant="hero", gap="lg") %}
  <div>Hero content (wider)</div>
  <aside>Supporting info</aside>
{% end %}

{# Sidebar on the right #}
{% call frame(variant="sidebar-end") %}
  <main>Main content</main>
  <aside>Sidebar</aside>
{% end %}
```

Override column ratios with a CSS custom property:

```text
{% call frame(variant="hero", cls="my-custom") %}...{% end %}
```

```css
.my-custom { --chirpui-frame-hero-columns: 3fr 1fr; }
```

### stack

Vertical flex column with configurable gap.

**Signature:**

```text
stack(gap=none, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `gap` | string | `none` | Gap size: `"xs"`, `"sm"`, `"md"`, `"lg"`, `"xl"` |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% call stack(gap="md") %}
  <h2>Title</h2>
  <p>Description</p>
  <div>Content</div>
{% end %}
```

### cluster

Horizontal flex row that wraps. Useful for tags, badges, or inline actions.

**Signature:**

```text
cluster(gap=none, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `gap` | string | `none` | Gap size: `"xs"`, `"sm"`, `"md"`, `"lg"` |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% call cluster(gap="sm") %}
  <span class="chirpui-badge">Python</span>
  <span class="chirpui-badge">Alpine.js</span>
  <span class="chirpui-badge">htmx</span>
{% end %}
```

### block

Grid cell with `min-width: 0` to prevent overflow. Use inside `grid()` for spanning.

**Signature:**

```text
block(span=1, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `span` | int/string | `1` | Column span: `1`, `2`, `3`, or `"full"` |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% call grid(cols=3) %}
  {% call block(span=2) %}Spans two columns{% end %}
  {% call block() %}Single column{% end %}
  {% call block(span="full") %}Full-width row{% end %}
{% end %}
```

---

## Page structure

### page_header

Full-width page title row with optional breadcrumbs, subtitle, meta, and an `actions` slot.

**Signature:**

```text
page_header(title, subtitle=none, meta=none, breadcrumb_items=none, variant="default", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | required | Page heading (renders as `<h1>`) |
| `subtitle` | string | `none` | Subheading text |
| `meta` | string | `none` | Additional meta line (rendered with `safe`) |
| `breadcrumb_items` | list | `none` | Breadcrumb path items |
| `variant` | string | `"default"` | Validated against `VARIANT_REGISTRY["page_header"]` |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `actions` -- buttons or controls aligned to the right.

**Example:**

```text
{% call page_header("Dashboard", subtitle="Overview of key metrics",
                    breadcrumb_items=[{"label": "Home", "href": "/"}]) %}
  {% slot actions %}
    {{ btn("Export", variant="ghost", icon="download") }}
  {% end %}
{% end %}
```

### section_header

Section title row with optional icon and actions slot.

**Signature:**

```text
section_header(title, subtitle=none, icon=none, variant="default", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | required | Section heading (renders as `<h2>`) |
| `subtitle` | string | `none` | Subheading text |
| `icon` | string | `none` | Icon name (rendered via `icon` filter) |
| `variant` | string | `"default"` | Use `"inline"` for compact inline headers |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `actions` -- section-level controls.

**Example:**

```text
{% call section_header("Recent Activity", icon="clock", variant="inline") %}
  {% slot actions %}
    {{ btn("Refresh", variant="ghost", size="sm") }}
  {% end %}
{% end %}
```

`section_header_inline(title, icon, cls)` is a deprecated alias for `section_header(..., variant="inline")`.

### section

Composite macro that combines a `surface` with a `section_header` and content area. Reduces boilerplate for grouped content regions.

**Signature:**

```text
section(title, subtitle=none, icon=none, surface_variant="muted",
        full_width=false, parallax=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | required | Section heading |
| `subtitle` | string | `none` | Subheading text |
| `icon` | string | `none` | Icon name |
| `surface_variant` | string | `"muted"` | Surface variant (validated) |
| `full_width` | bool | `false` | Wrap in `chirpui-blade` for edge-to-edge layout |
| `parallax` | bool | `false` | Scroll-driven background motion (Chrome 115+) |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `actions` -- section header actions.

**Example:**

```text
{% call section("Configuration", subtitle="App settings", surface_variant="muted") %}
  {% slot actions %}
    {{ btn("Auto-detect", variant="ghost", size="sm") }}
  {% end %}
  <form>...</form>
{% end %}
```

### section_collapsible

Details/summary section with a section header as the summary trigger.

**Signature:**

```text
section_collapsible(title, open=false, surface_variant="muted", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | required | Collapsible section heading |
| `open` | bool | `false` | Start expanded |
| `surface_variant` | string | `"muted"` | Surface variant for body |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% call section_collapsible("Advanced Settings", open=false) %}
  <p>Hidden by default. Click the header to expand.</p>
{% end %}
```

---

## Specialized layouts

### split_layout.html

Two-pane layout for tree/content, editor/preview, or content/inspector patterns.

**Signature:**

```text
split_layout(direction="horizontal", ratio="sidebar", gap="md", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `direction` | string | `"horizontal"` | `"horizontal"` or `"vertical"` |
| `ratio` | string | `"sidebar"` | `"sidebar"`, `"balanced"`, `"wide-primary"`, `"wide-secondary"` |
| `gap` | string | `"md"` | `"sm"`, `"md"`, or `"lg"` |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `primary`, `secondary`.

**Example:**

```text
{% from "chirpui/split_layout.html" import split_layout %}

{% call split_layout(ratio="sidebar") %}
  {% slot primary %}<nav>File tree</nav>{% end %}
  {% slot secondary %}<main>Editor</main>{% end %}
{% end %}
```

### split_panel.html

Resizable split panel with a draggable handle. Requires Alpine.js.

**Signature:**

```text
split_panel(direction="horizontal", default_split=50, min_split=10, max_split=90, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `direction` | string | `"horizontal"` | `"horizontal"` or `"vertical"` |
| `default_split` | int | `50` | Initial split percentage (first pane) |
| `min_split` | int | `10` | Minimum split percentage |
| `max_split` | int | `90` | Maximum split percentage |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `left` (first pane), `right` (second pane).

**Example:**

```text
{% from "chirpui/split_panel.html" import split_panel %}

{% call split_panel(default_split=30, min_split=20, max_split=80) %}
  {% slot left %}<nav>Sidebar</nav>{% end %}
  {% slot right %}<main>Content</main>{% end %}
{% end %}

{# Vertical split #}
{% call split_panel(direction="vertical", default_split=70) %}
  {% slot left %}Top pane{% end %}
  {% slot right %}Bottom pane{% end %}
{% end %}
```

### bento_grid.html

Asymmetric grid for feature showcases and dashboards. Items get card chrome by default. For raw asymmetric tracks without card styling, use `grid(preset="bento-211")` instead.

#### bento_grid

**Signature:**

```text
bento_grid(cols=3, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cols` | int | `3` | Number of columns |
| `cls` | string | `""` | Extra CSS classes |

#### bento_item

**Signature:**

```text
bento_item(span=none, span_row=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `span` | int/string | `none` | Column span: `2` or `"full"` |
| `span_row` | bool | `false` | Span two rows |
| `cls` | string | `""` | Extra CSS classes |

**Example:**

```text
{% from "chirpui/bento_grid.html" import bento_grid, bento_item %}

{% call bento_grid() %}
  {% call bento_item(span=2) %}
    <h3>Featured</h3>
    <p>Wide card spanning two columns.</p>
  {% end %}
  {% call bento_item() %}
    <h3>Stat</h3>
  {% end %}
  {% call bento_item(span_row=true) %}
    <h3>Tall card</h3>
  {% end %}
{% end %}
```

### panel.html

Titled pane for inspectors, activity feeds, file trees, and embedded work surfaces.

**Signature:**

```text
panel(title=none, subtitle=none, surface_variant="muted", scroll_body=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `none` | Panel heading |
| `subtitle` | string | `none` | Subheading text |
| `surface_variant` | string | `"muted"` | Surface variant (validated) |
| `scroll_body` | bool | `false` | Make body region scrollable |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `actions` (header controls), default slot (body content), `footer`.

**Example:**

```text
{% from "chirpui/panel.html" import panel %}

{% call panel(title="Activity", scroll_body=true) %}
  {% slot actions %}{{ btn("Clear", variant="ghost", size="sm") }}{% end %}
  <div>Activity rows...</div>
  {% slot footer %}<span class="chirpui-text-muted chirpui-ui-sm">Connected</span>{% end %}
{% end %}
```

### hero.html

#### hero

Full-width section with background for landing pages.

**Signature:**

```text
hero(title=none, subtitle=none, background="solid", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `none` | Heading text |
| `subtitle` | string | `none` | Subheading text |
| `background` | string | `"solid"` | `"solid"`, `"muted"`, `"gradient"`, `"mesh"`, `"animated-gradient"` |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** default (content), `action` (primary CTA).

**Example:**

```text
{% from "chirpui/hero.html" import hero %}

{% call hero(title="Welcome", subtitle="Build something great.", background="gradient") %}
  <p>Intro text goes here.</p>
  {% slot action %}
    <a href="/start" class="chirpui-btn chirpui-btn--primary">Get started</a>
  {% end %}
{% end %}
```

#### page_hero

Enhanced hero for docs, marketing, and app page headers with additional slots.

**Signature:**

```text
page_hero(title=none, subtitle=none, variant="editorial", background="solid", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `none` | Heading text |
| `subtitle` | string | `none` | Subheading text |
| `variant` | string | `"editorial"` | `"editorial"` or `"minimal"` |
| `background` | string | `"solid"` | Same options as `hero` |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `eyebrow`, `actions`, `metadata`, default (content), `footer`.

**Example:**

```text
{% from "chirpui/hero.html" import page_hero %}

{% call page_hero(title="API Reference", subtitle="Explore endpoints.",
                  variant="editorial", background="muted") %}
  {% slot eyebrow %}{{ breadcrumbs(items) }}{% end %}
  {% slot actions %}{{ btn("Share", variant="ghost") }}{% end %}
  {% slot metadata %}<time>Updated Jan 2026</time>{% end %}
  {% slot footer %}<span class="chirpui-badge">v2.0</span>{% end %}
{% end %}
```

### divider.html

Visual separator between content blocks.

**Signature:**

```text
divider(text=none, horizontal=false, variant="", cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | `none` | Optional text displayed in the divider |
| `horizontal` | bool | `false` | Horizontal orientation (default is vertical) |
| `variant` | string | `""` | Variant modifier (e.g. `"primary"`) |
| `cls` | string | `""` | Extra CSS classes |

**Examples:**

```text
{% from "chirpui/divider.html" import divider %}

{{ divider() }}
{{ divider("OR") }}
{{ divider("OR", horizontal=true, variant="primary") }}
```

### collapse.html

Single expand/collapse section using native `<details>` / `<summary>`.

**Signature:**

```text
collapse(trigger, open=false, cls="")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger` | string | required | Summary text |
| `open` | bool | `false` | Start expanded |
| `cls` | string | `""` | Extra CSS classes |

**Slots:** `header_actions` (controls in the summary row), default (hidden content).

**Example:**

```text
{% from "chirpui/collapse.html" import collapse %}

{% call collapse(trigger="Show details") %}
  <p>This content is hidden until the summary is clicked.</p>
{% end %}
```

### app_layout.html

Base layout template that extends Chirp's `chirp/layouts/boost.html`. Injects `chirpui.css`, the default theme, transition styles, and Alpine.js plugins. No macros -- extend it:

```text
{% extends "chirpui/app_layout.html" %}
{% block title %}My App{% end %}
{% block content %}
  {% from "chirpui/layout.html" import container, stack %}
  {% call container() %}
    {% call stack(gap="md") %}
      <h1>Hello</h1>
    {% end %}
  {% end %}
{% end %}
```

---

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-container` | Container wrapper |
| `chirpui-grid` | Grid container |
| `chirpui-grid--cols-{2,3,4}` | Column count modifier |
| `chirpui-grid--gap-{sm,md,lg}` | Gap modifier |
| `chirpui-grid--preset-bento-211` | Bento 2-1-1 preset |
| `chirpui-grid--preset-thirds` | Equal thirds preset |
| `chirpui-grid--preset-detail-two` | Detail two-column preset |
| `chirpui-grid--detail-two-single` | Single-column detail variant |
| `chirpui-grid--items-{start,end,center}` | Align items modifier |
| `chirpui-frame` | Frame container |
| `chirpui-frame--{balanced,hero,sidebar-end}` | Frame variant |
| `chirpui-stack` | Vertical stack |
| `chirpui-stack--{xs,sm,md,lg,xl}` | Stack gap modifier |
| `chirpui-cluster` | Horizontal cluster |
| `chirpui-cluster--{xs,sm,md,lg}` | Cluster gap modifier |
| `chirpui-block` | Grid block cell |
| `chirpui-block--span-{2,3,full}` | Block span modifier |
| `chirpui-page-header` | Page header |
| `chirpui-section-header` | Section header |
| `chirpui-section-header--inline` | Inline section header variant |
| `chirpui-section-collapsible` | Collapsible section |
| `chirpui-split-layout` | Split layout |
| `chirpui-split-panel` | Resizable split panel |
| `chirpui-bento` | Bento grid |
| `chirpui-bento__item` | Bento grid item |
| `chirpui-panel` | Panel |
| `chirpui-hero` | Hero section |
| `chirpui-divider` | Divider |
| `chirpui-collapse` | Collapse |
| `chirpui-blade` | Full-width blade wrapper |

All classes follow the BEM convention `chirpui-<block>--<modifier>`.

## Related

- [Layout presets](../guides/layout-presets.md)
- [Layout overflow](../guides/layout-overflow.md)
- [Grids and frames](../guides/grids-and-frames.md)
- [Vertical layout](../guides/vertical-layout.md)
- [Charts and stats](./charts-and-stats.md) -- `bento_grid()` vs `grid()` presets
