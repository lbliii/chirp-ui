# Reference Proof Analysis

Status: active proof-analysis ledger
Date: 2026-05-23

This ledger converts scenario-complete reference fixtures into decisions. It is
not a public API plan. A row can move a candidate toward recipe guidance, more
reference evidence, or a stop-and-ask API design proposal, but it cannot
authorize descriptors, macros, CSS, manifest schema, generated options,
runtime helpers, or copied-source workflows by itself.

## Decision Rules

- Existing primitives working in one private fixture means recipe guidance or
  proof analysis, not public API.
- Bengal plus one private fixture is still one theme pressure path plus one
  controlled reference. It is not enough to promote a registry-owned component.
- Promotion requires two independent scenario-complete references that tried
  current primitives and record the same missing contract.
- Response-helper promotion also requires owner clarity: Chirp routing,
  Chirp UI, or app-local recipe.
- Agent/discovery expansion requires repeated missing metadata or query shape,
  not general preference for a richer manifest.

## Current Decisions

| Candidate | Current Decision | Next Slice |
|---|---|---|
| Page actions | Keep in investigation. | Analyze whether current primitives merely split ownership or actually fail; collect a second non-Bengal reference before API design. |
| Linked navigation | Keep as recipe/browser-proofed composition. | Analyze guidance gaps around linked branches, active descendants, counts, and drawer fallback. |
| Compact headers | Keep recipe-first. | Analyze header choice guidance and empty optional-region behavior before any header API proposal. |
| Shell response/OOB | Keep route-local and recipe-first. | Analyze repeated target-branching boilerplate and owner boundary before helper design. |
| Dense reference/data pages | Keep recipe-first after current proof unless analysis finds a repeated dense-reference gap. | Compare fixture outcomes against data-grid/reference-page ambitions. |
| Agent discovery | Keep manifest schema closed after current proof unless repeated tasks need missing fields. | Compare `find --details` and source maps against agent routing needs. |

## Non-Authorizations

- No `page_actions()` macro.
- No new `nav_tree` parameters or sidebar branch macros.
- No `compact_page_header`, docs header, catalog header, or `page_hero` slot
  changes.
- No visual shell macro or new HTMX protocol.
- No data-grid engine, virtualized table, reference-page macro, or JavaScript
  layout runtime.
- No manifest schema changes, new descriptor fields, copied-source component
  workflow, or MCP/server tooling.

## Dense Reference/Data Analysis

Proof source: `/dense-reference-data-reference` and
`tests/browser/test_dense_reference_data_reference.py`.

Existing primitives tried: `resource_index`, `resource_card`, `filter_rail`,
`filter_bar`, `search_header`, `table`, `params_table`, `card`, `badge`, and
`callout`.

What worked:

- Resource search, filter controls, selection state, and result cards compose
  without a reference-page macro.
- Module cards, member tables, parameter tables, and feedback states can coexist
  in one dense route using existing primitives.
- Long module, member, and parameter names stay inside the document at 320,
  768, and 1280 widths.
- Empty, loading, and error states can use `callout` and ordinary content
  semantics without a reference-specific state primitive.

Recorded gaps:

- Filter counts currently read like navigation badges rather than structured
  filter metadata.
- Dense member-list rhythm is acceptable for a private fixture, but a second
  reference should compare `table`, `params_table`, and card rhythm before a
  data-display primitive is considered.
- Copyable anchors and route-local reference actions were not exercised enough
  to justify a reference-page action contract.

Decision: keep dense reference/data pages recipe-first. The fixture is evidence
against immediate data-grid, virtualized table, reference-page macro, or
JavaScript layout runtime work. The next useful slice is guidance that shows
when to combine `resource_index`, `resource_card`, `table`, and `params_table`,
plus another independent dense reference if a specific gap repeats.

## Agent Discovery Analysis

Proof source: `tests/test_find_cli.py`,
`docs/AGENT-SOURCE-INVENTORY.md`, and `docs/AGENT-SOURCE-MAP.md`.

Existing surfaces tried: `python -m chirp_ui find --details`,
`python -m chirp_ui find --role=pattern --details`,
`python -m chirp_ui find --maturity=experimental --details`,
`build_manifest()`, generated component options, and source inventory docs.

What worked:

- Detailed CLI discovery exposes component name, category, maturity, authoring,
  role, macro, template, runtime requirements, slots, and summary from the
  installed package.
- Page and pattern searches surface real primitives such as `page_header`,
  `page_hero`, `resource-index`, `filter-rail`, and `result-card`.
- Unpromoted proposal names such as `page-actions`, `compact-page-header`,
  `reference-page`, and `data-grid` are absent from discovery output.
- Source inventory and source map docs distinguish source-only proof from
  copyable-curated snippets.

Recorded gaps:

- Discovery does not yet link directly from a component to proof artifacts or
  reference-analysis rows.
- Agent workflows still need guidance that connects a user intent to
  `find --details`, durable docs, and verification commands.

Decision: keep the manifest schema and descriptor fields closed. Current
metadata solves the immediate agent-routing problem without a copied-source
workflow, new CLI command, MCP/server tool, or manifest expansion. The next
useful slice is guidance and examples for a discover/apply/verify workflow; a
schema change should wait for repeated tasks that need the same missing field.

## Page Actions Analysis

Proof source: `/page-actions-candidate` and
`tests/browser/test_page_actions_candidate.py`.

Existing primitives tried: `page_header`, `page_hero`, `dropdown_menu`,
`share_menu`, `action_bar`, and `copy_btn`.

What worked:

- Title-adjacent actions fit inside `page_header(variant="compact")`.
- Existing dropdown, share, visible action, and copy primitives can express
  copy URL, open LLM text, copy known prompt text, and external assistant
  handoff commands in one route.
- Long command labels stay inside the dropdown at phone width without document
  overflow.
- Copy feedback for known text works without a page-actions runtime.

Recorded gaps:

- Ownership is split: canonical URL, prompt text, AI handoff, grouped commands,
  and visible action affordances live across several primitives.
- The fixture did not exercise fetched LLM text, async copy/fetch status, or
  permissioned command visibility.
- External assistant handoff is only a safe link pattern; it is not a semantic
  AI handoff contract.

Decision: keep page actions in investigation. The fixture proves current
composition is viable, so it blocks an immediate `page_actions()` macro,
descriptor, CSS, manifest, generated options, or runtime helper. A public API
proposal needs a second non-Bengal reference that repeats the same
title-adjacent URL/LLM/AI command ownership gap after trying the existing
primitives.

## Linked Navigation Analysis

Proof source: `/linked-nav-candidate` and
`tests/browser/test_linked_nav_candidate.py`.

Existing primitives tried: `sidebar`, `sidebar_section`, `sidebar_link`,
`nav_tree(branch_mode="linked")`, `drawer`, and `drawer_trigger`.

What worked:

- Broad app sidebar links and a contextual linked branch tree can coexist in
  one route without a docs/catalog shell macro.
- Parent branches render as route anchors while children remain server-owned
  and appear only when `open=true`.
- Active child state, badges/counts, no-href groups, and long labels survive
  persistent sidebar and phone drawer contexts.
- Drawer fallback opens, closes with Escape, and keeps the linked tree usable
  at phone width.

Recorded gaps:

- Active-descendant parent emphasis is still a recipe convention rather than a
  registry-level semantic.
- Counts are visually useful, but they are still badge-like rather than a
  structured navigation metadata contract.
- Sidebar-to-drawer fallback requires app-owned duplication of the tree shape.

Decision: keep linked navigation as recipe/browser-proofed composition. Current
primitives cover the reference well enough to block new `nav_tree` parameters,
sidebar branch macros, emitted classes, CSS, manifest updates, `docs_sidebar`,
`catalog_sidebar`, `docs_shell`, or ARIA tree claims. The next useful slice is
guidance for linked branch recipes and a second independent reference only if
the same active-descendant/count/fallback gap repeats.
