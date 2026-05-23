# Reference Implementation Playbook

Status: canonical planning support
Date: 2026-05-23

Use this playbook when a Chirp UI candidate is blocked on evidence but cannot
wait for a nonexistent userbase. A reference implementation is deliberate
first-party proof: it behaves like a real app or packaged route family, tries
current primitives first, and records the smallest remaining gap before any
public API is proposed.

This playbook does not authorize public macro/API changes, descriptor fields,
manifest schema fields, emitted classes, CSS, generated component options,
runtime behavior, or extension protocols.

## Evidence Ladder

| Level | Meaning | Promotion Weight |
|---|---|---|
| Market proxy | External design-system research or product screenshots identify common pressure. | Requirements input only. |
| Recipe proof | Docs, examples, or showcase snippets demonstrate a composition. | Useful teaching proof, not promotion proof. |
| Private fixture | Browser/server tests prove current primitives can model a candidate shape. | Regression proof, not enough alone. |
| Scenario-complete reference | A first-party app/theme/package route family exercises current primitives under realistic data, navigation, actions, responsive states, and failure modes. | Qualifying implementation evidence. |
| Promotion candidate | Two independent reference implementations tried existing primitives and named the same missing contract. | Stop and ask for public API/design approval. |

## Scenario-Complete Criteria

A reference implementation must include:

- a named product or docs scenario with realistic content and routes,
- explicit current primitives tried before claiming a gap,
- data and labels long enough to stress wrapping and overflow,
- keyboard, focus, responsive, escaping, and target-boundary proof when relevant,
- a written promotion boundary that says no public API is authorized by the
  reference alone,
- a decision: recipe-only, gather another reference, or stop and ask for API
  design.

## Intake Template

```text
Reference implementation:
Candidate:
Scenario:
Existing primitives tried:
External systems that motivated the scenario:
Repeated gap:
Proof:
Promotion boundary:
Decision:
Not-now:
```

## Priority Candidates

| Candidate | Next Reference Implementation | Existing Primitives To Try | Stop-And-Ask Boundary |
|---|---|---|---|
| Page actions | AI/reference page with copy URL, open/copy LLM text, and non-social page commands. | `page_header`, `page_hero`, `dropdown_menu`, `share_menu`, `action_bar`, `copy_btn`. | `page_actions()` macro, runtime copy/fetch helpers, descriptor/CSS/manifest changes. |
| Linked navigation | Docs/catalog workspace with broad sidebar plus contextual linked branch tree and phone drawer fallback. | `sidebar`, `sidebar_section`, `sidebar_link`, `nav_tree(branch_mode="linked")`, `drawer`, `drawer_trigger`. | New `nav_tree` parameters, sidebar branch macros, docs/catalog shell. |
| Compact header | Dense docs/reference/catalog page comparing page identity, metadata, actions, search, and route proximity. | `page_header(variant="compact")`, `page_hero(variant="minimal")`, `search_header`, `entity_header`, `document_header`. | `compact_page_header`, `docs_header`, `page_hero` markup/slot changes. |
| Shell response/OOB | Hand-written route family outside `mount_pages()` with shell navigation, route-tabs, local fragments, and shell-actions OOB. | Existing `HX-Target` branching recipe, `shell_outlet_attrs`, `route_tabs`, fragment islands. | Public shell response helper or new HTMX convention. |
| Dense reference/data pages | API/reference object browser with filters, module/member cards, table-like data, and empty/loading/error states. | `resource_index`, `resource_card`, `filter_rail`, `filter_bar`, `table`, `params_table`, `search_header`, cards. | Heavy data-grid engine or reference-page macro. |
| Agent discovery | Agent task that discovers the right component using only installed package metadata and durable docs. | `python -m chirp_ui find --details`, manifest, source inventory/map. | Manifest schema changes or new CLI commands. |

## Anti-Goals

- Do not count market research as promotion proof.
- Do not count Bengal alone as the second independent reference.
- Do not create more artificial fixtures unless they test a new failure mode.
- Do not widen public surface area from a candidate sketch.
- Do not clone shadcn, Carbon, Polaris, Material, or Atlassian component names
  when Chirp UI's existing primitives already express the shape.
