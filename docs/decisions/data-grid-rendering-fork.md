# DESIGN — data_grid rendering fork

**Status:** accepted (issue [#261](https://github.com/lbliii/chirp-ui/issues/261))  
**Epic:** Premium Polish Phase D / Saga 3 data grid  
**Related:** [../patterns/data-grid.md](../patterns/data-grid.md)

---

## Problem

`data_grid` v1 renders a real `<table>` — correct default for server-driven,
accessible, no-JS sort/selection. That substrate makes **column resize** and
**row virtualization** impractical at log/market scale (Railway dashboard, lucky_cat
logs).

Prior art (Railway, lucky_cat) uses **div + CSS grid + ARIA grid roles**, inline
`grid-template-columns` from per-column width state, and a dedicated resize handle.

---

## Decision

Ship **two render modes**, not one compromised table:

| Mode | Macro flag | Substrate | When to use |
|---|---|---|---|
| **Table (default)** | *(none)* | Real `<table>`, `<thead>`, `<th scope="col">` | Server-driven CRUD lists, moderate row counts, sort + page-scoped selection |
| **ARIA grid (opt-in)** | `render_mode="aria_grid"` *(future)* | `role="grid"` over `display:grid` rows | Resize handles, virtualization, dense log/market feeds |

**Default stays `<table>`.** The ARIA-grid variant is a **follow-up implementation**
tracked separately; this decision unblocks the `Column` width contract and docs.

Do **not** bolt resize handles onto `<table>` — fighting table layout and
`<colgroup>` mobile behavior creates a hybrid that satisfies neither accessibility
story nor Railway-scale ergonomics.

---

## Column width contract (shipped now)

Extend :class:`~chirp_ui.grid_state.Column` with optional layout hints consumed
by the future ARIA-grid renderer and documented for callers today:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `width` | `str \| None` | `None` | Desktop/default column width (CSS length, e.g. `"120px"`, `"1fr"`, `"minmax(120px, 1fr)"`) |
| `mobile_width` | `str \| None` | `None` | Narrow-viewport override (separate per column — Railway pattern) |
| `resizable` | `bool` | `False` | Column participates in drag-resize in ARIA-grid mode |

Table mode **ignores** these fields today (no false promise). Sort/selection
projection (`sort_columns`, `ColumnSort`) is unchanged.

---

## ARIA-grid variant (future — not in this commit)

When implemented:

- Root: `role="grid"`, rows `role="row"`, headers `role="columnheader"`, cells
  `role="gridcell"`.
- Width state pushed to inline `grid-template-columns` on the rowgroup.
- Resize handle: `[data-column-resize-handle]` on resizable headers (pointer +
  keyboard — co-schedule with #198 split-panel parity).
- Virtualization: optional `data-item-index` + windowed row rendering; server
  still owns sort/filter; client only virtualizes **rendered** rows.

Proof: extend `tests/browser/test_data_grid_gauntlet.py` with an ARIA-grid
fixture before marking stable.

---

## Non-decisions

- Cross-page "select all N matching" — still out of scope (page-scoped selection).
- Per-column sticky/`frozen` — still first-column-only via `sticky_first_col`.
- Client-side sort engine — still rejected; server owns sort state.

---

## Related

- [#231](https://github.com/lbliii/chirp-ui/issues/231) — load-more refresh
- [#198](https://github.com/lbliii/chirp-ui/issues/198) — resize handle a11y parity
- `docs/plans/PLAN-premium-polish-saga.md` — Phase D proof loop
