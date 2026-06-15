Made the registry `maturity` field honest about thin composition wrappers. A
`maturity="stable"` component that composes other registry components (non-empty
`composes`) is now treated as a composition wrapper and must carry the same
promote-to-stable proof collateral as any stable promotion — either a
`| Promote to stable |` row in `docs/safety/public-surface-stabilization.md` or a
justified `STABLE_COMPOSERS_WITH_PROOF` allowlist entry naming its asserting
proof test. The new `test_no_thin_composition_wrapper_is_stable_without_proof`
(composing with the existing promote-to-stable-collateral invariant, no new
maturity tier) catches the class: `data_table` shipped `stable` with
`composes=("filter-row","table","pagination")` before #200 demoted it, and this
gate would flag any future repeat. The audit confirmed zero current offenders —
`data_table` is already `experimental`, and `table`/`table-wrap`/`calendar`/
`bar_chart`/`donut` plus the hardened ASCII set carry `composes=()` so the rule
provably never fires on those complete/low-feature primitives
([#203](https://github.com/lbliii/chirp-ui/issues/203)).
