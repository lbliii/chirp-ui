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

The main column (`.chirpui-app-shell__main`) uses **`min-width: 0`** and **`overflow-x: clip`**. If the page scrolls sideways, something inside the content is wider than the column — usually a **non-wrapping flex row**, a **custom grid without `min-width: 0` on children**, or **wide tables** without an `overflow-x: auto` wrapper.

**Fix:**

- **`grid()`** applies **`min-width: 0`** to direct children in CSS automatically.
- Use **`block()`** when you need **`span=`** for bento cells.
- Use **`cluster()`** and default-wrapping **`indicator_row()`** for wrapping content.
- Flex rows (headers, toolbars) with shrinking text columns need **`min-width: 0`** — page/section/entity headers do this in CSS; for custom markup use the **`chirpui-min-w-0`** utility class.
- For custom grids, use **`minmax(0, 1fr)`** tracks and **`min-width: 0`** on items.

See [Layout overflow](./layout-overflow.md) for the full checklist.

## Fragment islands

### `hx-target` must match island ID

When using `fragment_island` or `safe_region`, the target element's `id` must match the `hx-target` passed to HTMX requests. If the target doesn't exist when the swap fires, the response may be discarded or swapped into the wrong place.

```html
{% from "chirpui/fragment_island.html" import fragment_island %}
{{ fragment_island("my-target", content=...) }}
<!-- HTMX must use hx-target="#my-target" -->
```

When forms load via HTMX, **targets must live in the same subtree** as the form.

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

### Use `Alpine.safeData()` instead of `Alpine.data()` for named components

`Alpine.data()` must be called during `alpine:init`, which only fires once on initial page load. Under htmx boosted navigation, swapped-in scripts that use `alpine:init` will not re-register their components — causing "X is not defined" errors.

```html
<!-- BAD: breaks on htmx navigation -->
<script>
document.addEventListener('alpine:init', () => {
  Alpine.data('counter', () => ({ count: 0 }));
});
</script>

<!-- GOOD: works on initial load AND htmx swaps -->
<script>
Alpine.safeData('counter', () => ({ count: 0 }));
</script>
```

### Do not load Alpine.js yourself

Chirp is the single authority for Alpine injection. `use_chirp_ui(app)` auto-enables `alpine=True`, which injects Alpine core, all plugins (Mask, Intersect, Focus), store init, and the `safeData` helper. Adding your own `<script src="alpinejs">` tag will double-load Alpine and cause unpredictable behavior.

## Registration

Call **`use_chirp_ui(app)`** or **`register_filters(app)`** before rendering templates. If you render templates before registration, filters like `bem`, `html_attrs`, `validate_variant` will be missing and templates will fail.

```python
from chirp import App, use_chirp_ui
import chirp_ui

app = App(...)
use_chirp_ui(app, prefix="/static")  # Before any render
```

## CSRF

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

## Prefer `attrs_map` over `attrs`

Raw `attrs` strings are passed through unescaped. Use `attrs_map` (a dict) for structured attributes — it is escaped by the `html_attrs` filter, reducing XSS risk. See [Security](./security.md).

## Related

- [Security](./security.md)
