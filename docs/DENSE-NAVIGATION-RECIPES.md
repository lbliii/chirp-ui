# Dense Navigation Recipes

Status: accepted guidance
Date: 2026-05-12

Dense navigation is a layer problem. App identity, scope, command jump, broad
navigation, object context, route views, page tools, and attention states should
stay separate contracts even when the UI is compact.

This guide turns the dense-navigation study into copyable Chirp UI recipes. It
does not introduce a product-specific mega-shell.

## Layer Model

| Layer | Job | Chirp UI surface |
|---|---|---|
| App identity | Tell the user which product or app they are in | `app_shell`, `navbar`, logo/title slots |
| Scope | Set workspace, org, project, environment, customer, channel, file, or docs version | `scope_switcher`, `dropdown_menu`, `breadcrumbs` |
| Command jump | Move across entities, pages, actions, and resources | `command_palette_trigger`, `command_palette` |
| Broad navigation | Move between product areas or hierarchy roots | `sidebar`, `primary_nav`, `nav_tree` |
| Personal shortcuts | Recent, starred, saved, assigned, unread, nearby, later | `saved_view_strip`, `primary_nav`, `chip_group` |
| Object context | Explain the current object/path and object actions | `page_header`, `breadcrumbs`, `badge`, `inline_counter` |
| Local route views | Switch URL-backed views of the current object | `route_tabs` |
| Page tools | Filter, group, display, time range, refresh, export | `command_bar`, buttons, dropdowns |
| Attention | Counts, unread, pending, alert, loading, reserved states | badges, `badge_label`, `badge_loading`, `badge_expected` |

## Product-Suite Work Hub

Use when users move across work, strategy, projects, dashboards, and saved
personal views.

Recipe:

- `scope_switcher` for workspace or org.
- `command_palette_trigger` for global search/create.
- `primary_nav` for product modes.
- `sidebar` / `nav_tree` for broad and personal navigation.
- `route_tabs` for project-local views.
- `saved_view_strip` for assigned, starred, blocked, recently viewed, or team
  shortcuts.

Keep out of the public API for now:

- draggable personalization,
- persisted sidebar ordering,
- product-specific app switchers.

Reference implementation:

- `examples/component-showcase/templates/showcase/_suite_work_hub.html`

## Cloud And Deployment Console

Use when scope, resources, services, deployments, environments, and project
search all compete for space.

Recipe:

- `scope_switcher` before local controls.
- `command_palette_trigger` as search-or-jump.
- `primary_nav` or `saved_view_strip` for favorite services.
- `resource_card` or tables for resources.
- `route_tabs` for deployments, domains, logs, settings, and activity.
- Stable badges for resource counts and pending deployment counts.

Keep out of the public API for now:

- vendor-specific service schemas,
- drag-reorder favorites,
- async counter loading beyond reserved/loading visual states.

Reference implementation:

- `examples/component-showcase/templates/showcase/_cloud_console_nav.html`

## Observability And Ops Console

Use when dashboards, logs, traces, alerts, incidents, saved investigations, and
time controls need dense but predictable placement.

Recipe:

- Command search is the primary cross-system jump path.
- Sidebar groups operational domains.
- `command_bar` owns time range, refresh, filters, and export.
- `route_tabs` switch Logs, Metrics, Traces, Alerts, and Incidents.
- `saved_view_strip` captures investigations and common dashboard filters.

Keep out of the public API for now:

- a shortcut engine,
- JavaScript-managed toolbar overflow,
- a product-specific observability shell.

Reference implementation:

- `examples/component-showcase/templates/showcase/_ops_console_nav.html`

## Knowledge Workspace

Use when hierarchy, private/team boundaries, page-local routes, and nearby
topics matter.

Recipe:

- `scope_switcher` for workspace/teamspace.
- `nav_tree(branch_mode="linked")` for page hierarchy.
- `breadcrumbs(overflow="collapse")` for deep paths.
- `route_tabs` for Overview, Tasks, Comments, History, or Files.
- `resource_card` or `saved_view_strip` for nearby topics.

Keep out of the public API for now:

- real-time collaborative presence,
- drag-and-drop page trees,
- app-specific private/teamspace schemas.

Reference implementation:

- `examples/component-showcase/templates/showcase/_knowledge_workspace_nav.html`

## Object Page Console

Use when one durable business object owns multiple local views, nearby records,
status, saved filters, and page-local actions.

Recipe:

- `breadcrumbs(overflow="collapse")` for the object path.
- `page_header` for object title, lifecycle status, and primary actions.
- `route_tabs` for Overview, Activity, Related, History, and Settings.
- `command_bar` for local filters, display mode, refresh, and export.
- `saved_view_strip` for common object slices such as Mine, Blocked, Recently
  changed, or Needs review.
- `badge_label`, `badge_expected`, and `badge_loading` for every dense count
  whose accessible meaning is not obvious from its visible number.

Keep out of the public API for now:

- object-type-specific headers,
- persisted per-user object chrome,
- generic `dense_object_header` or `object_console_shell` macros.

Reference implementation:

- `examples/component-showcase/templates/showcase/_business_object_console.html`

## Developer Platform

Use when project/group/user scopes and workflow navigation are all first-class.

Recipe:

- `scope_switcher` for project, group, or profile.
- Command jump for issues, merge requests, pipelines, docs, settings, and
  resources.
- Context-sensitive sidebar for project/group workflows.
- `route_tabs` for current project views.
- `command_bar` for filters and display controls.

Keep out of the public API for now:

- Git-host-specific headers,
- route-specific hardcoded shortcut systems,
- product-clone component names.

Reference implementation:

- `examples/component-showcase/templates/showcase/_developer_platform_nav.html`

## Implementation Rule

Promote a dense-navigation macro only when all of these are true:

- The layer it owns is explicit.
- Existing primitive composition is measurably insufficient.
- At least two recipes repeat the same shape.
- Emitted classes can be registry-cited.
- Route, ARIA, overflow, and badge/count contracts are clear.
- Docs, examples, tests, manifest entries, and generated references move with
  the API.

Until then, keep the shape as a recipe.

## Composite Promotion Boundary

`workspace_shell`, dense object chrome, and product-specific shells stay
recipe-level unless a real consuming app repeats the same layer contract. A
showcase example is evidence for documentation; it is not enough evidence for a new stable macro.
