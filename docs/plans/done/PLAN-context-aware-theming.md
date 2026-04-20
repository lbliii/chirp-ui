# Epic: Context-Aware Component Theming — Surface-Sensitive Rendering

**Status**: Complete (Sprint 3.1 progress bar deferred)
**Created**: 2026-04-12
**Target**: 0.3.1
**Estimated Effort**: 10–14h
**Dependencies**: PLAN-provide-consume-expansion (complete), kida >= 0.3.4
**Source**: Codebase audit of 16 providers / 23 consumers; gap analysis of 8 candidate components

---

## Why This Matters

Provide/consume v1 wired the plumbing: 16 providers push context, 23 consumers read it. But most consumers only use context for **identity** (badge inherits variant name, accordion item inherits group name). Only a few use it for **adaptation** — adjusting their visual treatment based on where they're rendered.

The result: a timeline inside a `surface(variant="muted")` looks identical to one in the default surface. A callout inside a dark card uses the same background luminosity as one on a white page. Components know *what* their parent is, but don't *respond* to it.

### Consequences

1. **Visual inconsistency in composite layouts** — Timeline dots use fixed `--chirpui-fg-muted` regardless of surface background, causing low contrast on darker surfaces.
2. **Callout/surface clashing** — A `callout(variant="info")` inside `surface(variant="accent")` produces competing blue tones with no automatic adjustment.
3. **Settings rows ignore card context** — `settings_row_list(hoverable=true)` uses a fixed hover background that may be invisible on non-default cards. (Settings row uses `badge()` internally, which already consumes — but the row's own hover doesn't adapt.)
4. **Progress bar color is context-blind** — Progress bars inside glass/elevated surfaces don't adjust saturation, appearing either washed-out or oversaturated.
5. **KEYS.md accuracy gap** — `label_overline` is listed as a consumer of `_surface_variant` and `_card_variant`, but the template has no `consume()` call. The docs promise behavior that doesn't exist.

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| timeline.html | Dot/line color uses fixed CSS vars; no `consume()` | FIXES — consumes `_surface_variant`, applies contrast-aware class |
| callout.html | Background luminosity fixed per variant; no surface awareness | FIXES — consumes `_surface_variant`, modulates background via CSS class |
| status.html | Dot color fixed; no card/surface awareness | FIXES — consumes `_surface_variant` for contrast hinting |
| settings_row.html | Hover bg fixed; badge already consumes but row doesn't | FIXES — row-level hover adapts to card context |
| progress.html | Color saturation fixed; no surface awareness | MITIGATES — CSS custom property override on surface-aware class |
| KEYS.md line 28 | Claims label_overline consumes `_surface_variant` + `_card_variant` | FIXES — removes inaccurate claim (label_overline is typographic-only, consuming is a CSS no-op) |
| description_list.html | Row backgrounds fixed in dark card context | MITIGATES — low priority, works adequately |
| media_object.html | Layout primitive, no theming | UNRELATED — skip |

### The Fix

Add `consume("_surface_variant", "")` to 4–5 components (timeline, callout, status, settings_row, optionally progress) with corresponding CSS modifier classes that adjust contrast, luminosity, or saturation based on the inherited surface context. Fix KEYS.md accuracy. This is the "last mile" of provide/consume — making context flow produce visible changes, not just pass names through.

---

### Invariants

These must remain true throughout or we stop and reassess:

1. **No visual change without context** — Components rendered standalone (no parent provide) must look exactly as they do today. Every new CSS class is gated on a modifier that only appears when a context value is consumed.
2. **Explicit params always win** — Same invariant as v1. `consume()` is fallback only.
3. **Full test suite passes at every sprint** — `uv run poe ci` is the gate. No regressions.

---

## Target Architecture

### CSS Strategy: Surface-Aware Modifier Classes

Rather than complex `color-mix()` calculations in each component, the approach uses a single modifier class pattern:

```css
/* Component adapts to surface context via modifier */
.chirpui-timeline--on-muted .chirpui-timeline__dot {
    border-color: var(--chirpui-fg);  /* higher contrast on muted bg */
}
.chirpui-callout--on-accent {
    --chirpui-callout-bg-alpha: 0.12;  /* reduce bg opacity on accent surface */
}
```

Template consume pattern:
```jinja2
{% set _surface = consume("_surface_variant", "") %}
{% set _on_surface = " chirpui-timeline--on-" ~ _surface if _surface else "" %}
```

### Which Surfaces Trigger Adaptation

Only non-default surfaces trigger a modifier class. When `_surface_variant` is `""` or `"default"`, no modifier is added — preserving current behavior exactly.

Meaningful surface contexts: `muted`, `accent`, `elevated`, `glass`, `feature`.

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: CSS modifier pattern, audit contrast needs | 2h | Low | Yes (RFC only) |
| 1 | Timeline + callout surface adaptation | 4h | Low | Yes |
| 2 | Status + settings_row card/surface adaptation | 3h | Low | Yes |
| 3 | Progress bar (optional) + KEYS.md fix + doc cleanup | 2h | Low | Yes |
| 4 | Tests + showcase examples | 3h | Low | Yes |

---

## Sprint 0: Design & Validate

**Goal**: Validate the CSS modifier pattern and determine which surface variants need adaptation rules for each component.

### Task 0.1 — Prototype `--on-<surface>` modifier for timeline

Create a scratch CSS rule for `.chirpui-timeline--on-muted` and verify that the dot/line contrast improves on a muted surface. Test in the component showcase.

**Acceptance**: Visual confirmation that timeline dots are more visible on muted surfaces. Screenshot or showcase verification.

### Task 0.2 — Enumerate surface variants that need adaptation

For each target component, document which of the 5 surface contexts (`muted`, `accent`, `elevated`, `glass`, `feature`) actually need a CSS rule vs. which look fine as-is.

**Acceptance**: Decision matrix documented in this plan (Sprint 0 changelog).

### Task 0.3 — Validate consume + modifier pattern in kida

Test that `consume("_surface_variant", "")` inside `timeline_item()` (which is called inside `timeline()`'s slot) correctly reads the value provided by a `surface()` ancestor.

**Files**: Manual test or `tests/test_provide_consume.py` addition.
**Acceptance**: `consume()` inside a deeply-nested macro correctly reads the surface's provided value.

---

## Sprint 1: Timeline + Callout Surface Adaptation

**Goal**: Timeline dot/line and callout background adapt to their surface context.

### Task 1.1 — `timeline()` consumes `_surface_variant`

Add `consume("_surface_variant", "")` to both `timeline()` and `timeline_item()`. Apply `--on-<surface>` modifier class to the timeline container.

**Files**: `src/chirp_ui/templates/chirpui/timeline.html`
**Acceptance**: `rg 'consume.*_surface_variant' src/chirp_ui/templates/chirpui/timeline.html` returns a hit.

### Task 1.2 — CSS for timeline surface adaptation

Add `.chirpui-timeline--on-muted`, `--on-accent`, `--on-elevated` rules. Adjust dot border-color and line color for contrast.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `.chirpui-timeline--on-muted` exists in CSS. `test_template_css_contract.py` passes.

### Task 1.3 — `callout()` consumes `_surface_variant`

Add `consume("_surface_variant", "")` and apply `--on-<surface>` modifier class.

**Files**: `src/chirp_ui/templates/chirpui/callout.html`
**Acceptance**: `rg 'consume.*_surface_variant' src/chirp_ui/templates/chirpui/callout.html` returns a hit.

### Task 1.4 — CSS for callout surface adaptation

Add rules that reduce callout background opacity on accent/elevated surfaces to prevent color clashing.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `.chirpui-callout--on-accent` exists in CSS.

### Task 1.5 — Tests for Sprint 1

Three tests per component: standalone (no change), inside surface (modifier present), explicit variant overrides.

**Acceptance**: `uv run pytest tests/test_provide_consume.py -k "TimelineSurface or CalloutSurface" -q` passes.

---

## Sprint 2: Status + Settings Row Adaptation

**Goal**: Status indicator contrast and settings row hover adapt to card/surface context.

### Task 2.1 — `status_indicator()` consumes `_surface_variant`

Add `consume("_surface_variant", "")` with `--on-<surface>` modifier.

**Files**: `src/chirp_ui/templates/chirpui/status.html`
**Acceptance**: `rg 'consume.*_surface_variant' src/chirp_ui/templates/chirpui/status.html` returns a hit.

### Task 2.2 — CSS for status surface adaptation

Adjust dot opacity/border on non-default surfaces for visibility.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `.chirpui-status-indicator--on-muted` exists in CSS.

### Task 2.3 — `settings_row_list()` consumes `_card_variant`

Row hover background should adapt when inside a non-default card.

**Files**: `src/chirp_ui/templates/chirpui/settings_row.html`
**Acceptance**: `rg 'consume.*_card_variant' src/chirp_ui/templates/chirpui/settings_row.html` returns a hit.

### Task 2.4 — CSS for settings row card adaptation

Adjust `--hoverable` hover background on non-default card surfaces.

**Files**: `src/chirp_ui/templates/chirpui.css`
**Acceptance**: `.chirpui-settings-row-list--on-feature` (or similar) exists in CSS.

### Task 2.5 — Tests for Sprint 2

**Acceptance**: `uv run pytest tests/test_provide_consume.py -k "StatusSurface or SettingsRowCard" -q` passes.

---

## Sprint 3: Progress Bar + Doc Cleanup

**Goal**: Optional progress bar adaptation. Fix KEYS.md accuracy. Clean up aspirational claims.

### Task 3.1 — (Optional) `progress()` consumes `_surface_variant`

If Sprint 0 design review shows meaningful contrast improvement, add consume to progress bar with saturation adjustment CSS.

**Files**: `src/chirp_ui/templates/chirpui/progress.html`, `chirpui.css`
**Acceptance**: If implemented, `rg 'consume.*_surface_variant' src/chirp_ui/templates/chirpui/progress.html` returns a hit.

### Task 3.2 — Fix KEYS.md: remove label_overline as consumer

`label_overline.html` is typographic only — consuming surface/card variant would be a CSS no-op. Remove it from the consumer columns in the key registry.

**Files**: `docs/PROVIDE-CONSUME-KEYS.md`
**Acceptance**: `rg 'label_overline' docs/PROVIDE-CONSUME-KEYS.md` returns zero hits in consumer columns (may still appear in other docs as a non-consumer example).

### Task 3.3 — Update KEYS.md with new consumers

Add timeline, callout, status_indicator, settings_row_list to the consumer columns.

**Files**: `docs/PROVIDE-CONSUME-KEYS.md`
**Acceptance**: All new consumers appear in the registry.

---

## Sprint 4: Tests + Showcase

**Goal**: Full test coverage for all new consumers. Showcase examples demonstrating the visual difference.

### Task 4.1 — Comprehensive provide/consume tests

Add test classes for each new consumer following the three-test pattern:
1. Standalone rendering (no context) — unchanged behavior
2. Inside surface/card — modifier class present
3. Explicit param overrides consumed value

**Acceptance**: `uv run pytest tests/test_provide_consume.py -q` passes. All new classes have tests.

### Task 4.2 — Showcase: context-aware composition examples

Add showcase examples showing the same component rendered on default vs. muted vs. accent surfaces, demonstrating automatic visual adaptation.

**Files**: `examples/component-showcase/app.py` or showcase templates
**Acceptance**: Showcase page renders without error. Visual diff is apparent.

### Task 4.3 — Update COMPONENT-OPTIONS.md

Add "Surface-Aware" note to timeline, callout, status, and settings_row sections.

**Acceptance**: `rg 'Surface-Aware' docs/COMPONENT-OPTIONS.md` returns hits for each component.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `--on-<surface>` classes proliferate (5 surfaces × N components) | Medium | Medium | Sprint 0 design review limits to 2-3 meaningful surfaces per component. Most only need `on-muted` and `on-accent` |
| CSS specificity conflicts with existing variant styles | Low | Medium | `--on-<surface>` modifier is additive (adjusts custom properties), not competing with variant classes |
| Consume inside timeline_item not reaching surface ancestor | Low | High | Sprint 0 Task 0.3 validates this before any template changes |
| Visual regressions on existing pages | Low | High | Invariant #1: no modifier class emitted without surface context. Zero visual change for standalone components |
| Over-engineering: surfaces that don't need adaptation get rules | Medium | Low | Sprint 0 Task 0.2 creates decision matrix; rules only added where contrast actually improves |

---

## Success Metrics

| Metric | Current (0.3.0) | After Sprint 2 | After Sprint 4 |
|--------|-----------------|-----------------|-----------------|
| Components with surface adaptation | 3 (badge, divider, alert) | 7 (+timeline, callout, status, settings_row) | 7–8 (+optional progress) |
| `--on-<surface>` CSS rules | 0 | ~8 | ~12 |
| Provide/consume test cases | 45 | 55 | 65 |
| KEYS.md accuracy | ~90% (label_overline gap) | 95% | 100% |

---

## Relationship to Existing Work

- **PLAN-provide-consume-expansion** — prerequisite (complete) — established all providers and the consume pattern. This plan extends consumers with *visual adaptation*, not just identity inheritance.
- **PLAN-color-system-hardening** — parallel — surface adaptation relies on `--chirpui-*` color tokens being correct. Color system hardening (gamma fix, wider regex) is already complete.
- **PLAN-theme-tokens** — parallel — `--on-<surface>` modifiers will use the same token layer. Custom themes that override `--chirpui-success` etc. will automatically flow through surface-aware rules.

---

## Changelog

- **2026-04-12** — Sprints 0-4 implemented. 4 components (timeline, callout, status_indicator, settings_row_list) now surface/card-aware via `--on-<surface>` CSS modifiers. 16 new tests added. KEYS.md accuracy fixed (removed label_overline consumer claim, added actual consumers, updated _bar_density consumers). settings_row_list modifier bug fixed with kida 0.4.0 list comprehension.
- **2026-04-12** — Draft created from gap analysis of 8 candidate components against 16 existing providers.
