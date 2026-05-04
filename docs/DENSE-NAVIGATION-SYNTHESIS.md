# Dense Navigation Synthesis

Status: accepted guidance
Date: 2026-05-04

This document distills the dense navigation recipe study into component
contracts and primitive candidates. It is intentionally not a component API
proposal by itself. New public macros still need a concrete implementation plan,
tests, descriptors, docs, and migration notes.

## Inputs

The synthesis is based on the component showcase recipes for:

- dense object chrome,
- product-suite work hub,
- cloud and deployment console,
- observability and ops console,
- keyboard-first tracker,
- knowledge workspace,
- design/editor workbench,
- business object console,
- collaboration inbox,
- developer platform,
- reference/docs system.

## Core Finding

Dense navigation does not need a product-specific mega-header. It needs layer
discipline. The recipes could all be built from existing ChirpUI primitives once
the command launcher and stable badge contracts were available.

The most important rule is:

> A control should belong to the layer that explains its job, not to the row
> where it visually fits.

That means app identity, product movement, object context, local route views,
page tools, and command/search entrypoints remain separate contracts even when
they are visually compact.

## Repeated Contracts

| Contract | Job | Current ChirpUI surface |
|----------|-----|-------------------------|
| Scope | Sets the active workspace, project, org, environment, file, object, channel, or docs version | `dropdown_menu`, `breadcrumbs`, shell slots |
| Command jump | Moves across entities, pages, actions, and resources | `command_palette_trigger`, `command_palette` |
| Broad navigation | Moves between product areas, workflow areas, or hierarchies | `sidebar`, `primary_nav`, `nav_tree` |
| Personal shortcuts | Gives users recent, starred, saved, assigned, unread, nearby, or later paths | `primary_nav`, `chip_group`, `sidebar` |
| Object context | Explains the current object/path and object actions | `breadcrumbs`, `page_header`, `inline_counter`, `badge`, `dropdown_menu` |
| Local route views | Switches URL-backed views of the current object/workspace | `route_tabs` |
| Surface tools | Filters, grouping, display, time range, refresh, export, save view | `command_bar`, `dropdown_menu`, buttons |
| Attention | Counts, unread states, pending counts, alert states | `route_tabs`, `primary_nav`, badges, counters |
| Nearby discovery | Shows adjacent pages/resources without replacing the current hierarchy | `chip_group`, `resource_card`, `nav_tree` |

## Ready Contracts

These are already supported well enough to document as the blessed path:

- Use `command_palette_trigger` for dense chrome search and jump controls.
- Use `route_tabs` for URL-backed object-local views, not ARIA tabs.
- Use `nav_tree(branch_mode="linked")` for hierarchy that is primarily
  navigation.
- Use `breadcrumbs(overflow="collapse")` for deep object or page paths.
- Use `primary_nav` for compact horizontal route movement.
- Use `command_bar` for page-local controls and display options.
- Use `scope_switcher` for visible workspace, org, project, environment,
  account, file, channel, or docs-version scope selection.
- Use `saved_view_strip` for saved views, favorites, nearby topics, unread
  filters, assigned work, and compact shortcut rows.
- Use `resource_card` for nearby resource discovery below the chrome.

## Primitive Candidates

These candidates showed up repeatedly, but they should move at different speeds.

### 1. Sidebar Badge Parity

Readiness: codified.

Why: `route_tabs` and `primary_nav` already support `badge_label`,
`badge_expected`, and `badge_loading`. Several recipes need the same stability
and accessible-label contract in side navigation.

API:

```html
{{ sidebar_link(
  "/inbox",
  "Inbox",
  icon="alert",
  badge=3,
  badge_label="3 unread inbox items",
  badge_loading=false,
  badge_expected=true
) }}
```

Proof:

- sidebar render tests for visible, reserved, loading, and labelled badges,
- template/CSS contract coverage for emitted badge state classes,
- `COMPONENT-OPTIONS.md` and manifest rebuild if the macro signature changes,
- a showcase recipe updated to use the new states.

### 2. Scope Switcher Pattern

Readiness: codified as a small pattern macro.

Why: every dense app needs scope before local controls, but scope varies:
workspace, org, project, account, environment, file, customer, channel, or docs
version. The stable contract is intentionally small: render a compact dropdown
trigger for choosing scope using the existing `dropdown_menu` item model.

API:

```html
{{ scope_switcher("Prod / us-east", items=scopes, aria_label="Switch cloud scope") }}
```

Do not add product-specific scope item schemas until at least two real apps need
the same status treatment, metadata, and keyboard/focus contract.

### 3. Saved View Strip Pattern

Readiness: codified as a small pattern macro.

Why: saved views, favorites, starred items, nearby topics, unread filters, and
recent resources all benefit from the same compact row shape. Today `chip_group`
already expressed the low-level shape; `saved_view_strip` names the navigation
contract and keeps shortcut rows distinct from generic tag/facet chips.

API:

```html
{{ saved_view_strip(label="Saved views", views=[
  {"label": "Mine", "href": "/views/mine", "selected": true},
  {"label": "Blocked", "href": "/views/blocked"}
]) }}
```

Do not add saved-view editing, persistence, overflow menus, or async counts
until real apps prove the missing behavior.

### 4. Dense Navigation Frame

Readiness: not yet API.

Why: many recipes share a broad shape: top utilities, sidebar, object context,
route tabs, and page controls. The exact shell contract still changes by app
family, and the existing `app_shell`, `frame`, `grid`, `stack`, and `block`
primitives can express the pattern.

Do not add `dense_nav_frame`, `workspace_shell`, or product-specific shells
until the duplicated template shape is stable enough to reduce real complexity.

### 5. Shortcut Metadata

Readiness: command launcher only.

Why: shortcut labels are useful navigation hints, but a full shortcut engine is
not part of this phase. The visible control must remain usable without the
shortcut.

Current blessed composition:

```html
{{ command_palette_trigger(
  target="project-palette",
  label="Search project",
  placeholder="Search or jump",
  shortcut="/",
  icon="search",
  density="sm"
) }}
```

Do not add global shortcut dispatch until there is a real behavior layer plan.

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
|----------|------|--------|
| P1 | Publish a dense navigation recipes page | The showcase is copyable, but a focused docs page would teach the layer model more directly. |
| P2 | Add browser proof for `scope_switcher` and `saved_view_strip` in dense chrome | Needed if their layout or overflow behavior becomes more ambitious. |
| P3 | Revisit `workspace_shell` after real app usage | A shell macro should remove duplication, not freeze a speculative layout. |
| P3 | Add browser responsive proof for selected recipes | Needed only when CSS or layout behavior changes, not for static composition examples. |

## Acceptance Rule For New API

Before adding a dense navigation component, answer all of these:

1. Which layer does it own?
2. Which existing primitive composition is insufficient?
3. Which recipes repeat the same shape?
4. What public classes will it emit, and are they registry-cited?
5. What are its route, ARIA, overflow, and badge/count contracts?
6. Which docs, examples, tests, manifest entries, and generated references move
   with it?

If those answers are not concrete, keep the pattern as a documented recipe.
