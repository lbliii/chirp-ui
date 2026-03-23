---
title: Wizard forms
description: Server-driven multi-step forms with HTMX
draft: false
weight: 41
lang: en
type: doc
keywords: [chirp-ui, wizard, htmx]
icon: steps
---

# Wizard forms

Use **`wizard_form`** from `chirpui/wizard_form.html` when:

- Steps submit via HTMX fragments (same URL).
- The **step indicator** and **form** must update together — swap **`outerHTML`** on the whole wizard so both stay in sync.

## Parameters

| Param | Description |
|-------|-------------|
| `id` | **Required.** Stable DOM id; forms use **`hx-target="#id"`**. |
| `steps` | List of `{id, label}` (same shape as `stepper`). |
| `current` | 1-based active step index. |
| `cls`, `attrs` | Optional classes and raw attrs. |

## Form requirements

Forms must set:

- **`hx-target="#<id>`** — the wizard’s id.
- **`hx-swap="outerHTML"`** — replace the full wrapper.

## Backend

Each step handler returns the **full** `wizard_form` block for HTMX requests. Chirp’s `Page` type can fragment full-page vs partial.

Full cookbook: [WIZARD-FORM.md](https://github.com/lbliii/chirp-ui/blob/main/docs/WIZARD-FORM.md).

## Related

- [HTMX patterns](./htmx-patterns.md)
