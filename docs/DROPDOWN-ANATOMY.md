# Dropdown Anatomy

**Status:** shipped contract
**Scope:** `dropdown_menu`, `dropdown_select`, `dropdown_split`
**Runtime:** Alpine.js through `chirpui-alpine.js`

Dropdowns are interactive command and selection surfaces. They are not general
navigation containers; use navigation components for primary section movement.

## Macros

Import the family from `chirpui/dropdown_menu.html`:

```kida
{% from "chirpui/dropdown_menu.html" import dropdown_menu, dropdown_select, dropdown_split %}

{{ dropdown_menu("Actions", items=[
  {"label": "Edit", "action": "edit"},
  {"label": "Docs", "href": "/docs"},
]) }}

{{ dropdown_select("View", items=[
  {"label": "Open", "value": "open"},
  {"label": "Closed", "value": "closed"},
]) }}

{{ dropdown_split("Export", primary_href="/export", items=[
  {"label": "CSV", "href": "/export.csv"},
]) }}
```

## Shared Floating Menu Contract

`dropdown_menu` and `dropdown_split` use:

- root class: `chirpui-dropdown`
- menu class: `chirpui-dropdown__menu`
- item class: `chirpui-dropdown__item`
- Alpine controller: `x-data="chirpuiDropdown()"`
- generated ids: `x-id="['dropdown-menu']"` or `x-id="['dropdown-split']"`
- alignment state: `:data-align-x="alignX"` and `:data-align-y="alignY"`
- trigger ref: `x-ref="trigger"`
- panel ref: `x-ref="panel"`

The trigger renders as a focusable element with `role="button"`,
`tabindex="0"`, `aria-haspopup="menu"`, bound `aria-expanded`, and bound
`aria-controls`.

The menu renders with `role="menu"`, `x-show="open"`, `x-cloak`, and
`x-transition`. Plain dropdown menus also render `aria-orientation="vertical"`.

Menu items render as:

- `<a role="menuitem">` when `href` is present
- `<button type="button" role="menuitem">` when `action` is present
- `<span role="menuitem">` for non-action display items
- `<div role="separator">` for divider items

## Selection Events

`dropdown_menu` and `dropdown_split` dispatch `chirpui:dropdown-selected` from
`chirpuiDropdown().selectItem()`.

Payloads are read from escaped DOM attributes:

- `data-label`
- `data-href`
- `data-action`

Templates must not interpolate server-provided labels, URLs, or actions into
Alpine JavaScript object literals. This keeps HTML escaping separate from
JavaScript string escaping.

Event details are one of:

```javascript
{ label: "Edit", action: "edit" }
{ label: "Docs", href: "/docs" }
{ label: "Plain item" }
```

## Dropdown Select Contract

`dropdown_select` uses:

- root classes: `chirpui-dropdown chirpui-dropdown--select`
- Alpine controller: `x-data="chirpuiDropdownSelect()"`
- initialization: `x-init="init()"`
- generated ids: `x-id="['dropdown-select', 'listbox-option']"`
- root attributes: `data-item-count` and `data-selected`

The trigger renders with `role="combobox"`, `tabindex="0"`,
`aria-haspopup="listbox"`, bound `aria-expanded`, bound `aria-controls`, and
bound `aria-activedescendant`.

The menu renders with `role="listbox"`, `x-show="open"`, `x-cloak`, and
`x-transition`. Options render with `role="option"`, `tabindex="-1"`,
`data-label`, and `data-value`.

`dropdown_select` dispatches `chirpui:dropdown-selected` with:

```javascript
{ label: "Open", value: "open" }
```

## Focus And Keyboard Behavior

All dropdowns close on Escape, outside click, focus leaving the panel, and
window resize realignment. Selection returns focus to the trigger when the item
handler receives the trigger ref.

`dropdown_select` additionally focuses the first option on open and supports
ArrowDown, ArrowUp, and Enter through the named Alpine controller.

`dropdown_menu` and `dropdown_split` currently expose click, Escape, outside
click, and focus-return behavior. They do not publish roving-arrow menu
navigation yet.

## HTMX Link Behavior

When a dropdown item has `href`, the template passes the URL through
`route_link_attrs(href) | html_attrs`. In a Chirp app shell this can add
route-aware HTMX attributes such as `hx-target` and `hx-boost`.

Macro-authored `href`, `data-href`, and route attrs are HTML-escaped by the
template layer. App code should pass plain string values, not pre-rendered HTML.

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy, escaping, route attrs, and
  pre-hydration `x-cloak` contracts.
- `tests/browser/test_dropdowns.py` for open/close, Escape, outside click,
  event payload round trips, viewport alignment, select keyboard behavior, and
  selected-text updates.
