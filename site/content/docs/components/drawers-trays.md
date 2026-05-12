---
title: Drawer and tray anatomy
description: Rendered anatomy and behavior contracts for native drawers and store-backed trays
draft: false
weight: 27
lang: en
type: doc
keywords: [chirp-ui, drawer, tray, dialog, alpine, anatomy]
category: components
---

# Drawer and tray anatomy

Chirp UI ships two slide-out panel contracts:

- `drawer(...)` and `drawer_trigger(...)` from `chirpui/drawer.html`
- `tray(...)` and `tray_trigger(...)` from `chirpui/tray.html`

Native drawers render `<dialog>` and open through `chirpuiDialogTarget()`.
Trays render a div-based dialog controlled through `Alpine.store("trays")`,
with `x-trap.inert.noscroll` on the panel and a `chirpui:tray-closed` event.

The full rendered contract, ARIA roles, focus and close behavior, event
payloads, and proof locations live in the canonical source guide:
[`docs/DRAWER-TRAY-ANATOMY.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/DRAWER-TRAY-ANATOMY.md?plain=1).
