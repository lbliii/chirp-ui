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
