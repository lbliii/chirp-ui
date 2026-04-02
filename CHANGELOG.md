# Changelog

All notable changes to chirp-ui will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.4] — 2026-04-01

### Fixed

- **Pre-hydration safety** — Render `modal_overlay` and `tray` with static `--closed` class so they don't block clicks before Alpine hydrates
- **x-cloak on interactive elements** — Add `x-cloak` to `dropdown_select`, `dropdown_split`, and all "Copied!" spans to prevent flash of unstyled content
- **HTMX correctness for nav_link** — Add `hx-select="#page-content"` to `nav_link` for proper fragment targeting
- **Inline edit cancel** — Add `hx-boost="false"` and `hx-select="unset"` to inline edit cancel link

[0.2.4]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.4

## [0.2.3] — 2026-03-30

### Fixed

- **Alpine stores for modals/trays** — Register `Alpine.store("modals")` and `Alpine.store("trays")` in both `app_shell` and `app_shell_layout` so modal/tray components work on first page load without requiring Chirp to pre-register stores

[0.2.3]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.3

## [0.2.2] — 2026-03-30

### Added

- **Boost-aware macros** — `tabs`, `route_tabs`, and `button` emit `hx-boost="false"` on `<a>` elements when `hx_target` is set, preventing boost from hijacking clicks
- **Safe-by-default forms** — `form()` auto-adds `hx-select="unset"` and `hx-disinherit="hx-select"` when htmx is detected; explicit `hx_select` overrides the default
- **Browser test suite** — Playwright-based integration tests covering Alpine lifecycle, boosted navigation, dropdowns, fill mode, fragment forms, inline edit, modals, and tabs
- **Chirp integration tests** — `test_chirp_integration.py` for `use_chirp_ui()` registration and Alpine injection

### Changed

- **Dependency bumps** — `kida-templates>=0.3.0` (was >=0.2.8), `bengal-chirp>=0.2.0` for showcase/browser groups
- **CI** — `--maxfail=5` added to test gate job for early failure

[0.2.2]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.2

## [0.2.1] — 2026-03-23

### Added

- **Color filters** — `register_colors`, `resolve_color`, `sanitize_color`, and `contrast_text` for semantic palette names (e.g. faceted chips and badges); call `register_colors` once when using named colors with `filter_chips` / `badge`
- **filter_chips** — Faceted filter row component with optional semantic colors
- **label_overline** — Small-caps section labels inside cards
- **Layout & shell** — `chat_layout`, `document_header`, `empty_panel_state`, `file_tree`, `panel`, `split_layout`, `workspace_shell`
- **Docs** — `TRANSITIONS.md`, `UI-LAYERS.md`, layout guides (`LAYOUT-OVERFLOW`, `LAYOUT-PRESETS`, `LAYOUT-GRIDS-AND-FRAMES`, `LAYOUT-VERTICAL`), `COMPOSITION.md`, and DND-FRAGMENT-ISLAND / COMPONENT-OPTIONS updates
- **CI** — GitHub Actions workflow to publish the docs site to GitHub Pages

### Changed

- **Theme & motion** — Expanded `chirpui.css` and `chirpui-transitions.css` (tokens, surfaces, shell overflow, transition tokens)
- **App shell** — Refined `app_shell_layout`, `sidebar`, `navbar`, `shell_actions`, and related components for regions and overflow
- **Showcase** — Component showcase and static showcase expanded (e.g. chrome, dashboard, effects, typography, buttons, ASCII primitives)

### Fixed

- Template and showcase fixes from design-system sync (layout, islands, forms)

[0.2.1]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.1

## [0.2.0] — 2026-03-18

### Added

- **ASCII components** — 20+ new ASCII-art UI primitives: `ascii_7seg`, `ascii_badge`, `ascii_border`, `ascii_breaker_panel`, `ascii_checkbox`, `ascii_divider`, `ascii_empty`, `ascii_error`, `ascii_fader`, `ascii_indicator`, `ascii_knob`, `ascii_progress`, `ascii_radio`, `ascii_skeleton`, `ascii_sparkline`, `ascii_spinner`, `ascii_split_flap`, `ascii_stepper`, `ascii_table`, `ascii_ticker`, `ascii_tile_btn`, `ascii_toggle`, `ascii_vu_meter`
- **Background effects** — `constellation`, `holy_light`, `rune_field`, `symbol_rain` — CSS-only animated backgrounds
- **Gradient effects** — Blade sections and gradient hero effects
- **Expanded showcase** — Static showcase with cards, sections, shell actions, and full component gallery

### Changed

- **Token naming** — Improved CSS custom property naming for theme tokens
- **Component updates** — Refined `config_row`, `settings_row`, `description_list`, `table`, and `hero_effects` templates

[0.2.0]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.0

## [0.1.6] — 2026-03-12

### Added

- **route_tabs** — Route-family tab components: `render_route_tabs`, `route_tabs` macros; `tabbed_page_layout` for route-backed pages with `tab_items` and `current_path`
- **tab_is_active** — Template global (registered when Chirp has `template_global`); supports `exact`/`prefix` match for tab hrefs
- **value_type** filter — Infer type from value (bool, number, str, path, etc.); added to filters `__all__`
- **description_list** — Auto-detect item type via `value_type` when `item.type` is missing
- **chirpui.css** — Route tab styles
- **Docs** — PLAN-primitives-and-components, PLAN-route-tabs-and-tabbed-layout; app-shell golden path (tabbed_page_layout); type-aware-rendering; DND-FRAGMENT-ISLAND updates

### Changed

- **register_filters** — Registers `value_type` and `tab_is_active` (template global when available)

### Fixed

- **B009** — Replace `getattr(app, "template_global")` with `app.template_global` (ruff)

[0.1.6]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.6

## [0.1.5] — 2026-03-10

### Added

- **SECURITY.md** — `| safe` usage audit, `html_attrs` filter behavior (mapping vs raw string), XSS vector tests in `test_filters.py`
- **docs/ANTI-FOOTGUNS.md** — Common pitfalls: fragment island target matching, Alpine `x-data` placement, registration order, static path, CSRF, `attrs_map` over `attrs`
- **docs/COMPONENT-OPTIONS.md** — JavaScript Dependencies section (Alpine.js, chirpui.js) and static path guidance
- **README** — Version compatibility table, stability notes, SECURITY.md link
- **filters `__all__`** — Public API surface: `bem`, `field_errors`, `html_attrs`, `icon`, `validate_size`, `validate_variant`, `validate_variant_block`
- **Test env** — `validate_variant_block` and `validate_size` stubs for Chirp/chirp-ui filter parity
- **Template CSS contract** — Dynamic BEM modifiers (btn, modal, dropdown, star-rating, thumbs, segmented) verified against CSS

### Changed

- **config_row** — Template tweaks
- **DASHBOARD-MATURITY-CONTRACT** — Phase 1 marked complete ✓ (hardening)

### Fixed

- **Filter edge cases** — `html_attrs` (None, False, nested dict, special chars), `bem` (empty variant/modifier), `validate_variant` (empty allowed list), `field_errors` (nested dict, non-dict input)

[0.1.5]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.5

## [0.1.4] — 2026-03-10

### Added

- **fragment_island_with_result** — Macro that renders a co-located mutation result div at the top of the island. Use when forms inside HTMX-loaded content target a result div; guarantees target and form are in the same DOM subtree.
- **resource_index mutation_result_id** — Optional param to render a mutation result div at the start of the results block. Ensures target is co-located with HTMX-loaded content that contains mutating forms.
- **Anti-footgun docs** — DND-FRAGMENT-ISLAND.md: "Target must be co-located with form" guidance. COMPONENT-OPTIONS.md: mutation targets note for resource_index.

[0.1.4]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.4

## [0.1.3] — 2026-03-09

### Added

- **Alpine magics** — `$refs`, `$id`, `$dispatch`, `$nextTick` for dropdown focus management, unique ARIA IDs, and cross-component events
- **Custom events** — `chirpui:dropdown-selected`, `chirpui:tab-changed`, `chirpui:tray-closed`, `chirpui:modal-closed` for app-level handling (HTMX, analytics)
- **Dropdown accessibility** — Escape/click-outside with focus return; arrow-key navigation for dropdown_select; `x-ref` trigger/panel
- **docs/ALPINE-MAGICS.md** — Reference for magics and events

[0.1.3]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.3

## [0.1.2] — 2026-03-06

### Fixed

- **RUF001** — Replace ambiguous Unicode in icons and tests: `＋` (FULLWIDTH PLUS SIGN) → `+`, `×` (MULTIPLICATION SIGN) → `x` in test strings

[0.1.2]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.2

## [0.1.1] — 2026-03-04

### Added

- **Form components** — `star_rating` (CSS-only star picker with hover preview, sm/lg sizes), `thumbs_up_down` (binary sentiment), `segmented_control` (connected radio button group), `number_scale` (NPS-style horizontal numbered radio with endpoint labels)
- **Data display** — `sortable_list` (drag-to-reorder with handle, remove button, drag states), `bar_chart`, `donut`, `dropdown_menu`
- **Layout & shell** — `app_shell`, `app_shell_layout`, `action_strip`, `filter_bar`, `search_header`, `selection_bar`, `tray`, `modal_overlay`
- **Docs components** — `config_card`, `config_dashboard`, `index_card`, `nav_tree`, `params_table`, `signature`, `logo`, `command_bar`, `command_palette`
- **code_block** — `copy=true` param for copy-to-clipboard with hover-reveal button and "Copied!" feedback
- **Typography** — `--chirpui-ui-*` and `--chirpui-prose-*` tokens; utility classes (`.chirpui-ui-xs`, `.chirpui-ui-label`, etc.); page-header and section-header typography rules
- **CSS utilities** — `.chirpui-card--link`, `.chirpui-flow` (badge/tag rows), `.chirpui-grid--auto-fill`
- **theme_toggle** — Manual light/dark theme switch component
- **chirpui.js** — Client-side utilities (copy, clipboard, etc.)
- **validation.py** — Strict mode for component option validation
- **Documentation** — `COMPONENT-OPTIONS.md` (variant/size reference, strict mode), `TOKENS.md`, `TYPOGRAPHY.md`; macro slot context section (slot content inherits caller context)
- **Tests** — Component tests, CSS syntax validation, template–CSS contract checks, transition token checks

### Changed

- **streaming_block** — Pass slot content to block when `sse_streaming=true`
- **Ruff** — Format applied to test files; lint rules updated

### Fixed

- **Form macros** — `attrs` param now marked safe; fixes double-quote escaping that broke HTMX selectors (e.g. `hx-target`, `hx-post`)

[0.1.1]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.1

## [0.1.0] — 2026-02-10

### Added

- Initial release — Reusable Kida component library for Chirp
- Layout, UI, forms, data display, docs, streaming, and theming components
- htmx-native, zero JavaScript, composable via `{% slot %}`

[0.1.0]: https://github.com/lbliii/chirp-ui/releases/tag/v0.1.0
