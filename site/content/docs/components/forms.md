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

The largest component set in chirp-ui. All field macros live in `chirpui/forms.html` and share a common wrapper (`field_wrapper`) that provides labels, hints, required markers, and error display via the `field_errors` filter.

```text
{% from "chirpui/forms.html" import form, fieldset, text_field, select_field, form_actions %}
```

---

## Form structure

### form

Wrapper `<form>` element with first-class HTMX attribute support. Mutating HTMX forms (`hx-post`, `hx-put`, `hx-patch`, `hx-delete`) automatically get `hx-select="unset"`, `hx-disinherit="hx-select"`, and a reset-on-success handler unless overridden.

```text
form(action, method="get", enctype=none, cls="", attrs="", attrs_map=none,
     hx_get=none, hx_post=none, hx_put=none, hx_patch=none, hx_delete=none,
     hx_target=none, hx_swap=none, hx_trigger=none, hx_include=none,
     hx_select=none, hx_select_oob=none, hx_disabled_elt=none, hx_sync=none,
     hx_ext=none, hx_vals=none, hx_reset_on_success=none)
```

| Param | Default | Description |
|-------|---------|-------------|
| `action` | required | Form action URL |
| `method` | `"get"` | HTTP method |
| `enctype` | `none` | Set to `"multipart/form-data"` for file uploads |
| `hx_post` / `hx_put` / etc. | `none` | HTMX verb attrs; triggers auto-reset and `hx-select="unset"` |
| `hx_reset_on_success` | auto | Explicit `true`/`false` overrides the auto-detect |
| `hx_sync` | `none` | Prevent double-submit, e.g. `"this:replace"` |
| `attrs_map` | `none` | Dict of extra HTML attributes |

```text
{% call form("/items", method="post", hx_post="/items", hx_target="#list", hx_swap="beforeend") %}
    {{ text_field("title", label="Title", required=true) }}
    {% call form_actions(align="end") %}
        {{ btn("Save", type="submit", variant="primary") }}
    {% end %}
{% end %}
```

### fieldset

Groups related fields with an optional legend.

```text
fieldset(legend=none, cls="")
```

```text
{% call fieldset(legend="Shipping address") %}
    {{ text_field("street", label="Street") }}
    {{ text_field("city", label="City") }}
{% end %}
```

### field_wrapper

Internal shared wrapper used by most fields. You rarely call it directly, but it controls the label/hint/error layout.

```text
field_wrapper(name, label=none, errors=none, required=false, hint=none, modifier="")
```

### form_actions

Button row for submit/cancel. Use `align="end"` for right-aligned buttons.

```text
form_actions(align="start", cls="")
```

```text
{% call form_actions(align="end") %}
    {{ btn("Cancel", variant="ghost") }}
    {{ btn("Save", type="submit", variant="primary") }}
{% end %}
```

### hidden_field / csrf_hidden

```text
hidden_field(name, value="")
csrf_hidden(token=none, field_name="_csrf_token")
```

`csrf_hidden` calls Chirp's `csrf_token()` when no explicit token is passed. For non-Chirp apps, pass the token directly.

---

## Basic fields

All basic fields accept `name`, `label`, `errors`, `required`, `hint`, and render inside `field_wrapper`. Errors display automatically when the `errors` dict contains a matching key.

### text_field

```text
text_field(name, value="", label=none, errors=none, type="text",
           required=false, placeholder="", hint=none, attrs="")
```

Use the `type` param for `email`, `url`, `tel`, etc.

```text
{{ text_field("email", label="Email", type="email", required=true,
              placeholder="you@example.com", hint="We won't share this.") }}
```

### password_field

```text
password_field(name="password", value="", label=none, errors=none, required=true,
               placeholder="", hint=none, autocomplete="current-password", attrs="")
```

Defaults `autocomplete` to `"current-password"`. Use `"new-password"` on registration forms.

### textarea_field

```text
textarea_field(name, value="", label=none, errors=none,
               rows=4, required=false, placeholder="", hint=none)
```

### select_field

```text
select_field(name, options, selected="", label=none, errors=none,
             required=false, hint=none)
```

`options` is a list of `{"value": ..., "label": ...}` dicts.

```text
{{ select_field("status", options=[
    {"value": "draft", "label": "Draft"},
    {"value": "published", "label": "Published"},
], selected="draft", label="Status") }}
```

### multi_select_field

```text
multi_select_field(name, options, selected=none, label=none, errors=none,
                   required=false, hint=none, size=4)
```

Native `<select multiple>`. `selected` is a list of values. `size` controls visible rows.

### checkbox_field

```text
checkbox_field(name, checked=false, label=none, errors=none)
```

Renders an inline label with the checkbox.

### radio_field

```text
radio_field(name, options, selected="", label=none, errors=none,
            required=false, hint=none, layout="vertical")
```

`layout` can be `"vertical"` or `"horizontal"`.

### file_field

```text
file_field(name, label=none, errors=none, accept="", multiple=false,
           required=false, hint=none)
```

### date_field

```text
date_field(name, value="", label=none, errors=none, required=false,
           min=none, max=none, hint=none)
```

### range_field

```text
range_field(name, value=50, min=0, max=100, step=1, label=none,
            errors=none, hint=none, show_value=false)
```

When `show_value=true`, an `<output>` element displays the current value next to the label.

---

## Special fields

### toggle_field

Switch-style checkbox with optional size, color variant, and inside labels.

```text
toggle_field(name, checked=false, label=none, errors=none,
             size="", variant="", label_inside=false)
```

| Param | Values | Description |
|-------|--------|-------------|
| `size` | `"sm"`, `"lg"` | Small or large track |
| `variant` | `"success"`, `"danger"`, `"accent"` | Color when checked |
| `label_inside` | `false` | Show ON/OFF text inside the track |

```text
{{ toggle_field("dark_mode", checked=true, label="Dark mode", variant="accent") }}
```

### star_rating

CSS-only interactive star picker. Uses reverse-order radio inputs with `row-reverse` flex so the `~` sibling selector fills stars up to the hovered one.

```text
star_rating(name, count=5, selected=0, label=none, errors=none,
            required=false, hint=none, size="")
```

```text
{{ star_rating("rating", count=5, selected=3, label="Your rating") }}
```

### thumbs

Binary thumbs-up / thumbs-down radio pair.

```text
thumbs(name, selected="", label=none, errors=none,
       required=false, hint=none, size="")
```

`selected` is `"up"` or `"down"`.

### segmented_control

Connected button-group radio selector. Good for small option sets (2--5 items).

```text
segmented_control(name, options, selected="", label=none, errors=none,
                  required=false, hint=none, size="")
```

```text
{{ segmented_control("view", options=[
    {"value": "grid", "label": "Grid"},
    {"value": "list", "label": "List"},
], selected="grid", label="View mode") }}
```

### number_scale

NPS-style numbered radio row (e.g. 0--10).

```text
number_scale(name, min=0, max=10, selected=none, label=none, errors=none,
             required=false, hint=none, low_label="", high_label="")
```

```text
{{ number_scale("nps", label="How likely are you to recommend us?",
                low_label="Not at all", high_label="Extremely") }}
```

### input_group

Text input with a prefix and/or suffix (text or slotted content like icons).

```text
input_group(name, prefix=none, suffix=none, value="", label=none,
            errors=none, type="text", required=false, placeholder="",
            hint=none, attrs="")
```

```text
{{ input_group("price", prefix="$", suffix=".00", label="Price",
               placeholder="0", type="number") }}
```

---

## Masked fields (Alpine.js)

These require the `@alpinejs/mask` plugin (loaded by Chirp when Alpine is enabled).

### masked_field

Generic masked input. Pass `mask` for a static pattern or `mask_dynamic` for an Alpine expression.

```text
masked_field(name, value="", label=none, errors=none, mask=none, mask_dynamic=none,
             required=false, placeholder="", hint=none, attrs="")
```

```text
{{ masked_field("ssn", mask="999-99-9999", label="SSN") }}
{{ masked_field("expiry", mask="99/99", label="Card expiry") }}
```

### phone_field

Pre-configured masked field for phone numbers.

```text
phone_field(name, value="", label=none, errors=none, format="us",
            required=false, placeholder="", hint=none, attrs="")
```

`format`: `"us"` = `(999) 999-9999`, `"uk"` = `9999 999 9999`, `"intl"` = `+9 999 999 9999`.

### money_field

Currency input using Alpine `$money()`.

```text
money_field(name, value="", label=none, errors=none,
            decimal_sep=".", thousands_sep=",", precision=2,
            required=false, placeholder="", hint=none, attrs="")
```

---

## Search fields

### search_field

Text input with optional HTMX-powered live search (debounced `hx-get`).

```text
search_field(name, value="", label=none, search_url=none, search_target=none,
             search_trigger="keyup changed delay:300ms", search_include=none,
             search_sync=none, placeholder="Search...", errors=none, attrs="",
             attrs_map=none, search_attrs_map=none, search_hx_select=none)
```

When `search_url` and `search_target` are both set, the input fires `hx-get` on keyup with `hx-sync="this:replace"` to cancel stale requests.

### search_bar

Composite search input with layout variants. Use inside a `form()`.

```text
search_bar(name, value="", variant="solo", label=none, search_url=none,
           search_target=none, search_trigger="keyup changed delay:300ms",
           search_include=none, search_sync=none, placeholder="Search...",
           button_label="Search", button_icon="⌕", errors=none, attrs="",
           attrs_map=none, search_attrs_map=none, search_hx_select=none)
```

| Variant | Description |
|---------|-------------|
| `"solo"` | Input only, for live search |
| `"with-button"` | Input + compact submit button |
| `"with-icon"` | Input with a search icon prefix |

### key_value_form

Inline key + value inputs with a submit button. Useful for config/settings UIs.

```text
key_value_form(action, method="post", key_placeholder="", value_placeholder="",
               submit_label="Set", key_options=none, key_name="key",
               value_name="value", attrs="", attrs_map=none, cls="")
```

When `key_options` is provided, the key input gets a `<datalist>` for autocomplete suggestions.

---

## Companion templates

These macros live in their own template files but are closely related to forms.

### inline_edit_field (chirpui/inline_edit_field.html)

Click-to-edit pattern: a display view that swaps to an inline form on click.

```text
{% from "chirpui/inline_edit_field.html" import inline_edit_field_display, inline_edit_field_form %}
```

### tag_input (chirpui/tag_input.html)

Alpine-powered multi-tag input with add/remove.

```text
{% from "chirpui/tag_input.html" import tag_input %}
```

### segmented_control (chirpui/segmented_control.html)

Standalone version of the segmented control, also available as a standalone import.

```text
{% from "chirpui/segmented_control.html" import segmented_control %}
```

### wizard_form (chirpui/wizard_form.html)

Multi-step form with Alpine-managed state. See [Wizard forms](../guides/wizard-forms.md).

```text
{% from "chirpui/wizard_form.html" import wizard_form %}
```

### filter_bar (chirpui/filter_bar.html)

Form + `action_strip` layout for list/table toolbars. Uses standard form submission or HTMX.

```text
{% from "chirpui/filter_bar.html" import filter_bar %}
```

### filter_chips (chirpui/filter_chips.html)

Faceted pill-row filters with HTMX and `register_colors` support.

```text
{% from "chirpui/filter_chips.html" import filter_group, filter_chip %}
```

### search_header (chirpui/search_header.html)

Page-level search header with search bar and optional action buttons.

```text
{% from "chirpui/search_header.html" import search_header %}
```

### selection_bar (chirpui/selection_bar.html)

Sticky bar that appears when items in a list/table are selected, showing count and bulk actions.

```text
{% from "chirpui/selection_bar.html" import selection_bar %}
```

---

## Errors

Pass a Chirp error dict as `errors` to any field. The `field_errors` filter extracts messages for the given field name. When using chirp-ui without Chirp, define your own `field_errors` filter or pass `errors=none`.

```text
{{ text_field("title", value=form.title, label="Title",
              errors=errors, required=true) }}
```

See [Filters](../reference/filters.md) for filter details.

## HTMX patterns

Forms inside boosted layouts need `hx-select="unset"`, `hx-swap="innerHTML transition:false"`, and `hx-disinherit="hx-select"`. The `form()` macro handles `hx-select` and `hx-disinherit` automatically for mutating verbs. See [HTMX patterns](../guides/htmx-patterns.md).

## Related

- [Wizard forms](../guides/wizard-forms.md)
- [Buttons](./buttons.md)
- [Inline edit field](./inline-edit-field.md)
- [Filter bar / Filter chips](./filter-bar.md)
