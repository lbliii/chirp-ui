# chirp-ui Anti-Footgun Guide

Common pitfalls and how to avoid them.

---

## Fragment Island and HTMX

### `hx-target` must match island ID

When using `fragment_island` or `safe_region`, the target element's `id` must match the `hx-target` passed to HTMX requests. If the target doesn't exist when the swap fires, the response may be discarded or swapped into the wrong place.

```html
{% from "chirpui/fragment_island.html" import fragment_island %}
{{ fragment_island("my-target", content=...) }}
<!-- HTMX must use hx-target="#my-target" -->
```

See [DND-FRAGMENT-ISLAND.md](DND-FRAGMENT-ISLAND.md) for cookbook examples.

---

## Alpine.js

### `x-data` must be on or above the element using `x-show`/`x-bind`

Alpine directives like `x-show`, `x-bind`, `@click` resolve state from the nearest `x-data` ancestor. If `x-data` is missing or placed inside the element that uses `x-show`, the directive won't work.

```html
<!-- Correct: x-data wraps the toggle target -->
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Content</div>
</div>
```

---

## chirp-ui Registration

### `use_chirp_ui` (or `register_filters`) must be called before template rendering

When using Chirp, call `use_chirp_ui(app)` after app creation. If you render templates before registration, filters like `bem`, `html_attrs`, `validate_variant` will be missing and templates will fail.

```python
from chirp import App, use_chirp_ui
import chirp_ui

app = App(...)
use_chirp_ui(app, prefix="/static")  # Before any render
```

---

## Static Path Setup

### CSS and JS must be served from the correct path

Include `chirpui.css` and `chirpui.js` from `chirp_ui.static_path()`. With Chirp's `use_chirp_ui`, the prefix is configured automatically. For standalone setups, ensure your static file server serves the chirp-ui templates directory.

```python
from chirp.middleware.static import StaticFiles
import chirp_ui

app.add_middleware(StaticFiles(
    directory=str(chirp_ui.static_path()),
    prefix="/static"
))
```

---

## CSRF and Forms

### When to use `csrf_hidden` and what breaks without it

For forms that submit via `hx-post`/`hx-put`/`hx-patch`/`hx-delete`, include the CSRF token when your backend requires it. Use `{% slot form_content %}` in `confirm_dialog` for hidden fields:

```html
{% call confirm_dialog(..., confirm_url="/delete") %}
{% slot form_content %}
<input type="hidden" name="csrf_token" value="{{ csrf_token }}">
<input type="hidden" name="id" value="123">
{% end %}
{% end %}
```

Without the token, the server may reject the request with 403.

---

## Prefer `attrs_map` over `attrs`

Raw `attrs` strings are passed through unescaped. Use `attrs_map` (a dict) for structured attributes; it is escaped by the `html_attrs` filter, reducing XSS risk. See [SECURITY.md](../SECURITY.md).
