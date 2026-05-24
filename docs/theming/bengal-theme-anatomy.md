# Bengal Theme Controls Anatomy

This guide documents the interactive controls shipped by the packaged Bengal
`chirp-theme`. These controls are not Chirp UI component macros and are not
registry-owned `chirpui-*` component contracts. They are packaged Bengal theme
partials and static assets that use Chirp UI tokens, macros, and CSS as the
primitive layer for a static docs shell.

The source of truth lives in:

- `src/bengal_themes/chirp_theme/templates/base.html`
- `src/bengal_themes/chirp_theme/templates/partials/theme-controls.html`
- `src/bengal_themes/chirp_theme/templates/partials/search-modal.html`
- `src/bengal_themes/chirp_theme/templates/partials/search.html`
- `src/bengal_themes/chirp_theme/templates/partials/docs-nav.html`
- `src/bengal_themes/chirp_theme/templates/partials/docs-toc-sidebar.html`
- `src/bengal_themes/chirp_theme/templates/partials/navigation-components.html`
- `src/bengal_themes/chirp_theme/templates/partials/page-actions.html`
- `src/bengal_themes/chirp_theme/assets/js/core/theme.js`
- `src/bengal_themes/chirp_theme/assets/js/core/search.js`
- `src/bengal_themes/chirp_theme/assets/js/enhancements/action-bar.js`
- `src/bengal_themes/chirp_theme/assets/js/enhancements/mobile-nav.js`
- `src/bengal_themes/chirp_theme/assets/js/enhancements/tabs.js`
- `src/bengal_themes/chirp_theme/assets/js/enhancements/toc.js`

## Ownership Boundary

Use this anatomy when changing the packaged Bengal theme, published docs shell,
or theme asset package. Do not treat these selectors as a new app-level Chirp UI
vocabulary.

Stable app-level Chirp UI contracts still come from:

- component descriptors in `src/chirp_ui/components.py`
- Kida macros under `src/chirp_ui/templates/chirpui/`
- generated CSS from `src/chirp_ui/templates/css/partials/`
- `src/chirp_ui/manifest.json`

The Bengal theme may compose those contracts, but it should not fork component
CSS or create a parallel design system. New app components should be added to
the Chirp UI registry instead of being hidden in theme partials.

## Application Chrome Parity

Bengal docs chrome is a real application chrome consumer, but it is not the
same contract as Chirp UI app shell chrome. Treat it as packaged theme chrome
that proves token and behavior parity without creating new app-level APIs.

Parity expectations:

- header identity, docs rail, TOC rail, search trigger, mobile nav, and theme
  controls stay separate layers,
- persistent docs navigation uses Chirp UI sidebar/nav primitives where
  practical instead of private theme navigation semantics,
- mobile navigation uses the packaged dialog fallback and keeps search reachable,
- search modal behavior remains Bengal-owned while matching the command-surface
  rhythm expected from Chirp UI chrome,
- TOC and docs rail do not starve article content at tablet widths,
- spacing, borders, elevation, color, focus, and typography read from
  `--chirpui-*` tokens or documented transitional aliases,
- repeated theme-only structure must be evaluated as a Chirp UI registry
  candidate before it becomes a public app component.

Proof for Bengal chrome changes should include package-data tests, source-doc
parity checks, and browser proof when layout, focus, mobile nav, search, theme
controls, or TOC behavior changes.

## Theme Menu

The theme menu is a native popover.

Rendered structure:

- trigger: `.theme-dropdown__button`
- trigger relationship: `popovertarget="<menu-id>"`
- popover: `.theme-dropdown__menu--popover[popover]`
- sectioning: `.theme-menu-section` fieldsets with `legend.separator`
- options: `.theme-option`
- theme mode payload: `data-appearance="system|light|dark"`

Runtime:

- `core/theme.js` initializes the stored appearance preference.
- `window.BengalTheme` exposes `get`, `set`, and `toggle`.
- Selecting `data-appearance` updates `<html data-theme="light|dark">`.
- Initialization removes stale `bengal-palette` localStorage state and clears
  any `data-palette` attribute left by older builds.
- Popover open/close, light dismiss, escape handling, and top-layer behavior are
  owned by the browser.
- JavaScript only persists state, updates active option classes, watches system
  color-scheme changes, and positions the popover relative to its trigger.

Constraints:

- Keep the menu IDs unique when rendering desktop and mobile controls.
- Do not reintroduce legacy Bengal palette controls or `data-theme-pack` alias
  metadata. Future palette/theme-pack work should use a new Chirp UI-owned
  contract rather than old Bengal names.

## Search Modal

The command-palette search surface is a native dialog rendered only when
`config.search.ui.modal` is enabled.

Rendered structure:

- dialog: `#search-modal.search-modal`
- input: `#search-modal-input.search-modal__input`
- status: `#search-modal-status[role="status"][aria-live="polite"]`
- loading: `#search-modal-loading`
- recent section: `#search-modal-recent`
- recent list: `#search-modal-recent-list[role="listbox"]`
- results region: `#search-modal-results`
- results list: `#search-modal-results-list[role="listbox"]`
- no-results state: `#search-modal-no-results`
- close hooks: `[data-close-modal]`
- triggers: `#search-trigger`, `#nav-search-trigger`, and
  `.nav-search-trigger`

Runtime:

- `core/search.js` owns index loading, search, filtering, result rendering,
  keyboard shortcuts, recent searches, and modal state.
- `window.BengalSearch` exposes core search methods and modal helpers.
- `window.BengalSearchModal` exposes `open`, `close`, and `isOpen`.
- `Cmd/Ctrl+K` and `/` open the modal when focus is not inside an input.
- Escape closes the modal.
- Arrow keys move through results and recent searches.
- Enter opens the selected result.
- Search data loads from Bengal-generated index artifacts, not from a Chirp UI
  custom site generator.

Constraints:

- Keep result HTML generated by `core/search.js` aligned with the modal
  template IDs and classes.
- Keep the modal optional; sites without modal search should still use the
  inline or full search page path.
- Do not add inline scripts to templates for modal behavior.

## Inline Search

The inline search partial is a page-embedded search surface using the same
`core/search.js` module.

Rendered structure:

- root: `#search-container.search-inline`
- variant hook: `data-variant="default|compact|full"`
- result budget: `data-max-results`
- collapsed API hint: `data-collapsed-api`
- input: `#search-input`
- status: `#search-status[role="status"][aria-live="polite"]`
- optional filters: `#search-filters`
- results: `#search-results[role="region"]`

Runtime:

- `core/search.js` initializes the search page when `#search-input` exists.
- The same search index and transformation path powers inline and modal search.

Constraints:

- Keep modal and inline IDs distinct.
- Keep the variant set narrow unless a real Bengal template consumes a new
  variant.

## Page Actions Popover

The page actions popover is a native popover rendered near docs and reference
heroes. It keeps copy, LLM text, and AI handoff actions close to the page title
without making those actions Chirp UI registry components yet.

Rendered structure:

- root: `.chirp-theme-page-actions`
- trigger: `.chirp-theme-page-actions__trigger`
- trigger relationship: `popovertarget="<menu-id>"`
- popover: `.chirp-theme-page-actions__menu[popover]`
- header: `.chirp-theme-page-actions__header`
- action item: `.chirp-theme-page-actions__item`
- copy URL hook: `data-action="copy-url"`
- copy LLM text hook: `data-action="copy-llm-txt"`
- AI handoff hook: `data-ai="<assistant-id>"`

Runtime:

- `enhancements/action-bar.js` delegates copy actions through
  `[data-action^="copy"]`.
- The same script delegates AI handoff through `[data-ai]`, fetches the page's
  LLM text URL when available, copies it to the clipboard, and opens the target
  assistant in a new tab.
- Browser popover behavior owns opening, light dismiss, escape handling, and
  top-layer placement.

Constraints:

- Keep page action hooks data-driven and shared with older action-bar surfaces.
- Keep AI assistant IDs explicit; do not infer behavior from link labels.
- Keep `rel="noopener noreferrer"` on external AI and LLM text links.
- Do not promote page actions into a Chirp UI component until the app-shell
  page-action primitive has a registry-owned contract.

## Mobile Navigation

The mobile navigation is a native dialog rendered by `base.html`.

Rendered structure:

- trigger: `.mobile-nav-toggle`
- dialog: `#mobile-nav-dialog.mobile-nav-dialog`
- close form: `.mobile-nav-header[method="dialog"]`
- action row: `.mobile-nav-actions`
- optional search bridge: `.mobile-nav-search[data-open-search]`
- close button: `.mobile-nav-close`
- nav body: `.mobile-nav-content[role="navigation"]`
- submenu list item: `li.has-submenu`
- submenu toggle: `.mobile-nav-toggle-submenu[aria-expanded]`
- footer theme menu: `.mobile-nav-footer`

Runtime:

- `enhancements/mobile-nav.js` closes the dialog after navigation clicks,
  toggles submenus, auto-expands active sections, opens search through
  `window.BengalSearchModal.open()`, and closes on backdrop clicks.
- `window.BengalNav` exposes `open`, `close`, and `toggle`.
- Browser dialog behavior owns focus trap, escape key, backdrop, and modal
  stacking.

Constraints:

- Keep navigation links and submenu toggles separate. The split-button pattern
  lets a section link navigate while the chevron expands the submenu.
- Keep search bridging optional and gated by modal search config.
- Do not move mobile nav behavior into inline template scripts.

## Docs Navigation And TOC

Docs navigation is theme chrome over Bengal page context and Chirp UI sidebar
macros.

Docs navigation structure:

- `partials/docs-nav.html` imports `chirpui/sidebar.html`.
- root sidebar class: `.chirp-theme-docs-nav`
- section class: `.chirp-theme-docs-nav__section`
- branch link class: `.chirp-theme-docs-nav__branch-link`
- leaf link class: `.chirp-theme-docs-nav__leaf-link`
- current path comes from `page.href` or `page._path`
- tree data comes from `get_nav_context()` or `get_nav_tree()`

TOC structure:

- root: `.toc-sidebar[data-bengal="toc"]`
- progress bar: `.toc-progress-bar`
- nav: `.toc-nav[data-toc-mode="normal"]`
- scroll area: `.toc-scroll-container`
- tree: `.toc-items[role="tree"]`
- node: `.toc-item[role="treeitem"][data-level]`
- collapsible group: `details.toc-group`
- top-level section marker: `data-toc-section`
- link: `.toc-link[data-toc-item="#heading-id"]`
- metadata: `.toc-metadata`

Runtime:

- `enhancements/toc.js` tracks active headings, scroll progress, native
  `<details>` state, keyboard navigation, smooth scroll, and persisted compact
  state.
- `window.BengalTOC` exposes `init`, `cleanup`, `updateActiveItem`,
  `expandAll`, and `collapseAll`.
- Track pages may use `data-track-filtering="true"` on `.toc-sidebar`; the TOC
  script preserves nested groups inside the active track section.

Constraints:

- Keep raw HTML TOC fallback (`toc | safe`) limited to Bengal-provided already
  rendered TOC markup.
- Keep generated heading IDs and `data-toc-item` values in sync.
- Do not convert the docs TOC into a Chirp UI app component unless the same
  contract is promoted into the registry.

## Theme Tabs

Bengal theme tabs are docs-site content tabs, separate from Chirp UI's
`tabs(...)`, `tabs_container(...)`, and route tabs.

Rendered structure expected by `enhancements/tabs.js`:

- container: `.tabs` or `.code-tabs`
- nav list: `.tab-nav`
- nav item: `.tab-nav li`
- nav link: `.tab-nav a`
- pane: `.tab-pane`
- target hook: `data-tab-target="<pane-id>"`
- optional sync group: `data-sync="<group>"`
- optional sync value: `data-sync-value="<value>"`
- optional copy hook: `.copy-btn[data-copy-target="<code-id>"]`

Runtime:

- CSS in `components/tabs-native.css` provides the base `:target` behavior.
- `enhancements/tabs.js` adds sync groups, localStorage persistence, keyboard
  navigation, delegated clicks, and code-copy behavior.
- `window.BengalTabs` exposes `sync`, `switch`, and `restoreSync`.

Constraints:

- Do not conflate Bengal content tabs with Chirp UI route tabs.
- Keep sync groups explicit through `data-sync`; do not infer sync from labels.
- Keep code-copy targets text-based and avoid copying HTML.

## Evidence Ledger

This ledger applies the interactive anatomy contract from
[DESIGN-interactive-anatomy.md](../decisions/interactive-anatomy.md). It is a
docs/tests contract for packaged Bengal theme chrome, not descriptor or
manifest metadata.

| Field | Packaged Bengal theme controls |
| --- | --- |
| Surface | Theme menu, search modal, inline search, page actions popover, mobile navigation, docs navigation, TOC, and Bengal content tabs in `chirp-theme`. |
| Label | `stable` packaged theme contract; not a Chirp UI registry component API. Repeated shell patterns remain candidates for later registry promotion. |
| Anatomy | Theme controls own native popover triggers/menus and `data-appearance`; search owns modal/inline IDs, status regions, result lists, and close hooks; page actions own popover trigger/menu and `data-action`/`data-ai` hooks; mobile nav owns native dialog, search bridge, submenu toggles, nav body, and footer theme controls; docs nav/TOC own sidebar, tree, heading, and progress hooks; content tabs own `.tabs`/`.code-tabs`, nav links, panes, sync hooks, and copy hooks. |
| Native semantics | Theme and page actions use native `[popover]`; search modal and mobile nav use native `<dialog>`; inline search uses search input plus status/result regions; docs nav uses navigation/sidebar semantics; TOC uses tree/treeitem semantics; content tabs are docs-site tab surfaces and must not be conflated with Chirp UI route tabs. |
| Keyboard | Browser popover/dialog behavior owns Escape, light dismiss, and modal stacking for native surfaces; search owns `Cmd/Ctrl+K`, `/`, Escape, Arrow keys, and Enter; mobile nav owns submenu toggles and closes after navigation; TOC and content tabs own their script-level keyboard behavior. |
| Focus | Native dialogs/popovers own browser focus behavior where applicable; search opens from global/mobile triggers and focuses the modal workflow; mobile nav keeps search reachable from the dialog; TOC tracks active headings; content tab focus follows delegated link activation. |
| Runtime | Requires packaged Bengal static assets: `core/theme.js`, `core/search.js`, `enhancements/action-bar.js`, `enhancements/mobile-nav.js`, `enhancements/tabs.js`, and `enhancements/toc.js`; search data loads from Bengal-generated index artifacts. |
| Motion | Popover/dialog transitions and content-tab behavior are CSS/static-asset owned; reduced-motion expectations follow packaged theme CSS and Chirp UI transition-token governance where Chirp UI tokens are used. |
| Responsive and overflow | Browser proof covers rail/header/mobile chrome across phone, tablet, compact desktop, and desktop widths; page actions and API/search surfaces are checked for viewport containment and no document-level horizontal overflow. |
| Security and escaping | Templates render IDs, URLs, labels, and data hooks through normal template escaping; TOC raw HTML fallback is limited to Bengal-provided already-rendered markup; page actions keep external links `rel="noopener noreferrer"`; copy and AI handoff behavior reads explicit `data-action`, `data-url`, and `data-ai` hooks rather than inline script payloads. |
| Performance | Theme scripts use bounded initialization and delegated events for copy/AI actions; search owns index loading and filtering; TOC owns active-heading and scroll-progress behavior; no Chirp UI component runtime or manifest projection is implied by these theme hooks. |
| Proof | `tests/test_bengal_theme_package.py` checks packaged partial/static-asset hook parity, page-action hooks, search hooks, mobile nav hooks, TOC hooks, and content-tab hooks; `tests/browser/test_bengal_docs_chrome.py` checks responsive chrome, mobile nav, native theme popover, page actions popover, API/search surfaces, TOC top action, and no document horizontal overflow; `tests/test_docs_site.py` checks published docs bridge back to this guide. |
| Residual risk | Automated tests cover packaged hooks, rendered semantics, browser behavior, responsive layout, and overflow, but no manual screen-reader or assistive-technology proof is claimed. Theme-owned selectors should not be promoted into registry APIs without a separate Chirp UI component plan and proof. |

## Proof

Focused contracts live in `tests/test_bengal_theme_package.py`:

- required theme partials and assets are packaged
- palette controls map legacy Bengal names to curated Chirp UI theme-pack
  families
- theme controls, search modal, inline search, mobile nav, docs TOC, and theme
  tabs keep their template/static JS hook parity
- page actions keep copy, LLM text, and AI handoff hooks aligned with
  `enhancements/action-bar.js`
- built docs output includes non-empty header and mobile navigation links

Published site coverage lives in `tests/test_docs_site.py`, which ensures the
site mirror points back to this canonical guide and the docs IA migration matrix
names every published docs source.

Browser coverage lives in `tests/browser/test_bengal_docs_chrome.py`, which
checks responsive docs chrome, mobile nav, native theme popovers, page actions,
API/search surfaces, TOC actions, footer placement, and horizontal overflow.
