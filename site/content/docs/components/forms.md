---
title: Forms
description: Fields, fieldset, form actions, and validation display
draft: false
weight: 18
lang: en
type: doc
keywords: [chirp-ui, forms, fields]
icon: textbox
---

# Forms

Import from `chirpui/forms.html` (and `chirpui/auth.html` for auth-specific forms).

## Field macros

Includes `text_field`, `password_field`, `textarea_field`, `select_field`, `checkbox_field`, `toggle_field`, `radio_field`, `file_field`, `date_field`, `range_field`, `search_field`, `search_bar`, `multi_select_field`, `masked_field`, `phone_field`, `money_field`, and helpers like `fieldset`, `form`, `form_actions`, `poll_trigger`, `safe_region`.

## Errors

Use the `field_errors` filter with Chirp’s error dict shape — see [Filters](../reference/filters.md).

## HTMX

Forms inside boosted layouts may need `hx-select`, `hx-swap`, and `hx-disinherit` — see [HTMX patterns](../guides/htmx-patterns.md).

## Related

- [Wizard forms](../guides/wizard-forms.md)
- [Buttons](./buttons.md)
