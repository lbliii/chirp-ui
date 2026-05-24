# Screen: Agent Run Monitor

Status: golden screen fixture
Profile: `signal` candidate
Fixture route: `/screen-agent-run-monitor`
Source template:
`examples/component-showcase/templates/showcase/screen_agent_run_monitor.html`
Proof: `tests/test_data_integration.py`,
`tests/browser/test_golden_screen_fixtures.py`

## Use When

Use Agent Run Monitor when a product needs to show live agent, automation, or
background-run state with:

- current progress,
- run health,
- timeline state,
- streaming output,
- artifact previews,
- retry/recovery actions,
- selected-step inspection.

Good fits include agent traces, automation runs, evaluation jobs, import/export
jobs, incident automation, and build/deploy monitors.

## Do Not Use When

Do not use this screen for generic dashboards where live execution is not the
main object, or for review queues where humans decide the next action record by
record. Use Command Center or Review Queue instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `signal` candidate metadata; no packaged theme pack yet. |
| Run summary | `panel`, `sse_status`, `badge`, `progress_bar`. |
| Metrics and controls | `metric_strip`, `metric_item`, `copy_btn`, `sse_retry`. |
| Timeline | `timeline(items=..., density="compact", variant="cards")`. |
| Selected step | `inspector_panel`, `description_list`, status badge. |
| Streaming output | `model_card`, `streaming_block`, stable output target. |
| Artifacts | `result_collection`, `result_card`, artifact status badges. |

## Data Shape

The fixture expects run records with:

- run id and title,
- trigger/owner metadata,
- current progress and step count,
- health state,
- timeline events,
- selected step metadata,
- streaming output text,
- artifact cards and handoff states.

Use real-ish state labels. Agent UIs look unfinished when they collapse to raw
logs, naked JSON, or generic cards without status ownership.

## Required States

- Running state.
- Connected stream state.
- Warning/watch state.
- Retry action.
- Streaming output target.
- Artifact ready state.
- Artifact pending state.

## Agent Guidance

When the user asks for an agent dashboard, run monitor, automation trace,
evaluation job, workflow execution screen, or deploy/build monitor, start from
this screen before building a generic log page.

Prefer this screen when the primary user question is "what is happening right
now and what can I do if it fails?"

Use `signal` as a candidate profile label, but do not assume a packaged
`signal.css` theme exists yet. If the visual direction needs distinct tokens,
record that as evidence for the profile-system epic.

Do not render logs as the whole interface. Logs belong beside state, timeline,
artifacts, and recovery actions.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="agent-run-monitor"`.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow.
- Browser proof verifies timeline, streaming block, result collection, and
  inspector panel surfaces are present.

## Extraction Candidates

Track, but do not promote yet:

- `status_timeline`
- `artifact_strip`
- `state_stack`
- `object_inspector`
- `signal` token profile

These need repeated run/automation/incident screens before public API work.
