# Reference Implementations

Status: canonical reference-evidence index
Date: 2026-05-23

Reference implementation briefs turn market research and Bengal pressure into
buildable first-party scenarios. They are not public API plans. Each brief names
existing Chirp UI primitives to try, required proof, gaps to record, promotion
boundaries, and the decision rule for staying recipe-only or stopping for API
design approval.

Start with [../REFERENCE-IMPLEMENTATION-PLAYBOOK.md](../REFERENCE-IMPLEMENTATION-PLAYBOOK.md).

## Briefs

| Brief | Candidate | Primary Question |
|---|---|---|
| [PAGE-ACTIONS-AI-REFERENCE.md](PAGE-ACTIONS-AI-REFERENCE.md) | Page actions | Can existing header, dropdown, share, action, and copy primitives handle copy URL, LLM text, and AI handoff commands? |
| [LINKED-NAV-CATALOG-REFERENCE.md](LINKED-NAV-CATALOG-REFERENCE.md) | Linked navigation | Can existing sidebar, linked nav tree, and drawer primitives handle parent route links, active children, counts, and phone fallback? |
| [COMPACT-HEADER-REFERENCE.md](COMPACT-HEADER-REFERENCE.md) | Compact headers | Can existing header primitives cover dense docs/reference/catalog identity without new macros or `page_hero` changes? |
| [SHELL-RESPONSE-REFERENCE.md](SHELL-RESPONSE-REFERENCE.md) | Shell response/OOB | Does a third hand-written route family repeat response-target and shell-actions OOB boilerplate outside `mount_pages()`? |
| [DENSE-REFERENCE-DATA-REFERENCE.md](DENSE-REFERENCE-DATA-REFERENCE.md) | Dense reference/data pages | Can resource, filter, table, and feedback primitives cover API/reference density without a data-grid engine? |
| [AGENT-DISCOVERY-REFERENCE.md](AGENT-DISCOVERY-REFERENCE.md) | Agent discovery | Can installed package metadata and durable docs guide agents without new manifest schema or copied-source distribution? |

## Rules

- Do not add public APIs from a reference brief.
- Do not count a private fixture as scenario-complete unless it behaves like a
  realistic route family and records a gap.
- Do not count market research as promotion proof.
- Do not count Bengal as the second independent reference.
- Do use these briefs to decide which browser/server proof should come next.
