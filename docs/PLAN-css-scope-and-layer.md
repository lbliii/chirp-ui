# EPIC — CSS as a projection of the Python registry

**Status:** proposal
**Drafted:** 2026-04-17
**Owner:** Lawrence Lane
**Category:** architecture (load-bearing for `docs/VISION.md § CSS architecture as a registry projection`)

## One-paragraph thesis

Modularize the monolithic `chirpui.css` into per-component partials authored
with `@layer` + `@scope` + native nesting, concatenated by a pure-Python build
step, and cross-checked against an enriched `ComponentDescriptor.emits` field
so the stylesheet becomes a *projection* of the Python registry rather than a
parallel source of truth. Consumers see no change: the `chirpui-*` BEM classes,
macro outputs, and `grep` behavior stay byte-identical. What changes is that
the registry, the CSS, the tests, and the agent manifest can no longer drift.

## Evidence

| # | Finding | Source |
|---|---------|--------|
| E1 | `chirpui.css` is 15 624 lines and 167 `/* =====… */` section dividers — a monolith that has already survived 26+ sprints of hardening. | `wc -l src/chirp_ui/templates/chirpui.css`; `grep -c '^/\* ====' src/chirp_ui/templates/chirpui.css` |
| E2 | Style bleed across nested instances of the same block is an unavoidable hazard today. `card--link` inside `card--feature`, `surface` inside `surface`, and the `hover` rules on outer cards all leak unless the author pre-empts with verbose descendant selectors. | `examples/css-scope-prototype/card.scope.css` header; chirpui.css:4642–4985 |
| E3 | Two prior sprints already paid the drift-cost tax: Sprint 17 consolidated **102 compound `[data-style="neumorphic"]` selectors → 44** after the vocabulary fractured; Sprint 7 tokenized **51 hardcoded `font-weight: 600`** after they had already diverged. | `CLAUDE.md § Sharp edges` rows for Sprint 7 and Sprint 17 |
| E4 | The consumer override story today is specificity or `!important`. No layered API; no documented contract for "where does my site's override go so it wins without a fight." | `chirpui.css` contains zero `@layer` declarations (`grep -c '@layer' chirpui.css` == 0); consumer docs describe no override surface |
| E5 | The registry knows about `elements` and `tokens` per component (`ComponentDescriptor`), but it does NOT know which CSS classes the shipped stylesheet actually emits. `design_system_report()` cannot answer "is this class orphaned." | `src/chirp_ui/components.py:28-50`; no `emits` field |
| E6 | CI already has three CSS gates that would catch a regression within seconds of a bad partial: `css-check`, `css-contract-check`, `css-transition-check`. That safety net is the reason incremental migration is affordable. | `pyproject.toml:213-215, 224-232` |
| E7 | Free-threading is a hard platform bet (Python 3.14+, `_Py_mod_gil = 0`), so any build tool with GIL-held Python bindings (Lightning CSS, esbuild-py, etc.) is disqualified. Pure Python or subprocess-to-binary only. | `pyproject.toml: requires-python = ">=3.14"`; `memory/project_free_threading_tooling_constraint.md` |

**Problem statement.** A 15k-line monolith with no layered override API, demonstrated drift cost, and a registry that cannot see the CSS it is supposed to describe. Consumers override via specificity games. Agents cite classes they hallucinate. Every component rewrite re-pays the tax E3 quantified.

### Evidence → mitigation map

| Evidence | Sprint(s) |
|----------|-----------|
| E1 (monolith size)       | S2 (extract), S5–S6 (envelope rewrite) |
| E2 (nested bleed)        | S5 (pilot envelope), S6 (fan-out) |
| E3 (drift cost)          | S4 (registry `emits` parity test) |
| E4 (override story)      | S3 (layer order declared + documented) |
| E5 (registry blind to CSS) | S4 (`emits` field + parity test) |
| E6 (CI gates exist)      | S1 (build scaffold wires them) |
| E7 (free-threading)      | S0 (tool decision), S1 (pure-Python concat) |

## Invariants

Four invariants that must hold **after every sprint**. Any sprint that breaks one is rolled back, not patched forward.

1. **BEM API surface is byte-identical.** `git diff` on every `src/chirp_ui/templates/**/*.html` is empty across this epic. Consumer templates render identical HTML byte-for-byte. Enforced by `test_template_css_contract.py` + a new `test_rendered_html_golden.py` golden file.
2. **No CSS regressions.** `poe css-check`, `poe css-contract-check`, and `poe css-transition-check` all pass at every commit on the epic branch.
3. **Zero new runtime dependencies; build stays pure Python.** `uv tree` shows no additions outside `[dependency-groups.dev]`. Free-threading compat (E7) preserved.
4. **Registry-emits parity.** By end of S4, every class in the shipped `chirpui.css` appears in some `ComponentDescriptor.emits` set, and every class in any `emits` set appears in the stylesheet. Divergence fails `test_registry_emits_parity.py`.

## Target architecture

```
src/chirp_ui/templates/
    chirpui.css              # shipped (generated, committed)
    css/                     # NEW — authoring partials
        _layers.css          # @layer chirpui.reset, chirpui.token, …, chirpui.utility;
        _reset.css
        _tokens.css
        _base.css
        components/
            _card.css        # @layer chirpui.component { @scope … }
            _btn.css
            …
        _utility.css

scripts/
    build_chirpui_css.py     # NEW — pure-Python concat with banner comments

src/chirp_ui/components.py   # adds ComponentDescriptor.emits: frozenset[str]

tests/
    test_rendered_html_golden.py   # NEW — template output hasn't drifted
    test_registry_emits_parity.py  # NEW — registry.emits ↔ stylesheet classes
    test_chirpui_css_concat.py     # NEW — concat output bit-for-bit matches commit
```

**Envelope convention** (every component partial):

```css
@layer chirpui.component {
    @scope (.chirpui-NAME) to (.chirpui-NAME .chirpui-NAME) {
        :scope { /* root */ }
        .chirpui-NAME__part { /* children */ }
        :scope.chirpui-NAME--modifier { /* variants */ }
    }
}
```

**Consumer override contract** (published API):

```css
/* In the consuming site, loaded after chirpui.css */
@layer app.overrides {
    .chirpui-card { border-color: var(--brand-teal); }
}
```

`app.overrides` is declared after `chirpui.component` in the top-of-file layer order, so any rule inside it wins without `!important` or specificity tricks.

## Sprint overview

| Sprint | Goal | Risk | Ships |
|--------|------|------|-------|
| **S0** | Design lock-in: layer names, partial paths, build API, registry schema. Decision doc. | Low — doc only | `docs/DESIGN-css-registry-projection.md` |
| **S1** | Pure-Python concat build scaffold + poe task + bit-identical test. No content change. | Low — additive | `scripts/build_chirpui_css.py`, new poe task `build-css`, new test |
| **S2** | Split monolith into partials in declared layer order. Semantic no-op. | Medium — mechanical surgery | `src/chirp_ui/templates/css/**` |
| **S3** | Declare `@layer` order at the top of concatenated output; document `app.overrides` surface. | Low — prepend-only | Header block in `_layers.css`; `docs/CSS-OVERRIDE-SURFACE.md` |
| **S4** | Add `ComponentDescriptor.emits: frozenset[str]`; populate from partials; parity test. | Medium — data entry + enforcement | Updated descriptors; new parity test |
| **S5** | Pilot rewrite: `card` partial → `@layer chirpui.component { @scope … }` envelope. Visual-diff gate. | Medium — real CSS semantics change on one component | `src/chirp_ui/templates/css/components/_card.css` in envelope form |
| **S6** | Opportunistic fan-out. Rewrite partials to the envelope whenever a component is touched for another reason. Not a big-bang. | Low per component — spread over many PRs | Per-component PRs |
| **S7** | Emit machine-readable manifest from registry + `emits`. Agents cite real classes. | Low — additive output of S4 | `chirpui manifest --json` CLI + JSON schema |

Sprint 0 is always a design sprint — every downstream sprint has acceptance criteria that reference the design doc.

---

## Sprint 0 — Design lock-in

**Goal.** Answer the four open decisions in writing so S1–S7 can execute without re-litigation.

**Decisions to settle:**

1. **Layer namespace.** `chirpui.reset` / `chirpui.token` / `chirpui.base` / `chirpui.component` / `chirpui.utility` (namespaced) vs unnamespaced. Recommend namespaced — a consumer using a plain `reset` layer in their own app won't collide.
2. **Partials directory.** `src/chirp_ui/templates/css/` (adjacent to `chirpui.css`) vs `src/chirp_ui/templates/chirpui/css/` (namespaced alongside the macros). Recommend the first — matches the single-file neighbor and needs no `package-data` glob update.
3. **Concat script API.** Input = an ordered list of partials driven by a manifest in `scripts/build_chirpui_css.py`; output = `src/chirp_ui/templates/chirpui.css` with `/* === <file> === */` banners. Deterministic byte-for-byte given same inputs.
4. **Registry `emits` schema.** `frozenset[str]` of fully-qualified class names (`chirpui-card`, `chirpui-card__header`, `chirpui-card--feature`). Generated-at-import from `block` + `elements` + `variants` + `sizes` + `modifiers`, with an optional `extra_emits` escape hatch for classes the descriptor grammar can't express (e.g. `chirpui-card__header-wrap`).

**Tasks:**
- T0.1 Draft `docs/DESIGN-css-registry-projection.md` capturing the four decisions above, the envelope convention, and the override contract.
- T0.2 Add a diagram of the build flow: partials → concat → `chirpui.css` → consumers; parallel path: descriptors → `emits` → parity-test → manifest.
- T0.3 Publish the consumer override contract as a one-pager (`docs/CSS-OVERRIDE-SURFACE.md`) stubbed in S0, populated in S3.

**Acceptance:**
- `ls docs/DESIGN-css-registry-projection.md` returns a file.
- `grep -c '^## Decision' docs/DESIGN-css-registry-projection.md` ≥ 4.
- No code changes this sprint.

---

## Sprint 1 — Build scaffold

**Goal.** Wire the concat pipeline end-to-end with the *existing* monolith as input, so later sprints can move content without touching the build again.

**Tasks:**
- T1.1 Create `scripts/build_chirpui_css.py`: pure-Python, stdlib-only, reads an ordered manifest, writes `src/chirp_ui/templates/chirpui.css` with banner comments between partials. No minification, no source maps — both are out of scope for the library build.
- T1.2 Add a trivial `css/_prelude.css` containing a header comment + the future layer declaration site. At this sprint it's the entire current `chirpui.css` wrapped into one "partial" so the concat output equals the input.
- T1.3 Add `poe build-css = "python scripts/build_chirpui_css.py"`.
- T1.4 Add `tests/test_chirpui_css_concat.py`: run the script into a temp file, diff against the committed `chirpui.css`, assert byte-identical.
- T1.5 Wire `poe ci` to run `build-css` before `css-check` so a PR that edits partials but forgets to commit the rebuilt monolith fails loudly.

**Acceptance:**
- `poe build-css && git diff --exit-code src/chirp_ui/templates/chirpui.css` exits 0.
- `poe ci` passes with no other changes.
- `uv tree --depth 0` shows no new runtime dependencies.

---

## Sprint 2 — Extract partials

**Goal.** Split the monolith into one partial per `/* ==== */` section. Pure file surgery; no semantic change.

**Tasks:**
- T2.1 For each of the 167 section dividers (E1), create `src/chirp_ui/templates/css/components/_<name>.css` (or `_base.css`, `_reset.css`, `_tokens.css`, `_utility.css` for non-component sections).
- T2.2 Update the manifest in `scripts/build_chirpui_css.py` so the concat output still equals the original monolith line-for-line.
- T2.3 Run `poe build-css && git diff --exit-code src/chirp_ui/templates/chirpui.css` after each partial is extracted — must stay empty through the entire split.

**Acceptance:**
- `ls src/chirp_ui/templates/css/components/ | wc -l` ≥ 80 (one per component section).
- `poe ci` passes.
- `git diff --stat src/chirp_ui/templates/chirpui.css` shows 0 changes.

**Rollback criterion.** If `test_chirpui_css_concat.py` ever diverges during extraction, revert and restart the split — do not hand-edit the generated output.

---

## Sprint 3 — Cascade order as public API

**Goal.** Make the cascade legible and the consumer override surface contractual.

**Tasks:**
- T3.1 Add, as the first thing in the concatenated output: `@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;`. This is a no-op layering that only declares order.
- T3.2 Wrap each partial's rules in the appropriate `@layer chirpui.<name> { … }`. For components still authored in the pre-envelope form, `@layer chirpui.component { …existing rules… }` is the whole change.
- T3.3 Write `docs/CSS-OVERRIDE-SURFACE.md` — publish `@layer app.overrides { … }` as the supported override path; deprecate specificity-based overrides (soft deprecation: documented, not enforced).
- T3.4 Add a contract test that the concatenated output starts with the exact layer declaration string.

**Acceptance:**
- First non-blank non-comment line of `chirpui.css` matches the declared layer order exactly.
- `docs/CSS-OVERRIDE-SURFACE.md` exists and is linked from `docs/INDEX.md` and `CLAUDE.md § Key conventions`.
- `poe ci` passes; no visual regressions in the showcase.

---

## Sprint 4 — Registry `emits` + parity

**Goal.** Make the registry know what the CSS emits, and make the CSS prove it only emits what the registry declares.

**Tasks:**
- T4.1 Add `emits: frozenset[str]` to `ComponentDescriptor` in `src/chirp_ui/components.py`. Default-computed in `__post_init__` from `f"chirpui-{block}"`, `f"chirpui-{block}__{e}"` for each element, `f"chirpui-{block}--{v}"` for each variant/size/modifier.
- T4.2 Add `extra_emits: frozenset[str] = frozenset()` escape hatch for classes the grammar doesn't capture (e.g. compound state classes).
- T4.3 Write `tests/test_registry_emits_parity.py`:
  - Parse every `.chirpui-<ident>` class name from every partial.
  - Assert every CSS class ∈ the union of all `emits`.
  - Assert every `emits` class ∈ the CSS.
  - Asymmetric failures print which side is the orphan.
- T4.4 For each gap surfaced by the test, either extend `extra_emits` (if the class is legitimate) or delete the CSS (if it is orphaned — E3 shows that happens).

**Acceptance:**
- `uv run pytest tests/test_registry_emits_parity.py -q` passes.
- `design_system_report()` output contains the new `emits` field.
- `poe ci` passes.

---

## Sprint 5 — Pilot `card` to the `@scope` envelope

**Goal.** Prove the envelope convention end-to-end on a real, mid-complexity component with a known bleed hazard (E2).

**Tasks:**
- T5.1 Replace the contents of `src/chirp_ui/templates/css/components/_card.css` with the envelope-form rewrite. Use the faithful prototype in `examples/css-scope-prototype/card.scope.css` as the starting point; reconcile any recent drift in the monolith.
- T5.2 Add a browser test under `tests/browser/` that renders each card variant (`--feature`, `--horizontal`, `--stats`, `--link`, `--linked`, `--collapsible`, `--glass`, `--gradient-border`, `--gradient-header`) and the card-inside-card bleed case; screenshot-diffs against a committed baseline.
- T5.3 Update the `card` `ComponentDescriptor.extra_emits` if the rewrite consolidated any compound classes.
- T5.4 Document the envelope convention in `CLAUDE.md § Key conventions` as the default for new components.

**Acceptance:**
- `poe ci` passes.
- `poe test-browser` passes with the new card-variant screenshot baseline.
- The card-inside-card bleed case (outer `hover` border-color leaking to inner card) is visibly fixed.

**Rollback criterion.** Any visual regression in an existing card-bearing page that isn't the known bleed → revert this sprint and re-pilot on a simpler component (recommend `btn`).

---

## Sprint 6 — Opportunistic fan-out

**Goal.** Migrate remaining components to the envelope convention without a big-bang risk budget.

**Rules of engagement:**
- Whenever a PR touches a component's CSS for any other reason, the PR must also convert the partial to the envelope form.
- Each conversion is self-contained: one component's partial, one screenshot test, one entry in the PR description.
- No deadline. The invariants (registry-emits parity, CI gates) keep the half-converted codebase honest.

**Acceptance (per-component):**
- Partial matches the envelope convention.
- Variant screenshot baseline updated.
- `poe ci` + `poe test-browser` pass.

**Epic-level acceptance.** Tracked in a lightweight markdown checklist in `docs/PLAN-css-scope-and-layer.md § Migration status` — appended in S6. Closing the epic does not require 100 % conversion; it requires the *mechanism* (concat + layer order + registry parity + envelope convention) to be load-bearing.

---

## Sprint 7 — Agent-groundable manifest

**Goal.** Publish the registry (including `emits`) as a machine-readable manifest so AI coding agents cite real classes, not plausible ones.

**Tasks:**
- [x] T7.1 Add `src/chirp_ui/manifest.py` with a `build_manifest()` that returns a JSON-serializable snapshot of `COMPONENTS` including `block`, `variants`, `sizes`, `modifiers`, `elements`, `slots`, `tokens`, `emits`, `template`.
- [x] T7.2 Add a CLI entry point: `python -m chirp_ui.manifest --json > chirpui.manifest.json`. (`--md` remains a future additive flag.)
- [x] T7.3 Emit the manifest as a build artifact. `site/public/` is not committed (per `CLAUDE.md`), so instead: `poe docs-emit-manifest` writes `site/public/chirpui.manifest.json`, wired into `poe docs-build-all` so the published docs site always serves a fresh copy.
- [x] T7.4 Round-trip test — `tests/test_manifest.py` covers determinism, schema+version, per-component attribute parity, per-token parity, stats counts, valid JSON, and CLI parity with the Python API.

**Acceptance:**
- [x] `python -m chirp_ui.manifest --json | jq '.components | length'` returns 309.
- [x] The manifest is referenced from `docs/VISION.md § The flywheel` row 5 as the shipped artifact (Python API, CLI, site artifact).

---

## Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Sprint |
|----|------|------------|--------|------------|--------|
| R1 | Split misses a byte, breaks a downstream consumer bundle | Medium | High | Bit-identical concat test runs after every extraction | S1, S2 |
| R2 | `@scope` browser support not universal enough | Low | Medium | Baselines confirm Safari 17.4+/Chrome 118+/Firefox 128+ in widespread use by mid-2025; library is pre-compiled so no polyfill risk | S5 |
| R3 | Envelope rewrite introduces a subtle semantic change on a high-traffic component | Medium | High | Pilot on one component (S5) with browser screenshot test; fan-out (S6) repeats the gate per component | S5, S6 |
| R4 | Registry-emits parity test becomes a productivity drag if drift is noisy | Low | Medium | `extra_emits` escape hatch; parity failures print exact symmetric diff so PR author knows which side to fix | S4 |
| R5 | Consumer site relies on implicit cascade ordering that our explicit layer order changes | Low | Medium | `@layer app.overrides` is strictly-later than existing implicit rules; any consumer on specificity tricks continues to work (specificity beats layer outside layers) — document migration path in S3 | S3 |
| R6 | Someone proposes Lightning CSS or another GIL-bound tool mid-epic | Medium | High (platform bet) | `memory/project_free_threading_tooling_constraint.md` + S0 decision doc disqualify these tools upfront | S0 |
| R7 | Pilot `card` rewrite exposes that the monolith had an unintentional cross-component style dependency | Low | Medium | Browser screenshot tests in S5 cover the call-sites we know; accept one hotfix PR if a latent dep surfaces | S5 |

## Success metrics

| Metric | Baseline (today) | Checkpoint (after S4) | Target (after S5) | Target (after S6) |
|--------|------------------|-----------------------|-------------------|-------------------|
| Shipped `chirpui.css` authored-file count | 1 | 80+ partials | 80+ | 80+ |
| CI gates on CSS | 3 | 5 (adds concat + parity) | 6 (adds visual diff on pilot) | 6 |
| Classes cited by registry `emits` / classes in shipped CSS | 0 % | 100 % | 100 % | 100 % |
| Components in envelope form | 0 | 0 | 1 (`card`) | opportunistic — no target |
| New runtime deps | 0 | 0 | 0 | 0 |
| Consumer override API documented | No | Yes (S3) | Yes | Yes |

**Intermediate checkpoint (end of S4):** the *mechanism* is in place — partials exist, layer order is declared, registry sees the CSS. The envelope rewrite is still optional. This is the earliest safe stopping point if the pilot in S5 reveals an unsolvable regression; the epic still delivered E4 (override API) and E5 (registry parity).

## Migration status

The envelope convention is the default for new components and for any partial modified in an existing PR. Conversions do not need a dedicated PR — this is a flywheel, not a forced march.

**Detection.** A partial is "converted" when its first non-comment token is `@layer chirpui.component` (the build's `_wrap_in_layer` treats that as authored layering). Audit:

```bash
# List converted partials
grep -lE '^@layer chirpui\.component' src/chirp_ui/templates/css/partials/*.css
```

**Converted (envelope form):**

- [x] `045_card.css` — S5 pilot

**Legacy (flat, opportunistic conversion):** every other partial in `src/chirp_ui/templates/css/partials/`. Roughly 159 partials as of S6 opening; converted partials will shift to the list above as routine PRs land. No global checklist is maintained — the grep above is the source of truth.

**Epic closure signal.** The epic can close when:

1. The four mechanism invariants are green: concat build, layer declaration, registry–CSS parity, envelope-partial opt-out — all load-bearing in CI.
2. At least one high-traffic component (card) is in envelope form and has browser-test coverage of its variants.
3. The policy is documented in `CLAUDE.md § Key conventions` and new-component guidance points at card as the reference.

Percentage converted is not an epic gate — half-converted is a supported steady state.

## Open items

- **S0 decision: layer namespace.** Recommend `chirpui.*`. Needs a second opinion before S3 ships.
- **S0 decision: partials directory.** Recommend `src/chirp_ui/templates/css/`. Needs sign-off before S2 ships.
- **S7 scope creep risk.** Don't let the manifest absorb "and also generate docs / and also generate the showcase" — that's a separate epic.

## Related

- `docs/VISION.md § CSS architecture as a registry projection` — the *why* this epic exists
- `examples/css-scope-prototype/card.scope.css` — S5 starting point
- `CLAUDE.md § Sharp edges — what's been hardened` — the drift cost history (E3)
- `memory/project_css_scope_layer_decision.md` — decision record for the @scope-as-authoring-format direction
- `memory/project_free_threading_tooling_constraint.md` — R6 / E7 constraint
