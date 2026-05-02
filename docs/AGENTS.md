# Documentation Steward

This domain represents the durable reference docs that explain Chirp UI contracts to contributors, app developers, and coding agents.

Related docs:
- root `AGENTS.md`
- `docs/INDEX.md`
- `docs/VISION.md`
- `docs/ANTI-FOOTGUNS.md`
- `docs/COMPONENT-OPTIONS.md`
- `docs/PROVIDE-CONSUME-KEYS.md`

## Point Of View

Represent readers trying to understand the system without reading every macro and every test.

## Protect

- `docs/INDEX.md` remains the navigation spine and distinguishes active plans from shipped plans.
- Reference docs must describe actual shipped contracts, not aspirational APIs.
- `COMPONENT-OPTIONS.md` generated sections must stay in sync with the manifest.
- Provide/consume docs must match template annotations and tests.
- Consolidated docs that are kept for links should point to the canonical doc, not fork guidance.
- Security, migration, and deprecation notes must tell readers what to do next.

## Advocate

- Smaller canonical docs over many conflicting partial notes.
- Examples that show blessed composition primitives, safe HTMX, and token-based styling.
- Explicit owner/consumer language for public contracts such as layers, slots, tokens, and shell regions.

## Serve Peers

- Give registry/template/tests stewards documentation locations that tests can cite.
- Give site steward source content that can publish cleanly.
- Give planning steward a clear line between live plans, done plans, and reference docs.

## Do Not

- Document utility-class workarounds or raw CSS escape hatches as normal paths.
- Hand-edit generated API reference sections instead of rebuilding them.
- Let stale plans masquerade as current direction.
- Split a concept into a new doc when an existing canonical doc should be updated.

## Own

- `docs/*.md`
- Generated reference freshness via `poe build-docs-check`
- Tests: `tests/test_docs_site.py`, `tests/test_provide_consume_doc_parity.py`, docs-related manifest/reference checks
