# Server-Driven Data Grid

ChirpUI's data grid is **server-driven**: Python owns the sort and selection
state, the macro renders what the server computed, and HTMX moves rows. There is
no client-side sort engine and no virtualization — load-more fetches the next
page from the server. This is the deliberate inverse of a client grid like
TanStack: the source of truth lives where the Python developer already is, and
the test suite, `ty`, and a coding agent can all reason about it.

See also:

- [COMPONENT-OPTIONS.md § Data Grid](../COMPONENT-OPTIONS.md)
- [UI-LAYERS.md](../fundamentals/ui-layers.md)
- [HTMX-PATTERNS.md](../HTMX-PATTERNS.md)

## The typed state helper: `chirp_ui.grid_state`

`data_grid` renders from a small, Chirp-agnostic Python module modeled on
`route_tabs.py` (stdlib + dataclasses, no `import chirp`, no `import kida`). It
is unit-testable with plain pytest and fully `ty`-checkable without a render.

```python
from chirp_ui import Column, GridSort, parse_sort, sort_columns, selection_state
```

| Symbol | What it is |
|--------|------------|
| `Column(key, label, sortable=False, align="")` | A column declaration. `key` is the **stable** sort key sent to the server — never `label\|lower`, so renaming a label or shipping i18n/duplicate labels never breaks sorting. Optional `width`, `mobile_width`, and `resizable` seed the future ARIA-grid renderer (#261); table mode ignores them today. (No per-column `frozen`: v1 pins the **first visual column** via `sticky_first_col=true`, not an arbitrary column — see Sticky zones.) |
| `GridSort(key="", direction="asc")` | The typed current-sort state. |
| `ColumnSort` | A projected column ready to render: carries `aria_sort` (`ascending`/`descending`/`none`), `is_active`, and the fully-built toggle `next_url`. |
| `SelectionState` | A page-scoped selection snapshot: `count`, `all_selected`, `none_selected`, `partial`, `is_selected(id)`. |
| `parse_sort(raw, *, default_key, default_direction, allowed)` | Turns `?sort=name` / `?sort=-name` into a `GridSort`. Unknown/empty keys clamp to the default (the `tab_is_active` empty-href guard analog). |
| `sort_columns(columns, sort, base_url, *, param, extra_params)` | Projects columns into `ColumnSort` rows. Exactly one column is active per `GridSort`, so the single `aria-sort` invariant is **structural**, not a template branch. `extra_params` (e.g. an active filter query) survive in every `next_url`. |
| `selection_state(selected_ids, page_ids, total)` | Normalizes request ids into a `SelectionState`. |
| `column_aria_sort(key, sort)` / `sort_query(key, sort, param)` | Standalone projection primitives for callers who hand-render a single `<th>`. |

The thesis-critical property: the **same** `GridSort` the route uses to actually
order rows also produces the rendered `aria-sort` and the next-request URL. The
macro reads `col.aria_sort` and `col.next_url` directly and computes nothing, so
the advertised UI and the server data cannot drift.

## Route + template

```python
from chirp_ui import Column, parse_sort, sort_columns, selection_state

COLS = [
    Column("name", "Name", sortable=True),
    Column("status", "Status", sortable=True, align="center"),
    Column("seats", "Seats", sortable=True, align="right"),
]

@app.get("/users")
def users(req):
    sort = parse_sort(req.query.get("sort"), default_key="name",
                      allowed=tuple(c.key for c in COLS))
    rows = query_users(order_by=sort.key, desc=(sort.direction == "desc"))  # Python owns the sort
    cols = sort_columns(COLS, sort, base_url="/users",
                        extra_params={"q": req.query.get("q", "")})
    sel = selection_state(req.query.getlist("ids"),
                          page_ids=[u.id for u in rows], total=count_users())
    ctx = dict(columns=cols, rows=[[u.name, u.status, u.seats] for u in rows],
               row_ids=[u.id for u in rows], row_labels=[u.name for u in rows],
               selection=sel)
    if req.headers.get("HX-Target") == "users-grid-body":
        return Response(render_fragment("data_grid_rows", **ctx))  # load-more append
    return Template("users.html", **ctx)
```

```html
{% from "chirpui/data_grid.html" import data_grid %}
{% call data_grid(title="Users", columns=columns, rows=rows, row_ids=row_ids,
                  row_labels=row_labels, sort_url="/users", hx_target="#users-grid",
                  selection_id="users", selectable=true, sticky_first_col=true,
                  selection=selection, load_more_url="/users", has_more=has_more) %}
  {{ btn("Export", hx={"post": "/users/export", "include": "#users-grid"}) }}
{% end %}
```

## Sorting

- Each sortable header is a real `<button class="chirpui-table__sort">` inside a
  `<th scope="col" aria-sort=…>`. The **button** is the click target
  (keyboard-focusable, native Enter/Space) — not the bare `<th>`.
- The direction caret is CSS-only via `aria-sort` attribute selectors and is
  `aria-hidden`, so the screen reader announces sort state once, via `aria-sort`.
- A sort click issues `hx-get="{col.next_url}"` with `hx-swap="outerHTML"` and
  re-renders the whole grid (resets to page 1 / the first cursor). Each sort
  button has a stable id (`{selection_id}-sort-{col.key}`) so focus is retained
  on the activated control after the swap.

## Selection

- `selectable=true` prepends a select column. The header select-all is
  **page-scoped** (it selects the visible page, not the entire result set —
  documented, not over-promised) with the three states unchecked / checked /
  indeterminate. `indeterminate` is set only via the JS DOM property
  (`x-effect="$el.indeterminate = someSelected"`), never an HTML attribute.
- Each row checkbox's accessible name comes from `row_labels` (optional, parallel
  to `row_ids`) — a clean, plain-text name per row. The label is **never** derived
  from the rendered first cell (which is frequently rich HTML — avatar + link +
  badge — or an empty spacer cell); when no `row_labels` entry is given, the label
  falls back to the stable row id, so every checkbox stays distinct and
  screen-reader-clean.
- The server seeds checked/indeterminate from `SelectionState`, so selection is
  correct on a full load with JavaScript off. One idempotent
  `chirpuiGridSelection` Alpine factory owns live in-page toggling between
  requests. It re-seeds from server-checked rows after **every** swap: the sort
  swap (`outerHTML`) re-inits the component, and the load-more append
  (`beforeend`, which keeps the `x-data` root alive) is re-scanned via a scoped
  `htmx:afterSettle` listener the factory registers in `init()` — so a
  select-all then load-more correctly drops select-all to *indeterminate* (only
  the original page is selected of the now-larger set) and any server-checked
  appended row is re-adopted into the selection.
- Selection feeds a controlled `selection_bar` (always in the DOM,
  `x-show`/`x-text`) whose count lives in an `aria-live="polite"` region — it
  updates without a server roundtrip and without stealing focus. Bulk-action
  buttons in the `data_grid` default slot forward into the bar and submit the
  selected ids only when an action fires (`hx-include="#{selection_id}-grid"`).

## Sticky zones

Both sticky zones are pure CSS `position: sticky` on the real `<thead>`/cells —
never a cloned/`aria-hidden`/fixed header (which would duplicate headers for
screen readers and break `<th scope>` association). `sticky_first_col=true` pins
the **first visual column** (the select-checkbox column when `selectable=true`,
otherwise the first data column) with a solid background; z-index is token-driven
(`--chirpui-z-sticky-col` < `--chirpui-z-sticky` < `--chirpui-z-sticky-corner`)
so the top-left corner cell stacks above both zones. Per-column pinning of an
arbitrary labeled column is **out of scope for v1** (no `Column(frozen=…)`).

Each pinned zone carries a directional **seam shadow** (a bottom shadow under the
sticky header, an inline-end shadow on the pinned column) so scrolled content
visibly slides *under* the pin instead of blending into it — the shadow is
derived from `--chirpui-border` via `color-mix`, so it tracks the theme with no
new color token.

## Load-more vs pagination

- Pass `load_more_url` + `has_more=true` for an HTMX load-more `<button>` that
  appends the next page (`data_grid_rows` fragment, `hx-swap="beforeend"`).
- Or pass `total` + `url_pattern` for classic paged navigation.

The consumer's load-more route must advance the cursor/offset **and preserve the
active sort** in the next URL — ChirpUI renders only the rows and the refreshed
sentinel.

## `data_table` vs `data_grid` decision lens

| Use `data_table` | Use `data_grid` |
|------------------|-----------------|
| A thin, read-mostly listing: filter form + table + pagination. | An interactive grid: sortable columns, row selection, sticky first column, load-more. |
| No per-column sort state, no selection. | Server sort state (`grid_state`), selection bound to a selection bar. |
| `maturity = experimental` (deliberately thin). | `maturity = experimental` (earns stable after the gauntlet stabilizes). |

## Out of scope for v1

Cross-page "select all N matching" is **not** solved — selection is page-scoped
client state, re-seeded server-side from the preserved ids on full reload. A
server-side "select all matching query" affordance is a noted follow-up.

## Rendering fork (table default vs ARIA grid)

See [../decisions/data-grid-rendering-fork.md](../decisions/data-grid-rendering-fork.md).

| Mode | Substrate | When |
|---|---|---|
| **Table (default)** | Real `<table>` | Server-driven lists, sort + page-scoped selection, moderate row counts |
| **ARIA grid (future)** | `role="grid"` over CSS grid | Column resize, virtualization, dense log/market feeds |

`Column.width`, `Column.mobile_width`, and `Column.resizable` document the
width contract for the ARIA-grid variant. Do not bolt resize handles onto the
`<table>` default — the fork exists so each mode stays honest.
