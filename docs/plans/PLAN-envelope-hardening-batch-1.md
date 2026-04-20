# Epic: Envelope hardening batch 1 — close known bleed holes deliberately

**Status**: Draft
**Created**: 2026-04-20
**Target**: chirp-ui next minor (post-Sprint 26 base-layer hardening)
**Estimated Effort**: 10–14h across 7 PRs
**Dependencies**: `docs/plans/PLAN-css-scope-and-layer.md` (parent epic; S0–S5 + S7 done, S6 in opportunistic mode)
**Source**: parent epic E2 (nested-block bleed evidence), pilot `045_card.css` (Sprint 5), user memory `feedback_tray_shell_sharp_edges.md`, browser-test inventory under `tests/browser/`

---

## Why This Matters

The parent epic shipped the *mechanism* (concat build, layer order, registry-emits parity, envelope convention) and proved it on `card`. The remaining 159 partials are in flat form, queued for **opportunistic** conversion whenever a PR touches them for another reason.

That policy is correct as the steady-state default — but it has a known gap: **specific components have documented bleed risk in production today**, and waiting for an organic touch leaves the bleed in place indefinitely. Three components were called out explicitly in the parent epic's E2 ("`surface` inside `surface`") or in user memory (tray sharp edges); two more (`video-card`, `channel-card`) duplicate `card`'s structure but live outside its scope, so they did not inherit the pilot's bleed fix.

This plan executes one **deliberate hardening batch** — six conversions, one PR each — then returns to opportunistic mode. It does not change the parent policy; it discharges the highest-value residual risk before drifting into wait-and-see.

### Evidence

| # | Finding | Source |
|---|---------|--------|
| E1 | 160 partials shipped; 1 (`045_card.css`) in envelope form. 159 legacy, all carrying the bleed risk class the pilot fixed. | `ls src/chirp_ui/templates/css/partials/`; `grep -lE '^@layer chirpui\.component' src/chirp_ui/templates/css/partials/*.css` |
| E2 | Parent epic explicitly documented `surface`-inside-`surface` as a live bleed hazard. `039_surface.css` is 168 lines of flat selectors with 7+ `--variant` modifiers — exactly the shape the envelope was designed for. | `docs/plans/PLAN-css-scope-and-layer.md § Evidence E2`; `wc -l src/chirp_ui/templates/css/partials/039_surface.css`; `grep -c '^.chirpui-surface--' src/chirp_ui/templates/css/partials/039_surface.css` |
| E3 | `tray` was independently flagged in user memory as a sharp-edge surface (initial state, `#page-root` double-styling, `hx-select` inheritance gap). Conversion gives the partial the same bleed protection card now has. | `memory/feedback_tray_shell_sharp_edges.md`; `src/chirp_ui/templates/css/partials/065_tray.css` (98 lines) |
| E4 | `video-card`, `channel-card`, `resource-card` mirror `chirpui-card`'s visual structure (border + radius + overflow-clip + hover transition) but use their own block name, so the card pilot's `@scope (.chirpui-card) to (.chirpui-card .chirpui-card)` upper boundary does not protect them. They re-incur the same hover-leak risk on every render that nests one inside another. | `head -10 src/chirp_ui/templates/css/partials/{046,047,159}_*.css` |
| E5 | Browser-test scaffolding already exists for `tray`, `drawer`, `modals`, `card_variants`. These four components can be converted with the existing harness — no new test infrastructure required. `surface`, `callout`, `video-card`, `channel-card` need new browser tests (incremental, not net-new infra). | `ls tests/browser/test_*.py` |
| E6 | The CI gates that made the pilot affordable (`css-check`, `css-contract-check`, `css-transition-check`, `test_chirpui_css_concat.py`, `test_registry_emits_parity.py`) are all in place and green. Each conversion runs through the same gate that caught the pilot's drift. | `pyproject.toml § poe`; `tests/test_chirpui_css_concat.py`; `tests/test_registry_emits_parity.py` |

### Evidence → mitigation map

| Evidence | Sprint(s) |
|----------|-----------|
| E1 (1/160 converted) | S1–S6 (six deliberate conversions; opportunistic continues for the rest) |
| E2 (`surface` bleed) | S4 (surface envelope + new bleed-case browser test) |
| E3 (`tray` sharp edges) | S1 (tray conversion) |
| E4 (card-likes outside card scope) | S6 (video-card + channel-card batch) |
| E5 (existing browser tests) | S1, S2, S3 (cheapest first) |
| E6 (CI gates ready) | All sprints — gate is the per-PR acceptance |

### Invariants

These must remain true after every sprint. A sprint that breaks one is reverted, not patched forward.

1. **BEM API surface is byte-identical.** `git diff src/chirp_ui/templates/**/*.html` is empty across this batch. No template changes; only `.css` partials and added browser tests.
2. **No CSS regressions.** `poe ci` (lint + format + CSS gates + ty + tests) passes at every commit.
3. **Concat output is deterministic.** `poe build-css && git diff --exit-code src/chirp_ui/templates/chirpui.css` exits 0 after every conversion.
4. **Registry-emits parity holds.** `tests/test_registry_emits_parity.py` passes after every conversion. If a conversion consolidates compound classes, update `extra_emits` in the same PR.

---

## Target Architecture

No new architecture. Each converted partial moves from:

```css
/* Flat (today) */
.chirpui-NAME { ... }
.chirpui-NAME--variant { ... }
.chirpui-NAME__part { ... }
.chirpui-NAME:hover { ... }
```

to the envelope form already pioneered by `045_card.css`:

```css
@layer chirpui.component {
    @scope (.chirpui-NAME) to (.chirpui-NAME .chirpui-NAME) {
        :scope { ... }
        :scope:hover { ... }
        .chirpui-NAME__part { ... }
        :scope.chirpui-NAME--variant { ... }
    }
}
```

The upper scope boundary `.chirpui-NAME .chirpui-NAME` stops outer-instance rules at the first nested instance — fixing bleed (E2, E4).

After this batch: **7 of 160 partials in envelope form** (card pilot + six new). The remaining 153 stay in opportunistic mode per the parent epic.

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Prioritization audit + browser-test pattern doc | 1h | Low (doc only) | Yes (RFC only) |
| 1 | `065_tray.css` envelope (existing test) | 1.5h | Low | Yes |
| 2 | `053_drawer.css` envelope (existing test) | 1.5h | Low | Yes |
| 3 | `052_modal.css` envelope (existing test) | 1.5h | Low | Yes |
| 4 | `039_surface.css` envelope + new bleed-case browser test | 3h | Medium | Yes |
| 5 | `041_callout.css` envelope + new browser test | 1.5h | Low | Yes |
| 6 | `046_video-card.css` + `047_channel-card.css` envelope (one PR; mirror card scaffold) | 2h | Low | Yes |

Sprint 0 is design/decision only — no code. Sprints 1–3 are intentionally first because they have existing browser tests, so the per-PR effort is dominated by the CSS rewrite, not test scaffolding. Sprint 4 (`surface`) is the highest-leverage conversion but needs a new bleed-case test, hence the 3h estimate. Sprints 5–6 mop up the remaining card-likes and the other surface-shaped container.

---

## Sprint 0 — Prioritization audit & test-pattern doc

**Goal.** Lock in the order, the per-PR template, and the screenshot-test pattern for new conversions, so S1–S6 execute without re-litigation.

### Task 0.1 — Confirm prioritization in writing

Append a `## Hardening batch 1 — priority order` section to `docs/plans/PLAN-css-scope-and-layer.md § Migration status` listing the six partials in conversion order, each with a one-line bleed-risk justification and a link to the browser test it will use.

**Files**: `docs/plans/PLAN-css-scope-and-layer.md`
**Acceptance**: `grep -c 'Hardening batch 1' docs/plans/PLAN-css-scope-and-layer.md` ≥ 1; six files listed.

### Task 0.2 — Document the per-PR conversion template

Add a short `## Per-PR conversion template` subsection (under the existing `Migration status` section) with the checklist a contributor follows for one conversion: rewrite partial → run `poe build-css` → run `poe ci` → add/extend browser test → PR description references this batch plan.

**Files**: `docs/plans/PLAN-css-scope-and-layer.md`
**Acceptance**: subsection contains the five-step checklist verbatim.

### Task 0.3 — Document the bleed-case browser-test pattern

Add a brief `### Browser test: bleed case` subsection citing `tests/browser/test_card_variants.py` as the reference for testing nested-instance bleed. Surface, callout, video-card, channel-card tests will follow this pattern.

**Files**: `docs/plans/PLAN-css-scope-and-layer.md`
**Acceptance**: subsection exists and references `test_card_variants.py` by path.

**Sprint acceptance**: no code changes; `poe ci` still green; the parent epic's `Migration status` section grows three subsections.

---

## Sprint 1 — `tray` envelope

**Goal.** Convert the tray partial to envelope form. Existing `tests/browser/test_tray.py` is the regression gate.

### Task 1.1 — Rewrite `065_tray.css` to the envelope convention

Use the `:scope` / `&.chirpui-tray--modifier` pattern from `045_card.css`. Upper boundary: `.chirpui-tray .chirpui-tray` (defensive — tray-in-tray is unlikely but cheap to scope).

**Files**: `src/chirp_ui/templates/css/partials/065_tray.css`
**Acceptance**:
- First non-comment line is `@layer chirpui.component {`.
- `poe build-css && git diff --exit-code src/chirp_ui/templates/chirpui.css` exits 0 after committing the regenerated monolith.
- `poe ci` passes.
- `uv run pytest tests/browser/test_tray.py -q` passes.

### Task 1.2 — Update `extra_emits` if the rewrite consolidates classes

If the conversion exposes any compound class the descriptor grammar can't express, add it to `tray`'s `ComponentDescriptor.extra_emits`. Otherwise no descriptor change.

**Files**: `src/chirp_ui/components.py` (only if needed)
**Acceptance**: `uv run pytest tests/test_registry_emits_parity.py -q` passes.

**Sprint acceptance**: one PR, listed under `Migration status § Converted` in the parent epic. PR description cites this plan + the bleed-risk justification from S0.

---

## Sprint 2 — `drawer` envelope

**Goal.** Convert the drawer partial. Existing `tests/browser/test_drawer.py` is the regression gate. Drawer often contains other components (forms, lists), so the upper scope boundary `.chirpui-drawer .chirpui-drawer` is defensive against nested drawer use.

### Task 2.1 — Rewrite `053_drawer.css`

**Files**: `src/chirp_ui/templates/css/partials/053_drawer.css`
**Acceptance**: same gate as Sprint 1 (envelope opener, concat clean, `poe ci` green, `tests/browser/test_drawer.py` green, parity test green).

---

## Sprint 3 — `modal` envelope

**Goal.** Convert the modal partial. Existing `tests/browser/test_modals.py` is the regression gate. Modal-in-modal is a real pattern (confirmation dialog inside a settings modal), so the upper boundary genuinely matters.

### Task 3.1 — Rewrite `052_modal.css`

**Files**: `src/chirp_ui/templates/css/partials/052_modal.css`
**Acceptance**: same gate as Sprint 1; additionally `tests/browser/test_modals.py` exercises the modal-in-modal case (extend the existing test if it doesn't already).

---

## Sprint 4 — `surface` envelope + bleed-case browser test

**Goal.** The highest-leverage conversion. `surface` is structural — cards, callouts, panels are all surfaces underneath — and the parent epic's E2 explicitly cites `surface`-inside-`surface` as a live hazard. This sprint also adds the missing browser test.

### Task 4.1 — Add `tests/browser/test_surface.py`

Render a `surface--elevated` containing a `surface--muted`. Assert the inner surface's computed `box-shadow` is `none` (or matches `--muted`'s declared value), proving the outer's `--elevated` shadow does not leak in. Also render side-by-side `surface--default` with and without nesting to baseline.

**Files**: `tests/browser/test_surface.py` (new)
**Acceptance**: test exists, runs, **fails on the unconverted partial** (proving it catches the bleed), passes after Task 4.2.

### Task 4.2 — Rewrite `039_surface.css`

Use envelope form. The `:scope.chirpui-surface--variant` pattern handles the seven existing variant modifiers cleanly. Preserve the descendant rule `.chirpui-surface a { overflow-wrap: anywhere; }` inside `:scope` (it's intentionally a descendant selector, not a child).

**Files**: `src/chirp_ui/templates/css/partials/039_surface.css`
**Acceptance**: standard envelope gate; **plus** Task 4.1's test now passes.

### Task 4.3 — Update `surface`'s `extra_emits` if needed

**Files**: `src/chirp_ui/components.py` (only if needed)
**Acceptance**: parity test green.

**Rollback criterion.** If Task 4.1's test passes on the unconverted partial, the bleed isn't actually present — re-examine the test before claiming the conversion fixed anything.

---

## Sprint 5 — `callout` envelope + browser test

**Goal.** Callout is a surface-shaped container often nested inside a `surface` or `card`. The upper boundary protects against a callout-in-callout (notice → expandable detail → notice) pattern.

### Task 5.1 — Add `tests/browser/test_callout.py` covering each callout variant + a callout-in-callout case

**Files**: `tests/browser/test_callout.py` (new)
**Acceptance**: test renders all callout variants; nested case asserts the inner callout's icon/border-color comes from its own variant, not the outer's.

### Task 5.2 — Rewrite `041_callout.css`

**Files**: `src/chirp_ui/templates/css/partials/041_callout.css`
**Acceptance**: standard envelope gate + new test green.

---

## Sprint 6 — `video-card` + `channel-card` batch

**Goal.** Both partials mirror `card`'s structure (border + radius + overflow-clip + hover transition) but live outside `card`'s `@scope`. They re-incur the bleed risk the pilot fixed for `card`. Convert together — they're tiny (~150 lines combined) and structurally identical.

### Task 6.1 — Add `tests/browser/test_video_card_variants.py` and `tests/browser/test_channel_card_variants.py`

Mirror `tests/browser/test_card_variants.py`. For each component, exercise the variant matrix and one nested-instance case.

**Files**: `tests/browser/test_video_card_variants.py`, `tests/browser/test_channel_card_variants.py` (new)
**Acceptance**: both tests exist, run, and are green on the unconverted partials (baseline) and green after Task 6.2 (no regression).

### Task 6.2 — Rewrite `046_video-card.css` and `047_channel-card.css` to envelope form

**Files**: `src/chirp_ui/templates/css/partials/046_video-card.css`, `src/chirp_ui/templates/css/partials/047_channel-card.css`
**Acceptance**: standard envelope gate; both PRs (or one combined) listed under `Migration status § Converted`.

**Note on `159_resource-card.css`.** Deferred from this batch — it's a thin 7-line wrapper used inside `resource_index` grids, with no independent bleed surface. Convert opportunistically when `resource_index` is next touched.

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Sprint |
|----|------|------------|--------|------------|--------|
| R1 | Browser screenshot baselines diverge across runs (font rendering, CI vs local) | Medium | Low | Existing `tests/browser/conftest.py` already handles tolerance for the card pilot; reuse same harness | S1, S2, S3 |
| R2 | Surface conversion exposes a latent dependency in a downstream component (e.g. `aura` rendering inside a surface relies on a surface declarative quirk) | Low | Medium | Sprint 4 runs `poe ci` (which includes the full template/render test suite) and the showcase visual smoke test before merge | S4 |
| R3 | Modal-in-modal browser test exposes an existing bug unrelated to the conversion | Medium | Low | Acceptable outcome — file an issue, fix in a follow-up PR; envelope conversion is still mergeable since the test was added in the same PR and documents the new state | S3 |
| R4 | Six PRs in close succession overload review capacity | Low | Low | One sprint per week pace; each PR is < 50 LOC of CSS + < 100 LOC of test; reviewers familiar with the pilot template | All |
| R5 | A converted partial regresses a consumer site that relies on flat-CSS specificity | Low | Medium | Parent epic R5 + S3 already documented `app.overrides` as the supported override path; consumer regressions point at the override surface, not at this batch | All |
| R6 | New browser tests slow `poe test-browser` enough to discourage running it locally | Low | Low | Tests are scoped to single component renders; budget < 0.5s per added test; revisit if `test-browser` exceeds 60s wall clock | S4, S5, S6 |
| R7 | Batch creates a precedent for "deliberate batches" that erodes the opportunistic policy | Medium | Medium | This plan explicitly closes after S6 and returns to opportunistic mode; future deliberate batches require their own justified plan with E1-style evidence | (epic closure) |

---

## Success Metrics

| Metric | Baseline (today) | After S3 | After S4 | After S6 (final) |
|--------|------------------|----------|----------|------------------|
| Partials in envelope form | 1 / 160 (0.6 %) | 4 / 160 (2.5 %) | 5 / 160 (3.1 %) | 7 / 160 (4.4 %) |
| Documented bleed hazards still live in CSS | 2 (`surface`, `tray`) + 3 card-likes outside scope | 1 (`surface`) + 3 card-likes | 0 + 3 card-likes | 0 |
| Components with browser-test coverage of bleed case | 1 (`card`) | 1 (`card`) | 2 (`card`, `surface`) | 5 (`card`, `surface`, `callout`, `video-card`, `channel-card`) |
| New runtime deps | 0 | 0 | 0 | 0 |
| Parent epic invariants green | 4/4 | 4/4 | 4/4 | 4/4 |

**Intermediate checkpoint (after S3).** The three cheapest conversions (existing browser tests) are done — proves the per-PR template scales beyond the pilot. If S4's surface test reveals an unsolvable regression, the epic still delivered measurable value (3 conversions, 0 regressions, refined PR template).

**Stopping condition.** After S6 ships, this batch closes. The parent epic's Sprint 6 (opportunistic) resumes as the steady-state policy. **Percentage converted is not an epic gate** — it never was for the parent, and it isn't here either.

---

## Relationship to Existing Work

- **Parent epic `docs/plans/PLAN-css-scope-and-layer.md`** — this is one explicit batch executed under that epic's Sprint 6 (opportunistic fan-out). Each PR adds an entry to that epic's `Migration status § Converted` list.
- **Pilot `045_card.css`** — the structural template every conversion in this batch follows. New contributors should read it before attempting a conversion.
- **`memory/feedback_tray_shell_sharp_edges.md`** — drove the inclusion of `tray` in S1.
- **`memory/project_chirpui_vision.md`** — registry-as-bet thesis. This batch reinforces it by closing CSS bleed holes that would otherwise undermine the registry's claim to be the source of truth.
- **CI gates added in parent epic S1, S3, S4** — all are the per-sprint acceptance gate here. No new CI infrastructure required.

---

## Changelog

- **2026-04-20** — Initial draft. Six conversions identified by intersecting parent-epic E2/E3 evidence with user-memory sharp edges and existing browser-test coverage.
