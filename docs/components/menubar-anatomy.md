# Menubar Anatomy

**Status:** shipped contract
**Scope:** `menubar`, `menubar__item`
**Runtime:** Alpine.js through `chirpui-alpine.js`

The menubar is a horizontal application menu bar with top-level triggers and
vertical submenus. It is distinct from `dropdown_menu` command triggers and from
URL-backed `route_tabs` navigation.

## Macro

Import from `chirpui/menubar.html`:

```kida
{% from "chirpui/menubar.html" import menubar %}

{{ menubar(label="Application menu", items=[
  {"label": "File", "items": [
    {"label": "New", "action": "new"},
    {"label": "Open", "action": "open"},
  ]},
  {"label": "Edit", "items": [
    {"label": "Undo", "action": "undo"},
  ]},
]) }}
```

## Rendered Contract

- root class: `chirpui-menubar` with `role="menubar"` and `aria-label`
- trigger class: `chirpui-menubar__trigger` with `role="menuitem"`
- submenu class: `chirpui-menubar__menu` with `role="menu"`
- item class: `chirpui-menubar__item` with `--danger` / `--muted` variants
- Alpine controller: `x-data="chirpuiMenubar()"` with `x-init="init()"`
- generated id: `x-id="['menubar-panel']"`
- menu count: `data-menu-count`

Top-level triggers bind `aria-haspopup="menu"`, bound `aria-expanded`, bound
`aria-controls`, and `@keydown="onTriggerKeydown($event, index)"`.

Submenus render with `x-show="openIndex === index"`, `x-cloak`, and
`x-transition`. Items use `tabindex="-1"` and escaped `data-label` /
`data-action` / `data-href` attributes.

## Selection Events

Action items dispatch `chirpui:menubar-selected` with payloads read from escaped
DOM attributes:

```javascript
{ label: "New", action: "new" }
```

Href items navigate natively and close the open submenu on click.

## Focus And Keyboard Behavior

Top-level roving focus:

- ArrowLeft and ArrowRight move focus between top-level triggers and close any
  open submenu
- ArrowDown, Enter, or Space on a trigger opens its submenu and focuses the
  first item
- Escape closes the open submenu and returns focus to its trigger

Global dismiss:

- Escape on the root closes all submenus
- Click outside closes all submenus
- Focus leaving an open submenu closes it

## Boundary

Use `dropdown_menu` for compact command triggers, `navigation_menu` for site
navigation with flyouts, and `route_tabs` for URL-backed views.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered menubar family, not descriptor or manifest
metadata.

| Field | Menubar |
| --- | --- |
| Surface | `menubar` horizontal application menu with vertical submenus. |
| Label | `stable` rendered macro contract under the stable `menubar` component family. |
| Anatomy | `.chirpui-menubar`, `.chirpui-menubar__trigger`, `.chirpui-menubar__menu`, `.chirpui-menubar__item`, generated `menubar-panel` ids, `data-menu-count`, trigger/panel refs. |
| Native semantics | Root uses `role="menubar"`; top-level triggers and submenu items use `menuitem`; submenus use `role="menu"` with `aria-orientation="vertical"`. |
| Keyboard | ArrowLeft/ArrowRight move between top-level triggers; ArrowDown/Enter/Space open submenus; Escape closes and returns focus to the owning trigger. |
| Focus | Opening a submenu focuses the first item in `$nextTick`; closing returns focus to the trigger when invoked from keyboard dismissal paths. |
| Runtime | Requires `chirpuiMenubar()` in `chirpui-alpine.js`, Alpine refs, `x-id`, `x-show`, `x-cloak`, `x-transition`, outside/focusin handlers. |
| Motion | Submenus use `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Submenus are absolutely positioned under their trigger with floating elevation; browser gauntlet covers open/close behavior at default fixture widths. |
| Security and escaping | Selection payloads are read from escaped `data-label` and `data-action` attributes; href items use template attribute helpers and `route_link_attrs()` where applicable. |
| Performance | Open/close state is local to the menubar root; no page-global observers are part of the contract. |
| Proof | `tests/test_components.py` checks rendered menubar/submenu anatomy; `tests/browser/test_menubar_gauntlet.py` checks top-level roving focus, submenu open, Escape/outside close, selection events, and axe. |
| Residual risk | Automated tests cover rendered semantics and keyboard behavior, but no manual screen-reader or assistive-technology proof is claimed. Submenu vertical ArrowUp/Down roving is not yet published. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy and ARIA roles.
- `tests/browser/test_menubar_gauntlet.py` for top-level roving focus, submenu
  open, Escape/outside close, selection payload round trips, and axe scans.
