# Shell, sections, and route tabs — contract checklist

Use this when building a Chirp app with chirp-ui’s app shell and subsection navigation.

## Layers

| Layer | Responsibility |
|-------|------------------|
| **App shell** | `app_shell` / layout: sidebar, topbar, `#main`. Persists across boosted navigation. |
| **Page content** | `#page-content` — selected via `hx-select` on boosted requests. |
| **Page chrome** | Inside `#page-content`: route tabs, page header, toolbars. |

Stable fragment targets (`#page-root`, `#page-content-inner`) are documented in [UI-LAYERS.md](../fundamentals/ui-layers.md).

## Delivery modes (quick reference)

| Delivery | Template usage | Swap target | Layout chain | OOB |
|----------|----------------|-------------|--------------|-----|
| Full page (browser nav) | All layouts nested | `body` (full doc) | Root to deepest | N/A |
| Boosted nav (`hx-boost`) | Layouts from `hx-select` target down | `#page-content` | Mid-chain | Sidebar, title, breadcrumbs |
| Route tab click | Page chrome + content | `#page-root` | Innermost only | Title, breadcrumbs |
| Fragment endpoint | Named block only | Caller's `hx-target` | None | Per response |
| SSE / EventStream | Fragment yields | Caller's `hx-target` | None | Per event |

## Chirp: sections and metadata

1. **`register_section(Section(...))`** before `mount_pages()` — define `id`, `label`, `tab_items`, `breadcrumb_prefix`, `active_prefixes`.
2. **`TabItem`** fields: `label`, `href`, optional `icon`, `badge`, `match` (`"exact"` default or `"prefix"` for nested URLs). Same information flows to templates as `tab_items` / `route_tabs` dicts.
3. **Each page** `_meta.py`: set `section="<id>"` so shell context resolves tabs and breadcrumbs for that route family.
4. **`app.check()`** — run in CI; it warns on unknown `meta.section`, missing tab routes, duplicate tab hrefs in a section, section coverage (`active_prefixes` vs `meta.section`), and other hypermedia contracts.

## chirp-ui: route tabs

1. **`render_route_tabs`** / **`tab_is_active`** — register via `use_chirp_ui(app)`; tabs are `role="navigation"` links, not ARIA `tablist`.
2. **Tab dict shape**: `{ label, href, icon?, badge?, match? }`. Prefix matching follows `tab_is_active` in `chirp_ui/route_tabs.py`.
3. **Targets** — default `hx-target="#page-root"` so subsection navigation swaps page chrome + inner content without reloading the app shell.
4. **Boost** — route tab links use `hx-boost="false"` so they do not inherit the shell’s boosted `hx-select`; see component source.
5. **Scope** — route tabs are for local views of one object, workspace, or subsection. Broad cross-feature navigation belongs in `primary_nav`, `sidebar`, `nav_tree`, or an app-level section tree.

## OOB handoffs

When a response must update sidebar, breadcrumbs, document title, or the tab strip without a full page load, use **`register_oob_region`** (or Chirp’s shell OOB helpers) with stable `target_id`s aligned to your layout. Fragment responses that change the current section should include matching OOB swaps so chrome stays consistent.

## Consumer app chrome recipe

Use this shape for filesystem-style app pages before proposing a new chrome
macro:

```html
{% extends "chirpui/app_shell_layout.html" %}
{% block sidebar %}
  {% from "chirpui/sidebar.html" import sidebar, sidebar_link, sidebar_section %}
  {% call sidebar(current_path=current_path) %}
    {% call sidebar_section("Workspace") %}
      {{ sidebar_link("/workspace", "Overview", match="prefix") }}
      {{ sidebar_link("/admin", "Admin", match="prefix") }}
    {% end %}
  {% end %}
{% end %}
{% block content %}
  {% from "chirpui/route_tabs.html" import route_tabs %}
  {% from "chirpui/breadcrumbs.html" import breadcrumbs %}
  {% from "chirpui/command_bar.html" import command_bar %}
  {% from "chirpui/button.html" import btn %}
  {% from "chirpui/shell_actions.html" import shell_actions_bar %}

  {% if include_shell_actions_oob %}
  <div id="chirp-shell-actions" hx-swap-oob="innerHTML">
    {{ shell_actions_bar(shell_actions) }}
  </div>
  {% end %}

  <div id="page-root">
    {{ route_tabs(tab_items, current_path) }}
    {{ breadcrumbs(breadcrumb_items) }}
    {% call command_bar(aria_label="Workspace tools") %}
      {{ btn("Filter", hx_get="/workspace/filter", hx_target="#page-content-inner",
        hx_swap="innerHTML", attrs_map={"hx-disinherit": "hx-select"}) }}
    {% end %}
    <div id="page-content-inner">
      {% block page_inner %}{% end %}
    </div>
  </div>
{% end %}
```

Server routes should branch on `HX-Target`, not only `HX-Request`:

| Request target | Response shape |
|---|---|
| `main` | full page response containing `#page-content` plus any OOB shell regions that changed |
| `page-root` | page chrome fragment for route-tab swaps |
| `page-content-inner` or local target | local fragment only, with inherited shell selectors cleared |

### Server response patterns

Use small route-local helpers when a page family needs all three response
shapes:

```python
def hx_target(request: Request, target: str) -> bool:
    headers = getattr(request, "headers", {})
    return bool(headers.get("HX-Request")) and headers.get("HX-Target") == target


def include_shell_actions_oob(request: Request) -> bool:
    return hx_target(request, "main")
```

Full shell response for normal navigation and boosted shell navigation:

```python
@app.route("/workspace")
async def workspace_page(request: Request):
    if hx_target(request, "page-root"):
        return Response(workspace_page_root_fragment("/workspace"))

    return Template(
        "workspace_page.html",
        current_path="/workspace",
        shell_actions=workspace_shell_actions(),
        include_shell_actions_oob=include_shell_actions_oob(request),
    )
```

The template owns the OOB shell region only when the route handler asks for it:

```html
{% from "chirpui/shell_actions.html" import shell_actions_bar %}

{% if include_shell_actions_oob %}
<div id="chirp-shell-actions" hx-swap-oob="innerHTML">
  {{ shell_actions_bar(shell_actions) }}
</div>
{% end %}
```

Page-root fragments should contain page chrome and content for the route-tab
target, but not the persistent shell:

```python
def workspace_page_root_fragment(path: str) -> str:
    return f"""
<div id="route-tabs">...</div>
<header>...</header>
<div id="page-content-inner">...</div>
"""
```

Local fragments should stay local and clear shell selector inheritance from the
trigger:

```html
{{ btn("Filter",
    hx_get="/workspace/filter-fragment",
    hx_target="#page-content-inner",
    hx_swap="innerHTML",
    attrs_map={"hx-disinherit": "hx-select"}) }}
```

## Filesystem Mounted App Recipe

For filesystem-routed Chirp apps, prefer letting `mount_pages()` and the
registered Chirp UI page-shell contract choose response shape. The copyable
test fixture is:

```text
tests/fixtures/filesystem_chrome/
  app.py
  pages/
    _layout.html
    workspace/
      _context.py
      _meta.py
      page.py
      page.html
      runs.py
      runs.html
      filter_fragment.py
    admin/
      _context.py
      _meta.py
      page.py
      page.html
      audit.py
      audit.html
```

App setup registers sections, enables Chirp UI, then mounts pages:

```python
from chirp import App, AppConfig
from chirp.ext.chirp_ui import use_chirp_ui
from chirp.pages import Section, TabItem

app = App(AppConfig(template_dir="pages"))
use_chirp_ui(app)
app.register_section(
    Section(
        id="workspace",
        label="Workspace",
        tab_items=(
            TabItem("Overview", "/workspace", match="exact"),
            TabItem("Runs", "/workspace/runs", match="exact"),
        ),
        breadcrumb_prefix=({"label": "App", "href": "/workspace"},),
        active_prefixes=("/workspace",),
    )
)
app.mount_pages("pages")
```

The root `_layout.html` owns the app shell and sidebar:

```html
{# preset: chirpui-app-shell #}
{# target: body #}
{# domain: workspace #}
{# shell: workspace #}
{% extends "chirpui/app_shell_layout.html" %}
{% block brand %}Workspace{% end %}
{% block sidebar %}
{% from "chirpui/sidebar.html" import sidebar, sidebar_link, sidebar_section %}
{% call sidebar(current_path=current_path) %}
  {% call sidebar_section("App") %}
    {{ sidebar_link("/workspace", "Workspace", match="prefix") }}
    {{ sidebar_link("/admin", "Admin", match="prefix") }}
  {% end %}
{% end %}
{% end %}
```

Each route family contributes route-scoped shell actions through `_context.py`:

```python
from chirp import ShellAction, ShellActions, ShellActionZone


def context():
    return {
        "shell_actions": ShellActions(
            primary=ShellActionZone(
                items=(ShellAction(id="new-run", label="New run", href="/workspace/new"),)
            )
        )
    }
```

`_meta.py` connects the route family to the registered section:

```python
from chirp.pages import RouteMeta

META = RouteMeta(
    title="Workspace",
    section="workspace",
    breadcrumb_label="Workspace",
)
```

Page handlers can return context dictionaries when a sibling template exists:

```python
def get():
    return {
        "page_title": "Workspace",
        "view_title": "Workspace overview",
    }
```

The page template provides the three contract blocks directly:

```html
{% block page_root %}
<div id="page-root">
{% block page_root_inner %}
  <div id="route-tabs">
    {{ render_route_tabs(tab_items, current_path, target="#page-root") }}
  </div>
  <header>...</header>
  <div id="page-content-inner">
  {% block page_content %}
    ...
  {% end %}
  </div>
{% end %}
</div>
{% end %}
```

With that structure:

| Request | Chirp UI contract result |
|---|---|
| full navigation | full shell with one `#main`, one `#page-content`, and one `#page-root` |
| boosted sidebar navigation to `#main` | full page response with `#page-content` plus shell action OOB updates |
| route-tab navigation to `#page-root` | `page_root_inner` fragment plus shell action OOB updates when route metadata changes |
| local tool target `#page-content-inner` | `page_content` or endpoint-local fragment without shell wrappers |

Proof:

- `tests/test_filesystem_chrome_response_targets.py`
- `tests/browser/test_filesystem_chrome_app.py`

The first consumer-adoption proof lives in
`tests/browser/test_consumer_workspace_chrome.py`,
`tests/browser/test_consumer_admin_chrome.py`, and
`tests/browser/test_consumer_chrome_htmx_boundaries.py`.

## Reliability tips

- Keep **one source of truth** for tab definitions: `Section.tab_items` (`TabItem`), not a parallel app-only model.
- After adding routes, run **`app.check()`** and fix section / tab href warnings.
- Prefer **prefix** `match` when a tab represents a URL subtree (e.g. `/settings` for `/settings/wizard`).
