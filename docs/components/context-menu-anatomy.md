# Context Menu Anatomy

**Status:** shipped contract
**Scope:** `context_menu`, `context_menu__item`
**Runtime:** Alpine.js through `chirpui-alpine.js`

Context menus are contextual command surfaces opened from an owning object,
region, row, card, canvas, or tree item. They are not primary navigation, not
a replacement for visible row actions, and not a general dropdown trigger style.

## Macro

Import from `chirpui/context_menu.html`:

```kida
{% from "chirpui/context_menu.html" import context_menu %}

{% call context_menu(items=[
  {"label": "Open", "action": "open", "icon": "↗"},
  {"label": "Rename", "action": "rename"},
  {"label": "Delete", "action": "delete", "variant": "danger"},
], label="Row actions") %}
  <div class="chirpui-surface">Right-click for actions</div>
{% end %}
```

## Rendered Contract

- root class: `chirpui-context-menu` (`display: contents`; hosts trigger + panel)
- trigger class: `chirpui-context-menu__target`
- panel class: `chirpui-context-menu__panel`
- item class: `chirpui-context-menu__item` with `--danger` / `--muted` variants
- Alpine controller: `x-data="chirpuiContextMenu()"`
- generated id: `x-id="['context-menu-panel']"`
- item count: `data-item-count`

The trigger renders as `role="button"`, `tabindex="0"`, `aria-haspopup="menu"`,
bound `aria-expanded`, bound `aria-controls`, and `@contextmenu.prevent`.

The panel renders as `role="menu"`, `aria-orientation="vertical"`, fixed at
pointer coordinates via `:style`, `x-show="open"`, `x-cloak`, and `x-transition`.

Items render as `<a role="menuitem">` when `href` is present or
`<button type="button" role="menuitem">` otherwise, each with `tabindex="-1"`,
`x-ref="item-N"`, and escaped `data-label` / `data-action` / `data-href`
attributes.

## Selection Events

`context_menu` dispatches `chirpui:context-menu-selected` from
`chirpuiContextMenu().selectItem()`.

Selection payloads are rendered into escaped DOM attributes and read by named Alpine code,
not interpolated into Alpine JavaScript object literals:

```javascript
{ label: "Rename", action: "rename" }
{ label: "Docs", href: "/docs" }
```

## Focus And Keyboard Behavior

Pointer open uses the native `contextmenu` event at `clientX/clientY`.
Keyboard open from the focused trigger accepts Enter, Space, ArrowDown,
`ContextMenu` or Shift+F10 and positions from the trigger rectangle.

Inside the open menu:

- ArrowDown and ArrowUp move among items via roving tabindex
- Home and End move to first and last item
- Enter and Space activate the focused item through `@click="selectItem($el)"`
- Escape closes the menu and returns focus to the trigger
- Click outside and focus leaving the panel close the menu

Disabled items stay focusable with `aria-disabled="true"` and do not dispatch
selection events.

The Alpine factory clamps the panel to the viewport on open.

## Boundary

Use existing components for non-contextual commands:

- `row_actions(...)` or `dropdown_menu(...)` for visible action affordances.
- `action_strip(...)` or `action_bar(...)` for page-level commands.
- `dropdown_select(...)` for command/filter selection.

Do not reuse `dropdown_menu(...)` as a fake context menu.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered context menu family, not descriptor or
manifest metadata.

| Field | Context menu |
| --- | --- |
| Surface | `context_menu` contextual command menu around a non-interactive region. |
| Label | `stable` rendered macro contract under the stable `context-menu` component family. |
| Anatomy | `.chirpui-context-menu`, `.chirpui-context-menu__target`, `.chirpui-context-menu__panel`, `.chirpui-context-menu__item`, generated `context-menu-panel` id, `data-item-count`, item `x-ref`s. |
| Native semantics | Focusable trigger with `role="button"`, `tabindex="0"`, `aria-haspopup="menu"`, bound `aria-expanded`, and bound `aria-controls`; menu uses `role="menu"`; items use `menuitem`. |
| Keyboard | Opens from pointer or keyboard trigger contract; ArrowDown/Up/Home/End roving focus; Escape and outside click close; disabled items are focusable-but-inert. |
| Focus | Open moves focus to the first item in `$nextTick`; close returns focus to the trigger synchronously before hiding the panel. |
| Runtime | Requires `chirpuiContextMenu()` in `chirpui-alpine.js`, Alpine refs, `x-id`, `x-show`, `x-cloak`, `x-transition`, viewport clamping, and outside/focusout handlers. |
| Motion | Panel uses `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Panel is `position: fixed`, clamped to the viewport, with `max-inline-size` and scroll when needed; browser gauntlet covers pointer positioning inside the viewport. |
| Security and escaping | Selection payloads are read from escaped `data-label`, `data-action`, and `data-href` attributes; templates must not interpolate server values into Alpine JavaScript object literals. |
| Performance | Viewport clamping runs on open via local panel refs; no page-global observers are part of the contract. |
| Proof | `tests/test_components.py` checks rendered anatomy, variants, href/disabled/icon modes, and item counts; `tests/browser/test_context_menu_gauntlet.py` checks pointer/keyboard open, roving focus, Escape/outside close, selection events, disabled inertness, and axe. |
| Residual risk | Automated tests cover rendered semantics, keyboard events, escaping, and viewport behavior, but no manual screen-reader or assistive-technology proof is claimed. Submenus, checkbox/radio items, and typeahead search remain out of scope for v1. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy, escaping, variants, and item
  counts.
- `tests/browser/test_context_menu_gauntlet.py` for pointer/keyboard open,
  roving focus, Escape/outside close, selection payload round trips, disabled
  inertness, and axe scans.
