# Sprint 0: Behavior Layer Hardening — Design & Validate

**Parent epic**: `PLAN-behavior-layer-hardening.md`
**Status**: Complete
**Date**: 2026-04-10

---

## Task 0.1 — ASCII Macro Signatures

26 untested components. All use `validate_variant()` and `cls=""` for class injection.

### Display-only (14)

| # | Macro | Params | BEM Root | Variants | Slots |
|---|-------|--------|----------|----------|-------|
| 1 | `ascii_7seg(text, label, variant)` | text, label=none, variant="" | `chirpui-ascii-7seg` | default, accent, success, warning, error | No |
| 2 | `ascii_badge(text, glyph, variant, frame)` | text="", glyph="", variant="", frame="" | `chirpui-ascii-badge` | default, success, warning, error, accent, muted; frames: pipe, bracket, angle, none | No |
| 3 | `ascii_divider(glyph, variant)` | glyph="", variant="" | `chirpui-ascii-divider` | single, double, heavy, dots | No |
| 4 | `ascii_empty(glyph, heading, description, variant)` | glyph="◇", heading="Nothing here", description="", variant="default" | `chirpui-ascii-empty` | default, muted, accent | Yes |
| 5 | `ascii_error(code, heading, description)` | code="404", heading="", description="" | `chirpui-ascii-error` | codes: 404, 403, 500, 503, timeout, empty | Yes |
| 6 | `ascii_indicator(label, variant, blink, glyph)` | label=none, variant="success", blink=false, glyph="square" | `chirpui-ascii-indicator` | success, warning, error, muted, accent; glyphs: square, round, diamond | No (row has slot) |
| 7 | `ascii_progress(value, label, variant, width)` | value=0, label="", variant="", width=20 | `chirpui-ascii-progress` | default, accent, success, warning | No |
| 8 | `ascii_skeleton(variant, lines, width)` | variant="", lines=1, width="" | `chirpui-ascii-skeleton` | text, card, avatar, heading | No |
| 9 | `ascii_sparkline(values, variant)` | values=[], variant="" | `chirpui-ascii-sparkline` | default, accent, muted, gradient | No |
| 10 | `ascii_spinner(charset, size, label)` | charset="braille", size="md", label="" | `chirpui-ascii-spinner` | charsets: braille, box, dots, arrows, blocks | No |
| 11 | `ascii_stepper(steps, current, variant)` | steps, current=0, variant="" | `chirpui-ascii-stepper` | default, accent, success | No |
| 12 | `ascii_ticker(text, variant, speed)` | text, variant="", speed="" | `chirpui-ascii-ticker` | default, accent, success, warning, error; speeds: slow, default, fast | No |
| 13 | `split_flap(text, variant, animate)` | text, variant="", animate=true | `chirpui-split-flap` | default, amber, green | No (board has slot) |
| 14 | `ascii_card(title, variant, glyph)` | title=none, variant="", glyph="" | `chirpui-ascii-card` | single, double, rounded, heavy | Yes |

### Interactive (8)

| # | Macro | Params | BEM Root | Variants | Slots |
|---|-------|--------|----------|----------|-------|
| 15 | `ascii_checkbox(name, label, checked, variant, disabled)` | name, label=none, checked=false, variant="", disabled=false | `chirpui-ascii-checkbox` | default, accent, success, danger | No (group has slot) |
| 16 | `ascii_fader(name, value, label, variant)` | name, value=0, label=none, variant="" | `chirpui-ascii-fader` | default, accent, success, warning, danger | No (bank has slot) |
| 17 | `ascii_knob(name, options, selected, label, variant)` | name, options, selected=none, label=none, variant="" | `chirpui-ascii-knob` | default, accent | No |
| 18 | `ascii_modal(id, title, variant)` | id, title=none, variant="" | `chirpui-ascii-modal` | single, double, heavy | Yes |
| 19 | `ascii_radio(name, value, label, checked, disabled)` | name, value, label=none, checked=false, disabled=false | `chirpui-ascii-radio` | default, accent; layouts: vertical, horizontal | No (group has slot) |
| 20 | `ascii_toggle(name, checked, label, variant, size, disabled)` | name, checked=false, label=none, variant="", size="", disabled=false | `chirpui-ascii-toggle` | default, success, danger, accent; sizes: sm, md, lg | No |
| 21 | `ascii_tile_btn(glyph, label, variant, lit, toggle, name, disabled)` | glyph="■", label=none, variant="", lit=false, toggle=false, name=none, disabled=false | `chirpui-ascii-tile-btn` | default, success, warning, danger, accent | No (grid has slot) |
| 22 | `ascii_vu_meter(name, value, label, variant, width, peak, animate)` | name=none, value=0, label=none, variant="", width=20, peak=false, animate=false | `chirpui-ascii-vu` | default, accent, success, warning | No (stack has slot) |

### Composite (4)

| # | Macro | Params | BEM Root | Variants | Slots |
|---|-------|--------|----------|----------|-------|
| 23 | `ascii_border(variant, glyph)` | variant="", glyph="" | `chirpui-ascii-border` | single, double, rounded, heavy | Yes |
| 24 | `ascii_table(headers, variant, align, compact, striped, sticky_header)` | headers=none, variant="single", align=none, compact=false, striped=false, sticky_header=false | `chirpui-ascii-table` | single, double, heavy, rounded | Yes |
| 25 | `ascii_tabs(variant)` + `ascii_tab(id, label, url, hx_target, active)` | variant="" / id, label, url=none, hx_target=none, active=false | `chirpui-ascii-tabs` | default, accent | Yes |
| 26 | `breaker_panel(title, variant, size, master)` + `breaker(name, label, checked, variant, disabled)` | title=none, variant="double", size="" / name, label=none, checked=false, variant="", disabled=false | `chirpui-ascii-breaker-panel` | default, double, heavy; sizes: sm, md | Yes |

### Companion macros (also need tests)

Several components have companion layout macros:
- `indicator_row()` — wraps `indicator()` calls
- `fader_bank(title)` — wraps `ascii_fader()` calls
- `ascii_checkbox_group(legend)` — wraps `ascii_checkbox()` calls
- `ascii_radio_group(name, legend, layout, variant)` — wraps `ascii_radio()` calls
- `split_flap_row(cells)` / `split_flap_board(title, variant)` — wraps `split_flap()` calls
- `tile_grid(cols)` — wraps `tile_btn()` calls
- `vu_meter_stack(title)` — wraps `ascii_vu_meter()` calls
- `ascii_modal_trigger(target, label)` — button to open modal

---

## Task 0.2 — Orphaned Provider Decisions

**Revised decision (2026-04-10)**: Wire all providers to consumers and showcase the pattern, rather than removing any.

| Key | Provider(s) | Consumer(s) | What It Enables |
|-----|-------------|-------------|-----------------|
| `_card_variant` | card.html | badge, divider, alert | Warning card → auto-warning badges/dividers inside. Most visual showcase candidate. |
| `_bar_surface` | command_bar.html, filter_bar.html | button, icon_btn | Bar children inherit surface tone (dark surface → ghost buttons). |
| `_bar_density` | command_bar.html, filter_bar.html | button, field macros | Dense bar → compact buttons/fields automatically. |
| `_surface_variant` | surface.html, panel.html | divider, badge, card | Muted surface → muted dividers/badges inside. |
| `_streaming_role` | streaming.html | copy_button | Role-aware styling in assistant vs user bubbles. |
| `_suspense_busy` | suspense.html | button, interactive fields | Auto-disable buttons during deferred loading. Genuinely useful UX. |

**Also fix**: `_sse_state` is consumed by `sse_retry()` but never provided. Add `{% provide _sse_state = state %}` to `sse_status()`.

**Summary**: Remove 5 orphaned providers. Wire 1 (`_surface_variant`). Add 1 missing provider (`_sse_state`).

---

## Task 0.3 — Error Boundary v2 API

### Current API (v1)

```
DOM contract:
  [data-error-body]      — hidden on error, shown on reset
  [data-error-fallback]  — shown on error, hidden on reset
  [data-error-reset]     — click resets to healthy

Events listened:
  chirp:island:error     — triggers fallback (filtered by id/name)

State emitted:
  { boundaryId, state: "error" | "healthy" }
```

### Proposed Additions (v2)

**1. Error message display**

New DOM element: `[data-error-message]` inside the fallback region.

On error, populate with `detail.reason` via `textContent` (not innerHTML — XSS safe):
```javascript
const msg = root.querySelector("[data-error-message]");
// in showFallback:
if (msg && reason) msg.textContent = reason;
// in clearFallback:
if (msg) msg.textContent = "";
```

Backward-compat: If `[data-error-message]` doesn't exist, behavior is unchanged.

**2. Retry button**

New DOM element: `[data-error-retry]` inside the fallback region.

On click:
1. Dispatch `setAction(payload, api, "retry", "pending", { boundaryId })`
2. Reset to healthy state (call `clearFallback()`)

```javascript
const retry = root.querySelector("[data-error-retry]");
const onRetry = () => {
  setAction(payload, api, "retry", "pending", { boundaryId });
  clearFallback();
};
retry?.addEventListener("click", onRetry);
// cleanup: retry?.removeEventListener("click", onRetry);
```

The retry button does **not** re-mount the failed island — that's the consumer's responsibility. The action event signals intent; an outer coordinator or htmx swap handles the actual retry. This prevents infinite loops.

Backward-compat: If `[data-error-retry]` doesn't exist, behavior is unchanged. Existing `[data-error-reset]` continues to work (reset without retry action).

**3. Telemetry event**

On error (inside `showFallback`), dispatch a separate telemetry event:

```javascript
document.dispatchEvent(new CustomEvent("chirp:island:error:report", {
  detail: { boundaryId, reason, timestamp: Date.now(), source: "error_boundary" }
}));
```

This is fire-and-forget. Consumers can attach a listener for logging, Sentry, etc. No state change.

**4. Store error reason in state**

Extend state emission to include the reason:
```javascript
// v1: setState(payload, api, { boundaryId, state: "error" });
// v2: setState(payload, api, { boundaryId, state: "error", reason });
```

On clear: `{ boundaryId, state: "healthy", reason: null }`.

### Updated DOM contract (v2)

```
[data-error-body]       — hidden on error, shown on reset (unchanged)
[data-error-fallback]   — shown on error, hidden on reset (unchanged)
[data-error-reset]      — click resets to healthy (unchanged)
[data-error-message]    — NEW: populated with error reason text on error, cleared on reset
[data-error-retry]      — NEW: click dispatches retry action + resets to healthy

Events listened:
  chirp:island:error     — triggers fallback (unchanged)

Events emitted:
  chirp:island:state     — now includes `reason` field
  chirp:island:action    — NEW: { action: "retry", status: "pending", boundaryId }
  chirp:island:error:report — NEW: telemetry event with boundaryId, reason, timestamp
```

### Import change

Need to add `setAction` to the import:
```javascript
import { readProps, registerPrimitive, setState, setAction } from "/static/islands/foundation.js";
```

---

## Task 0.4 — Alpine Playwright Priority

Ranked by user-facing risk and interaction complexity. Excluded components with implicit coverage (command_palette trigger, modal_overlay trigger, tray trigger — these are simple `showModal()` / store setters).

| Rank | Component | x-data Shape | Why Priority | Key Test Cases |
|------|-----------|-------------|--------------|----------------|
| 1 | **theme_toggle** | `{ theme, icons, cycle() }` + `{ style, icons, cycle() }` | Core UX — broken theme = broken site. localStorage persistence. | Cycle light→dark→system; persists across reload; applies correct class |
| 2 | **copy_button** | `{ copied: false }` | High-frequency user action. Clipboard API. | Click copies text; "Copied!" feedback appears; reverts after timeout |
| 3 | **toast** | bare x-data | User feedback channel. Auto-dismiss timing. | Renders; auto-dismisses after delay; manual dismiss works |
| 4 | **alert** | bare x-data | Critical for error/warning display. Dismiss behavior. | Renders variants; dismiss removes from DOM |
| 5 | **app_shell_layout** | `{ collapsible, collapsed, toggle() }` | Structural — sidebar collapse affects entire layout. localStorage. | Toggle collapses sidebar; persists; respects breakpoint |
| 6 | **sse_status** | `{ retrying: false }` | Real-time features depend on connection state visibility. | Shows connected/disconnected/error; retry button works |
| 7 | **reveal_on_scroll** | `{ shown: false }` + x-intersect | Viewport-dependent — can't unit test. Intersection Observer. | Element hidden until scrolled into view; stays shown after |
| 8 | **confetti** | `{ active: false }` | Engagement feature. Animation trigger. | Trigger activates; particles render; auto-deactivates |

**Deferred (5 components, lower risk)**:
- `ripple_button` — cosmetic animation only
- `code` block copy — same pattern as copy_button
- `streaming` copy — same pattern as copy_button
- `ascii_modal` — native `<dialog>`, minimal Alpine
- `sortable_list` — complex but niche

---

## Summary of Sprint 0 Outputs

| Task | Output | Key Decision |
|------|--------|-------------|
| 0.1 | 26 macro signatures documented | 14 display, 8 interactive, 4 composite + 8 companion macros |
| 0.2 | Provider decisions | Wire all 7 keys to consumers + showcase the pattern, add 1 (`_sse_state`) |
| 0.3 | Error boundary v2 spec | 4 additions: message display, retry button, telemetry event, reason in state |
| 0.4 | Playwright top 8 | theme_toggle, copy_button, toast, alert, app_shell_layout, sse_status, reveal_on_scroll, confetti |
