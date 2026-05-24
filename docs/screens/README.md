# Screen Catalog

Status: initial catalog
Date: 2026-05-23

The screen catalog is the taste-floor layer above primitives, components, and
patterns. Each entry describes a complete product situation with a profile,
composition map, fixture route, proof, and agent guidance.

Screen entries are recipes, not public macros. They do not authorize new
component APIs, manifest fields, theme-pack metadata, or utility classes.

Typography guidance for these screens uses the recipe-only role matrix in
`docs/decisions/typography-role-matrix.md`. Role names such as `metadata`,
`metric`, `object-title`, and `hero-display` describe screen intent; they are
not public token names or utility classes.

## Available Golden Screens

| Screen | Profile | Fixture | Use When |
|---|---|---|---|
| [Command Center](command-center.md) | `atlas` | `/screen-command-center` | Operational dashboards need metrics, queues, incident state, activity, and selected-object inspection. |
| [Review Queue](review-queue.md) | `sage` | `/screen-review-queue` | Triage/review tools need filters, a result collection, selected-object inspector, and state-rich items. |
| [Agent Run Monitor](agent-run-monitor.md) | `signal` candidate | `/screen-agent-run-monitor` | Agent, automation, build, import, or evaluation jobs need live state, artifacts, logs, and retry context. |
| [Product/Docs Home](product-docs-home.md) | `ember` | `/screen-product-docs-home` | Product and docs entry pages need identity, proof, lifecycle explanation, entry points, and CTA. |

## Agent Selection Rule

Choose a screen archetype before choosing individual components.

- Use **Command Center** for operational SaaS, infrastructure, admin,
  monitoring, and executive/operator dashboards.
- Use **Review Queue** for moderation, approval, support triage, inbox review,
  search results with selected detail, and queue-based work.
- Use **Agent Run Monitor** for live agent traces, automation runs, evaluation
  jobs, imports, builds, deploys, and recovery workflows.
- Use **Product/Docs Home** for product pages, docs homes, library homepages,
  launch pages, and internal platform entry pages.
- If the requested product situation does not match a catalog entry, start from
  the closest pattern doc and record the gap instead of inventing utility
  classes.

## Promotion Boundary

Screen catalog entries can become copyable guidance only when they cite:

- a source template or fixture route,
- realistic data and state coverage,
- responsive/browser proof,
- profile guidance,
- no utility-style local class vocabulary as the normal authoring path.

The first implementation routes live in the component showcase because the
catalog is still recipe-first. Public macros such as `command_center()` or
`review_queue()` remain not-now until repeated independent screens prove a
stable API.
