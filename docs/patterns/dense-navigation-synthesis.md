# Dense Navigation Synthesis

Status: accepted guidance
Date: 2026-05-04

This is the decision ledger for the dense navigation study. Use
[NAVIGATION.md](navigation.md) for the canonical navigation contract and
[DENSE-NAVIGATION-RECIPES.md](dense-navigation-recipes.md) for copyable recipe
families. This document does not authorize new public macros by itself.

## Core Finding

Dense navigation does not need a product-specific mega-header. It needs layer
discipline:

> A control belongs to the layer that explains its job, not to the row where it
> visually fits.

Keep app identity, product movement, object context, local route views, page
tools, and command/search entrypoints as separate contracts even when the UI is
compact.

## Inputs

The study covered dense object chrome, product-suite hubs, cloud/deployment
consoles, observability consoles, keyboard-first trackers, knowledge
workspaces, design/editor workbenches, business object consoles, collaboration
inboxes, developer platforms, and reference/docs systems.

## Repeated Contracts

| Contract | Job | Current surface |
|---|---|---|
| Scope | Workspace, org, project, environment, object, channel, or docs version. | `scope_switcher`, `dropdown_menu`, `breadcrumbs` |
| Command jump | Cross-entity, route, action, and resource movement. | `command_palette_trigger`, `command_palette` |
| Broad nav | Product, workflow, or hierarchy movement. | `sidebar`, `primary_nav`, `nav_tree` |
| Shortcuts | Recent, starred, saved, assigned, unread, nearby, or later paths. | `saved_view_strip`, `primary_nav`, `chip_group` |
| Object context | Current object/path plus object actions. | `breadcrumbs`, `page_header`, `inline_counter`, `badge`, `dropdown_menu` |
| Local route views | URL-backed views of the current object/workspace. | `route_tabs` |
| Surface tools | Filters, grouping, display, time range, refresh, export, save view. | `command_bar`, `dropdown_menu`, buttons |
| Attention | Counts, unread states, pending counts, alert states. | `route_tabs`, `primary_nav`, badges, counters |

## Blessed Path

- Use `command_palette_trigger` for dense search/jump controls.
- Use `route_tabs` for URL-backed object-local views, not ARIA tabs.
- Use `nav_tree(branch_mode="linked")` for navigational hierarchy.
- Use `breadcrumbs(overflow="collapse")` for deep paths.
- Use `primary_nav` for compact horizontal route movement.
- Use `command_bar` for page-local controls and display options.
- Use `scope_switcher` for visible workspace, org, project, environment,
  account, file, channel, or docs-version scope selection.
- Use `saved_view_strip` for saved views, favorites, nearby topics, unread
  filters, assigned work, and compact shortcut rows.
- Use `resource_card` for nearby resource discovery below the chrome.

## Promotion Decisions

| Candidate | Readiness | Decision |
|---|---|---|
| Sidebar Badge Parity | Codified | Sidebar links should eventually match `route_tabs` and `primary_nav` badge stability: accessible labels, reserved space, loading, and expected states. |
| `scope_switcher` | Codified | Keep the contract small: compact dropdown-backed scope selection. Do not add product-specific schemas until repeated apps need the same metadata and state treatment. |
| `saved_view_strip` | Codified | Use this for saved views, favorites, nearby topics, unread filters, assigned work, and compact shortcut rows. Do not add editing, persistence, overflow menus, or async counts without real app evidence. |
| `dense_nav_frame` | Not API | Keep broad shell/frame ideas recipe-level until repeated route families prove a stable duplicated shape. |
| Shortcut metadata | Command launcher only | Show shortcut hints on visible controls, but do not add global shortcut dispatch without a behavior-layer plan. |

## Anti-Decisions

Do not add:

- `github_header`, `slack_sidebar`, `figma_shell`, or any product clone,
- utility classes for dense spacing, hiding, alignment, or overflow,
- JavaScript-managed responsive overflow for these recipes,
- drag-and-drop personalization,
- persisted saved-view or sidebar customization,
- a shortcut engine,
- async counter loading protocols beyond reserved/loading visual states.

## Backlog

| Priority | Item | Reason |
|---|---|---|
| Done | Publish a dense navigation recipes page | Shipped as `docs/patterns/dense-navigation-recipes.md`; keep it recipe-first until real app usage proves new macros. |
| P2 | Add browser proof for `scope_switcher` and `saved_view_strip` in dense chrome | Only needed if their layout or overflow behavior becomes more ambitious. |
| P3 | Revisit `workspace_shell` | A shell macro should remove repeated real complexity, not freeze speculative layout. |
| P3 | Add responsive browser proof for selected recipes | Needed when CSS or layout behavior changes, not for static composition examples. |

## Acceptance Rule For New API

Before adding a dense navigation component, answer:

1. Which layer does it own?
2. Which existing primitive composition is insufficient?
3. Which recipes repeat the same shape?
4. What public classes will it emit, and are they registry-cited?
5. What are its route, ARIA, overflow, and badge/count contracts?
6. Which docs, examples, tests, manifest entries, and generated references move
   with it?

If those answers are not concrete, keep the pattern as a documented recipe.
