# Screen: Review Queue

Status: golden screen fixture
Profile: `sage`
Fixture route: `/screen-review-queue`
Source template: `examples/component-showcase/templates/showcase/support_shell.html`
Proof: `tests/test_data_integration.py`,
`tests/browser/test_golden_screen_fixtures.py`

## Use When

Use Review Queue when a product needs focused triage or review work with:

- a queue/filter rail,
- a searchable result collection,
- state-rich result cards,
- selected-object inspection,
- compact metrics,
- batch-ready action regions.

Good fits include support triage, moderation queues, approval workflows,
document review, issue intake, internal inboxes, and search results with a
selected detail panel.

## Do Not Use When

Do not use this screen for dashboards where metrics are the primary object,
marketing/product pages, or single-object detail pages. Use Command Center,
Product/Docs Home, or Resource Detail patterns instead.

## Composition Map

| Job | Current Surface |
|---|---|
| Profile | `sage` token mood through screen metadata. |
| Shell | `workspace_shell` owns sidebar, content, and inspector placement. |
| Command surface | `command_bar`, search form, hint actions, HTMX update boundary. |
| Filters | `filter_bar`, queue selector, state selector, reset action. |
| Queue rail | `filter_rail` and `filter_rail_item`. |
| Main readout | `panel`, `metric_strip`, `metric_item`. |
| Results | `result_collection`, `result_card`, `badge`, `chip_group`. |
| Inspector | `inspector_panel`, selected ticket metadata, timeline list. |
| Empty state | `empty_state` when filters remove all tickets. |

## Data Shape

The fixture expects ticket/review records with:

- `id`, `customer`, `subject`, `queue`, `status`, `owner`,
- plan or tier,
- score, age, and summary,
- tags,
- timeline events.

Use realistic review data: long subjects, mixed priority, stale/escalated
states, and enough metadata to prove the inspector is not decorative.

## Required States

- Ready item.
- Needs-reply item.
- Escalated item.
- Filtered result collection.
- Selected ticket inspector.
- Empty result state through filters/search.
- Pending indicator during HTMX updates.

## Agent Guidance

When the user asks for moderation, approvals, inbox triage, support queues,
review workflows, or search results with selected detail, start from this
screen before assembling cards manually.

Prefer this screen over Command Center when the primary work is deciding what
happens to individual records.

Use the `sage` profile unless the screen needs urgent incident/automation
energy. If it does, record the need for the future `signal` profile instead of
changing this screen's local CSS.

Do not create page-local grid wrappers for the rail/content/inspector layout.
This fixture intentionally uses `workspace_shell`, `filter_rail`,
`result_collection`, and `inspector_panel` as the semantic path.

## Proof Checklist

- Server route renders and exposes `data-screen-archetype="review-queue"`.
- Fixture route preserves form and HTMX actions under `/screen-review-queue`.
- Browser proof covers 320, 390, 768, and 1280 widths with no document
  horizontal overflow.
- Browser proof verifies `workspace_shell`, `filter_rail`,
  `result_collection`, `result_card`, and `inspector_panel` are present.
- Existing support-shell route remains available for baseline comparison.

## Extraction Candidates

Track, but do not promote yet:

- `object_inspector`
- `review_queue_shell`
- `metadata_bar`
- `state_stack`

These need at least one more independent review/triage screen before public API
work.
