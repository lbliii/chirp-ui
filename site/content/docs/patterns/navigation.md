---
title: Navigation Patterns
description: Dense navigation contracts and route semantics for Chirp UI pages
draft: false
weight: 10
lang: en
type: doc
keywords: [chirp-ui, navigation, route tabs, command palette, sidebar]
category: patterns
---

Navigation in Chirp UI is layered. A compact control can be a route link, tab
panel switch, disclosure, command launcher, or search entry, and those jobs have
different semantics.

Use the canonical repository guide for the full decision model:
[`docs/NAVIGATION.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/NAVIGATION.md?plain=1).
For copyable dense application chrome recipes, see
[`docs/DENSE-NAVIGATION-RECIPES.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/DENSE-NAVIGATION-RECIPES.md?plain=1).
For current roadmap status, see
[`docs/plans/PLAN-application-chrome-system.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/plans/PLAN-application-chrome-system.md?plain=1).

## Source Of Truth

This page is a published bridge. The repository docs remain the contract for
component semantics, application chrome layering, and promotion decisions:

- `docs/NAVIGATION.md` owns the layer model and component decision matrix.
- `docs/DENSE-NAVIGATION-RECIPES.md` owns copyable recipe families.
- `docs/plans/PLAN-application-chrome-system.md` owns the active app-chrome
  backlog and composite gates.
- `docs/RESPONSIVE.md` owns stress-width expectations.
- `docs/VISUAL-AUDIT-SHOWCASE.md` owns rhythm and visual proof expectations.

Do not add a published-only application chrome API here. New public macros,
parameters, emitted classes, or manifest facts must ship through the registry,
templates, generated CSS, generated component options, examples, and tests.

## Use This When

- A page needs global app or site movement.
- An object page needs breadcrumbs, title metadata, actions, and local routes.
- A docs or workspace surface has nested section navigation.
- A dense topbar needs search, jump, command, status, or overflow controls.

## Blessed Surfaces

- `site_header`, `navbar`, `primary_nav`, `sidebar`, and `nav_tree` for broad
  navigation.
- `drawer` and `tray` for phone fallback, inspectors, and supplemental overlay
  chrome when persistent rails would starve the main surface.
- `breadcrumbs` and page headers for object or path context.
- `render_route_tabs` / `route_tabs` for URL-backed local views.
- `tabs_panels` only for in-place tab panel switching.
- `command_palette_trigger` plus `command_palette` for search and jump.
- `command_bar`, `filter_bar`, and `action_strip` for page-local tools.

## Checks

- Route navigation stays link-native with real `href` values.
- Current pages use `aria-current="page"`.
- Route tabs are not modeled as ARIA tabs.
- Ordinary disclosure navigation is not modeled as an ARIA menu.
- Dense nav reserves room for expected badge counts.
- Mobile layouts keep context and primary actions reachable.
- Application chrome remains recipe-first until repeated real app usage proves
  a stable composite contract.
- Browser proof covers rail/tray fallback, command focus, route-tab scroll, and
  no unintended horizontal overflow before composite promotion.
