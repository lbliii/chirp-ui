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

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered modal family, not descriptor or manifest metadata.

| Field | Native modal | Confirm dialog | Modal overlay |
| --- | --- | --- | --- |
| Surface | `modal` plus `modal_trigger` | `confirm_dialog` plus `confirm_trigger` | `modal_overlay` plus `modal_overlay_trigger` |
| Label | `stable` | `stable` | `stable` |
| Anatomy | `<dialog id>`, `.chirpui-modal`, size class, optional header, title, header actions slot, close form, body, footer, trigger button, `data-dialog-target`. | Native `<dialog>` with `.chirpui-confirm`, shared modal header/close/body structure, optional danger icon, message, footer, cancel form, confirm form, trigger button. | Store-backed root `#modal-{id}`, backdrop, panel, header, title, close button, body, trigger button, Alpine state bindings. |
| Native semantics | Native `<dialog>` opened with `showModal()`; trigger is a `<button type="button">`; close is a `form method="dialog"` submit button with `aria-label="Close"`. | Native `<dialog>` opened with `showModal()`; cancel uses `form method="dialog"`; confirm action is either dialog-close form or explicit form submit/HTMX action. | Div-based dialog surface with `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, bound `aria-hidden`, trigger `aria-controls`, and bound `aria-expanded`. |
| Keyboard | Native dialog keyboard behavior after `showModal()`; close/cancel controls are normal buttons. | Native dialog keyboard behavior after `showModal()`; cancel and confirm controls are normal form controls. | Alpine focus trap owns modal keyboard containment while open; close button and backdrop actions close the overlay. |
| Focus | Browser owns native modal focus behavior after `showModal()`; visible focus comes from global control styles; focus-return behavior is covered by browser tests where triggered. | Browser owns native dialog focus behavior; cancel/close use native dialog close semantics; explicit confirm submits may navigate or swap content. | `x-trap.inert.noscroll` contains focus while open and releases it when store state closes; Alpine lifecycle tests cover store initialization across navigation. |
| Runtime | `chirpuiDialogTarget()` resolves `data-dialog-target` or `data-target` and calls `showModal()`; requires native `<dialog>` support plus `chirpui-alpine.js` for the trigger factory. | Same `chirpuiDialogTarget()` trigger contract; optional HTMX submit contract emits `hx-delete` or `hx-post`; `hx-disinherit="hx-select hx-target hx-swap"` protects forms from shell inheritance. | Requires Alpine store `Alpine.store("modals")`, inline Alpine bindings, and `x-trap.inert.noscroll`; dispatches `chirpui:modal-closed` on explicit close paths. |
| Motion | No anatomy-specific animation contract beyond component CSS and transition-token governance. | No anatomy-specific animation contract beyond component CSS and transition-token governance. | Overlay open/close classes are state-bound; reduced-motion expectations follow component CSS and transition-token governance. |
| Responsive and overflow | Size classes own dialog width; modal body owns local content flow; no document-level horizontal overflow should be introduced by the shell. | Small modal sizing owns confirmation width; message/footer content should wrap locally. | Panel and body own overlay content overflow; backdrop covers the viewport without shifting the document. |
| Security and escaping | Macro arguments render through normal template escaping and `html_attrs`/attribute helpers; no raw HTML escape hatch is part of the modal anatomy contract. | Message/title/action attributes render through normal escaping; HTMX attributes are emitted from explicit macro parameters; no inline JavaScript payload interpolation. | Id/title/content arguments render through template escaping and attributes; inline Alpine expressions use component-owned state access rather than user-provided JavaScript strings. |
| Performance | Trigger lookup is local to the target id; no page-global listeners or observers are required by native modal anatomy. | Same native trigger lookup; HTMX form attributes do not add modal-family observers. | Uses one Alpine store and local bindings; no per-frame work, scroll listeners, or observers are part of the overlay contract. |
| Proof | `tests/test_components.py` checks rendered native modal anatomy; `tests/browser/test_modals.py` checks `showModal()` opening and native close forms. | `tests/test_components.py` checks confirm anatomy and HTMX attributes; `tests/browser/test_modals.py` checks confirm trigger/cancel behavior. | `tests/test_components.py` checks overlay ARIA/anatomy; `tests/browser/test_modals.py` checks overlay open/close/events; `tests/browser/test_alpine_lifecycle.py` checks store initialization across navigation. |
| Residual risk | Automated tests cover rendered semantics and browser behavior, but no manual screen-reader or assistive-technology proof is claimed. | Automated tests cover rendered semantics and browser behavior, but no manual screen-reader or assistive-technology proof is claimed. | Automated tests cover focus trap wiring and events, but no manual screen-reader or assistive-technology proof is claimed. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered modal, overlay, confirm, HTMX, ARIA,
  close-control, and trigger anatomy.
- `tests/browser/test_modals.py` for overlay open/close/events, native
  `showModal()` opening, native close forms, and confirm trigger/cancel behavior.
- `tests/browser/test_alpine_lifecycle.py` for modal store initialization and
  known store behavior across navigation.
