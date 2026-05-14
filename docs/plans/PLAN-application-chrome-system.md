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

Evaluation docket:

| Candidate | Evidence Required | Accept If | Reject If | Collateral If Accepted |
|---|---|---|---|---|
| `object_header` | Two consuming apps repeat breadcrumbs, title, metadata, actions, and route-row placement with existing primitives. | It removes repeated boilerplate while preserving link-native routes and clear slot ownership. | It mostly aliases `page_header`, `entity_header`, `breadcrumbs`, and `action_strip`. | Descriptor, macro, CSS partial, generated CSS, manifest, generated options, examples, published docs, browser proof, changelog. |
| `chrome_frame` | Two consuming apps repeat the same shell region boundaries and overflow behavior beyond current `app_shell` and layout primitives. | The owned layer is explicit and does not hide product-specific navigation in generic slots. | It becomes a mega-shell or duplicates `app_shell`, `sidebar`, `drawer`, `tray`, and `route_tabs`. | Descriptor, macro, CSS partial, generated CSS, manifest, generated options, recipes, docs, browser proof, changelog. |
| `workspace_shell` | Two consuming apps need the same workspace/sidebar/tab/page-tool contract and cannot express it with filesystem layouts plus current shell blocks. | It improves the Chirp shell contract across routes without app-local wrapper glue. | It encodes one product's IA or requires JavaScript-managed responsive overflow. | Shell contract docs, migration notes, app examples, HTMX/browser proof, generated docs where public API changes. |

Docket entry template:

```text
Candidate:
Consumers:
Repeated shape:
Existing primitives tried:
Missing contract:
Accepted / rejected:
Required proof:
Collateral:
Not-now spillover:
```

Current evidence log:

| Evidence | Counts As Real Consumer? | Composite Signal |
|---|---:|---|
| Dense object chrome showcase recipes | No | Good documentation evidence for layered composition; not enough for `object_header`. |
| Rail-to-drawer showcase recipe and browser fixture | No | Good responsive proof for existing primitives; not enough for `application_chrome`. |
| Application chrome gauntlet families | No | Good browser stress evidence across product shapes; not enough for a stable shell API. |
| Bengal docs chrome | Partial | Real packaged-theme consumer for token/layout parity, but not the same contract as Chirp app shell chrome. |
| Workspace consumer browser fixture | Yes | Proves a filesystem-style app shell can compose brand, sidebar, route tabs, breadcrumbs, command trigger, page toolbar, shell actions, and inner HTMX fragments without a new chrome macro. |
| Admin consumer browser fixture | Yes | Proves a second route family can repeat the recipe with different tabs, actions, copy, and page tools; the repeated pain is shell/OOB response wiring, not visual composition. |

Consumer adoption findings from the first real-consumer wave:

- The existing `app_shell_layout`, `sidebar`, `route_tabs`, `breadcrumbs`,
  `command_palette_trigger`, `command_bar`, `btn`, and `block` primitives are
  enough to build two app chrome consumers without adding
  `application_chrome()`.
- Shell navigation and page-root tab navigation are different HTMX contracts.
  Shell-targeted requests should return a full page response with OOB shell
  region updates; tab-targeted requests can return a `#page-root` fragment.
- Local page tools need fragment-island behavior. Buttons/forms that target
  `#page-content-inner` must clear inherited shell `hx-select`, using the
  existing `hx-select="unset"` / `hx-disinherit="hx-select"` pattern.
- The first failure mode was not spacing, tokens, or a missing visual macro.
  It was target ownership: treating every `HX-Request` as a page-root request
  made shell-level navigation empty-swap content.
- The second failure mode was persistent shell metadata: shell actions live
  outside `#page-content`, so shell navigation needs an OOB shell-actions
  update when route-scoped actions change.

Consumer adoption proof now covers:

| Contract | Workspace Consumer | Admin Consumer | Boundary Proof |
|---|---|---|---|
| Persistent shell identity | `Consumer Chrome` brand and workspace sidebar state | same brand with admin sidebar state | shell navigation keeps one `#main` and one `#page-content` |
| Route-backed page chrome | overview/runs/settings route tabs | access/jobs/audit route tabs | tab clicks target only `#page-root` |
| Route-scoped shell actions | `New run` / `Refresh` | `Invite member` / `Audit` | shell navigation updates actions by OOB response |
| Command surface | workspace command trigger opens and focuses palette | admin search trigger is reachable | palette remains page-local, not shell-owned |
| Page tools | filter/refresh/export toolbar | review/suspend/export toolbar | inner filter targets only `#page-content-inner` |
| Responsive sanity | workspace browser proof at desktop and phone widths | admin browser proof at phone width | no duplicate roots after HTMX swaps |

## Composite Decision Review: Consumer Adoption Wave 1

Date: 2026-05-13

Decision: keep application chrome recipe-level. Do not add
`application_chrome()`, `workspace_shell()`, `chrome_frame()`, or
`object_header()` from this evidence wave.

Why:

- Two consumers repeated the same layered app chrome shape, but the visual
  composition remained readable with existing primitives.
- The only repeated hard part was response ownership across shell, page-root,
  and inner-fragment HTMX targets.
- That problem is a shell/OOB contract issue. A visual composite would hide the
  failure mode instead of making route handlers return the right response
  shape.
- The route tabs, breadcrumbs, command trigger, command bar, shell actions,
  sidebar, and block primitives all held their current contracts under browser
  proof.

Candidate review:

| Candidate | Decision | Evidence | Follow-up |
|---|---|---|---|
| `application_chrome()` | Reject | The repeated shape spans app identity, sidebar, route tabs, page tools, shell actions, and local fragments. One macro would become a mega-shell. | Keep recipe docs and browser fixtures. |
| `workspace_shell()` | Defer | Two consumers share route tabs and page tools, but differ in IA, actions, and content. | Revisit only after a real filesystem app shows the same wrapper glue is repeated across many routes. |
| `chrome_frame()` | Defer | The target-boundary problem is real, but the owned layer is not a visual frame. | Consider a narrow shell response/OOB helper outside this plan if route code repeats. |
| `object_header()` | Reject for this wave | The consumers are workspace/admin route families, not object-detail headers. | Wait for object-page repetition with metadata/actions/route row evidence. |

Accepted next investments:

- Keep the consumer browser fixtures as regression proof for shell/page-root
  target ownership.
- Prefer docs and examples that teach `HX-Target` branching and OOB shell
  region updates.
- If more consumers repeat the same route-handler boilerplate, evaluate a
  shell-response helper before evaluating a visual macro.

Not accepted:

- Component registry work for a new app chrome composite.
- CSS partials for a new chrome wrapper.
- Manifest/generated-options/changelog work for any new public macro.

## Shell Response Helper Decision: Wave 2

Date: 2026-05-13

Decision: keep shell response branching as a documented recipe for now. Do not
promote a public `chirp_ui` helper in this wave.

Evidence:

- Server contract tests now pin the three response shapes:
  `HX-Target: main`, `HX-Target: page-root`, and local inner-fragment targets.
- Browser proof now verifies route-scoped shell actions replace through
  `#chirp-shell-actions` OOB during boosted shell navigation.
- The private browser-fixture helper reduced the repeated condition to:
  `bool(HX-Request) and HX-Target == <target>`.
- The helper did not reveal a new Chirp UI component, CSS, registry, manifest,
  or macro contract. It is route-handler glue.

Decision matrix:

| Candidate | Decision | Reason |
|---|---|---|
| Public Python helper in `chirp_ui` | Defer | The current need is proven in browser fixtures, not yet in a production/copyable filesystem app. |
| Chirp framework helper | Defer to Chirp evidence | `HX-Target` response selection is closer to routing/page-composition than to component rendering. |
| Docs recipe | Accept | It solves the immediate ambiguity without expanding public API. |
| Visual chrome macro | Reject | The issue is response ownership, not markup composition. |

Promotion trigger:

- three route families repeat the same branching and OOB-context boilerplate,
- the helper can be named around response ownership rather than app chrome,
- docs can show migration from the recipe to the helper without changing
  template contracts,
- tests cover shell, page-root, and local-fragment response shapes before the
  helper is public.

## Filesystem Adoption Decision: Wave 3

Date: 2026-05-13

Decision: make filesystem-mounted app pages the recommended adoption path for
application chrome. Keep manual route helpers and visual chrome composites
deferred.

Evidence:

- `tests/fixtures/filesystem_chrome/` is a copyable mounted app with
  `_layout.html`, `_context.py`, `_meta.py`, section registration, route tabs,
  shell actions, command trigger, page tools, and a local fragment endpoint.
- Server tests prove the mounted fixture returns the right response shape for
  full navigation, boosted shell navigation, route-tab navigation, and local
  fragments.
- Browser tests prove sidebar navigation, route-tab swaps, shell-actions OOB
  replacement, command-palette focus, local fragment swaps, horizontal overflow
  sanity, and singleton `#main` / `#page-content` / `#page-root` ownership.
- The mounted app no longer needs per-route `HX-Target` branching for normal
  page responses. Chirp's page-shell contract maps `#main`, `#page-root`, and
  `#page-content-inner` to the right blocks.

What changed from Wave 2:

- Manual-route consumers still need target branching.
- Filesystem-mounted consumers can express the same contract declaratively with
  layout metadata, `Section` registration, and page blocks.
- Shell-actions OOB is automatic for targets that trigger shell updates.
- The ergonomic gap moved from "we need a helper" to "we need clearer
  filesystem recipes and proof."

Decision matrix:

| Candidate | Decision | Reason |
|---|---|---|
| Public `chirp_ui` response helper | Reject for filesystem pages | The mounted route contract already chooses the response shape. |
| Public visual app chrome macro | Reject | The fixture composes existing primitives without visual-contract drift. |
| Upstream Chirp routing/helper work | Defer | Only manual routes still show helper pressure; filesystem pages are already covered. |
| Docs and fixture adoption | Accept | This gives app authors a copyable path with executable proof. |

Next promotion trigger:

- a production/copyable app repeats the filesystem block structure but still
  needs wrapper glue outside the documented recipe,
- the repeated glue belongs to Chirp UI rather than Chirp routing,
- proof shows existing page blocks and shell regions cannot express the
  contract cleanly.

Open consumer evidence still required before composite work:

- one production or copyable filesystem-routed Chirp app beyond the browser
  fixture using persistent shell plus route-backed object/workspace tabs,
- one additional app or packaged integration repeating the same missing shape
  after the shell/OOB guidance above has been applied,
- notes showing which existing primitives were tried and where boilerplate or
  contract drift remained,
- browser proof that the repeated shape fails recipe-level composition before
  a macro is proposed.

## Release Readiness Ledger

Every application chrome slice should close with a short ledger in the PR
description or plan update:

| Slice | Required Proof | Required Collateral |
|---|---|---|
| Docs bridge | docs source tests and `uv run poe build-docs-check` | `docs/NAVIGATION.md`, site pattern page, docs IA map |
| Rail-to-tray recipe | render semantics plus browser proof at 320, 390, 768, 1024, and 1280 | recipe fixture/example, responsive notes, focused tests |
| Chrome gauntlet | browser family checks for context, primary action, command focus, route-tab scroll, badges, and overflow | browser fixtures, test coverage, visual audit references |
| Rhythm audit | visual-audit docs/tests and browser proof when markup changes | `docs/VISUAL-AUDIT-SHOWCASE.md`, visual audit page when needed |
| Bengal parity | theme package tests plus browser proof for layout/focus changes | Bengal anatomy docs, theme parity docs, package data checks |
| Composite promotion | full component contract proof | descriptor, macro, CSS partial, generated CSS, manifest, generated options, docs, examples, browser proof, changelog |

Use `uv run poe ci` when a slice touches public macro/API, generated outputs,
CSS, packaging, or multiple runtime surfaces. Narrower checks are acceptable for
docs-only or browser-fixture-only slices when the PR names the checks and the
remaining browser/environment gap.

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
