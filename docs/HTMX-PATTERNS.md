# HTMX Patterns in chirp-ui

How chirp-ui components integrate with htmx. Covers the `hx={}` dict pattern,
auto-injected attributes, and when to use what.

---

## The `hx={}` dict pattern

Components that accept htmx attributes (`btn`, `icon_btn`, `form`) support two
APIs for passing them:

### Dict (preferred)

```html
{{ btn("Save", hx={"post": "/save", "target": "#result", "swap": "innerHTML"}) }}
```

Keys are short htmx names without the `hx-` prefix. `build_hx_attrs()` converts
them to proper `hx-*` attributes and drops `None` values.

### Individual kwargs (override)

```html
{{ btn("Save", hx_post="/save", hx_target="#result") }}
```

Individual kwargs override keys from the `hx` dict when both are provided:

```html
{# hx_target wins over dict's "target" #}
{{ btn("Save", hx={"post": "/save", "target": "#list"}, hx_target="#detail") }}
```

### When to use which

| Scenario | Recommended |
|----------|-------------|
| Static htmx config (most cases) | `hx={}` dict |
| Dynamic override of one key | `hx={}` dict + individual kwarg |
| Passing htmx config from Python context | `hx=config_dict` |

---

## Auto-injected attributes

chirp-ui components automatically inject certain htmx attributes to prevent
common integration bugs. These are **not** visible in the macro signature but
are added at render time.

### `hx-boost="false"` on links with htmx requests

**Components:** `btn`, `tabs`, `route_tabs`

**What:** When an `<a>` element has an explicit htmx request attribute
(`hx-get`, `hx-post`, etc.), `hx-boost="false"` is added automatically.

**Why:** Without this, `hx-boost` (inherited from the app shell or a parent
element) intercepts the click before the explicit htmx request fires. The boost
navigation replaces the page content, and the intended htmx swap never happens.
This is one of the most common htmx integration bugs — the component "works in
isolation but breaks inside the app shell."

### `hx-select="unset"` on forms with htmx

**Components:** `form`

**What:** When a form has an htmx mutating method (`hx-post`, `hx-put`,
`hx-patch`, `hx-delete`), `hx-select="unset"` and
`hx-disinherit="hx-select"` are added automatically.

**Why:** App shells typically set `hx-select="#page-content"` on the boost
container to extract only the page content from full-page responses. Without
`hx-select="unset"`, this selector is inherited by forms inside the shell,
causing htmx to try to extract `#page-content` from a fragment response that
doesn't contain it — resulting in an empty swap.

`hx-disinherit="hx-select"` prevents the form's `hx-select="unset"` from
leaking into child elements that might have their own htmx requests.

**Override:** Pass `hx_select="..."` explicitly to set a custom value. The
auto-injection only fires when `hx_select` is not provided.

### `hx-on::after-request` form reset

**Components:** `form`

**What:** Forms with htmx mutating methods automatically reset after a
successful response (2xx status).

**Why:** After a successful POST/PUT/PATCH, the form fields should clear so the
user doesn't accidentally resubmit. This matches native browser behavior for
non-AJAX form submissions.

**Override:** Pass `hx_reset_on_success=false` to disable.

### `hx-disinherit` on fragment islands

**Components:** `safe_region`, `fragment_island`, `wizard_form`

**What:** These components add `hx-disinherit="hx-select hx-target hx-swap"` to
isolate their htmx context from inherited shell attributes.

**Why:** Fragment islands are mutation regions inside boosted layouts. Without
disinherit, they inherit the shell's `hx-target`, `hx-swap`, and `hx-select`,
which causes local updates to replace the wrong element or extract the wrong
selector from the response.

---

## `build_hx_attrs()` — the merge function

All htmx attribute handling goes through `build_hx_attrs()`, registered as a
template global. It:

1. Merges `hx={}` dict with individual `hx_*` kwargs (kwargs win)
2. Converts underscore names to hyphen names (`hx_post` → `hx-post`)
3. Drops `None` values
4. Validates against 33 known htmx attributes (warns on unknown keys)
5. Returns a dict ready for `| html_attrs`

Direct usage in custom templates:

```html
<div {{ build_hx_attrs(hx_get="/api/data", hx_target="#results") | html_attrs }}>
```

Or with the dict pattern:

```html
{% set config = {"get": url, "target": "#results", "swap": "innerHTML"} %}
<div {{ build_hx_attrs(hx=config) | html_attrs }}>
```

---

## See also

- [DND-FRAGMENT-ISLAND.md](DND-FRAGMENT-ISLAND.md) — Fragment island patterns for drag-and-drop regions
- [HTMX-ADVANCEMENT.md](HTMX-ADVANCEMENT.md) — Design decisions for htmx integration
- [ANTI-FOOTGUNS.md](ANTI-FOOTGUNS.md) — Common htmx pitfalls and how chirp-ui prevents them
