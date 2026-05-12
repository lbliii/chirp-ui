# Modal Anatomy

**Status:** shipped contract
**Scope:** `modal`, `modal_trigger`, `modal_overlay`, `modal_overlay_trigger`,
`confirm_dialog`, `confirm_trigger`
**Runtime:** native `<dialog>` plus Alpine.js through `chirpui-alpine.js`

Chirp UI has two modal models:

- Native dialogs: `modal` and `confirm_dialog` render `<dialog>` and rely on
  browser dialog behavior after `showModal()`.
- Store-backed overlays: `modal_overlay` renders a div-based dialog surface
  controlled by `Alpine.store("modals")`.

Do not treat the two models as interchangeable in tests or docs.

## Native Modal Contract

Import native modal macros from `chirpui/modal.html`:

```kida
{% from "chirpui/modal.html" import modal, modal_trigger %}

{{ modal_trigger("settings", label="Open settings") }}

{% call modal("settings", title="Settings", size="lg") %}
  <p>Modal content.</p>
  {% slot footer %}
    <form method="dialog">
      <button type="submit">Done</button>
    </form>
  {% end %}
{% end %}
```

`modal(...)` renders:

- `<dialog id="...">`
- `closedby="any"`
- root classes from the `modal` BEM block, including `chirpui-modal--sm`,
  `chirpui-modal--md`, or `chirpui-modal--lg`
- optional `.chirpui-modal__header` when `title` is provided
- `.chirpui-modal__title`
- `.chirpui-modal__header-actions` slot
- close form with `method="dialog"`
- `.chirpui-modal__close` with `aria-label="Close"`
- `.chirpui-modal__body`
- `.chirpui-modal__footer`

`modal_trigger(...)` renders:

- `<button type="button">`
- `.chirpui-modal-trigger`
- `x-data="chirpuiDialogTarget()"`
- `data-dialog-target`
- `@click="open()"`

`chirpuiDialogTarget().open()` resolves `data-dialog-target` or `data-target`
and calls the target dialog's `showModal()` method.

## Confirm Dialog Contract

Import confirmation macros from `chirpui/confirm.html`:

```kida
{% from "chirpui/confirm.html" import confirm_dialog, confirm_trigger %}

{{ confirm_trigger("delete-item", label="Delete") }}

{{ confirm_dialog(
  "delete-item",
  title="Delete item?",
  message="This cannot be undone.",
  variant="danger",
  confirm_url="/items/1/delete",
  confirm_method="DELETE",
  hx_target="#items"
) }}
```

`confirm_dialog(...)` renders a native `<dialog>` with:

- root classes: `.chirpui-confirm`, `.chirpui-modal`, `.chirpui-modal--small`
- optional `.chirpui-confirm--danger`
- `closedby="any"`
- modal header/title/close classes shared with `modal`
- `.chirpui-confirm__icon` for danger dialogs
- `.chirpui-confirm__message`
- `.chirpui-confirm__footer`
- cancel form with `method="dialog"`
- confirm form

When `confirm_url` is omitted, the confirm action also uses
`method="dialog"`. When `confirm_url` is provided, the confirm form renders
`method`, `action`, and optional HTMX attributes.

With `hx_target`, confirm forms disinherit shell HTMX attributes using:

```html
hx-disinherit="hx-select hx-target hx-swap"
```

`confirm_method="DELETE"` emits `hx-delete`; other HTMX submit paths currently
emit `hx-post`.

`confirm_trigger(...)` uses the same `chirpuiDialogTarget()` contract as
`modal_trigger(...)` and adds `.chirpui-confirm-trigger`.

## Modal Overlay Contract

Import overlay macros from `chirpui/modal_overlay.html`:

```kida
{% from "chirpui/modal_overlay.html" import modal_overlay, modal_overlay_trigger %}

{{ modal_overlay_trigger("confirm", "Open") }}

{% call modal_overlay("confirm", "Confirm") %}
  <p>Overlay content.</p>
{% end %}
```

`modal_overlay_trigger(...)` renders:

- `<button type="button">`
- `.chirpui-btn` plus optional variant class and `.chirpui-btn--sm`
- inline Alpine access to `$store.modals[id]`
- `aria-controls="modal-{id}"`
- bound `aria-expanded`

`modal_overlay(...)` renders:

- root `.chirpui-modal chirpui-modal--closed`
- id `modal-{id}`
- role `dialog`
- `aria-modal="true"`
- `aria-labelledby="modal-{id}-title"`
- bound `aria-hidden`
- `.chirpui-modal__backdrop`
- `.chirpui-modal__panel`
- `x-trap.inert.noscroll="$store.modals[id]"`
- `.chirpui-modal__header`
- `.chirpui-modal__title`
- `.chirpui-modal__close`
- `.chirpui-modal__body`

The backdrop and close button set `$store.modals[id] = false` and dispatch
`chirpui:modal-closed` with:

```javascript
{ id: "confirm" }
```

## Focus And Closing

Native dialogs rely on browser `<dialog>` behavior once opened with
`showModal()`. Close controls use `form method="dialog"` unless a confirm action
submits to an explicit URL.

Modal overlays rely on Alpine state, `x-trap.inert.noscroll`, backdrop clicks,
and explicit close buttons. Overlay close actions dispatch
`chirpui:modal-closed`; native dialogs currently do not emit this event.

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered modal, overlay, confirm, HTMX, ARIA,
  close-control, and trigger anatomy.
- `tests/browser/test_modals.py` for overlay open/close/events, native
  `showModal()` opening, native close forms, and confirm trigger/cancel behavior.
- `tests/browser/test_alpine_lifecycle.py` for modal store initialization and
  known store behavior across navigation.
