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

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for the rendered tabs family, not descriptor or manifest
metadata.

| Field | Htmx tabs | Client-side tab panels | Route tabs and tabbed page layout |
| --- | --- | --- | --- |
| Surface | `tabs` plus `tab` for in-place htmx tab widgets. | `tabs_container`, `tab_button`, and `tab_panel` for Alpine-controlled panels. | `render_route_tabs`, compatibility alias `route_tabs`, and `tabbed_page_layout` for URL-backed local navigation. |
| Label | `stable` | `stable` | `stable`; `route_tabs` is a compatibility alias, while `render_route_tabs` is preferred authoring. |
| Anatomy | `.chirpui-tabs` root with `role="tablist"`; `.chirpui-tab` links with id `tab-{id}`, active class, `role="tab"`, `aria-selected`, optional `href`, and htmx attributes when a target is provided. | `.chirpui-tabs` root with `x-id`, `x-data="chirpuiTabs()"`, and `data-active`; tab buttons with `data-tab-id`; panels with `.chirpui-tab-panel`, bound ids, `x-show`, `x-cloak`, and `x-transition`. | `<nav class="chirpui-route-tabs">` with route-tab links, active class, `aria-current="page"`, optional icons and badges; layout owns `#page-root`, `#page-content`, optional `#route-tabs`, and `#page-content-inner`. |
| Native semantics | ARIA tab widget semantics: root `role="tablist"` and children `role="tab"` with `aria-selected`. | ARIA tab/panel semantics: buttons use `role="tab"` and panels use `role="tabpanel"` with generated `aria-controls`/`aria-labelledby` relationships. | Navigation semantics: `<nav role="navigation" aria-label="Subsection navigation">` plus links and `aria-current="page"`; route tabs are not ARIA tab widgets. |
| Keyboard | Activation follows anchor/click behavior and HTMX swap handling; no roving-arrow tablist keyboard model is published for htmx tabs. | Activation follows button/click behavior through `selectTab($el)`; no roving-arrow tablist keyboard model is published for Alpine tab panels. | Activation follows native link behavior; keyboard navigation is browser link navigation, not tablist arrow navigation. |
| Focus | Focus remains on the activated tab link/button unless browser or HTMX navigation changes it; shell swap tests verify the surrounding shell remains stable. | Focus remains on the activated tab button; `aria-selected` and panel visibility update through Alpine state. | Focus follows native link/HTMX navigation behavior; stable fragment targets prevent route-tab swaps from replacing the whole shell. |
| Runtime | Requires HTMX when `url` and `hx_target` are provided; emits `hx-boost="false"`, `hx-select="unset"`, `hx-get`, `hx-target`, `hx-swap`, and `hx-push-url="false"`. | Requires `chirpuiTabs()` in `chirpui-alpine.js`, `x-id`, escaped `data-tab-id`, `x-show`, `x-cloak`, `x-transition`, and `chirpui:tab-changed` dispatch from the controller. | Requires route matching through `tab_is_active`; HTMX links emit `hx-boost="false"`, `hx-select="unset"`, `hx-get`, `hx-target`, `hx-push-url="true"`, and `hx-swap="innerHTML"`. |
| Motion | No anatomy-specific animation contract beyond component CSS and transition-token governance. | Panels use `x-transition`; reduced-motion expectations follow component CSS and transition-token governance. | No anatomy-specific animation contract beyond component CSS and transition-token governance. |
| Responsive and overflow | Tab row and target content own local overflow; htmx swaps must stay inside the declared target. | Tab buttons and panels own local wrapping/overflow; hidden panels stay pre-hydration safe with `x-cloak`. | Badges reserve space for loading/expected states; route-tab rows own local overflow and must not replace shell chrome during swaps. |
| Security and escaping | Tab labels, ids, URLs, and HTMX attributes render through normal template escaping and attribute helpers. | Tab ids are read from escaped `data-tab-id`; templates must not interpolate tab ids into Alpine JavaScript string literals. | Tab labels, hrefs, icons, badges, and badge labels render through normal escaping; route matching accepts dict-like and dataclass item shapes. |
| Performance | HTMX work is scoped to the explicit target and does not push browser history for in-place tabs. | Alpine state is local to the tabs root; no page-global observers, scroll listeners, or per-frame work are part of the contract. | Route matching is item-local; htmx swaps target `#page-root` by default and do not require page-global observers. |
| Proof | `tests/test_components.py` checks htmx tab anatomy; `tests/browser/test_tabs.py` checks boosted-shell tab clicks, no-push URL behavior, and shell preservation. | `tests/test_components.py` checks tab-panel anatomy and escaped data-attribute payload safety; `tests/browser/test_tabs.py` checks panel switching, tab-change events, and `aria-selected` updates; `tests/browser/test_alpine_lifecycle.py` checks Alpine tabs after boosted navigation. | `tests/test_route_tabs.py` checks active matching, HTMX attrs, badges, alias behavior, and layout structure; browser shell tests cover route-tab swaps in app chrome contexts. |
| Residual risk | Automated tests cover rendered semantics and HTMX behavior, but no manual screen-reader or assistive-technology proof is claimed. Roving-arrow tablist keyboard behavior is not published. | Automated tests cover rendered semantics and click-driven state changes, but no manual screen-reader or assistive-technology proof is claimed. Roving-arrow tablist keyboard behavior is not published. | Automated tests cover rendered navigation semantics and swap contracts, but no manual screen-reader or assistive-technology proof is claimed. Route tabs must continue to avoid ARIA tab-widget claims. |

## Proof

Executable coverage lives in:

- `tests/test_components.py` for htmx tab anatomy, tab-panel anatomy, and
  tab-panel data-attribute payload safety.
- `tests/test_route_tabs.py` for route-tab active matching, HTMX attrs, badges,
  alias behavior, and `tabbed_page_layout` structure.
- `tests/browser/test_tabs.py` for htmx tab swaps inside a boosted shell,
  no-push URL behavior, client-side panel switching, tab-change events, and
  `aria-selected` updates.
