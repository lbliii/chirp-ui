# Context Menu Anatomy

**Status:** design contract, not shipped
**Scope:** proposed `context_menu` family
**Runtime:** expected Alpine.js through `chirpui-alpine.js`

Chirp UI does not ship a context-menu macro yet. This document is the pre-
implementation contract for the behavior-heavy surface so the eventual macro is
small, testable, and distinct from `dropdown_menu`.

Context menus are contextual command surfaces opened from an owning object,
region, row, card, canvas, or tree item. They are not primary navigation, not a
replacement for visible row actions, and not a general dropdown trigger style.

## Boundary

Use existing components today:

- `row_actions(...)` or `dropdown_menu(...)` for visible action affordances.
- `action_strip(...)` or `action_bar(...)` for page-level commands.
- `dropdown_select(...)` for command/filter selection.

Do not publish `context_menu(...)`, `context_menu_trigger(...)`, or
`chirpui-context-menu*` app markup until render tests and browser tests prove
the contract below.

## Proposed Macros

The likely macro family is:

```kida
{% from "chirpui/context_menu.html" import context_menu, context_menu_item %}

{% call context_menu(id="file-actions", label="File actions") %}
  {{ context_menu_item("Rename", action="rename") }}
  {{ context_menu_item("Duplicate", action="duplicate") }}
  {{ context_menu_item("Delete", action="delete", variant="danger") }}
{% end %}
```

The API is intentionally not approved. The implementation slice must still
decide whether items are dict-driven, child-macro-driven, or both. The decision
must follow the dropdown payload rule: server-provided labels, URLs, and actions
are rendered into escaped DOM attributes and read by named Alpine code, not
interpolated into inline JavaScript object literals.

## Trigger Semantics

A context menu needs both pointer and keyboard entry:

- Pointer: open on the native `contextmenu` event after `preventDefault()` only
  for the owned region.
- Keyboard: open from the focused owner on `ContextMenu` or `Shift+F10`.
- Optional visible trigger: allowed only as an additional affordance, not the
  sole path, because a context menu must be keyboard reachable from the owning
  object.
- Disabled owner: must not open.

The owning element needs an accessible name independent of the menu. The menu
label should identify the command group, not repeat every selected object.

## Menu Semantics

The opened panel should use menu semantics:

- menu root: `role="menu"`
- command item: `role="menuitem"`
- checkbox item, if implemented later: `role="menuitemcheckbox"`
- radio item, if implemented later: `role="menuitemradio"`
- divider: `role="separator"`
- unavailable command: `aria-disabled="true"` and skipped by activation

The first implementation should support command items and separators only.
Checkbox/radio groups, submenus, and typeahead are deferred until a second
browser-proof slice.

## Focus And Keyboard

Required behavior:

- Open moves focus into the first enabled item.
- ArrowDown and ArrowUp move among enabled items and wrap.
- Home and End move to first and last enabled item.
- Enter and Space activate the focused item.
- Escape closes the menu and returns focus to the owning element.
- Tab closes the menu and allows normal document focus movement.
- Pointer activation closes the menu and returns focus to the owner unless the
  activated element navigates away.

The implementation should use roving `tabindex`, not make every menu item
tabbable.

## Positioning And Overflow

Pointer-opened menus position from the event coordinates. Keyboard-opened menus
position from the owning element rectangle. In both cases:

- The panel must stay inside the visual viewport with the existing dropdown
  viewport-padding token policy.
- It must flip horizontally and vertically near edges.
- Long labels wrap or truncate locally without creating document horizontal
  overflow.
- Reposition on resize; do not run per-frame layout work while idle.

## Events

The proposed selection event is `chirpui:context-menu-selected` with a detail
payload assembled from escaped DOM attributes:

```javascript
{ label: "Rename", action: "rename" }
{ label: "Open", href: "/files/a" }
```

If the item is an anchor, normal navigation or HTMX route attrs should remain
available. The event is for application state and analytics hooks; it must not
be required for basic link activation.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
pre-implementation docs/tests contract, not descriptor or manifest metadata.

| Field | Context menu |
| --- | --- |
| Surface | Proposed `context_menu` contextual command surface. |
| Label | `research` until a macro, Alpine factory, render tests, and browser tests ship together. |
| Anatomy | Owning element, generated menu id, menu panel, command item rows, optional icon/shortcut/meta regions, separators, open/closed state attributes, and event-coordinate placement state. Candidate classes are not public until the macro ships. |
| Native semantics | Owner keeps its native role/name; opened panel uses `role="menu"`; command rows use `menuitem`; separators use `separator`; disabled commands use `aria-disabled="true"`. |
| Keyboard | Opens from `contextmenu`, `ContextMenu`, and `Shift+F10`; ArrowDown/ArrowUp/Home/End move roving focus; Enter/Space activates; Escape closes and returns focus; Tab closes and lets document focus continue. |
| Focus | Open focuses the first enabled item; disabled items are skipped; close returns focus to the owner unless navigation occurs; HTMX/Alpine remount must not leave focus in a detached panel. |
| Runtime | Expected named Alpine factory in `chirpui-alpine.js`, local owner/panel refs, generated ids, viewport-aware placement, and no inline `<script>` in macros. |
| Motion | Menu open/close may use existing transition tokens; reduced motion must avoid spatial animation. |
| Responsive and overflow | Pointer placement and keyboard placement both stay within the visual viewport; long labels stay inside the panel; no document-level horizontal overflow. |
| Security and escaping | Labels, hrefs, and action ids render into escaped DOM attributes and are read by named Alpine code; do not interpolate server values into Alpine JavaScript object literals. |
| Performance | Only open/resize paths may measure layout; no page-global observer or per-frame pointer work while closed. |
| Proof | Required before shipment: render anatomy tests in `tests/test_components.py`, strict-undefined item tests, escaping tests for `data-*` payloads, browser tests for pointer open, keyboard open, roving focus, activation, Escape, outside click, resize flip, and overflow containment. |
| Residual risk | No assistive-technology proof is claimed. Submenus, checkbox/radio menu items, and typeahead are deferred. |

## Implementation Gate

Before promoting this from design contract to shipped component:

1. Add macro/template, descriptor, CSS partial, Alpine factory, generated CSS,
   manifest, and component options in one slice.
2. Add render tests for roles, ids, state attrs, disabled items, separators,
   escaped payload attributes, and empty item lists under strict undefined.
3. Add browser tests for right-click, keyboard open, roving focus, activation,
   Escape/outside dismissal, focus return, resize/edge flipping, and no document
   horizontal overflow.
4. Add a component-showcase example only after browser proof exists.
5. Revisit this source doc and move any shipped facts into the published docs
   mirror.

## Not Now

- Submenus.
- Checkbox/radio menu items.
- Typeahead search.
- A global context-menu manager.
- Reusing `dropdown_menu(...)` as a fake context menu.
