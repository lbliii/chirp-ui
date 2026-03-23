---
title: Pitfalls
description: Common mistakes and how to avoid them
draft: false
weight: 43
lang: en
type: doc
keywords: [chirp-ui, footguns, debugging]
icon: warning
---

# Pitfalls

## Layout and horizontal scroll

If the page scrolls sideways, something inside the content is wider than the column — usually a non-wrapping flex row, a grid without **`min-width: 0`**, or a wide table without **`overflow-x: auto`**.

**Fix:** Use **`grid()`**, **`block()`**, **`cluster()`**, and **`chirpui-min-w-0`** on custom flex rows. See [Layout overflow](./layout-overflow.md).

## Fragment islands

- **`hx-target`** must reference an existing **`id`** in the fragment.
- When forms load via HTMX, **targets must live in the same subtree** as the form.

## Alpine.js

- **`x-data`** must wrap elements using **`x-show`** / **`@click`**.
- Use **`Alpine.safeData()`** for named components (htmx-safe re-registration).
- **Do not** load Alpine yourself — Chirp injects it when enabled.

## Registration

Call **`use_chirp_ui(app)`** or **`register_filters(app)`** before rendering templates.

## CSRF

Use your framework’s CSRF tokens on mutating forms (`csrf_hidden` in chirp-ui forms).

## More

Full guide: [ANTI-FOOTGUNS.md](https://github.com/lbliii/chirp-ui/blob/main/docs/ANTI-FOOTGUNS.md).

## Related

- [Security](./security.md)
