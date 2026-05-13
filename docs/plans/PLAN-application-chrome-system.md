# chirp-ui: Application Chrome System

Status: active plan
Date: 2026-05-13
Depends on:

- [PLAN-navigation-contract-application.md](PLAN-navigation-contract-application.md)
- [PLAN-dense-object-chrome-next.md](PLAN-dense-object-chrome-next.md)
- [../UI-LAYERS.md](../UI-LAYERS.md)
- [../NAVIGATION.md](../NAVIGATION.md)
- [../DENSE-NAVIGATION-RECIPES.md](../DENSE-NAVIGATION-RECIPES.md)
- [../RESPONSIVE.md](../RESPONSIVE.md)
- [../VISUAL-AUDIT-SHOWCASE.md](../VISUAL-AUDIT-SHOWCASE.md)

## Goal

Make Chirp UI excellent at modern application chrome: layered shells, rails,
trays, object context, command surfaces, route surfaces, page tools, and
responsive overflow that compose cleanly without utility classes or a premature
mega-shell macro.

This is a system plan, not a request to add `application_chrome()`.

## Research Inputs

- Android adaptive navigation switches between navigation bar and rail by
  window size class rather than freezing one shell shape:
  <https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation>
- Carbon treats UI shell as cooperating header, left panel, and right panel
  regions:
  <https://carbondesignsystem.com/components/UI-shell-header/style/>
- Fluent separates inline and overlay drawers and documents modality,
  scrolling, anatomy, placement, and responsive drawer behavior:
  <https://fluent2.microsoft.design/components/web/react/core/drawer/usage>
- Apple split views and sidebars emphasize panes, current selection, compact
  fallbacks, and reveal/hide controls:
  <https://developer.apple.com/design/Human-Interface-Guidelines/split-views>
  and <https://developer.apple.com/design/Human-Interface-Guidelines/sidebars>
- Atlassian's navigation redesign targets one coherent navigation model across
  products:
  <https://www.atlassian.com/blog/design/designing-atlassians-new-navigation>
- Skeleton's Svelte toolkit validates the primitive shape: app shell slots,
  app bar, app rail, drawer, route-link tabs, and responsive sidebar-to-drawer
  recipes, while relying on Tailwind utility classes Chirp UI intentionally
  does not adopt:
  <https://v1.skeleton.dev/components/app-shell>,
  <https://v2.skeleton.dev/components/app-rail>,
  <https://v2.skeleton.dev/utilities/drawers>

## Steward Synthesis

Consulted stewards: Core Registry/API, Template/CSS/Behavior, Tests,
Documentation, Examples/Showcase, Planning, Published Site, Build Projection,
and Bengal Theme.

Convergence:

- Application chrome is important enough to become a first-class system.
- The first deliverables should be contracts, recipes, browser gauntlets, and
  token/rhythm proof.
- Existing primitives should be strengthened before adding new public macros.
- Rail, tray, drawer, sidebar, route tabs, command triggers, and badge states
  need in-context browser proof, not only isolated component proof.
- Published docs must expose the system without inventing site-only component
  facts.
- Bengal docs chrome is a real consumer, but it is not the same contract as
  Chirp app shell chrome.

Minority reports:

- A small `object_header` or `chrome_frame` may become useful later.
- Defer it until at least two real consuming apps repeat the same shape and
  existing primitives are proven insufficient.

## Five-Rock Status

| Rock | Status | Decision |
|---|---|---|
| Chrome Layer Model | Residual contract work | Current layer model exists; add app-chrome bridge, decision tables, and rendered semantic tests. |
| Rail And Tray Design Contracts | Active implementation backlog | Add rail-to-tray recipes and browser proof using existing `sidebar`, `nav_tree`, `drawer`, and `tray`. |
| Modern Visual Rhythm | Active audit backlog | Treat rhythm as token/control-size/elevation proof, not utility spacing classes. |
| Responsive Chrome Gauntlet | Active test backlog | Build a recipe-family browser gauntlet before any composite promotion. |
| Recipe First, Composite Later | Accepted boundary | No `application_chrome()`, `object_chrome()`, `workspace_header()`, or `dense_nav_frame()` without real app evidence. |

## Contract Map

| Layer | Job | Current Chirp UI surface | Next proof |
|---|---|---|---|
| App identity | Persistent product/app orientation | `app_shell`, `navbar`, logo/title slots | Published app-chrome docs route. |
| Product rail | Broad app/workspace movement | `sidebar`, `primary_nav`, `nav_tree` | Rail-to-tray recipe and browser proof. |
| Secondary rail | Hierarchy, saved views, nearby scope | `nav_tree`, `saved_view_strip`, `scope_switcher` | Recipe-family gauntlet. |
| Object context | Current object/path/actions | `breadcrumbs`, `page_header`, `inline_counter`, `badge`, `dropdown_menu` | Real app repetition before composite. |
| Local routes | URL-backed object/workspace views | `route_tabs` | Gauntlet scroll and active-route proof. |
| Page tools | Filters, sort, display, refresh, export | `command_bar`, `filter_bar`, buttons, dropdowns | Mixed-control rhythm proof. |
| Command overlay | Search, jump, create, actions | `command_palette_trigger`, `command_palette` | Focus/open proof inside full chrome. |
| Overlay chrome | Phone fallback, inspectors, supplemental panels | `drawer`, `tray`, modal/dialog primitives | In-context focus, close, overflow proof. |

## Ranked Backlog

### 1. Application Chrome Docs Bridge

Add a thin bridge from canonical docs to the application chrome system:

- `docs/NAVIGATION.md`: layer and rail/tray decision table.
- `docs/UI-LAYERS.md`: vocabulary boundary, if needed.
- `site/content/docs/patterns/navigation.md`: published summary sourced from
  canonical docs.
- `docs/DOCS-IA-MIGRATION.md`: published-page source map.

Proof:

- docs tests pin canonical links and recipe-first boundary,
- `uv run poe build-docs-check`.

### 2. Rail-To-Tray Recipe

Create a copyable recipe using existing primitives only:

- persistent rail/sidebar on desktop/tablet,
- drawer or tray fallback on phones,
- command trigger remains reachable,
- route links remain link-native,
- current route state is not duplicated ambiguously.

Proof:

- render test for landmarks and link/button semantics,
- Playwright at 320, 390, 768, 1024, and 1280,
- no document-level horizontal overflow,
- tray/drawer opens, closes by click and Escape, and returns focus.

### 3. Application Chrome Gauntlet

Add a browser gauntlet covering representative recipe families:

- dense object,
- cloud/control-plane,
- suite work hub,
- knowledge/workbench,
- business object console,
- Bengal docs chrome when the packaged theme is in scope.

Proof:

- current context visible,
- primary action reachable,
- route tabs scroll instead of wrapping tall,
- rail/tray fallback works,
- command trigger opens and focuses search,
- reserved/loading badges do not announce bad counts,
- HTMX swaps preserve shell/page boundaries,
- no unintended horizontal overflow at stress widths.

### 4. Chrome Rhythm Audit

Audit the visual system before adding API:

- app shell,
- sidebar/nav tree,
- primary nav,
- route tabs,
- command bar/action strip,
- drawer/tray,
- Bengal header/docs rail/TOC/search/theme controls.

Proof:

- token/control-height/elevation inventory,
- visual audit checklist update,
- browser checks for overlap, touch target size, long labels, theme states.

### 5. Composite Evaluation Docket

Only after two real consuming apps repeat the same missing shape:

- compare extending `entity_header` / `page_header`,
- compare a narrow `object_header`,
- reject generic `application_chrome` unless the layer it owns is explicit.

Required promotion proof:

- descriptor and manifest entry,
- emitted classes in CSS and registry,
- strict-undefined render cases,
- slot parity,
- generated `COMPONENT-OPTIONS.md`,
- examples and published docs,
- browser responsive proof,
- changelog fragment.

## Not Now

- `application_chrome()`
- `object_chrome()`
- `workspace_header()`
- `dense_nav_frame()`
- product-specific shell clones
- utility classes for density, hiding, spacing, alignment, or overflow
- JavaScript-managed responsive overflow
- shortcut engine
- persisted rail personalization
- async counter protocol beyond reserved/loading badge states
- new manifest schema fields for chrome layers

## Steward Notes

Accepted findings:

- Keep the registry untouched until public macro, param, emitted class, token,
  runtime requirement, or slot contract changes.
- Browser proof must validate full chrome compositions, not only isolated
  components.
- Published docs should expose Application Chrome as a pattern sourced from
  canonical docs, not as site-only API.
- Bengal theme chrome needs its own parity and browser proof because static
  docs chrome is not identical to Chirp app shell chrome.

Deferred findings:

- `object_header` / `chrome_frame` composite evaluation.
- Bengal built-site browser gauntlet until the next theme-focused slice.
- Package inventory ratchet for Bengal assets.

Required proof for this plan slice:

- docs/index tests,
- docs-site source mapping tests,
- `uv run poe build-docs-check`.
