---
title: Components
description: The on-site catalog of every chirp-ui macro — grouped, scannable, with live examples
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, components, catalog, layout, cards, forms, modal, macros]
category: components
---

# Component catalog

chirp-ui ships a registry of Kida macros — import from `chirpui/` and use with
`{% call %}`. Every public macro is backed by `manifest.json`, so this catalog,
the [component showcase](/showcase/), and the [API reference](/api/) all stay in
sync with the registry.

Browse the catalog below by category, see live specimens in the showcase, and
read the anatomy deep-dives for the components with the most moving parts. You
never need to leave the site or run a local app to see a component rendered.

:::{cards}
:columns: 3
:gap: medium

:::{card} Component showcase
:icon: layers
:link: /showcase/
Every macro and pattern rendered in one static, offline-friendly gallery.
:::{/card}

:::{card} Live specimens
:icon: eye
:link: ./controls/
In-page `component_specimen` demos for high-traffic primitives.
:::{/card}

:::{card} Authoring vocabulary
:icon: code
:link: /docs/reference/
Shortcodes and directives for embedding components and callouts in prose.
:::{/card}

:::{/cards}

## Catalog by category

The registry groups macros into the categories below. Counts reflect the public
(non-internal) surface in `manifest.json`.

| Category | What lives here | Representative macros |
|----------|-----------------|-----------------------|
| **Layout** | Page scaffolding and composition primitives | `app_shell`, `container`, `grid`, `stack`, `block`, `cluster`, `frame`, `page_header`, `section_header`, `divider`, `description_list` |
| **Container** | Surface chrome that frames content | `card`, `surface`, `panel`, `modal`, `overlay`, `settings_row`, `config_row` |
| **Navigation** | Moving between and within views | `breadcrumbs`, `nav_tree`, `nav_link`, `dropdown`, `dropdown_select`, `filter_rail`, `nav_progress`, `index_card` |
| **Control** | Buttons, toolbars, and action clusters | `btn`, `icon_btn`, `btn_group`, `action_bar`, `action_strip`, `command_bar`, `copy_btn`, `filter_group`, `kbd` |
| **Form** | Fields, fieldsets, and form chrome | `form`, `field`, `fieldset`, `filter_bar`, `form_actions`, `form_error_summary`, `inline_edit`, `input_group`, `composer_shell` |
| **Data display** | Tables, charts, avatars, and records | `data_table`, `bar_chart`, `calendar`, `avatar`, `avatar_stack`, `chip`, `timeline`, `tree_view`, `description_list` |
| **Feedback** | Status, alerts, and progress | `alert`, `badge`, `callout`, `confirm`, `progress`, `empty_state`, `notification_dot`, `counter_badge`, `live_badge` |
| **Interactive** | Stateful widgets and motion behaviors | `accordion`, `carousel`, `collapse`, `command_palette`, `infinite_scroll`, `sortable`, `island_root` |
| **Overlay** | Layered surfaces | `drawer`, `tray`, `popover` |
| **Content** | Inline content primitives | `code`, `code_block`, `install_snippet`, `item`, `label_overline`, `logo`, `signature` |
| **Typography** | Type scale and measure utilities | `display`, `font_*`, `measure_*`, `text_*` helpers |
| **Marketing** | Landing-page and site-shell sections | `site_shell`, `site_header`, `site_footer`, `band`, `cta_band`, `feature_section`, `feature_stack`, `logo_cloud` |
| **Media** | Catalog and watch-side surfaces | `catalog_rail`, `media_hero_shelf`, `title_card`, `video_thumbnail`, `live_event_card` |
| **Social** | Community and discussion surfaces | `topic_card`, `answer_card`, `thread_reader_layout`, `moderation_queue_item` |
| **Effect** | Decorative and ambient treatments | `aura`, `aurora`, `bento`, `bg_pattern`, `border_beam`, `ambient` |
| **ASCII** | Terminal-flavored primitives | `ascii_card`, `ascii_tabs`, `ascii_modal`, `ascii_border`, `ascii_table`, `ascii_7seg`, `ascii_fader`, `ascii_knob`, and more |
| **Composite** | Full assembled surfaces | `resource_index` |

For the complete, machine-readable list of every macro with its parameters,
slots, variants, and maturity, see the [API reference](/api/) (generated from
`manifest.json`).

## Live examples

These pages render real components in-page using the `component_specimen`
shortcode and document the rendered contract for the components with the most
moving parts.

:::{cards}
:columns: 2
:gap: medium

:::{card} Control selection
:icon: settings
:link: ./controls/
Native fields, dropdown selects, toggle groups, sliders, date inputs, and
composed data tables — each with a live specimen.
:::{/card}

:::{card} Appearance and tone
:icon: palette
:link: ./appearance-tone/
The shared `appearance` / `tone` vocabulary for visual treatment and semantic
intent across high-traffic components.
:::{/card}

:::{card} Dropdown anatomy
:icon: chevron-down
:link: ./dropdowns/
ARIA roles, Alpine controllers, focus behavior, event payloads, and HTMX link
attributes for menus, selects, and split menus.
:::{/card}

:::{card} Modal anatomy
:icon: enlarge
:link: ./modals/
Native `<dialog>` usage, Alpine target/store behavior, close controls, events,
and HTMX confirm forms.
:::{/card}

:::{card} Tabs anatomy
:icon: list
:link: ./tabs/
HTMX tabs, client-side tab panels, and URL-backed route tabs — keeping ARIA tab
widgets distinct from navigation links.
:::{/card}

:::{card} Drawer & tray anatomy
:icon: sidebar
:link: ./drawers-trays/
Slide-out dialog behavior, Alpine store state, close events, and focus trapping.
:::{/card}

:::{card} Type-aware rendering
:icon: file-text
:link: ./type-aware-rendering/
How `description_list` and friends adapt their markup to the shape of the data
you pass.
:::{/card}

:::{card} ASCII primitives
:icon: terminal
:link: ./ascii/
The terminal-flavored component family — cards, tabs, modals, faders, knobs, and
seven-segment displays.
:::{/card}

:::{card} Islands & mutation
:icon: package
:link: ./islands/
HTMX fragment islands, polling triggers, and confirm flows for server-driven
dashboards.
:::{/card}

:::{/cards}

## Composition helpers

For server-driven dashboards and settings pages, chirp-ui ships macros that
standardize common htmx patterns instead of hand-writing hidden buttons:

- `fragment_island(...)` wraps a target region refreshed independently
- `fragment_island_with_result(...)` pairs a controls region with a result pane
- `poll_trigger(url, target, delay=...)` renders the hidden polling button used
  for load-time or delayed refreshes
- `confirm_dialog(...)` and `confirm_trigger(...)` provide consistent
  confirmation flows around destructive or high-friction actions

```html
{% from "chirpui/fragment_island.html" import poll_trigger %}

<div id="collection-status"></div>
{{ poll_trigger("/collections/status?refresh=1", "#collection-status", delay="1s") }}
```

Use these helpers instead of hand-writing hidden htmx buttons in each template.

## Out-of-band, suspense, and navigation

- **OOB helpers** — `oob_fragment`, `oob_toast`, and `counter_badge` compose
  out-of-band swaps for server-driven updates.
- **Suspense** — `suspense_slot` and `suspense_group` drive skeleton-to-content
  deferred loading.
- **Navigation extras** — `nav_progress` renders a CSS-only loading bar for htmx
  page transitions.
- **Streaming** — `streaming_block`, `model_card`, `sse_status`, and `sse_retry`
  support htmx SSE and LLM UIs.

Browse the [showcase](/showcase/) to see each of these rendered, and the
[API reference](/api/) for every parameter.
