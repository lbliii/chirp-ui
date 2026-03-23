---
title: Accessibility
description: Keyboard, motion, focus, and semantic status
draft: false
weight: 45
lang: en
type: doc
keywords: [chirp-ui, a11y, accessibility]
icon: accessibility
---

# Accessibility

## Keyboard and focus

- Interactive components (dropdowns, modals, trays) rely on Alpine + focusable elements. Ensure **focus** moves into dialogs when opened and returns on close (Chirp/Alpine patterns).
- For **icon-only** buttons, provide **`aria-label`** or visible text.

## Motion

- Motion tokens (`--chirpui-duration-*`, `--chirpui-easing-*`) should respect **`prefers-reduced-motion`** — see [Motion and transitions](../theming/motion-and-transitions.md) and `chirpui-transitions.css`.

## Color and status

- Do not rely on color alone — pair **icons**, **labels**, and **`status`** variants.
- Use semantic tokens for status surfaces so contrast stays consistent in light/dark themes.

## Forms

- Associate **labels** with inputs (`for` / `id`); use **`field_errors`** for screen-reader-friendly error lists.

## Related

- [Pitfalls](./pitfalls.md)
- [Security](./security.md)
