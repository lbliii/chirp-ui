---
title: Build a CRUD app
description: Forms, tables, modals, toast, and fragment islands
draft: false
weight: 57
lang: en
type: doc
keywords: [chirp-ui, tutorial, crud, htmx]
icon: database
---

# Build a CRUD app

End-to-end pattern for list → create/edit → delete with htmx.

## 1. List view

Render **`table`** or **`description_list`** inside **`container()`**. Wrap wide tables for horizontal scroll — [Layout overflow](../guides/layout-overflow.md).

## 2. Forms

Use macros from **`chirpui/forms.html`**. Submit with **`hx-post`** targeting a **`fragment_island`** — [HTMX patterns](../guides/htmx-patterns.md).

## 3. Modals

Use **`modal`** / **`confirm`** for destructive flows per [Dashboard patterns](../guides/dashboard-patterns.md).

## 4. Feedback

Return **`HX-Trigger`** or swap **`toast`** containers for success/error messages.

## 5. CSRF

Include your framework’s CSRF hidden field (`csrf_hidden` helper in chirp-ui forms).

## Related

- [Components: Forms](../components/forms.md)
- [Components: Tables](../components/tables-and-data.md)
- [Security](../guides/security.md)
