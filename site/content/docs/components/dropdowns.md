---
title: Dropdown anatomy
description: Rendered anatomy and Alpine contracts for dropdown menus, selects, and split menus
draft: false
weight: 24
lang: en
type: doc
keywords: [chirp-ui, dropdown, menu, select, alpine, anatomy]
category: components
---

# Dropdown anatomy

Chirp UI ships three dropdown macros from `chirpui/dropdown_menu.html`:

- `dropdown_menu(trigger, items, id="chirpui-dropdown")`
- `dropdown_select(trigger_label, items, selected=none, id="chirpui-dropdown-select")`
- `dropdown_split(primary_label, primary_href=none, primary_action=none, items=[], icon=none)`

`dropdown_menu` and `dropdown_split` use the `chirpuiDropdown()` Alpine
controller. Item selection is dispatched through
`chirpui:dropdown-selected`, with payloads read from escaped `data-label`,
`data-href`, and `data-action` attributes.

`dropdown_select` uses `chirpuiDropdownSelect()` and emits
`chirpui:dropdown-selected` with `{ label, value }`.

## Dropdown select vs combobox

`dropdown_select(...)` is the current Chirp UI combobox-like surface. It is
published as the `dropdown-select` registry/manifest component and renders a
`role="combobox"` trigger with a `role="listbox"` menu. Use it for command
choices, filters, density switches, and other app-state selections that should
not submit a normal HTML form.

Use `select_field(...)` from `chirpui/forms.html` when the value belongs to a
form payload or should use the platform picker on mobile.

The full rendered contract, ARIA roles, focus behavior, keyboard behavior,
HTMX link behavior, and proof locations live in the canonical source guide:
[`docs/components/dropdown-anatomy.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/components/dropdown-anatomy.md?plain=1).
