# chirp-ui: Application Chrome System

Status: active plan
Date: 2026-05-13
Depends on:

- [PLAN-navigation-contract-application.md](done/PLAN-navigation-contract-application.md)
- [PLAN-dense-object-chrome-next.md](done/PLAN-dense-object-chrome-next.md)
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
- Bengal docs chrome is a first-party proving ground, but it is not the same
  contract as Chirp app shell chrome.

Minority reports:

- A small `object_header` or `chrome_frame` may become useful later.
- Defer it until at least two independent reference implementations repeat the
  same shape and existing primitives are proven insufficient.

## Five-Rock Status

| Rock | Status | Decision |
|---|---|---|
| Chrome Layer Model | Residual contract work | Current layer model exists; add app-chrome bridge, decision tables, and rendered semantic tests. |
| Rail And Tray Design Contracts | Active implementation backlog | Add rail-to-tray recipes and browser proof using existing `sidebar`, `nav_tree`, `drawer`, and `tray`. |
| Modern Visual Rhythm | Active audit backlog | Treat rhythm as token/control-size/elevation proof, not utility spacing classes. |
| Responsive Chrome Gauntlet | Active test backlog | Build a recipe-family browser gauntlet before any composite promotion. |
| Recipe First, Composite Later | Accepted boundary | No `application_chrome()`, `object_chrome()`, `workspace_header()`, or `dense_nav_frame()` without independent reference implementation evidence. |

## Contract Map

| Layer | Job | Current Chirp UI surface | Next proof |
|---|---|---|---|
| App identity | Persistent product/app orientation | `app_shell`, `navbar`, logo/title slots | Published app-chrome docs route. |
| Product rail | Broad app/workspace movement | `sidebar`, `primary_nav`, `nav_tree` | Rail-to-tray recipe and browser proof. |
| Secondary rail | Hierarchy, saved views, nearby scope | `nav_tree`, `saved_view_strip`, `scope_switcher` | Recipe-family gauntlet. |
| Object context | Current object/path/actions | `breadcrumbs`, `page_header`, `inline_counter`, `badge`, `dropdown_menu` | Reference implementation repetition before composite. |
| Local routes | URL-backed object/workspace views | `route_tabs` | Gauntlet scroll and active-route proof. |
| Page tools | Filters, sort, display, refresh, export | `command_bar`, `filter_bar`, buttons, dropdowns | Mixed-control rhythm proof. |
| Command overlay | Search, jump, create, actions | `command_palette_trigger`, `command_palette` | Focus/open proof inside full chrome. |
| Overlay chrome | Phone fallback, inspectors, supplemental panels | `drawer`, `tray`, modal/dialog primitives | In-context focus, close, overflow proof. |

## Evidence-Ledger Synthesis: Shell Primitive Readiness

The interactive anatomy ledgers now give application chrome a concrete
dependency map. They do not authorize a shell macro by themselves; they tell us
which lower-level contracts are strong enough to compose, and which gaps should
be solved before promoting any broader primitive.

Readiness decision: Chirp UI is ready to improve recipes, examples, and narrow
helpers around shell response ownership and page actions. It is not ready for a generic `application_chrome()`, `catalog_shell()`, or `docs_shell()` macro from the current evidence.

| Dependency | Evidence Ledger | Shell Readiness | Open Gap | Next Action |
|---|---|---|---|---|
| Modal and confirm surfaces | [MODAL-ANATOMY.md](../MODAL-ANATOMY.md) | Native dialog and overlay contracts are stable enough for shell recipes. | Native dialogs and store-backed overlays intentionally have different event models. | Compose them explicitly; do not hide both behind one shell slot. |
| Dropdown command surfaces | [DROPDOWN-ANATOMY.md](../DROPDOWN-ANATOMY.md) | Command menus, selects, and split actions are stable enough for page tools. | Menu/split roving-arrow navigation is not published; select has stronger keyboard behavior than command menus. | Use dropdowns for actions/selects now; avoid claiming full menu-button keyboard parity until implemented and tested. |
| Drawer and tray fallback chrome | [DRAWER-TRAY-ANATOMY.md](../DRAWER-TRAY-ANATOMY.md) | Native drawer and store-backed tray contracts are stable enough for rail-to-drawer/tray recipes. | A tray close browser test still records an app-shell topbar hit-target anomaly. | Keep browser proof in-context before promoting any responsive shell fallback helper. |
| Tabs and route tabs | [TABS-ANATOMY.md](../TABS-ANATOMY.md) | Route tabs and tabbed layout are stable enough for URL-backed local views. | Route tabs are navigation, not ARIA tab widgets; roving-arrow tablist keyboard behavior is not published. | Keep route-tab shell recipes link-native and avoid tab-widget claims. |
| Bengal theme controls | [BENGAL-THEME-ANATOMY.md](../BENGAL-THEME-ANATOMY.md) | Packaged theme chrome is strong evidence for shell pressure and page actions. | Theme selectors are not registry APIs; Bengal docs chrome is only a partial app-shell proving ground. | Promote smaller repeated contracts only after another reference implementation repeats the same gap. |

Cross-ledger primitive candidates:

| Candidate | Status After Ledger Pass | Why |
|---|---|---|
| Page actions primitive | Candidate for next investigation | Bengal page actions repeat copy URL, LLM text, and AI handoff hooks with native popover behavior, but the app-level component contract, slots, escaping, and non-docs use cases are not designed yet. |
| Linked nav-tree/sidebar semantics | Candidate for next investigation | Bengal docs rail pressure shows richer parent/child navigation needs than generic sidebar links, but route semantics and collapsible behavior need a registry-level design. |
| Shell response/OOB helper | Candidate for recipe/helper evaluation | Internal route fixtures show repeated target ownership and shell-actions replacement pressure; this is routing/response glue, not a visual shell macro. |
| Compact page header | Candidate for `page_hero`/header maturation | Bengal had to hide empty hero chrome and keep page actions near titles; solve empty-slot/header density first before inventing a docs-shell macro. |
| Generic application shell macro | Deferred | Existing `app_shell_layout`, sidebar/nav, route tabs, drawers/trays, command palette, and action primitives compose real fixtures; the repeated pain is response ownership and smaller contracts. |
| Catalog/docs shell macro | Deferred | Bengal and catalog recipes expose useful pressure, but the owned layer is still product-specific information architecture. |

Promotion gate for the next implementation slice:

- choose one narrow candidate, not a mega-shell,
- name the reference implementations and existing primitives tried,
- write the registry/API contract before touching descriptors or macros,
- prove rendered anatomy, escaping, keyboard/focus, HTMX/Alpine boundaries, and
  responsive overflow,
- update docs/examples/generated outputs only if a public API is actually promoted.

## Linked Nav-Tree/Sidebar Semantics Investigation

Status: active investigation inside this plan, no public API authorized.

The readiness matrix identified linked nav-tree/sidebar semantics as a narrow
candidate because Bengal docs chrome needed a symbolic outer rail plus a
contextual docs tree with richer parent/child semantics than a flat sidebar.
Chirp UI already has `nav_tree(branch_mode="linked")`, `sidebar`,
`sidebar_section`, and `sidebar_link`. The open question is whether the repeated
gap is a small registry-owned navigation contract or a theme-specific docs IA
recipe.

This investigation does not authorize new `nav_tree` parameters, new sidebar macros, emitted classes, CSS, manifest changes, generated docs, or a docs-shell macro.

Existing surfaces tried:

| Surface | What it solves | Remaining gap |
|---|---|---|
| `sidebar` / `sidebar_section` / `sidebar_link` | Shell sidebar landmarks, section grouping, active route matching, badges, and shell HTMX attrs. | Does not model branch parents with children as one structured navigation item. |
| `nav_tree(branch_mode="disclosure")` | Client/browser-owned disclosure hierarchy using native `<details>`. | Parent route link and disclosure affordance are coupled in a summary; not ideal for server-controlled docs trees. |
| `nav_tree(branch_mode="linked")` | Branch parents can be direct route links; children render only when server marks `open=true`. | Contract lacks explicit guidance for active descendants, child-count metadata, compact branch/leaf rhythm, and sidebar integration. |
| Bengal docs nav partials | Prove the custom docs rail target shape with active branches and compact child rows. | Theme selectors and page-context fallback logic are not Chirp UI registry API. |
| Rail-to-drawer recipe | Proves linked nav trees can compose with drawer fallback and command triggers. | Showcase/browser fixture proof is not enough to promote new macro surface. |

Implementation scan:

| Evidence | Current Shape | Counts Toward Promotion? | Reason |
|---|---|---:|---|
| Bengal docs navigation | Contextual docs tree, active branch styling, compact iterable child rows, and fallback from `page.href` to `page._path`. | Partial | Packaged-theme pressure, but tied to Bengal page context and theme selectors. |
| Rail-to-drawer recipe | Uses `nav_tree(branch_mode="linked")` in persistent rail and drawer fallback. | Partial | Good responsive proof for existing primitives, but it does not prove a new API gap. |
| Knowledge workspace recipe | Uses linked disclosure navigation for nested pages. | No | Recipe evidence only; it does not provide a second scenario-complete implementation with the same missing contract. |
| Filesystem app-shell fixture | Uses `sidebar` and `sidebar_link` for broad app sections. | No | Proves sidebar shell navigation, not linked branch hierarchy. |
| Generic docs recipes | Mention sidebar/nav-tree composition. | No | Prose guidance is not implementation repetition. |

### Linked Nav Reference Evidence Search

Search date: 2026-05-23

Result: no second qualifying non-Bengal linked-branch reference implementation
exists in the repository yet. This is not a reason to wait for a userbase; it
means the next slice should deliberately build or identify a scenario-complete
first-party reference implementation before proposing public API. Linked
nav-tree/sidebar semantics remain in investigation, with no `nav_tree`
parameters, sidebar branch macros, CSS, manifest, generated docs, or docs-shell
promotion authorized.

Search scope:

- `docs/`
- `examples/`
- `tests/browser/templates/`
- `tests/browser/app.py`
- `src/chirp_ui/templates/`
- excluded Bengal theme templates to avoid counting the original docs-theme
  pressure as the second implementation context

Qualifying criteria:

- the implementation must be a scenario-complete app, packaged integration, or
  copyable reference page, not only prose or a showcase snippet,
- it must try `sidebar`, `sidebar_section`, `sidebar_link`, and
  `nav_tree(branch_mode="linked")` or explain why one does not fit,
- it must repeat the same missing linked-branch contract as Bengal: parent
  route links, server-owned open state, active descendants, child rows,
  compact branch/leaf rhythm, badge/count metadata, and mobile fallback,
- it must record the remaining gap without using Bengal selectors or
  page-context fallbacks.

Search findings:

| Candidate | Evidence Found | Why It Does Not Qualify |
|---|---|---|
| Bengal docs navigation | Packaged-theme docs tree with active branches, compact child rows, and page-context fallback behavior. | Original pressure only; selectors and data shaping are Bengal-owned, not Chirp UI API. |
| Rail-to-drawer recipe | Uses `nav_tree(branch_mode="linked")` in persistent rail and drawer fallback with browser proof. | Recipe/fixture evidence; it proves existing composition, not a repeated missing API gap. |
| Application chrome gauntlet | Uses linked `nav_tree` in a product rail with long labels and route-like branches. | Browser stress evidence only; it does not try sidebar integration or record a missing contract. |
| General gauntlet linkability rooms | Exercise `nav_tree(branch_mode="linked")`, `file_tree` forwarding, hinted items, active children, and branch links. | Component stress proof, not a scenario-complete reference implementation with docs/sidebar IA pressure. |
| Component showcase navigation page | Demonstrates linked branches in example snippets. | Showcase examples are not implementation repetition and do not prove a missing API. |
| Filesystem/app chrome fixtures | Use `sidebar`, `sidebar_section`, and `sidebar_link` for broad app sections. | Proves shell sidebar navigation, not hierarchical linked branch semantics. |
| Forum/product/media pattern docs | Mention `nav_tree`, sidebars, or assistant panels in recipes. | Prose/pattern evidence only; no rendered repeated linked-branch gap. |

Decision after search:

- Keep linked nav-tree/sidebar semantics unauthorized for public API changes.
- Keep `nav_tree(branch_mode="linked")` as the current hierarchical navigation
  primitive.
- Do not add `docs_sidebar`, `catalog_sidebar`, sidebar branch macros, or new
  branch metadata from this evidence.
- The next useful linked-nav slice is a scenario-complete first-party reference
  implementation that composes `sidebar` and `nav_tree(branch_mode="linked")`
  together and records whether sidebar integration, active descendants,
  child-count metadata, compact branch/leaf rhythm, or mobile fallback remain
  insufficient.

### Private Linked Nav Fixture

Status: implemented as test evidence only, no public API authorized.

Fixture:

- route: `/linked-nav-candidate`
- template: `tests/browser/templates/linked_nav_candidate_page.html`
- browser proof: `tests/browser/test_linked_nav_candidate.py`

What the fixture proves:

- Existing `sidebar`, `sidebar_section`, and `sidebar_link` can provide broad
  app-shell navigation while `nav_tree(branch_mode="linked")` provides a
  contextual linked branch hierarchy inside the same sidebar.
- Linked branch parents render as route links, not native disclosure summaries.
- Children render only when the server marks a branch `open=true`; closed
  branch children are omitted from the rendered tree.
- Active child links, no-href groups, branch badges, and long child labels can
  render in the private sidebar fixture without document-level horizontal
  overflow.
- The same linked tree can render inside a phone drawer fallback with existing
  `drawer` and `drawer_trigger` primitives, preserving branch links,
  server-opened children, active child state, omitted closed children, and focus
  return.

What the fixture does not prove:

- It does not authorize new `nav_tree` parameters, sidebar branch macros,
  emitted classes, CSS, manifest changes, generated docs, or a docs-shell
  macro.
- It does not prove that active descendants, child-count metadata, compact
  branch/leaf rhythm, or mobile fallback need a new public contract.
- It does not count as qualifying implementation evidence until it records a
  repeated gap inside a scenario-complete reference implementation.

Fixture decision:

| Question | Current Answer |
|---|---|
| Do existing primitives render the linked-sidebar candidate shape? | Yes, as a private fixture. |
| Is there enough evidence for public API promotion? | No. |
| What remains to analyze? | Whether active descendants, count metadata, compact rhythm, and mobile fallback are sufficiently expressible with existing `nav_tree` and `sidebar` composition. |
| What would unlock promotion? | A second independent reference implementation that repeats the same linked-branch gap after trying this fixture pattern. |

### Linked Nav Fixture Analysis

Analysis date: 2026-05-23

Decision: keep linked nav-tree/sidebar semantics in investigation. The fixture
shows existing primitives can render a credible linked-sidebar candidate, but
it does not prove a public `nav_tree` or `sidebar` API gap.

| Behavior | Existing Primitive Outcome | Remaining Gap | API Signal |
|---|---|---|---|
| Sidebar integration | `sidebar`, `sidebar_section`, and `sidebar_link` can host a contextual `nav_tree(branch_mode="linked")`. | The app owns the wrapper relationship between broad shell sections and contextual hierarchy. | Weak: composition is acceptable. |
| Branch parent links | Linked branch parents render as anchors with no `<summary>` disclosure conflict. | Server owns which branches render children through `open=true`. | Weak: current contract is clear. |
| Active child state | Active children render `aria-current="page"` and active link classes. | Parent branches with active children are not automatically marked as active descendants. | Medium only if another reference implementation needs registry-owned active-descendant semantics. |
| Count metadata | Branch badges render visible counts such as `Guide 4`. | There is no richer child-count label or count-specific branch metadata contract. | Medium only if repeated reference implementations need accessible count semantics beyond badges. |
| No-href grouping | Branches without `href` render as text while their open children remain linked. | Apps must shape no-href group behavior explicitly. | Weak: existing behavior is adequate in the fixture. |
| Long labels and overflow | Long child labels stay contained in the sidebar at 320px with no document overflow. | Compact branch/leaf rhythm remains visual proof, not a new API need. | Weak: current CSS holds for the fixture. |
| Mobile fallback | The fixture proves phone-width containment and a phone drawer fallback with the same linked tree. | A future public contract would still need policy for when apps choose horizontal sidebar, drawer, or tray fallback. | Medium only if a second reference implementation repeats mobile fallback boilerplate. |

Current gap classification:

- Real gap: Chirp UI does not automatically derive active-descendant parent
  state, richer child-count metadata, or mobile fallback policy for linked
  branch navigation inside sidebars.
- Not yet a promotion gap: the private fixture is still artificial, and the
  existing composition renders the candidate without new API or CSS.
- Practical next step: keep the fixture as regression/evidence, record the
  remaining gap notes, then build or identify a scenario-complete reference
  implementation that repeats the same linked-branch gap.

Next-slice options from this analysis:

| Slice | Purpose | Promotion Risk |
|---|---|---|
| Private mobile fallback stress | Done: same linked tree now composes in a phone drawer fallback with browser proof. | Closed; private evidence only. |
| Fixture gap notes | Add explicit comments/docs around active-descendant and count metadata limits. | Low; docs/test only. |
| Reference evidence research | Use external design-system patterns to define a non-Bengal app/docs/reference page with sidebar plus linked branch hierarchy. | Low; evidence gathering. |
| Public API proposal | Draft a promotion proposal only after a second reference implementation repeats the gap. | High; stop and ask first. |

### Private Linked Nav Mobile Fallback Stress

Status: implemented as private browser evidence, no public API authorized.

Fixture delta:

- template: `tests/browser/templates/linked_nav_candidate_page.html`
- browser proof: `tests/browser/test_linked_nav_candidate.py`
- existing primitives added to the private composition: `drawer` and
  `drawer_trigger`

What the mobile fallback stress proves:

- The private linked-nav fixture can hide the persistent sidebar at phone width
  and expose a drawer trigger without adding a shell/sidebar macro.
- `nav_tree(branch_mode="linked")` keeps the same linked branch behavior inside
  a left drawer: branch parents remain anchors, no `<summary>` disclosure
  appears, active children keep `aria-current="page"`, and closed branch
  children remain omitted.
- Long linked-nav child labels stay inside the open drawer at 320px without
  document-level horizontal overflow.
- The existing drawer contract opens, closes with Escape, and returns focus to
  the trigger in this navigation fallback.

Decision:

- This closes the private mobile fallback stress slice.
- It weakens the case for an immediate public linked-sidebar primitive because
  existing `sidebar`, `nav_tree(branch_mode="linked")`, `drawer`, and
  `drawer_trigger` compose the candidate across desktop and phone contexts.
- The remaining gap is policy and repetition, not render capability: another
  independent reference implementation must repeat the same active-descendant,
  richer count metadata, or responsive fallback boilerplate before promotion is
  justified.

### Private Linked Nav Gap Notes

Status: recorded as investigation notes only, no public API authorized.

The private fixture now proves render capability across desktop sidebar and
phone drawer contexts. The remaining questions are narrower than the original
candidate:

| Gap | Fixture Evidence | Current Decision |
|---|---|---|
| Active-descendant parent state | Active children render `aria-current="page"` and active classes; parent branches are plain route links. | Do not add `active_descendant` until a second reference implementation needs parent highlighting separate from current-page state. |
| Rich count metadata | Branch badges render visible counts such as `Guide 4`. | Do not add `child_count` or `child_count_label` until repeated reference implementations need accessible count semantics that badges cannot express. |
| Compact branch/leaf rhythm | Long labels, open children, and no-href groups stay contained in sidebar and drawer fixtures. | Treat rhythm as CSS/recipe evidence, not a macro parameter. |
| Responsive fallback policy | Existing `sidebar`, `drawer`, and `drawer_trigger` compose a phone fallback. | Do not add a shell-owned responsive policy until reference implementations repeat the same sidebar-to-drawer boilerplate. |

Practical guidance for the next reference implementation:

- Start with `sidebar`, `sidebar_section`, `sidebar_link`,
  `nav_tree(branch_mode="linked")`, `drawer`, and `drawer_trigger`.
- Mark branches `open=true` server-side when children should render.
- Treat active child state and parent branch emphasis as app data until repeated
  reference implementations prove Chirp UI should derive it.
- Use badges for visible counts first; promote richer count metadata only when
  accessibility or IA needs cannot be handled by existing badge labels.
- Record the exact repeated boilerplate before proposing a public primitive.

Candidate contract questions:

- Should `nav_tree(branch_mode="linked")` grow explicit branch metadata such as
  `active_descendant`, `child_count`, `child_count_label`, or `branch_label`?
- Should sidebar learn a structured branch item, or should `nav_tree` remain the
  only hierarchical navigation macro?
- Should linked branches expose a separate disclosure toggle, or should
  server-controlled `open=true` remain the linked-branch contract?
- How should active parent, active child, and current page differ in classes and
  ARIA?
- Which behavior belongs to Chirp UI, and which stays in Bengal page-context
  shaping such as `page.href` / `page._path` fallbacks?

Promotion gate:

- Bengal plus one additional independent reference implementation repeat the
  same linked branch gap.
- The additional implementation tries `sidebar`, `sidebar_section`,
  `sidebar_link`, and `nav_tree(branch_mode="linked")`, then records what
  remains insufficient.
- A draft contract names item schema, active/open semantics, ARIA, route-link
  HTMX attrs, badge/count behavior, compact branch/leaf rhythm, and mobile
  drawer/tray behavior.
- Render tests cover branch links, child rows, active descendants, no-href
  branches, badges/counts, hints, escaping, strict undefined, and route attrs.
- Browser tests cover keyboard/link behavior, active route updates, phone drawer fallback, long labels, compact child rows, and no document-level
  horizontal overflow.
- Collateral plan includes descriptor/manifest impact if the macro signature
  changes, CSS partial and generated CSS if classes change, docs/examples,
  generated component options, browser proof, and changelog.

Not now:

- Do not add a `docs_sidebar`, `catalog_sidebar`, or `docs_shell` macro.
- Do not move Bengal `.chirp-theme-docs-nav*` selectors into `chirpui-*`
  classes.
- Do not add nav-tree descriptor/schema changes without a separate API plan.
- Do not make linked branch navigation an ARIA tree unless keyboard behavior and
  assistive-technology expectations are explicitly designed and tested.
- Do not count recipe prose as a reference implementation.

## Shell Response/OOB Helper Investigation

Status: active investigation inside this plan, no public API authorized.

The readiness matrix identified shell response/OOB helper pressure because
internal route fixtures repeated target ownership and route-scoped shell-action
replacement logic. This is not a visual shell problem. It is response-shape
selection across persistent shell navigation, route-tab page chrome, and local
fragments.

This investigation does not authorize a public `chirp_ui` helper, a Chirp
routing API, a shell macro, new component descriptors, emitted classes, CSS,
manifest changes, generated docs, or a new HTMX protocol.

Existing surfaces tried:

| Surface | What it solves | Remaining gap |
|---|---|---|
| [SHELL-TABS-CONTRACT.md](../SHELL-TABS-CONTRACT.md) route-local helpers | Documents `HX-Target` branching for `main`, `page-root`, and local fragment targets. | Manual routes can still repeat small request-target and OOB inclusion helpers. |
| Filesystem mounted pages with `mount_pages()` | Lets Chirp's page-shell contract choose full page, page-root, and local block responses declaratively. | Does not cover hand-written route families that bypass filesystem pages. |
| `shell_outlet_attrs()` and shell OOB regions | Provide stable shell targets and replacement points such as shell actions. | Route handlers still decide when a response owns shell-level OOB updates. |
| `route_tabs` | Keeps local URL-backed views link-native and targets `#page-root`. | Does not decide whether the server should return full page chrome or only local content. |
| `fragment_island` / `safe_region` patterns | Keep local tools from inheriting shell selectors and over-swapping page chrome. | They protect fragment boundaries but do not classify the incoming request. |
| Workspace/admin route fixtures | Prove the target-boundary and shell-actions OOB behavior in browser fixtures. | Fixture-private helper evidence is not enough to publish a shared API. |

Implementation scan:

| Evidence | Current Shape | Counts Toward Promotion? | Reason |
|---|---|---:|---|
| Filesystem mounted app fixture | `_layout.html`, registered sections, page blocks, route tabs, shell actions, and fragment endpoints. | Covered | This path should prefer `mount_pages()` and the registered page-shell contract, not a Chirp UI helper. |
| Manual route references from Wave 1/Wave 2 | Route handlers branch on `HX-Target` and include OOB shell actions for shell navigation. | Partial | Repeated internal pressure, but still fixture/proof driven and close to routing concerns. |
| Workspace/admin browser fixtures | Browser proof for `main`, `page-root`, local fragments, OOB actions, and singleton shell targets. | Partial | Good regression evidence for the boundary, not enough to decide public API ownership. |
| Bengal docs chrome | Static/docs theme shell with docs rail, page actions, footer, and search. | No | It proves theme shell pressure, but not the same HTMX response-helper contract. |
| Published recipe prose | Documents response shapes and target ownership. | No | Prose guidance is necessary collateral; it is not implementation repetition. |

Candidate contract questions:

- Is the owner Chirp routing/framework, `chirp_ui`, or app-local recipe code?
- Should the contract be named around response ownership, not application
  chrome, for example a response target decision rather than shell helper?
- Should the API return booleans, an enum, or a decision object that names full
  page, page-root, local fragment, and shell OOB ownership?
- Which target identifiers are configurable, and which stay conventional:
  `main`, `page-root`, `page-content-inner`, `chirp-shell-actions`?
- How should no `HX-Request`, missing `HX-Target`, boosted shell navigation,
  route-tab navigation, and local fragment requests differ?
- Can filesystem pages and manual routes share a contract, or should mounted
  pages remain the preferred higher-level path?

Promotion gate:

- Three route families repeat the same branching and shell-actions OOB
  boilerplate outside filesystem mounted pages.
- The helper can be named around response ownership rather than visual shell
  composition.
- The design explicitly says whether ownership belongs to Chirp routing,
  `chirp_ui`, or local recipe code.
- Tests cover no `HX-Request`, missing `HX-Target`, `HX-Target: main`,
  `HX-Target: page-root`, local fragment targets, and OOB shell actions.
- Docs can migrate from route-local helpers to the promoted helper without
  changing template contracts.
- Collateral plan says no descriptor, manifest, CSS, generated options, or
  component docs change unless the chosen owner is a public Chirp UI API.

Not now:

- Do not add a public `chirp_ui` shell response helper from this plan slice.
- Do not add `application_chrome()`, `chrome_frame()`, or another visual macro
  to solve a response-ownership problem.
- Do not move routing decisions into component templates.
- Do not create a new HTMX convention when `HX-Target` already carries the
  required distinction.
- Do not replace the filesystem mounted page-shell contract with a lower-level
  helper.
- Do not count Bengal theme chrome as proof for this specific response-helper
  contract.

### Shell Response Route-Local Gap Notes

Status: recorded as route-local evidence only, no public API authorized.

The manual workspace/admin route references now prove the important response-shape
branches without adding a shared helper:

| Request Shape | Expected Response | Current Owner |
|---|---|---|
| normal full-page request | full template with `#page-content` and `#page-root`, no shell-actions OOB fragment | route handler plus template context |
| `HX-Request` without `HX-Target` | full template, no page-root fragment, no shell-actions OOB fragment | route handler should avoid target inference |
| `HX-Target: main` | full template with `#page-content`, `#page-root`, and shell-actions OOB when actions changed | route handler opts into shell OOB context |
| `HX-Target: page-root` | route-tab/page chrome fragment only, no persistent shell and no shell-actions OOB | page-root fragment renderer |
| local target such as `page-content-inner` | local fragment only, with inherited shell selectors cleared by the caller | local endpoint or fragment island |

Current decision:

- Keep `_is_hx_target()` and `_include_shell_actions_oob()` as fixture-local
  examples of the documented [SHELL-TABS-CONTRACT.md](../SHELL-TABS-CONTRACT.md)
  pattern.
- Do not promote a public helper from two manual fixture route families; this
  is still close to Chirp routing/page composition and has not appeared in a
  third scenario-complete route reference.
- Do not add descriptor, manifest, CSS, generated component options, or macro
  collateral for this slice.
- The next qualifying evidence would be a third hand-written route family,
  outside `mount_pages()`, that repeats the same `HX-Target` branching and OOB
  context boilerplate after applying the documented recipe.

## Compact Page Header/Page Hero Investigation

Status: active investigation inside this plan, no public API authorized.

The readiness matrix identified compact page header pressure because Bengal had
to keep page actions close to titles while avoiding empty hero chrome on dense
docs, API, and catalog pages. This is a header anatomy and optional-region
problem, not a docs-shell problem.

This investigation does not authorize new `page_hero` parameters, a new compact
header macro, slot changes, emitted classes, CSS, manifest changes, generated
docs, or a docs/catalog shell macro.

Existing surfaces tried:

| Surface | What it solves | Remaining gap |
|---|---|---|
| `page_header(variant="compact")` | Stable compact title/subtitle/action relationship for application pages. | Does not cover hero backgrounds, eyebrow/footer/metadata slots, or docs landing treatment. |
| `page_hero(variant="minimal")` | Provides page-scale hero treatment with title, subtitle, eyebrow, actions, metadata, content, and footer slots. | Currently emits optional slot wrappers even when callers provide no content. |
| `search_header` / `resource_index` | Prove denser header plus search/filter/result rhythm for catalog-like pages. | Search-first composition is not a general page hero replacement. |
| `document_header` / `entity_header` | Cover dense document/object orientation with metadata and actions. | They own object/document anatomy, not docs-page hero semantics. |
| Bengal docs hero/header treatment | Proves packaged-theme pressure for title, actions, metadata, TOC/search context, and compact catalog headers. | Theme selectors and Bengal page context are not Chirp UI registry API. |
| Header relationship CSS/browser proof | Proves title/action attachment, margin trimming, wrapping, and overflow behavior for current headers. | Does not prove empty hero slot omission or a new compact hero contract. |

Implementation scan:

| Evidence | Current Shape | Counts Toward Promotion? | Reason |
|---|---|---:|---|
| Bengal docs/API/catalog pages | Custom theme header treatment keeps title, actions, metadata, and page content compact. | Partial | Packaged-theme pressure, but still Bengal-specific IA and selectors. |
| Application chrome route fixtures | Use `page_header`, route tabs, breadcrumbs, command bars, and shell actions. | No | Proves existing compact app headers, not a `page_hero` gap. |
| Catalog/resource recipes | Use `resource_index`, `search_header`, and header relationship proof. | Partial | Good dense-header evidence, but search-first pages are a narrower shape. |
| Forum/media pattern pages | Use `detail_header`, `entity_header`, and page heroes for content-rich pages. | No | Pattern evidence is not repeated app pressure for compact docs headers. |
| Private compact-header candidate fixture | Compares `page_header`, `page_hero`, `search_header`, `entity_header`, and `document_header` in one dense page. | No | Artificial browser evidence; it proves current primitives compose, not that a new macro is needed. |
| Generated docs prose | Describes header primitives and relationships. | No | Prose can guide the contract, but does not count as implementation repetition. |

Candidate contract questions:

- Should `page_hero` omit empty named-slot wrappers, or should CSS continue to
  collapse empty regions for backward-compatible markup?
- Is the real missing primitive a compact hero/header, an extension of
  `page_header`, or better guidance for choosing `page_header` over
  `page_hero`?
- Which optional regions are contractually meaningful: eyebrow, actions,
  metadata, content, footer, or page-action menus?
- Should page actions live in the header primitive, a separate page-actions
  primitive, or a recipe that composes both?
- How should semantic heading level, landmarks, breadcrumbs, and route tabs
  compose without duplicating page identity?
- Which behavior belongs to Chirp UI, and which remains Bengal theme-specific
  catalog/docs presentation?

Promotion gate:

- Bengal plus one additional independent reference implementation repeat the
  same empty-region or dense-header gap after trying
  `page_header(variant="compact")`,
  `page_hero(variant="minimal")`, `search_header`, and `entity_header`.
- A draft contract names owned regions, heading semantics, optional slot
  omission/collapse behavior, action placement, metadata/footer behavior,
  background support, and responsive wrapping.
- Render tests cover empty slots, filled eyebrow/actions/metadata/content/footer
  slots, title-only pages, subtitle-only variants where valid, escaping, strict
  undefined, class emission, and descriptor/manifest parity if public surface
  changes.
- Browser tests cover long titles, long actions, no document-level horizontal
  overflow, phone/tablet/desktop widths, search/action adjacency, and route-tab
  proximity when composed in app chrome.
- Collateral plan includes macro docs, descriptor/manifest impact, CSS partial
  and generated CSS if classes or empty wrappers change, generated component
  options, examples, published docs, browser proof, and changelog.

Not now:

- Do not add a `compact_page_header`, `docs_header`, `catalog_header`, or
  `docs_shell` macro from this plan slice.
- Do not change `page_hero` markup, slot wrappers, descriptor metadata, or CSS
  without a separate API/design plan.
- Do not move Bengal `.chirp-theme-*` header selectors into `chirpui-*`
  classes.
- Do not solve page actions by hiding them inside a generic hero contract before
  the page-actions primitive investigation is decided.
- Do not count recipe prose or visual preference as implementation repetition.

### Private Compact Header Candidate Fixture

Status: implemented as browser evidence only, no public API authorized.

Fixture:

- route: `/compact-header-candidate`
- template: `tests/browser/templates/compact_header_candidate_page.html`
- browser proof: `tests/browser/test_compact_header_candidate.py`

Existing primitives tried:

- `page_header(variant="compact")`
- `page_hero(variant="minimal")`
- `search_header`
- `entity_header`
- `document_header`

What the fixture proves:

- `page_header(variant="compact")` can keep a long title, subtitle, metadata,
  and page actions in a dense header without document-level horizontal overflow
  at phone, tablet, and desktop widths.
- `page_hero(variant="minimal")` keeps filled eyebrow, actions, metadata,
  content, and footer regions available for pages that need hero semantics.
- Empty `page_hero` eyebrow, actions, metadata, and footer wrappers collapse
  through current CSS.
- `search_header`, `entity_header`, and `document_header` already cover
  search-first, object-detail, and document-detail header needs in the same
  dense page without a new docs/catalog header macro.

What remains unresolved:

- `page_hero` still emits its structural content wrapper even when the caller
  provides no body content.
- The fixture is artificial and does not count as a second scenario-complete
  compact-docs or compact-reference implementation.
- Empty-wrapper omission, slot wrapper changes, or a new compact hero/header
  primitive would still require a separate public API/design plan.

Decision:

- Keep compact header/page hero maturation in investigation.
- Prefer better guidance for choosing `page_header`, `page_hero`,
  `search_header`, `entity_header`, or `document_header` before introducing a
  new macro.
- Do not add `compact_page_header`, `docs_header`, `catalog_header`,
  `docs_shell`, new `page_hero` parameters, markup changes, CSS, descriptor
  changes, manifest changes, or generated options from this fixture.
- The next qualifying evidence would be a scenario-complete non-Bengal compact
  docs, reference, or catalog page that repeats the same gap after trying these
  primitives.

## Promotion Readiness Queue

Status: decision queue for future implementation slices, no public API
authorized.

The investigations above are useful only if they change sequencing. The current
readiness queue keeps the next work narrow: gather missing implementation evidence,
prototype with existing primitives where possible, and promote only the
smallest contract that survives proof. This queue supersedes any impulse to
start with `application_chrome()`, `catalog_shell()`, `docs_shell()`, or another
whole-frame macro.

No userbase assumption: Chirp UI does not currently have external adoption data
that can carry promotion decisions. Planning must not wait for or cite an
imaginary userbase. The usable substitute is deliberate reference evidence:
external design-system research to define common product pressures, Bengal as a
first-party proving ground, and scenario-complete non-Bengal reference
implementations that exercise current primitives under browser/server proof.

| Candidate | Current Readiness | Primary Blocker | Next Slice | Promotion Bias |
|---|---|---|---|---|
| Page actions primitive | Closest narrow component candidate | Bengal plus private `/page-actions-candidate` prove current composition, but no second scenario-complete reference implementation repeats copy URL / LLM text / AI handoff pressure. | Build or identify a non-Bengal page-action reference implementation after applying `page_header`, `page_hero`, `dropdown_menu`, `share_menu`, and `action_bar`. | Promote a page-local command primitive only if the second independent reference implementation repeats the same gap. |
| Linked nav-tree/sidebar semantics | Good navigation contract candidate | Bengal plus private `/linked-nav-candidate` prove desktop/phone composition, but no second scenario-complete reference implementation repeats the linked-branch gap. | Build or identify a non-Bengal linked-branch reference implementation after applying `sidebar`, `nav_tree(branch_mode="linked")`, `drawer`, and `drawer_trigger`. | Prefer extending hierarchical navigation over a docs/sidebar shell macro only after implementation repetition. |
| Shell response/OOB helper | Good routing-helper candidate, weak Chirp UI ownership | Filesystem pages already solve the best adoption path; two manual route fixture families remain only partial evidence. | Collect a third hand-written route family outside `mount_pages()` that repeats `HX-Target` branching and shell-actions OOB context boilerplate. | Prefer Chirp routing or app-local recipe unless repeated code clearly belongs in Chirp UI. |
| Compact page header / `page_hero` maturation | Good header anatomy candidate | Bengal plus private `/compact-header-candidate` prove current header composition, but no second scenario-complete compact docs/reference/catalog implementation repeats the gap. | Build or identify a non-Bengal dense-header reference implementation after applying `page_header`, `page_hero`, `search_header`, `entity_header`, and `document_header`. | Prefer omitting/collapsing optional regions or clarifying header choice before adding a new macro. |
| Generic application shell macro | Not ready | Existing primitives compose real fixtures; missing pain is smaller contracts. | Continue recipe/browser gauntlets only. | Reject until two independent reference implementations repeat the same missing owned layer. |
| Catalog/docs shell macro | Not ready | Product-specific information architecture is doing the work. | Keep Bengal and catalog learnings as implementation pressure for smaller contracts. | Reject until a reusable shell-owned contract is separable from docs/catalog IA. |

Evidence ladder for any queue item:

1. Recipe pressure: docs, showcase, or one theme demonstrates a useful shape.
2. Partial implementation: one scenario-complete app/theme plus browser proof
   shows a repeated gap, but ownership is still unclear.
3. Promotion candidate: two independent reference implementations tried
   existing primitives and name the same missing contract.
4. Public API proposal: descriptor/macro/CSS/manifest/docs/tests/changelog
   collateral is planned before implementation.
5. Shipped contract: generated outputs and browser proof are green, with
   migration notes when existing surfaces overlap.

Reference implementation evidence intake:

| Evidence Field | Required Record |
|---|---|
| Implementation identity | App/theme/package name, route/page family, and whether it is Bengal, private fixture, recipe prose, or scenario-complete non-Bengal reference usage. |
| Existing primitives tried | Exact Chirp UI primitives used before claiming a gap, including macro variants and response/overlay helpers where relevant. |
| Repeated gap | The smallest behavior current primitives cannot express without repeated boilerplate or theme-owned policy. |
| Proof | Render, server, or browser test that shows the attempted composition and the remaining gap. |
| Promotion boundary | Explicit statement that no public API, descriptor, CSS, manifest, generated docs, or runtime change is authorized by intake alone. |
| Next decision | Either keep as recipe evidence, collect another reference implementation, or stop and ask for a public API/design plan. |

Reference scenario queue:

- [../REFERENCE-IMPLEMENTATION-PLAYBOOK.md](../REFERENCE-IMPLEMENTATION-PLAYBOOK.md)
- [../reference-implementations/README.md](../reference-implementations/README.md)
- [../reference-implementations/PAGE-ACTIONS-AI-REFERENCE.md](../reference-implementations/PAGE-ACTIONS-AI-REFERENCE.md)
- [../reference-implementations/LINKED-NAV-CATALOG-REFERENCE.md](../reference-implementations/LINKED-NAV-CATALOG-REFERENCE.md)
- [../reference-implementations/COMPACT-HEADER-REFERENCE.md](../reference-implementations/COMPACT-HEADER-REFERENCE.md)
- [../reference-implementations/SHELL-RESPONSE-REFERENCE.md](../reference-implementations/SHELL-RESPONSE-REFERENCE.md)
- [../reference-implementations/DENSE-REFERENCE-DATA-REFERENCE.md](../reference-implementations/DENSE-REFERENCE-DATA-REFERENCE.md)
- [../reference-implementations/AGENT-DISCOVERY-REFERENCE.md](../reference-implementations/AGENT-DISCOVERY-REFERENCE.md)

Reference implementation proof status:

| Candidate | Current Proof | What It Allows | What It Does Not Allow |
|---|---|---|---|
| Page actions | `/page-actions-candidate` plus `tests/browser/test_page_actions_candidate.py` | Analyze whether URL copy, LLM text, and AI handoff need a page-local command primitive. | No `page_actions()` macro, descriptor, CSS, manifest, or runtime helper. |
| Linked navigation | `/linked-nav-candidate` plus `tests/browser/test_linked_nav_candidate.py` | Analyze linked parent routes, server-owned open state, active descendants, counts, and drawer fallback. | No new `nav_tree` parameters, sidebar branch macros, or docs/catalog shell. |
| Compact headers | `/compact-header-candidate` plus `tests/browser/test_compact_header_candidate.py` | Analyze whether current header/hero primitives cover dense title/action/tab relationships. | No `compact_page_header`, `docs_header`, `page_hero` slot changes, CSS, or manifest changes. |
| Shell response/OOB | workspace/admin route-family matrix in `tests/test_shell_response_targets.py` plus OOB browser proof | Analyze repeated response-target branching and shell-actions replacement pressure. | No visual shell macro, new HTMX protocol, descriptor, CSS, manifest, or public helper. |
| Dense reference/data pages | `/dense-reference-data-reference` plus `tests/browser/test_dense_reference_data_reference.py` | Analyze whether existing resource, rail, table, params, badge, and callout primitives cover API density. | No data-grid engine, virtualized table, reference-page macro, filter-count API, CSS, manifest, or JavaScript layout runtime. |
| Agent discovery | `tests/test_find_cli.py` details proof for page and pattern primitives | Analyze whether installed metadata steers agents toward real primitives. | No manifest schema changes, copied-source distribution, MCP tooling, or new CLI commands. |

Disqualifiers for promotion evidence:

- artificial/private fixtures without scenario completeness,
- recipe prose, pattern docs, or visual preference without rendered usage,
- Bengal-only selectors or page-context fallbacks when the candidate requires a
  general Chirp UI contract,
- stress tests that prove current primitives work but do not show implementation
  repetition,
- a proposed API sketch without two independent reference implementations and
  collateral planning.

### Post-Fixture Repository Reference Evidence Scan

Scan date: 2026-05-23

Result: no new qualifying scenario-complete non-Bengal reference implementation
exists in this repository after the private fixture phase. This is a planning
input, not a userbase gate. The app-chrome candidates remain in investigation,
with no public API, descriptor, CSS, manifest, generated docs, or runtime
changes authorized.

Search scope:

- `docs/`
- `examples/`
- `tests/browser/templates/`
- `tests/browser/app.py`
- `tests/fixtures/`
- `src/chirp_ui/templates/`
- excluded Bengal theme templates and the private candidate fixtures as
  qualifying reference implementations; they remain evidence, not promotion
  proof

| Candidate | Repo Evidence Found | Classification | Decision |
|---|---|---|---|
| Page actions primitive | `share_menu`, `dropdown_menu`, `action_bar`, `copy_button`, streaming copy controls, forum/social examples, dense object menus, and `/page-actions-candidate`. | Existing primitives, recipes, stress pages, and one private fixture. | No second scenario-complete copy URL / LLM text / AI handoff reference implementation; keep `page_actions()` unauthorized. |
| Linked nav-tree/sidebar semantics | `nav_tree(branch_mode="linked")` in showcase recipes, gauntlet/file-tree stress, rail-to-drawer recipes, reference-docs showcase, knowledge workspace recipe, and `/linked-nav-candidate`. | Recipes, browser stress, and one private fixture. | No second scenario-complete linked-branch sidebar reference implementation; keep sidebar/nav-tree API unchanged. |
| Shell response/OOB helper | Filesystem chrome fixture, two manual route fixture families, `SHELL-TABS-CONTRACT.md`, `HTMX-PATTERNS.md`, and route-tab/page-root tests. | Good recipe and fixture proof, but still routing/page-composition evidence. | No third scenario-complete hand-written route family outside `mount_pages()`; keep helpers fixture-local. |
| Compact header / `page_hero` maturation | Many `page_header` showcase pages, `search_header`, `entity_header`, `document_header`, catalog/resource recipes, and `/compact-header-candidate`. | Existing primitives, recipes, and one private fixture. | No second scenario-complete compact docs/reference/catalog implementation; do not change `page_hero` markup or add compact header macros. |
| Generic application/docs/catalog shell | Dense navigation recipes, rail-to-drawer recipe, application chrome gauntlet, Bengal theme pressure, and published bridge docs. | Broad composition pressure, not one repeated owned shell contract. | Keep mega-shell APIs deferred; continue smaller-contract evidence only. |

What counts next:

- a scenario-complete app/package/theme route family, not a showcase or private
  fixture,
- explicit use of the current primitives listed in the promotion queue,
- a named repeated gap after those primitives are tried,
- focused proof for the attempted composition and remaining gap,
- an explicit stop-and-ask point before any public surface changes.

Next implementation rule:

- If the next slice is evidence gathering, it may add docs, scans, fixtures, or
  private examples with tests.
- If the next slice changes public macro/API, descriptor metadata, emitted
  classes, CSS, manifest, generated component options, or runtime behavior,
  stop and ask before implementing.
- If a candidate cannot name two independent reference implementations,
  continue recipes and browser proof instead of widening the public surface.

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

Only after two independent reference implementations repeat the same missing shape:

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
| `object_header` | Two reference implementations repeat breadcrumbs, title, metadata, actions, and route-row placement with existing primitives. | It removes repeated boilerplate while preserving link-native routes and clear slot ownership. | It mostly aliases `page_header`, `entity_header`, `breadcrumbs`, and `action_strip`. | Descriptor, macro, CSS partial, generated CSS, manifest, generated options, examples, published docs, browser proof, changelog. |
| `chrome_frame` | Two reference implementations repeat the same shell region boundaries and overflow behavior beyond current `app_shell` and layout primitives. | The owned layer is explicit and does not hide product-specific navigation in generic slots. | It becomes a mega-shell or duplicates `app_shell`, `sidebar`, `drawer`, `tray`, and `route_tabs`. | Descriptor, macro, CSS partial, generated CSS, manifest, generated options, recipes, docs, browser proof, changelog. |
| `workspace_shell` | Two reference implementations need the same workspace/sidebar/tab/page-tool contract and cannot express it with filesystem layouts plus current shell blocks. | It improves the Chirp shell contract across routes without app-local wrapper glue. | It encodes one product's IA or requires JavaScript-managed responsive overflow. | Shell contract docs, migration notes, app examples, HTMX/browser proof, generated docs where public API changes. |

Docket entry template:

```text
Candidate:
Reference implementations:
Repeated shape:
Existing primitives tried:
Missing contract:
Accepted / rejected:
Required proof:
Collateral:
Not-now spillover:
```

Current evidence log:

| Evidence | Counts As Reference Implementation? | Composite Signal |
|---|---:|---|
| Dense object chrome showcase recipes | No | Good documentation evidence for layered composition; not enough for `object_header`. |
| Rail-to-drawer showcase recipe and browser fixture | No | Good responsive proof for existing primitives; not enough for `application_chrome`. |
| Application chrome gauntlet families | No | Good browser stress evidence across product shapes; not enough for a stable shell API. |
| Bengal docs chrome | Partial | Packaged-theme proving ground for token/layout parity, but not the same contract as Chirp app shell chrome. |
| Workspace reference browser fixture | Yes | Proves a filesystem-style app shell can compose brand, sidebar, route tabs, breadcrumbs, command trigger, page toolbar, shell actions, and inner HTMX fragments without a new chrome macro. |
| Admin reference browser fixture | Yes | Proves a second route family can repeat the recipe with different tabs, actions, copy, and page tools; the repeated pain is shell/OOB response wiring, not visual composition. |

Reference implementation findings from the first chrome wave:

- The existing `app_shell_layout`, `sidebar`, `route_tabs`, `breadcrumbs`,
  `command_palette_trigger`, `command_bar`, `btn`, and `block` primitives are
  enough to build two app chrome reference implementations without adding
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

Reference implementation proof now covers:

| Contract | Workspace Reference | Admin Reference | Boundary Proof |
|---|---|---|---|
| Persistent shell identity | `Consumer Chrome` brand and workspace sidebar state | same brand with admin sidebar state | shell navigation keeps one `#main` and one `#page-content` |
| Route-backed page chrome | overview/runs/settings route tabs | access/jobs/audit route tabs | tab clicks target only `#page-root` |
| Route-scoped shell actions | `New run` / `Refresh` | `Invite member` / `Audit` | shell navigation updates actions by OOB response |
| Command surface | workspace command trigger opens and focuses palette | admin search trigger is reachable | palette remains page-local, not shell-owned |
| Page tools | filter/refresh/export toolbar | review/suspend/export toolbar | inner filter targets only `#page-content-inner` |
| Responsive sanity | workspace browser proof at desktop and phone widths | admin browser proof at phone width | no duplicate roots after HTMX swaps |

## Composite Decision Review: Reference Implementation Wave 1

Date: 2026-05-13

Decision: keep application chrome recipe-level. Do not add
`application_chrome()`, `workspace_shell()`, `chrome_frame()`, or
`object_header()` from this evidence wave.

Why:

- Two reference implementations repeated the same layered app chrome shape, but the visual
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
| `workspace_shell()` | Defer | Two reference implementations share route tabs and page tools, but differ in IA, actions, and content. | Revisit only after a scenario-complete filesystem reference app shows the same wrapper glue is repeated across many routes. |
| `chrome_frame()` | Defer | The target-boundary problem is real, but the owned layer is not a visual frame. | Consider a narrow shell response/OOB helper outside this plan if route code repeats. |
| `object_header()` | Reject for this wave | The references are workspace/admin route families, not object-detail headers. | Wait for object-page repetition with metadata/actions/route row evidence. |

Accepted next investments:

- Keep the reference browser fixtures as regression proof for shell/page-root
  target ownership.
- Prefer docs and examples that teach `HX-Target` branching and OOB shell
  region updates.
- If more reference implementations repeat the same route-handler boilerplate, evaluate a
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

- Manual-route references still need target branching.
- Filesystem-mounted references can express the same contract declaratively with
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

Open implementation evidence still required before composite work:

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
