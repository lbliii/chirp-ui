---
title: Control selection
description: Choose native fields, dropdown selects, toggle groups, sliders, and table composition
draft: false
weight: 23
lang: en
type: doc
keywords: [chirp-ui, controls, forms, select, combobox, slider, table]
category: components
---

# Control selection

Chirp UI covers common control jobs with native form controls first, then adds
interactive components where the interaction is not a normal form submit.

| Need | Use |
|------|-----|
| Normal form option list | `select_field(...)` |
| App-state or filter selection menu | `dropdown_select(...)` |
| Small visible single-choice group | `toggle_group(type="single", ...)` |
| Small visible multi-choice group | `toggle_group(type="multiple", ...)` |
| Native date input | `date_field(...)` |
| Standalone range control | `slider(...)` |
| Form range control with hint/error handling | `range_field(...)` |
| Bounded overflow region | `scroll_area(...)` |
| Reusable list/menu/result row | `item(...)` |
| Record table with filters and pagination | `data_table(...)` |

## Native select or dropdown select

Use `select_field(...)` when the value belongs to a form payload. Use
`dropdown_select(...)` when selection is app state, a filter, or a command
surface choice. `dropdown_select(...)` is the current combobox-like Chirp UI
surface; it renders combobox/listbox anatomy and uses
`chirpuiDropdownSelect()` for keyboard behavior.

{{< component_specimen name="toggle_group" title="Toggle group" description="Use visible grouped options for compact single or multiple choice." >}}

## Date picker boundary

Use `date_field(...)` for stable date input. A popover calendar picker needs
browser proof for keyboard navigation, focus movement, Escape/outside
dismissal, and viewport containment before it should become a stable component.

{{< component_specimen name="slider" title="Slider" description="Use the standalone range primitive outside full form-field chrome." >}}

## Data table boundary

Compose dense record pages with `data_table(...)`:

```html
{% from "chirpui/data_table.html" import data_table %}

{% call data_table(
  title="Records",
  headers=["Name", "Status"],
  rows=records,
  filter_action="/records",
  current=page,
  total=pages,
  url_pattern="/records?page={page}",
) %}
  ...
{% end %}
```

{{< component_specimen name="data_table" title="Data table" description="A parent wrapper for filters, table rows, empty state, and pagination." >}}

## Supporting primitives

These primitives are intentionally small. They provide shared anatomy that docs,
forms, menus, and marketing/product pages can reuse.

{{< component_specimen name="item" title="Item" description="Reusable row anatomy for result lists, menu rows, and command surfaces." >}}

{{< component_specimen name="scroll_area" title="Scroll area" description="A bounded overflow region with optional edge affordance." >}}

{{< component_specimen name="kbd" title="Keyboard key" description="Inline key and chord rendering." >}}

{{< component_specimen name="separator" title="Separator" description="Semantic or decorative separation with optional label." >}}

{{< component_specimen name="aspect_ratio" title="Aspect ratio" description="Stable media and preview framing." >}}

{{< component_specimen name="label" title="Label" description="Standalone form-label anatomy for custom controls." >}}

The full source guide is
[`docs/components/control-selection.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/components/control-selection.md?plain=1).
