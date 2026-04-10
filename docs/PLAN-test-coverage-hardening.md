# Epic: Test Coverage Hardening — Close the 27% Gap

**Status**: Draft
**Created**: 2026-04-10
**Target**: 0.3.0
**Estimated Effort**: 18–28h
**Dependencies**: None (all test infrastructure exists)
**Source**: Codebase audit of 188 templates, test suite analysis (1,005 tests, 80% coverage gate)

---

## Why This Matters

chirp-ui has 1,005 tests and an 80% coverage gate — respectable for a pre-alpha component library. But the coverage is **unevenly distributed**: the 137 tested components are well-exercised while 51 components (27%) have zero render tests. Worse, the interactive layer — 21 Alpine.js components and 9 island state helpers — has almost no behavioral testing beyond 8 Playwright test files covering basic modal/dropdown/tab flows.

### Consequences

1. **51 untested components can silently break** — A CSS contract test catches missing classes, but not broken macro signatures, missing slot injection, or wrong HTML structure. A rename in `forms.html` could break `chat_input.html` with no test failure.
2. **Island state helpers are a black box** — 9 JS files (`foundation.js`, `action_queue.js`, `draft_store.js`, `grid_state.js`, etc.) provide the connective tissue between Alpine components and Chirp's server model. Zero unit tests means a batched action could silently drop, a draft could fail to persist, or an error boundary could swallow exceptions — all invisible until a user reports it.
3. **21 Alpine interactions lack browser tests** — `copy_button`, `command_palette`, `drawer`, `toast`, `split_panel`, `theme_toggle`, `sse_status`, and `streaming` all use `x-data` but have no Playwright coverage. Theme persistence, clipboard API, SSE reconnection, and toast auto-dismiss are all untested interactive behaviors.
4. **Provide/consume orphans mask dead code** — 6 providers emit context that nothing consumes. Without tests asserting consumption, these providers could be removed (or broken) without detection. The provide/consume expansion plan (PLAN-provide-consume-expansion.md) adds consumers but doesn't test the orphaned providers' intended behavior.
5. **ASCII component suite is entirely untested** — 19 ASCII/TUI components added in recent sprints have zero render tests, despite having their own variant/size registrations in `validation.py`.

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| Template count vs test count | 51/188 (27%) components have zero render tests | FIXES — Sprints 1-3 add render tests for all 51 |
| `templates/islands/*.js` | 9 JS files, 0 unit tests | FIXES — Sprint 2 adds JS test infrastructure + tests |
| Alpine `x-data` audit | 21 components with `x-data`, only 8 browser test files | FIXES — Sprint 3 adds Playwright tests for 13 untested interactive components |
| Provide/consume audit | 6 orphaned providers, 1 orphaned consumer | MITIGATES — Sprint 1 adds "provider-without-consumer" render tests |
| ASCII component audit | 19 ASCII components, 0 tests | FIXES — Sprint 1 batch covers all ASCII components |
| Coverage config | 80% fail_under, branch coverage enabled | MITIGATES — higher coverage from this work may justify raising threshold to 85% |

### The Fix

Three-phase test expansion: (1) render tests for all 51 untested components, (2) JS unit test infrastructure for island state helpers, (3) Playwright browser tests for untested Alpine interactions. Each phase ships independently and raises the coverage floor.

---

### Invariants

These must remain true throughout or we stop and reassess:

1. **`uv run poe ci` passes at every sprint** — No test additions break existing behavior. Lint, format, CSS contract, ty, and all existing tests must pass.
2. **Tests run without Chirp** — All new tests use the `conftest.py` fixture with stubs. No real Chirp app dependency for unit tests. Browser tests may use bengal-pounce fixtures.
3. **No template changes in this epic** — This is a test-only effort. Template fixes discovered during testing become separate issues, not scope creep.

---

## Target Architecture

### Test file organization (after completion)

```
tests/
  conftest.py                      # Existing Kida env fixture (unchanged)
  test_components.py               # Existing + new render tests for 51 components
  test_ascii_components.py         # Dedicated ASCII suite (19 components)
  test_provide_consume.py          # Existing (add orphan-provider coverage)
  test_css_syntax.py               # Existing (unchanged)
  test_template_css_contract.py    # Existing (unchanged)
  test_transition_tokens.py        # Existing (unchanged)
  test_filters.py                  # Existing (unchanged)
  test_validation.py               # Existing (unchanged)
  test_icons.py                    # Existing (unchanged)
  test_route_tabs.py               # Existing (unchanged)
  js/                              # NEW: JS unit tests
    conftest.py                    # Node/Deno runner fixture
    test_foundation.js             # Event dispatch, state primitives
    test_action_queue.js           # Batching, deduplication
    test_draft_store.js            # localStorage persistence
    test_grid_state.js             # Selection state
    test_error_boundary.js         # Error handling
    test_state_sync.js             # Form input syncing
    test_upload_state.js           # File upload progress
    test_wizard_state.js           # Multi-step state
    test_counter.js                # Simple counter
  browser/                         # Existing + new Playwright tests
    test_alpine_lifecycle.py       # Existing (unchanged)
    test_boosted_nav.py            # Existing (unchanged)
    test_dropdowns.py              # Existing (unchanged)
    test_fill_mode.py              # Existing (unchanged)
    test_fragment_forms.py         # Existing (unchanged)
    test_inline_edit.py            # Existing (unchanged)
    test_modals.py                 # Existing (unchanged)
    test_tabs.py                   # Existing (unchanged)
    test_copy_button.py            # NEW: clipboard API
    test_command_palette.py        # NEW: search/filter/keyboard
    test_drawer.py                 # NEW: open/close/backdrop
    test_toast.py                  # NEW: show/auto-dismiss
    test_theme_toggle.py           # NEW: persistence, cycling
    test_streaming.py              # NEW: bubble state transitions
    test_split_panel.py            # NEW: resize interaction
    test_sse_status.py             # NEW: connection state display
```

### Coverage targets

| Metric | Current | After Sprint 2 | After Sprint 4 |
|--------|---------|----------------|----------------|
| Components with render tests | 137/188 (73%) | 188/188 (100%) | 188/188 (100%) |
| Island JS files with unit tests | 0/9 (0%) | 9/9 (100%) | 9/9 (100%) |
| Alpine x-data components with browser tests | ~8/24 (33%) | ~8/24 (33%) | 21/24 (88%) |
| Total test count | ~1,005 | ~1,150 | ~1,250 |
| Coverage threshold | 80% | 80% (verify headroom) | 85% (raise gate) |

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: test patterns, JS runner, component inventory | 2h | Low | Yes (inventory only) |
| 1 | Render tests for 51 untested components | 6h | Low | Yes |
| 2 | JS unit test infrastructure + island state tests | 5h | Medium | Yes |
| 3 | Playwright browser tests for 8 priority Alpine components | 6h | Medium | Yes |
| 4 | Provide/consume orphan tests + coverage gate raise | 3h | Low | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Lock down test patterns, choose a JS test runner, and produce the final component inventory.

### Task 0.1 — Finalize untested component inventory

Cross-reference all 188 templates against `test_components.py`, `test_ascii_components.py`, and `test_provide_consume.py`. Produce a checklist of exactly which components need tests and what kind (render-only vs interactive).

**Acceptance**: Checklist file at `docs/test-coverage-checklist.md` with every untested component, its category, and target sprint.

### Task 0.2 — Choose JS test runner for island helpers

Evaluate options: Node + vitest, Deno test, or Playwright-based JS evaluation. Key constraint: island helpers use `Alpine.safeData`, `CustomEvent`, and `localStorage` — need DOM-like environment.

**Acceptance**: Decision documented in sprint 0 notes. Runner can execute a trivial `foundation.js` test.

### Task 0.3 — Define render test pattern for batch coverage

Establish a parameterized test pattern for batch-covering components with minimal boilerplate:

```python
@pytest.mark.parametrize("component,call", [
    ("chat_input", '{{ chat_input(name="msg") }}'),
    ("chat_layout", '{% call chat_layout() %}content{% endcall %}'),
    ...
])
def test_component_renders(env, component, call):
    tmpl = env.from_string(f'{{% from "chirpui/{component}.html" import {component} %}}{call}')
    html = tmpl.render()
    assert f"chirpui-{component.replace('_', '-')}" in html or html.strip()
```

**Acceptance**: Pattern renders 3 sample untested components successfully.

---

## Sprint 1: Render Tests for Untested Components

**Goal**: Every one of the 188 components has at least one render test asserting it produces valid HTML with expected BEM classes.

### Task 1.1 — ASCII component render tests (19 components)

Add `test_ascii_components.py` (or extend existing) with render tests for all 19 ASCII components: `ascii_7seg`, `ascii_border`, `ascii_breaker_panel`, `ascii_card`, `ascii_checkbox`, `ascii_fader`, `ascii_knob`, `ascii_modal`, `ascii_radio`, `ascii_sparkline`, `ascii_split_flap`, `ascii_stepper`, `ascii_table`, `ascii_tabs`, `ascii_ticker`, `ascii_tile_btn`, `ascii_toggle`, `ascii_vu_meter`.

**Files**: `tests/test_ascii_components.py`
**Acceptance**: `uv run pytest tests/test_ascii_components.py -q` passes with 19+ tests. `rg 'def test_' tests/test_ascii_components.py | wc -l` >= 19.

### Task 1.2 — Chat/messaging component render tests (9 components)

Add render tests for: `channel_card`, `chat_input`, `chat_layout`, `comment`, `mention`, `conversation_item`, `conversation_list`, `message_bubble`, `message_thread`.

**Files**: `tests/test_components.py` (extend existing TestChat class or add new)
**Acceptance**: `uv run pytest tests/test_components.py -k "chat or comment or mention or conversation or message" -q` passes.

### Task 1.3 — Interactive component render tests (10 components)

Render-only tests (no browser) for: `command_bar`, `command_palette`, `dnd`, `infinite_scroll`, `playlist`, `rune_field`, `search_header`, `selection_bar`, `share_menu`, `sortable_list`.

**Files**: `tests/test_components.py`
**Acceptance**: Each component has at least one render test producing non-empty HTML.

### Task 1.4 — Specialty component render tests (13 components)

Render tests for: `chapter_list`, `entity_header`, `holy_light`, `label_overline`, `live_badge`, `oob`, `post_card`, `profile_header`, `reaction_pill`, `resource_index`, `shell_frame`, `symbol_rain`, `theme_toggle`, `tabbed_page_layout`, `typing_indicator`.

**Files**: `tests/test_components.py`
**Acceptance**: `uv run poe ci` passes. All 188 components now have at least one test.

---

## Sprint 2: JS Unit Test Infrastructure + Island State Tests

**Goal**: Establish JS unit testing for island state helpers and cover all 9 files.

### Task 2.1 — Set up JS test runner

Install and configure the chosen runner (from Sprint 0). Add a `test:js` script to `pyproject.toml` or `Makefile`. Ensure CI runs JS tests alongside Python tests.

**Files**: `pyproject.toml` or `Makefile`, `tests/js/`
**Acceptance**: `make test-js` (or equivalent) runs and passes with at least one test.

### Task 2.2 — `foundation.js` tests

Test the core event dispatch system: `chirp:island:state`, `chirp:island:action`, `chirp:island:error` events. Verify event payloads, bubbling, and error handling.

**Files**: `tests/js/test_foundation.js`
**Acceptance**: All foundation.js public functions have at least one test. Event dispatch verified.

### Task 2.3 — `action_queue.js` tests

Test action batching, deduplication, and queue draining. Verify that duplicate actions are collapsed and ordering is preserved.

**Files**: `tests/js/test_action_queue.js`
**Acceptance**: Tests cover: enqueue, dedup, batch flush, empty queue.

### Task 2.4 — Remaining island helper tests (7 files)

Cover `counter.js`, `draft_store.js`, `error_boundary.js`, `grid_state.js`, `state_sync.js`, `upload_state.js`, `wizard_state.js`.

**Files**: `tests/js/test_*.js`
**Acceptance**: `make test-js` passes. Each helper file has at least 2 tests covering primary behavior + edge case.

---

## Sprint 3: Playwright Browser Tests for Alpine Components

**Goal**: Add behavioral tests for the 8 highest-priority untested Alpine interactions.

### Task 3.1 — `copy_button` clipboard test

Test: click copies content, "Copied!" feedback appears, resets after timeout.

**Files**: `tests/browser/test_copy_button.py`
**Acceptance**: Playwright test passes. Clipboard API mocked or granted.

### Task 3.2 — `command_palette` keyboard + search test

Test: Cmd+K opens palette, typing filters results, Enter selects, Escape closes.

**Files**: `tests/browser/test_command_palette.py`
**Acceptance**: 3+ test functions covering open/filter/select/close.

### Task 3.3 — `drawer` open/close/backdrop test

Test: drawer opens via trigger, backdrop click closes, escape closes, focus trap works.

**Files**: `tests/browser/test_drawer.py`
**Acceptance**: Tests cover open, close-via-backdrop, close-via-escape.

### Task 3.4 — `toast` lifecycle test

Test: toast appears, auto-dismisses after timeout, manual dismiss works.

**Files**: `tests/browser/test_toast.py`
**Acceptance**: Tests cover show, auto-dismiss timing, manual dismiss.

### Task 3.5 — `theme_toggle` persistence test

Test: toggle cycles light/dark/system, persists to localStorage, survives page reload.

**Files**: `tests/browser/test_theme_toggle.py`
**Acceptance**: Tests verify localStorage write and read-on-load.

### Task 3.6 — `streaming`, `split_panel`, `sse_status` tests

Cover remaining priority interactive components.

**Files**: `tests/browser/test_streaming.py`, `test_split_panel.py`, `test_sse_status.py`
**Acceptance**: Each file has 2+ tests. `uv run pytest tests/browser/ -q` passes.

---

## Sprint 4: Orphan Coverage + Gate Raise

**Goal**: Test orphaned provide/consume pairs and raise the coverage threshold.

### Task 4.1 — Orphaned provider render tests

Add tests verifying that the 6 orphaned providers (`_card_variant`, `_surface_variant`, `_bar_surface`, `_bar_density`, `_streaming_role`, `_suspense_busy`) emit `{% provide %}` blocks that future consumers can read. This proves the infrastructure works even before consumers are implemented.

**Files**: `tests/test_provide_consume.py`
**Acceptance**: 6 new tests pass. Each verifies the provide block exists in rendered output context.

### Task 4.2 — Orphaned consumer test

Test `_sse_state` consumption in `sse_retry()` with manually provided context.

**Files**: `tests/test_provide_consume.py`
**Acceptance**: Test passes with manual `{% provide _sse_state = "error" %}` wrapper.

### Task 4.3 — Raise coverage gate

If overall coverage exceeds 85% after Sprints 1-3, raise `fail_under` from 80 to 85 in `pyproject.toml`.

**Files**: `pyproject.toml`
**Acceptance**: `uv run pytest --cov --cov-fail-under=85` passes.

### Task 4.4 — Remove test coverage checklist

Delete `docs/test-coverage-checklist.md` (Sprint 0 artifact) now that all items are addressed.

**Acceptance**: Checklist file removed. `uv run poe ci` passes.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| JS test runner adds heavy dev dependency | Medium | Low | Choose lightweight runner (vitest or Deno); keep in `[dev]` extras only |
| Batch render tests are shallow (catch render, miss semantics) | Medium | Medium | Sprint 0 Task 0.3 establishes pattern with BEM class assertions, not just "renders without error" |
| Playwright tests flaky in CI (timing, browser version) | Medium | Medium | Use `expect(locator).to_be_visible()` patterns with auto-retry; pin Playwright version |
| Template changes between sprint 0 and sprint 1 invalidate inventory | Low | Low | Inventory is a snapshot; re-verify against glob before each sprint |
| Island JS helpers depend on Alpine internals not available in test env | Medium | High | Sprint 0 Task 0.2 validates runner can load Alpine. If blocked, test pure logic only (action_queue, counter, etc.) |

---

## Success Metrics

| Metric | Current | After Sprint 2 | After Sprint 4 |
|--------|---------|----------------|----------------|
| Components with render tests | 137/188 (73%) | 188/188 (100%) | 188/188 (100%) |
| Island JS unit tests | 0 | 20+ | 20+ |
| Browser test files | 8 | 8 | 16 |
| Total test count | ~1,005 | ~1,150 | ~1,250 |
| Coverage gate | 80% | 80% | 85% |
| Provide/consume pairs fully tested | 5/11 | 5/11 | 11/11 |

---

## Relationship to Existing Work

- **PLAN-provide-consume-expansion.md** — parallel — that plan adds consumers; this plan tests the existing (orphaned) providers. Sprint 4 here complements Sprint 1-4 there.
- **PLAN-ascii-maturity.md** — complete — ASCII components exist but lack tests. Sprint 1 Task 1.1 closes that gap.
- **PLAN-streaming-maturity.md** — parallel — streaming browser tests (Sprint 3) validate the streaming component behavior that plan refines.
- **PLAN-chirpui-alpine-migration.md** — independent — JS test infrastructure (Sprint 2) will be useful when Alpine migration adds new interactive behaviors.

---

## Changelog

- **2026-04-10** — Sprint 0+1 complete. Actual inventory: 33 untested components (not 51 — ASCII suite already had 152 tests). All 33 now covered in `tests/test_coverage_sprint1.py` (72 tests). `app_layout` excluded (requires Chirp). Total: 1062 tests passing, CI green.
- **2026-04-10** — Draft created from codebase audit (51 untested components, 0 JS tests, 21 untested Alpine interactions)
