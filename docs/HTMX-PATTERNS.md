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

### Rapid-click defaults

chirp-ui owns safe transport defaults for the HTML it emits. Apps still own
business semantics: idempotency, permissions, destructive-action policy,
endpoint cost, rate limits, and conflict handling.

| Surface | Default | Override |
|---------|---------|----------|
| App-shell boosted navigation | `shell_outlet_attrs()` emits `hx-sync="<target>:replace"` so the latest navigation intent wins for the shared shell target. | Pass `sync="..."` or `sync=""` to shell helpers when a custom shell needs different queueing. |
| Live search and local filters | `search_field()`, `search_bar()`, and `filter_row()` use `hx-sync="this:replace"` for local fragment GETs, and default to `hx-select="unset"` plus `hx-disinherit="hx-select"` so app-shell selectors do not empty-swap fragments. | Pass `search_sync`, `search_hx_select`, `search_attrs_map`, or explicit `attrs_map` htmx attributes. |
| Mutating forms and action buttons | `form()`, mutating `btn()` / `icon_btn()` htmx requests, confirm dialogs, and shell action forms drop repeated in-flight submissions and disable local submit/action controls when possible. | Pass `hx_sync`, `hx_disabled_elt`, or matching `attrs_map` / `hx={}` values. Use `""` where supported to opt out. |

These defaults reduce accidental duplicate requests and stale swaps. They do
not replace server-side idempotency or authorization checks.

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

**Components:** `form`, local live-search/filter helpers, mutating `btn` /
`icon_btn` requests

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

### `hx-sync` request coordination

**Components:** `app_shell_layout`, `app_shell` shell links, `nav_link`,
`sidebar_link`, `shell_brand_link`, `search_field`, `search_bar`,
`filter_row`, `form`, `btn`, `icon_btn`, `confirm_dialog`, `shell_actions`

**What:** Shell navigation coordinates on the shell target with replacement
semantics. Live search and filter controls replace stale local requests.
Mutating submits and actions drop repeated in-flight submissions.

**Why:** Rapid clicks or typing should not let older responses overwrite newer
UI, and accidental double-submit should not be the default behavior of shipped
Chirp UI helpers.

**Override:** Use the exposed sync parameters (`sync`, `search_sync`,
`hx_sync`) or explicit htmx attrs when app semantics need queueing, aborting, or
repeatable actions.

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
