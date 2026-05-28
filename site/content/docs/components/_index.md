---
title: Components
description: Layout, UI, forms, streaming, and dashboard components
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, components, layout, cards, forms, modal]
category: components
---

# Components

chirp-ui provides Kida macros organized by category. Import from `chirpui/` and use with `{% call %}`.

## Categories

| Category | Examples |
|----------|----------|
| **Layout** | container, grid, stack, block, page_header, section_header, divider, breadcrumbs, navbar, sidebar, hero, surface, callout |
| **UI** | card, card_header, modal, drawer, tabs, accordion, dropdown, popover, toast, table, pagination, alert, button_group, toggle_group, item |
| **Forms** | text_field, password_field, textarea_field, select_field, checkbox_field, toggle_field, radio_field, file_field, date_field, slider, form_error_summary |
| **Data display** | badge, spinner, skeleton, progress, description_list (type-aware), timeline, tree_view, calendar, data_table |
| **Streaming** | streaming_block, copy_btn, model_card, sse_status, sse_retry — for htmx SSE and LLM UIs |
| **HTMX helpers** | oob_fragment, oob_toast, counter_badge — out-of-band swap composition |
| **Suspense** | suspense_slot, suspense_group — skeleton-to-content deferred loading |
| **Navigation extras** | nav_progress — CSS-only loading bar for htmx page transitions |
| **ASCII primitives** | ascii_card, ascii_tabs, ascii_modal, ascii_border, ascii_table, ascii_7seg, ascii_fader, ascii_knob, and 19 more |
| **Mutation helpers** | fragment_island, fragment_island_with_result, poll_trigger, confirm_dialog, confirm_trigger |

See the [component showcase](https://github.com/lbliii/chirp-ui#usage) for live examples. Run:

```bash
pip install chirp chirp-ui
python examples/component-showcase/app.py
```

Open http://localhost:8000

## Mutation helpers

For server-driven dashboards and settings pages, chirp-ui also ships a small set
of macros that standardize common htmx patterns:

- `fragment_island(...)` wraps a target region that is refreshed independently
- `fragment_island_with_result(...)` pairs a controls region with a result pane
- `poll_trigger(url, target, delay=...)` renders the hidden polling button used
  for load-time or delayed refreshes
- `confirm_dialog(...)` and `confirm_trigger(...)` provide consistent
  confirmation flows around destructive or high-friction actions

Example:

```html
{% from "chirpui/fragment_island.html" import poll_trigger %}

<div id="collection-status"></div>
{{ poll_trigger("/collections/status?refresh=1", "#collection-status", delay="1s") }}
```

Use these helpers instead of hand-writing hidden htmx buttons in each template.

## Visual presets

The `appearance` / `tone` pilot gives high-traffic components a shared macro
vocabulary for visual treatment and semantic intent without introducing utility
classes. See [Appearance and tone](/docs/components/appearance-tone/) for the
published guide.

## Interactive anatomy

Use [Control selection](/docs/components/controls/) when choosing between native
fields, dropdown-select, toggle groups, sliders, date inputs, and composed data
tables.

Dropdown menus, selects, and split menus have a published rendered contract for
ARIA roles, Alpine controllers, focus behavior, event payloads, and HTMX link
attrs. See [Dropdown anatomy](/docs/components/dropdowns/).

Native modals, overlay modals, and confirm dialogs have a published rendered
contract for `<dialog>` usage, Alpine target/store behavior, close controls,
events, and HTMX confirm forms. See [Modal anatomy](/docs/components/modals/).

Htmx tabs, client-side tab panels, and URL-backed route tabs have a published
rendered contract that keeps ARIA tab widgets distinct from navigation links.
See [Tabs anatomy](/docs/components/tabs/).

Native drawers and store-backed trays have a published rendered contract for
slide-out dialog behavior, Alpine store state, close events, and focus trapping.
See [Drawer and tray anatomy](/docs/components/drawers-trays/).
