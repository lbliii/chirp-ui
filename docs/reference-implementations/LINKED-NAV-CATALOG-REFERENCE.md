# Linked Nav Catalog Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: linked nav-tree/sidebar semantics

## Scenario

Build a non-Bengal catalog/docs workspace with a broad application sidebar and
a contextual linked branch tree. The tree should include parent route links,
server-owned open state, active child pages, count badges, no-href groups, long
labels, and a phone drawer fallback.

## Existing Primitives To Try

- `sidebar`
- `sidebar_section`
- `sidebar_link`
- `nav_tree(branch_mode="linked")`
- `drawer`
- `drawer_trigger`

## Required Proof

- Parent branches render as anchors, not disclosure summaries.
- Closed branch children are omitted unless the server marks the branch
  `open=true`.
- Active child links render current-page state.
- Count badges are visible and accessible enough for the scenario.
- Long labels stay contained in persistent sidebar and phone drawer contexts.
- Drawer opens, closes with Escape, and returns focus to the trigger.
- The page has no document-level horizontal overflow at 320px.

## Gap To Record

Record a gap only if current primitives cannot express:

- active-descendant parent emphasis separate from current-page state,
- richer child-count metadata than badges can provide,
- repeated sidebar-to-drawer fallback boilerplate,
- compact branch/leaf rhythm across desktop and phone contexts,
- route-link HTMX ownership without app-local repetition.

## Promotion Boundary

This brief does not authorize new `nav_tree` parameters, sidebar branch macros,
emitted classes, CSS, manifest updates, generated component options,
`docs_sidebar`, `catalog_sidebar`, `docs_shell`, or ARIA tree claims.

## Decision Rule

- If existing primitives cover the scenario, keep linked navigation as a
  recipe and browser-proofed composition.
- If Bengal and a second independent reference implementation repeat the same
  gap, stop and ask for a navigation API/design plan.
