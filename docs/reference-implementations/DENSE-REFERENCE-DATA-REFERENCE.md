# Dense Reference Data Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: dense reference/API/data page primitives

## Scenario

Build a non-Bengal API/reference object browser with module/member cards,
filters, search, table-like parameter data, empty states, loading states, error
states, and long technical names. The scenario should approximate Carbon and
Polaris dense admin/data pressure while staying within Chirp UI's lightweight
server-rendered contract.

## Existing Primitives To Try

- `resource_index`
- `resource_card`
- `filter_rail`
- `filter_bar`
- `search_header`
- `table`
- `params_table`
- `card`
- `badge`
- `callout`

## Required Proof

- Filter and search controls stay reachable at phone and desktop widths.
- Long module, function, parameter, and type names wrap without overflow.
- Empty, loading, and error states are represented with existing feedback
  primitives.
- Parameter data remains readable without introducing a heavy grid engine.
- Cards and table-like regions keep landmarks/headings understandable.
- Browser proof covers 320, 768, and 1280 widths.

## Gap To Record

Record a gap only if current primitives cannot express:

- dense member-list rhythm,
- module/function/class card anatomy,
- filter counts as metadata rather than notifications,
- reference-specific empty/loading/error states,
- parameter table readability,
- copyable anchors or route-local reference actions.

## Promotion Boundary

This brief does not authorize a data-grid engine, virtualized table,
reference-page macro, new filter-count API, emitted classes, CSS, descriptor changes,
manifest updates, generated component options, or JavaScript layout runtime.

## Decision Rule

- If existing primitives cover the scenario, add recipe guidance and keep the
  surface recipe-only.
- If two independent reference implementations repeat the same data/reference
  gap, stop and ask for a narrow primitive design.
