---
title: Modal anatomy
description: Rendered anatomy and behavior contracts for native modals, overlays, and confirm dialogs
draft: false
weight: 25
lang: en
type: doc
keywords: [chirp-ui, modal, dialog, confirm, alpine, anatomy]
category: components
---

# Modal anatomy

Chirp UI ships native dialog and store-backed overlay modal contracts:

- `modal(...)` and `modal_trigger(...)` from `chirpui/modal.html`
- `confirm_dialog(...)` and `confirm_trigger(...)` from `chirpui/confirm.html`
- `modal_overlay(...)` and `modal_overlay_trigger(...)` from `chirpui/modal_overlay.html`

Native dialogs render `<dialog>` and open through the
`chirpuiDialogTarget()` Alpine controller. Overlay modals render a div-based
dialog controlled through `Alpine.store("modals")`, with
`x-trap.inert.noscroll` on the panel.

The full rendered contract, ARIA roles, focus and close behavior, HTMX confirm
form behavior, and proof locations live in the canonical source guide:
[`docs/MODAL-ANATOMY.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/MODAL-ANATOMY.md?plain=1).
