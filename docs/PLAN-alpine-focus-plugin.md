# chirp-ui: Alpine Focus Plugin Integration

## Goal

Add the [Alpine Focus plugin](https://alpinejs.dev/plugins/focus) to ChirpUI and use `x-trap` for proper focus management in tray and modal overlay components. Improves accessibility (WCAG 2.1 focus containment) and reduces custom focus/scroll logic.

---

## Background

### Focus Plugin Capabilities

| Feature | Description |
|---------|-------------|
| **x-trap** | Trap focus within element when expression is true; return focus when false |
| **.inert** | Set `aria-hidden="true"` on siblings when trap is active (screen reader isolation) |
| **.noscroll** | Disable body scroll when trap is active |
| **.noreturn** | Don't return focus on close (e.g. dropdowns) |
| **.noautofocus** | Don't auto-focus first element when trap engages |
| **$focus** | Magic: `first()`, `last()`, `next()`, `previous()`, `wrap()`, `within()` |

### Current ChirpUI State

| Component | Implementation | Focus/Scroll Today |
|-----------|----------------|---------------------|
| **tray** | div-based, `Alpine.store('trays')` | No focus trap. Body scroll lock via `Alpine.effect` in app_shell_layout. |
| **modal_overlay** | div-based, `Alpine.store('modals')` | Same as tray. |
| **modal** | Native `<dialog>` | Browser focus trap via `showModal()`. No change needed. |
| **drawer** | Native `<dialog>` | Same as modal. No change needed. |
| **dropdown_menu** | Alpine x-data | Manual: `close($refs.trigger)` returns focus. No trap (dropdown closes on outside click). |
| **dropdown_select** | Alpine x-data | Manual `focusedIndex` + `keyDown`/`keyUp` for arrow keys. Could use `$focus`. |

---

## Scope

### In Scope

1. Add `@alpinejs/focus` to app_layout and app_shell_layout
2. Add `x-trap.inert.noscroll` to tray and modal_overlay panels
3. Evaluate removing body overflow `Alpine.effect` (x-trap.noscroll may supersede)
4. Update PLAN-chirpui-alpine-migration.md with Focus dependency

### Out of Scope (Future)

- Refactor dropdown_select to use `$focus.wrap().next()/.previous()` — current impl works
- modal.html / drawer.html — native dialog already traps focus

---

## Implementation Plan

### Phase 1: Add Focus Plugin

**Files:** `app_layout.html`, `app_shell_layout.html`

Add script before Alpine core (after Intersect):

```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.14.0/dist/cdn.min.js"></script>
```

**Order:** Mask → Intersect → Focus → Alpine

**Deliverable:** `x-trap` and `$focus` available in app templates.

---

### Phase 2: Add x-trap to Tray

**File:** `tray.html`

Add `x-trap.inert.noscroll` to the panel div. The trap expression must be the open state for this tray.

**Before:**
```html
<div class="chirpui-tray__panel">
```

**After:**
```html
<div class="chirpui-tray__panel" x-trap.inert.noscroll="$store.trays['{{ id }}']">
```

**Considerations:**
- x-trap activates when `$store.trays['id']` is true
- `.inert` — siblings (backdrop, etc.) get aria-hidden when trap active; Focus plugin handles this
- `.noscroll` — body scroll disabled when trap active
- Focus returns to trigger on close: tray_trigger is a button, but it's not in the same x-data scope as the tray. The Focus plugin returns focus to "where it was previously" — the element that was focused before the trap engaged. When user clicks tray_trigger, that button had focus; when tray opens, focus moves into panel. When tray closes, Focus should return to the trigger. **Caveat:** tray_trigger and tray are separate components; the "previous" focus might be the trigger if it was the last focused element. Need to verify.

**Focus return behavior:** Alpine Focus stores the last focused element before trap engages. When trap disengages, it restores focus there. The trigger button receives the click, so it had focus (or the click target). When we open the tray, focus moves into the panel (first focusable = close button or first input). When we close via backdrop click or close button, the "previous" focus would be the close button (last in trap) — not ideal. Actually the plugin docs say it stores "where focus was previously" before the trap. So when user clicks "Open", the trigger had focus. Trap engages, focus moves to first focusable in panel. When trap disengages, focus returns to trigger. Good.

**Deliverable:** Tray has focus trap, inert, noscroll.

---

### Phase 3: Add x-trap to Modal Overlay

**File:** `modal_overlay.html`

Same pattern as tray:

```html
<div class="chirpui-modal__panel" x-trap.inert.noscroll="$store.modals['{{ id }}']">
```

**Deliverable:** Modal overlay has focus trap, inert, noscroll.

---

### Phase 4: Body Overflow Effect

**File:** `app_shell_layout.html` (and app_layout if it has the same effect)

**Current:** Alpine.effect toggles `document.body.style.overflow` when any modal or tray is open.

**Options:**
- **A) Keep effect** — Redundant with x-trap.noscroll but harmless. Belt-and-suspenders.
- **B) Remove effect** — Rely on x-trap.noscroll per-dialog. Each tray/modal manages its own. When last one closes, noscroll disengages.

**Recommendation:** **B** — Remove the effect. x-trap.noscroll is the standard approach. Simpler mental model: each dialog owns its scroll lock.

**Caveat:** The effect runs when `any` modal or tray is open. With x-trap.noscroll, each dialog has its own trap. When tray "filters" opens, its panel has x-trap.noscroll="true" (when $store.trays['filters'] is true). So that one panel's trap engages. When we have multiple trays (uncommon), each would have its own trap. Nested modals: Focus plugin handles nesting. So we're good.

**Deliverable:** Remove Alpine.effect for body overflow from app_shell_layout and app_layout (if present).

---

### Phase 5: Tests and Docs

**Tests:**
- Verify tray template renders `x-trap.inert.noscroll`
- Verify modal_overlay template renders `x-trap.inert.noscroll`
- Optional: integration test that focus is trapped (would require Playwright/puppeteer)

**Docs:**
- Update PLAN-chirpui-alpine-migration.md: add Focus to Dependencies
- Add note: "Focus plugin: x-trap on tray and modal_overlay for accessibility"

---

## Rollback

- Revert template changes; remove Focus script
- Restore body overflow Alpine.effect if removed
- No data migration; purely frontend

---

## Acceptance Criteria

- [x] @alpinejs/focus loaded in app_layout and app_shell_layout
- [x] tray panel has x-trap.inert.noscroll
- [x] modal_overlay panel has x-trap.inert.noscroll
- [x] Body scroll locks when tray/modal open (via x-trap.noscroll)
- [x] Focus returns to trigger when tray/modal closed (Focus plugin default)
- [x] Tab cycles only within open tray/modal (x-trap)
- [x] Body overflow Alpine.effect removed
- [x] Tests pass (test_tray_emits_dispatch, test_modal_overlay_emits_dispatch assert x-trap)
- [x] PLAN-chirpui-alpine-migration.md updated

---

## Chirp Apps (Dori, etc.)

Apps using Chirp's `alpine=True` injection get Alpine from Chirp (not from app_shell_layout). Chirp's `alpine_snippet` now includes @alpinejs/focus before Alpine core, so tray and modal_overlay work in Dori and any Chirp app with alpine=True. No app changes needed.

## References

- [Alpine Focus Plugin](https://alpinejs.dev/plugins/focus)
- [WCAG 2.1 Focus Management (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [Tabbable](https://github.com/focus-trap/tabbable) — used internally by Focus plugin
