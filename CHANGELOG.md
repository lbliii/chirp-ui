# Changelog

All notable changes to chirp-ui are recorded here via [Towncrier](https://towncrier.readthedocs.io/) fragments in `changelog.d/`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [0.11.3] - 2026-07-13

### Changed

- Bump minimum stack dependencies to Kida 0.11, Chirp 0.10, and Pounce 0.8.2; add `poe template-check` strict Kida verification (wired into `poe ci` / `poe check`) and `app.check()` contract proofs for the upgraded Chirp integration (#373, #380–#390).
- Document combobox typeahead anatomy, dropdown-select boundary, and disabled-option gauntlet proof (#341).
- Document navigation menu flyout anatomy and browser gauntlet proof (#336).
- Make Bengal chirp-theme print/PDF output a fully verified reading surface: clean printed URLs and source provenance, adaptive pagination for long authored blocks, tagged PDF structure and outlines, grayscale and background-off scenarios, Poppler semantic/raster checks, and downloadable CI proof artifacts.
- Promote hover-card to stable with anatomy doc and browser gauntlet proof (#338).
- Promoted `context-menu`, `menubar`, and `input-otp` to stable after shipped anatomy docs, browser gauntlets, and stabilization Current Slice proof for Wave 1 contract hardening (#335, #337, #339).

### Fixed

- Include `itsdangerous` in the component-showcase extra so Chirp can import its session middleware during application startup.


## [0.11.2] - 2026-07-13

### Fixed

- Make dark-mode Bengal pages print with a white paper palette, high-contrast body and syntax text, readable table and code sizes, compact lists, and no single-item list tails stranded on a final page.


## [0.11.1] - 2026-07-13

### Fixed

- Make Bengal chirp-theme PDF exports preserve every tab and disclosure body, label non-printable interactive embeds, restore interactive state after printing, use wide paper sizes effectively, and keep related content together across page breaks.


## [0.11.0] - 2026-06-23

### Added

- **AI chat UI** — `composer()` (Enter-to-send, attachments, suggestions),
  message-turn layouts (actions, reasoning, tool calls, citations),
  streaming via `prose()` and server-sent events, and model settings via
  `config_form()` / `param_override`. See `docs/patterns/ai-chat.md` and
  `docs/patterns/sse-events.md`.
- **Showcase tooling** — manifest-backed blocks gallery at `/blocks`, live theme
  explorer with preset switching ([#213](https://github.com/lbliii/chirp-ui/issues/213)),
  golden-screen and shell-recipe registry sections, a `chirp-ui` console script,
  and an optional MCP server (`chirp-ui mcp`) with `find_components`,
  `get_component`, and `list_categories`. Closes
  [#211](https://github.com/lbliii/chirp-ui/issues/211) and
  [#212](https://github.com/lbliii/chirp-ui/issues/212).
- **New components** — focus-managed popover/dropdown, `input_otp`, `hover_card`,
  `menubar`, and `navigation_menu`
  ([#202](https://github.com/lbliii/chirp-ui/issues/202)).
- **Visual polish** — warmer default colors and hero gradients, toast
  stacking/swipe, tabular numbers, sliding route-tab pill, compact/dense density
  modes, and `fab()` / `command_palette_fab()` floating action buttons.
- **Smaller CSS bundles** — `css_subset` and `build_chirpui_css.py --components`
  ship only the component partials you use.
- **Lucky Cat golden screen** — `data-dense-market` layout archetype at
  `/screen-lucky-cat-market`, with fixture data and docs
  ([#262](https://github.com/lbliii/chirp-ui/issues/262)).
- **`Column` sizing** — optional `width`, `mobile_width`, and `resizable` for
  richer data grid layouts.
- **Docs site** — data-driven YAML resume page, CSP guide for Alpine inline
  expressions, and Bengal theme now loads Alpine correctly for interactive
  chirp-ui macros.
- **Graph explorer page** — vendored `bengal-graph-explorer.js` for the new
  `/graph/` route (Bengal 0.5.1).

### Changed

- **Responsive cards** — `card` and `surface` reflow inside narrow columns (like
  the context rail) without waiting for a viewport breakpoint
  ([#209](https://github.com/lbliii/chirp-ui/issues/209)).
- **Resizable sidebar** — drag to any width, with persistence and keyboard
  control ([#219](https://github.com/lbliii/chirp-ui/issues/219)).
- **Drawer, tray, and split-panel** — pointer and keyboard resize,
  swipe-to-dismiss, and optional `persist_open` for boosted navigation
  ([#198](https://github.com/lbliii/chirp-ui/issues/198)).
- **Docs site navigation** — unified global side rail and top bar, centered doc
  catalog rail, Layouts/Dev section hubs, redesigned releases index, and live
  showcase links throughout.
- **Docs site polish** — compact notebook layout, blog hero typography fix, API
  symbol card grids, and link hover previews.
- **Alpine runtime check** — removed a stale internal TODO now that Chirp
  wiring is complete ([#191](https://github.com/lbliii/chirp-ui/issues/191)).

### Removed

- Bengal docs theme: legacy default-Bengal CSS (breadcrumbs, pagination, section
  headers, loading spinner) replaced by chirp-ui primitives.

### Fixed

- **Accessibility** — default accent colors now meet WCAG AA contrast; deeply
  nested docs sidebar folders highlight consistently, including the folder
  containing the current page.
- **Security (CSP)** — shell inline scripts and HTMX swaps work with Chirp 0.8+
  CSP nonces; island adapters mount correctly on fresh page loads.
- **Composer and streaming** — Enter-to-send under htmx 2, showcase
  abort/dismiss errors, unified demo SSE wiring, and streaming lifecycle cleanup.
- **Layout nits** — story cards no longer show empty slots, toggle-group items
  don't collide, table action buttons stay on one row, and list item trailing
  content aligns correctly.
- **Showcase** — blocks gallery previews render correctly; missing icons
  registered (`plus`, `send`, `stop`, `file`, `x`, `info`).
- **Docs theme** — doc-page hero Actions menu moved to top-right; page-nav
  tokens renamed from `--chirp-theme-*` to `--chirpui-*`.
- **CSS build** — confirmed `@scope` rules survive production minification
  ([#247](https://github.com/lbliii/chirp-ui/issues/247)).


## [0.10.0] - 2026-06-15

### Added

- Added **`data_grid`** — a server-driven interactive data grid composite
  (`chirpui/data_grid.html`) backed by a new typed Python state helper
  **`chirp_ui.grid_state`** (Chirp-agnostic, stdlib + dataclasses, in the
  `route_tabs.py` mold). The helper exposes `Column`, `GridSort`, `ColumnSort`,
  `SelectionState`, and the plain functions `parse_sort`, `sort_columns`,
  `selection_state`, `column_aria_sort`, `sort_query` (exported from
  `chirp_ui.__all__` and registered as Kida template globals).

  `sort_columns(...)` projects each column into a `ColumnSort` carrying the
  `aria_sort` value and the fully-built toggle `next_url` the macro renders **but
  never computes**, so the server's `ORDER BY` and the rendered headers cannot
  drift. The grid ships sortable columns (real `<button class="chirpui-table__sort">`
  in a `<th aria-sort=…>`, single-sort invariant, stable sort key — never
  `header|lower`, focus retained on the activated button after the swap), row
  selection bound to a controlled `selection_bar` via one idempotent
  `chirpuiGridSelection` Alpine factory (page-scoped select-all with the
  JS-property `indeterminate` state, live `aria-live` count, server-seeded so it is
  correct with JavaScript off). The factory re-seeds from server-checked rows after
  **every** swap — including the load-more `beforeend` append, via a scoped
  `htmx:afterSettle` listener registered in `init()` — so select-all then load-more
  correctly drops select-all to *indeterminate* (only the original page is selected
  of the now-larger set) and a server-checked appended row is re-adopted (WCAG
  4.1.2). Each row checkbox's accessible name comes from an optional `row_labels`
  list (clean plain text) and **never** the rendered first cell (which may be rich
  HTML or an empty spacer) — it falls back to the stable row id, so every label
  stays distinct and screen-reader-clean. Sticky header + opt-in sticky first
  column are pure `position: sticky` with token-driven z-index (incl. a top-left
  corner override) and a directional **seam shadow** (`color-mix` over
  `--chirpui-border`) so scrolled content visibly slides under the pin. v1 pins the
  first **visual** column (no per-column `Column(frozen=…)` — deliberately not
  shipped rather than advertise a no-op). HTMX load-more uses the `data_grid_rows`
  fragment (`beforeend`). The previously-orphaned `.chirpui-table__sort` CSS hook is
  finally emitted. `table()` gained additive
  `selectable` / `select_name` / `selection` / `row_id` / `sticky_first_col`
  params (defaults off = byte-identical; the legacy `sortable=`/`sort_url=`
  `header|lower` path is unchanged and documented as legacy). `selection_bar()`
  gained an additive `controlled=` mode. Proven by `tests/test_grid_state.py`,
  `tests/test_components.py`, `tests/js/grid_selection.test.js`, and the
  `tests/browser/test_data_grid_gauntlet.py` a11y gauntlet (single-active
  aria-sort, focusable sort button, focus retention, three-state select-all,
  sticky pinning, load-more without duplicate ids, axe-clean). Differentiator vs
  TanStack: Python/HTMX-native — the server owns the sort and selection state;
  load-more replaces client virtualization. Cross-page "select all N matching" is
  out of scope for v1. See `docs/patterns/data-grid.md` and
  `docs/COMPONENT-OPTIONS.md § Data Grid`
  ([#200](https://github.com/lbliii/chirp-ui/issues/200)).
- Added Docs/API/Releases/All scope chips to the Cmd+K search modal so results can be narrowed in place, reusing the same API/release predicates that drive result grouping and ranking; styled the chips to mirror the /search filter affordance and reset the scope to All when the modal closes. Gave the JS-disabled /search page a styled server-side fallback that lists every indexed page grouped by section, guarded by a kida render test that renders the real search.html noscript fragment. Authored Playwright proofs that the preload modes are honored (smart/lazy issue zero index fetches on a cold page; hover, focus, and Cmd+K each warm the index once before the modal opens; immediate warms once after idle) and that the search combobox wires aria-activedescendant to the active option id on both the modal and the /search page, clearing it on close and returning focus to the trigger.
- Added `combobox` — a typeahead autocomplete input following the WAI-ARIA combobox pattern. A `role="combobox"` text input filters a `role="listbox"` of server-rendered options as you type (client-side substring match); ArrowDown/ArrowUp rove the visible options via `aria-activedescendant` (the active option carries `aria-selected="true"`), Enter selects the active option, and Escape / click-outside close the list. Selecting fills the visible input with the option label, writes the option value to a hidden input submitted under `name`, and dispatches `chirpui:combobox-selected` `{value, label}`. Options are server-rendered, so the field degrades to a plain text input with JavaScript off. Behaviour lives in the idempotent `chirpuiCombobox` Alpine factory. Ships experimental with a keyboard/a11y browser gauntlet ([#201](https://github.com/lbliii/chirp-ui/issues/201)).
- Added `context_menu` — a right-click / keyboard context menu anchored at the pointer. Wrap any non-interactive region in `context_menu(items=[...])`; right-clicking (or the ContextMenu key / Shift+F10 / Enter on the focused region) opens a `role="menu"` panel at the cursor with full keyboard support: roving tabindex via ArrowUp/Down/Home/End, Enter/Space to activate, Escape to close and return focus, click-outside dismissal, and viewport clamping. Items accept `action`/`href`, an icon, `disabled` (focusable-but-inert per WAI-ARIA), and `default`/`danger`/`muted` variants; selecting one dispatches `chirpui:context-menu-selected` with `{label, action?, href?}`. Behaviour lives in the idempotent `chirpuiContextMenu` Alpine factory. Ships experimental with a keyboard/a11y browser gauntlet ([#202](https://github.com/lbliii/chirp-ui/issues/202)).
- Added `date_picker` — a date and date-range form control. A readonly display input opens a `role="dialog"` calendar popover with a `role="grid"` of `role="gridcell"` day buttons; the canonical value is an ISO `YYYY-MM-DD` string in a hidden input (range mode adds a second hidden input under `end_name`, default `{name}_end`). The calendar is fully client-rendered, so month navigation has no server round-trip. Keyboard: roving tabindex with Arrow (Left/Right ±1, Up/Down ±7), Home/End (week), PageUp/PageDown (month), Enter/Space to pick, Escape to close and return focus; focus movement clamps into `[min, max]` so it never strands on a disabled day. `min`/`max` (ISO) disable out-of-range days, today is marked with `aria-current`, and day names announce selection/range/today state. Range mode highlights the span and orders endpoints regardless of click order. Behaviour lives in the `chirpuiDatePicker` Alpine factory. Ships experimental with a keyboard/range/min-max/axe browser gauntlet; v1 is Sunday-first, English labels (localization is a follow-up) ([#201](https://github.com/lbliii/chirp-ui/issues/201)).
- Added a **route-context rail** region to `app_shell` (`context_rail=true` + a
  `context_rail` slot on the macro; a `context_rail` flag + `{% block context_rail %}`
  on `app_shell_layout.html`). It renders an optional trailing-edge secondary region
  (`<aside id="chirpui-context-rail">`, a labelled `complementary` landmark) for an
  inspector/detail panel that updates with the current route. The update protocol
  mirrors shell actions: a route response includes an out-of-band fragment targeting
  the outlet — use the new `context_rail_oob()` helper in `chirpui/oob.html`. Works
  standalone with htmx OOB; under Chirp, boosted navigation carries the rail fragment
  in the same response. Responsive: the rail stacks under main below 72rem and joins
  the single column below 48rem. Width is `--chirpui-context-rail-width` (default
  20rem); `context_rail_variant="muted"` tints the surface. This is the one blessed
  shell-region composite per the [Application Chrome Posture ADR](docs/decisions/application-chrome-posture.md)
  ([#195](https://github.com/lbliii/chirp-ui/issues/195)).
- Added a `make pre-pr` / `poe pre-pr` gate (full `poe ci` + a docs-chrome browser/a11y smoke covering folder-toggle, landmark, and axe proofs) and a non-required CI `browser-smoke` job, since `poe ci` intentionally does not run the Playwright suite.
- Added a client-side Alpine runtime self-check to `chirpui-alpine.js`: when
  chirp-ui components that require Alpine render but Alpine never initializes (a missing,
  blocked, or misconfigured CDN script; a CSP block; a network error; or
  `alpine=False`), the runtime now logs a loud `console.warn` with the likely
  causes instead of leaving every interactive component silently inert. The
  end-to-end Alpine-liveness proof (`tests/browser/test_alpine_lifecycle.py`,
  including the new silent-disable case) is now wired into the
  `test-browser-chrome` gate, and a Vitest unit test covers the self-check logic
  in the fast `poe ci` suite ([#189](https://github.com/lbliii/chirp-ui/issues/189), [#190](https://github.com/lbliii/chirp-ui/issues/190)).
- Added a complete, manifest-driven on-site component index at `site/content/docs/components/all.md` that lists every public Chirp UI macro grouped by category with its one-line description, generated by `scripts/build_component_index.py` (with a `build-component-index-check` poe task wired into `verify-generated` and `make release-preflight`) and guarded by `tests/docs_contracts/test_onsite_component_coverage.py`, so all public components are discoverable on-site without leaving for GitHub or running a local app, and the catalog can never silently drift behind the registry.
- Added a multi-select (token-pill) mode to `combobox` (`multiple=true`). Selecting an option adds a removable pill, keeps the list open, and clears the query; each selected value submits as a repeated hidden `name` input. Backspace on the empty input removes the last pill, the per-pill remove button removes a specific one, and already-selected options drop out of the list. The control wraps the pills and a borderless flexing input. Single-select is unchanged. Multi-select requires JavaScript (pills/values are Alpine-managed); v1 starts empty. Proven by the combobox browser gauntlet (pills, hidden-input submission, remove, Backspace, axe) ([#201](https://github.com/lbliii/chirp-ui/issues/201)).
- Added a scoped AGENTS.md steward network with audit and SME-question records so
  agent work loads local domain invariants, review hooks, and verification
  expectations at major repository boundaries.
- Added an **`id_suffix`** parameter to `shell_actions_bar()` and `shell_action()`
  (`chirpui/shell_actions.html`). Passing e.g. `id_suffix="-drawer"` namespaces the
  overflow dropdown id and each menu-action id, so the same actions bar can render
  in two regions at once (a topbar copy plus a mobile-drawer copy) without colliding
  duplicate element ids. `shell_actions_bar` threads the suffix down into each
  `shell_action`. The default `""` preserves the canonical ids, keeping every
  single-instance render byte-identical
  ([#224](https://github.com/lbliii/chirp-ui/issues/224)).
- Added an always-available **`topbar_leading`** zone to both shell entry points
  (a `topbar_leading` slot on the `app_shell()` macro; a `{% block topbar_leading %}`
  on `app_shell_layout.html`). It renders a **non-anchor** leading region before the
  brand — the correct home for a hamburger / back / command affordance. Interactive
  controls belong here, never in the `brand` slot/block (which nests inside the
  brand `<a>`, producing invalid HTML and hijacking the click). The built-in
  `nav_drawer` hamburger and the layout's collapsible `sidebar_toggle` render in the
  same wrapper. See `docs/patterns/navigation.md § Leading affordance`
  ([#220](https://github.com/lbliii/chirp-ui/issues/220)).
- Added an opt-in **mobile nav drawer** to `app_shell` (`nav_drawer=true` on the
  macro; `nav_drawer=True` in the render context for `app_shell_layout.html`).
  Below the 48rem breakpoint a topbar hamburger opens the sidebar as an accessible
  off-canvas slide-over, and — with `context_rail=true` — a second trigger opens
  the rail. It is a thin, additive affordance over the existing regions: the same
  sidebar/rail `<aside>` is repositioned (no duplicated nav), so `aria-current`,
  `syncNav`, and OOB swaps keep working; unset, the shell is byte-for-byte
  unchanged (the horizontal-strip fallback). The open/close behavior — focus trap,
  `Esc`, scrim dismiss, body scroll-lock, focus return, link-dismiss, and
  auto-close when the viewport grows past the breakpoint — is vanilla JS in
  `shell_runtime_script()` with **no Alpine dependency** ("works without Chirp,
  better with Chirp"). The open drawer is `role="dialog" aria-modal="true"` and
  named (sidebar via `aria-labelledby`, rail via its `aria-label`); the rail's
  close control is injected by the runtime so it is never stranded by the rail's
  OOB content swaps. Proven end-to-end by `tests/browser/test_shell_nav_drawer_gauntlet.py`
  (in the `test-browser-chrome-check` gate). See `docs/patterns/navigation.md § Mobile Nav Drawer`
  ([#196](https://github.com/lbliii/chirp-ui/issues/196)).
- Added arrow-key result navigation to `command_palette`. The search input is now a `role="combobox"` over the `role="listbox"` results: ArrowUp/ArrowDown rove the `role="option"` items via `aria-activedescendant` (the active item carries `aria-selected="true"` and an `--active` highlight), Enter activates the active item, and each fresh htmx result set auto-highlights its first item. A new `command_palette_item(id, label, href|action, hint)` helper renders results as roving options; legacy raw-HTML results stay Tab-navigable. Behaviour lives in the new `chirpuiCommandPalette` Alpine factory (which also owns Cmd/Ctrl+K open). Proven by the command-palette browser gauntlet, now in the `test-browser-chrome` gate ([#201](https://github.com/lbliii/chirp-ui/issues/201)).
- Added layout affinity conventions, workspace shell recipes, and relationship-owned spacing contracts so composed Chirp UI screens handle rhythm, pressure, wrapping, and local overflow with less page-specific CSS.
- Added the Tracks learning-path feature: a top-level section that assembles separate documents into one ordered, navigable pillar page (data-file model via `site/data/tracks.yaml`), with an LMS card index, in-track progress + prev/next, sidebar scroll-spy, and localStorage resume.
- Dogfooded every shipped chirp-theme template family on the live docs site (blog, tutorial, resume, authors, changelog) and added an on-site shortcodes/directives reference plus a component catalog, so the theme's surfaces are demonstrated and regression-guarded rather than undocumented.
- Extended `check_alpine_runtime()` to detect Alpine **core** (not just the
  `chirpui-alpine.js` registration script): the result now carries `core_loaded`
  and `core_url_valid` plus a human-readable `problems` tuple, and flags the
  silent CDN footgun where an Alpine core `<script>` is present but its URL is a
  bare `alpinejs@<version>` (CommonJS) instead of the browser build ending in
  `/dist/cdn.min.js`. Detection is framework-agnostic (matches `alpinejs@` /
  `@alpinejs/csp` srcs and Chirp's `data-chirp="alpine"` marker, and ignores the
  mask/intersect/focus plugins). The existing `ok` / `script_loaded` contract is
  unchanged ([#191](https://github.com/lbliii/chirp-ui/issues/191)).
- Extended the chirp-theme dogfood: a first-class `notebook` section now ships a real dogfood notebook page (so the notebook layout renders on the live site) and is guarded by the family-coverage smoke test, a structured-frontmatter changelog entry exercises the version-grouped `change_section` path in `changelog/single.html`, and `tutorial/list.html` is deduped onto the shared `learning_index()` macro instead of an inlined `resource_index` block. The `/docs/` landing destination cards each lead with a shipped Phosphor icon, an adoption quickstart documents applying `theme: "chirp-theme"` to a Bengal site (minimum Bengal 0.3.3 and the `library_asset_tags` requirement), and the family-coverage smoke test now also guards that a category landing aggregates multiple pages (the singular `category:` frontmatter Bengal's default `categories` taxonomy reads).
- Added eight new stable layout and control primitives: `aspect_ratio` (fixed-ratio frame for media, previews, and embeds), `item` (reusable row anatomy for lists, menus, command results, and resource links), `kbd` (inline keyboard-key hint for shortcuts), `ui_label` from `label.html` (standalone label primitive for custom controls and compact forms), `scroll_area` (contained overflow region for sidebars, menus, code previews, and panels), `separator` (semantic or decorative divider), `slider` (native range-input wrapper for numeric settings and filters), and `toggle_group` (grouped single- or multiple-selection toggle buttons) ([#118](https://github.com/lbliii/chirp-ui/issues/118)).

### Changed

- Extended the existing-token typography and rhythm polish pass to navigation, segmented-control, disclosure, and overlay component defaults.
- Demoted `workspace_shell` from `stable` to `experimental` maturity to match the
  new [Application Chrome Posture ADR](docs/decisions/application-chrome-posture.md):
  the blessed application-chrome composite is the route-context rail wired into
  `app_shell`, not the broader workbench *frame*, which the application-chrome plan
  still defers. The macro itself is unchanged and continues to render; only its
  stability signal (manifest, `chirp-ui find`, generated docs) moves to experimental,
  aligning it with `composer_shell` and `dock`.
- Demoted the **`data-table`** descriptor from `stable` to `experimental`
  (metadata-only; no render change). Per [#200](https://github.com/lbliii/chirp-ui/issues/200)'s
  acceptance ("no longer a thin wrapper labeled stable"), `data_table` is the
  deliberately-thin filter+table+pagination convenience wrapper and the new
  `data_grid` composite is now the real interactive grid. `table` and `table-wrap`
  remain `stable` — they are genuinely complete low-level primitives (real
  `<table>` semantics, alignment, widths, sticky header/col, slots). Agents and
  docs that read the manifest will see the new maturity value; it is intentional,
  not a regression. See `docs/safety/public-surface-stabilization.md`.
- Document and begin the bespoke `chirp-theme` rewrite by routing the desktop shell through Chirp UI navbar/footer primitives, marking core page/search/error surfaces, moving docs heroes/navigation/TOC and blog/card compatibility surfaces toward Chirp UI primitives, adding a catalog-style double-left-rail docs surface with symbol-first outer navigation, quieter contextual inner rail rows, a redesigned page-map TOC rail, and a rail-native back-to-top action, replacing raw release lists with ordered release cards, widening hover/focus nav dropdowns, removing legacy hard-coded Bengal palette controls/assets, and preserving the transitional Bengal asset shim.
- Extended the existing-token typography and rhythm polish pass to data display and loading feedback component defaults.
- Extended the existing-token typography and rhythm polish pass to header, setup, divider, tooltip, and compact affordance component defaults.
- Extended the existing-token typography and rhythm polish pass to message, conversation, social, and media component defaults.
- Extended the existing-token typography and rhythm polish pass to site navigation, feature, resource, and token-input metadata surfaces.
- Extended the existing-token typography and rhythm polish pass to special form controls, rating controls, range values, and drag affordances.
- Extended the typography and rhythm polish pass to small controls, navigation affordances, and animated control primitives using existing Chirp UI tokens.
- Improve registry discovery and add source-only reference proof, analysis, and recipe guidance for Chirp UI promotion candidates.
- Made the registry `maturity` field honest about thin composition wrappers. A
  `maturity="stable"` component that composes other registry components (non-empty
  `composes`) is now treated as a composition wrapper and must carry the same
  promote-to-stable proof collateral as any stable promotion — either a
  `| Promote to stable |` row in `docs/safety/public-surface-stabilization.md` or a
  justified `STABLE_COMPOSERS_WITH_PROOF` allowlist entry naming its asserting
  proof test. The new `test_no_thin_composition_wrapper_is_stable_without_proof`
  (composing with the existing promote-to-stable-collateral invariant, no new
  maturity tier) catches the class: `data_table` shipped `stable` with
  `composes=("filter-row","table","pagination")` before #200 demoted it, and this
  gate would flag any future repeat. The audit confirmed zero current offenders —
  `data_table` is already `experimental`, and `table`/`table-wrap`/`calendar`/
  `bar_chart`/`donut` plus the hardened ASCII set carry `composes=()` so the rule
  provably never fires on those complete/low-feature primitives
  ([#203](https://github.com/lbliii/chirp-ui/issues/203)).
- Polished the chirp-theme home hero preview card and finished a slice of the CSS-token layering cleanup: the preview-card nav labels now read at body-copy contrast, the "example interface" overline uses the brand sans small-caps treatment, the window-chrome traffic-light dots were resized and recolored from public `--chirpui-*` tokens so they read as an intentional macOS-style cluster, and the remaining raw `rgba()` panel gradients/shadows are now token-driven. Release history can surface a one-line `highlight:`/`summary:` frontmatter line per card, now exercised on the latest and a feature release. Also deleted the dead `.has-prose-content` / `base/prose-content.css` primitive from the mermaid component CSS and the CSS scoping docs (no template ever emitted it), and lowered the legacy `var(--color-*)` ceiling to lock in the migration gain.
- Raise the default visual taste floor for Chirp UI screens and high-impact components while preserving registry-owned component vocabulary.
- Reconciled the chirp-theme JavaScript subsystems against what actually ships. Deleted the template-unreferenced dead modules `holo.js`, `session-path-tracker.js`, `data-table.js`, and the bundled `tabulator.min.js`, and removed the Tabulator/data-table branch from `lazy-loaders.js` and the `base.html` lazy bundle so only the live Mermaid and D3-graph lazy features remain. Stripped dead SPA-navigation listeners (`contentLoaded`, `turbo:*`, `pjax:*`, `astro:*`) that Bengal never dispatches from `toc.js`, `tracks.js`, `graph-contextual.js`, and `link-previews.js`, and added a `data-toc-bound` idempotency guard so the progressive-enhancement registry callback and the `ready()` auto-init no longer double-bind the TOC. Enabled `content.mermaid` in the site config so the existing blog mermaid dogfood renders with the full toolbar/theme bundle. Added regression tests asserting every `data-bengal` hook has a matching `Bengal.enhance.register()` init path, that no dead SPA listeners remain, that the retired modules stay deleted, and that `BENGAL_LAZY_ASSETS` carries exactly the keys for the enabled features; plus a vitest `mockDeniedStorage()` helper and theme.js regression proving theme switching still flips `data-theme` (and warns) when `localStorage` throws.
- Refactored the chirp-theme non-documentation content types onto a shared list shell: the tutorial/resume/notebook lists (via `partials/learning-index.html`) and the changelog/releases/authors lists now compose `page_hero` + a grid/timeline directly instead of `chirpui/resource_index`, which removes the inert "Filter…/Search" GET form (non-functional on a static build, duplicating the global Cmd+K) and the duplicate page-hero/results heading — each list now leads with a single heading and the item count in the hero metadata. Single-page reading columns are also centered (added `margin-inline: auto` to the `type-identity.css` reading-measure block, with a sibling rule for the track article that carries `.prose`), so prose no longer hard-anchors left while the footer centers.
- Replaced the hand-maintained static component showcase with the live `examples/component-showcase` Chirp app, now deployed as a Railway service at <https://chirp-ui-showcase-production.up.railway.app> and reachable from the `/showcase/` docs route (which keeps its inline live specimens and links out to the deployed app). Removed the static gallery and its build scaffolding — the `assemble-static-showcase.sh` script, the `docs-assemble-showcase`/`showcase-guard` poe tasks, the Makefile `showcase*` targets, and the Pages assemble+guard steps — so `docs-build-all` is now just the Bengal build plus manifest emit. Added Railway deploy config (`railway.json`, `examples/component-showcase/Dockerfile`, `.dockerignore`) and a `$PORT` bind in the example app so it runs unchanged locally and binds `0.0.0.0:$PORT` on the platform.
- Reworked the docs sidebar disclosure: sections now open/close via an open/closed folder icon (a real toggle button beside the navigable label — no caret), keeping section labels visible when collapsed and adding zero nested-interactive / landmark / region axe violations.
- Scope Chirp UI view-transition names to direct shell main boundaries to avoid duplicate transition names in embedded shell previews.
- Unified active-link sync into one canonical implementation in
  `shell_runtime_script()`, emitted by **both** shell entry points. The
  `app_shell()` macro path now gets client active-sync it never had, and
  `app_shell_layout.html` no longer carries a divergent inline copy. The shared
  `syncNav` **mirrors the server's per-item `match=`**: `sidebar_link` /
  `navbar_link` emit `data-chirpui-shell-match="exact"|"prefix"` only when `match=`
  is set, and the JS toggles the `--active` class plus `aria-current` for those
  links alone. The macro's `#chirpui-sidebar-nav` and the layout's
  `#chirpui-topbar-breadcrumbs` announcers now reach parity.

  **Behavior change to call out:** the layout's old blind-prefix client toggle —
  which ran `path === href || path.startsWith(href + "/")` against **every** link
  regardless of `match=` — is gone. Match-less sidebar/navbar links are now
  **server-authoritative** (active state comes from server-rendered `active=` /
  `aria-current`, not a client path guess). Shells that relied on the old
  auto-highlight without setting `match=` should set `match="prefix"` (or
  `match="exact"`) on those links to restore client re-highlighting across boosted
  navigation ([#197](https://github.com/lbliii/chirp-ui/issues/197)).
- Wired the cross-track membership widget into `doc/single.html`, so any doc whose slug appears in a `site/data/tracks.yaml` track now renders an in-track prev/next + progress card after its page navigation. A doc that belongs to multiple tracks surfaces one card per membership, and a doc in no track renders nothing. The prev/next links are plain internal anchors, so site-wide htmx boost handles them without a per-link opt-out.
- Lowered the Bengal asset-path contract floor in `chirpui_asset_path()` from `0.3.3` to `0.3.2`, so the library asset-path scheme is also emitted on Bengal `0.3.2`. The `chirp-theme` package still requires Bengal `>= 0.3.3` for `library_asset_tags()` ([#118](https://github.com/lbliii/chirp-ui/issues/118)).

### Fixed

- Accepted `notebook` as a documentation destination in the search-relevance fixture: now that the notebook family is first-class (#146/#147) and ships a "render a card from Python" dogfood page, that page legitimately ranks #1 for the query "card". Added `notebook` to the test's `DOC_SECTIONS` so this cross-family interaction is correct behavior rather than a failure.
- Added semantic icon aliases for common integration status names so `activity`,
  `pause`, `info`, and `warning` render without validation warnings.
- Completed the autodoc Python member detail and raised its visual floor: each documented method/function now renders its full Returns and Raises blocks inside the member accordion body (reading `member.metadata.returns`, `member.metadata.parsed_doc.returns`, and `member.metadata.parsed_doc.raises` via the shared `returns.html`/`raises.html` partials, strict-undefined guarded), so a raising member like `register_colors` finally surfaces its `ValueError`. The nested Python and OpenAPI reference list pages now pass `title=none` to `resource_index` so the page hero owns the sole `<h1>` and the results section heading is the only subheading (matching the already-fixed `/api/` home), and the now-dead `.chirp-theme-api-index .chirpui-search-header__content { display: none }` rule was removed.
- Fixed `data_grid`'s "Load more" button never being refreshed or removed after the last page. `data_grid_rows` now accepts `load_more_url`/`has_more` (plus label/trigger/swap/`selection_id`) and emits the load-more sentinel as an `hx-swap-oob` update to a stable `#{selection_id}-load-more` container via the new `grid_load_more` macro — so each load-more fetch refreshes the button's next-page URL or, on the last page, removes it. Previously the button persisted past exhaustion and re-clicking it silently fetched past the end of the result set. Adds a load-more-to-exhaustion browser gauntlet assertion ([#231](https://github.com/lbliii/chirp-ui/issues/231)).
- Fixed `segmented_control()` rendering 42px tall instead of the 40px shared control-height contract. The pill `segmented_control()` and the legacy form-field `segmented_control_field()` share the `.chirpui-segmented` block class, and the form-field block's `border: 1px solid` leaked onto the borderless pill — pushing it 2px proud of its neighbouring controls in toolbars and action strips. The legacy container rule is now scoped to the form-field structure (`:has(> .chirpui-segmented__input)`) so it no longer applies to the pill, and the option `min-block-size` math is explicit, so the pill computes to exactly the control-height token. The form field is unchanged ([#230](https://github.com/lbliii/chirp-ui/issues/230)).
- Fixed flagship-page defects: dark-mode and home primary-button contrast, the Outfit webfont never loading, `search_bar` rendering a raw icon name, ~89 broken `/api/<module>/<member>/` autodoc links (now in-page anchors), unique nav landmark names, valid `<aside>` roles, a decorative reading-progress bar, and keyboard-scrollable parameter tables.
- Fixed route-scoped shell regions stranding stale content on boosted navigation.
  The `htmx:beforeSwap` reset that empties a shell region before its out-of-band
  fragment lands previously lived only in `app_shell_layout.html`'s inline script
  and was hardcoded to `#chirp-shell-actions` — so the `app_shell()` macro path had
  no reset at all, and the new route-context rail (`#chirpui-context-rail`) was
  never cleared. It is now in the shared `shell_runtime_script()` (emitted by both
  shell entry points) and covers both regions: navigating to a route that ships no
  fragment for a region now empties it rather than stranding the prior route's
  content. Adds a Playwright gauntlet proving the rail swaps on boosted nav and
  clears on a contextless route (wired into the `test-browser-chrome` gate)
  ([#195](https://github.com/lbliii/chirp-ui/issues/195)).
- Fixed the changelog/releases timelines and the authors profile. The "newest first" timelines were not chronological: the dotted `sort(attribute="metadata.date,title")` silently fell back to title-alpha (kida's attribute resolver does not descend dotted paths), so changelog now sorts by the flat `date` and releases by version (`title`). `/releases/` now renders its bespoke `releases/list.html` timeline (it was orphaned as `type: page` and fell through to the generic section index, which re-emitted the dead filter). The authors directory no longer shows "0 authors" for a published author (its data source now resolves the author content pages), and an author profile now renders an initials avatar, a single bio, and a real authored-post feed (matched via `metadata.author` across `site.pages`) instead of a self-referential card and a metric tile wasted on the author's own name.
- Gave every `<nav>` landmark a unique, static accessible name and made the floating back-to-top button honor `prefers-reduced-motion`. The chirp-ui `navbar()` and `sidebar()` macros now accept an `aria_label` parameter so a page with multiple navigation landmarks (the theme's primary header nav, the docs catalog rail, and the docs sections tree) reads as distinct entries in a screen reader's landmark menu rather than "navigation, navigation, navigation" — the docs sections label is now baked into the template instead of relying on `docs-nav.js` runtime injection, so it survives even where that script never loads (the static showcase). The theme's `interactive.js` back-to-top handler now picks `behavior:'auto'` (an instant jump) for reduced-motion users via the shared `BengalUtils.prefersReducedMotion()` helper, and the showcase demo navs each carry a unique label.
- Hardened the chirp-theme document head and critical render path: the Outfit display webfont is now reliably wired (the 400/600 woff2 weights preload with crossorigin and the generated fonts.css is linked, gated on the configured display font), and the unused .ttf font duplicates were dropped so only woff2 ships. The theme stylesheet now loads non-render-blocking via a stdlib-only `rel=preload as=style` + onload swap with a `<noscript>` fallback, and the d3js.org preconnect is gated behind the graph feature instead of being emitted on every page. The Bengal min-version contract is now loud: theme.toml declares both `requires_bengal` and a `[bengal] min_version` floor, and base.html emits a dev-visible diagnostic (naming Bengal >= 0.3.3) when `library_asset_tags()` is unavailable instead of silently shipping a token-less style-only build.
- Made the built-home `style.css` non-render-blocking test (#157) fingerprint-tolerant: Bengal emits `style.<hash>.css` in built output, so the assertion now matches the stylesheet by stem+extension instead of the literal unhashed filename. The test skips on a clean checkout (it needs a built `site/public`) but failed a local `poe ci` run after `poe docs-build`; this keeps the local build gate green.
- Made the chirp-theme's SEO surface emit absolute URLs end to end: the production environment now builds canonical, Open Graph, sitemap `<loc>`, and the robots.txt `Sitemap:` directive from the full absolute origin (`https://lbliii.github.io/chirp-ui`) instead of a path-only baseurl, and `og:image`/`twitter:image` are wrapped in `canonical_url(...)` so social scrapers receive absolute https image references instead of relative paths that yield no preview card. Added JSON-LD structured-data render tests (home → WebSite + SearchAction + Organization; doc → TechArticle + BreadcrumbList; post → BlogPosting; product → Product/Offer) that parse the emitted graphs and assert correct `@type`s, plus SEO config guards for the absolute production origin and the enabled RSS feed.


## [0.9.0] - 2026-05-14

### Added

- Added a Bengal theme controls anatomy guide and published site mirror covering `chirp-theme` theme menus, search, mobile navigation, TOC, and content-tab hooks.
- Added a Sprint 4 documentation IA migration matrix that maps published docs
  pages to canonical durable sources and SSG-owned agent artifact source
  provenance, without overriding Bengal's `llms.txt` or `agent.json` behavior.
- Added a Sprint 6 agent source inventory with provenance labels, snippet eligibility states, and tests that prevent generated, static-showcase, docs-wrapper, and browser-fixture sources from becoming copyable snippets.
- Added a Sprint 6 agent source map that records Bengal-owned generated outputs, Chirp-owned source inputs, the published manifest boundary, and forbidden output-name overlaps.
- Added a drawer and tray anatomy guide plus published site mirror covering
  native drawer and store-backed tray rendered contracts.
- Added a dropdown anatomy guide and published site mirror covering dropdown
  menu, select, and split-menu rendered contracts.
- Added a modal anatomy guide and published site mirror covering native modals,
  overlay modals, and confirm dialog rendered contracts.
- Added a tabs anatomy guide and published site mirror covering htmx tabs,
  client-side tab panels, route tabs, and tabbed page layout contracts.
- Added an application chrome system plan and navigation collateral for layered
  shells, rails, trays, route rows, command overlays, and recipe-first promotion
  gates.
- Added application chrome epic follow-up proof for rail-to-drawer recipes,
  multi-family browser gauntlets, rhythm audits, Bengal parity, composite
  evaluation, and release-readiness tracking.
- Added descriptor-backed `appearance` and `tone` macro parameters for the pilot
  components: `btn`, `badge`, `alert`, `card`, `surface`, and form fields.
  The shared destructive tone is `danger`; existing component-local
  `variant="error"` compatibility remains unchanged.
- Added the first token-only theme-pack catalog with immutable Python metadata
  and packaged `atlas`, `ember`, and `sage` CSS resources discoverable through
  the library contract, manifest, a `/theme-packs` showcase matrix, and Bengal
  palette-control mapping metadata. The catalog packs are also covered by
  browser tests that verify packaged light, dark, and system token resolution
  across navigation, forms, overlay layers, compact data tables, and desktop/mobile
  viewports.

### Changed

- Added rapid-click request coordination defaults for boosted shell navigation, live search/filter helpers, and mutating HTMX form/action helpers.
- Cleaned first-party showcase chrome so new examples stop teaching legacy
  helper-class chains, added a static visual audit surface with browser
  guardrails, and documented the pre-1.0 compatibility policy for legacy helpers.

### Fixed

- Fixed dropdown menu and split-menu selection payload handling so labels, URLs,
  and actions are read from escaped `data-*` attributes instead of interpolated
  into inline Alpine JavaScript literals.
- Fixed tab-panel selection handling so tab ids are read from escaped `data-*`
  attributes by `chirpuiTabs()` instead of interpolated into inline Alpine
  JavaScript literals.


## [0.8.0] - 2026-05-11

### Added

- Added a framework-neutral Chirp UI library contract for host integrations and
  advanced `chirp-theme` toward Chirp UI-native Bengal theme templates, assets,
  and content surfaces. ([#102](https://github.com/lbliii/chirp-ui/issues/102))

### Changed

- Upgrade the Kida dependency floor to `kida-templates>=0.9.0`, refresh the lockfile, and add Kida-backed escape-audit coverage for trusted markup sites. ([#103](https://github.com/lbliii/chirp-ui/issues/103))


## [0.7.0] - 2026-05-05

### Added

- Add a cloud/control-plane dense navigation recipe for scope, services, favorites, resource search, and deployment views.
- Add dense object chrome recipes, stable nav badge states, and compact command palette trigger options.
- Added a browser-test product page pattern fixture that exercises the documented recipes across responsive widths.
- Added a browser-tested forum-site pattern fixture covering dense community, thread, Q&A, moderation, and activity compositions.
- Added a business object console navigation recipe to the component showcase.
- Added a collaboration inbox navigation recipe to the component showcase.
- Added a developer platform navigation recipe to the component showcase.
- Added a keyboard-first tracker navigation recipe to the component showcase.
- Added a knowledge workspace navigation recipe to the component showcase.
- Added a product-suite work hub navigation recipe to the component showcase.
- Added a reference documentation navigation recipe to the component showcase.
- Added an active plan for product-page composition recipes inspired by the LangChain homepage design review.
- Added an editor workbench navigation recipe to the component showcase.
- Added an experimental `cta_band` marketing pattern for final and mid-page product calls to action.
- Added an experimental `logo_cloud` marketing pattern for accessible customer, partner, integration, and ecosystem proof bands.
- Added an experimental `story_card` marketing pattern for customer outcome and use-case proof grids.
- Added an observability and ops console navigation recipe to the component showcase.
- Added canonical navigation contract guidance, a dense object-navigation showcase example, and opt-in breadcrumb overflow for deep path trails.
- Added dense navigation synthesis guidance with primitive candidates and anti-decisions.
- Added experimental official pattern assets for marketing, media, forum/social, and detail surfaces, including `detail_header`, `facet_chip`, `thread_reader_layout`, `topic_card`, `answer_card`, `moderation_queue_item`, and media catalog/watch patterns.
- Added product-page pattern recipes for hero/proof, lifecycle showcase, proof bands, product choice grids, customer story strips, and CTA bands.
- Added scope switcher and saved view strip navigation patterns plus stable sidebar badge states.
- Added scoped AGENTS.md steward guidance for registry, rendering, theme, build, CI/release, tests, docs, planning, examples, and published site ownership.

### Changed

- Action bar items now resolve semantic icon names through the ChirpUI icon registry, with forum/social action names for reply, vote, watch, follow, report, and share.
- Added `arrow-up` and `arrow-down` icon aliases so forum vote recipes resolve through the icon registry.
- Added a forum-pattern friction log that separates resolved action/icon ergonomics from Elbysodic surfaces that still need migration evidence before component promotion.
- Hardened component showcase contracts so examples must use generated CSS, manifest-backed templates, and warning-free current component APIs.
- Recorded the Elbysodic forum-pattern consumer pass, including which PBP surfaces should try existing ChirpUI vocabulary before any new public forum macros are proposed.
- Recorded the forum pattern promotion checkpoint: the browser fixture does not yet justify public forum-specific macros, while action-bar semantic icons address the first validated friction point.
- Updated action-bar and post-card API examples to teach semantic icon names instead of raw glyphs.
- Updated the AGENTS.md steward system with swarm protocol guidance, contract checklists, and CI/release stewardship.

### Fixed

- Fixed `app_layout.html` to use Chirp's current injected Alpine runtime, load the data-theme-aware starter theme, and avoid duplicate/stale Alpine scripts in showcase-style apps.
- Fixed the docs-site build wrapper, GitHub Pages workflow, and chirp-theme optional metadata/menu defaults so published release pages render under Bengal 0.3.2's current CLI.
- Fixed dropdown select events to preserve option values and hardened split button menu positioning and fused visual styling.
- Fixed shell-frame boosted navigation scroll restoration, hash-anchor landing, and split panel Alpine drag state issues found while running the 0.6.0 browser release gate.


## [0.6.0] - 2026-04-26

### Added

- Add manifest metadata for composite slot forwarding via `composes`, `slot_forwards`, and `slots_yielded`.
- Added Elbysodic-driven navigation, metadata, avatar, chip, rendered-content, composer, and token-input primitives.
- Added `nav_tree(branch_mode="linked")` for link-first section trees, with server-controlled open branches, item badges, and registry-cited item state hooks.
- Added a browser gauntlet route and responsive detector tests for broad ChirpUI component compositions.
- Added a packaged token-only app theme starter plus documentation for wiring app-owned light, dark, and system theme tokens after `chirpui.css`.
- Added contextual-detail contracts for block tooltips, hinted nav tree items, hinted timeline titles, and gauntlet coverage for hover/focus/touch composition.
- Added linkability contracts for file tree branch forwarding and timeline title links, with gauntlet coverage for linkable composition surfaces.
- Release 0.6.0 — kida-templates 0.7.0/0.8.0 upgrade hardening, agent-grounding-depth manifest (the full Python surface), CSS envelope hardening batch 1, modularized `chirpui.css` from partials, base-layer containment + preflight-style defaults, composite contract tests with a provide/consume introspection API, dev-mode fail-fast diagnostics, app theme starter, Elbysodic-driven primitives, and the responsive composition gauntlet.

### Changed

- Clear the registry auto-category debt by promoting CSS-only descriptors into explicit categories, descriptor-local emit trims, primitive vocabulary docs, manifest authoring hints, discovery helpers, and debt gates.
- Harden the agent manifest with explicit maturity, runtime requirements, public metadata checks, and a manifest quality scorecard for public components.
- Hardened app shell, navigation strips, tables, rendered content, control sizing, and mobile touch targets for phone and tablet layouts.
- Refresh the README to match the current Kida-style product framing, registry/manifest contract, and current chirp-ui development workflow.
- Upgrade the Kida template dependency floor to 0.8.0 so Mapping optional-chain misses stay null-safe under strict mode.

### Fixed

- Aligned icon buttons, segmented controls, and small ASCII toggles to the shared control height tokens, including touch-target promotion on narrow/coarse-pointer contexts.
- Fixed button and icon button htmx request shorthands so button elements default to `hx-select="unset"` inside boosted shells, matching link-button fragment behavior.
- Fixed card titles and badge text so long unbroken content can wrap instead of escaping narrow viewports.
- Fixed shell-frame boosted navigation so same-route refreshes preserve scroll and hash links land below the sticky topbar.
- Fixed split panel drag state so Alpine receives JavaScript booleans and can resize panes reliably.


## [0.5.0] - 2026-04-20

### Added

- **Agent-grounding-depth epic — manifest is the full Python surface** — `chirpui-manifest@2` now carries every component's complete Python API: params (with defaults and required flags), named slots, provides/consumes keys, and the `{#- chirp-ui: … -#}` doc-block description. Extraction is AST-only via `kida.lexer`/`kida.parser` (free-threading safe, no template compile). New surfaces built on this: (1) `docs/COMPONENT-OPTIONS.md` grows a generated `## API Reference` block regenerated by `poe build-docs` / gated by `poe build-docs-check`, (2) `python -m chirp_ui find <query> [--category=…]` substring-matches components by name/block/category/description over the shipped manifest, and (3) `make release-preflight` — prereq of `make build`/`make release`/`make gh-release` — regenerates `chirpui.css` + `manifest.json` + `COMPONENT-OPTIONS.md` and fails the release with a "commit these files" message if `git diff --quiet` reports drift. Plans triaged into `docs/plans/` (in-flight) and `docs/plans/done/` (shipped) with cross-refs updated; `docs/INDEX.md` split into the two buckets so agents cannot cite stale plans as live direction. Full plan in `docs/plans/PLAN-agent-grounding-depth.md`.
- **Base-layer containment + preflight-style defaults** — content no longer punches past cards, surfaces, callouts, or bento cells without manual wrapping. `.chirpui-surface` and `.chirpui-callout` get `min-width: 0` + `overflow-wrap: break-word`; `.chirpui-field__input` gets `max-width: 100%` + `min-width: 0`; card/surface links wrap long URLs via `overflow-wrap: anywhere`. New utility classes: `.chirpui-scroll-x` (local horizontal scroll region), `.chirpui-truncate` (single-line ellipsis), `.chirpui-clamp-2` / `.chirpui-clamp-3` (multi-line clamp). Zero-specificity `:where()` reset bounds raw `<img>` / `<svg>` / `<video>` / `<iframe>` / `<embed>` / `<object>` / `<canvas>`; `<pre>` and `<table>` dropped inside a card/surface/callout auto-scroll horizontally. `prefers-reduced-motion: reduce` is now honored globally via `*, ::before, ::after`. `:root` picks up `accent-color: var(--chirpui-accent)` so native checkboxes, radios, range, and progress match the brand. Prose paragraphs use `text-wrap: pretty`; code blocks and prose `<pre>` get `overscroll-behavior: contain` so scroll doesn't chain to the page. Full epic rationale in `docs/PLAN-base-layer-hardening.md`; usage in `docs/LAYOUT.md § Content containment`.
- **CSS modularization + registry parity + agent-groundable manifest** — `chirpui.css` is now an output of the Python component registry rather than a hand-authored monolith. 160 per-component partials under `src/chirp_ui/templates/css/partials/` are concatenated into the shipped stylesheet by `scripts/build_chirpui_css.py` (pure-Python stdlib; free-threading safe); `poe build-css` regenerates, `poe build-css-check` fails CI if the committed output is stale. The cascade order is now public API: `chirpui.css` declares `@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;` at the top — consumers override by placing rules in `@layer app.overrides` (or any later-declared layer), no specificity tricks required (`docs/CSS-OVERRIDE-SURFACE.md`). `ComponentDescriptor` gains an `emits` property and a registry↔CSS parity test pins every registry-cited class to a real selector in the stylesheet (and vice versa), so AI agents that ground against the registry cite real classes. The `@scope (.chirpui-X) to (.chirpui-X .chirpui-X) { … }` envelope is the default authoring form for new components; `045_card.css` is the pilot and is covered by `tests/browser/test_card_variants.py` (nested-instance bleed fix verified by computed-style assertion). New: `chirp_ui.manifest` module — `build_manifest()` (Python API), `python -m chirp_ui.manifest --json` (CLI), and `site/public/chirpui.manifest.json` (build artifact, regenerated by `poe docs-build-all`) — publishes 309 components and 356 tokens under schema `chirpui-manifest@1`. Full plan in `docs/PLAN-css-scope-and-layer.md`; registry-projection rationale in `docs/VISION.md § CSS architecture as a registry projection`.
- **Composite contract tests + provide/consume introspection** — new `tests/test_composite_contracts.py` parametrizes 18 composites (card, modal, panel, accordion, form, feature_section, site_shell/header/footer, filter_bar, command_bar, suspense, surface, resource_index, tag_browse_tray) and asserts each renders without `ChirpUIValidationWarning`, catching invalid variant / unknown icon classes of bug at chirp-ui CI time. ``chirp_ui.inspect`` gains ``list_provides()``, ``list_consumes()``, and ``audit_provide_consume()`` (plus ``--provides``, ``--consumes``, ``--audit-context`` CLI subcommands) — a regex parser over the existing ``{# @provides ... #}`` / ``{# @consumes ... #}`` annotations so apps can audit dead provides, orphan consumers, and annotation drift. Two real drifts surfaced and fixed: ``panel.html`` and ``surface.html`` listed ``_surface_variant`` consumers as ``status`` and ``settings_row``, but the actual macros are ``status_indicator`` and ``settings_row_list``.
- **Dev-mode diagnostics** — ``set_strict("auto")`` now reads the ``CHIRP_UI_DEV`` environment variable (truthy: ``1``/``true``/``yes``/``on``) at call time, so dev hosts opt in once and every ``ChirpUIValidationWarning`` (invalid variant, unknown icon, bad size, unparseable color) escalates to ``ValueError``. New ``chirp_ui.alpine`` module exposes ``ALPINE_REQUIRED_COMPONENTS`` (manifest of the 8 chirp-ui Alpine factory names) and a pure ``check_alpine_runtime(html)`` helper so frameworks can detect layouts that import interactive macros (theme toggle, command palette, collapsible sidebar, dropdown, dialog, copy) but forget to load ``chirpui-alpine.js``.

### Changed

- Remove vestigial `from __future__ import annotations` imports (9 files) and add `DesignSystemReport`/`DesignSystemStats` TypedDicts for `design_system_report()` return type. ([#py314-cleanup](https://github.com/lbliii/chirp-ui/issues/py314-cleanup))
- **Upgrade kida-templates 0.6.0 → 0.7.0 + harden templates for `strict_undefined=True` default flip** — Kida 0.7.0 flips `strict_undefined` to `True` by default (previously `False`), so any `{{ item.optional_key }}` reference where `optional_key` is missing from a dict now raises `UndefinedError` instead of rendering empty. Rather than opt out, all dict-iterating macros were hardened to use explicit guards: `.get("key")` for branching, `| default("")` for inline rendering. Affected components: `timeline`, `dock`, `segmented_control`, `route_tabs`, `nav_tree`, `tree_view`, `bar_chart`, `breadcrumbs`, `description_list`, and five `forms.html` macros (`select_field`, `radio_field`, `segmented_control_field`, `multi_select_field`, `key_value_form` datalist) plus `config_row`. New regression suite in `tests/test_strict_undefined.py` renders each affected macro with the minimal `[{}]` input and asserts no `UndefinedError`, so future strict-mode breakage is caught immediately. No public API changes — callers that already passed complete dicts are unaffected.

### Fixed

- **CSS envelope hardening, batch 1 — six high-bleed components scoped** — `tray`, `drawer`, `modal`, `surface`, `callout`, `video-card`, and `channel-card` partials now use the `@layer chirpui.component { @scope (.chirpui-X) to (.chirpui-X .chirpui-X) { … } }` envelope convention introduced by the `045_card.css` pilot. The upper scope boundary stops outer-component rules at the first nested instance, fixing a class of cascade bleeds — most notably `:scope:hover` on video-card flipping inner card borders, `link:hover .name` on channel-card tinting nested names, and `:has()`-driven empty-header autohide on callout matching across nested boundaries. Each component is paired with a dedicated browser test under `tests/browser/` (`test_surface.py`, `test_callout.py`, `test_video_channel_cards.py`, plus updates to `test_tray.py`) that asserts variant rendering survives and the nested-bleed boundary holds via computed-style comparison. Test infra fix: `tests/browser/templates/base.html` now loads `chirpui-alpine.js` before Alpine core so its `alpine:init` listeners register before the event fires (defer scripts execute in document order). Full per-component bleed analysis in `docs/PLAN-envelope-hardening-batch-1.md`; convention rationale in `docs/PLAN-css-scope-and-layer.md`.
- **Shell actions** — Map Chirp ``ShellAction``/``ShellMenuItem`` variants (``default``, ``secondary``) to ``btn`` variants via new ``shell_action_btn_variant`` filter; register ``chevron-down`` in the icon set; overflow trigger uses ``ghost`` + named chevron icon. Test ``env`` fixture registers the filter for standalone Kida renders.


## [0.4.0] - 2026-04-13

### Added

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
