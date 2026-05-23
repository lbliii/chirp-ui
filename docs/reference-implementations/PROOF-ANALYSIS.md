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
