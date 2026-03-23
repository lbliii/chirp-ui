---
title: App Shell
description: Sidebar, breadcrumbs, command palette, and layout patterns
draft: false
weight: 40
lang: en
type: doc
keywords: [chirp-ui, app shell, sidebar, breadcrumbs, layout]
category: app-shell
---

# App Shell

**Vocabulary:** [UI layers & terms](./ui-layers/) — app shell, page chrome, surface chrome, shell regions, and the built-in HTMX shell-coherence behavior.

**Quick start:** Extend `chirpui/app_shell_layout.html` and fill the blocks. No manual HTML boilerplate.

```html
{% extends "chirpui/app_shell_layout.html" %}
{% block brand %}My App{% end %}
{% block sidebar %}
  {% from "chirpui/sidebar.html" import sidebar, sidebar_link, sidebar_section %}
  {% call sidebar() %}
    {% call sidebar_section("Main") %}
      {{ sidebar_link("/", "Home", match="exact") }}
      {{ sidebar_link("/items", "Items", match="prefix") }}
    {% end %}
  {% end %}
{% end %}
```

`match="exact"` highlights the link only when the URL matches exactly. `match="prefix"` highlights when the URL starts with the href (e.g. `/items/42` highlights the Items link). Chirp auto-injects `current_path` into template context, so `match=` works without manual `nav=` strings. After htmx navigation, a built-in client-side script keeps active states in sync.

## Layout overflow

The shell main area clips horizontal overflow and scrolls vertically. Build pages with **`grid()` + `block()`**, **`cluster()`**, and wrapping indicator rows so content stays in column; use **`overflow-x: auto`** only on inner wrappers for wide tables or code. See the repo doc **`docs/LAYOUT-OVERFLOW.md`** for the full checklist.

## Full-height main

For chat, maps, or IDE-style surfaces that should **fill the viewport** below the topbar (with scroll **inside** panels), opt in with **`{% block main_shell_class %} chirpui-app-shell__main--fill{% end %}`**, put a direct child of **`#page-content`** with class **`chirpui-page-fill`**, and use **`chat_layout(..., fill=true)`** for chat pages. See **`docs/LAYOUT-VERTICAL.md`** for the flex chain, **`min-height: 0`**, and the **`chirpui-chat-layout__messages-body`** wrapper class for SSE/HTMX roots inside the messages column.

## Components

- **sidebar** — Collapsible navigation with sections
- **breadcrumbs** — Path navigation
- **command_palette** — Cmd+K search
- **toast_container** — Toast notifications
- **shell_actions** — Route-scoped topbar actions that update automatically on navigation

## Golden Path

The recommended app path is now:

1. Call `use_chirp_ui(app)` so Chirp registers the canonical shell contract.
2. Keep one section descriptor source in Python for sidebar groups, tab families, and breadcrumb prefixes.
3. Extend `chirpui/tabbed_page_layout.html` for route-backed pages and pass `tab_items` plus `current_path`.
4. Return `Page(..., "page_content", page_block_name="page_root", ...)` or `PageComposition(..., fragment_block="page_content", page_block="page_root", ...)`.
5. Let Chirp validate that your leaf pages actually provide the required shell blocks.

That gives you one shell, one tab model, one set of fragment targets, and predictable OOB updates without app-local wrapper glue.

## Reference Pattern

This is the smallest durable pattern for a dashboard-style app:

```python
from chirp import App, AppConfig, Page, Request, use_chirp_ui

app = App(AppConfig(template_dir="templates"))
use_chirp_ui(app)


@app.get("/projects")
def projects(request: Request) -> Page:
    tab_items = (
        {"label": "Overview", "href": "/projects", "match": "exact"},
        {"label": "Runs", "href": "/projects/runs", "match": "prefix"},
    )
    return Page(
        "projects/page.html",
        "page_content",
        page_block_name="page_root",
        page_title="Projects",
        current_path=request.path,
        tab_items=tab_items,
        breadcrumb_items=[
            {"label": "Home", "href": "/"},
            {"label": "Projects"},
        ],
    )
```

```html
{% extends "chirpui/tabbed_page_layout.html" %}
{% from "chirpui/layout.html" import page_header %}

{% block page_header %}{{ page_header("Projects") }}{% end %}
{% block page_content %}
<p>Project content.</p>
{% end %}
```

If you need persistent sidebar, breadcrumbs, and shell actions, layer this under your app shell layout and keep the page-level template focused on `page_header`, `page_toolbar`, and `page_content`.

### shell_actions

Route-scoped topbar actions (buttons, links, menus) that update automatically
when navigating via htmx boost (sidebar) or tab clicks (hx-target #main or #page-root).

When extending `chirpui/app_shell_layout.html`, `shell_actions` is provided by
the layout chain from Chirp's merged `_context.py` results. When using the
`app_shell()` macro, pass it explicitly:

```html
{% call app_shell(brand="My App", shell_actions=shell_actions | default(none)) %}
  ...
{% end %}
```

The rendering macro is `shell_actions_bar(shell_actions)` from
`chirpui/shell_actions.html`. See [Chirp's app-shell guide](https://lbliii.github.io/chirp/docs/guides/app-shell/#shell-actions)
for the full cascade/override pattern (primary, controls, overflow zones;
`remove=`; `mode="replace"`).

**Design:** Prefer shell_actions for actions that apply across the whole section (e.g. "New Chain" on Discover). Page-level action strips are better for actions that only apply to the current tab. Avoid duplicating the same action in both.

**Tabbed layout:** Tabs are topmost. Put title, action strips, and content underneath (inside page_content). Order: Tabs → Title → Actions → Content.

### route_tabs and tabbed_page_layout

For route-backed subsection tabs (e.g. Workspace → Analytics, Events, Logs), the canonical macro is `render_route_tabs` from `chirpui/route_tabs.html`:

```html
{% from "chirpui/route_tabs.html" import render_route_tabs %}
{{ render_route_tabs(tab_items, current_path, target="#page-root") }}
```

Tab items: `{label, href, icon?, badge?, match?}`. `match`: `"exact"` or `"prefix"`. ChirpUI registers `tab_is_active` as a template global via `use_chirp_ui()`. The older `route_tabs(...)` name still works as a compatibility alias, but `render_route_tabs(...)` avoids the common macro/context name collision footgun.

For the full tabbed layout structure, prefer extending `chirpui/tabbed_page_layout.html` so the template itself exposes Chirp's `page_root`, `page_root_inner`, and `page_content` contract blocks:

```html
{% extends "chirpui/tabbed_page_layout.html" %}

{% block page_header %}{{ page_header("Section Title") }}{% end %}
{% block page_toolbar %}{% end %}
{% block page_content %}...{% end %}
```

Pass `tab_items` and `current_path` in page context. ChirpUI also keeps the older `tabbed_page_layout(...)` macro for compatibility, but extending the template is the recommended path for apps that use Chirp fragment targets.

See [Chirp's chirp-ui guide](https://lbliii.github.io/chirp/docs/guides/chirp-ui/) for full app-shell patterns and htmx integration.

### HTMX fragment targets

ChirpUI registers its page shell contract via `use_chirp_ui()`. That contract maps the built-in fragment targets to explicit template blocks, and Chirp validates those blocks for leaf page templates during app contract checks:

| Target | Block | Use case |
|--------|-------|----------|
| `#main` | `page_root` | Sidebar navigation (full content + tabs) |
| `#page-root` | `page_root_inner` | Tab clicks (tabs + content) |
| `#page-content-inner` | `page_content` | Narrow content swaps |

`<main id="main">` carries `hx-boost="true"`, `hx-target="#main"`, `hx-swap="innerHTML"`, and `hx-select="#page-content"` — all links inside inherit SPA navigation automatically. The `#main` element persists in the DOM (never replaced), so its `view-transition-name` is never duplicated during swaps. Content is wrapped in `<div id="page-content">` inside `#main`. Sidebar links (outside `#main`) carry their own `hx-target="#main"` via `sidebar_link()`. Section tab links use `hx-target="#page-root"`. For custom targets, use `app.register_fragment_target("target-id", fragment_block="block_name")` before `mount_pages()`. Set `triggers_shell_update=False` for narrow content swaps that should not update the topbar (e.g. inline form results).

## Debugging

When shell navigation behaves strangely, check these first:

- If sidebar navigation fails, verify the page provides `page_root`.
- If tab clicks fail, verify the page provides `page_root_inner`.
- If a narrow mutation fails, verify the target maps to `page_content` or another registered fragment block.
- Run Chirp contract checks in tests or startup so missing blocks fail before a user clicks around.
- Prefer `tab_items` and `render_route_tabs(...)` over the older `route_tabs(...)` naming to avoid macro/context collisions.

The best mental model is: target id -> registered fragment block -> block exists on the leaf page template. Once those three line up, HTMX navigation and OOB shell updates become routine.

### Polling shell regions

Use `poll_trigger()` from `chirpui/fragment_island.html` when a shell region
needs a delayed or load-triggered refresh without visible UI chrome:

```html
{% from "chirpui/fragment_island.html" import poll_trigger %}

<div id="shell-status"></div>
{{ poll_trigger("/status/summary", "#shell-status") }}
{{ poll_trigger("/status/summary?refresh=1", "#shell-status", delay="2s") }}
```

This keeps the polling markup consistent with the rest of the app-shell and
avoids repeating hidden `hx-get` button boilerplate across templates.
