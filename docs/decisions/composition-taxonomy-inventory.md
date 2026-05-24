# DESIGN: Composition Taxonomy Inventory

Status: active inventory
Date: 2026-05-23
Purpose: map existing Chirp UI surfaces to the visual taste-floor taxonomy
before building screen-catalog fixtures or promoting new public API.

## Decision

The visual taste floor should be executed through existing registry-owned
layers first. New components, public screen macros, theme-pack fields, or
manifest schema should appear only after the golden screens prove repeated
gaps.

The current system has enough surface area to start with recipes and fixtures:

- primitives own rhythm, layout, and relationship pressure;
- components own concrete UI objects;
- theme packs own token mood only;
- pattern docs already cover product, media, forum, search, workspace, dense
  navigation, visual audit, and app chrome recipes;
- the component showcase and static visual audit already provide proof
  infrastructure.

The missing layer is a curated screen catalog: complete product situations with
profile pairings, realistic data, responsive proof, and agent guidance.

## Taxonomy Inventory

| Layer | Existing Source | Ready To Use For Golden Screens | Gap |
|---|---|---:|---|
| Design doctrine | `docs/strategy/vision.md`, `docs/plans/PLAN-visual-taste-floor-saga.md` | Yes | Taste laws need validation through fixtures before becoming stable docs. |
| Tokens | `docs/fundamentals/tokens.md`, `docs/theming/app-theme.md`, `src/chirp_ui/templates/themes/` | Yes | Profiles need screen-specific intent, anti-use cases, and screenshot proof. |
| Visual grammar | `docs/fundamentals/relationship-contracts.md`, `docs/patterns/visual-audit-showcase.md`, `docs/plans/PLAN-application-chrome-system.md` | Partial | Rules are scattered; use golden screens to decide what belongs in a durable grammar doc. |
| Primitives | `docs/fundamentals/primitives.md`, `src/chirp_ui/templates/chirpui/layout.html` | Yes | Agents need mappings from product situations to primitive compositions. |
| Components | `src/chirp_ui/components.py`, `docs/COMPONENT-OPTIONS.md`, generated manifest | Yes | Component count is high, but screen-level selection guidance is thin. |
| Layout relationships | `docs/fundamentals/relationship-contracts.md`, `docs/decisions/layout-affinity.md`, `docs/patterns/layout-affinity-resolver-authoring.md` | Yes, recipe-first | Relationship vocabulary is not screen-catalog guidance yet. |
| Patterns | `docs/patterns/*.md`, `examples/component-showcase/templates/showcase/*` | Yes | Pattern docs do not yet converge into named screen archetypes. |
| Screens | Planned in `docs/plans/PLAN-visual-taste-floor-saga.md` | No | Need Command Center and Review Queue fixtures before public screen docs. |
| Shells | `docs/fundamentals/ui-layers.md`, `docs/components/shell-tabs-contract.md`, `docs/patterns/navigation.md`, app chrome plan | Yes, recipe-first | Need shell/screen boundaries in fixture guidance. |
| Flows | Wizard, tabs, route tabs, htmx fragments, upload/grid state examples | Partial | Multi-screen stateful flows are not taste-floor MVP. |
| Catalog | `docs/INDEX.md`, component options, source inventory, visual audit | Partial | Need `docs/screens/` only after first fixtures. |
| Agent guidance | `docs/agents/agent-source-inventory.md`, `docs/agents/agent-source-map.md`, `docs/agents/agent-curated-snippets.md` | Partial | Need "choose a screen first" rules after screen entries exist. |
| Proof fixtures | `examples/design-system-gap-showcase/index.html`, component showcase, browser tests | Yes | Need golden-screen-specific render/browser proof. |

## Existing Surfaces By Golden Screen

### Command Center

Use current surfaces:

- `app_shell`, `route_tabs`, `page_hero`, command and navigation patterns from
  application chrome guidance;
- `metric_grid`, `metric_card`, `status`/badge, `table`, `timeline`, `alert`,
  `callout`, `card`, `panel`, and `empty_state`;
- `atlas` profile for operational SaaS mood.

Likely gaps:

- A reusable `screen_header` or `workspace_summary` may emerge if dashboard
  header/context markup repeats.
- A `metadata_bar` may be needed if counts, owners, timestamps, and runtime
  provenance appear in every screen.
- Avoid promoting from the first screen alone.

Proof target:

- Dense dashboard remains organized at 1440, 1024, 768, 390, and 320 widths.
- Long queue labels and reserved/loading badges do not widen the document.

### Review Queue

Use current surfaces:

- `filter_rail`, `result_collection`, `result_card`, `inspector_panel`,
  `row_actions`, `button_group`, `segmented_control`, `badge`, `description_list`,
  `tabs`, and dense navigation recipes;
- `sage` profile for low-glare review/planning work.

Likely gaps:

- `object_inspector` may deserve promotion if selected-detail regions repeat
  across Review Queue, Resource Detail, and Project Workspace.
- `review_queue_shell` should remain recipe-only until at least two independent
  review/triage screens repeat the contract.

Proof target:

- Filter rail, result list, and inspector stack or collapse without horizontal
  overflow.
- Selected, stale, verified, failed, empty, and loading states are visible and
  not color-only.

### Agent Run Monitor

Use current surfaces:

- streaming blocks, SSE status, timeline, code/log blocks, copy buttons,
  progress, alert/callout, artifact/resource cards, tabs, retry controls;
- `signal` as a proposed profile, not yet a committed token pack.

Likely gaps:

- `status_timeline`, `artifact_strip`, and `state_stack` may emerge from
  repeated run/automation/incident screens.
- `signal` should not become a packaged theme pack until this screen proves the
  need for a distinct token mood.

Proof target:

- Logs, artifacts, retries, and failure context feel designed instead of
  terminal-dump adjacent.
- Loading/running/error/recovered states have stable layout.

### Product/Docs Home

Use current surfaces:

- `site_shell`, `site_header`, `hero`, `band`, `logo_cloud`, `feature_section`,
  `index_card`, `story_card`, `cta_band`, `tabs_panels`, and product-page
  pattern recipes;
- `ember` profile for product/docs/editorial mood.

Likely gaps:

- Product/docs first viewport may need stronger media/proof composition, but
  that should start as a recipe before a component.
- Avoid generic card-heavy landing pages; use product identity, proof, and
  docs entry points.

Proof target:

- First viewport signals product identity and proof without feeling like a
  wireframe.
- Phone width leaves a hint of the next section without overlapping content.

## Catalog Readiness

Do not create public `docs/screens/` entries until at least two source fixtures
exist. The first entries should be:

1. Command Center with `atlas`.
2. Review Queue with `sage`.

After those pass render and browser proof, create the screen-entry template and
agent guidance blocks. Agent guidance should be marked curated only after the
source inventory names the screen catalog as an eligible source.

## Extraction Ledger

Track these candidates while building fixtures:

| Candidate | Starting Status | Promote When |
|---|---|---|
| `screen_header` | Candidate | Three screens repeat the same title/context/actions/provenance contract. |
| `metadata_bar` | Candidate | Counts, owners, timestamps, and status metadata repeat across app and agent screens. |
| `object_inspector` | Candidate | Review Queue, Resource Detail, and Project Workspace need the same selected-object anatomy. |
| `status_timeline` | Candidate | Agent Run Monitor and incident/automation screens repeat state progression. |
| `artifact_strip` | Candidate | Agent, import, and build screens repeat artifact previews/actions. |
| `review_queue_shell` | Recipe-only | Two independent review/triage domains prove identical rail/list/inspector behavior. |
| `proof_band` | Recipe-only | Product/docs screens repeat the same proof anatomy beyond current `logo_cloud` and metrics. |

Every candidate must stay out of the public API until the root stop-and-ask
rules are satisfied.

## Next Slice

Build the first two golden-screen fixtures:

1. Command Center using existing operational/dashboard primitives and the
   `atlas` profile.
2. Review Queue using dense workspace primitives and the `sage` profile.

The first implementation pass should prefer existing component-showcase or
static visual-audit infrastructure and should log any local CSS workaround as a
future extraction candidate instead of normalizing it as app guidance.

## Proof

For this inventory:

- Source-backed docs only; no runtime behavior changes.
- Focused docs/path ratchets are sufficient.

For the next slice:

- render tests for fixture presence and required state markers;
- browser overflow proof at phone, tablet, and desktop widths;
- screenshot/manual review notes if visual comparison is not automated yet.
