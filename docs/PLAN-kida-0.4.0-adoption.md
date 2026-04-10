# Epic: Kida 0.4.0 Feature Adoption — Render Safety & Expression Ergonomics

**Status**: Complete
**Created**: 2026-04-10
**Target**: chirp-ui 0.3.0
**Estimated Effort**: 8–14h
**Dependencies**: kida-templates ≥ 0.4.0 (bumped in this branch)
**Source**: kida 0.4.0 release notes + codebase analysis of 188 templates

---

## Why This Matters

Kida 0.4.0 ships native error boundaries, scoped slots, list comprehensions, and a compile-time partial evaluator. chirp-ui renders user-provided content through slots and `| safe` filters across 188 templates — any render-time exception currently crashes the entire page or silently swallows OOB swaps.

**Concrete consequences:**

1. **5 OOB-critical templates** (`oob.html`, `toast.html`, `streaming.html`, `fragment_island.html`, `sse_status.html`) produce zero visual feedback when slot content fails to render — notifications and live updates silently vanish.
2. **11 templates** accept arbitrary `caller()` content with no render guard — a broken slot caller crashes the host component.
3. **9 templates** use `| safe` on user-provided attributes — malformed input produces broken HTML rather than a graceful fallback.
4. **4 templates** have 3–5 chained ternary expressions for class assembly (worst: `layout.html` grid with 5 nested chains) — hard to read, easy to break.
5. Provide/consume (33 files) is the correct pattern for deep context propagation and does not need migration to scoped slots.

**The fix:** Adopt `{% try %}` error boundaries on the highest-risk render paths, use list comprehensions to simplify class assembly where it's gnarly, and document scoped slots + partial evaluator for downstream adopters.

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| OOB templates | 5 templates silently fail on bad slot content | FIXES — Sprint 1 wraps in `{% try %}` |
| caller() templates | 11 accept arbitrary content, no guard | FIXES — Sprint 1 targets highest-risk 4 |
| `\| safe` filters | 9 templates pass user data through `\| safe` | MITIGATES — `{% try %}` catches render crash, not injection |
| Class ternary chains | 4 templates with 3–5 chains | FIXES — Sprint 2 uses list comprehensions |
| Provide/consume (33 files) | All use deep cross-macro propagation | UNRELATED — correct pattern, no migration needed |
| Scoped slots | No current inversion-of-control patterns | UNRELATED — document for future use |
| Partial evaluator | Opt-in compile-time optimization | MITIGATES — Chirp controls Environment; chirp-ui documents the flag |

### Invariants

These must remain true throughout or we stop and reassess:

1. **All 1085 tests pass**: no regressions from error boundary wrapping or expression changes.
2. **Template CSS contract holds**: `test_template_css_contract.py` stays green — no class name drift.
3. **No behavior change on the happy path**: `{% try %}` blocks are invisible when content renders successfully; list comprehensions produce identical class strings.

---

## Target Architecture

```
Before (0.3.4):
  slot content → render error → page crash / silent OOB loss

After (0.4.0):
  slot content → {% try %} → render error → {% fallback %} → graceful skeleton/empty/message
                           → success     → normal output (zero overhead)
```

**Error boundary placement tiers:**

| Tier | Where | Fallback strategy |
|------|-------|-------------------|
| **Critical** | OOB fragments, toast, streaming | Empty string (OOB swap still arrives, just empty) |
| **Visible** | suspense_slot, resource_index, metric_grid | Default skeleton |
| **Slot guards** | Any `{% slot %}` inside `caller()`-accepting macros | Omit the slot region |

**List comprehension targets:**

| Template | Current | After |
|----------|---------|-------|
| `layout.html` grid | 5 nested `{% if %}` chains | `[cls for cls in [...] if cls] \| join(" ")` |
| `layout.html` frame/stack/cluster | 3–4 chains each | Same pattern |

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Bump + suspense_slot boundary + docs | 2h | Low | Yes ✅ |
| 1 | Error boundaries on OOB-critical + high-risk templates | 4–6h | Medium | Yes ✅ |
| 2 | List comprehension cleanup in layout.html | 2–3h | Low | Yes ✅ |
| 3 | Document scoped slots + partial evaluator for adopters | 1–2h | Low | Yes ✅ |

---

## Sprint 0: Bump & First Boundary ✅

**Goal**: Bump kida dep, prove error boundaries work in chirp-ui, update CLAUDE.md.

**Done in this branch:**

### Task 0.1 — Bump kida-templates to ≥ 0.4.0

**Files**: `pyproject.toml`, `uv.lock`, `README.md`
**Acceptance**: `uv run python -c "import kida; print(kida.__version__)"` prints `0.4.0`

### Task 0.2 — Error boundary in suspense_slot

**Files**: `src/chirp_ui/templates/chirpui/suspense.html`
**Acceptance**: `uv run pytest tests/test_components.py::TestSuspense -q` — 12 tests pass including new `test_suspense_slot_error_boundary_fallback`

### Task 0.3 — Document kida 0.4.0 features in CLAUDE.md

**Files**: `CLAUDE.md`
**Acceptance**: CLAUDE.md contains entries for error boundaries, scoped slots, list comprehensions

---

## Sprint 1: Error Boundaries on Critical Render Paths ✅

**Goal**: Wrap OOB-critical and high-risk slot content in `{% try %}` so render errors produce graceful fallbacks instead of silent failures or page crashes.

### Task 1.1 — OOB templates: oob.html

Wrap `oob_fragment()` slot content and `oob_toast()` body in `{% try %}`. Fallback: empty content (the OOB swap still arrives with the correct `id` and `hx-swap-oob`, just empty — better than no swap at all).

**Files**: `src/chirp_ui/templates/chirpui/oob.html`
**Acceptance**: New test renders `oob_fragment` with broken caller content → still produces `hx-swap-oob` wrapper div.

### Task 1.2 — Streaming templates: streaming.html

Wrap `streaming_bubble()` and `streaming_block()` slot content in `{% try %}`. Fallback: render the container with an error-state class (`chirpui-streaming--error`) so CSS can style it.

**Files**: `src/chirp_ui/templates/chirpui/streaming.html`, `src/chirp_ui/templates/chirpui.css`
**Acceptance**: New test renders streaming_bubble with broken slot content → produces container with `chirpui-streaming--error` class.

### Task 1.3 — Toast: toast.html

Wrap toast body in `{% try %}`. Fallback: render the toast shell with a generic "Notification" message so the user sees *something*.

**Files**: `src/chirp_ui/templates/chirpui/toast.html`
**Acceptance**: New test renders toast with broken slot → produces toast element with fallback text.

### Task 1.4 — Fragment island: fragment_island.html

Wrap the main `{% slot %}` in fragment_island and fragment_island_form in `{% try %}`. Fallback: empty content in the `aria-live` region.

**Files**: `src/chirp_ui/templates/chirpui/fragment_island.html`
**Acceptance**: New test renders fragment_island with broken caller → still produces the `id` and `aria-live` wrapper.

### Task 1.5 — CSS for error state

Add `chirpui-streaming--error` styles (muted background, reduced opacity or error icon placeholder).

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `test_template_css_contract.py` passes.

---

## Sprint 2: List Comprehension Cleanup in Layout ✅

**Goal**: Replace the longest ternary chains in `layout.html` with list comprehensions for readability without changing output.

### Task 2.1 — Grid class assembly

Replace the 5-level nested `{% if %}` chain in `grid()` with:
```
{% set _classes = [cls for cls in [
    "chirpui-grid",
    "chirpui-grid--cols-" ~ cols if cols and not _has_preset else "",
    "chirpui-grid--gap-" ~ gap if gap else "",
    _preset_class,
    "chirpui-grid--items-" ~ items if items else "",
    cls
] if cls] %}
<div class="{{ _classes | join(' ') }}">
```

**Files**: `src/chirp_ui/templates/chirpui/layout.html`
**Acceptance**: All existing layout tests pass unchanged. `rg 'chirpui-grid--' tests/` confirms all class assertions still hold.

### Task 2.2 — Frame, stack, cluster, block class assembly

Apply the same list-comprehension pattern to `frame()`, `stack()`, `cluster()`, and `block()`.

**Files**: `src/chirp_ui/templates/chirpui/layout.html`
**Acceptance**: All layout tests pass. No new CSS classes introduced.

### Task 2.3 — Snapshot test for class output parity

Add a focused test that renders `grid()`, `frame()`, `stack()`, `cluster()`, `block()` with known args and asserts the exact class string matches pre-refactor output.

**Files**: `tests/test_components.py`
**Acceptance**: `uv run pytest tests/test_components.py::TestLayout -q` passes.

---

## Sprint 3: Document Scoped Slots & Partial Evaluator

**Goal**: Document kida 0.4.0 features that chirp-ui doesn't adopt directly but that downstream Chirp app developers should know about.

### Task 3.1 — Scoped slots guide

Add a section to `docs/COMPONENT-OPTIONS.md` explaining when to use scoped slots (`{% slot name let:var=expr %}`) vs provide/consume. Key guidance: scoped slots for parent-templates-child-data inversion-of-control; provide/consume for deep cross-macro context propagation.

**Files**: `docs/COMPONENT-OPTIONS.md`
**Acceptance**: File contains "Scoped Slots" section with usage example.

### Task 3.2 — Partial evaluator note

Add a note to `docs/COMPONENT-OPTIONS.md` or `README.md` explaining that Chirp apps can opt into the partial evaluator via `Environment(partial_eval=True)` for compile-time constant folding. chirp-ui templates are compatible but don't require it.

**Files**: `docs/COMPONENT-OPTIONS.md` or `README.md`
**Acceptance**: Document mentions `partial_eval=True`.

### Task 3.3 — Error boundary pattern guide

Document the `{% try %}...{% fallback %}` pattern for chirp-ui component authors — when to use it, fallback strategies per component tier (OOB-critical, visible, slot guard).

**Files**: `docs/COMPONENT-OPTIONS.md`
**Acceptance**: File contains "Error Boundaries" section with tier table and example.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `{% try %}` overhead on hot render paths | Low | Low | kida's `{% try %}` is zero-cost on success path (no exception = no overhead). Benchmark in Sprint 1 if concerned. |
| List comprehension changes class ordering | Medium | Medium | Sprint 2 Task 2.3 adds snapshot test asserting exact class output parity before/after. |
| Scoped slot syntax changes in kida 0.5 | Low | Low | Sprint 3 docs note the `let:` syntax is 0.4.0-specific; provide/consume remains the primary pattern. |
| Error boundary masks real bugs during dev | Medium | Low | Use `set_strict()` to disable boundaries in dev/test; boundaries active in prod only. (Deferred — evaluate after Sprint 1.) |

---

## Success Metrics

| Metric | Current | After Sprint 1 | After Sprint 2 |
|--------|---------|----------------|----------------|
| OOB templates with render-crash protection | 1 (suspense_slot) | 5 (+ oob, toast, streaming, fragment_island) | 5 |
| Templates with 3+ ternary class chains | 4 | 4 | 0 |
| kida 0.4.0 features documented | 3 (CLAUDE.md) | 3 | 6 (+ COMPONENT-OPTIONS.md) |
| Test count | 1085 | ~1095 | ~1100 |

---

## Relationship to Existing Work

- **Behavior layer hardening (#47)** — Sprint 1 extends the error boundary pattern started there (client-side island error_boundary). This is the *template-level* complement.
- **Streaming maturity (#43)** — Sprint 1 Task 1.2 hardens the streaming templates that #43 introduced.
- **Provide/consume expansion** — No conflict. Scoped slots are an alternative pattern documented in Sprint 3, not a replacement.

---

## Changelog

- **2026-04-10** — Sprint 0 complete: dep bumped, suspense_slot boundary added, CLAUDE.md updated, plan drafted.
- **2026-04-10** — Sprints 1–2 complete: error boundaries on oob/streaming/fragment_island (toast skipped — no slot content), layout.html class assembly refactored to list comprehensions. 1089 tests pass. Toast boundary omitted because errors in toast originate at the call site (argument evaluation), not inside the macro body.
- **2026-04-10** — Sprint 3 complete: documented error boundaries (tier guide, syntax, when-not-to-use), scoped slots (vs provide/consume decision guide), and partial evaluator (opt-in via Environment) in COMPONENT-OPTIONS.md. All 4 sprints done.
