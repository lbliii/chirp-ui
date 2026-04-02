---
title: Tables and data
description: table, description_list, params_table, tree_view, sortable_list
draft: false
weight: 19
lang: en
type: doc
keywords: [chirp-ui, table, tree]
icon: table
---

# Tables and data

Components for tabular data, key-value lists, parameter documentation, sortable drag lists, and resource browse pages.

## Quick reference

| Template | Macros | Purpose |
|----------|--------|---------|
| `table.html` | `table`, `row`, `aligned_row`, `table_empty` | Responsive table with headers, sorting, alignment |
| `params_table.html` | `params_table` | API parameter documentation table |
| `description_list.html` | `description_list`, `description_item` | Key-value pairs (stacked or horizontal) |
| `list.html` | `list_group`, `list_item` | Simple vertical list |
| `sortable_list.html` | `sortable_list`, `sortable_item` | Drag-to-reorder container (CSS only, wire Alpine yourself) |
| `resource_index.html` | `resource_index` | Search + filter + results composite for browse pages |
| `row_actions.html` | `row_actions` | Kebab dropdown menu for table rows |

## table

Responsive table with configurable headers, column alignment, widths, sorting, and striped/compact modes.

```text
{% from "chirpui/table.html" import table, row, aligned_row, table_empty %}

{% call table(headers=["Name", "Email", "Role"], striped=true) %}
  {{ row("Alice", "alice@example.com", "Admin") }}
  {{ row("Bob", "bob@example.com", "User") }}
{% end %}
```

**With column alignment and widths:**

```text
{% call table(headers=["Name", "Status", "Count"], align=["left", "center", "right"], widths=["2fr", "1fr", "1fr"]) %}
  {{ aligned_row(["Alice", "Active", "42"], ["left", "center", "right"]) }}
{% end %}
```

**Sortable headers with HTMX:**

```text
{% call table(headers=["Name", "Email"], sortable=true, sort_url="/users", hx_target="#user-table") %}
  {{ row(user.name, user.email) }}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `headers` | `list` | `none` | Column header labels |
| `sortable` | `bool` | `false` | Enable sortable header clicks |
| `sort_url` | `str` | `none` | Base URL for sort requests |
| `hx_target` | `str` | `none` | HTMX target for sort responses |
| `striped` | `bool` | `false` | Alternate row shading |
| `sticky_header` | `bool` | `false` | Sticky table header |
| `actions_header` | `bool` | `false` | Add trailing actions column |
| `align` | `list` | `none` | Per-column alignment (`"left"`, `"center"`, `"right"`) |
| `widths` | `list` | `none` | Per-column CSS widths (e.g. `"2fr"`, `"1fr"`) |
| `compact` | `bool` | `false` | Tighter row spacing |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `caption` -- table caption element.

### row

```text
{{ row("Alice", "alice@example.com", "Admin") }}
```

Accepts variadic `*cells` and wraps each in a `<td>`.

### aligned_row

```text
{{ aligned_row(["Alice", "Active", "42"], ["left", "center", "right"]) }}
```

| Param | Type | Description |
|-------|------|-------------|
| `cells` | `list` | Cell values |
| `align` | `list` | Per-cell alignment |

### table_empty

```text
{{ table_empty("No users found", icon="?") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `message` | `str` | `"No data available"` | Empty state message |
| `icon` | `str` | `"◇"` | Leading icon |

## params_table

API parameter documentation table with Name, Type, Default, and Description columns. Columns are configurable.

```text
{% from "chirpui/params_table.html" import params_table %}

{{ params_table(rows=[
    {"name": "query", "type": "str", "default": '""', "description": "Search query"},
    {"name": "limit", "type": "int", "default": "10", "description": "Max results"},
], title="Parameters") }}

{{ params_table(rows=returns, title="Returns", columns=["name", "type", "description"]) }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `rows` | `list[dict]` | required | Row data (keys: `name`, `type`, `default`, `description`) |
| `title` | `str` | `none` | Optional heading above table |
| `columns` | `list` | `none` | Column keys to show (default: all four) |
| `cls` | `str` | `""` | Extra CSS classes |

## description_list

Key-value pairs for settings, metadata, profiles. Supports stacked and horizontal variants, type-aware rendering, and modifiers for hover, dividers, and spacing.

```text
{% from "chirpui/description_list.html" import description_list, description_item %}

{{ description_list(items=[
    {"term": "Name", "detail": "Alice"},
    {"term": "Active", "detail": true},
], variant="horizontal", hoverable=true) }}
```

**Using slots:**

```text
{% call description_list(variant="stacked", divided=true) %}
  {{ description_item("Name", "Alice", icon="user") }}
  {{ description_item("Email", "alice@example.com", type="url") }}
{% end %}
```

### description_list params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `items` | `list[dict]` | `none` | Data items (`term`, `detail`, optional `type`) |
| `variant` | `str` | `"stacked"` | `"stacked"` or `"horizontal"` |
| `compact` | `bool` | `false` | Tighter spacing |
| `relaxed` | `bool` | `false` | Extra vertical spacing |
| `hoverable` | `bool` | `false` | Highlight row on hover |
| `divided` | `bool` | `false` | Border between rows |
| `term_width` | `str` | `""` | CSS custom property for term column width |
| `detail_align` | `str` | `""` | `"left"`, `"center"`, or `"right"` |
| `cls` | `str` | `""` | Extra CSS classes |

**Slots:** `header` -- content above the list. Default slot for manual `description_item` children.

### description_item params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `term` | `str` | required | Label/key |
| `detail` | `any` | required | Value |
| `type` | `str` | `none` | Override type detection (`"bool"`, `"url"`, `"path"`, `"number"`, `"unset"`) |
| `icon` | `str` | `none` | Icon before term |
| `cls` | `str` | `""` | Extra CSS classes |

Boolean values render as `badge("Yes"/"No")`. Unset values get muted styling.

## list_group / list_item

Simple vertical list for text rows or linked items.

```text
{% from "chirpui/list.html" import list_group, list_item %}

{{ list_group(["Item 1", "Item 2", "Item 3"], bordered=true) }}

{{ list_group([{"label": "Dashboard", "href": "/dash"}, {"label": "Settings", "href": "/settings"}], linked=true) }}
```

**Using slots:**

```text
{% call list_group(bordered=true) %}
  {% call list_item() %}Custom row content{% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `items` | `list` | `none` | String items or `{label, href}` dicts |
| `linked` | `bool` | `false` | Render items with `href` as links |
| `bordered` | `bool` | `false` | Add borders between items |
| `cls` | `str` | `""` | Extra CSS classes |

## sortable_list / sortable_item

CSS-styled drag-to-reorder containers. ChirpUI provides the visual structure and drag affordances; Alpine wiring (`@dragstart`, `@drop`, `x-data`) is left to the consumer.

```text
{% from "chirpui/sortable_list.html" import sortable_list, sortable_item %}

{% call sortable_list(attrs='x-data="sortable" @drop="handleDrop"') %}
  {% for step in steps %}
    {% call sortable_item(attrs='draggable="true" @dragstart="drag"') %}
      {{ step.name }}
    {% end %}
  {% end %}
{% end %}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `cls` | `str` | `""` | Extra CSS classes |
| `attrs` | `str` | `""` | Extra HTML attributes (rendered with `| safe`) |

## resource_index

Full browse page composite: search header + filter bar + selection bar + results area. Composes `search_header`, `filter_bar`, `selection_bar`, and `empty_state`.

```text
{% from "chirpui/resource_index.html" import resource_index %}

{% call resource_index("Skills", search_action="/skills", query=q,
    filter_action="/skills/filter", results_layout="grid", results_cols=3) %}
  {% slot toolbar_controls %}{{ select("sort", options=sort_opts) }}{% end %}
  {% slot filter_controls %}{{ select("category", options=cats) }}{% end %}
  {% for skill in skills %}
    {{ skill_card(skill) }}
  {% end %}
{% end %}
```

Key params (see template source for the full list):

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | `str` | required | Page title |
| `search_action` | `str` | required | Search form action URL |
| `query` | `str` | `""` | Current search value |
| `filter_action` | `str` | `none` | Filter form action (enables filter bar) |
| `results_layout` | `str` | `"stack"` | `"stack"` or `"grid"` |
| `results_cols` | `int` | `2` | Grid columns (2, 3, or 4) |
| `has_results` | `bool` | `true` | Show results or empty state |
| `empty_title` | `str` | `"No results found"` | Empty state heading |

**Slots:** `toolbar_controls`, `filter_primary`, `filter_controls`, `filter_actions`, `selection`, `filters_panel`, `empty`, default (result items).

## row_actions

Kebab dropdown menu for table rows. Wraps `dropdown_menu` with a `"⋮"` ghost button trigger.

```text
{% from "chirpui/row_actions.html" import row_actions %}

{{ row_actions(items=[
    {"label": "Edit", "href": "/items/1/edit"},
    {"label": "Duplicate", "action": "duplicate"},
    {"divider": true},
    {"label": "Delete", "href": "/items/1/delete", "variant": "danger", "icon": "x"},
], id="row-1-actions") }}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `items` | `list[dict]` | required | Menu items (`label`, `href`, `action`, `variant`, `icon`, `divider`) |
| `id` | `str` | `"chirpui-row-actions"` | Unique ID for the dropdown |

## CSS classes

| Class | Element |
|-------|---------|
| `chirpui-table-wrap` | Scrollable table wrapper |
| `chirpui-table` | Table element |
| `chirpui-table--striped` | Striped rows modifier |
| `chirpui-table--compact` | Compact spacing modifier |
| `chirpui-table__th--left/center/right` | Column alignment |
| `chirpui-params-table` | Params table wrapper |
| `chirpui-dl` | Description list |
| `chirpui-dl--horizontal` | Side-by-side variant |
| `chirpui-dl--hoverable` | Hover highlight |
| `chirpui-dl--divided` | Row borders |
| `chirpui-list` | List group |
| `chirpui-list--bordered` | Bordered list |
| `chirpui-sortable` | Sortable container |
| `chirpui-resource-index` | Resource index wrapper |

## Dense tables

Wrap wide tables in a child with `overflow-x: auto`. See [Layout overflow](../guides/layout-overflow.md).

## Related

- [Charts and stats](./charts-and-stats.md)
- [Type-aware rendering](./type-aware-rendering.md)
- [HTMX patterns](../guides/htmx-patterns.md)
