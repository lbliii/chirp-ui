# Drawer And Tray Anatomy

**Status:** shipped contract
**Scope:** `drawer`, `drawer_trigger`, `tray`, `tray_trigger`
**Runtime:** native `<dialog>` plus Alpine.js through `chirpui-alpine.js`

Chirp UI has two slide-out panel models:

- Native drawers: `drawer` renders `<dialog>` and opens through
  `chirpuiDialogTarget()`.
- Store-backed trays: `tray` renders a div-based dialog surface controlled by
  `Alpine.store("trays")`.

Use native drawers when browser dialog behavior is the right fit. Use trays
when the surface needs store-controlled open state and explicit
`chirpui:tray-closed` events.

## Native Drawer Contract

Import from `chirpui/drawer.html`:

```kida
{% from "chirpui/drawer.html" import drawer, drawer_trigger %}

{{ drawer_trigger("filters", label="Open filters") }}

{% call drawer("filters", title="Filters", side="right") %}
  <p>Drawer content.</p>
{% end %}
```

`drawer(...)` renders:

- `<dialog id="...">`
- `closedby="any"`
- root classes: `.chirpui-drawer` and `.chirpui-drawer--left` or
  `.chirpui-drawer--right`
- `.chirpui-drawer__panel`
- optional `.chirpui-drawer__header` when `title` is provided
- `.chirpui-drawer__title`
- `.chirpui-drawer__header-actions` slot
- close form with `method="dialog"`
- `.chirpui-drawer__close` with `aria-label="Close"`
- `.chirpui-drawer__body`

`drawer_trigger(...)` renders:

- `<button type="button">`
- `.chirpui-drawer-trigger`
- `x-data="chirpuiDialogTarget()"`
- `data-dialog-target`
- `@click="open()"`

`chirpuiDialogTarget().open()` resolves `data-dialog-target` or `data-target`
and calls the target dialog's `showModal()` method.

## Tray Contract

Import from `chirpui/tray.html`:

```kida
{% from "chirpui/tray.html" import tray, tray_trigger %}

{{ tray_trigger("filters", "Filters", icon="settings") }}

{% call tray("filters", "Filters", position="right") %}
  <p>Tray content.</p>
{% end %}
```

`tray_trigger(...)` renders:

- `<button type="button">`
- `.chirpui-btn.chirpui-btn--default.chirpui-btn--sm`
- inline Alpine store open action for `$store.trays[id]`
- optional icon span with `aria-hidden="true"`
- `aria-controls="tray-{id}"`
- bound `aria-expanded`

`tray(...)` renders:

- root `.chirpui-tray`
- position class `.chirpui-tray--left` or `.chirpui-tray--right`
- static `.chirpui-tray--closed` for pre-hydration safety
- id `tray-{id}`
- `role="dialog"`
- `aria-modal="true"`
- `aria-labelledby="tray-{id}-title"`
- static and bound `aria-hidden`
- `.chirpui-tray__backdrop`
- `.chirpui-tray__panel`
- `x-trap.inert.noscroll="$store.trays[id]"`
- `.chirpui-tray__header`
- `.chirpui-tray__title`
- `.chirpui-tray__close`
- `.chirpui-tray__body`

The backdrop and close button set `$store.trays[id] = false` and dispatch
`chirpui:tray-closed` with:

```javascript
{ id: "filters" }
```

## Focus And Closing

Native drawers rely on browser `<dialog>` behavior once opened with
`showModal()`. Close controls use `form method="dialog"`, and Escape closes the
native dialog.

Trays rely on Alpine store state, `x-trap.inert.noscroll`, backdrop clicks, and
explicit close buttons. Tray close actions dispatch `chirpui:tray-closed`;
native drawers currently do not emit this event.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](DESIGN-interactive-anatomy.md). It is a
docs/tests contract for the rendered drawer/tray family, not descriptor or
manifest metadata.

| Field | Native drawer | Tray |
| --- | --- | --- |
| Surface | `drawer` plus `drawer_trigger`. | `tray` plus `tray_trigger`. |
| Label | `stable` | `stable` |
| Anatomy | `<dialog id>`, `.chirpui-drawer`, side class, panel, optional header, title, header actions slot, close form, close button, body, trigger button, `data-dialog-target`. | Store-backed root `#tray-{id}`, position class, pre-hydration closed class, backdrop, panel, header, title, close button, body, trigger button, `data-tray-id`, and store-bound state. |
| Native semantics | Native `<dialog>` opened with `showModal()`; trigger is a `<button type="button">`; close is a `form method="dialog"` submit button with `aria-label="Close"`. | Div-based dialog surface with `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, static and bound `aria-hidden`, trigger `aria-controls`, and bound `aria-expanded`. |
| Keyboard | Native dialog keyboard behavior after `showModal()`; Escape closes the dialog; close control is a normal button. | Alpine focus trap owns keyboard containment while open; explicit close button and backdrop close the tray. |
| Focus | Browser owns native drawer focus behavior after `showModal()`; visible focus comes from global control styles; trigger wiring is covered by browser tests. | `x-trap.inert.noscroll` contains focus while open and releases it when store state closes; Alpine lifecycle tests cover store initialization and persistence behavior across boosted navigation. |
| Runtime | `chirpuiDialogTarget()` resolves `data-dialog-target` or `data-target` and calls `showModal()`; requires native `<dialog>` support plus `chirpui-alpine.js` for the trigger factory. | Requires Alpine store `Alpine.store("trays")`, `data-tray-id`, inline Alpine bindings, and `x-trap.inert.noscroll`; dispatches `chirpui:tray-closed` on explicit close paths. |
| Motion | Drawer slide behavior is CSS-owned; reduced-motion expectations follow component CSS and transition-token governance. | Tray open/closed classes are state-bound; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Side classes own placement; panel and body own local content flow; browser tests cover long title/body pressure at phone and tablet widths. | Position classes own placement; panel and body own local content flow; browser tests cover long title/body pressure at phone and tablet widths. |
| Security and escaping | Macro arguments render through normal template escaping and `html_attrs`/attribute helpers; no raw HTML escape hatch is part of drawer anatomy. | Id/title/content arguments render through template escaping and attributes; tray ids stay in escaped `data-tray-id` attributes and out of Alpine JavaScript string literals. |
| Performance | Trigger lookup is local to the target id; no page-global listeners or observers are required by native drawer anatomy. | Uses one Alpine store and local bindings; no per-frame work, scroll listeners, or observers are part of the tray contract. |
| Proof | `tests/test_components.py` checks rendered anatomy and trigger wiring; `tests/browser/test_drawer.py` checks trigger/open/close/Escape behavior and long-content overflow. | `tests/test_components.py` checks anatomy, pre-hydration state, focus-trap attributes, close events, CSS pressure, and id payload safety; `tests/browser/test_tray.py` checks open/close, backdrop close, `chirpui:tray-closed`, ARIA, and long-content overflow; `tests/browser/test_alpine_lifecycle.py` checks store initialization and persistence behavior. |
| Residual risk | Automated tests cover rendered semantics, native close behavior, Escape, and overflow, but no manual screen-reader or assistive-technology proof is claimed. | Automated tests cover rendered semantics, focus-trap wiring, events, and overflow, but no manual screen-reader or assistive-technology proof is claimed. A browser test currently dispatches the close click directly because of a known hit-target anomaly with the app-shell topbar. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for drawer and tray rendered anatomy, trigger
  wiring, pre-hydration closed state, focus-trap attributes, and close events.
- `tests/browser/test_drawer.py` for native drawer trigger/open/close/Escape
  behavior.
- `tests/browser/test_tray.py` for tray open/close, backdrop close,
  `chirpui:tray-closed`, and ARIA attributes.
- `tests/browser/test_alpine_lifecycle.py` for Alpine store initialization and
  persistence behavior across boosted navigation.
