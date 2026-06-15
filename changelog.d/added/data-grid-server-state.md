Added **`data_grid`** — a server-driven interactive data grid composite
(`chirpui/data_grid.html`) backed by a new typed Python state helper
**`chirp_ui.grid_state`** (Chirp-agnostic, stdlib + dataclasses, in the
`route_tabs.py` mold). The helper exposes `Column`, `GridSort`, `ColumnSort`,
`SelectionState`, and the plain functions `parse_sort`, `sort_columns`,
`selection_state`, `column_aria_sort`, `sort_query` (exported from
`chirp_ui.__all__` and registered as Kida template globals).

`sort_columns(...)` projects each column into a `ColumnSort` carrying the
`aria_sort` value and the fully-built toggle `next_url` the macro renders **but
never computes**, so the server's `ORDER BY` and the rendered headers cannot
drift. The grid ships sortable columns (real `<button class="chirpui-table__sort">`
in a `<th aria-sort=…>`, single-sort invariant, stable sort key — never
`header|lower`, focus retained on the activated button after the swap), row
selection bound to a controlled `selection_bar` via one idempotent
`chirpuiGridSelection` Alpine factory (page-scoped select-all with the
JS-property `indeterminate` state, live `aria-live` count, server-seeded so it is
correct with JavaScript off). The factory re-seeds from server-checked rows after
**every** swap — including the load-more `beforeend` append, via a scoped
`htmx:afterSettle` listener registered in `init()` — so select-all then load-more
correctly drops select-all to *indeterminate* (only the original page is selected
of the now-larger set) and a server-checked appended row is re-adopted (WCAG
4.1.2). Each row checkbox's accessible name comes from an optional `row_labels`
list (clean plain text) and **never** the rendered first cell (which may be rich
HTML or an empty spacer) — it falls back to the stable row id, so every label
stays distinct and screen-reader-clean. Sticky header + opt-in sticky first
column are pure `position: sticky` with token-driven z-index (incl. a top-left
corner override) and a directional **seam shadow** (`color-mix` over
`--chirpui-border`) so scrolled content visibly slides under the pin. v1 pins the
first **visual** column (no per-column `Column(frozen=…)` — deliberately not
shipped rather than advertise a no-op). HTMX load-more uses the `data_grid_rows`
fragment (`beforeend`). The previously-orphaned `.chirpui-table__sort` CSS hook is
finally emitted. `table()` gained additive
`selectable` / `select_name` / `selection` / `row_id` / `sticky_first_col`
params (defaults off = byte-identical; the legacy `sortable=`/`sort_url=`
`header|lower` path is unchanged and documented as legacy). `selection_bar()`
gained an additive `controlled=` mode. Proven by `tests/test_grid_state.py`,
`tests/test_components.py`, `tests/js/grid_selection.test.js`, and the
`tests/browser/test_data_grid_gauntlet.py` a11y gauntlet (single-active
aria-sort, focusable sort button, focus retention, three-state select-all,
sticky pinning, load-more without duplicate ids, axe-clean). Differentiator vs
TanStack: Python/HTMX-native — the server owns the sort and selection state;
load-more replaces client virtualization. Cross-page "select all N matching" is
out of scope for v1. See `docs/patterns/data-grid.md` and
`docs/COMPONENT-OPTIONS.md § Data Grid`
([#200](https://github.com/lbliii/chirp-ui/issues/200)).
