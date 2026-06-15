Demoted the **`data-table`** descriptor from `stable` to `experimental`
(metadata-only; no render change). Per [#200](https://github.com/lbliii/chirp-ui/issues/200)'s
acceptance ("no longer a thin wrapper labeled stable"), `data_table` is the
deliberately-thin filter+table+pagination convenience wrapper and the new
`data_grid` composite is now the real interactive grid. `table` and `table-wrap`
remain `stable` — they are genuinely complete low-level primitives (real
`<table>` semantics, alignment, widths, sticky header/col, slots). Agents and
docs that read the manifest will see the new maturity value; it is intentional,
not a regression. See `docs/safety/public-surface-stabilization.md`.
