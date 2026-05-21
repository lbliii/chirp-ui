# Search Shell Recipes

Status: recipe contract
Date: 2026-05-21

Search shells are dense, server-rendered workspaces for catalog, reference,
inventory, and object-library browsing. They combine a query control, suggested
queries, scoped facets, version or state filters, result metrics, and dense
result cards. Chirp UI keeps this recipe-first until repeated consumers prove
which pieces deserve public macros.

The component registry still owns shipped component APIs. This document owns
composition contracts for advanced HTMX and Alpine search surfaces built from
existing primitives.

## Contract Summary

- Native HTML remains the baseline. Search shells use GET forms and real links
  so the URL is shareable, refreshable, and usable without JavaScript.
- HTMX enhances the same URLs. Every enhanced control names the request URL,
  swap target, selected fragment, URL push behavior, request coordination, and
  pending indicator.
- Recipe-level layout affinity may be used to make command surfaces
  self-compose: search controls can declare `role=search`, `pressure=flex`,
  `affinity=fill`; suggested queries can declare `role=hints`,
  `pressure=compress`; pending indicators can declare `role=status`,
  `pressure=rigid`. See [DESIGN-layout-affinity.md](DESIGN-layout-affinity.md).
- Alpine is limited to local affordances such as setting the visible query
  value and toggling a pending class. Server state lives in the URL and rendered
  HTML.
- Counts are scoped to what the user can see or reach from the current filter.
  Labels use domain nouns such as `docs`, `docsets`, and `products`, not generic
  `records` unless the domain truly calls them records.
- Responsive behavior is part of the recipe. Command controls wrap, rails
  reflow, and result grids collapse before any page-level horizontal overflow.

## Progressive Enhancement

Each control needs a native path and an HTMX path that agree on state:

| Control | Native contract | HTMX contract |
|---|---|---|
| Search submit | `<form method="get" action="/search">` includes current facet and version hidden inputs. | `hx-get` uses the same route, targets the whole search surface, selects the surface, pushes the URL, and replaces stale requests. |
| Live search input | The input is named `q` and belongs to the form. | `hx-trigger="input changed delay:..."` targets only the result frame, includes query plus hidden state, selects the frame, pushes the URL, and replaces stale frame requests. |
| Suggested query | Real `href` contains the suggested query and preserved active filters. | `hx-get` uses the same href, targets/selects the surface, pushes the URL, and may use tiny Alpine to mirror the query into the input before the response arrives. |
| Facet rail item | Real `href` contains the selected facet and preserved compatible state. | `hx-get` targets/selects the surface and uses `hx-boost="false"` when inside boosted shells. |
| Reset | Real `href` clears the state the label promises to clear. | HTMX path targets/selects the surface and clears the local input affordance if needed. |

Do not branch only on `HX-Request`. A route that serves both full pages and
fragments should inspect `HX-Target` when response shape differs.

## Scoped Counts

Counts should answer the question implied by their location.

| Location | Count should mean | Avoid |
|---|---|---|
| Global result metrics | Items visible in the current query, facet, family, and version scope. | Mixing visible docs with all-time products. |
| Category rail | Matching docs reachable by selecting that category under the current query and version. | Static category totals that ignore an active query. |
| Family rail | Matching products and docs inside the selected category under current query and version. | Showing hidden families with stale totals unless the UI labels them as unavailable. |
| Result card badge | Matching docs on that card in the current scope. | Reusing total catalog doc counts. |

Use domain labels consistently. If the object is documentation, prefer `doc`;
if it is a package or product, prefer `product`; if it is an indexed content
source, prefer the source noun.

## Responsive Command Surface

Search shells are not allowed to depend on horizontal scrolling for primary
search controls. The command surface should follow these tiers:

| Tier | Behavior |
|---|---|
| Desktop | Search form and suggested queries can share one row. Hints wrap within the command surface instead of overflowing the page. |
| Tablet | Search form takes the first row; hints wrap below it. Rails may stay visible when the result workspace remains usable. |
| Phone | Search input and submit action stack or use full-width controls. Hints wrap into compact chips or move into a drawer/tray if there are too many. |
| Stress phone | The surface must still avoid page-level horizontal overflow at 320px. Long labels wrap or truncate inside stable control dimensions. |

Use `command_bar(wrap="wrap")` or an equivalent wrapping command surface for
search shells. `wrap="scroll"` is acceptable for secondary toolbars, not the
main search form.
`command_bar` and `filter_bar` own direct search, hint, and action rhythm:
visible search labels get a full row, trailing hints align with
`data-chirpui-affinity="end"` when space allows, and action-strip zones trim
direct child margins. Page CSS should style domain tone only, not rebuild
search-form columns or hint wrapping.

The canonical layout-affinity prototype contract lives in
[DESIGN-layout-affinity.md](DESIGN-layout-affinity.md). This search-shell guide
uses the attributes only where the command-surface resolver consumes them; it
does not redefine the vocabulary or promote descriptor/manifest fields.

When using the experimental layout-affinity prototype, mark command-surface
children with recipe attributes rather than app-local flex classes:

```html
<form data-chirpui-role="search" data-chirpui-pressure="flex" data-chirpui-affinity="fill">
<div data-chirpui-role="hints" data-chirpui-pressure="compress" data-chirpui-affinity="end">
<span data-chirpui-role="status" data-chirpui-pressure="rigid">
```

## Facet Rails

Facet rails are navigation, not just decoration:

- Rail headings use a stable number or icon plus a label, stacked when space is
  tight.
- Every item is a link with an `aria-label`, visible active state, and a count
  whose scope is documented by the recipe.
- Selecting a higher-level facet should preserve compatible state and drop
  incompatible lower-level state.
- Rails can reflow into horizontal strips or stacked panels on smaller screens,
  but active state and counts remain visible.

## Pending And Settling Feedback

Search shells should make reactive updates feel immediate without taking over
state ownership:

- Add one scoped pending indicator with `role="status"` and `aria-live="polite"`.
- Wire `hx-indicator` from search, hints, facets, and reset controls to that
  indicator.
- Use `hx-sync` so older live-search responses cannot overwrite newer intent.
- If Alpine toggles a pending class, clear it on `htmx:after-settle` and
  `htmx:response-error`.
- Respect reduced-motion preferences for settle animations.

## Dense Result Items

Dense result cards should have a repeatable anatomy:

- Product/source identity.
- Title link.
- Short summary.
- Scoped count badge.
- Coverage chips or topics.
- A small list of representative child links with docset/source labels.

Keep cards visually quiet. The result grid should support scanning and
comparison before it tries to look editorial.

## Proof Checklist

For a new search shell recipe or a material change to an existing one, run:

- Render tests for fallback URLs, hidden state fields, HTMX target/select/push
  attributes, scoped counts, and pending indicator wiring.
- Browser tests at 320px, 390px, 768px, 1024px, and desktop width for no
  document horizontal overflow, visible primary controls, and wrapped hints.
- At least one browser interaction that clicks a facet or suggested query and
  proves the URL, visible results, and target boundary update together.

Promotion to public macros requires a separate registry/API plan, descriptor
coverage, generated docs, CSS partial ownership, and migration guidance.
