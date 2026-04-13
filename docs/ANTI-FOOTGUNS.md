# chirp-ui Anti-Footgun Guide

Common pitfalls and how to avoid them.

---

## Layout and horizontal scroll

The main column (`.chirpui-app-shell__main`) uses **`min-width: 0`** and **`overflow-x: clip`**. If the page scrolls sideways, something inside the content is wider than the column—usually a **non-wrapping flex row**, a **custom grid without `min-width: 0` on children**, or **wide tables** without an `overflow-x: auto` wrapper.

**Fix:** Flow **`grid()`** applies **`min-width: 0`** to direct children in CSS; use **`block()`** when you need **`span=`**. Prefer **`cluster()`** and default-wrapping **`indicator_row()`**. Flex **rows** (headers, toolbars): shrinking text columns need **`min-width: 0`** — page/section/entity headers do this in CSS; for custom markup use **`chirpui-min-w-0`**. For custom grids, use **`minmax(0, 1fr)`** tracks and **`min-width: 0`** on items. Full checklist: [LAYOUT-OVERFLOW.md](LAYOUT-OVERFLOW.md).

---

## App shell scroll model

Default app shells scroll with the **document**, not with `#main`. If you reintroduce `height: 100dvh` plus `overflow-y: auto` on `.chirpui-app-shell__main`, you break sticky-topbar expectations, anchor landings, and browser history restoration.

**Fix:** Keep default routes in document-scroll mode. Only opt into **`chirpui-app-shell__main--fill`** when the route intentionally needs bounded inner scroll (chat, map, IDE-style layouts). Pair that with a direct `#page-content > .chirpui-page-fill` root so the shell can re-sync fill mode after boosted navigation. See [LAYOUT-VERTICAL.md](LAYOUT-VERTICAL.md).

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
`shimmer_button()`, `pulsing_button()`, `site_header()` brand links,
`site_nav_link()`, `footer_link()`, `app_shell()` brand links,
`shell_brand_link()`, `navbar()` brand links, `navbar_link()`,
`breadcrumbs()`, `pagination()`, `nav_tree()`, `dock()`, `timeline()`,
`timeline_item()`, `logo()`, `badge()`, `card_link()`, `card_main_link()`,
`resource_card()`, `icon_btn()`, `index_card()`, `metric_card()`,
`split_button()` primary links, `dropdown_menu()` item links,
`dropdown_split()` primary/item links, `action_bar_item()`,
`list_group(linked=true)`, `video_card()` main link, `channel_card()`,
`profile_header()` name links, `profile_header_info()`, `post_card()`,
`post_card_header()`, `video_thumbnail()`, `mention()`, `trending_tag()`,
`conversation_item()`, `playlist_item()`, `comment()` author/replies links,
`filter_chip()`, `link()`, `calendar()` nav links, `bar_chart()` label links,
`tab()`, `ascii_tab()`, `empty_state()` action links, and
`tag_browse` badge/clear links.

Use plain `href=` first:

```kida
{{ btn("Open showcase", href="/showcase") }}
{{ site_nav_link("/docs", "Docs") }}
{{ footer_link("/contact", "Contact") }}
```

Do not manually thread `swap_attrs()` into those components unless you need a
special override. External links and explicit `hx-*` args still win. This only
applies to links owned by the component itself, not arbitrary raw `<a>` tags
you pass through a slot. For example, `split_button()` upgrades its
`primary_href`, but not arbitrary menu links you slot into the dropdown body,
and `navbar_dropdown()` still leaves its slotted menu links alone. Simpler
wrappers like `logo()`, `badge()`, `breadcrumbs()`, `dock()`, `nav_tree()`,
`list_group(linked=true)`, `video_thumbnail()`, `mention()`,
`trending_tag()`, `index_card()`, `pulsing_button()`, and the link-card macros
do not expose `hx_*` / `attrs_map` overrides on their outer anchor; when you
need custom HTMX on that element, use raw link markup or a component like
`btn()`, `icon_btn()`, `shimmer_button()`, `metric_card()`, or `pagination()`
that exposes those knobs. Explicit HTMX helpers like `nav_link()`,
`route_tabs()`, and `inline_edit_field_form()` keep their existing manual
contract, and timestamp/fragment-style links like `chapter_item()` stay plain
anchors on purpose.

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

## `attrs_unsafe` vs `attrs_map` — choosing the right escape hatch

All chirp-ui macros that accept custom HTML attributes expose two parameters:

| Parameter | Escaping | Use when |
|-----------|----------|----------|
| `attrs_map={"data-x": val}` | **Safe** — dict values are HTML-escaped by `html_attrs` | Any user-controlled or dynamic data |
| `attrs_unsafe='data-x="static"'` | **Unsafe** — raw string passed through `\| safe` | Static strings, framework-generated markup only |

**Rule:** Default to `attrs_map`. Only use `attrs_unsafe` when you need to inject pre-built attribute strings that are not user-controlled.

```html
{# SAFE — values are escaped #}
{{ btn("Save", attrs_map={"data-id": item.id, "data-name": item.name}) }}

{# UNSAFE — raw string, only for static known-safe content #}
{{ btn("Save", attrs_unsafe='data-turbo-frame="modal"') }}
```

**Deprecated:** The old `attrs=""` parameter still works but emits `ChirpUIDeprecationWarning`. Migrate to `attrs_unsafe` (same behavior, explicit about the escaping bypass) or `attrs_map` (safe). See [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Scripting_Prevention_Cheat_Sheet.html).

---

## HTMX integration footguns

chirp-ui auto-injects several htmx attributes to prevent common bugs. If you're debugging unexpected htmx behavior, check [HTMX-PATTERNS.md](HTMX-PATTERNS.md) for the full list. Key auto-behaviors:

- **`hx-boost="false"`** on `<a>` elements with explicit htmx requests (prevents boost from hijacking the click)
- **`hx-select="unset"`** on forms with htmx (prevents inherited `hx-select` from breaking fragment swaps)
- **`hx-disinherit`** on fragment islands (isolates local htmx context from shell attributes)

Use `hx={"post": "/url", "target": "#id"}` instead of individual `hx_post`/`hx_target` kwargs.

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

Macros: `render_route_tabs`, `format_date`, `render_nav`

Context variables: `route_tabs`, `items`, `skills`

---

## Resolved footguns (no longer applicable)

The following issues were fixed in sharp-edges phases 1–3. **Do not re-triage these.** They are listed here so audits can skip them.

| Former footgun | Resolution | Phase/Sprint |
|---------------|------------|-------------|
| `validate_variant` silently returns first allowed value | Emits `ChirpUIValidationWarning`; strict mode raises `ValueError` | 1/1 |
| `register_colors` accepts invalid colors, fails at render | Validates color strings at registration time | 1/1 |
| `btn()` defaults to `type="submit"` (form submission footgun) | Changed to `type="button"` | 3/9 |
| `inline_edit_field` hardcoded fallback ID causes collisions | Warns when `swap_id` not provided | 3/9 |
| `build_hx_attrs()` silently accepts typos like `hx={"typo": ...}` | Validates against 33 known htmx attrs; warns on unknown keys | 3/10 |
| `field_errors()` silently drops non-list values (DRF/Pydantic dicts) | Warns and coerces to `[str(val)]` | 3/10 |
| Pagination uses `<span aria-disabled>` (not keyboard-focusable) | Changed to `<button disabled>` | 3/11 |
| Avatar has no `role="presentation"` for decorative use | `decorative=true` parameter added | 3/11 |
| Alpine `register()` overwrites on double-load/htmx swap | Idempotency guard — first registration wins | 3/12 |
| `safeSetItem()` silently swallows localStorage failures | `console.warn` on catch | 3/12 |
| Provide/consume contracts invisible to template readers | `@provides`/`@consumes` annotations on all 43 statements | 3/13 |
| `tab_is_active()` with empty `href=""` matches all paths | Returns `False` for empty href | 1/8 |
| `contrast_text()` returns "white" on invalid color with no warning | Emits warning | 2/6 |
| `data-theme="system"` has no matching CSS rule | CSS rule added | 1/3 |
| `localStorage` throws in Safari private browsing (chirpui.js) | try/catch added | 1/3 |
| z-index values scattered (1–10000) across 40+ rules | Token system `--chirpui-z-*` | 2/7 |
| CSS hardcoded `color: white` breaks dark mode (20+ sites) | Replaced with `--chirpui-on-*` tokens | 1/3 |
| `--chirpui-spacing-2xs` used but never defined | Defined in `:root` | 1/3 |
| Breakpoints mix `767px`/`768px`/`48rem` | Normalized to `rem` | 1/3 |
| Test stubs (`conftest.py`) diverge from real filter logic | Stubs updated to match production filters | 1/4 |
| 106/195 templates undocumented in COMPONENT-OPTIONS.md | All documented | 1/5 |

For the full history, see [PLAN-sharp-edges.md](PLAN-sharp-edges.md) (phases 1–2) and [PLAN-sharp-edges-phase3.md](PLAN-sharp-edges-phase3.md).
