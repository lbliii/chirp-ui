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
- `docs/REGISTRY-DISCOVERY.md` for discovery workflow.
- `docs/AGENT-SOURCE-INVENTORY.md` for snippet eligibility.
- `docs/AGENT-SOURCE-MAP.md` for generated-output ownership.
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
