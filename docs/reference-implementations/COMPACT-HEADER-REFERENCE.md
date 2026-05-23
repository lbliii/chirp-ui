# Compact Header Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: compact page header / page hero maturation

## Scenario

Build a dense non-Bengal docs/reference/catalog page where page identity,
metadata, search, route proximity, and page actions must stay close without
turning the page into a large hero. Include title-only, long-title, metadata,
actions, search-first, document-detail, and object-detail variants in the same
reference family.

## Existing Primitives To Try

- `page_header(variant="compact")`
- `page_hero(variant="minimal")`
- `search_header`
- `entity_header`
- `document_header`
- `route_tabs`

## Required Proof

- Long titles and action labels wrap without overlap.
- Empty `page_hero` optional regions collapse or remain intentionally visible
  according to the current contract.
- Search-first and object/detail headers do not require a new docs-only macro.
- Route tabs stay near page identity without being mistaken for ARIA tabs.
- Browser proof covers phone, tablet, and desktop widths.
- No document-level horizontal overflow.

## Gap To Record

Record a gap only if current primitives cannot express:

- empty-region omission or collapse without brittle theme CSS,
- compact title/action/metadata placement across multiple page types,
- search/header/action adjacency without duplicated wrappers,
- route-tab proximity without shell-owned page identity,
- a clear choice between `page_header`, `page_hero`, `search_header`,
  `entity_header`, and `document_header`.

## Promotion Boundary

This brief does not authorize `compact_page_header`, `docs_header`,
`catalog_header`, `docs_shell`, new `page_hero` parameters, slot changes,
markup changes, emitted classes, CSS, descriptor changes, manifest updates, or
generated component options.

## Decision Rule

- If existing primitives cover the scenario, improve guidance and keep the
  surface recipe-first.
- If Bengal and a second independent reference implementation repeat the same
  gap, stop and ask for a header API/design plan.
