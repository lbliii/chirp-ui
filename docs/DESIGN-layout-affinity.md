# DESIGN: Layout Affinity

Status: proposed recipe-first contract
Date: 2026-05-21
Plan: [PLAN-layout-affinity-rollout.md](plans/PLAN-layout-affinity-rollout.md)
Resolver authoring: [LAYOUT-AFFINITY-RESOLVER-AUTHORING.md](LAYOUT-AFFINITY-RESOLVER-AUTHORING.md)

## Status Block

- Prototype recipe attributes.
- Not yet descriptor API.
- Not yet manifest contract.
- Allowed only where documented parent resolvers consume them.

Layout affinity is a machine-readable layout-intent contract for Chirp UI
components and recipes. Components can describe what job they perform, how they
behave under space pressure, and where they naturally belong. Parent primitives
can then resolve those signals into wrapping, stretching, alignment, and
overflow behavior without app-local utility classes.

The internal metaphor is magnetic or polarized components. The public language
is intentionally boring: role, pressure, and affinity.

## Problem

Dense interfaces often need the same judgments again and again:

- Search controls should take available width.
- Suggested searches should wrap before the page scrolls.
- Status indicators should stay compact.
- Actions should prefer the inline end on wide screens.
- Rails and card headers should keep labels and counts from stretching each
  other into awkward shapes.

Humans can make these calls visually. Agentic developers need those calls to be
discoverable from contracts instead of inferred from screenshots or guessed with
one-off CSS.

## Decision

Start layout affinity as a recipe-level HTML/data-attribute contract:

```html
data-chirpui-role="search"
data-chirpui-pressure="flex"
data-chirpui-affinity="fill"
```

Known parent primitives, starting with `command_bar` / `action_strip`, may
resolve these attributes. The attributes are not a general utility-class
vocabulary and do not control raw margin, padding, width, or position values.

## Initial Vocabulary

`data-chirpui-role` describes the element's job:

- `search`
- `actions`
- `filters`
- `hints`
- `status`
- `metadata`
- `nav`
- `content`
- `aside`
- `rail`

`data-chirpui-pressure` describes how the element behaves as space changes:

- `rigid`: keep intrinsic size
- `flex`: take available room
- `compress`: wrap or shrink before forcing overflow
- `overflow`: may scroll or truncate when the parent explicitly allows it
- `isolate`: avoid inherited stretching or placement pressure

`data-chirpui-affinity` describes natural placement:

- `start`
- `end`
- `center`
- `fill`
- `block-start`
- `block-end`

Values are tokens, not CSS dimensions. A parent may ignore a value it does not
resolve.

## Authoring Vocabulary Contract

Agents and app authors may use only documented tokens. Do not coin values such
as `left`, `right`, `grow`, `shrink`, `positive`, `negative`, `primary`, or
pixel-like values. If a needed behavior does not fit the vocabulary, add a
prototype note here before using a new value in templates.

Prototype-supported values currently emitted in source templates:

| Attribute | Emitted values |
|---|---|
| `data-chirpui-role` | `actions`, `aside`, `content`, `filters`, `hints`, `metadata`, `nav`, `rail`, `search`, `status` |
| `data-chirpui-pressure` | `compress`, `flex`, `rigid` |
| `data-chirpui-affinity` | `block-end`, `block-start`, `end`, `fill`, `start` |

Reserved vocabulary is documented in **Initial Vocabulary**, but reserved
values should not appear in source templates until a resolver uses them and
tests prove the behavior. This keeps layout affinity from becoming a grab bag
of utility-style names.

## For Agents

Use the attribute only when a documented parent resolver owns the decision:

```html
<form data-chirpui-role="search" data-chirpui-pressure="flex" data-chirpui-affinity="fill">
<div data-chirpui-role="actions" data-chirpui-pressure="rigid" data-chirpui-affinity="end">
```

Do not use layout affinity as a styling escape hatch:

```html
<!-- Do not add undocumented values. -->
<div data-chirpui-pressure="grow" data-chirpui-affinity="left">
```

If the desired behavior needs a new value, add it to this RFC, add source-scan
tests, and prove a parent resolver before using it in examples.

## Resolver Model

Resolution is parent-scoped:

- `command_bar` resolves search, hints, actions, and status.
- `filter_bar` resolves search, filters, and actions.
- `card` resolves metadata, content, badges, and actions inside its scoped
  boundary.
- `frame` resolves rail, nav, and content overflow/min-width protection in
  structural shell recipes.
- `workspace_shell` resolves its owned sidebar, main content, toolbar, and
  inspector parts for workbench-style shells.
- `workspace_primitives` resolves its owned filter rails, result collections,
  result cards, metric strips, and inspector panels.
- `cluster` and `stack` are prototype-only experiments and are not
  manifest-promotion candidates yet.

No global CSS should try to make every component react to every other
component. Affinity only works when a parent primitive documents the resolver.
Maintainers adding resolver behavior must follow
[LAYOUT-AFFINITY-RESOLVER-AUTHORING.md](LAYOUT-AFFINITY-RESOLVER-AUTHORING.md)
so selector scope, tests, docs, and manifest boundaries move together.

## First Prototype

The first implementation is recipe-only:

- Catalog shell search form emits `role=search`, `pressure=flex`,
  `affinity=fill`.
- Catalog shell suggested searches emit `role=hints`, `pressure=compress`,
  `affinity=end`.
- Catalog shell pending status emits `role=status`, `pressure=rigid`.
- `command_bar` resolves those attributes while preserving fallback behavior
  for plain forms and hint groups.

This does not add public macro parameters or descriptor fields.

## Second Prototype

The second consumer is the component-showcase data page filter toolbar:

- The search zone emits `role=search`, `pressure=flex`, `affinity=fill`.
- The select-filter zone emits `role=filters`, `pressure=compress`.
- The export action zone emits `role=actions`, `pressure=rigid`,
  `affinity=end`.
- `filter_bar` resolves the same parent-scoped attributes as `command_bar`
  because it is also an `action_strip` composite.

This keeps the vocabulary unchanged across two surfaces: a bespoke catalog
search shell and a shipped data/filter toolbar primitive.

## Third Prototype

The third consumer is card header and metadata composition, which is not an
`action_strip` surface:

- Card header content emits `role=content`, `pressure=flex`, `affinity=fill`.
- Card header actions emit `role=actions`, `pressure=rigid`, `affinity=end`.
- Resource card badges, top metadata, and footer metadata emit
  `role=metadata`, `pressure=compress`, and block/start/end affinity where
  relevant.
- `card` resolves those attributes inside its own scoped CSS boundary so
  nested cards keep their own independent layout contract.

This is the first component-owned internal layout-affinity contract. It still
does not add public macro parameters or descriptor fields.

## Shell And Micro-Resolver Prototype

The fourth consumer is a layout primitive prototype:

- `frame` hosts a rail/content/nav shell with `role=rail`, `role=content`, and
  `role=nav`.
- `cluster` and `stack` currently demonstrate copyable markup pressure, but
  their generic resolver behavior is explicitly not promoted because it risks
  becoming utility classes in attribute form.

This proves the vocabulary can describe page regions and small inline groups
without adding layout utility classes, while keeping low-level primitives
outside the manifest promotion set until a narrower boundary is accepted.

## Workspace Shell Resolver

The first repeated inspector/workspace resolver owner is the existing
`workspace_shell` component. It emits component-owned layout-affinity parts for
its heading, toolbar, sidebar, main content, and inspector. The support queue
payoff page now uses `workspace_shell` to own the rail/content/inspector
placement that was previously app-local CSS.

This is an inspector/workspace resolver, not a generic x/y positioning system:
the component decides its own internal parts, and apps still provide semantic
slot content.

## Payoff Experiment

The operations workspace shell is the first deliberate larger-payoff test. It
combines command search, filter controls, a frame rail, dense workload cards,
and a right inspector panel without adding a new public resolver. Its job is to
measure what current `command_bar`, `filter_bar`, `card`, and `frame`
resolvers can carry before a new primitive is justified.

The support queue shell is the second payoff test. It repeats the same
command/filter/rail/card/inspector shape in a different customer-operations
domain with different data, labels, states, and actions. It then dogfoods
`workspace_shell` so the repeated inspector/workspace shape is component-owned
instead of page-owned CSS, but it still does not promote descriptor, manifest,
or macro API surface.

Known gap: the operations shell remains the baseline page-owned version. That
lets us compare how much boilerplate `workspace_shell` removes before promoting
any descriptor or manifest projection.

## Boilerplate Comparison

The support shell is now the first `workspace_shell` proof, while the operations
shell intentionally remains the page-owned baseline. A second operations route
uses the same operations data through `workspace_shell`, so the comparison can
separate domain differences from structural ownership.

Measured on the shell body and example-local CSS after the support migration:

| Surface | Structural owner | Shell template structural lines | Example CSS structural selector lines |
|---|---|---:|---:|
| Operations shell | page-owned `frame` + page grid | 13 | 37 |
| Operations shell workspace variant | `workspace_shell` with same operations data | 8 | shared with baseline |
| Support shell | `workspace_shell` | 8 | 26 |

The reduction is not the main value by itself. The important change is contract
ownership: sidebar/content/inspector placement moved from page CSS into
`workspace_shell`, while page CSS now only owns product-specific rail links,
cards, ticket measures, and copy density.

Decision: keep `/operations-shell` as the baseline route and use
`/operations-shell-workspace` as the direct migration candidate. Do not delete
the baseline yet. The same-data side-by-side route makes the payoff measurable
and keeps us honest about whether `workspace_shell` solves the advanced-shell
problem generally or only for the support page.

## Dense Workspace Primitives

The first promoted inner primitives are intentionally narrow:

- `filter_rail` and `filter_rail_item` for sidebar navigation/filter rails.
- `metric_strip` and `metric_item` for compact readouts that wrap predictably.
- `result_collection` and `result_card` for dense searchable result surfaces.
- `inspector_panel` for selected-object side panels.

These primitives do not add a general positioning solver. They encode the
repeated shapes that catalog, support, and operations workspaces were already
hand-authoring, then emit the same layout-affinity attributes inside a
registry-cited component surface. The `/operations-shell-workspace` route is
the first migration target because it shares data with the page-owned baseline.

The source vocabulary is now importable from `chirp_ui.layout_affinity`. That
module is a contract helper for tests and agents, not a manifest schema
projection. Manifest fields remain deferred until the resolver names and
vocabulary survive more migrations.

## Agent Contract

The future agent-facing contract should answer:

- Where does this component naturally belong?
- Does it stretch, wrap, stay compact, or isolate?
- Which parent primitives resolve its intent?
- What happens at phone, tablet, and desktop widths?
- What should an agent avoid wrapping in app-local classes?

Eventually, descriptor and manifest metadata may project layout intent. That is
deferred until the recipe-level contract proves stable across multiple real
surfaces.

## Descriptor And Manifest Readiness

The three proven consumers give us enough evidence to design the projection,
but not enough to ship it in `chirpui-manifest@5`. Actual descriptor fields and
manifest keys remain deferred because they are public schema changes.

Recommended future manifest shape for parent resolvers:

```json
{
  "layout_resolver": {
    "scope": "direct-children",
    "roles": ["search", "filters", "hints", "actions", "status"],
    "pressures": ["flex", "compress", "rigid"],
    "affinities": ["fill", "end"],
    "notes": "Resolved by command_bar/filter_bar action-strip chrome."
  }
}
```

Recommended future manifest shape for component-owned internal parts:

```json
{
  "layout_parts": [
    {
      "part": "header-content",
      "role": "content",
      "pressure": "flex",
      "affinity": "fill"
    },
    {
      "part": "header-actions",
      "role": "actions",
      "pressure": "rigid",
      "affinity": "end"
    }
  ]
}
```

Recommended future descriptor fields should mirror those two shapes rather than
adding a single flat `layout_role` to every component:

```python
layout_resolver: LayoutResolver | None
layout_parts: tuple[LayoutPart, ...]
```

Adding these fields requires a manifest schema bump, generated
`manifest.json`, docs, examples, tests, changelog notes, and steward review.
Until then, `data-chirpui-role`, `data-chirpui-pressure`, and
`data-chirpui-affinity` are HTML/CSS contracts only.

Promotion gates for `chirpui-manifest@6`:

- Registry steward accepts descriptor field names and validation vocabulary.
- Template/CSS steward accepts resolver scoping rules and nested-component
  behavior.
- Docs/site steward accepts agent-facing examples that do not look like utility
  classes.
- Tests prove deterministic projection and no under-reported layout parts for
  `command_bar`, `filter_bar`, and `card`.
- Backward compatibility notes state that `chirpui-manifest@5` consumers should
  ignore the HTML attributes unless they inspect rendered templates directly.

## Non-Goals

- No utility classes.
- No numeric x/y positioning.
- No margin or padding shorthands.
- No JavaScript layout measurement.
- No global resolver that changes arbitrary descendants.
- No physics-themed public API names such as `charge`.
- No public macro params until repeated use proves the vocabulary.

## Rollout Gates

1. Recipe prototype in catalog shell with render and browser proof.
2. Second consumer in dense object chrome or resource index toolbar.
3. Third consumer in card/header composition or app shell command surface.
4. Descriptor and manifest RFC only after the resolver vocabulary survives
   those consumers unchanged.
5. Manifest schema bump only after steward review accepts the descriptor shape.
6. Public macro params only after descriptor projection has a concrete
   downstream consumer.

## Required Proof

- Render tests assert emitted recipe attributes.
- CSS tests assert parent-scoped resolver selectors.
- Browser tests assert no horizontal overflow and no overlap across stress
  phone, phone, tablet, and desktop widths.
- Docs distinguish recipe-level attributes from public macro API.
