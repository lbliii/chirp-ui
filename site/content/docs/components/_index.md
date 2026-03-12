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
| **UI** | card, card_header, modal, drawer, tabs, accordion, dropdown, popover, toast, table, pagination, alert, button_group |
| **Forms** | text_field, password_field, textarea_field, select_field, checkbox_field, toggle_field, radio_field, file_field, date_field |
| **Data display** | badge, spinner, skeleton, progress, [description_list](./type-aware-rendering.md) (type-aware), timeline, tree_view, calendar |
| **Streaming** | streaming_block, copy_btn, model_card — for htmx SSE and LLM UIs |
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
