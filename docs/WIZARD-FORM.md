# Wizard Form (server-driven multi-step)

ChirpUI provides `wizard_form` for server-driven multi-step forms with HTMX fragment swaps. It bundles the stepper, swap target, and form slot so the step indicator stays in sync when forms submit.

---

## When to use

Use `wizard_form` when:

- You have a multi-step form that submits via HTMX (fragment-style, same URL)
- The server returns the next step's form and you need the step indicator to update
- The form lives inside an app shell with `hx-boost` or broad `hx-select`

The component codifies the pattern: **swap the entire parent** (stepper + form) so both stay in sync. Swapping only the form would lose the step indicator.

---

## Usage

```html
{% from "chirpui/wizard_form.html" import wizard_form %}

{% call wizard_form("checkout", steps=steps, current=step) %}
<form method="post" action="/wizard/step2"
      hx-post="/wizard/step2"
      hx-target="#checkout"
      hx-swap="outerHTML">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  ...fields...
</form>
{% end %}
```

### Parameters

| Param | Description |
|-------|-------------|
| `id` | **Required.** Stable DOM id; must match `hx-target="#id"` on forms inside the slot. |
| `steps` | List of `{id, label}` (same shape as `stepper`). |
| `current` | 1-based index of active step. |
| `cls` | Extra CSS classes. |
| `attrs` | Raw HTML attributes. |

### Form requirements

Forms inside the slot **must** specify:

- `hx-target="#<id>"` — the wizard_form's `id`
- `hx-swap="outerHTML"` — replace the entire wrapper (stepper + form)

The component applies `hx-disinherit="hx-select hx-target hx-swap"` so forms do not inherit shell-level attributes.

---

## Backend pattern

For fragment-style wizards, each step handler returns the **full** `wizard_form` wrapper for HTMX requests. Chirp's `Page` type negotiates automatically: fragment requests get the block content; full-page requests get the layout.

```python
# Handler returns Page with block that renders full wizard_form
return Page("wizard/step2.html", "wizard", step=2, steps=steps, form=form_data)
```

Template `wizard/step2.html`:

```html
{% block wizard %}
{% from "chirpui/wizard_form.html" import wizard_form %}
{% call wizard_form("checkout", steps=steps, current=step) %}
<form method="post" action="/wizard/step2"
      hx-post="/wizard/step2"
      hx-target="#checkout"
      hx-swap="outerHTML">
  ...fields...
</form>
{% end %}
{% endblock %}
```

### Validation errors

On validation failure, return `ValidationError` with the same block so the form re-renders with errors:

```python
return ValidationError(
    "wizard/step2.html",
    "wizard",
    errors=result.errors,
    form={**data, **form_values},
    step=2,
    steps=steps,
)
```

### OOB (optional)

To swap the stepper and form separately, use Chirp's `OOB` return type with one fragment for the stepper (OOB) and one for the form (primary). This is more complex; the default pattern (return full wrapper) is usually sufficient.

---

## Session state

Store step data server-side with `SessionMiddleware` and `get_session()`. See the [Chirp wizard example](https://github.com/lbliii/chirp/tree/main/examples/wizard) for the full pattern:

- `_get_wizard_data()` / `_set_wizard_data()` / `_clear_wizard_data()`
- Validate each step, merge into session, advance or re-render on error
- Redirect to previous step if required data is missing

---

## Relation to wizard_state

| Component | Pattern | Use when |
|-----------|---------|----------|
| `wizard_form` | Server-driven; each step is a server round-trip | You need validation, persistence, or server-rendered content per step |
| `wizard_state` | Client-side island; show/hide sections by step | All steps are present in the DOM; no server round-trips for navigation |

Use `wizard_form` when the server must validate and persist data between steps. Use `wizard_state` when steps are static and navigation is purely client-side.
