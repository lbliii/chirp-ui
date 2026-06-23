# Screen Archetype Matrix

Status: recipe catalog expansion
Date: 2026-05-23

This matrix is the screen-level selection layer for Chirp UI app mocks. It
names complete product situations before agents or app authors choose
components.

The matrix is recipe-only. It does not create public screen macros, manifest
fields, theme-pack names, typography role tokens, or utility classes.

## Canonical Archetypes

| Archetype | Profile | Status | Start From | Use When | Visual Job |
|---|---|---|---|---|---|
| `command-center` | `atlas` | Golden fixture | [Command Center](command-center.md) | Operators need metrics, queues, incidents, activity, and selected-object inspection. | Make dense operational state feel composed instead of becoming a generic card dashboard. |
| `review-queue` | `sage` | Golden fixture | [Review Queue](review-queue.md) | Reviewers need filters, result records, state, batch readiness, and an inspector. | Keep triage work calm, scannable, and decision-oriented. |
| `agent-run-monitor` | `signal` candidate | Golden fixture | [Agent Run Monitor](agent-run-monitor.md) | A run, automation, import, deploy, or evaluation needs live state, logs, artifacts, and recovery actions. | Treat state, provenance, logs, and retry controls as designed product UI. |
| `product-docs-home` | `ember` | Golden fixture | [Product/Docs Home](product-docs-home.md) | A product, library, or platform needs identity, proof, entry points, lifecycle explanation, and CTA. | Make the first viewport feel authored without using marketing-card clutter. |
| `data-dense-market` | `atlas` | Golden fixture | [Data-Dense Market](data-dense-market.md) | Traders and finance operators need ticker search, movers, market catalog, selected-symbol inspection, and live activity. | Make number-heavy market state feel premium and composed instead of spreadsheet-like. |
| `settings-detail` | `sage` | Planned recipe target | Review Queue plus form/panel primitives | Users need account, billing, workspace, policy, or integration settings with save state. | Make controls and explanatory copy feel intentional instead of form-heavy. |
| `data-index-detail` | `atlas` or `sage` | Planned recipe target | Review Queue plus dense reference-data proof | Users need a table/list, filters, saved views, selected detail, and bulk-safe actions. | Balance scan density, selection, and detail without collapsing into spreadsheet chrome. |
| `setup-flow` | `ember` or `sage` | Planned recipe target | Product/Docs Home plus wizard/form patterns | Users need onboarding, import setup, credential connection, or guided configuration. | Make progression, prerequisites, validation, and recovery visible without tutorial clutter. |
| `dashboard-overview` | `atlas` | Planned recipe target | Command Center with weaker incident/inspector emphasis | Leaders need a periodic summary across health, adoption, outcomes, and exceptions. | Keep summary metrics and narrative context specific instead of a neutral stat grid. |

## Selection Flow

1. Name the user's product situation in one sentence.
2. Choose the closest archetype and profile from the matrix.
3. Start from the linked golden fixture when one exists.
4. If the archetype is only a planned recipe target, compose from the named
   existing screen and record the missing relationship as evidence.
5. Use the screen entry template before adding new page-local CSS.

## Planned Recipe Rules

Planned recipe targets are not weaker because they are undocumented; they are
weaker because they have not yet survived fixture data, responsive proof, and
promotion review.

For a planned recipe target:

- reuse existing primitives and component macros first,
- preserve the intended profile instead of inventing a new theme mood,
- name populated, loading, empty, invalid, disabled, warning, and error states,
- capture any repeated local CSS workaround in
  [promotion-ledger.md](promotion-ledger.md),
- avoid copied utility-style class names, even for temporary layout fixes.

## Taste Floor Criteria

Every archetype should make these decisions explicit before it becomes a
fixture-backed screen:

- shell: app, workspace, site, or flow shell ownership,
- hierarchy: page title, region titles, object titles, metadata, and actions,
- density: roomy, standard, compact, or dense,
- rhythm: where stack, cluster, grid, frame, panel, and inspector relationships
  own spacing,
- state: selected, pending, empty, loading, warning, error, disabled, and
  recovered state coverage,
- visual interest: state, metadata, profile mood, proof, or narrative, not
  decoration,
- anti-use: screens or moods where the archetype should not be applied.

## Not Authorized

This matrix does not authorize:

- `settings_detail()`, `data_index_detail()`, `setup_flow()`,
  `dashboard_overview()`, or any other public screen macro,
- a Python screen registry,
- `chirpui-manifest` screen fields,
- public profile metadata,
- new theme packs,
- typography role tokens,
- utility classes for spacing, layout, or text alignment.
