# Workspace Shell Recipes

Status: experimental, agent-facing

Use these recipes when a page is a dense app workspace rather than a marketing
page or simple document view. The goal is to let an agentic developer assemble
the right shell, rails, results, metrics, and inspector without inventing
page-local layout CSS.

## Search Workspace

Use for catalog search, docs search, resource browsers, and inventory pages.

- Outer shell: `workspace_shell`
- Commands: `command_bar`
- Filters: `filter_bar`
- Navigation: `filter_rail` / `filter_rail_item`
- Results: `result_collection` / `result_card`
- Readouts: `metric_strip` / `metric_item`
- Empty state: `empty_state`

Expected behavior:

- Search uses `data-chirpui-role="search"` with `pressure="flex"` and
  `affinity="fill"`.
- Hints use `role="hints"` and wrap before causing page overflow.
- Result cards keep actions compact and metadata in the footer.
- Rails and result grids must not force horizontal scrolling at phone widths.

## Operations Workspace

Use for workloads, deployments, queues, regions, and health consoles.

- Outer shell: `workspace_shell(show_inspector=true)`
- Sidebar slot: `filter_rail`
- Main slot: `metric_strip` followed by `result_collection`
- Inspector slot: `inspector_panel`

Expected behavior:

- The selected workload appears in the inspector, not as a second page-owned
  card layout.
- Metrics use compact readouts instead of badge-only count rows when the values
  are operational measures.
- Workload cards expose status through a slot action and keep owner/region/tier
  in the footer.

## Support Queue

Use for tickets, customers, escalations, priority queues, and triage surfaces.

- Outer shell: `workspace_shell(show_inspector=true)`
- Queue rail: `filter_rail`
- Ticket collection: `result_collection`
- Ticket summary: `result_card`
- Selected ticket: `inspector_panel`

Expected behavior:

- Queue and status controls live in `filter_bar`.
- The inspector summarizes the selected ticket and timeline.
- Action buttons stay in compact command/action regions, not inside arbitrary
  wrappers.

## Admin Workspace

Use for settings, permissions, policy, environment, and governance consoles.

- Outer shell: `workspace_shell`
- Group navigation: `filter_rail`
- Object list: `result_collection`
- Object card: `result_card`
- Selected object details: `inspector_panel` when a side panel is useful.

Expected behavior:

- Prefer `result_card` for repeated settings objects.
- Prefer `metric_strip` only when the metrics are meaningful operational
  readouts.
- Do not add new page-owned rail/grid/inspector classes until a primitive gap is
  identified.

## HTMX Boundary

The shell should have one stable surface id and one stable frame id:

```html
<div id="workspace-surface">
  {% call command_bar(...) %}
    <form hx-target="#workspace-frame" hx-select="#workspace-frame">...</form>
  {% end %}

  <section id="workspace-frame" aria-live="polite">
    {% call workspace_shell(...) %}...{% end %}
  </section>
</div>
```

Use `hx-sync` on the frame or surface for reactive search so rapid input does
not race older responses into view.

## Agent Checklist

- Start with `workspace_shell` for multi-region app workspaces.
- Use `filter_rail` for sidebar navigation or filters.
- Use `result_collection` and `result_card` for dense search results.
- Use `metric_strip` for count/status readouts that need stable wrapping.
- Use `inspector_panel` for selected-object details.
- Keep app-local classes for domain copy and data styling only.
- Verify phone, tablet, and desktop widths before calling the shell done.
