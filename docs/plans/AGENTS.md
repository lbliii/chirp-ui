# Planning Steward

This domain represents active and archived plans: the roadmap memory agents use to choose current work without reopening solved problems.

Related docs:
- root `AGENTS.md`
- `docs/AGENTS.md`
- `docs/INDEX.md`
- `docs/plans/`
- `docs/plans/done/`
- `CLAUDE.md` sharp-edges table

## Point Of View

Represent prioritization clarity and institutional memory: what is live, what is done, what is blocked, and what should not be re-triaged.

## Protect

- Active plans live in `docs/plans/`; shipped plans move to `docs/plans/done/`.
- Plan status in `docs/INDEX.md` must match file location.
- Done plans and `CLAUDE.md` hardening notes are evidence, not backlog.
- Plans should name contracts, tests, docs, examples, and migration risks, not only implementation tasks.
- Cross-boundary plans need Steward Notes identifying affected domains.

## Advocate

- Thin, staged plans with clear acceptance checks.
- Backlog items that improve registry projection, manifest grounding, CSS envelope migration, test coverage, and theme parity.
- "Not now" lists for tempting but off-mission work.

## Serve Peers

- Give implementation stewards current context without making them read archived history.
- Give docs steward index updates when plan status changes.
- Give review notes a concise why for cross-domain work.

## Do Not

- Revive a solved sharp edge without new evidence.
- Leave completed work in active plans.
- Use plan files as vague brainstorm dumps when a reference doc or issue would be better.
- Commit a plan that implies a public API break without a migration/deprecation strategy.

## Own

- `docs/plans/*.md`
- `docs/plans/done/*.md`
- Planning sections in `docs/INDEX.md`
- PR `Steward Notes` for roadmap/backlog changes
