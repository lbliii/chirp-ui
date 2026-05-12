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
