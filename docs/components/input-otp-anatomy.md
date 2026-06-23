# Input OTP Anatomy

**Status:** shipped contract
**Scope:** `input_otp`
**Runtime:** Alpine.js through `chirpui-alpine.js`

`input_otp` renders grouped one-time-code cells with paste, backspace, and
arrow-key navigation. A hidden input carries the composed value for form posts.

## Macro

Import from `chirpui/input_otp.html`:

```kida
{% from "chirpui/input_otp.html" import input_otp %}

{{ input_otp("code", length=6, label="Verification code") }}
```

## Rendered Contract

- root class: `chirpui-input-otp`
- label class: `chirpui-input-otp__label` (optional)
- group class: `chirpui-input-otp__group` with `role="group"`
- cell class: `chirpui-input-otp__cell`
- Alpine controller: `x-data="chirpuiInputOtp()"`
- length: `data-length`
- hidden input: `name="{{ name }}"` with `:value="value"`

Each cell renders as a single-character `input[type="text"]` with
`inputmode="numeric"`, `pattern="[0-9]*"`, `maxlength="1"`, and
`aria-label="Digit N of M"`.

## Change Events

`input_otp` dispatches `chirpui:otp-change` from `syncValue()` whenever cell
values change:

```javascript
{ value: "123456" }
```

## Focus And Keyboard Behavior

- Typing a digit keeps only the last numeric character and advances focus to the
  next cell
- Backspace on an empty cell clears the previous cell and moves focus backward
- ArrowLeft and ArrowRight move focus between cells without mutating values
- Paste spreads digits across cells up to `data-length` and updates the hidden
  value

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered input OTP surface, not descriptor or
manifest metadata.

| Field | Input OTP |
| --- | --- |
| Surface | `input_otp` grouped one-time-code entry for verification flows. |
| Label | `stable` rendered macro contract under the stable `input-otp` component family. |
| Anatomy | `.chirpui-input-otp`, `.chirpui-input-otp__label`, `.chirpui-input-otp__group`, `.chirpui-input-otp__cell`, hidden named input, `data-length`, cell `x-ref`s. |
| Native semantics | Visible cells are native text inputs with numeric input mode; the group exposes `role="group"` and per-cell accessible names. |
| Keyboard | Typing advances cells; Backspace moves backward on empty cells; ArrowLeft/ArrowRight move focus; paste fills contiguous cells. |
| Focus | Focus moves cell-by-cell through Alpine `focusElement()` helpers; paste focuses the last filled or next empty cell. |
| Runtime | Requires `chirpuiInputOtp()` in `chirpui-alpine.js`, Alpine refs, and hidden-value sync through `syncValue()`. |
| Motion | No motion-specific behavior beyond focus-visible styling on cells. |
| Responsive and overflow | Cells use fixed inline/block size and wrap within the group flex row; browser gauntlet covers default six-cell layout. |
| Security and escaping | Cell values are user-entered digits filtered to `\D` removal in Alpine handlers; hidden input value is composed locally. |
| Performance | Value sync is local to the OTP root on input/keydown/paste events; no page-global observers are part of the contract. |
| Proof | `tests/test_components.py` checks rendered anatomy and cell count; `tests/browser/test_input_otp.py` checks paste, backspace, arrow navigation, typing advance, hidden-value sync, accessible names, and `chirpui:otp-change`. |
| Residual risk | Automated tests cover keyboard and paste behavior, but no manual screen-reader or assistive-technology proof is claimed. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for rendered anatomy and cell count.
- `tests/browser/test_input_otp.py` for paste, backspace, arrow navigation,
  typing advance, hidden input sync, accessible naming, and change events.
