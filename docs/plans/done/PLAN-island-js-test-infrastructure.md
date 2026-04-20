# Epic: Island JS Test Infrastructure — Unit Tests for the Interactive Spine

**Status**: Complete
**Created**: 2026-04-10
**Target**: 0.3.0
**Estimated Effort**: 10–16h
**Dependencies**: Node.js or Deno runtime available in CI; foundation.js must remain the sole dependency for island helpers
**Source**: Codebase audit — 9 island state helpers (525 LOC), 0 unit tests, 0 test infrastructure; PLAN-test-coverage-hardening.md Sprint 2 (not yet started)

---

## Why This Matters

The 9 island state helpers (`foundation.js`, `action_queue.js`, `counter.js`, `draft_store.js`, `error_boundary.js`, `grid_state.js`, `state_sync.js`, `upload_state.js`, `wizard_state.js`) are the connective tissue between Alpine.js components and Chirp's server model. They manage action batching, draft persistence, multi-step wizard state, file upload progress, grid selection, URL synchronization, and error boundaries. Every interactive island in chirp-ui depends on this layer — and it has **zero tests and zero test infrastructure**.

1. **Zero coverage on 525 lines of stateful JS** — A broken `action_queue.js` silently drops batched actions; a broken `draft_store.js` loses user input to localStorage failures; a broken `wizard_state.js` skips steps or traps users. All invisible until end-user reports.
2. **No JS test runner in the project** — chirp-ui has a mature Python test suite (1,062 tests, 80% coverage gate) but no mechanism to test JavaScript. Adding the first JS test requires solving runner selection, DOM mocking, CI integration, and the `foundation.js` dependency chain.
3. **Foundation.js is a shared dependency with no contract tests** — All 8 other helpers import from `foundation.js` (readProps, setState, setAction, setError, registerPrimitive). If foundation's event dispatch or cleanup semantics change, every helper breaks silently.
4. **Helpers use browser APIs that need careful mocking** — localStorage (draft_store), URL/history.replaceState (state_sync), setInterval (upload_state), CustomEvent (foundation, error_boundary). Without a DOM-like environment, these are untestable; with one, we need to validate the mocking doesn't mask real bugs.
5. **Blocks PLAN-test-coverage-hardening Sprint 2** — The existing test coverage plan explicitly depends on JS test infrastructure existing. Until this is solved, Sprint 2 (and the path to 85% coverage gate) is blocked.

### Evidence

| Layer/Source | Key Finding | Proposal Impact |
|-------------|-------------|-----------------|
| `templates/islands/*.js` | 9 files, 525 LOC, 0 tests | FIXES — Sprint 1-3 add tests for all 9 files |
| `tests/js/` | Directory does not exist | FIXES — Sprint 0-1 create infrastructure |
| `foundation.js` | 7 public functions used by all 8 helpers | FIXES — Sprint 1 adds contract tests for all 7 |
| `draft_store.js` | localStorage read/write + 250ms debounce + JSON parse error handling | FIXES — Sprint 2 tests persistence, debounce, and error recovery |
| `wizard_state.js` | Step navigation with boundary guards + data-step-id resolution | FIXES — Sprint 2 tests state machine transitions and edge cases |
| `upload_state.js` | setInterval-based progress simulation (120ms, +15 per tick) | FIXES — Sprint 2 tests timer lifecycle and progress math |
| `state_sync.js` | URL query param sync via history.replaceState | FIXES — Sprint 3 tests URL state management |
| `error_boundary.js` | CustomEvent listener with complex id/name filtering | FIXES — Sprint 3 tests event filtering logic |
| `grid_state.js` | DOM reordering via appendChild + Set-based selection + filter | FIXES — Sprint 3 tests sort/filter/select interactions |
| PLAN-test-coverage-hardening | Sprint 2 blocked on JS test infrastructure | FIXES — Unblocks Sprint 2-4 of that plan |

### Invariants

These must remain true throughout or we stop and reassess:

1. **No production JS changes in this epic**: This is test-only. No modifications to `templates/islands/*.js`. If bugs are discovered, they become separate issues.
2. **`uv run poe ci` passes at every sprint**: JS test failures don't break the Python CI gate. JS tests run as a separate target (`make test-js`) that CI calls alongside Python tests.
3. **Tests run without a browser**: Unit tests use jsdom or Deno's DOM shim — no Playwright, no headless Chrome. Browser integration tests belong in `tests/browser/`.

---

## Target Architecture

### Test file organization (after completion)

```
tests/
  js/
    setup.js              # DOM environment setup (jsdom or Deno shim)
    helpers.js            # Mock factories: localStorage, CustomEvent, Alpine.safeData
    test_foundation.js    # 7 public functions × 2-3 tests each = ~18 tests
    test_action_queue.js  # Mount, click→pending→success/error, cleanup = ~8 tests
    test_counter.js       # Seed, increment, decrement, numeric coercion = ~6 tests
    test_draft_store.js   # Save, restore, debounce, JSON error, missing fields = ~10 tests
    test_error_boundary.js # Error show/hide, event filtering, reset = ~8 tests
    test_grid_state.js    # Filter, sort toggle, select/deselect, DOM reorder = ~10 tests
    test_state_sync.js    # URL read, URL write, multi-input sync, empty value = ~8 tests
    test_upload_state.js  # No-file error, progress ticks, completion, cleanup = ~8 tests
    test_wizard_state.js  # Next/prev, boundary guards, step ID resolution = ~8 tests
  # Total: ~84 JS unit tests
```

### Build integration

```
Makefile:
  test-js:    # runs vitest (or deno test) on tests/js/
  test:       # existing Python tests
  ci:         # existing lint+format+css+ty+test, now also calls test-js

pyproject.toml:
  [tool.poe.tasks]
  ci = "... && make test-js"  # or separate poe task
```

### Dependency budget

| Package | Purpose | Dev-only? |
|---------|---------|-----------|
| vitest | Test runner + assertion library | Yes |
| jsdom | DOM environment for Node | Yes |
| **OR** Deno | Runtime with built-in test runner + DOM | Yes (no npm) |

Decision made in Sprint 0. Deno preferred if `deno test` can load ES modules with `window.chirpIslands` global; vitest if Alpine.safeData mocking needs deeper jsdom integration.

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: runner selection, mock strategy, foundation.js contract | 2h | Low | Yes (decision doc only) |
| 1 | Infrastructure + foundation.js tests | 3–4h | Medium | Yes |
| 2 | Pure-logic helpers: counter, draft_store, wizard_state, upload_state | 3–5h | Low | Yes |
| 3 | DOM-heavy helpers: action_queue, error_boundary, grid_state, state_sync | 3–5h | Medium | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Choose a JS test runner, design the mock strategy, and validate that foundation.js can be loaded and tested outside a browser.

### Task 0.1 — Runner evaluation

Test both options:
- **vitest + jsdom**: `npm init -y && npm i -D vitest jsdom`, write a trivial test that imports `foundation.js` and calls `readProps({})`.
- **Deno test**: `deno test` with `--config` for DOM shim, same trivial test.

Evaluate: ES module compatibility, `window`/`document` globals, timer mocking (`vi.useFakeTimers()` vs `Deno.test` with `FakeTime`), CI integration complexity.

**Acceptance**: One runner successfully imports `foundation.js`, calls `readProps({})`, and asserts the return value. Decision documented in this plan's changelog.

### Task 0.2 — Mock strategy design

Island helpers depend on:
- `window.chirpIslands.register()` — called by `registerPrimitive()`
- `Alpine.safeData()` — not directly used by helpers but expected by Chirp
- `localStorage` — used by draft_store
- `history.replaceState()` — used by state_sync
- `CustomEvent` + `document.dispatchEvent()` — used by foundation, error_boundary
- `setTimeout` / `setInterval` — used by action_queue (450ms), draft_store (250ms), upload_state (120ms)

Design mock factories for each. Decide: stub per-test or global setup?

**Acceptance**: `tests/js/helpers.js` exports `mockLocalStorage()`, `mockChirpIslands()`, `createPayload(element)`. Each returns a teardown function.

### Task 0.3 — Foundation.js contract definition

List the 7 public functions with their exact signatures and behavioral contracts:

| Function | Inputs | Outputs/Side Effects | Contract |
|----------|--------|---------------------|----------|
| `readProps(payload)` | `{props: {...}}` or `{}` | Returns props object or `{}` | Never throws; always returns object |
| `attachCleanup(payload, fn)` | payload with element, function | WeakMap entry | Cleanup callable exactly once |
| `runCleanup(payload)` | payload with element | Invokes + deletes cleanup | No-op if no cleanup registered |
| `setState(payload, api, state)` | payload, optional api, state obj | Event dispatch or api.emitState() | Prefers api; falls back to CustomEvent |
| `setAction(payload, api, action, status, extra)` | payload, optional api, action details | Event or api.emitAction() | Same preference as setState |
| `setError(payload, api, reason, extra)` | payload, optional api, error details | Event or api.emitError() | Same preference as setState |
| `registerPrimitive(name, adapter)` | string, function | Registers with window.chirpIslands | Throws if registry missing |

**Acceptance**: Contract table written. Each row has at least one test case sketched.

---

## Sprint 1: Infrastructure + Foundation Tests

**Goal**: Ship a working JS test runner with ~18 tests covering foundation.js — proving the infrastructure works and testing the shared dependency first.

### Task 1.1 — Set up test runner

Install chosen runner (from Sprint 0). Create:
- `tests/js/setup.js` — DOM environment initialization
- `tests/js/helpers.js` — mock factories from Sprint 0 Task 0.2
- `Makefile` target `test-js`
- CI integration (add `make test-js` to `poe ci` or equivalent)

**Files**: `Makefile`, `tests/js/setup.js`, `tests/js/helpers.js`, `package.json` (if vitest)
**Acceptance**: `make test-js` runs and exits 0 with at least one passing test.

### Task 1.2 — readProps + registerPrimitive tests

Test the two "structural" functions:
- `readProps({})` → `{}`
- `readProps({props: {seed: 5}})` → `{seed: 5}`
- `readProps(null)` → `{}` (or throws — verify actual behavior)
- `registerPrimitive("foo", fn)` → `window.chirpIslands.register` called with correct args
- `registerPrimitive("foo", fn)` without registry → throws

**Files**: `tests/js/test_foundation.js`
**Acceptance**: 5+ tests pass.

### Task 1.3 — Cleanup lifecycle tests

Test the WeakMap-based cleanup system:
- `attachCleanup` + `runCleanup` → cleanup function called once
- Double `runCleanup` → no-op (no error, no double-call)
- `runCleanup` without prior `attachCleanup` → no-op
- Cleanup with different payload elements → independent

**Files**: `tests/js/test_foundation.js`
**Acceptance**: 4+ tests pass.

### Task 1.4 — Event emission tests (setState, setAction, setError)

Test the dual-path emission (api object vs CustomEvent fallback):
- With api object: `setState(payload, {emitState: spy}, {count: 1})` → spy called
- Without api: `setState(payload, null, {count: 1})` → CustomEvent dispatched on document
- Event detail contains sanitized payload info (safeDetail)
- setAction includes action name and status in event detail
- setError includes reason in event detail

**Files**: `tests/js/test_foundation.js`
**Acceptance**: 9+ tests pass. `make test-js` shows 18+ total tests. `uv run poe ci` still passes.

---

## Sprint 2: Pure-Logic Helpers

**Goal**: Test the 4 helpers with the most self-contained logic — counter, draft_store, wizard_state, upload_state. These have clear state machines and minimal DOM interaction beyond their own container.

### Task 2.1 — counter.js tests

Test the simplest helper to validate the mount→render→action pattern:
- Mount with seed=0 → state {count: 0}
- Mount with seed=5 → state {count: 5}
- Seed as string "3" → state {count: 3} (Number coercion)
- Seed as non-numeric → state {count: 0} (NaN → 0)
- Increment → count + 1, setAction("increment", "success")
- Decrement → count - 1, setAction("decrement", "success")

**Files**: `tests/js/test_counter.js`
**Acceptance**: 6+ tests pass.

### Task 2.2 — draft_store.js tests

Test localStorage persistence with debouncing:
- Mount with existing localStorage key → fields restored, state.restored = true
- Mount with no localStorage key → state.restored = false
- Input event → 250ms debounce → localStorage write with JSON structure `{savedAt, data}`
- Rapid inputs → only last value persisted (debounce cancels previous)
- Corrupted localStorage JSON → graceful recovery (no throw, state.restored = false)
- Field extraction uses `name` attr, falls back to `data-draft-field`

**Files**: `tests/js/test_draft_store.js`
**Acceptance**: 10+ tests pass. Uses fake timers for debounce testing.

### Task 2.3 — wizard_state.js tests

Test the multi-step state machine:
- Mount with 3 step nodes → state {step: id, index: 0, total: 3}
- Step ID from data-step-id, fallback to index
- Next: index 0→1, correct step shown, others hidden
- Prev: index 1→0, correct step shown
- Boundary: next at last step → no-op (index stays at total-1)
- Boundary: prev at first step → no-op (index stays at 0)
- Prev button disabled at index 0; Next button disabled at last index
- Action emitted with step ID on navigation

**Files**: `tests/js/test_wizard_state.js`
**Acceptance**: 8+ tests pass.

### Task 2.4 — upload_state.js tests

Test the interval-based progress simulation:
- Mount + trigger with no files → error action "no_files"
- Mount + trigger with files → pending action, interval starts
- Progress increments by 15 every 120ms, capped at 100
- Progress 100 → interval cleared, success action, button re-enabled
- Cleanup → clearInterval called

**Files**: `tests/js/test_upload_state.js`
**Acceptance**: 8+ tests pass. Uses fake timers for interval testing. `make test-js` shows 50+ total tests.

---

## Sprint 3: DOM-Heavy Helpers

**Goal**: Test the 4 helpers with significant DOM interaction — action_queue, error_boundary, grid_state, state_sync. These require richer DOM setup and event simulation.

### Task 3.1 — action_queue.js tests

Test the click→delay→result flow:
- Mount initializes with "idle" status
- Click trigger → button disabled, "pending" status
- 450ms later → "success" or "error" based on data-action-fail
- data-action-fail="true" → error path
- Button re-enabled after completion
- Cleanup removes event listener

**Files**: `tests/js/test_action_queue.js`
**Acceptance**: 8+ tests pass. Uses fake timers.

### Task 3.2 — error_boundary.js tests

Test error event filtering and recovery:
- "chirp:island:error" event with matching id → fallback shown, body hidden
- "chirp:island:error" event with non-matching id → no change
- Reset button click → body restored, fallback hidden, state = "healthy"
- Initial state is "healthy"
- Cleanup removes document event listener

**Files**: `tests/js/test_error_boundary.js`
**Acceptance**: 8+ tests pass.

### Task 3.3 — grid_state.js tests

Test filter, sort, and selection:
- Filter input → rows with non-matching text hidden
- Filter is case-insensitive and trims whitespace
- Sort toggle → rows reordered by localeCompare, state.sort flips asc/desc
- Checkbox click → added to state.selected Set
- Checkbox uncheck → removed from Set
- Render syncs checkbox checked state with Set
- Empty filter → all rows visible

**Files**: `tests/js/test_grid_state.js`
**Acceptance**: 10+ tests pass.

### Task 3.4 — state_sync.js tests

Test URL↔input synchronization:
- Mount reads initial value from URL query param
- Mount falls back to props.initial if no query param
- Input change → URL updated via replaceState
- Empty input → query param removed
- Multiple inputs stay synchronized
- Cleanup removes all input event listeners

**Files**: `tests/js/test_state_sync.js`
**Acceptance**: 8+ tests pass. `make test-js` shows ~84 total tests. `uv run poe ci` passes.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| JS test runner adds heavy node_modules to repo | Medium | Low | **RESOLVED** — vitest + jsdom installed; node_modules in .gitignore |
| Island helpers import foundation.js via absolute server path `/static/islands/` | Medium | Medium | **RESOLVED** — vitest `resolve.alias` maps `/static/islands` → source directory |
| jsdom doesn't support `CustomEvent` constructor correctly | Low | High | **RESOLVED** — Sprint 0 confirmed CustomEvent dispatch works on both document and window |
| Fake timers interact badly with async event dispatch | Medium | Medium | Use synchronous patterns where possible; test timer helpers in isolation before combining with events |
| `window.chirpIslands` global not initialized in test env | High | Low | Sprint 0 Task 0.2 creates `mockChirpIslands()` factory. Every test calls it in setup. |
| Tests are shallow — mock too much, miss real integration bugs | Medium | Medium | Sprint 3 helpers use real DOM operations (appendChild, hidden attribute) not mocked; mocks limited to external APIs (localStorage, URL, timers) |

---

## Success Metrics

| Metric | Current | After Sprint 1 | After Sprint 3 |
|--------|---------|----------------|----------------|
| Island JS files with unit tests | 0/9 (0%) | 1/9 (11%) | 9/9 (100%) |
| JS unit test count | 0 | ~18 | ~84 |
| JS test runner exists | No | Yes | Yes |
| CI runs JS tests | No | Yes | Yes |
| Foundation.js public functions tested | 0/7 | 7/7 | 7/7 |
| Helpers with timer/async coverage | 0/4 | 0/4 | 4/4 (action_queue, draft_store, upload_state, state_sync) |

---

## Relationship to Existing Work

- **PLAN-test-coverage-hardening.md** — prerequisite for Sprint 2 — that plan's Sprint 2 ("JS unit test infrastructure + island state tests") is exactly this epic, extracted into a standalone plan with more design rigor. Completing this unblocks Sprints 3-4 of that plan.
- **PLAN-streaming-maturity.md** — complete — streaming components are tested at the template level; island helpers provide the interactive layer underneath. No overlap.
- **PLAN-ascii-maturity.md** — independent — ASCII components don't use island helpers.
- **PLAN-provide-consume-expansion.md** — independent — provide/consume is template-time context; island helpers are runtime JS state. Orthogonal.

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-10 | Sprint 3 complete — EPIC DONE | action_queue (9), error_boundary (11), grid_state (13), state_sync (11) = 44 new tests. Total: 115 JS tests across 9 files. All 9 island helpers tested. jsdom SecurityError for replaceState resolved via spy. |
| 2026-04-10 | Sprint 2 complete | counter (11), draft_store (10), wizard_state (14), upload_state (11) = 46 new tests. Total: 71 JS tests across 5 files. Fake timers validated for debounce (250ms), interval (120ms), and async delay (450ms). |
| 2026-04-10 | Sprint 1 complete | 25 foundation.js tests (all 7 public functions), 2 counter smoke tests = 27 total JS tests passing |
| 2026-04-10 | Sprint 0 complete | See findings below |
| 2026-04-10 | Draft created | Extracted from PLAN-test-coverage-hardening Sprint 2; expanded with per-helper analysis, mock strategy, and foundation.js contract |

---

## Sprint 0 Findings

### 0.1 — Runner Decision: vitest + jsdom

**Winner: vitest 4.1.4 + jsdom** (Node v25.8.1)

Deno was not available on this system. vitest was validated against all critical requirements:

| Requirement | Result |
|-------------|--------|
| ES module import of foundation.js | Pass — native ESM |
| Path alias for `/static/islands` → `src/chirp_ui/templates/islands` | Pass — vitest `resolve.alias` |
| `CustomEvent` dispatch on document and window | Pass — jsdom supports CustomEvent |
| `WeakMap` for cleanup tracking | Pass — native V8 |
| `window.chirpIslands` global mocking | Pass — simple object assignment |
| `vi.useFakeTimers()` for debounce/interval | Available — not yet tested in Sprint 0 |
| CI integration via `make test-js` | Pass — `npx vitest run` |

**Config**: `vitest.config.js` at project root. Tests in `tests/js/**/*.test.js`.
**Naming**: vitest convention `*.test.js` (not Python `test_*.js`).

### 0.2 — Mock Strategy

Four mock factories in `tests/js/helpers.js`:

| Factory | Purpose | Teardown |
|---------|---------|----------|
| `mockChirpIslands()` | Stubs `window.chirpIslands.register()` — needed because every helper calls `registerPrimitive()` at module load | Deletes `window.chirpIslands` |
| `mockLocalStorage()` | Map-backed localStorage with vi.fn() spies — needed by draft_store | Clears map |
| `createPayload(element, props, overrides)` | Builds a standard island payload with sensible defaults | N/A (pure) |
| `createMockApi()` | Returns `{ emitState, emitAction, emitError }` as vi.fn() spies | N/A (pure) |

**Key insight**: Island helpers import foundation.js at module level, which means `registerPrimitive()` runs during `import`. The `mockChirpIslands()` factory MUST be called before any helper is imported. In vitest, dynamic `await import()` handles this.

### 0.3 — Foundation.js Contract

7 exported functions, all validated with 9 passing tests:

| Function | Signature | Contract | Tested? |
|----------|-----------|----------|---------|
| `readProps(payload)` | `{props?} → Object` | Returns `payload.props` if object; else `{}`. Never throws on null/undefined. | Yes (3 tests) |
| `attachCleanup(payload, fn)` | `{element}, Function → void` | Stores cleanup fn in WeakMap keyed to `payload.element`. No-op if payload/element/fn invalid. | Sprint 1 |
| `runCleanup(payload)` | `{element} → void` | Runs + deletes stored cleanup. No-op if none registered. | Sprint 1 |
| `setState(payload, api, state)` | `payload, api?, Object → void` | If `api.emitState` exists, calls it. Otherwise dispatches `"chirp:island:state"` CustomEvent on both `document` and `window`. Detail includes `safeDetail(payload)` + state. | Yes (2 tests) |
| `setAction(payload, api, action, status, extra)` | `payload, api?, String, String, Object? → void` | Same api/event pattern as setState. Detail includes action, status, and extra. | Sprint 1 |
| `setError(payload, api, reason, extra)` | `payload, api?, String, Object? → void` | Same api/event pattern. Detail includes `error: "primitive"` + reason. | Sprint 1 |
| `registerPrimitive(name, adapter)` | `String, Object → void` | Calls `window.chirpIslands.register(name, adapter)`. Throws if registry missing. | Yes (2 tests) |

**`safeDetail(payload)`** (private): Extracts only `{ name, id, version }` from payload — prevents leaking element refs or props into event detail.

### Helper Import Dependency Map

All 8 non-foundation helpers import the same 3-4 functions:

| Helper | readProps | setState | setAction | setError | registerPrimitive |
|--------|-----------|----------|-----------|----------|-------------------|
| action_queue | x | x | x | | x |
| counter | x | x | x | | x |
| draft_store | x | x | x | | x |
| error_boundary | x | x | | | x |
| grid_state | x | x | x | | x |
| state_sync | x | x | | | x |
| upload_state | x | x | x | | x |
| wizard_state | x | x | x | | x |

No helper uses `setError`, `attachCleanup`, or `runCleanup` directly. These are available for user-authored island primitives.
