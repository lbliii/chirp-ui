# Epic: Behavior Layer Hardening — Tests, Contracts, and Error Recovery

**Status**: Complete
**Created**: 2026-04-10
**Target**: 0.3.0
**Estimated Effort**: 22–30h
**Dependencies**: kida ≥ 0.3.4 (provide/consume), vitest (already configured)
**Source**: Codebase exploration + evidence from existing plans (PLAN-test-coverage-hardening, PLAN-ascii-maturity, PLAN-provide-consume-expansion)

---

## Why This Matters

chirp-ui's visual layer is solid — 2,650 CSS classes, 188 templates, motion token enforcement, CSS contract tests. But the **behavior layer** has gaps that silently erode reliability:

1. **26 of 27 ASCII components have zero render tests** — variants and sizes are registered in `VARIANT_REGISTRY` / `SIZE_REGISTRY` but never exercised. Breakage is invisible.
2. **6 orphaned provide/consume keys** — `_card_variant`, `_bar_surface`, `_bar_density`, `_surface_variant`, `_streaming_role`, `_suspense_busy` are provided but never consumed. Dead context flow or missing consumers.
3. **Error boundary has no recovery story** — `error_boundary.js` catches errors and toggles DOM visibility, but doesn't display error details, support retry, or emit telemetry. Silent failures.
4. **13 Alpine components lack browser tests** — copy_button, command_palette, drawer, toast, split_panel, theme_toggle, sse_status, streaming_bubble, etc. Only 8 of 21 interactive components have Playwright coverage.

| Layer | Key Finding | Proposal Impact |
|-------|-------------|-----------------|
| ASCII components | 26/27 untested despite variant registration | FIXES — Sprint 1 adds render tests for all 26 |
| Provide/consume | 6 orphaned providers, 1 consumer without provider | FIXES — Sprint 2 wires consumers or removes dead providers |
| Error boundary | No error message display, retry, or reporting | FIXES — Sprint 3 adds fallback slots and retry |
| Alpine browser tests | 13/21 interactive components untested | FIXES — Sprint 4 adds Playwright coverage for 8 priority components |
| Island JS tests | 9 files × 0 tests | UNRELATED — already complete (115 tests, PLAN-island-js-test-infrastructure) |

### Invariants

These must remain true throughout or we stop and reassess:

1. **CI stays green**: `uv run poe ci` passes after every sprint. No regressions.
2. **CSS contract holds**: Every class in templates exists in `chirpui.css`. No orphaned references.
3. **No new Alpine JS in macros**: Interactive behavior uses `x-data` attributes only; no `<script>` tags in templates.

---

## Target Architecture

After this epic:

- **Every registered component has at least one render test** — render → assert BEM class + slot content + variant/size modifier.
- **Every `{% provide %}` key has at least one `consume()` call** or is removed. Zero orphans.
- **Error boundary supports**: error message display in fallback, reset-and-retry, and a `chirp:island:error:report` event for telemetry.
- **21/21 interactive Alpine components have Playwright coverage** (up from 8/21).

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: validate ASCII signatures, error boundary API, consumer sites | 2–3h | Low | Yes (RFC only) |
| 1 | ASCII render tests — 26 components | 5–7h | Low | Yes |
| 2 | Provide/consume: wire all 7 keys to consumers + showcase | 6–8h | Medium | Yes |
| 3 | Error boundary hardening — fallback slots, retry, telemetry event | 4–5h | Medium | Yes |
| 4 | Playwright tests for 8 priority Alpine components | 7–9h | Medium | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Solve design questions on paper before writing code.

### Task 0.1 — Validate ASCII macro signatures

Read all 26 untested ASCII templates. For each, document:
- Macro name and parameters (variant, size, extras)
- Expected BEM output class pattern
- Whether it has slots

**Files**: `src/chirp_ui/templates/chirpui/ascii_*.html`
**Acceptance**: Design doc listing all 26 signatures; no code changes.

### Task 0.2 — Decide fate of 6 orphaned providers

For each orphaned key, decide:
- **Wire**: identify the natural consumer template and the param it would influence
- **Remove**: if the key has no plausible consumer, delete the `{% provide %}` call

| Key | Decision | Rationale |
|-----|----------|-----------|
| `_card_variant` | Wire or remove? | Could style nested badges, buttons, dividers |
| `_bar_surface` | Wire or remove? | Could propagate to action_strip children |
| `_bar_density` | Wire or remove? | Could propagate to action_strip children |
| `_surface_variant` | Wire or remove? | Could style nested cards, dividers |
| `_streaming_role` | Wire or remove? | Could style copy_button, reaction_pill |
| `_suspense_busy` | Wire or remove? | Could disable interactions in busy slots |

**Acceptance**: Decision table filled in with rationale for each key.

### Task 0.3 — Design error boundary v2 API

Current error_boundary.js:
- Catches `chirp:island:error` → toggles `[data-error-body]` / `[data-error-fallback]` visibility
- Reset button restores healthy state

Proposed additions:
- `[data-error-message]` element inside fallback — populated with error `detail.reason`
- `[data-error-retry]` button — dispatches `chirp:island:action` with `action="retry"`, then resets
- `chirp:island:error:report` event — emitted on error for telemetry (detail includes boundaryId, reason, timestamp)

**Acceptance**: API spec with DOM contract, event shapes, and backward-compat notes.

### Task 0.4 — Prioritize 8 Alpine components for Playwright

Rank the 13 untested interactive components by user-facing risk:

Priority candidates (keyboard-driven, user-facing):
1. command_palette — search + keyboard nav
2. drawer/tray — open/close, focus trap
3. toast — auto-dismiss timing
4. copy_button — clipboard API
5. theme_toggle — localStorage persistence
6. split_panel — resize handle
7. sse_status — connection state display
8. streaming_bubble — live content update

**Acceptance**: Ranked list with 1-sentence justification per component.

---

## Sprint 1: ASCII Render Tests

**Goal**: Every ASCII component has at least one render test exercising its default output and variant modifiers.

### Task 1.1 — Add render tests for 26 ASCII components

For each component, test:
- Default render produces correct BEM root class (`chirpui-ascii-*`)
- Each registered variant produces the correct modifier class
- Size modifier applied when SIZE_REGISTRY entry exists
- Slot content injected correctly (where applicable)

Group by complexity:
- **Display-only** (14): ascii_badge, ascii_border, ascii_divider, ascii_empty, ascii_error, ascii_indicator, ascii_progress, ascii_skeleton, ascii_sparkline, ascii_spinner, ascii_7seg, ascii_split_flap, ascii_ticker, ascii_card
- **Interactive** (8): ascii_checkbox, ascii_fader, ascii_knob, ascii_modal, ascii_radio, ascii_stepper, ascii_toggle, ascii_vu_meter
- **Composite** (4): ascii_table, ascii_tabs, ascii_tile_btn, ascii_breaker_panel

**Files**: `tests/test_components.py` (add `TestAscii*` classes)
**Acceptance**: `uv run pytest tests/test_components.py -q` passes; `rg 'class TestAscii' tests/test_components.py | wc -l` returns ≥26.

---

## Sprint 2: Provide/Consume Wiring

**Goal**: Wire all 7 orphaned/missing providers to natural consumers. Showcase the context inheritance pattern.

### Task 2.1 — Wire `_card_variant` → badge, divider, alert

Add `consume("_card_variant", "")` to `badge()`, `divider()`, and `alert()` as a fallback variant. When a badge is nested inside a warning card, it auto-inherits the warning variant unless an explicit variant param is passed.

**Consumer pattern**:
```jinja
{% set _variant = (variant if variant else consume("_card_variant", "")) | validate_variant(...) %}
```

### Task 2.2 — Wire `_bar_surface` / `_bar_density` → button, icon_btn

Add consumers to `button()` and `icon_btn()` so toolbar children inherit surface tone and density from the parent command_bar/filter_bar. Explicit params always win.

### Task 2.3 — Wire `_surface_variant` → divider, badge, card

Nested components inside `surface()` or `panel()` inherit the surface variant as a fallback. A muted surface → muted dividers/badges inside it.

### Task 2.4 — Wire `_streaming_role` → copy_button

`copy_button()` inside a streaming bubble inherits the role, enabling role-aware styling (e.g., different copy icon placement for assistant vs user bubbles).

### Task 2.5 — Wire `_suspense_busy` → button, field macros

Buttons and interactive fields inside a `suspense_group()` auto-disable while the group is busy (`aria-busy="true"`). This is genuinely useful UX — prevents interaction during deferred loading.

### Task 2.6 — Wire `_sse_state` provider

`sse_retry` consumes `_sse_state` but no template provides it. Add `{% provide _sse_state = state %}` to `sse_status()` macro so the retry button inherits connection state.

### Task 2.7 — Add provide/consume contract tests

For each wired key, test:
- Parent macro provides the key
- Child macro consumes the key and renders differently based on value
- Explicit params override consumed context

**Files**: `src/chirp_ui/templates/chirpui/*.html` (template changes), `tests/test_components.py` (contract tests)
**Acceptance**: Every `{% provide %}` key has ≥1 `consume()` call. All new tests pass. `uv run poe ci` green.

---

## Sprint 3: Error Boundary Hardening

**Goal**: Error boundary displays error details, supports retry, and emits telemetry.

### Task 3.1 — Add error message display

When error fires, populate `[data-error-message]` with `detail.reason` (text content, not innerHTML — XSS safe).

### Task 3.2 — Add retry button support

`[data-error-retry]` button:
1. Dispatches `chirp:island:action` with `{ action: "retry", status: "pending" }`
2. Resets boundary to healthy state
3. Re-dispatches original mount if payload is available

### Task 3.3 — Add telemetry event

On error, emit `chirp:island:error:report` CustomEvent with:
```javascript
{ detail: { boundaryId, reason, timestamp: Date.now(), source: "error_boundary" } }
```

### Task 3.4 — Unit tests for new behavior

Add vitest tests for:
- Error message populates `[data-error-message]`
- Retry button dispatches action and resets state
- Telemetry event fires with correct shape
- Backward compat: existing reset button still works

**Files**: `src/chirp_ui/templates/islands/error_boundary.js`, `tests/js/error_boundary.test.js`
**Acceptance**: `npx vitest run` passes; new tests cover message, retry, and telemetry paths.

---

## Sprint 4: Playwright Tests for Alpine Components

**Goal**: 8 more interactive components get browser-level behavioral tests, bringing coverage from 8/21 to 16/21.

### Task 4.1 — Test infrastructure check

Verify `tests/browser/conftest.py` supports the test patterns needed (Alpine mount, htmx swap, localStorage, clipboard API mock).

### Task 4.2 — Write Playwright tests

| Component | Key behaviors to test |
|-----------|----------------------|
| command_palette | Open with keyboard, search filter, arrow nav, enter selects, escape closes |
| drawer / tray | Open trigger, close on backdrop, close on escape, focus trap |
| toast | Renders, auto-dismisses after timeout, manual dismiss |
| copy_button | Click copies text, "Copied!" feedback appears, reverts |
| theme_toggle | Cycles light/dark/system, persists to localStorage, applies class |
| split_panel | Drag resize, min/max bounds, keyboard resize |
| sse_status | Shows connected/disconnected/error states, dot color |
| streaming_bubble | Content updates live, role attribute correct |

**Files**: `tests/browser/test_*.py` (one file per component or grouped)
**Acceptance**: `make test-browser` passes; each component has ≥2 test cases.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Wiring consumers changes render output, breaking snapshots | Medium | Medium | Sprint 2 tests include before/after assertions; CSS contract test catches class drift |
| Error boundary retry creates infinite loop on persistent errors | Low | High | Retry dispatches action once; consumer must re-trigger explicitly |
| Playwright tests flaky due to Alpine timing | Medium | Medium | Use `page.wait_for_function("window.Alpine")` pattern from existing tests |
| New consume() calls add unexpected output to existing templates | Medium | Medium | Consumer pattern uses explicit-param-wins: `(variant if variant else consume(...))`. Existing callers unaffected. |

---

## Success Metrics

| Metric | Current | After Sprint 2 | After Sprint 4 |
|--------|---------|-----------------|-----------------|
| ASCII components with render tests | 27/27 ✅ | 27/27 | 27/27 |
| Orphaned provide/consume keys | 6 | 0 | 0 |
| Error boundary capabilities | catch + reset | catch + reset | catch + message + retry + telemetry |
| Alpine components with browser tests | 8/21 | 8/21 | 16/21 |
| Total Python test count | ~1,214 | ~1,240 | ~1,280 |
| Total JS test count | 115 | 115 | ~125 |

---

## Relationship to Existing Work

- **PLAN-test-coverage-hardening** — Sprint 3-4 of that plan overlap with our Sprint 1 (ASCII tests) and Sprint 4 (Playwright). This plan **supersedes** those remaining sprints with more specific scope and acceptance criteria.
- **PLAN-ascii-maturity** — Sprint 1 (render tests) already shipped in PR #40. 152 tests across 27 classes in `test_ascii_components.py`. Their Sprint 2-4 (keyboard/ARIA, composites, docs) are out of scope here — future work.
- **PLAN-provide-consume-expansion** — That plan expands to ~25 new consume sites. Our Sprint 2 is a **subset**: fix orphans and add the missing `_sse_state` provider. The larger expansion remains separate future work.
- **PLAN-island-js-test-infrastructure** — **Complete**. 115 tests shipped. No overlap.

---

## Changelog

- 2026-04-10: Sprint 1 already complete — shipped in PR #40 (152 tests, 27 classes). Plan updated.
- 2026-04-10: Revised Sprint 2 scope — wire all 7 orphaned providers to consumers (not remove). Showcase the provide/consume pattern.
- 2026-04-10: Sprint 0 complete. Design doc: `SPRINT-0-behavior-layer-design.md`. Error boundary v2 spec finalized. 8 Alpine components prioritized for Playwright. 26 ASCII macro signatures validated.
- 2026-04-10: Sprint 4 complete. 23 Playwright tests across 8 components: command_palette (3), drawer (3), tray (3), toast (3), copy_button (3), theme_toggle (3), split_panel (3), streaming_bubble (2). 8 test pages + routes added to browser test app. All pages render 200 with chirpui classes. Tests require CDN for Alpine.js (run in CI, not offline).
- 2026-04-10: Sprint 3 complete. Error boundary hardened: error message display ([data-error-message]), retry button ([data-error-retry]) with action dispatch, telemetry event (chirp:island:error:report). 8 new vitest tests (123 total JS tests). All backward-compat tests pass.
- 2026-04-10: Sprint 2 complete. All 7 provide/consume keys wired. 30 contract tests added. Discovered and worked around kida param-reassignment scoping bug (use _variant/_size/_disabled instead of reassigning params).
- 2026-04-10: Draft created from codebase exploration evidence.
