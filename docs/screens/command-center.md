# Screen: Command Center

Status: golden screen fixture
Profile: `atlas`
Fixture route: `/screen-command-center`
Source template: `examples/component-showcase/templates/showcase/operations_shell.html`
Proof: `tests/test_data_integration.py`,
`tests/browser/test_golden_screen_fixtures.py`

## Use When

Use Command Center when an application needs an operational overview with:

- high-signal metrics,
- workload or queue cards,
- incident/watch/healthy states,
- recent activity or event summaries,
- selected-object inspection,
- command search and filters.

Good fits include admin consoles, infrastructure dashboards, platform
operations, release control rooms, background-job monitors, and reliability
workspaces.

## Do Not Use When

Do not use this screen for editorial product pages, low-density onboarding,
marketing-first pages, or simple settings forms. Those need a product/docs home,
onboarding flow, or settings surface instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `atlas` token mood through screen metadata. |
| Shell and command surface | `command_bar`, search form, hint actions, HTMX update boundary. |
| Scope and filtering | `filter_bar`, dense fields, reset action. |
| Layout frame | `frame(variant="sidebar-start")` plus page-owned proof CSS until a stronger shell contract is proven. |
| Area rail | Rail links with `data-chirpui-role`, pressure, and affinity attributes. |
| Metrics | Badges and compact metric readout. |
| Workload cards | `card`, `badge`, `chip_group`, footer actions. |
| Inspector | Selected workload card with description metadata and event list. |
| Empty state | `empty_state` when filters remove all workloads. |

## Data Shape

The fixture expects workload records with:

- `id`, `name`, `area`, `status`, `owner`, `region`, `tier`,
- latency and error-rate values,
- deploy/version metadata,
- summary text,
- tags,
- recent events.

Use realistic long labels and mixed states. A command center that only contains
short placeholder cards does not prove the taste floor.

## Required States

- Healthy workload.
- Watch workload.
- Incident workload.
- Filtered result list.
- Selected workload inspector.
- Empty result state through filters/search.
- Pending indicator during HTMX updates.

## Agent Guidance

When the user asks for an operational dashboard, admin console, platform
overview, reliability room, queue monitor, or executive/operator control
surface, start from this screen before assembling individual components.

Prefer this screen over a generic `grid()` of `card()` elements when the page
needs live state, operational metadata, filters, and a selected-object region.

Use the `atlas` profile unless the user explicitly asks for a lower-glare
review/planning workspace.

Do not invent utility classes for spacing, width, typography, or alignment. If
the fixture needs local CSS to express a repeated semantic relationship, record
that as an extraction candidate in the taste-floor plan.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="command-center"`.
- Fixture route preserves form and HTMX actions under `/screen-command-center`.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow.
- Inspector remains visible at desktop width.
- Existing operations-shell route remains available for baseline comparison.

## Extraction Candidates

Track, but do not promote yet:

- `screen_header`
- `metadata_bar`
- `workspace_summary`
- `object_inspector`

These need repeated evidence from additional screens before public API work.
