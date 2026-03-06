# Proposal: Click-to-Edit Styling Improvements

**Status:** Implemented  
**Date:** 2025-03-06  
**Scope:** `inline_edit_field`, `config_row_editable` in Chirp UI

---

## Summary

Improve discoverability and affordance of Chirp UI's click-to-edit components by applying industry best practices. The current implementation relies on a text "Edit" button only; the value area has no hover feedback, cursor change, or icon, making editability unclear.

---

## Research Summary

### Best Practices (from UX Stack Exchange, PatternFly, Webapphuddle, UX Design World)

1. **Discoverability is the main challenge** — Hover-only affordances are poor; users often don't discover editable fields without explicit cues.

2. **Always-visible or hover-revealed edit icon** — PatternFly, LinkedIn, Tumblr use a pencil icon. Clear indication is required; otherwise users must click/hover each cell to discover editability.

3. **Value-area affordance** — On hover:
   - Background highlight (e.g. butter yellow, off-white, or subtle surface-alt)
   - Border or dashed underline to suggest input-like state
   - `cursor: pointer` on the clickable area

4. **Tooltip on edit control** — "Edit" or "Click to edit" helps screen readers and keyboard users.

5. **Clear visual states** — Distinct view vs edit mode; explicit Save/Cancel (already present).

6. **Icon options** — Pencil (✎) is the universal edit affordance; PatternFly uses `fa-pencil-alt`.

---

## Current State

- **`inline_edit_field.html`**: Display block has `<span class="chirpui-inline-edit__value">{{ value }}</span>` and a ghost button with `{{ edit_label }}` (default "Edit"). No icon, no value-area hover.
- **`config_row.html`**: `config_row_editable` uses `inline_edit_field_display`; no extra styling.
- **CSS**: `.chirpui-inline-edit` has basic layout; `.chirpui-inline-edit__value` has font styling only; `.chirpui-inline-edit__trigger` is flex-shrink; no hover state on value.

---

## Proposed Changes

### 1. Value-area affordance (display mode)

Make the value + trigger area feel like a single clickable unit:

- **Hover on `.chirpui-inline-edit--display`**:
  - Subtle background: `var(--chirpui-surface-alt)` or `color-mix(in srgb, var(--chirpui-accent) 8%, transparent)`
  - Optional: `border-radius: var(--chirpui-radius-sm)` for a contained box
  - `cursor: pointer` on the clickable area
- **Value span** (`.chirpui-inline-edit__value`): Optional `border-bottom: 1px dashed var(--chirpui-border)` on hover to hint at input-like state (subtle; can be opt-in via modifier).

### 2. Edit icon (pencil)

Add a pencil icon to the edit trigger for better discoverability:

- **Option A (recommended):** Icon + text — "Edit" button shows `✎` (U+270E) or `✏` (U+270F) before the label. Keeps text for clarity; icon reinforces editability.
- **Option B:** Icon-only button — Replace "Edit" with icon only; use `title` for tooltip. More compact; matches LinkedIn/Tumblr style.
- **Option C:** Icon on hover — Icon appears when hovering the value area. More subtle than A/B; lower discoverability.

**Recommendation:** Option A — icon + "Edit" text. Chirp UI already uses Unicode for icons (⌕, ⚙, etc.); no new dependencies.

### 3. Tooltip on edit control

Add `title="{{ edit_label }}"` (or "Click to edit" when `edit_label` is "Edit") to the trigger button. Already has `aria-label`; `title` adds native tooltip on hover.

### 4. Config row distinction

`.chirpui-config-row--editable` should be visually distinct from read-only rows:

- Slightly different background on hover for the control column (e.g. `.chirpui-config-row__editable` inherits the inline-edit hover).
- Or: subtle left border/accent on editable rows — `border-inline-start: 2px solid transparent` → on hover `var(--chirpui-accent-dim)`.

### 5. Optional: Click-to-edit on value

Currently only the button triggers edit. Best practice: clicking the value itself could also trigger edit (same UX as clicking the button). This requires wrapping the value in a `<label>` for the trigger or using JavaScript. **Out of scope** for this proposal — HTMX swap is triggered by the button; extending to value click would need `hx-trigger` on a parent or a different structure. **Defer** to a follow-up.

---

## Implementation Plan

### Phase 1: CSS-only (low risk)

1. **`chirpui.css`** — Inline edit section (~737):
   - `.chirpui-inline-edit--display`: Add `cursor: pointer`, `border-radius`, `padding`, `margin` (negative to offset) so the hover box is contained.
   - `.chirpui-inline-edit--display:hover`: `background: var(--chirpui-surface-alt)` or `color-mix(in srgb, var(--chirpui-accent) 8%, transparent)`.
   - `.chirpui-inline-edit__trigger`: Add `title` via JS/CSS — **not possible**; must be in HTML.

2. **`inline_edit_field.html`** — Add `title="{{ edit_label }}"` to the trigger button.

### Phase 2: HTML + CSS

1. **`inline_edit_field.html`** — Add pencil icon to trigger:
   ```html
   <button ... type="button" class="chirpui-inline-edit__trigger ..." title="{{ edit_label }}" aria-label="{{ edit_label }}">
       <span class="chirpui-inline-edit__icon" aria-hidden="true">&#9998;</span>
       {{ edit_label }}
   </button>
   ```
   Or icon-only variant: `{% if edit_label %}{{ edit_label }}{% else %}<span ...>&#9998;</span>{% end %}`

2. **`chirpui.css`** — Style `.chirpui-inline-edit__icon` (font-size, color, opacity).

3. **Optional param** — `edit_icon=true` to show icon; `edit_icon=false` keeps text-only for backward compatibility. Default: `true`.

### Phase 3: Config row (optional)

4. **`chirpui.css`** — `.chirpui-config-row--editable` or `.chirpui-config-row__editable` hover state to align with inline-edit affordance.

---

## Files to Modify

| File | Changes |
|------|---------|
| `chirp_ui/templates/chirpui/inline_edit_field.html` | Add `title`, optional pencil icon (`&#9998;` or `edit_icon` param) |
| `chirp_ui/templates/chirpui.css` | `.chirpui-inline-edit--display` hover, `.chirpui-inline-edit__value` cursor, `.chirpui-inline-edit__icon`, `.chirpui-config-row__editable` hover |

---

## Alternatives Considered

- **Inline SVG pencil:** More control; adds markup. Chirp UI uses Unicode elsewhere; keep consistency.
- **Icon-only button:** More compact; "Edit" text helps. Prefer icon + text.
- **Hover-only icon:** Lower discoverability; research recommends always-visible or hover-revealed on the value area, not the icon.

---

## Backward Compatibility

- All changes are additive (new CSS, optional HTML). Existing `inline_edit_field_display` and `config_row_editable` calls work unchanged.
- If `edit_icon` param is added, default `true` keeps new behavior; `false` preserves old look.

---

## Testing

- Visual check in Dori settings page (uses `config_row_editable`).
- Verify hover states in light and dark themes.
- Ensure `aria-label` and `title` are present for accessibility.
