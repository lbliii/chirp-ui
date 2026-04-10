# Epic: Streaming & SSE Component Maturity — Variants, Context Flow, and Resilience

**Status**: Complete
**Created**: 2026-04-10
**Target**: 0.3.0
**Estimated Effort**: 18–28h
**Dependencies**: kida ≥ 0.3.4 (provide/consume), chirpui 0.2.6 (current)
**Source**: Codebase analysis — 15 macros across 5 templates with mid-maturity test coverage, no provide/consume, and variant gaps vs. ASCII component benchmark

---

## Why This Matters

The streaming/SSE/suspense component family (15 macros across `streaming.html`, `sse_status.html`, `suspense.html`, `toast.html`, `oob.html`) is chirp-ui's real-time UI toolkit — the layer that makes LLM chat interfaces, live dashboards, and deferred-loading patterns work over the wire. But compared to the recently-matured ASCII family (27 components, 1367 tests, full a11y), these components ship with variant gaps, no provide/consume context flow, and incomplete accessibility.

1. **No provide/consume context** — streaming role, SSE endpoint state, and suspense resolution status must be passed explicitly through every nesting level; parent context can't flow to children across slot boundaries
2. **Limited variants** — `streaming_block` has no visual variants (only a boolean `streaming` flag); `streaming_bubble` hardcodes `aria-label="assistant response"` regardless of role; `suspense_slot` has no skeleton variant validation
3. **34 tests for 15 macros** — 2.3 tests per macro vs. button's 6.5 per macro and ASCII icon's 12; streaming_bubble role combinations and error states are untested
4. **No error/thinking states** — streaming bubbles can't distinguish content vs. thinking vs. error states visually; SSE retry has no feedback on failure; no typing indicator pattern
5. **4 forward CSS gaps** (streaming family) — `chirpui-copy-btn__done`, `chirpui-copy-btn__label`, `chirpui-model-card__footer`, `chirpui-toast__message` reference classes that don't exist in `chirpui.css`
6. **4 variant registry mismatches** — btn success/warning/default and modal medium are registered but have no CSS (2 real gaps + 2 registry cleanups)

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| Template analysis | 15 macros, 0 provide/consume keys | FIXES — Sprint 2 adds `_streaming_role`, `_sse_state`, `_suspense_busy` keys |
| test_components.py | 34 tests / 15 macros = 2.3x coverage ratio | FIXES — Sprint 1 targets 60+ tests (4x ratio) |
| streaming.html | `aria-label="assistant response"` hardcoded regardless of role param | FIXES — Sprint 1 parametrizes aria-label by role |
| chirpui.css scan | 4 streaming template classes missing CSS definitions | FIXES — Sprint 3 closes forward CSS gaps |
| validation.py | 4 registered variants with no CSS (2 real + 2 registry cleanups) | FIXES — Sprint 3 adds missing variant CSS or cleans registry |
| sse_status.html | Retry button has no error/loading feedback | FIXES — Sprint 2 adds retry state indicators |
| suspense.html | `suspense_group` can't track child slot resolution | MITIGATES — Sprint 2 adds provide key for busy state |

---

### Invariants

These must remain true throughout or we stop and reassess:

1. **CSS contract holds**: every `chirpui-*` class referenced in templates exists in `chirpui.css` (enforced by `test_template_css_contract.py`)
2. **No JavaScript in macros**: streaming/SSE components stay pure HTML + HTMX + Alpine `x-data` — no `<script>` tags
3. **Existing macro signatures don't break**: new parameters are additive; no existing call site needs updating

---

## Target Architecture

After this epic, the streaming/SSE/suspense family will have:

```
15 macros (current)      →  15 macros (no new macros — depth over breadth)
 0 provide/consume keys  →  3 keys (_streaming_role, _sse_state, _suspense_busy)
34 tests                 →  65+ tests (4x per-macro coverage)
 0 variant states        →  3 streaming states (content, thinking, error)
 4 forward CSS gaps      →  0 gaps (all template classes have CSS)
 4 registry mismatches   →  0 mismatches (all registered variants have CSS or cleaned)
```

### Provide/Consume Key Design

```
_streaming_role     — provided by streaming_bubble(role=...)
                      consumed by copy_btn, model_card (auto-inherit role context)

_sse_state          — provided by sse_status(state=...)
                      consumed by sse_retry (auto-disable when connected)

_suspense_busy      — provided by suspense_group()
                      consumed by suspense_slot (coordinate resolution tracking)
```

### Streaming Bubble State Machine

```
streaming_bubble(role, state)

  state="content"   →  default; renders message body
  state="thinking"  →  pulsing cursor + aria-busy="true"
  state="error"     →  error variant styling + role="alert"
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: state model, provide keys, CSS gap inventory | 2–3h | Low | Yes (RFC only) |
| 1 | Test density + a11y fixes | 5–7h | Low | Yes |
| 2 | Provide/consume + streaming states | 5–8h | Medium | Yes |
| 3 | CSS contract closure + variant registry alignment | 4–6h | Low | Yes |
| 4 | Documentation + showcase coverage | 2–4h | Low | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Solve the state model and context key design on paper before touching code.

### Task 0.1 — Define streaming state variants

Decide the streaming_bubble state enum: `content | thinking | error`. Map each to CSS classes, aria attributes, and visual treatment. Confirm no overlap with existing `message_bubble` role variants.

**Acceptance**: Design doc section added to this plan; `rg 'state=' src/chirp_ui/templates/chirpui/streaming.html` confirms no conflicting param exists.

### Task 0.2 — Define provide/consume keys

Finalize 3 keys (`_streaming_role`, `_sse_state`, `_suspense_busy`). Validate that names don't collide with existing keys in `docs/PROVIDE-CONSUME-KEYS.md`.

**Acceptance**: Keys added to PROVIDE-CONSUME-KEYS.md; `rg '_streaming_role\|_sse_state\|_suspense_busy' docs/PROVIDE-CONSUME-KEYS.md` returns 3 hits.

### Task 0.3 — Inventory forward CSS gaps

Generate definitive list of template classes missing CSS. Separate into: (a) need new CSS rules, (b) template class is wrong (typo/stale), (c) generated dynamically (skip).

**Acceptance**: Inventory table added to this plan with disposition per class.

---

## Sprint 1: Test Density & A11y Fixes

**Goal**: Bring test coverage to 4x per-macro ratio and fix accessibility gaps — no behavioral changes.

### Task 1.1 — Expand streaming test coverage

Add tests for: streaming_bubble with all 4 roles (user, assistant, system, default), copy_btn clipboard state, model_card without SSE, streaming_block inactive state. Target: 15 new tests.

**Files**: `tests/test_components.py` (TestStreaming class)
**Acceptance**: `uv run pytest tests/test_components.py::TestStreaming -v` passes with 22+ tests (up from 7).

### Task 1.2 — Expand suspense/SSE test coverage

Add tests for: suspense_slot with all skeleton variants (card, text, custom), suspense_group with nested slots, sse_status custom state validation, sse_retry POST method. Target: 10 new tests.

**Files**: `tests/test_components.py` (TestSuspense, TestSseStatus classes)
**Acceptance**: `uv run pytest tests/test_components.py::TestSuspense tests/test_components.py::TestSseStatus -v` passes with 26+ tests (up from 16).

### Task 1.3 — Fix streaming_bubble aria-label

Parametrize `aria-label` based on `role`: "assistant response", "user message", "system message", "message". Remove hardcoded string.

**Files**: `src/chirp_ui/templates/chirpui/streaming.html`
**Acceptance**: `uv run pytest tests/test_components.py::TestStreaming -v` includes test for each role's aria-label; `rg 'aria-label="assistant response"' src/chirp_ui/templates/chirpui/streaming.html` returns zero hardcoded hits.

### Task 1.4 — Expand toast/OOB test coverage

Add tests for: toast with custom `id`, oob_toast variant propagation, counter_badge with `oob=false`. Target: 6 new tests.

**Files**: `tests/test_components.py` (TestToast, TestOobHelpers classes)
**Acceptance**: `uv run pytest tests/test_components.py::TestToast tests/test_components.py::TestOobHelpers -v` passes with 24+ tests (up from 18).

---

## Sprint 2: Provide/Consume & Streaming States

**Goal**: Add parent-to-child context flow and streaming state variants — the behavioral leap.

### Task 2.1 — Add provide/consume to streaming_bubble

`streaming_bubble` provides `_streaming_role` so nested `copy_btn` and `model_card` can consume the role without explicit params.

**Files**: `src/chirp_ui/templates/chirpui/streaming.html`
**Acceptance**: `uv run pytest tests/test_provide_consume.py -k streaming -v` passes with 5+ new tests.

### Task 2.2 — Add provide/consume to sse_status

`sse_status` provides `_sse_state` so nested `sse_retry` can auto-disable/enable based on connection state.

**Files**: `src/chirp_ui/templates/chirpui/sse_status.html`
**Acceptance**: `uv run pytest tests/test_provide_consume.py -k sse -v` passes with 3+ new tests.

### Task 2.3 — Add provide/consume to suspense_group

`suspense_group` provides `_suspense_busy` so child slots can coordinate resolution.

**Files**: `src/chirp_ui/templates/chirpui/suspense.html`
**Acceptance**: `uv run pytest tests/test_provide_consume.py -k suspense -v` passes with 3+ new tests.

### Task 2.4 — Add streaming state variants

Add `state` param to `streaming_bubble`: `content` (default), `thinking` (pulsing cursor, aria-busy), `error` (error styling, role=alert). Register in VARIANT_REGISTRY.

**Files**: `src/chirp_ui/templates/chirpui/streaming.html`, `src/chirp_ui/validation.py`
**Acceptance**: `uv run pytest tests/test_components.py::TestStreaming -v` passes with state variant tests; `rg 'streaming_bubble.*state' tests/test_components.py` returns hits.

### Task 2.5 — Add retry state feedback to sse_retry

Add `loading` state with spinner and `aria-busy="true"` during retry attempt. Alpine.js `x-data` for state toggle on click.

**Files**: `src/chirp_ui/templates/chirpui/sse_status.html`
**Acceptance**: `uv run pytest tests/test_components.py::TestSseStatus -v` includes retry loading state test.

---

## Sprint 3: CSS Contract Closure

**Goal**: Close all forward CSS gaps and align variant registry with CSS — zero mismatches.

### Task 3.1 — Add missing CSS for streaming template classes

Add CSS rules for 4 streaming-family classes missing from `chirpui.css`:
- `.chirpui-copy-btn__label` — flex child for "Copy" text
- `.chirpui-copy-btn__done` — flex child for "Copied!" text
- `.chirpui-model-card__footer` — model-card-specific footer overrides
- `.chirpui-toast__message` — flex child for toast text

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `rg 'chirpui-copy-btn__label|chirpui-copy-btn__done|chirpui-model-card__footer|chirpui-toast__message' src/chirp_ui/templates/chirpui.css` returns 4 hits.

### Task 3.2 — Fix variant registry mismatches

Add CSS for `chirpui-btn--success` and `chirpui-btn--warning`. Remove `"default"` from btn registry and `"medium"` from modal SIZE_REGISTRY (these are the unstyled defaults, not variants).

**Files**: `src/chirp_ui/templates/chirpui.css`, `src/chirp_ui/validation.py`
**Acceptance**: `rg 'chirpui-btn--success' src/chirp_ui/templates/chirpui.css` returns hit; `"default"` no longer in btn variant tuple.

### Task 3.3 — Add streaming state CSS

Add CSS for new streaming states: `.chirpui-streaming-bubble--thinking` (pulsing cursor animation), `.chirpui-streaming-bubble--error` (error color treatment). Use existing motion tokens.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `uv run pytest tests/test_transition_tokens.py -v` passes (no hardcoded timings); `rg 'streaming-bubble--thinking' src/chirp_ui/templates/chirpui.css` returns hit.

---

## Sprint 4: Documentation & Showcase

**Goal**: Document the matured streaming patterns for downstream users.

### Task 4.1 — Update COMPONENT-OPTIONS.md

Expand streaming/SSE/suspense sections with: new state variants, provide/consume keys, retry patterns, and composition examples.

**Files**: `docs/COMPONENT-OPTIONS.md`
**Acceptance**: `rg 'state="thinking"' docs/COMPONENT-OPTIONS.md` returns example.

### Task 4.2 — Update PROVIDE-CONSUME-KEYS.md

Add the 3 new keys with descriptions and usage examples.

**Files**: `docs/PROVIDE-CONSUME-KEYS.md`
**Acceptance**: `rg '_streaming_role\|_sse_state\|_suspense_busy' docs/PROVIDE-CONSUME-KEYS.md` returns 3 hits.

### Task 4.3 — Add showcase coverage

Add streaming/SSE examples to the component showcase (connected, thinking, error states; retry demo; suspense skeleton-to-content).

**Files**: `examples/component-showcase/templates/`
**Acceptance**: Showcase renders streaming section without errors.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Provide/consume scoping issue (kida ≤ 0.3.4 bug with same-name params) | Medium | Medium | Sprint 0 validates key names don't collide with macro params; use `_` prefix convention |
| CSS gap inventory is stale (templates changed since analysis) | Low | Low | Sprint 0 Task 0.3 generates fresh inventory before Sprint 3 starts |
| Streaming state variants break existing usage | Low | High | Invariant 3 — `state` defaults to "content"; existing calls without `state` param unchanged |
| New CSS rules inflate stylesheet size | Low | Low | New rules are ~50 lines; chirpui.css is already 2000+ lines |
| Alpine.js dependency for retry state feedback | Low | Medium | Sprint 2.5 uses minimal `x-data`; same pattern as copy_btn (already validated) |

---

## Success Metrics

| Metric | Current | After Sprint 1 | After Sprint 4 |
|--------|---------|-----------------|-----------------|
| Tests per macro | 2.3 | 4.3+ | 4.3+ |
| Total streaming/SSE tests | 34 | 65+ | 65+ |
| Provide/consume keys | 0 | 0 | 3 |
| Forward CSS gaps (streaming) | 4 | 4 | 0 |
| Registry mismatches | 4 | 4 | 0 |
| Streaming state variants | 0 | 0 | 3 (content, thinking, error) |
| Aria-label accuracy | partial | fixed | fixed |

---

## Relationship to Existing Work

- **ASCII Component Maturity (PLAN-ascii-maturity.md)** — parallel precedent — this epic follows the same structure: tests → a11y → variants → docs. ASCII work validates the pattern.
- **Provide/Consume Expansion (PLAN-provide-consume-expansion.md)** — prerequisite complete — kida 0.3.4 adoption and initial provide/consume rollout landed in 0.2.6. This epic extends that to streaming components.
- **Elevated Design Layer (#42)** — parallel — deep shadows and corner brackets could apply to streaming surfaces in future work, but are not in scope here.

---

## Changelog

- **2026-04-10**: Initial draft from codebase analysis (15 macros, 34 tests, 0 provide/consume keys)
- **2026-04-10**: Sprint 0 complete — design decisions below
- **2026-04-10**: Sprint 1 complete — 45 new tests, aria-label fix, 79 total streaming/SSE tests
- **2026-04-10**: Sprint 2 complete — 3 provide/consume keys, streaming state variants, sse_retry loading
- **2026-04-10**: Sprint 3 complete — 11 CSS rules added, 0 forward gaps, 0 registry mismatches
- **2026-04-10**: Sprint 4 complete — COMPONENT-OPTIONS.md streaming section, PROVIDE-CONSUME-KEYS.md updated
- **2026-04-10**: Epic complete — 920 tests passing, all acceptance criteria met

---

## Sprint 0 Findings

### 0.1 — Streaming State Variant Design

The `state` param is **orthogonal** to the existing `streaming` boolean and `role` param.
`streaming` controls whether the cursor animates; `role` controls sender identity; `state`
controls the semantic phase of a message.

| `state` | CSS class | `aria-*` | Visual | Notes |
|---------|-----------|----------|--------|-------|
| `""` / `"content"` (default) | *(none — base class)* | current behavior | Normal message | Backwards compatible; existing calls unchanged |
| `"thinking"` | `chirpui-streaming-bubble--thinking` | `aria-busy="true"` | Pulsing dots animation | Distinct from streaming cursor — represents "model is processing" |
| `"error"` | `chirpui-streaming-bubble--error` | `role="alert"` | Error color treatment (`--chirpui-error`) | Replaces generic `aria-label`; adds alert semantics |

**aria-label fix:** Currently hardcoded to `"assistant response"`. New mapping:

| `role` | `aria-label` |
|--------|-------------|
| `"assistant"` | `"assistant response"` |
| `"user"` | `"user message"` |
| `"system"` | `"system message"` |
| `"default"` | `"message"` |

**Registry entry:** `"streaming_bubble": ("", "content", "thinking", "error")` in VARIANT_REGISTRY.

**No overlap with message_bubble:** `message_bubble` variants are roles (`default`, `user`, `assistant`, `system`).
Streaming states are phases (`content`, `thinking`, `error`). Orthogonal by design.

### 0.2 — Provide/Consume Key Design

All 3 proposed keys validated against `docs/PROVIDE-CONSUME-KEYS.md` — no collisions.

| Key | Type | Default | Provider | Consumer(s) | Rationale |
|-----|------|---------|----------|-------------|-----------|
| `_streaming_role` | `str` | `"assistant"` | `streaming_bubble(role=...)` | `copy_btn` (label context), `model_card` (aria-label) | Nested children shouldn't need explicit `role` when bubble provides it |
| `_sse_state` | `str` | `"connected"` | `sse_status(state=...)` | `sse_retry` (auto-disable when connected) | Retry button only makes sense when disconnected/error |
| `_suspense_busy` | `str` | `"true"` | `suspense_group()` | `suspense_slot` (coordination) | Slots can adjust rendering when group is/isn't busy |

**Consumer patterns:**
```jinja2
{# copy_btn: inherit role for contextual labeling #}
{% set _role = consume("_streaming_role", "assistant") %}

{# sse_retry: auto-detect connection state #}
{% set _state = consume("_sse_state", "") %}
{% if _state != "connected" %}...{% end %}

{# suspense_slot: inherit busy state #}
{% set _busy = consume("_suspense_busy", "true") %}
```

### 0.3 — Forward CSS Gap Inventory (Streaming Family)

Verified against `chirpui.css` on 2026-04-10. Only streaming-related templates scoped.

| Class | Template | Disposition |
|-------|----------|-------------|
| `chirpui-copy-btn__done` | `streaming.html:52` | **Needs CSS** — "Copied!" label span, should match copy-btn styling |
| `chirpui-copy-btn__label` | `streaming.html:51` | **Needs CSS** — "Copy" label span |
| `chirpui-model-card__footer` | `streaming.html:77` | **Needs CSS** — used alongside `chirpui-card__footer`; add model-card-specific overrides |
| `chirpui-toast__message` | `toast.html:26` | **Needs CSS** — toast text span, currently unstyled (flex child sizing) |

**False positives removed:**
- `chirpui-toasts` — HTML `id` attribute, not a CSS class
- `chirpui-counter-badge--`, `chirpui-message-bubble--`, `chirpui-sse-status--`, `chirpui-toast--` — dynamic BEM modifier prefixes; actual variant classes all exist in CSS

**Registry variant gaps (broader, not streaming-specific):**

| Registered variant | CSS class | Status |
|-------------------|-----------|--------|
| btn `"default"` | `.chirpui-btn--default` | Missing — empty string is the actual default; consider removing from registry |
| btn `"success"` | `.chirpui-btn--success` | Missing — needs CSS |
| btn `"warning"` | `.chirpui-btn--warning` | Missing — needs CSS |
| modal `"medium"` | `.chirpui-modal--medium` | Missing — medium is the default size; consider removing from registry |

**Revised scope for Sprint 3:** 4 streaming CSS rules + 2 real btn variant rules + 2 registry cleanups.
