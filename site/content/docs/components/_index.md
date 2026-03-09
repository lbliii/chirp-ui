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
| **Data display** | badge, spinner, skeleton, progress, description_list, timeline, tree_view, calendar |
| **Streaming** | streaming_block, copy_btn, model_card — for htmx SSE and LLM UIs |

See the [component showcase](https://github.com/lbliii/chirp-ui#usage) for live examples. Run:

```bash
pip install chirp chirp-ui
python examples/component-showcase/app.py
```

Open http://localhost:8000
