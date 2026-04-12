# chirp-ui Anti-Footgun Guide

Common pitfalls and how to avoid them.

---

## Layout and horizontal scroll

The main column (`.chirpui-app-shell__main`) uses **`min-width: 0`** and **`overflow-x: clip`**. If the page scrolls sideways, something inside the content is wider than the column—usually a **non-wrapping flex row**, a **custom grid without `min-width: 0` on children**, or **wide tables** without an `overflow-x: auto` wrapper.

**Fix:** Flow **`grid()`** applies **`min-width: 0`** to direct children in CSS; use **`block()`** when you need **`span=`**. Prefer **`cluster()`** and default-wrapping **`indicator_row()`**. Flex **rows** (headers, toolbars): shrinking text columns need **`min-width: 0`** — page/section/entity headers do this in CSS; for custom markup use **`chirpui-min-w-0`**. For custom grids, use **`minmax(0, 1fr)`** tracks and **`min-width: 0`** on items. Full checklist: [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md).

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

chirp-ui's shared behavior runtime follows this rule already. If you need a new
named controller, add it to `chirpui-alpine.js` instead of introducing another
inline component-local registration script.

### Do not load Alpine.js yourself — Chirp is the single authority

`use_chirp_ui(app)` auto-enables `alpine=True`, which injects Alpine core, all plugins (Mask, Intersect, Focus), store init, and the `safeData` helper. Adding your own `<script src="alpinejs">` tag will double-load Alpine and cause unpredictable behavior.

### Keep medium-complex behavior out of inline `x-data`

Inline `x-data` is fine for tiny one-state widgets. It should not hold behavior
that depends on `$refs`, `$nextTick`, keyboard handling, `localStorage`,
viewport measurement, dialog targeting, or repeated logic across templates. Use
the shared controllers in `chirpui-alpine.js` for those cases.

---

## chirp-ui Registration

### `use_chirp_ui` (or `register_filters`) must be called before template rendering

When using Chirp, call `use_chirp_ui(app)` after app creation. If you render templates before registration, filters like `bem`, `html_attrs`, `validate_variant` and globals like `build_hx_attrs` will be missing and templates will fail.

```python
from chirp import App, use_chirp_ui
import chirp_ui

app = App(...)
use_chirp_ui(app, prefix="/static")  # Before any render
```

### Prefer plain `href=` on supported link components

When `use_chirp_ui(app)` is active, selected link-bearing components auto-apply
Chirp's route-aware swap attrs for internal links. That includes `btn()`,
`site_header()` brand links, `site_nav_link()`, `footer_link()`, `app_shell()`
brand links, and `shell_brand_link()`.

Use plain `href=` first:

```kida
{{ btn("Open showcase", href="/showcase") }}
{{ site_nav_link("/docs", "Docs") }}
{{ footer_link("/contact", "Contact") }}
```

Do not manually thread `swap_attrs()` into those components unless you need a
special override. External links and explicit `hx-*` args still win.

---

## Static Path Setup

### CSS and JS must be served from the correct path

Include `chirpui.css`, `chirpui.js`, and `chirpui-alpine.js` from
`chirp_ui.static_path()`. With Chirp's `use_chirp_ui`, the prefix is configured
automatically and the Alpine runtime is injected for full pages. For standalone
setups, ensure your static file server serves the chirp-ui templates directory
and load `chirpui-alpine.js` before the Alpine core script.

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

---

## Kida Macros

### Macro and context variable must not share the same name

When a macro and a context variable have the same name (e.g. both `route_tabs`), the macro shadows the variable. On pages where the variable is not in context, `{% if route_tabs | default([]) %}` resolves to the macro (truthy), so the block runs and passes the macro as the first argument. Inside the macro, `{% for tab in tabs %}` then tries to iterate over the macro → "MacroWrapper object is not iterable".

**Fix:** Use verb-prefixed names for macros and noun-like names for context variables:

```kida
{% from "_route_tabs.html" import render_route_tabs %}
{% if route_tabs | default([]) %}
    {{ render_route_tabs(route_tabs, current_path) }}
{% end %}
```

| Macros | Context variables |
|--------|-------------------|
| `render_route_tabs`, `format_date`, `render_nav` | `route_tabs`, `items`, `skills` |
