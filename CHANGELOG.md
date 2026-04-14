# Changelog

All notable changes to chirp-ui are recorded here via [Towncrier](https://towncrier.readthedocs.io/) fragments in `changelog.d/`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [0.4.0] - 2026-04-13

### Added

- Packaged Bengal theme (`bengal_themes.chirp_theme`) with standalone CSS, templates, and assets — registered as `chirp-theme` entry point for Bengal's theme registry. ([#bengal-theme](https://github.com/lbliii/chirp-ui/issues/bengal-theme))
- Context-aware theming: `timeline`, `callout`, `status_indicator`, and `settings_row_list` now automatically adapt their visual treatment when nested inside `surface()` or `card()` containers via `--on-<surface>` CSS modifier classes. ([#context-aware-theming](https://github.com/lbliii/chirp-ui/issues/context-aware-theming))
- ComponentDescriptor coverage: added 101 new descriptors to `COMPONENTS` registry (199 total), plus a test gate ensuring every template has a descriptor or is explicitly excluded. ([#descriptor-coverage](https://github.com/lbliii/chirp-ui/issues/descriptor-coverage))
- New composite components: `install_snippet` (command + copy button), `filter_row` (lightweight inline filter form), `tag_browse` (tray + badges for tag-filtered listings), and `settings_row` (label + status badge + detail). ([#new-composites](https://github.com/lbliii/chirp-ui/issues/new-composites))
- Sharp-edges audit: normalized variant/size defaults to empty strings, added `hx={}` dict shorthand to `btn`/`icon_btn`/`form`, filled 53 missing CSS tokens, migrated `overflow: hidden` → `overflow: clip`, wrapped `localStorage` in try/catch, aligned test stubs with real filters (43 parity tests), and documented all 195 templates in `COMPONENT-OPTIONS.md`. ([#sharp-edges-audit](https://github.com/lbliii/chirp-ui/issues/sharp-edges-audit))
- 10 reusable SVG pattern tiles under `templates/patterns/` with matching `--chirpui-pattern-*` tokens and `.chirpui-texture` / `.chirpui-texture--*` overlay utilities.

  CSS-only gradient patterns: `--chirpui-bg-pattern-base` / `--chirpui-bg-pattern-ink` / `--chirpui-bg-pattern-ink-accent`, `.chirpui-bg-pattern--*` (dots, grid, diag, crosshatch, weave, accent-dots), `.chirpui-band` + `--pattern-dots` / `--pattern-grid`, full-page `.chirpui-ambient` + `.chirpui-ambient-root`, and `.chirpui-surface--noise-overlay` / `--static-overlay` for card grain and scan-line texture. ([#svg-pattern-tiles](https://github.com/lbliii/chirp-ui/issues/svg-pattern-tiles))
- Migrated 5 composite templates from double-nesting `{% slot %}` workaround to kida's `{% yield %}` directive: `layout.html`, `workspace_shell.html`, `file_tree.html`, `empty_panel_state.html`, `document_header.html`. ([#yield-migration](https://github.com/lbliii/chirp-ui/issues/yield-migration))
- Sharp-edges phase 2: renamed colliding macros (`segmented_control` → `segmented_control_field`, `tab` → `tab_button`), `bem()` now strips invalid modifiers, `contrast_text()` warns on unparseable colors, added `is_strict()`/`reset_colors()` APIs, added `--chirpui-z-*`/`--chirpui-anim-*` tokens and replaced 114 hardcoded CSS values with token references, expanded `STATUS_WORDS` to 25 entries, and guarded `tab_is_active()` against empty href. ([#sharp-edges-phase2](https://github.com/lbliii/chirp-ui/issues/sharp-edges-phase2))
- Sharp-edges phase 3: `btn()` defaults to `type="button"` (prevents accidental form submits), `inline_edit_field` warns on missing `swap_id` via `check_required_id()`, `build_hx_attrs()` validates attribute names against known htmx attrs, `field_errors()` warns and coerces non-list values, pagination disabled states use `<button disabled>` instead of `<span aria-disabled>`, avatar gains `decorative` mode, notification dot pluralizes aria-label, Alpine `register()` gets idempotency guard, store init checks existence before overwriting, `safeSetItem()` logs storage failures, and 44 `@provides`/`@consumes` annotations document every provide/consume contract inline. ([#sharp-edges-phase3](https://github.com/lbliii/chirp-ui/issues/sharp-edges-phase3))
- Sharp-edges phase 4: standardize slot naming across container components (`footer` param→slot in card, `actions` canonical in alert/empty/hero/profile_header with backward-compat aliases), rename `attrs` → `attrs_unsafe` across 37 macros with deprecation warning, promote `hx={}` dict in all macro docstrings and new `HTMX-PATTERNS.md` guide, refactor neumorphic CSS from 102 → 44 selectors via `@layer chirpui-theme` + gradient tokens + `:is()` consolidation, add `assert_element()` structural test helper with 29 new tests for top-20 components, and create `docs/INDEX.md` navigation index with consolidated `docs/LAYOUT.md`. ([#sharp-edges-phase4](https://github.com/lbliii/chirp-ui/issues/sharp-edges-phase4))

### Fixed

- Add global CSS reset (`box-sizing: border-box`, `body { margin: 0 }`), fix `vh` → `dvh` on modals/drawers/dropdowns for mobile, add `:focus-visible` to tabs/accordion/collapse/segmented, fix neumorphic dark-mode shadow visibility, fix confetti layout thrash, raise toast z-index above sticky headers, add `@supports` guard on site-header glass, add scroll-anchor support for sticky navbar/site-header, and prefer `Alpine.safeData` for htmx compatibility. ([#css-hardening](https://github.com/lbliii/chirp-ui/issues/css-hardening))
- Added missing `chirpui-font-medium` CSS utility (font-weight: 500), used by `settings_row` and `config_row` templates. ([#font-medium-utility](https://github.com/lbliii/chirp-ui/issues/font-medium-utility))
- Muted color-mix tokens (`--chirpui-*-muted`) now derive from `var(--chirpui-surface)` instead of bare `white`, fixing near-white backgrounds in dark mode. ([#muted-dark-mode](https://github.com/lbliii/chirp-ui/issues/muted-dark-mode))
- Tray overlay now includes static `aria-hidden="true"` for pre-Alpine hydration, preventing screen readers from seeing closed tray content during the hydration gap. ([#tray-aria-hidden](https://github.com/lbliii/chirp-ui/issues/tray-aria-hidden))


## [0.3.0] — 2026-04-10

### Added

- **kida 0.4.0 adoption** — Native error boundaries (`{% try %}`/`{% fallback %}`), list comprehensions, scoped slots (`let:`), and opt-in partial evaluator. Error boundaries added to `suspense_slot`, `oob_fragment`, `streaming_bubble`, `streaming_block`, and `safe_region`/`fragment_island` — render errors now fall back gracefully instead of crashing the page. Layout primitives refactored from nested ternary chains to list comprehensions for readability
- **Elevated design layer** — Display type scale (`prose-6xl`/`prose-7xl` up to 74px, `.chirpui-display`), gradient text `--secondary` and `--rainbow` variants, 5-layer `shadow-deep` token with `surface--deep` and `inset-glow` modifiers, `divider--dotted` and `divider--fade` patterns, `grain--dot` CSS-only texture, and `surface--cornered` corner-bracket card accents
- **Provide/consume expansion** — `surface`/`panel` provide `_surface_variant`, `card` provides `_card_variant`, `accordion` provides `_accordion_name` (items auto-inherit), `form` gains `density` param providing `_form_density` to fields (new `chirpui-field--dense` CSS), `sidebar`/`navbar` gain `current_path` param providing `_nav_current_path` to links. Full key registry in `docs/PROVIDE-CONSUME-KEYS.md`
- **ASCII component maturity** — 3 new composites (`ascii_card`, `ascii_tabs`, `ascii_modal`), 152 render tests for all 27 ASCII components, a11y improvements (fader upgraded to `type="range"`, VU meter gains `role="meter"`), and ASCII component documentation page
- **Streaming & SSE maturity** — Streaming state variants (`thinking`, `error`) for `streaming_bubble`, 3 provide/consume context keys (`_streaming_role`, `_sse_state`, `_suspense_busy`), role-aware aria-labels, 45 new tests, and 11 CSS rules closing all forward gaps
- **Behavior layer hardening** — Wire all 7 orphaned provide/consume keys to natural consumers (badge, alert, divider, button, icon_btn, copy_button) with 30 contract tests. Harden error boundary with message display, retry button, and telemetry event
- **Island system documentation** — Site docs for architecture, foundation API, all 7 built-in primitives, fragment islands, event protocol, and custom primitive authoring guide
- **JS unit test infrastructure** — 115 vitest tests covering all 9 island helpers (action_queue, counter, draft_store, error_boundary, foundation, grid_state, state_sync, upload_state, wizard_state)
- **Component render tests** — 33 new render tests for previously untested components
- **Playwright browser tests** — 23 tests for 8 Alpine components (command_palette, drawer, tray, toast, copy_button, theme_toggle, split_panel, streaming_bubble)

### Fixed

- **Color system gamma bug** — `_linear_to_srgb` divided instead of multiplied by 12.92, producing 166x too-dark values for near-black OKLch colors. Widened `sanitize_color` to accept modern CSS (negative hue, `oklcha()`, `lab()`/`lch()`, leading-dot decimals, `none` keyword, unit suffixes) while keeping injection blocked. Added 80+ color pipeline tests
- **`contrast_text()` color formats** — Now handles `rgb()`, `hsl()`, and `oklch()` formats instead of silently falling back to white for non-hex colors

### Changed

- **kida-templates >= 0.4.0** — Bumped minimum dependency for error boundaries, scoped slots, and list comprehensions

[0.3.0]: https://github.com/lbliii/chirp-ui/releases/tag/v0.3.0

## [0.2.6] — 2026-04-09

### Added

- **`provide`/`consume` context flow** — Adopt kida 0.3.4's parent-to-child render context for slot-boundary state passing
- **Table row auto-alignment** — `row()` inside `table(align=...)` inherits column alignment automatically via `provide`/`consume`; `aligned_row()` is soft-deprecated
- **Hero variant broadcast** — Effect macros (`particle_bg`, `meteor`, `spotlight_card`, `symbol_rain`, `holy_light`, `rune_field`, `constellation`) consume variant from parent `hero_effects()` when no explicit variant is passed
- **Bar surface context** — `command_bar` and `filter_bar` provide `_bar_surface` and `_bar_density` to slot children

### Changed

- **kida-templates ≥ 0.3.4** — Bumped minimum dependency for `provide`/`consume` support and Markup-aware `~` operator fix

### Fixed

- **Table alignment footgun** — Data-driven `rows=` parameter flows alignment to all cells automatically (#36)
- **Donut label semantics** — Renamed `label=` to `text=`, added `caption=` for secondary text; `label=` kept as backward-compatible alias (#36)

### Deprecated

- **`aligned_row()`** — Use `row()` inside `table(align=...)` instead; will be removed in 0.3.0

[0.2.6]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.6

## [0.2.5] — 2026-04-03

### Changed

- **O(1) color lookup** — `resolve_color` now uses a dict instead of linear scan; `icon` filter caches sorted icon list after first call

### Added

- **Shell tabs contract** — `docs/SHELL-TABS-CONTRACT.md` documenting shell-region tab ownership rules; `route_tabs` accepts dict-shape `tab_items`
- **Alpine.js troubleshooting guide** — CLAUDE.md section for diagnosing dead interactive components (missing Alpine script, CDN URL issues)

[0.2.5]: https://github.com/lbliii/chirp-ui/releases/tag/v0.2.5

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
