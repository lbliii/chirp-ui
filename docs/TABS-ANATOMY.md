# Tabs Anatomy

**Status:** shipped contract
**Scope:** `tabs`, `tab`, `tabs_container`, `tab_button`, `tab_panel`,
`render_route_tabs`, `route_tabs`, `tabbed_page_layout`
**Runtime:** htmx and Alpine.js through `chirpui-alpine.js`

Chirp UI has three tab-like surfaces with different semantics:

- `tabs` / `tab`: htmx-capable tab widgets with `tablist` / `tab` roles.
- `tabs_panels`: client-side panel switching with Alpine and `tabpanel`.
- `route_tabs`: URL-backed local navigation links with `role="navigation"` and
  `aria-current="page"`, not ARIA tab widgets.

Use route tabs for URL-backed local views. Use true tab semantics only when the
surface controls in-place panels.

## Htmx Tabs

Import from `chirpui/tabs.html`:

```kida
{% from "chirpui/tabs.html" import tabs, tab %}

{% call tabs(active="overview") %}
  {{ tab("overview", "Overview", url="/tabs/overview", hx_target="#tab-content", active=true) }}
  {{ tab("details", "Details", url="/tabs/details", hx_target="#tab-content") }}
{% end %}
```

`tabs(...)` renders:

- root class: `.chirpui-tabs`
- `role="tablist"`

`tab(...)` renders:

- root class: `.chirpui-tab`
- optional `.chirpui-tab--active`
- id `tab-{id}`
- `role="tab"`
- `aria-selected`
- optional `href`

When `url` and `hx_target` are provided, the tab emits:

- `hx-boost="false"`
- `hx-select="unset"`
- `hx-get`
- `hx-target`
- `hx-swap`
- `hx-push-url="false"`

When `url` is provided without `hx_target`, the template delegates to
`route_link_attrs(url) | html_attrs`.

## Client-Side Tab Panels

Import from `chirpui/tabs_panels.html`:

```kida
{% from "chirpui/tabs_panels.html" import tabs_container, tab_button, tab_panel %}

{% call tabs_container(active="overview") %}
  {{ tab_button("overview", "Overview") }}
  {{ tab_button("details", "Details") }}
  {% call tab_panel("overview") %}Overview content{% end %}
  {% call tab_panel("details") %}Details content{% end %}
{% end %}
```

`tabs_container(...)` renders:

- root class: `.chirpui-tabs`
- `x-id="['tab', 'tabpanel']"`
- `x-data="chirpuiTabs()"`
- `data-active`

`tab_button(...)` renders:

- `<button type="button">`
- `.chirpui-tabs__tab`
- `data-tab-id`
- `role="tab"`
- bound `aria-selected`
- bound `aria-controls`
- bound generated id
- `@click="selectTab($el)"`

`tab_panel(...)` renders:

- `.chirpui-tab-panel`
- `data-tab-id`
- `role="tabpanel"`
- bound generated id
- bound `aria-labelledby`
- `x-show`
- `x-cloak`
- `x-transition`

`chirpuiTabs().selectTab()` reads the selected id from escaped `data-tab-id`,
updates active state, and dispatches:

```javascript
{ tab: "overview" }
```

Templates must not interpolate tab ids into Alpine JavaScript string literals.

## Route Tabs

Import from `chirpui/route_tabs.html`:

```kida
{% from "chirpui/route_tabs.html" import render_route_tabs %}

{{ render_route_tabs(tab_items, current_path, target="#page-root") }}
```

`render_route_tabs(...)` renders:

- `<nav role="navigation" aria-label="Subsection navigation">`
- root class: `.chirpui-route-tabs`
- link class: `.chirpui-route-tab`
- active class: `.chirpui-route-tab--active`
- `aria-current="page"` on the active link
- `hx-boost="false"`
- `hx-select="unset"`
- `hx-get`
- `hx-target`, defaulting to `#page-root`
- `hx-push-url="true"`
- `hx-swap="innerHTML"`

Tab items support:

```python
{"label": "...", "href": "...", "icon": "...", "badge": 2, "badge_label": "...", "match": "prefix"}
```

Badges reserve space when `badge_expected`, `badge_reserved`, or
`badge_loading` is present. Visible badges may receive `aria-label`; reserved
badges are `aria-hidden`.

`route_tabs(...)` remains a compatibility alias for `render_route_tabs(...)`.
Prefer `render_route_tabs(...)` in templates to avoid macro/context name
collisions with variables named `route_tabs`.

## Tabbed Page Layout

`chirpui/tabbed_page_layout.html` provides the route-tab page structure:

- `#page-root`
- `#page-content`
- optional `#route-tabs`
- `#page-content-inner`

Extending the template is preferred for route-backed pages that need stable
fragment targets for boosted shell navigation and route-tab swaps.

## Proof

Executable coverage lives in:

- `tests/test_components.py` for htmx tab anatomy, tab-panel anatomy, and
  tab-panel data-attribute payload safety.
- `tests/test_route_tabs.py` for route-tab active matching, HTMX attrs, badges,
  alias behavior, and `tabbed_page_layout` structure.
- `tests/browser/test_tabs.py` for htmx tab swaps inside a boosted shell,
  no-push URL behavior, client-side panel switching, tab-change events, and
  `aria-selected` updates.
