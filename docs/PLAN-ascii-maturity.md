# Epic: ASCII Component Maturity — Tests, A11y, and Interactive Variants

**Status**: Partially Complete
**Created**: 2026-04-09
**Target**: 0.3.0
**Estimated Effort**: 16–24h
**Dependencies**: None (ASCII components are self-contained)
**Source**: Codebase exploration — 24 ASCII components with 0 dedicated tests, no keyboard support, no documentation

---

## Why This Matters

The ASCII component family (24 components) is one of chirp-ui's most distinctive features — a full terminal-aesthetic UI toolkit in pure CSS and Unicode box-drawing. But it ships with zero dedicated test coverage, inconsistent accessibility, and no public documentation. This undermines trust in the very feature that differentiates the library.

1. **Zero test coverage** — none of the 24 ASCII components have dedicated render tests; a CSS class rename or macro signature change could break them silently
2. **No keyboard support on interactive controls** — `ascii_knob`, `ascii_fader`, `ascii_toggle`, `ascii_checkbox`, `ascii_radio` render as visual-only; screen reader users and keyboard navigators are locked out
3. **Missing interactive composite variants** — the family covers controls (knob, fader, toggle) and display (7seg, sparkline, table) but has no ASCII card, tabs, or modal — the three most-used composites in the library
4. **No public documentation** — 24 components with no site page, no usage examples, no variant gallery
5. **Variant validation gaps** — some ASCII components accept variant strings without routing through `validate_variant()`

### Evidence Table

| Source | Finding | Proposal Impact |
|--------|---------|-----------------|
| test_components.py | 0/24 ASCII components have dedicated tests | FIXES — Sprint 1 adds full render tests |
| Template grep | 15 @click handlers lack @keydown equivalents across library; ASCII controls among them | FIXES — Sprint 2 adds keyboard support to interactive ASCII controls |
| Template inventory | No ascii_card, ascii_tabs, ascii_modal exist | FIXES — Sprint 3 adds 3 interactive composites |
| site/content/ | No ASCII documentation page | FIXES — Sprint 4 adds docs + showcase |
| validation.py | Some ASCII components skip validate_variant() | FIXES — Sprint 1 normalizes validation |

---

### Invariants

These must remain true throughout or we stop and reassess:

1. **CSS contract holds**: every `chirpui-ascii-*` class referenced in templates exists in `chirpui.css` (enforced by `test_template_css_contract.py`)
2. **No JavaScript in ASCII macros**: the family stays pure CSS + Alpine `x-data` attributes only — no `<script>` tags
3. **Existing macro signatures don't break**: new parameters are additive; no existing call site needs updating

---

## Target Architecture

After this epic, the ASCII family will have:

```
24 existing components  →  27 components (+ ascii_card, ascii_tabs, ascii_modal)
 0 dedicated tests      →  ~80 render tests (3+ per component)
 0 keyboard handlers    →  5 interactive controls with @keydown support
 0 docs pages           →  1 site page with variant gallery + usage examples
```

Every interactive ASCII control (`knob`, `fader`, `toggle`, `checkbox`, `radio`) will support:
- Arrow key increment/decrement (knob, fader)
- Space/Enter toggle (toggle, checkbox, radio)
- `aria-label`, `aria-valuenow`/`aria-checked` as appropriate
- `role` attributes matching semantic function

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: audit all 24 ASCII macros, catalog signatures and gaps | 2h | Low | Yes (audit doc only) |
| 1 | Render tests for all 24 existing components | 6–8h | Low | Yes |
| 2 | A11y + keyboard support for 5 interactive ASCII controls | 4–6h | Medium | Yes |
| 3 | Three new interactive composites: ascii_card, ascii_tabs, ascii_modal | 4–6h | Medium | Yes |
| 4 | Documentation: site page + showcase integration | 2–4h | Low | Yes |

---

## Sprint 0: Audit & Design

**Goal**: Catalog every ASCII component's macro signature, variants, a11y state, and test needs — solve design questions before writing code.

### Task 0.1 — Signature Audit

Read all 24 `ascii_*.html` templates. For each, record:
- Macro name and parameters (with defaults)
- Whether it uses `validate_variant()` / `validate_size()`
- ARIA attributes present/absent
- Interactive behavior (Alpine `x-data`, `@click`, `@keydown`)

**Files**: `src/chirp_ui/templates/chirpui/ascii_*.html`
**Acceptance**: Markdown table with 24 rows covering all fields above

### Task 0.2 — Keyboard Design

For each interactive ASCII control, design the keyboard interaction:
- `ascii_knob`: Arrow Up/Down to change value, Home/End for min/max
- `ascii_fader`: Arrow Up/Down, same as knob
- `ascii_toggle`: Space to toggle
- `ascii_checkbox`: Space to toggle
- `ascii_radio`: Arrow Up/Down to cycle within group

**Acceptance**: Keyboard interaction spec written; each control maps to a WAI-ARIA pattern (slider, switch, checkbox, radio)

### Task 0.3 — Composite Design

Sketch macro signatures for the three new composites:
- `ascii_card(title, variant, cls)` — box-drawn border, optional header divider
- `ascii_tabs(items, active, variant, cls)` — tab bar with box-drawing selection indicator
- `ascii_modal(title, variant, cls)` — box-drawn overlay with close button

**Acceptance**: Macro signatures written with expected HTML output sketched

---

## Sprint 1: Render Tests

**Goal**: Every existing ASCII component has at least 3 render tests covering default output, variant application, and custom class passthrough.

### Task 1.1 — Test Scaffolding

Add an `ascii` test section in `tests/test_components.py` (or a new `tests/test_ascii_components.py` if the file is already large).

**Files**: `tests/test_components.py` or `tests/test_ascii_components.py`
**Acceptance**: Test file imports and fixture setup pass; `uv run pytest tests/test_ascii_components.py -q` exits 0

### Task 1.2 — Render Tests for Display Components (12)

Cover: `ascii_7seg`, `ascii_badge`, `ascii_border`, `ascii_divider`, `ascii_empty`, `ascii_error`, `ascii_icon`, `ascii_indicator`, `ascii_progress`, `ascii_skeleton`, `ascii_sparkline`, `ascii_spinner`

Each component gets:
1. Default render (no args beyond required)
2. Variant render (each declared variant)
3. Custom `cls=` passthrough
4. Content slot (where applicable)

**Acceptance**: `uv run pytest tests/test_ascii_components.py -k display -q` — all pass

### Task 1.3 — Render Tests for Control Components (8)

Cover: `ascii_checkbox`, `ascii_fader`, `ascii_knob`, `ascii_radio`, `ascii_toggle`, `ascii_breaker_panel`, `ascii_stepper`, `ascii_tile_btn`

Same 4-test pattern plus:
5. Alpine `x-data` attribute present on interactive controls

**Acceptance**: `uv run pytest tests/test_ascii_components.py -k control -q` — all pass

### Task 1.4 — Render Tests for Data Components (4)

Cover: `ascii_table`, `ascii_ticker`, `ascii_split_flap`, `ascii_vu_meter`

Same 4-test pattern plus:
5. Data rendering (rows for table, digits for split_flap, level for vu_meter)

**Acceptance**: `uv run pytest tests/test_ascii_components.py -k data -q` — all pass

### Task 1.5 — Validation Normalization

Ensure all 24 ASCII components route their `variant` parameter through `validate_variant()`. Fix any that accept raw strings.

**Files**: `src/chirp_ui/templates/chirpui/ascii_*.html`, `src/chirp_ui/validation.py`
**Acceptance**: `rg 'variant' src/chirp_ui/templates/chirpui/ascii_*.html` shows `validate_variant` in every file that accepts a variant parameter

---

## Sprint 2: Accessibility & Keyboard Support

**Goal**: The 5 interactive ASCII controls (knob, fader, toggle, checkbox, radio) gain proper ARIA roles and keyboard interaction.

### Task 2.1 — ARIA Attributes

Add semantic roles and states:

| Control | `role` | Key ARIA attrs |
|---------|--------|----------------|
| `ascii_knob` | `slider` | `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-label` |
| `ascii_fader` | `slider` | same as knob |
| `ascii_toggle` | `switch` | `aria-checked`, `aria-label` |
| `ascii_checkbox` | `checkbox` | `aria-checked`, `aria-label` |
| `ascii_radio` | `radio` | `aria-checked`, `aria-label` |

**Files**: `src/chirp_ui/templates/chirpui/ascii_knob.html`, `ascii_fader.html`, `ascii_toggle.html`, `ascii_checkbox.html`, `ascii_radio.html`
**Acceptance**: `rg 'role=' src/chirp_ui/templates/chirpui/ascii_{knob,fader,toggle,checkbox,radio}.html` returns matches for all 5

### Task 2.2 — Keyboard Handlers

Add `@keydown` handlers alongside existing `@click`:

- Slider controls (knob, fader): `@keydown.up.prevent`, `@keydown.down.prevent`, `@keydown.home.prevent`, `@keydown.end.prevent`
- Toggle controls (toggle, checkbox): `@keydown.space.prevent`
- Radio: `@keydown.up.prevent`, `@keydown.down.prevent` to cycle

Add `tabindex="0"` to make controls focusable.

**Files**: same 5 templates
**Acceptance**: Each control has at least 2 `@keydown` handlers; `tabindex="0"` present

### Task 2.3 — A11y Render Tests

Add tests verifying ARIA attributes and keyboard attributes are present in rendered output.

**Files**: `tests/test_ascii_components.py`
**Acceptance**: `uv run pytest tests/test_ascii_components.py -k a11y -q` — all pass

---

## Sprint 3: Interactive Composites

**Goal**: Add `ascii_card`, `ascii_tabs`, and `ascii_modal` — box-drawn variants of the three most-used composites.

### Task 3.1 — ascii_card

Box-drawn card with Unicode borders (╭─╮│╰─╯), optional title bar with divider, content slot.

```
╭─── Title ────────────╮
│ Content here          │
╰───────────────────────╯
```

**Files**: `src/chirp_ui/templates/chirpui/ascii_card.html`, `src/chirp_ui/templates/chirpui.css`
**Acceptance**: Renders box-drawn border; variant classes applied; CSS contract test passes; 4+ render tests

### Task 3.2 — ascii_tabs

Tab bar using box-drawing characters, active tab highlighted:

```
┌─────┐
│ Tab1 │ Tab2   Tab3
└──────┴────────────────
```

**Files**: `src/chirp_ui/templates/chirpui/ascii_tabs.html`, `src/chirp_ui/templates/chirpui.css`
**Acceptance**: Renders tab bar; active tab distinguished; `role="tablist"` present; 4+ render tests

### Task 3.3 — ascii_modal

Box-drawn dialog overlay with title bar and close button:

```
╔══════════════════════╗
║  Title          [×]  ║
╠══════════════════════╣
║ Content              ║
╚══════════════════════╝
```

Uses `<dialog>` element (native modal), styled with box-drawing.

**Files**: `src/chirp_ui/templates/chirpui/ascii_modal.html`, `src/chirp_ui/templates/chirpui.css`
**Acceptance**: Uses `<dialog>`; box-drawn border renders; `aria-label` on close button; 4+ render tests

### Task 3.4 — CSS & Validation

Add `chirpui-ascii-card`, `chirpui-ascii-tabs`, `chirpui-ascii-modal` classes to `chirpui.css`. Register any new variants in `VARIANT_REGISTRY`.

**Acceptance**: `uv run poe ci` passes (includes CSS contract, transition tokens, all tests)

---

## Sprint 4: Documentation & Showcase

**Goal**: ASCII components become discoverable — public docs page and showcase integration.

### Task 4.1 — Showcase Page

Add or enhance the ASCII showcase category in the dynamic component showcase. Show every ASCII component with each variant.

**Files**: `examples/component-showcase/templates/showcase/ascii-primitives.html`
**Acceptance**: Showcase page renders all 27 ASCII components; accessible via showcase navigation

### Task 4.2 — Site Documentation

Add `site/content/docs/components/ascii.md` with:
- Family overview and design philosophy
- Per-component usage examples (macro call + rendered output)
- Variant gallery
- Keyboard interaction table for interactive controls
- When to use ASCII vs standard components

**Files**: `site/content/docs/components/ascii.md`
**Acceptance**: `uv run poe docs-build` succeeds; page renders in local preview

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Keyboard handlers conflict with Alpine page-level listeners | Medium | Medium | Sprint 0 Task 0.2 designs interactions against WAI-ARIA patterns; test in browser |
| New composites duplicate existing component logic | Low | Low | ascii_modal wraps native `<dialog>`, ascii_tabs reuses tablist role — no logic duplication |
| CSS additions bloat chirpui.css beyond acceptable size | Low | Low | ASCII styles are lightweight (box-drawing + monospace); ~50 lines per component |
| Variant validation changes break existing ASCII usage | Medium | High | Sprint 1 Task 1.5 adds tests first, then normalizes; invariant #3 protects signatures |

---

## Success Metrics

| Metric | Current | After Sprint 1 | After Sprint 4 |
|--------|---------|----------------|----------------|
| ASCII components with ≥1 test | 0 / 24 (0%) | 24 / 24 (100%) | 27 / 27 (100%) |
| ASCII render tests | 0 | ~80 | ~95 |
| Interactive ASCII controls with keyboard support | 0 / 5 | 0 / 5 | 5 / 5 |
| Interactive ASCII controls with ARIA roles | 0 / 5 | 0 / 5 | 5 / 5 |
| ASCII components in public docs | 0 | 0 | 27 |
| New ASCII composites | 0 | 0 | 3 |

---

## Relationship to Existing Work

- **PLAN-primitives-and-components.md** — parallel; that plan focuses on layout/surface primitives, this focuses on ASCII family. No overlap.
- **PLAN-modern-css-backgrounds.md** — parallel; background effects are a separate visual family. ASCII and effects could share a "decorative" showcase section.
- **Adoption flywheel** — ASCII components are a differentiator. Making them documented and testable supports the kida/chirp/chirp-ui adoption story.

---

## Changelog

- **2026-04-10**: Sprint 1 (render tests) complete — shipped in PLAN-behavior-layer-hardening Sprint 1 / PR #40 (152 tests across 27 ASCII component classes in `test_ascii_components.py`). Sprint 0 (audit) also complete via PLAN-behavior-layer-hardening Sprint 0. Remaining: Sprint 2 (a11y/keyboard), Sprint 3 (composites ascii_card/tabs/modal already exist), Sprint 4 (docs).
- **2026-04-09**: Draft created from codebase exploration. 24 existing components audited; 0 tests, 0 docs, 5 interactive controls without keyboard support identified.
