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

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md). It is a
docs/tests contract for the rendered dropdown family, not descriptor or
manifest metadata.

| Field | Dropdown menu | Dropdown select | Dropdown split |
| --- | --- | --- | --- |
| Surface | `dropdown_menu` command menu. | `dropdown_select` combobox/listbox selection surface. | `dropdown_split` primary action plus command menu. |
| Label | `stable` rendered macro contract under the stable `dropdown` component family. | `stable` rendered macro contract under the stable `dropdown` component family. | `stable` rendered macro contract under the stable `dropdown` component family. |
| Anatomy | `.chirpui-dropdown`, trigger ref, panel ref, `.chirpui-dropdown__menu`, `.chirpui-dropdown__item`, generated `dropdown-menu` id, alignment state attributes. | `.chirpui-dropdown.chirpui-dropdown--select`, trigger, listbox menu, option rows, selected text, `data-item-count`, `data-selected`, generated `dropdown-select` and `listbox-option` ids. | `.chirpui-dropdown.chirpui-dropdown--split`, primary link/button, split trigger, menu, menu items, generated `dropdown-split` id, alignment state attributes. |
| Native semantics | Focusable trigger with `role="button"`, `tabindex="0"`, `aria-haspopup="menu"`, bound `aria-expanded`, and bound `aria-controls`; menu uses `role="menu"`; items use `menuitem` or `separator`. | Trigger uses `role="combobox"`, `tabindex="0"`, `aria-haspopup="listbox"`, bound `aria-expanded`, bound `aria-controls`, and bound `aria-activedescendant`; menu uses `role="listbox"`; options use `role="option"`. | Primary action keeps native link/button semantics; secondary trigger uses menu-button semantics; menu uses `role="menu"` and menuitem/separator rows. |
| Keyboard | Opens from the trigger and closes on Escape; action items are activated as native anchors or buttons; roving-arrow menu navigation is not yet published. | Opens from the trigger, closes on Escape, focuses the first option on open, and supports ArrowDown, ArrowUp, and Enter in `chirpuiDropdownSelect()`. | Primary action follows native link/button behavior; secondary menu opens from the trigger and closes on Escape; roving-arrow menu navigation is not yet published. |
| Focus | Selection returns focus to the trigger when the item handler receives the trigger ref; outside click, focus leaving the panel, and resize realignment close the menu. | Initial open moves focus to the first option; selected text and active descendant update through Alpine state; selection returns focus through the controller. | Menu selection returns focus to the split trigger when the handler receives the trigger ref; primary action is independent of menu focus state. |
| Runtime | Requires `chirpuiDropdown()` in `chirpui-alpine.js`, Alpine refs, `x-id`, `x-show`, `x-cloak`, `x-transition`, outside/focusout handlers, and viewport alignment state. | Requires `chirpuiDropdownSelect()` in `chirpui-alpine.js`, `x-init="init()"`, `x-id`, `x-show`, `x-cloak`, `x-transition`, keyboard handlers, and selected-option state. | Requires `chirpuiDropdown()` plus split-specific trigger and primary action wiring; href items may receive route-aware HTMX attributes through `route_link_attrs()`. |
| Motion | Menus use `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. | Listbox uses `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. | Menus use `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Controller aligns menus with `data-align-x` and `data-align-y`; browser tests cover viewport edge alignment and long-menu containment. | Controller updates selection without shifting dense toolbar layout; browser tests cover select interactions in cramped toolbar contexts. | Controller aligns the menu near split actions; browser and gauntlet tests cover viewport containment near edges. |
| Security and escaping | Selection payloads are read from escaped `data-label`, `data-href`, and `data-action` attributes by `selectItem()`; templates must not interpolate server values into Alpine JavaScript object literals. | Selection payloads are read from escaped `data-label` and `data-value` attributes; tabular option state stays in DOM attributes, not JS string literals. | Menu item payloads follow the same escaped `data-*` attribute contract as `dropdown_menu`; primary href and route attrs are emitted through template attribute helpers. |
| Performance | Alignment work happens on open/resize paths through local trigger/panel refs; no per-frame work or page-global observers are part of the contract. | Selection state is local to the dropdown root; no page-global observers are part of the contract. | Alignment work is local to the split dropdown root; no per-frame work or page-global observers are part of the contract. |
| Proof | `tests/test_components.py` checks rendered anatomy, escaping, route attrs, and `x-cloak`; `tests/browser/test_dropdowns.py` checks open/close, Escape, outside click, events, and alignment. | `tests/test_components.py` checks combobox/listbox anatomy and escaped data attributes; `tests/browser/test_dropdowns.py` checks select keyboard behavior and selected-text updates. | `tests/test_components.py` checks split anatomy; `tests/browser/test_dropdowns.py` and gauntlet browser tests check viewport containment and menu behavior. |
| Residual risk | Automated tests cover rendered semantics, keyboard events, escaping, and viewport behavior, but no manual screen-reader or assistive-technology proof is claimed. Roving-arrow menu navigation remains unpublished. | Automated tests cover rendered semantics and keyboard behavior, but no manual screen-reader or assistive-technology proof is claimed. | Automated tests cover rendered semantics and viewport behavior, but no manual screen-reader or assistive-technology proof is claimed. Roving-arrow menu navigation remains unpublished. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy, escaping, route attrs, and
  pre-hydration `x-cloak` contracts.
- `tests/browser/test_dropdowns.py` for open/close, Escape, outside click,
  event payload round trips, viewport alignment, select keyboard behavior, and
  selected-text updates.
