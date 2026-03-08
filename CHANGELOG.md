# Changelog

All notable changes to chirp-ui will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Alpine magics** — `$refs`, `$id`, `$dispatch`, `$nextTick` for dropdown focus management, unique ARIA IDs, and cross-component events
- **Custom events** — `chirpui:dropdown-selected`, `chirpui:tab-changed`, `chirpui:tray-closed`, `chirpui:modal-closed` for app-level handling (HTMX, analytics)
- **Dropdown accessibility** — Escape/click-outside with focus return; arrow-key navigation for dropdown_select; `x-ref` trigger/panel
- **docs/ALPINE-MAGICS.md** — Reference for magics and events

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
