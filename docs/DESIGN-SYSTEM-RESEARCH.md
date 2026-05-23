# Design System Research

**Status:** Research note  
**Date:** 2026-05-23  
**Scope:** External design-system research, Chirp UI product opinion, Bengal shell implications, and pre-1.0 positioning gates

## Goal

Use current design-system practice to sharpen Chirp UI's own opinion without
turning it into a Python clone of any React, Tailwind, or enterprise design
system.

The target position is:

> Chirp UI is a Python-native contract design system for server-rendered apps:
> registry-cited components, safe Kida macros, generated CSS, HTMX-aware
> behavior, Bengal-ready themes, and agent-groundable manifests.

This research note is sequencing input. It does not authorize new public macro
parameters, descriptor fields, manifest schema fields, component names, theme
entry points, dependencies, or cascade-layer changes.

## Research Inputs

Primary sources:

- [shadcn/ui components](https://ui.shadcn.com/docs/components)
- [shadcn/ui blocks](https://ui.shadcn.com/blocks)
- [shadcn/ui registry](https://ui.shadcn.com/docs/registry)
- [shadcn/ui CLI](https://ui.shadcn.com/docs/cli)
- [shadcn/ui namespaces](https://ui.shadcn.com/docs/registry/namespace)
- [shadcn/ui MCP server](https://ui.shadcn.com/docs/mcp)
- [shadcn/ui theming](https://ui.shadcn.com/docs/theming)
- [Material Design 3 components](https://m3.material.io/components)
- [Material Design 3 navigation drawer](https://m3.material.io/components/navigation-drawer/overview)
- [Material Design 3 navigation rail](https://m3.material.io/components/navigation-rail/overview)
- [Radix Primitives introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [Base UI about](https://base-ui.com/react/overview/about)
- [React Aria](https://react-aria.adobe.com/)
- [Carbon components overview](https://carbondesignsystem.com/components/overview/components/)
- [Carbon data table](https://carbondesignsystem.com/components/data-table/usage/)
- [Carbon UI shell left panel](https://carbondesignsystem.com/components/UI-shell-left-panel/usage/)
- [Carbon UI shell right panel](https://carbondesignsystem.com/components/UI-shell-right-panel/usage/)
- [Android adaptive navigation](https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation)
- [Atlassian components](https://atlassian.design/components)
- [Atlassian navigation redesign](https://www.atlassian.com/blog/design/designing-atlassians-new-navigation)
- [GOV.UK Design System get started](https://design-system.service.gov.uk/get-started/)
- [GOV.UK accessibility strategy](https://design-system.service.gov.uk/accessibility/accessibility-strategy/)
- [U.S. Web Design System developer docs](https://designsystem.digital.gov/documentation/developers/)
- [Shopify Polaris components](https://polaris.shopify.com/components)

Internal sources:

- [VISION.md](VISION.md)
- [PRIMITIVES.md](PRIMITIVES.md)
- [DENSE-NAVIGATION-SYNTHESIS.md](DENSE-NAVIGATION-SYNTHESIS.md)
- [DESIGN-layout-affinity.md](DESIGN-layout-affinity.md)
- [plans/PLAN-application-chrome-system.md](plans/PLAN-application-chrome-system.md)
- [plans/PLAN-bengal-chirpui-library-contract.md](plans/PLAN-bengal-chirpui-library-contract.md)

## Benchmark Matrix

| System | Strongest lesson | Chirp UI should borrow | Chirp UI should not copy |
|---|---|---|---|
| shadcn/ui | Registry distribution, local ownership, CLI install, private namespaces, MCP installability. | Treat registry, manifest, CLI, docs, and agent access as product surfaces. | Tailwind utility authoring, copied source as the normal update model, React-specific assumptions. |
| Radix Primitives | Accessible unstyled behavior primitives with open component parts and consistent APIs. | Anatomy-level contracts, part ownership, state attributes, focus/keyboard seriousness. | React runtime ownership or headless behavior that leaves CSS and layout entirely app-owned. |
| Base UI | Headless accessible primitives, explicit composability, browser/platform testing claims. | Clear component anatomy, broad interaction proof, explicit browser support posture. | Styling-neutral posture; Chirp UI is intentionally styled and token-backed. |
| React Aria | Deep accessibility, internationalization, adaptive interactions, high/low-level API escape paths. | Acceptance criteria for device, screen reader, keyboard, focus, locale, and RTL behavior. | Hook-based state ownership and React-only context patterns. |
| Carbon | UI shell as cooperating header, left panel, and right panel regions with independent but coordinated contracts. | Shell layer vocabulary, accessibility status ledgers, independent panels that still compose. | Enterprise-platform rigidity or one shell shape for all docs/apps. |
| Android Material adaptive navigation | Navigation bar/rail/drawer selection changes by window size and posture. | Adaptive shell decisions based on available space, not fixed desktop-first markup. | Mobile-native component names or JS-managed responsive switching when CSS and HTML can do it. |
| Atlassian navigation | Unified navigation across products must balance consistency and product-specific needs. | One navigation model with clear escape valves and evidence gates. | A one-size-fits-all shell or over-customizable product chrome. |
| GOV.UK | Components and patterns publish research/testing evidence and prioritize real user impact. | Evidence labels, accessibility concern severity, user-research/readiness language. | Government-service visual style or pace; Chirp UI serves app builders with faster iteration. |
| USWDS | Components, patterns, tokens, utilities, templates, maturity, accessibility, and performance docs are all first-class. | Maturity and performance documentation around shipped surfaces. | Utility-class scale; Chirp UI's no-utility rule is a core differentiator. |
| Shopify Polaris | Product-domain components, deprecation clarity, merchant-task language, admin app density. | Domain-shaped guidance for admin/workspace use cases and explicit deprecated surface lists. | Product-specific admin assumptions or deprecation churn without migration proof. |

## Component/Feature/Primitive Parity Matrix

Legend:

- `Strong`: first-class documented surface.
- `Partial`: supported through lower-level pieces, recipes, or narrower
  component families.
- `Gap`: no clear first-class equivalent in the cited system.
- `N/A`: not the system's job.

This matrix is a requirements proxy, not promotion evidence. It identifies
where Chirp UI is already differentiated, where it should mature, and where
copying another system would violate the registry-first/no-utility-class
strategy.

| Surface | Chirp UI Today | shadcn/ui | Material Design 3 | Carbon | Shopify Polaris | Atlassian Design System | Chirp UI Strategy |
|---|---|---|---|---|---|---|---|
| Distribution and discovery | Strong: Python package, registry descriptors, manifest, `find`, Bengal package data. | Strong: components, blocks, registry schema, CLI install, namespaces, MCP. | Partial: design guidance and platform implementations, not one web package contract. | Strong: React/Web Components, Storybook, component status. | Strong: React/Web Components direction, domain docs, tokens/icons. | Strong: packages, tokens, components, product guidance. | Make registry/manifest/find feel as productized as shadcn without copied-source ownership. |
| Layout primitives | Strong: `stack`, `cluster`, `grid`, `frame`, `block`, layout macros, no utility vocabulary. | Partial: layout mostly Tailwind/CSS plus blocks; primitives are app-owned. | Partial: adaptive layout guidance, app bars, rails/drawers, platform scaffolds. | Strong: grid, UI shell, structured layout guidance. | Strong: `Box`, stacks, grids, layout, page. | Strong: primitives, grid, page layout, side nav/aside guidance. | Keep no-utility-class primitives as a core differentiator; add examples before new layout API. |
| App/site shell | Partial: `app_shell`, `site_shell`, `workspace_shell`, recipes, shell/OOB contracts. | Strong in blocks: dashboards with sidebar/header/table/chart composition. | Strong: top app bars, navigation rail/drawer/bar patterns. | Strong: UI shell header, left panel, right panel. | Partial: `Page`; `Frame`, `Navigation`, `Top bar` are deprecated in Polaris React. | Strong: page layout and navigation system direction. | Stay recipe-first; promote only smaller repeated contracts or a narrow shell after reference implementations. |
| Navigation hierarchy | Strong primitives: `sidebar`, `primary_nav`, `nav_tree`, `route_tabs`, breadcrumbs. | Strong: Sidebar, Navigation Menu, Breadcrumb, Tabs, Pagination. | Strong: drawers, rails, bars, tabs. | Strong: UI shell side nav, breadcrumb, tabs, tree view feature flag. | Partial: tabs, pagination, links, resource lists; primary app nav is not the current core React direction. | Strong: navigation consolidation around menu/flyout/expandable menu ideas. | Mature linked branch semantics and responsive fallback only through reference evidence. |
| Page header and actions | Partial: `page_header`, `page_hero`, headers, `action_bar`, `share_menu`; no `page_actions`. | Partial: page actions are block/app composition with Button/Dropdown/Command. | Partial: top app bars, buttons, FABs, menus. | Partial: shell header and data-table toolbar patterns, not generic page actions. | Strong domain precedent: `Page` owns title and page-level actions; `Page actions` is deprecated. | Strong product pattern precedent: page layout/header/actions. | Investigate a narrow page-actions primitive, but do not hide it inside a mega-shell. |
| Forms and validation | Strong: form, field, inputs, error summary, validation helpers. | Strong: Field, Input, Checkbox, Select, Combobox, Date Picker, OTP, etc. | Strong: text fields, selection controls, sliders, date/time patterns. | Strong: form controls, dropdowns, date picker, validation status. | Strong: merchant/admin form controls and form layout. | Strong: form and field surfaces. | Keep safe attributes, strict undefined, and server-rendered form ergonomics as differentiators. |
| Overlays and command surfaces | Strong: modal, drawer, tray, dropdown, command palette/bar, popovers through existing components. | Strong: Dialog, Sheet, Drawer, Popover, Command, Dropdown, Menubar, Tooltip. | Strong: dialogs, menus, sheets, tooltips. | Strong: modal/menu/popover/toggletip and shell panels. | Partial: Popover/Tooltip; Modal/Sheet are deprecated in Polaris React. | Strong: modal, popup, menu, blanket/focus patterns. | Continue anatomy ledgers before adding behavior-bearing APIs. |
| Dense data and object browsing | Partial/strong: `table`, `params_table`, `resource_index`, cards, filters; no full enterprise data-table engine. | Strong recipe level: Data Table, Table, Chart, dashboard blocks. | Partial: lists/cards; data tables are not a central M3 web primitive. | Strong: data table with selection, expansion, toolbar, pagination, AI label. | Strong: Data table, Index table, Resource list, Index filters. | Strong/partial: product data tables and dynamic table patterns. | Prioritize reference/API cards, resource indexes, filter rails, and lightweight tables before a heavy grid engine. |
| Feedback/status/loading | Strong: alerts/callouts/badges/progress/skeleton/toast-like surfaces. | Strong: Alert, Badge, Progress, Skeleton, Sonner, Toast. | Strong: badges, progress, snackbars, tooltips. | Strong: notification, inline loading, loading, progress, tag. | Strong: banner, badge, skeletons, spinner, progress bar. | Strong: flags, lozenges, progress, skeleton-like patterns. | Keep stable feedback primitives registry-cited and avoid effect-heavy defaults. |
| Media/charts/AI affordances | Partial: bar/donut charts, media cards, AI/streaming examples, LLM-oriented page-actions pressure. | Strong: Chart built on Recharts, dashboard chart blocks. | Partial: design guidance; implementation depends on platform/toolkit. | Strong AI affordance precedent: AI label across components, including data table. | Partial: media cards/thumbnails; no generic AI affordance contract. | Partial: product AI patterns vary by app. | Differentiate with explicit AI/LLM trust boundaries and generated-output tests, not decorative AI styling. |
| Tokens/theming | Strong: Python tokens, generated CSS layers, theme package assets. | Strong: CSS variables and Tailwind-oriented theming. | Strong: color, type, shape, motion tokens in design language. | Strong: IBM tokens and themes. | Strong: Shopify tokens and icon system. | Strong: design tokens and primitives. | Keep cascade order public API and package theme assets through Bengal/library contracts. |
| Agent/readiness metadata | Strong foundation: manifest, source maps, `find`, evidence labels emerging. | Strong direction: registry schema, CLI, MCP, LLM-friendly metadata. | Partial/N/A. | Partial: status and accessibility testing docs. | Partial: docs are task/domain rich, but not agent-contract oriented. | Partial: design/developer docs and package contracts. | This is a category to win: registry-grounded agent discovery plus executable parity tests. |

### Parity Takeaways

- Chirp UI should not chase raw component count. It already has broad coverage;
  the next quality jump is contract maturity, not more names.
- shadcn is the best benchmark for distribution, blocks, and agent-facing
  registry ergonomics, but the copied-source/Tailwind model conflicts with
  Chirp UI's package-and-registry contract.
- Carbon and Polaris are the strongest benchmarks for dense product/admin
  workflows: data tables, page structure, filters, and shell/action placement.
- Material and Atlassian are the strongest benchmarks for navigation doctrine:
  adaptive regions, reduced shell fragmentation, and consistent product-suite
  movement.
- Chirp UI's categorical opportunity is a Python/server-rendered design system
  where components, docs, generated CSS, manifests, tests, and agents all agree.

## Core Findings

### 1. shadcn's moat is distribution, not styling

The practical shadcn insight is that a design system can be a registry-backed
code distribution network. Components, blocks, hooks, themes, rules, and other
resources can be resolved through a schema, installed through a CLI, namespaced
for public/private sources, and exposed to agents through MCP.

Chirp UI already has a stronger source of truth in the Python
`ComponentDescriptor` registry and manifest, but it should productize that
surface with the same seriousness:

- `find` and manifest queries should feel like a first-class component catalog.
- Registry entries should explain use, anatomy, slots, runtime requirements,
  evidence, and maturity well enough for agents to choose correctly.
- Private or app-local extension stories should be designed around typed Python
  contracts, not copied source.
- Agent workflows should become "discover, apply, verify" rather than "copy a
  plausible snippet."

### 2. Headless systems win on behavior proof, not visual distinctiveness

Radix, Base UI, and React Aria all treat accessible behavior as expensive,
specialized infrastructure. They expose parts, state, slots, focus behavior,
keyboard behavior, and styling hooks so teams can build their own visual system
without rebuilding accessibility from scratch.

Chirp UI's equivalent is not a React headless layer. It is:

- safe Kida macro output,
- native HTML first,
- HTMX target boundaries,
- Alpine controllers only where behavior requires them,
- descriptor/manifest metadata,
- render and browser proof.

The missing maturity surface is "anatomy as contract" for more components:
rendered parts, semantic roles, focus targets, runtime requirements, state
attributes, and test names should be easy to inspect.

### 3. Mature systems distinguish components, patterns, shells, and evidence

GOV.UK and USWDS separate components from patterns. GOV.UK also publishes
research and testing context so teams can judge whether a pattern is safe to use
or needs service-specific research. Carbon separates shell regions instead of
collapsing everything into one mega-component.

Chirp UI should keep its existing "recipe first, composite later" rule and make
the evidence labels sharper:

- `stable`: normal public vocabulary with render/browser/docs proof.
- `experimental`: public but settling; use with care.
- `recipe-only`: copyable composition guidance; no macro contract yet.
- `compatibility`: retained public surface that should not be taught first.
- `research`: external evidence or design direction that has not yet changed
  Chirp UI.

### 4. Shells need layer discipline before API

Carbon and Atlassian both show why shell work becomes expensive when each
product invents its own navigation model. Material/Android shows that shell
navigation should adapt by available space. Bengal's custom theme confirms the
same issue in static docs: the useful shape is not "one app shell", it is a
small set of coordinated regions with explicit ownership.

For Chirp UI, the correct sequencing is:

1. improve smaller contracts (`sidebar`, `nav_tree`, compact headers,
   page actions, reference cards),
2. prove rail/tray/docs/catalog behavior in Bengal and at least one other
   independent reference implementation,
3. only then evaluate a narrow `docs_shell` or `catalog_shell`.

### 5. Chirp UI's durable differentiation is contract verification

Most systems document component usage. Some ship schemas. Few can let a Python
app, Python test suite, generated CSS, generated manifest, and coding agent all
inspect the same UI contract.

That is the differentiator to defend:

- no utility-class vocabulary,
- registry-cited classes,
- generated CSS and manifest,
- macro/template parity,
- safe attributes by default,
- HTMX-aware shell and fragment contracts,
- package/library metadata for themes and frameworks,
- tests that reject drift.

## Product Opinion

Chirp UI should be opinionated in five ways.

### Python-native over copied source

shadcn lets app teams own copied component source. Chirp UI should instead let
Python teams own configuration, theme tokens, app composition, and extension
points while the library owns validated components. The update story should be
"upgrade package and run verification", not "diff copied source forever."

### Contracts over classes

Tailwind and many registry components make class strings the authoring unit.
Chirp UI should make components, slots, variants, tokens, provides/consumes,
runtime requirements, and emitted classes the authoring unit.

### Recipes before composites

Composite APIs should trail evidence. A repeated pattern graduates only when
recipe-level composition has been tried and the remaining boilerplate is a real
contract gap, not taste.

### Behavior belongs where the platform cannot carry it

Native HTML, CSS, HTMX, and server-rendered URLs should remain the baseline.
Alpine and JavaScript should own only behavior that cannot be expressed safely
through those primitives.

### Evidence labels are product UX

Developers and agents need to know whether a surface is stable, experimental,
recipe-only, compatibility-only, or research-only. That label should appear in
registry metadata, generated docs, and source plans.

## Bengal Shell Implications

Bengal is now a serious proof source because it is an installable packaged
theme, not a showcase-only fixture.

Use Bengal to test these contract gaps:

| Bengal pressure | Chirp UI maturity opportunity | First proof |
|---|---|---|
| Symbolic outer rail plus contextual docs tree | richer `sidebar` / `nav_tree` semantics before a shell macro | theme package render tests and browser rail proof |
| Page actions for copy URL, LLM text, AI handoff, share | `page_actions` recipe, later primitive if repeated | Bengal docs pages plus one app/docs reference implementation |
| Compact docs/reference header | `page_hero` empty-slot cleanup or compact header primitive | render tests proving empty wrappers are omitted or hidden by contract |
| API/reference dense pages | reference-card and member-list recipes | API module/list/function pages in Bengal browser tests |
| Theme semantic icons | icon extension and diagnostics path | package-data checks and unknown-icon diagnostics |
| Footer in content flow | shell/content/footer ownership guidance | Bengal docs chrome browser proof |

Do not treat Bengal alone as enough evidence for `application_chrome()` or a
generic shell. Bengal is evidence for docs/catalog shell pressure and smaller
component contracts.

## Backlog

### Wave 1: Research Ledger And Evidence Labels

Add source-backed documentation that classifies external evidence and internal
surfaces without changing public APIs.

Tasks:

- Keep this research note linked from [INDEX.md](INDEX.md).
- Add or update a design-system positioning section in [VISION.md](VISION.md)
  only after the product language is reviewed against code reality.
- Maintain the evidence-label glossary in
  [PUBLIC-SURFACE-STABILIZATION.md](PUBLIC-SURFACE-STABILIZATION.md)
  as registry/docs labels evolve.
- Add a Bengal evidence row to
  [plans/PLAN-application-chrome-system.md](plans/PLAN-application-chrome-system.md)
  only when new theme proof lands.

Proof:

- docs link checks,
- docs IA ratchets if new tests are warranted,
- no generated docs touched.

### Wave 2: Registry Product Surface

Make Chirp UI's registry feel like a design-system product, not just internal
metadata.

Candidate work:

- enrich manifest/docs output with anatomy, runtime, maturity, and proof links
  using existing descriptor data where possible,
- improve `python -m chirp_ui find` output for authoring, maturity, and recipe
  discovery,
- document app-local extension patterns that preserve registry authority,
- evaluate an agent-facing query surface analogous to shadcn MCP, but backed by
  `build_manifest()` and local package data.

Stop-and-ask before:

- manifest schema changes,
- new descriptor fields,
- new CLI command names,
- new public extension protocols.

Proof:

- manifest checks,
- `find` tests,
- generated docs freshness when output changes,
- agent-source inventory updates.

### Wave 3: Anatomy Contracts

Move complex interactive and shell-adjacent components toward anatomy docs that
are executable, not prose-only.

Candidate surfaces:

- `sidebar` / `nav_tree`,
- `page_hero` / compact header,
- `drawer` / `tray`,
- `route_tabs`,
- `command_palette`,
- `page_actions` recipe,
- reference/API card recipes.

Required anatomy fields:

- named parts and slots,
- semantic roles and labels,
- state attributes,
- focus targets,
- keyboard behavior,
- runtime requirements,
- responsive constraints,
- render/browser proof.

Proof:

- focused render tests,
- browser tests for focus and overflow where behavior matters,
- docs source links to tests or fixtures.

### Wave 4: Accessibility And Performance Ledger

Adopt an explicit evidence ledger similar in spirit to GOV.UK and Carbon, but
scaled to Chirp UI.

Candidate fields:

- native semantics checked,
- keyboard checked,
- focus checked,
- screen-reader risk noted,
- reduced-motion checked,
- overflow checked,
- interaction/browser proof checked,
- performance-sensitive behavior noted.

Start with high-risk surfaces:

- modal/dialog/confirm,
- drawer/tray,
- command palette,
- shell navigation,
- route tabs,
- forms and validation,
- Bengal docs chrome.

Proof:

- tests reference the ledger fields,
- browser gauntlets cover stress widths and focus movement,
- no claims of manual screen-reader testing unless it was actually performed.

### Evidence Model Without A Userbase

Chirp UI cannot plan around downstream adoption data it does not have. External
design-system research is therefore a market proxy for requirements discovery,
not promotion proof by itself. It can tell us which pressures are common:
shell anatomy, page actions, navigation hierarchy, responsive fallback,
accessibility expectations, and documentation patterns.

Promotion evidence must come from work we can verify now:

- Bengal as a first-party proving ground for docs/catalog pressure.
- Scenario-complete non-Bengal reference implementations that use existing
  Chirp UI primitives before naming a gap.
- Browser, render, server, escaping, and generated-output tests for the
  attempted composition and the remaining gap.
- `docs/reference-implementations/PROOF-ANALYSIS.md` as the source-only ledger
  that decides whether a proven scenario remains recipe guidance, needs another
  independent reference, or is ready for a stop-and-ask public API plan.
- `docs/reference-implementations/RECIPE-GUIDANCE.md` as the source-only
  authoring layer when the proof decision is to keep current primitives and
  teach the recipe.
- Explicit stop-and-ask before any public macro/API, descriptor, CSS, manifest,
  generated docs, runtime, or extension-contract change.

### Wave 5: Bengal-Driven Primitive Maturation

Run small PRs that promote repeated Bengal needs into stronger Chirp UI
contracts.

Preferred order:

1. `page_hero` empty-slot cleanup or compact header recipe.
2. richer linked-branch navigation semantics for `sidebar` / `nav_tree`.
3. `page_actions` recipe with copy/LLM/share behavior and trust boundaries.
4. reference/API dense card recipes.
5. semantic icon extension and diagnostics.
6. shell promotion docket for `docs_shell` / `catalog_shell`.

Acceptance:

- every promoted surface names its implementation evidence,
- every public API change has migration/projection collateral,
- every recipe-only surface stays labelled recipe-only until promotion proof is
  complete.

## Composite Promotion Gate

Do not add `application_chrome()`, `docs_shell()`, `catalog_shell()`, or a
similar shell composite until all are true:

- Bengal and at least one other independent reference implementation repeat the
  same structural gap.
- Existing `app_shell`, `site_shell`, `workspace_shell`, `sidebar`, `nav_tree`,
  `frame`, `command_bar`, and layout primitives were tried.
- The remaining problem is structural ownership, not visual taste.
- Render tests prove landmarks, slots, attributes, and empty states.
- Browser tests cover 320, 390, 768, 1024, and 1280 widths.
- Accessibility and performance notes are explicit.
- Descriptor, macro, CSS partial, generated CSS, manifest, generated options,
  docs, examples, and changelog collateral are ready.

## Not Now

- Python shadcn clone.
- Tailwind-compatible utility vocabulary.
- copied-source component install model.
- generic `application_chrome()`.
- manifest schema bump for research-only findings.
- app-local shell class system inside Chirp UI.
- new JavaScript layout engine for responsive rails.
- claims of screen-reader proof without actual manual verification.

## Steward Notes

Consulted stewards:

- Documentation
- Planning
- Application chrome
- Bengal theme
- Core registry/API
- Templates/CSS/Behavior
- Tests
- Agent grounding

Accepted findings:

- Treat shadcn's registry/MCP system as a distribution and agent-product lesson,
  not a styling lesson.
- Keep Chirp UI's no-utility-class rule as a differentiator.
- Use Bengal as first-party proving-ground evidence for docs/catalog shell
  pressure.
- Mature smaller contracts before shell composites.
- Add evidence labels and anatomy/proof ledgers before broad public API work.

Deferred findings:

- MCP-compatible Chirp UI registry server.
- Public shell composite.
- Manifest schema changes for anatomy or evidence labels.
- New icon extension protocol.

Required proof for this planning slice:

- docs-only review,
- link from [INDEX.md](INDEX.md),
- `git diff --check`.
