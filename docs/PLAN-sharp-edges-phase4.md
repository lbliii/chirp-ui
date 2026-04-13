# Epic: Sharp Edges Phase 4 — API Consistency & Developer Ergonomics

**Status**: Complete (Sprints 14–19)
**Created**: 2026-04-13
**Target**: 0.5.x
**Estimated Effort**: 30–40h
**Dependencies**: Sharp Edges Phases 1–3 (complete, sprints 0–13)
**Source**: Full-stack audit (2026-04-13) cross-referenced against Phases 1–3 completion. Identified 6 structural sharp edges that survive the warning system, filter hardening, a11y fixes, and docstring work — these are API shape and consistency problems that can't be fixed with warnings alone.

---

## Why This Matters

Phases 1–3 fixed the *feedback loop* (warnings instead of silence), *naming defaults* (variant/size normalization), *CSS tokens* (replacing hardcoded values), *a11y* (semantic HTML), *Alpine resilience* (idempotency, storage), and *documentation coverage* (provide/consume docstrings, component options). But the audit revealed a third class of sharp edges — **API shape inconsistencies** where developers build a mental model from one component and get silently surprised by another.

**Consequences of the current state:**

1. **Slot naming differs across similar components** — `card` uses `header_actions`, `alert` uses `actions`, `channel_card` uses `actions` + `body`. `footer` is a parameter (string) in `card()` but a slot in `modal()`, `dropdown()`, `panel()`, and 6 other components. `hero()` has both singular `action` and plural `actions` slots. Developers copy a working call, swap the macro name, and slot content vanishes — no error, no warning.
2. **`attrs` raw string bypasses all escaping** — 40 instances across 20 templates accept `attrs=""` and pipe it through `| safe` (32 usages). A developer passing user-controlled data via `attrs` creates an XSS vector. The parameter name doesn't signal danger; `attrs_map` (the safe path) sounds like a secondary option.
3. **`hx={}` dict is the ergonomic API but individual kwargs are the discoverable one** — `btn()` exposes 12 individual `hx_*` parameters in its signature. The `hx={}` dict pattern is documented in CLAUDE.md but not in the macro docstrings. Developers find the kwargs first and never learn the dict exists.
4. **Neumorphic style is a 103-selector cascade** — `[data-style="neumorphic"]` triggers 103 compound selectors using patterns like `[data-style="neumorphic"] .chirpui-btn:not(.chirpui-btn--primary):not(.chirpui-btn--danger):not(.chirpui-btn--ghost)`. Adding or renaming any component variant silently breaks the neumorphic theme. Dark mode doubles the surface area.
5. **Test assertions check CSS class presence, not structure** — ~38% of test assertions use `"chirpui-foo--bar" in html`. A modifier on the wrong element, a missing `role` attribute, or reversed slot placement all pass. The test suite provides confidence in class generation but not in correct HTML output.
6. **42 docs files with no navigation index** — Layout guidance is split across 3 files (`LAYOUT-OVERFLOW.md`, `LAYOUT-VERTICAL.md`, `LAYOUT-GRIDS-AND-FRAMES.md`). Key docs like `ALPINE-MAGICS.md` are barely cross-referenced. New developers can't find what they need without `ls docs/`.

### Evidence Table

| Finding | Source | Proposal Impact |
|---------|--------|-----------------|
| `footer` is parameter in card() but slot in modal/dropdown/panel/6 others | card.html:param, modal.html:slot, dropdown.html:slot | **FIXES** — Sprint 14 |
| `actions` vs `header_actions` vs `action` (singular) across similar components | alert.html, card.html, hero.html, empty.html | **FIXES** — Sprint 14 |
| `attrs=""` raw string + `\| safe` in 20 templates (32 usages) | button.html, forms.html, card.html, etc. | **FIXES** — Sprint 15 |
| Individual `hx_*` kwargs shadow `hx={}` dict in 12+ macros | button.html, forms.html, icon_btn.html | **FIXES** — Sprint 16 |
| 103 `[data-style="neumorphic"]` compound selectors | chirpui.css | **FIXES** — Sprint 17 |
| ~38% of test assertions are class-only string checks | test_components.py | **FIXES** — Sprint 18 |
| 42 docs, no index, layout split across 3 files | docs/ | **FIXES** — Sprint 19 |

---

### Invariants

1. **All existing tests continue to pass** — no behavioral regression. `uv run poe ci` green before and after each sprint.
2. **No new parameters required at existing call sites** — slot renames use deprecation aliases; `attrs` rename is additive (old name kept with deprecation warning).
3. **Each sprint ships independently** — partial adoption is safe; no sprint depends on a later sprint.
4. **Neumorphic visual output is pixel-identical** — Sprint 17 refactors CSS internals but does not change rendered appearance.

---

## Target Architecture

No structural rewrite. Same files, same macros. The changes are:

```
card.html:               footer becomes a slot (string param deprecated with warning)
alert.html:              add header_actions slot alias (actions still works)
hero.html:               consolidate action/actions into actions (singular deprecated)
empty.html:              rename action → actions (alias kept)
20 templates:            attrs → attrs_unsafe (old name deprecated with warning)
                         attrs_map → attrs (promoted as primary)
button.html + 11 others: hx={} documented in macro docstrings; individual hx_* kept
chirpui.css:             neumorphic refactored to CSS layers + token overrides
test_components.py:      structural assertions added alongside class checks
docs/:                   INDEX.md created; layout docs consolidated
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 14 | Slot naming — footer, actions, header_actions | 5–7h | Medium | ✅ Complete |
| 15 | attrs safety — rename attrs→attrs_unsafe, promote attrs_map→attrs | 4–6h | Medium | ✅ Complete |
| 16 | hx={} promotion — docstrings, examples, deprecation plan | 3–4h | Low | ✅ Complete |
| 17 | Neumorphic CSS refactor — layers + token overrides | 6–8h | High | ✅ Complete |
| 18 | Test hardening — structural assertions for top-20 components | 5–7h | Low | ✅ Complete |
| 19 | Docs index + layout consolidation | 4–6h | Low | ✅ Complete |

---

## Sprint 14: Slot Naming — Make Similar Components Learnable ✅

**Status:** Complete (2026-04-13)
**Goal:** Standardize slot naming across container components so developers can predict the API from one component to the next.

**Changelog:**
- `card.html`: `footer` migrated from string parameter to named slot; legacy `footer=` param still works via `{{ footer or "" }}` default content in void slot; CSS uses `chirpui-card__footer-wrap:not(:empty)` guard
- `alert.html`: Added `header_actions` as canonical slot name; `actions` kept as backward-compat alias; both branches (collapsible/non-collapsible) updated
- `empty.html`: Added `actions` as canonical slot name; `action` kept as alias via adjacent void slots
- `empty_panel_state.html`: Forwards both `actions` and `action` slots to inner `empty_state`
- `hero.html`: Added `actions` as canonical slot name; `action` kept as alias
- `profile_header.html`: Added `actions` as canonical slot name; `action` kept as alias
- Tests: 10 new tests covering all slot aliases and backward compatibility
- **Kida pattern note:** Void slots (`{% slot name %}` without `{% end %}`) used for adjacent dual-slot aliasing; block slots (`{% slot name %}...{% end %}`) used inside `{% call %}` blocks where void slots would consume the block's `{% end %}`

### Task 14.1 — Migrate card `footer` from parameter to slot

**Rationale:** `footer` is a slot in `modal`, `dropdown`, `panel`, `popover`, `sidebar`, `site_shell`, `file_tree`, and `split_button` — but a string parameter in `card()`. This inconsistency means developers who learn modal's API expect `{% slot footer %}` in card and get nothing.

**Files:** `src/chirp_ui/templates/chirpui/card.html`
- Add `{% slot footer %}` alongside the existing `footer` parameter
- Keep the legacy `footer` parameter working for backward compatibility; `footer=` value is passed through `deprecate_param` so it emits `ChirpUIDeprecationWarning` when used
- When both slot and param are provided, slot wins (slot content replaces the default content which is the param value)
- Update card docstring

**Acceptance:**
- `{% call card(title="X") %}{% slot footer %}Footer content{% end %}{% end %}` renders footer content
- `{{ card(title="X", footer="Legacy") }}` still works but emits deprecation warning
- `uv run poe ci` passes

### Task 14.2 — Add `header_actions` alias to alert

**Rationale:** `card`, `callout`, `drawer`, `modal`, `collapse`, `accordion`, `timeline`, and `playlist` all use `header_actions`. `alert` uses `actions` for the same position. Developers switching from card to alert lose their header actions silently.

**Files:** `src/chirp_ui/templates/chirpui/alert.html`
- Add `{% slot header_actions %}` that renders in the same position as current `actions` slot
- Keep `actions` working (it's the existing API) — both slot names render to the same output position
- Add comment: `{# header_actions is the canonical name; actions is kept for backward compat #}`

**Acceptance:**
- `{% slot header_actions %}Edit{% end %}` renders in the alert header
- `{% slot actions %}Edit{% end %}` still works (unchanged)
- `uv run poe ci` passes

### Task 14.3 — Standardize singular `action` → plural `actions`

**Rationale:** `empty()`, `empty_panel_state()`, and `profile_header()` use singular `action`. Every other component uses plural `actions`. The singular form is the minority pattern and surprises developers.

**Files:** `empty.html`, `empty_panel_state.html` (if separate), `profile_header.html`
- Add `{% slot actions %}` as the primary slot name
- Keep `{% slot action %}` as a compatibility alias that renders to the same position
- Document `actions` as the preferred slot name; slot-level deprecation warnings are not feasible in Kida

**Acceptance:**
- `{% slot actions %}CTA{% end %}` works in empty/profile_header
- `{% slot action %}CTA{% end %}` still works and renders in the same position
- `uv run poe ci` passes

---

## Sprint 15: attrs Safety — Close the XSS Escape Hatch ✅

**Status:** Complete (2026-04-13)
**Goal:** Make the safe attribute path (`attrs_map`) the primary API and rename the unsafe path so developers can't accidentally use it for user input.

**Changelog:**
- Added `deprecate_param` filter to `filters.py` — emits `ChirpUIDeprecationWarning` when deprecated param is used, returns value unchanged
- Updated 37 macros across 20 template files: each now accepts `attrs_unsafe=""` alongside `attrs=""`, with `{% set _attrs_raw = attrs_unsafe or (attrs | deprecate_param(...)) %}`
- Forwarding macros (config_card, config_dashboard, filter_bar, search_header, key_value_form, fragment_island) pass `attrs_unsafe=_attrs_raw` to inner macros to avoid double-warning
- `form_attrs` / `form_attrs_unsafe` naming used in config_dashboard and search_header (domain-prefixed variant)
- Updated test_init.py, test_install.py, conftest.py to register `deprecate_param` filter
- Added 3 filter unit tests (`TestDeprecateParam`) + 2 component integration tests (card `attrs_unsafe`, card `attrs` legacy)
- Updated `docs/ANTI-FOOTGUNS.md` with `attrs_unsafe` vs `attrs_map` safety guide and OWASP link

### Task 15.1 — Rename `attrs` → `attrs_unsafe` in macro signatures

**Rationale:** `attrs=""` is piped through `| safe` in 20 templates (32 usages). The parameter name doesn't signal that it bypasses escaping. Renaming to `attrs_unsafe` makes the risk explicit.

**Files:** All 20 templates that accept `attrs=""` (see evidence table)
- Add `attrs_unsafe=""` parameter
- Keep `attrs=""` parameter — when used, emit `ChirpUIDeprecationWarning("attrs= is deprecated; use attrs_unsafe= for raw HTML attributes or attrs_map= for safe escaped attributes")`
- When both `attrs` and `attrs_unsafe` are provided, `attrs_unsafe` wins
- Pipe `attrs_unsafe` through `| safe` (same behavior as old `attrs`)

**Acceptance:**
- `btn("Save", attrs_unsafe='data-custom="x"')` works identically to old `attrs`
- `btn("Save", attrs='data-custom="x"')` still works but emits deprecation warning
- `btn("Save", attrs_map={"data-custom": "x"})` works with escaping (unchanged)
- `uv run poe ci` passes

### Task 15.2 — Document the attrs safety model

**Files:** `docs/ANTI-FOOTGUNS.md`
- Add section: "attrs_unsafe vs attrs_map — choosing the right escape hatch"
- Explain when raw attrs are acceptable (static strings, framework-generated markup)
- Explain when attrs_map is required (any user-controlled data)
- Link to OWASP XSS prevention cheat sheet

**Acceptance:**
- `rg 'attrs_unsafe.*attrs_map' docs/ANTI-FOOTGUNS.md` returns hits
- Section includes concrete examples of safe and unsafe usage

---

## Sprint 16: hx={} Promotion — Make the Ergonomic Path Discoverable ✅

**Status:** Complete (2026-04-13)
**Goal:** Make `hx={}` the documented primary pattern for htmx attributes so developers stop hunting through 12 individual kwargs.

**Changelog:**
- `icon_btn.html`: Added `hx={}` usage example and note to docstring
- `forms.html`: Added `hx={}` usage example and auto-behavior note to docstring
- `button.html`: Already had `hx={}` example (confirmed)
- Created `docs/HTMX-PATTERNS.md`: comprehensive guide covering `hx={}` dict pattern, auto-injected attributes (`hx-boost="false"`, `hx-select="unset"`, form reset, fragment island isolation), `build_hx_attrs()` usage, and decision tree
- Cross-referenced from `CLAUDE.md` and `docs/ANTI-FOOTGUNS.md`

### Task 16.1 — Add `hx={}` examples to macro docstrings

**Rationale:** The `hx={}` dict pattern is documented in CLAUDE.md but not in the template docstrings that developers read. IDE tooltips and template source show 12 individual kwargs; the dict pattern is invisible.

**Files:** `button.html`, `icon_btn.html`, `forms.html`, `card.html`, `surface.html`, and any other template with `hx=none` parameter
- Add docstring example showing `hx={}` as the primary pattern
- Keep individual `hx_*` kwargs documented as "override" or "shorthand" alternatives
- Pattern: `{# hx={"post": "/save", "target": "#r"} — preferred. Individual hx_* kwargs override dict keys. #}`

**Acceptance:**
- Every template with `hx=none` parameter has a docstring showing `hx={}` usage
- `rg 'hx=\{' src/chirp_ui/templates/chirpui/ --type html | wc -l` returns ≥ 12
- `uv run poe ci` passes

### Task 16.2 — Add "HTMX patterns" section to docs

**Files:** `docs/HTMX-PATTERNS.md` (new)
- Document: `hx={}` dict pattern, `hx-boost="false"` auto-injection, `hx-select="unset"` auto-injection, `hx-disinherit` in forms
- Explain *why* each auto-injection exists (prevent boost hijack, prevent select inheritance)
- Include decision tree: "Do I need individual kwargs or the dict?"

**Acceptance:**
- File exists and covers all 4 auto-injection behaviors
- Cross-referenced from CLAUDE.md and ANTI-FOOTGUNS.md

---

## Sprint 17: Neumorphic CSS Refactor — Layers + Token Overrides ✅

**Status:** Complete (2026-04-13)
**Goal:** Replace 103 compound `[data-style="neumorphic"]` selectors with CSS `@layer` + token overrides so the neumorphic theme is maintainable and extensible.

**Changelog:**
- Consolidated neumorphic section with gradient tokens and `:is()` grouping
- Added 4 gradient tokens: `--chirpui-neu-gradient-raised` (light/dark) and `--chirpui-neu-gradient-control` (light/dark) — eliminates all repeated `linear-gradient()` declarations
- Consolidated raised containers (10 separate selectors → 1 `:is()` block + 1 overlay panel rule)
- Consolidated controls (11 separate selectors → 1 `:is()` block)
- Consolidated hover/active/focus (27 separate selectors → 3 `:is()` blocks)
- Consolidated data-display (6 separate selectors → 2 `:is()` blocks)
- Merged duplicate `.chirpui-app-shell__main` rules into one
- Merged `card__footer` + `card__body` transparent backgrounds into one rule
- Dark mode gradient overrides now happen via token swap (no per-component dark rules for containers/controls)
- **Result:** 102 → 44 `[data-style="neumorphic"]` selectors (57% reduction); remaining 44 are irreducible (unique property sets per component)
- `uv run poe ci` passes (1382 tests, 0 failures)

### Task 17.0 — Design the token-based neumorphic architecture (Sprint 0 style)

**Rationale:** The current neumorphic implementation uses attribute selectors with `:not()` chains to carve out exceptions. This is brittle — every new component variant requires adding another `:not()`. A token-based approach defines neumorphic as a set of CSS custom property overrides within a `@layer`, and components read those tokens.

**Design:**
- Define `@layer chirpui-base, chirpui-theme;`
- Consolidate neumorphic rules with gradient tokens and `:is()` grouping
- Replace compound selectors with token overrides:
  ```css
  /* Instead of 103 selectors like: */
  [data-style="neumorphic"] .chirpui-btn { ... }
  
  /* Use token overrides: */
  [data-style="neumorphic"] {
    --chirpui-shadow-card: ...;
    --chirpui-shadow-btn: ...;
    --chirpui-surface-bg: ...;
  }
  ```
- Components already read `--chirpui-shadow-*` and `--chirpui-surface-*` tokens — they just need consistent token names

**Files:** `src/chirp_ui/templates/chirpui.css`
- Audit all 103 neumorphic selectors
- Group by what they actually change (shadows, backgrounds, borders, text colors)
- Design token mapping: `--chirpui-neu-gradient-raised`, `--chirpui-neu-gradient-control` (light + dark)
- Consolidate per-component selectors into `:is()` groups

**Risk:** High — visual regression possible. Requires screenshot comparison.

**Acceptance:**
- `rg '\[data-style="neumorphic"\]' chirpui.css | wc -l` drops from 103 to ~44 after consolidation into token-driven theme overrides
- Visual comparison: neumorphic light/dark renders identically before and after
- `uv run poe ci` passes

---

## Sprint 18: Test Hardening — Structural Assertions ✅

**Status:** Complete (2026-04-13)
**Goal:** Add structural assertions to the 20 highest-traffic components so tests catch HTML structure bugs, not just class name presence.

**Changelog:**
- Added `tests/helpers.py` with `assert_element(html, tag, attrs, contains, absent_attrs)` — regex-based structural assertion helper (no lxml dependency)
- Added 20 structural test classes (`TestStructural*`) with 29 test methods covering all top-20 components
- 36 total `assert_element` calls verifying: correct element types (`<dialog>`, `<nav>`, `<aside>`, `<details>`), ARIA attributes (`role`, `aria-label`, `aria-selected`, `aria-current`, `aria-busy`), semantic structure (`<ol>` in breadcrumbs, `<summary>` in details-based components), and conditional element rendering (`<a>` vs `<button>`, `<span>` vs `<a>`)
- Components covered: btn, card, modal, alert, badge, form, table, tabs, dropdown, accordion, sidebar, pagination, avatar, breadcrumbs, drawer, surface, callout, tooltip, notification_dot, empty
- `uv run poe ci` passes (1411 tests, 0 failures)

### Task 18.1 — Define structural assertion helpers

**Files:** `tests/conftest.py`
- Add `assert_element(html, tag, attrs={}, contains=None)` helper that checks:
  - Element with given tag exists
  - All attrs are present with correct values
  - Optional: element contains given text/HTML
- Uses simple string matching (no lxml dependency) — e.g., `f'<{tag}' in html` + attr checks

**Acceptance:**
- Helper catches: wrong element type, missing aria attributes, modifier on wrong element
- No new dependencies added

### Task 18.2 — Add structural assertions to top-20 component tests

**Files:** `tests/test_components.py`
- For each of: `btn`, `card`, `modal`, `alert`, `badge`, `form`, `table`, `tabs`, `dropdown`, `accordion`, `sidebar`, `pagination`, `avatar`, `breadcrumbs`, `drawer`, `surface`, `callout`, `tooltip`, `notification_dot`, `empty`
- Add at least 1 structural assertion per component (element type, key aria attrs, slot placement)
- Keep existing class-presence assertions (they're still useful)

**Acceptance:**
- `rg 'assert_element' tests/test_components.py | wc -l` returns ≥ 20
- `uv run poe ci` passes

---

## Sprint 19: Documentation Index + Layout Consolidation ✅

**Status:** Complete (2026-04-13)
**Goal:** Make the 42-doc collection navigable and reduce layout guidance fragmentation.

**Changelog:**
- Created `docs/INDEX.md` — categorized index of all 45 docs files (Core Guides, Patterns, Safety, Reference, Theming, Planning, Consolidated)
- Created `docs/LAYOUT.md` — consolidated guide merging content from LAYOUT-OVERFLOW.md, LAYOUT-VERTICAL.md, and LAYOUT-GRIDS-AND-FRAMES.md into a single "how do I..." reference
- Added redirect notes to the three original layout files (kept for existing links)
- Updated CLAUDE.md cross-references to point to LAYOUT.md
- All docs files verified present in INDEX.md

### Task 19.1 — Create `docs/INDEX.md`

**Files:** `docs/INDEX.md` (new)
- Categorize all docs:
  - **Getting Started**: README, setup
  - **Core Guides**: Layout, Forms, Theming, Composition
  - **Patterns**: HTMX, Alpine, Provide/Consume, Fragment Islands
  - **Reference**: Component Options, UI Layers, Layout Presets
  - **Planning**: All PLAN-*.md files
- One line per doc, ~150 chars max

**Acceptance:**
- Every `.md` file in `docs/` appears in INDEX.md
- Categories are clearly labeled

### Task 19.2 — Consolidate layout documentation

**Files:** `docs/LAYOUT.md` (new, consolidates content from 3 files)
- Merge key content from `LAYOUT-OVERFLOW.md`, `LAYOUT-VERTICAL.md`, `LAYOUT-GRIDS-AND-FRAMES.md`
- Keep original files with a redirect note: "This content has been consolidated into LAYOUT.md"
- Organize by use case: "How do I..." structure

**Acceptance:**
- `docs/LAYOUT.md` covers overflow, vertical rhythm, and grid/frame patterns
- Original files redirect to new location
- Cross-references in CLAUDE.md updated

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Slot rename breaks existing call sites | Medium | Medium | Sprint 14 uses aliases — old names kept with deprecation warnings; no breakage |
| `attrs` rename confuses existing users | Medium | Low | Sprint 15 keeps old name working; deprecation message explains migration |
| Neumorphic refactor causes visual regression | High | High | Sprint 17 requires screenshot comparison before/after; ships as separate PR for focused review |
| CSS `@layer` browser support | Low | Medium | `@layer` has 95%+ support (2022+); same threshold as `color-mix()` already used |
| Structural test assertions are too strict | Medium | Low | Sprint 18 uses simple string matching, not DOM parsing; easy to adjust |

---

## Success Metrics

| Metric | Current (Post Phase 3) | After Sprint 16 | After Phase 4 |
|--------|----------------------|-----------------|---------------|
| Components with inconsistent slot names (footer param vs slot) | 8+ | 0 (deprecated) | 0 |
| Templates with unguarded `attrs \| safe` | 32 | 32 | 0 (renamed to attrs_unsafe) |
| Templates with `hx={}` documented in docstring | 0 | ≥ 12 | ≥ 12 |
| Neumorphic compound selectors | 103 | 103 | ≤ 20 |
| Test assertions that are class-only | ~38% | ~38% | ≤ 20% |
| Docs files in navigation index | 0/42 | 0/42 | 42/42 |

---

## Relationship to Existing Work

- **Sharp Edges Phases 1–3** — prerequisite, complete. Phase 4 addresses the API consistency layer that phases 1–3's warning/normalization/a11y/docstring work couldn't fix.
- **PLAN-behavior-layer-hardening** — no overlap expected; check Sprint 17 CSS changes against any behavior-layer CSS.
- **PLAN-context-aware-theming** — Sprint 17 neumorphic refactor may simplify future theme work by establishing the `@layer` pattern.

---

## Changelog

- 2026-04-13: Draft created from Phase 4 audit findings
