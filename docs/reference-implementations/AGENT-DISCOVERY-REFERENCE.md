# Agent Discovery Reference Brief

Status: reference implementation brief
Date: 2026-05-23
Candidate: registry and agent discovery product surface

## Scenario

Run a realistic agent task that starts with only an installed Chirp UI package
and durable docs. The agent must discover the right component or recipe using
manifest-backed metadata instead of guessing component names, utility classes,
or unsupported macro parameters.

## Existing Surfaces To Try

- `python -m chirp_ui find --details`
- `python -m chirp_ui find --maturity=experimental --details`
- `python -m chirp_ui find --role=pattern --details`
- `build_manifest()`
- `docs/agents/agent-source-inventory.md`
- `docs/agents/agent-source-map.md`
- `docs/agents/registry-discovery.md`
- `docs/COMPONENT-OPTIONS.md`

## Required Proof

- Search by job, category, maturity, authoring, and role returns useful
  candidates.
- Details expose macro, template, runtime requirements, slots, maturity,
  authoring, and role.
- Agent-source docs tell the agent which sources are source-only versus copyable-curated.
- Experimental and recipe-only surfaces are not presented as preferred stable APIs.
- The task can end with a valid existing primitive or a documented not-now boundary.

## Gap To Record

Record a gap only if existing metadata cannot answer:

- which primitive to choose,
- whether a surface is stable, experimental, recipe-only, or compatibility,
- which macro/template/runtime/slot contract exists,
- whether a source is copyable or only grounding material,
- why a requested component should remain not-now.

## Promotion Boundary

This brief does not authorize manifest schema changes, new descriptor fields,
new CLI commands, MCP/server tooling, public extension protocols, generated component option changes, or copied-source installation.

## Decision Rule

- If current `find`, manifest, and source docs answer the task, improve
  examples only.
- If repeated agent tasks need the same missing field or query shape, stop and
  ask for a manifest/discovery API plan.
