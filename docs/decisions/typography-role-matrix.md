# Typography Role Matrix

Status: recipe-only audit matrix
Date: 2026-05-24
Plan: `docs/plans/PLAN-visual-taste-floor-saga.md`
Research input: `docs/decisions/typography-rhythm-taste-floor.md`

This matrix turns the typography research into screen-level authoring guidance.
It does not add public token names, utility classes, macro parameters, manifest
fields, or theme-pack metadata.

## Audit Scope

Commands used for this slice:

- `rg -n "clamp\\(" src/chirp_ui/templates/chirpui.css src/chirp_ui/templates/themes docs/fundamentals/typography.md`
- `rg -n "font-size|font-weight|line-height|letter-spacing|chirpui-ui|chirpui-prose|chirpui-font" examples/component-showcase/templates/showcase/operations_shell.html examples/component-showcase/templates/showcase/support_shell.html examples/component-showcase/templates/showcase/screen_agent_run_monitor.html examples/component-showcase/templates/showcase/screen_product_docs_home.html`
- `rg -n "line-height:\\s*[0-9]|font-weight:\\s*(bold|500|600|700)|letter-spacing:\\s*[-0-9.]" src/chirp_ui/templates/css/partials -g "*.css"`
- `rg -n -- "--chirpui-font-md" src/chirp_ui/templates/css/partials/167_workspace-primitives.css src/chirp_ui/templates/chirpui.css`

## Audit Findings

| Finding | Evidence | Decision |
|---|---|---|
| Core UI and prose sizes are fluid through viewport `clamp()` values. | `docs/fundamentals/typography.md` and generated `chirpui.css` define `--chirpui-font-sm` through display prose sizes with viewport middle terms. | Treat as a role-matrix risk. Dense app UI should prove stable rem-based roles before public token changes. |
| Golden screen templates do not hard-code typography declarations. | The four golden screen templates contain no direct `font-size`, `font-weight`, `line-height`, or `letter-spacing` declarations. | Keep screen fixtures macro/composition-led; do the type pass through components, existing tokens, or recipe-local CSS only when necessary. |
| Component CSS has many literal line-height, weight, and tracking values. | The partial audit found `line-height: 1`, `font-weight: 500`, and tracked labels across buttons, forms, navigation, ASCII components, and workspace primitives. | Not all literals are defects. Classify them by role before replacing them with public tokens. |
| Workspace primitives used an undefined typography token. | `chirpui-result-card__title` and `chirpui-inspector-panel__title` referenced `--chirpui-font-md`, which was not a defined token. | Fixed by using `--chirpui-font-base` in the source partial and regenerated CSS. |
| Metadata and metrics rely on repeated size/color patterns. | Workspace primitives use muted `xs/sm` labels, tight line-height, and larger metric/title values across filters, metrics, result cards, and inspector panels. | Candidate for recipe-only role mapping first: `metadata`, `metric`, `object-title`, `panel-title`, and `dense-body`. |

## Role Matrix

These role names are recipe vocabulary only.

| Role | Current Token Baseline | Screen Surfaces | Notes |
|---|---|---|---|
| `page-title` | `--chirpui-ui-lg` or existing page header output | All golden screens | Must distinguish app page title from product hero display. |
| `panel-title` | `--chirpui-font-lg` plus tight line-height | Command Center, Review Queue, Agent Run Monitor | Used for scoped panels such as timelines, queues, inspectors, and metric groups. |
| `object-title` | `--chirpui-font-base` plus tight line-height | Review Queue result cards, inspector panels, command workload cards | Fixed from the undefined `--chirpui-font-md` reference. |
| `dense-body` | `--chirpui-font-sm` | Workload summaries, ticket summaries, artifact descriptions | Needs line-height proof for two-line descriptions and long labels. |
| `metadata` | `--chirpui-font-xs` or `--chirpui-font-sm` with `--chirpui-text-muted` | Owners, routes, counts, provenance, timestamps, footer rows | Muted text should stay legible and should not become disabled-looking. |
| `count-label` | `--chirpui-font-xs` with compact/tight line-height | Filter counts, badges, scoped metrics | Needs stable minimum sizes so counts do not resize controls. |
| `metric` | `--chirpui-font-lg` or `--chirpui-ui-lg` | Metric strips, stat cards, proof metrics | Numeric emphasis should not inherit generic title styling by accident. |
| `status-label` | Existing badge/status component typography | All state-rich screens | State text needs semantic color plus readable label treatment, not color alone. |
| `log-line` | Existing code scale | Agent Run Monitor | Needs proof for dense log lines, wrapping, and scroll containers. |
| `hero-display` | Existing prose/display scale | Product/Docs Home | Responsive display type belongs here, not in dense app chrome. |
| `proof-copy` | `--chirpui-prose-base` or `--chirpui-ui-base` by context | Product/Docs Home proof band, stories, CTA | Needs measure and rhythm more than size escalation. |

## Profile Implications

| Profile | Type Intent | Immediate Constraint |
|---|---|---|
| `atlas` | Compact, operational, high-signal titles and metadata. | Avoid hero/display sizing in dashboards. |
| `sage` | Low-glare review rhythm with calm object titles and readable detail. | Muted text must remain usable for queue decisions. |
| `signal` | Technical live-state typography for metrics, logs, artifacts, and traces. | Logs and state labels need their own proof before token promotion. |
| `ember` | Expressive product/docs type with stronger display and proof rhythm. | Display type must not leak into app workspace components. |

## Implementation Outcome

Completed in the typography implementation slice:

1. The four screen docs now map their typography roles with recipe-only
   language.
2. Workspace primitives use existing tokens for object titles, dense body copy,
   metadata rhythm, count labels, and metric values.
3. Product/docs surfaces use existing prose/display, line-height, measure, and
   numeric treatment tokens without adding public role tokens.
4. Product/Docs Home now uses `page_hero` so the `hero-display` role actually
   reaches the first viewport.
5. Browser proof checks computed typography hierarchy, body/log line-height,
   tabular numeric metrics, and no document horizontal overflow.

If repeated workarounds remain after another independent screen pass, Stop and
ask for a public typography-token promotion plan.

## Not Now

- Public role tokens such as `--chirpui-type-object-title`.
- Typography utility classes for these roles.
- Font dependencies or bundled font assets.
- Manifest metadata for typography roles.
