# Reference Recipe Guidance

Status: active recipe guidance
Date: 2026-05-23

This is source-only authoring guidance for candidates that have reference proof
but are not promoted public APIs. It does not authorize new public APIs,
descriptors, macros, CSS, manifest schema, generated options, runtime helpers,
or copied-source workflows.

Use this guide after `PROOF-ANALYSIS.md`: start from `PROOF-ANALYSIS.md`,
prefer current primitives, record a repeated gap only when current primitives
fail in another scenario-complete reference, then stop and ask for API design
before changing public contracts.

## Recipe Index

| Candidate | Current Guidance |
|---|---|
| Dense reference/data pages | Use resource, card, rail, table, params, badge, and callout primitives before considering data-grid or reference-page APIs. |
| Agent discovery | Use installed registry discovery and source maps before considering manifest schema or copied-source workflow changes. |
| Page actions | Compose header actions, dropdowns, share, action bars, and copy buttons before considering a page-actions primitive. |
| Linked navigation | Compose sidebar, linked nav tree, and drawer fallback before considering new nav-tree/sidebar API. |
| Compact headers | Choose among existing header primitives before considering compact header or page-hero markup changes. |
| Shell response/OOB | Keep target branching route-local or filesystem-mounted before considering response helper APIs. |

## Dense Reference/Data Pages

Use this recipe for API reference, module browser, object catalog, and dense
documentation pages that need search, filters, cards, parameter tables, and
feedback states.

Start with:

- `resource_index` for the search/filter/results frame.
- `resource_card` for module, class, endpoint, or object summaries.
- `filter_rail` only when the filter set is persistent navigation-like scope.
- `filter_bar` for route-local filter controls.
- `table` for compact member lists.
- `params_table` for API parameter and return-value data.
- `badge` for maturity/status labels, not overloaded filter metadata.
- `callout` for empty, loading, warning, and error states.

Authoring rules:

- Keep dense reference pages recipe-first when existing primitives preserve
  search reachability, readable names, and no document-level overflow.
- Prefer `resource_index` plus `resource_card` before creating a bespoke
  reference-page wrapper.
- Prefer `table` or `params_table` before proposing a data-grid engine.
- Treat counts in rails as navigation metadata only when they behave like scope
  counts; do not reuse them for rich filter state without new proof.
- Record another reference only if copyable anchors, route-local actions,
  filter metadata, or member-list rhythm fails in a second dense reference.

Not authorized: data-grid engine, virtualized table, reference-page macro,
filter-count API, JavaScript layout runtime, emitted classes, CSS, descriptor
changes, manifest updates, or generated options.

## Agent Discovery

Use this recipe when an agent or contributor needs to discover a component,
primitive, pattern, or not-now boundary from an installed Chirp UI package.

Start with:

- `python -m chirp_ui find --details` for broad local discovery.
- `python -m chirp_ui find --role=pattern --details` for recipe-like surfaces.
- `python -m chirp_ui find --maturity=experimental --details` for stabilization
  audits.
- `docs/agents/registry-discovery.md` for discovery workflow.
- `docs/agents/agent-source-inventory.md` for snippet eligibility.
- `docs/agents/agent-source-map.md` for generated-output ownership.
- `docs/COMPONENT-OPTIONS.md` for generated macro options.

Authoring rules:

- Discover first, then inspect durable docs, then verify with focused tests.
- Treat `authoring=preferred` primitives as the first composition vocabulary.
- Treat `maturity=experimental` and `role=pattern` as caution labels, not
  preferred stable APIs.
- Treat browser tests and proof ledgers as source-only evidence, never automatic
  copyable snippets.
- Add guidance before adding manifest schema when existing metadata answers the
  user or agent task.
- Record a schema gap only when repeated tasks need the same missing field or
  query shape.

Not authorized: manifest schema changes, descriptor fields, new CLI commands,
MCP/server tooling, public extension protocols, generated option changes, or
copied-source installation.

## Page Actions

Use this recipe for page-local commands such as copy URL, open LLM text, copy
known prompt text, visible secondary actions, and external assistant handoff
links.

Start with:

- `page_header` actions for title-adjacent placement.
- `page_hero` actions only when the page genuinely needs hero treatment.
- `dropdown_menu` for grouped page commands.
- `share_menu` for canonical share/copy URL behavior.
- `action_bar` for visible commands that should not hide in a menu.
- `copy_button` for known local text with feedback.

Authoring rules:

- Keep commands near page identity, usually in compact `page_header` actions.
- Use `dropdown_menu` for grouped non-social commands and long labels.
- Use `share_menu` when the command is truly share/copy URL behavior.
- Use `copy_button` only for known text; do not imply fetched LLM text support
  without a tested route and feedback contract.
- Use ordinary safe external links for assistant handoff; do not claim a
  semantic AI handoff protocol.
- Record another reference only if URL, LLM text, AI handoff, grouped command,
  or async copy/fetch ownership repeats as app-owned glue.

Not authorized: `page_actions()` macro, copy/fetch runtime helper, AI handoff
protocol, descriptor changes, emitted classes, CSS, manifest updates, generated
options, or public page-actions docs.

## Linked Navigation

Use this recipe for catalog, docs, or workspace navigation where parent branch
labels are real route links and children are controlled by server-owned open
state.

Start with:

- `sidebar` for persistent broad navigation.
- `sidebar_section` for app-level groups.
- `sidebar_link` for broad app routes and active route matching.
- `nav_tree(branch_mode="linked")` for contextual branch links.
- `drawer` and `drawer_trigger` for phone fallback.

Authoring rules:

- Use linked branch mode when parent branch labels must navigate.
- Let the server decide `open=true`; do not rely on hidden client-owned
  children for route context.
- Keep active child state as current-page state; do not imply parent
  active-descendant semantics unless the recipe explicitly styles it.
- Treat branch counts as lightweight metadata, not rich filter state.
- Keep the persistent sidebar and drawer fallback data shape identical.
- Record another reference only if active-descendant emphasis, count metadata,
  sidebar-to-drawer duplication, or route HTMX ownership repeats as a gap.

Not authorized: new `nav_tree` parameters, sidebar branch macros, emitted
classes, CSS, manifest updates, generated options, `docs_sidebar`,
`catalog_sidebar`, `docs_shell`, or ARIA tree claims.

## Compact Headers

Use this recipe when a docs, reference, catalog, or product page needs identity,
metadata, search, route proximity, and actions without a large hero.

Start with:

- `page_header(variant="compact")` for ordinary dense page identity.
- `page_hero(variant="minimal")` only when the page still needs hero slots.
- `search_header` for search-first resource pages.
- `entity_header` for object/detail surfaces.
- `document_header` for document-oriented pages.
- `route_tabs` for link-native local route navigation near page identity.

Authoring rules:

- Prefer `page_header(variant="compact")` for title, subtitle, metadata, and
  actions that should stay close.
- Use `page_hero` when eyebrow, metadata, content, actions, or footer regions
  are part of the page's intended hero treatment.
- Use `search_header` when search is the primary page action, not a header
  accessory.
- Use `entity_header` or `document_header` when object/document semantics are
  stronger than generic page identity.
- Keep `route_tabs` link-native; do not describe them as ARIA tab widgets.
- Record another reference only if empty optional regions, title/action
  placement, search adjacency, or route proximity repeats as a gap.

Not authorized: `compact_page_header`, `docs_header`, `catalog_header`,
`docs_shell`, new `page_hero` parameters, slot changes, markup changes, emitted
classes, CSS, descriptor changes, manifest updates, or generated options.

## Shell Response/OOB

Use this recipe when hand-written route families need persistent shell
navigation, route-tab page roots, local fragments, and route-scoped shell
actions.

Start with:

- Filesystem `mount_pages()` when the app can use filesystem-mounted pages.
- `SHELL-TABS-CONTRACT.md` for response target rules.
- `HX-Target` branching for hand-written routes.
- `shell_outlet_attrs` for shell-owned outlets.
- `route_tabs` targeting `#page-root`.
- Local fragment targets such as `#page-content-inner`.
- Shell actions OOB replacement only when shell-scoped actions change.

Authoring rules:

- Return a full page for normal requests.
- Do not infer page-root fragments from `HX-Request` without `HX-Target`.
- Return shell-owned content plus OOB shell actions for `HX-Target: main`.
- Return only page-root chrome/content for `HX-Target: page-root`.
- Return only local content for local fragment targets.
- Keep helper functions route-local until three independent hand-written route
  families repeat the same boilerplate and ownership is settled.

Not authorized: public `chirp_ui` helper, Chirp routing API, visual shell macro,
component descriptor, emitted classes, CSS, manifest updates, generated options,
or new HTMX protocol.
