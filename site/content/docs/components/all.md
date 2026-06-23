---
title: All components
description: The complete on-site index of every public Chirp UI macro - generated from manifest.json
draft: false
weight: 21
lang: en
type: doc
keywords: [chirp-ui, components, catalog, index, macros, manifest]
tags: [components, reference]
category: components
---

# All components

This is the complete, manifest-backed index of **every public Chirp UI macro** -
grouped by category, each with its one-line description. It is generated from
`src/chirp_ui/manifest.json`, so it can never drift behind the registry: the
[on-site coverage test](https://github.com/lbliii/chirp-ui/blob/main/tests/docs_contracts/test_onsite_component_coverage.py)
fails CI if a public component is missing here.

You never need to leave the site or run a local app to discover a component:

- See any macro rendered in the [component showcase](/showcase/).
- Read every parameter, slot, variant, and maturity in the [API reference](/api/).
- Read the anatomy deep-dives linked from the [component catalog](./).

**Maturity:** `stable` = documented public surface for normal app use;
`experimental` = public but still settling; `legacy` = supported compatibility
surface with a preferred replacement. Components the manifest marks `internal`
(Chirp UI composition infrastructure) are intentionally omitted.

<!-- chirpui:generated:start -->
_379 public components across 17 categories._

## Layout

_59 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `actions` *(CSS / utility)* | stable | - |
| `app_shell` | stable | App Shell component |
| `aspect_ratio` | stable | Aspect Ratio |
| `block` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `chat_layout` | stable | Chat Layout component |
| `children` *(CSS / utility)* | stable | - |
| `citation_chip` | stable | Citations |
| `clamp-2` *(CSS / utility)* | legacy | - |
| `clamp-3` *(CSS / utility)* | legacy | - |
| `cluster` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `container` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `density` *(CSS / utility)* | stable | - |
| `description_list` | stable | Description list component |
| `detail_header` | experimental | Detail header |
| `divider` | stable | Divider component |
| `document_header` | stable | Document header |
| `entity_header` | stable | Entity header (dashboard-grade) |
| `flow` *(CSS / utility)* | stable | - |
| `focus-ring` *(CSS / utility)* | legacy | - |
| `frame` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `grid` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `hero` | stable | Hero component |
| `inline` *(CSS / utility)* | stable | - |
| `inspector_panel` | experimental | Dense workspace primitives |
| `layer` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `list-reset` *(CSS / utility)* | legacy | - |
| `mb-md` *(CSS / utility)* | legacy | - |
| `media_object` | stable | Media Object layout primitive |
| `message_actions` | stable | Message actions |
| `message_meta` | stable | Message meta |
| `message_bubble` | stable | Message Bubble component |
| `metric_grid` | stable | Metric grid/card |
| `min-w-0` *(CSS / utility)* | legacy | - |
| `mt-md` *(CSS / utility)* | legacy | - |
| `mt-sm` *(CSS / utility)* | legacy | - |
| `page-fill` *(CSS / utility)* | experimental | - |
| `page_header` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `page_hero` | stable | Hero component |
| `placeholder-inline` *(CSS / utility)* | legacy | - |
| `reasoning_block` | stable | Reasoning + tool-call disclosure |
| `scroll_area` | stable | Scroll Area |
| `scroll-x` *(CSS / utility)* | legacy | - |
| `search_header` | experimental | Search Header composite |
| `section_collapsible` | experimental | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `section_header` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `separator` | stable | Separator |
| `shell-action-form` *(CSS / utility)* | experimental | - |
| `shell_actions_bar` | stable | Shell actions renderer |
| `shell-section` *(CSS / utility)* | experimental | - |
| `sources_summary` | stable | Citations |
| `split_layout` | stable | Split layout |
| `split_panel` | stable | Split Panel |
| `stack` | stable | Layout primitives — container, grid (flow), frame (structural), stack, cluster, layer (overlap deck), block. |
| `status_step` | stable | Status timeline |
| `status_timeline` | stable | Status timeline |
| `tool_call_card` | stable | Reasoning + tool-call disclosure |
| `truncate` *(CSS / utility)* | legacy | - |
| `visually-hidden` *(CSS / utility)* | legacy | - |
| `workspace_shell` | experimental | Workspace shell |

## Container

_9 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `card` | stable | Card component |
| `config_row_toggle` | stable | Config row — label \| control (toggle, select, editable) |
| `config-row-list` *(CSS / utility)* | stable | - |
| `modal` | stable | Modal component |
| `overlay` | stable | Overlay component |
| `panel` | stable | Panel component |
| `settings_row` | stable | Settings row — label \| status badge \| detail |
| `settings_row_list` | stable | Settings row — label \| status badge \| detail |
| `surface` | stable | Surface component |

## Navigation

_33 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `breadcrumbs` | stable | Breadcrumbs component |
| `context_menu` | experimental | Context Menu |
| `context_menu` | experimental | Context Menu |
| `conversation_item` | stable | Conversation Item component |
| `conversation_list` | stable | Conversation List component |
| `dropdown` | stable | Dropdown component |
| `dropdown_select` | stable | Dropdown menu, select, and split-button primitives. |
| `dropdown_menu` | stable | Dropdown menu, select, and split-button primitives. |
| `filter_rail` | experimental | Dense workspace primitives |
| `index_card` | stable | Index card component |
| `link` | stable | Link component |
| `menubar` | experimental | Menubar |
| `menubar` | experimental | Menubar |
| `nav_link` | stable | SPA-style link for content areas |
| `nav-pill` *(CSS / utility)* | stable | - |
| `nav_progress` | stable | Navigation progress bar |
| `nav_tree` | stable | Nav tree component |
| `navbar` | stable | Navbar component |
| `navbar_dropdown` | stable | Navbar component |
| `navigation_menu` | experimental | Navigation Menu |
| `pagination` | stable | Pagination component |
| `primary_nav` | stable | Primary navigation |
| `render_route_tabs` | stable | Route-backed subsection tabs |
| `route-tabs` *(CSS / utility)* | stable | - |
| `saved_view_strip` | stable | Saved view strip |
| `scope_switcher` | stable | Scope switcher |
| `sidebar` | stable | Sidebar component |
| `sidebar_toggle` | stable | Sidebar component |
| `stepper` | stable | Stepper component |
| `tab` | stable | Tabs component |
| `tab-panel` *(CSS / utility)* | stable | - |
| `tabs` | stable | Tabs component |
| `tooltip` | stable | Tooltip macro |

## Control

_25 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `action_bar` | stable | Action Bar component |
| `action_strip` | stable | Action Strip component |
| `btn` | stable | Button component. Use chirpui-btn with variants. Supports loading state for htmx. |
| `btn-group` *(CSS / utility)* | stable | - |
| `bulk-bar` *(CSS / utility)* | experimental | - |
| `command-bar` *(CSS / utility)* | stable | - |
| `copy_button` | stable | Copy button |
| `fab` | stable | Floating Action Button |
| `facet_chip` | experimental | Facet chip |
| `filter_group` | stable | Filter chips — radiogroup + pill chips (named colors / HTMX) |
| `filter_row` | stable | Filter Bar composite |
| `icon_btn` | stable | Icon Button |
| `kbd` | stable | Keyboard key |
| `row_actions` | stable | Row actions (kebab menu) |
| `segmented_control` | stable | Segmented Control |
| `selection_bar` | stable | Selection Bar |
| `shortcuts_help` | stable | Keyboard shortcuts help |
| `slider` | stable | Slider |
| `split_button` | stable | Split button component |
| `star-rating` *(CSS / utility)* | stable | - |
| `tag_browse_tray` | stable | Tag browse — tray + selection badges for tag-filtered listings |
| `theme_toggle` | stable | Theme + style toggles |
| `thumbs` *(CSS / utility)* | stable | - |
| `toggle` *(CSS / utility)* | experimental | - |
| `toggle_group` | stable | Toggle Group |

## Form

_27 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `advanced_params` | stable | Parameter override controls |
| `attachment_chip` | experimental | File item / attachment chip |
| `composer` | experimental | Chat Input / Composer |
| `combobox` | experimental | Combobox / autocomplete |
| `composer_shell` | experimental | Composer shell |
| `date_picker` | experimental | Date / range picker |
| `field_wrapper` | stable | Form field macros |
| `fieldset` | stable | Form field macros |
| `filter-bar` *(CSS / utility)* | stable | - |
| `suggestion_chips` | experimental | Follow-up / suggestion chips |
| `form` | stable | Form field macros |
| `form_actions` | stable | Form field macros |
| `form_error_summary` | stable | Form field macros |
| `inline_edit_field_display` | stable | Inline edit field |
| `input_group` | stable | Form field macros |
| `input_otp` | experimental | Input OTP |
| `key-value-form` *(CSS / utility)* | stable | - |
| `ui_label` | stable | Label |
| `number-scale` *(CSS / utility)* | experimental | - |
| `param_field` | stable | Parameter override controls |
| `scope_indicator` | stable | Parameter override controls |
| `search_bar` | stable | Form field macros |
| `tag_input` | stable | Tag input component |
| `tag_input` | stable | Tag input component |
| `toggle_field` | stable | Form field macros |
| `token_input` | experimental | Token input |
| `wizard_form` | stable | Wizard form component |

## Data display

_38 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `animated_stat_card` | stable | Animated Stat Card |
| `avatar` | stable | Avatar component |
| `avatar_stack` | stable | Avatar Stack component |
| `bar_chart` | stable | Bar Chart component |
| `calendar` | stable | Calendar component |
| `channel_card` | stable | Channel Card component |
| `chapter_item` | stable | Chapter List component |
| `chapter_list` | stable | Chapter List component |
| `chip` | stable | Chip group |
| `chip_group` | stable | Chip group |
| `comment` | stable | Comment component |
| `data_grid` | experimental | Data Grid |
| `data_table` | experimental | Data Table |
| `dl` *(CSS / utility)* | stable | - |
| `donut` | stable | Donut Chart component |
| `file_tree` | stable | File tree |
| `inline_counter` | stable | Inline counter |
| `latest_line` | stable | Latest line |
| `list_group` | stable | List component |
| `message_thread` | stable | Message Thread component |
| `metric_card` | stable | Metric grid/card |
| `metric_strip` | experimental | Dense workspace primitives |
| `model-card` *(CSS / utility)* | experimental | - |
| `params_table` | stable | Params table component |
| `playlist` | stable | Playlist component |
| `playlist_item` | stable | Playlist component |
| `post_card` | stable | Post Card component |
| `profile_header` | stable | Profile Header component |
| `resource-card` *(CSS / utility)* | experimental | - |
| `result_card` | experimental | Dense workspace primitives |
| `result_collection` | experimental | Dense workspace primitives |
| `stat` | stable | Stat component |
| `table` | stable | Table component |
| `table` | stable | Table component |
| `timeline` | stable | Timeline component |
| `tree_view` | stable | Tree view component |
| `trending_tag` | stable | Trending Tag component |
| `video_card` | stable | Video Card component |

## Feedback

_26 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `alert` | stable | Alert component |
| `badge` | stable | Badge component |
| `callout` | stable | Callout component |
| `confirm_dialog` | stable | Confirm dialog component |
| `counter-badge` *(CSS / utility)* | stable | - |
| `empty_panel_state` | stable | Empty panel state |
| `empty_state` | stable | Empty State component |
| `live_badge` | stable | Live Badge component |
| `load_sentinel` | stable | Streaming and AI components |
| `notification_dot` | stable | Notification Dot |
| `progress` *(CSS / utility)* | stable | - |
| `progress_bar` | stable | Progress Bar component |
| `result-slot` *(CSS / utility)* | experimental | - |
| `skeleton` | stable | Skeleton component |
| `spinner` | stable | Spinner component |
| `spinner-thinking` *(CSS / utility)* | experimental | - |
| `sse-retry` *(CSS / utility)* | experimental | - |
| `sse_status` | stable | SSE connection status and error recovery |
| `status_indicator` | stable | Status Indicator component |
| `streaming` *(CSS / utility)* | stable | - |
| `streaming-block` *(CSS / utility)* | stable | - |
| `streaming_bubble` | stable | Streaming and AI components |
| `suspense-group` *(CSS / utility)* | experimental | - |
| `toast` | stable | Toast component |
| `toast-container` *(CSS / utility)* | stable | - |
| `typing_indicator` | stable | Typing Indicator component |

## Interactive

_9 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `accordion` | stable | Accordion component |
| `carousel` | stable | Carousel component |
| `collapse` | stable | Collapse component |
| `command_palette` | stable | Command Palette component |
| `dnd_list` | stable | Drag-drop primitives |
| `infinite_scroll` | stable | Infinite Scroll component |
| `island_root` | stable | Framework-agnostic island mount wrappers |
| `reaction_pill` | stable | Reaction Pill component |
| `sortable_list` | stable | Sortable list macros |

## Overlay

_4 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `drawer` | stable | Drawer component |
| `hover_card` | experimental | Hover Card |
| `popover` | stable | Popover component |
| `tray` | stable | Tray (slide-out panel) |

## Content

_11 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `code` *(CSS / utility)* | stable | - |
| `code-block` *(CSS / utility)* | stable | - |
| `code-block-wrapper` *(CSS / utility)* | stable | - |
| `comment-thread` *(CSS / utility)* | stable | - |
| `install_snippet` | stable | Code macros |
| `item` | stable | Item |
| `label_overline` | stable | Small caps / overline label for cards and dense panels. |
| `logo` | stable | Logo component |
| `mention` | stable | Mention component |
| `message-reactions` *(CSS / utility)* | stable | - |
| `signature` | stable | Signature component |

## Typography

_30 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `display` *(CSS / utility)* | legacy | - |
| `font-2xl` *(CSS / utility)* | legacy | - |
| `font-base` *(CSS / utility)* | legacy | - |
| `font-lg` *(CSS / utility)* | legacy | - |
| `font-medium` *(CSS / utility)* | legacy | - |
| `font-mono` *(CSS / utility)* | legacy | - |
| `font-sm` *(CSS / utility)* | legacy | - |
| `font-xl` *(CSS / utility)* | legacy | - |
| `font-xs` *(CSS / utility)* | legacy | - |
| `measure-lg` *(CSS / utility)* | legacy | - |
| `measure-md` *(CSS / utility)* | legacy | - |
| `measure-sm` *(CSS / utility)* | legacy | - |
| `prose` *(CSS / utility)* | stable | - |
| `prose-lg` *(CSS / utility)* | legacy | - |
| `prose-sm` *(CSS / utility)* | legacy | - |
| `rendered_content` | stable | Rendered content |
| `tabular` *(CSS / utility)* | stable | - |
| `text-muted` *(CSS / utility)* | legacy | - |
| `ui-base` *(CSS / utility)* | legacy | - |
| `ui-bold` *(CSS / utility)* | legacy | - |
| `ui-label` *(CSS / utility)* | legacy | - |
| `ui-lg` *(CSS / utility)* | legacy | - |
| `ui-medium` *(CSS / utility)* | legacy | - |
| `ui-meta` *(CSS / utility)* | legacy | - |
| `ui-normal` *(CSS / utility)* | legacy | - |
| `ui-semibold` *(CSS / utility)* | legacy | - |
| `ui-sm` *(CSS / utility)* | legacy | - |
| `ui-title` *(CSS / utility)* | legacy | - |
| `ui-xl` *(CSS / utility)* | legacy | - |
| `ui-xs` *(CSS / utility)* | legacy | - |

## Marketing

_11 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `band` | experimental | Band component |
| `cta_band` | stable | CTA Band |
| `feature_section` | experimental | Feature Section component |
| `feature_stack` | experimental | Feature Section component |
| `lifecycle_showcase` | experimental | Marketing pattern assets |
| `logo_cloud` | stable | Logo Cloud |
| `site_footer` | experimental | Site Footer component |
| `site_header` | experimental | Site Header component |
| `site_nav_link` | experimental | Site Header component |
| `site_shell` | experimental | Site Shell component |
| `story_card` | stable | Story Card |

## Media

_6 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `catalog_rail` | experimental | Media pattern assets |
| `live_event_card` | experimental | Media pattern assets |
| `media_hero_shelf` | experimental | Media pattern assets |
| `title_card` | experimental | Media pattern assets |
| `video_thumbnail` | stable | Video Thumbnail component |
| `watch_companion_layout` | experimental | Media pattern assets |

## Social

_4 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `answer_card` | experimental | Forum and social pattern assets |
| `moderation_queue_item` | experimental | Forum and social pattern assets |
| `thread_reader_layout` | experimental | Thread reader layout |
| `topic_card` | experimental | Forum and social pattern assets |

## Effect

_46 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `ambient` *(CSS / utility)* | experimental | - |
| `ambient-root` *(CSS / utility)* | experimental | - |
| `animated_counter` | experimental | Animated Counter |
| `aura` | experimental | Aura — chromatic halo behind stacked content (glass surfaces, cards, etc.) |
| `aura_tone` *(CSS / utility)* | experimental | - |
| `aurora` | experimental | Aurora Background |
| `bento` *(CSS / utility)* | experimental | - |
| `bg-pattern` *(CSS / utility)* | experimental | - |
| `blade` *(CSS / utility)* | experimental | - |
| `border_beam` | experimental | Border Beam |
| `bounce-in` *(CSS / utility)* | experimental | - |
| `click-jello` *(CSS / utility)* | experimental | - |
| `click-wobble` *(CSS / utility)* | experimental | - |
| `confetti` | experimental | Confetti |
| `constellation` | experimental | Constellation |
| `dock` | experimental | Floating Dock |
| `glitch_text` | experimental | Glitch Text Effect |
| `glow_card` | experimental | Glow Card |
| `gradient_text` | experimental | Gradient Text |
| `grain` | experimental | Grain Overlay |
| `hero_effects` | experimental | Hero Effects |
| `holy_light` | experimental | Holy Light |
| `hover-jello` *(CSS / utility)* | experimental | - |
| `hover-rubber` *(CSS / utility)* | experimental | - |
| `hover-wobble` *(CSS / utility)* | experimental | - |
| `jello` *(CSS / utility)* | experimental | - |
| `marquee` | experimental | Marquee |
| `meteor` | experimental | Meteor Effect |
| `neon_text` | experimental | Neon Text |
| `number_ticker` | experimental | Number Ticker |
| `orbit` | experimental | Orbit |
| `particle_bg` | experimental | Particle Background |
| `pulsing_button` | experimental | Pulsing Button |
| `reveal_on_scroll` | experimental | Reveal on scroll — animate content when it enters the viewport |
| `ripple_button` | experimental | Ripple Button |
| `rubber-band` *(CSS / utility)* | experimental | - |
| `rune_field` | experimental | Rune Field |
| `scanline` | experimental | Scanline Overlay |
| `shimmer_button` | experimental | Shimmer Button |
| `sparkle` | experimental | Sparkle |
| `spotlight_card` | experimental | Spotlight Card |
| `symbol_rain` | experimental | Symbol Rain |
| `text_reveal` | experimental | Text Reveal |
| `texture` *(CSS / utility)* | experimental | - |
| `typewriter` | experimental | Typewriter Effect |
| `wobble` | experimental | Wobble / Jello / Rubber-band / Bounce-in |

## ASCII

_40 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `ascii` *(CSS / utility)* | experimental | - |
| `ascii_7seg` | stable | ASCII 7-Segment Display |
| `ascii_badge` | stable | ASCII Badge |
| `ascii_border` | stable | ASCII Border |
| `breaker_panel` | stable | ASCII Breaker Panel |
| `ascii_card` | stable | ASCII Card |
| `ascii_checkbox` | stable | ASCII Checkbox |
| `ascii-checkbox-group` *(CSS / utility)* | experimental | - |
| `ascii_divider` | stable | ASCII Divider |
| `ascii_empty` | stable | ASCII Empty State component |
| `ascii_error` | stable | ASCII Error Page |
| `ascii_fader` | stable | ASCII Fader / Slider |
| `ascii-fader-bank` *(CSS / utility)* | experimental | - |
| `ascii-fill` *(CSS / utility)* | experimental | - |
| `ascii-fill-hover` *(CSS / utility)* | experimental | - |
| `indicator` | stable | ASCII Indicator Light |
| `ascii-indicator-row` *(CSS / utility)* | experimental | - |
| `ascii_knob` | stable | ASCII Knob / Rotary Selector |
| `ascii_modal` | stable | ASCII Modal |
| `ascii-modal-trigger` *(CSS / utility)* | experimental | - |
| `ascii_progress` | stable | ASCII Progress |
| `ascii-radio` *(CSS / utility)* | experimental | - |
| `ascii_radio_group` | stable | ASCII Radio |
| `ascii_skeleton` | stable | ASCII Skeleton |
| `ascii_sparkline` | stable | ASCII Sparkline |
| `ascii_spinner` | stable | ASCII Spinner component |
| `ascii_stepper` | stable | ASCII Stepper |
| `ascii_switch` | stable | ASCII Toggle |
| `ascii_tab` | stable | ASCII Tabs |
| `ascii_table` | stable | ASCII Table |
| `ascii_tabs` | stable | ASCII Tabs |
| `ascii_ticker` | stable | ASCII Ticker |
| `tile_btn` | stable | ASCII Tile Button |
| `ascii-tile-grid` *(CSS / utility)* | experimental | - |
| `ascii_toggle` | stable | ASCII Toggle |
| `ascii_vu_meter` | stable | ASCII VU Meter |
| `ascii-vu-stack` *(CSS / utility)* | experimental | - |
| `split_flap` | stable | ASCII Split-Flap Display |
| `split-flap-board` *(CSS / utility)* | experimental | - |
| `split-flap-row` *(CSS / utility)* | experimental | - |

## Composite

_1 components._

| Macro | Maturity | Description |
|-------|----------|-------------|
| `resource_index` | stable | Resource Index composite |
<!-- chirpui:generated:end -->
