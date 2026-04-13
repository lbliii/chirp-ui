# Epic: Sharp Edges — Ergonomic, Intuitive, Reliable

**Status**: Complete (all sprints 0–8 implemented)
**Created**: 2026-04-13
**Target**: 0.4.0
**Estimated Effort**: 50–70h (30–50h Phase 1 ✓ + 20–25h Phase 2)
**Dependencies**: None (self-contained; kida 0.4.0 already adopted)
**Source**: Full-stack audit of templates (30+ files), CSS (15,524 lines), Python filters/validation, JS, docs, and test infrastructure. Phase 2 sourced from second full-stack audit (2026-04-13) covering areas the first audit missed.

---

## Why This Matters

chirp-ui has 195 components and a rich design token system, but the developer experience erodes trust in three ways: the library silently does the wrong thing, similar components behave inconsistently, and over half the components are invisible to new users. A component library that can't be learned by pattern-matching forces developers back to reading source on every call.

**Consequences of the current state:**

1. **Silent failures mask bugs** — `validate_variant("xl", ("sm","md","lg"))` silently returns `"sm"`. `register_colors({"brand": "not-a-color"})` succeeds now, fails at render time. `settings_row(status="ready")` renders as muted (not success) because "ready" isn't in the hardcoded word list. Users can't tell "working" from "silently wrong."
2. **Inconsistent naming breaks pattern-matching** — `badge` defaults variant to `"primary"`, `button` to `""`, `alert` to `"info"`. `modal` accepts `size="medium"` while everything else uses `"md"`. Some macros use `cls`, others need `attrs_map`. Users copy a working call, swap the macro name, and get surprised.
3. **Macro signature bloat** — `btn()` has 22 parameters. Interdependent params like `form_action` + `attrs_map` aren't documented as pairs; passing one without the other silently drops HTMX behavior.
4. **CSS undermines its own token system** — 20+ instances of hardcoded `color: white` (breaks dark mode), badges use `0.15rem 0.45rem` padding instead of tokens, breakpoints mix `767px`/`768px`/`48rem`. `--chirpui-spacing-2xs` is used but never defined.
5. **`overflow: hidden` on 55+ components** — tooltips, dropdowns, and timeline icons clip silently when nested inside cards or blocks. No documentation warns about this.
6. **chirpui.js has 3 bugs in 16 lines** — `localStorage` throws in Safari private browsing (no try/catch), `data-theme="system"` has no matching CSS rule, and the script must be synchronous but nothing enforces or documents this.
7. **54% of components are undocumented** — 106 of 195 templates have no entry in COMPONENT-OPTIONS.md, including visual effects, ASCII components, and core interactive widgets like `accordion`, `carousel`, and `pagination`.
8. **Test stubs diverge from real filters** — `conftest.py` stubs check `dict` instead of `Mapping`, ignore strict mode, and use different serialization logic. Green CI, broken runtime.
9. **No "X vs Y" guidance** — `modal` vs `tray` vs `drawer`, `card` vs `resource_card` vs `config_card`, `filter_bar` vs `filter_chips` — overlapping components with no decision criteria.
10. **Undocumented context propagation** — `badge`, `callout`, `settings_row` consume `_card_variant`/`_surface_variant` from ancestors via provide/consume. Moving a component changes its appearance with no code change and no warning.

**The fix:** Six focused sprints — design first, then harden the feedback loop (warnings), normalize the API surface, fix CSS/JS correctness bugs, align test infrastructure, and close the documentation gap.

### Evidence Table

| Finding | Source | Proposal Impact |
|---------|--------|-----------------|
| `validate_variant` silently returns first allowed value | `filters.py:354-369` | **FIXES** — Sprint 1 |
| `register_colors` accepts invalid colors, fails at render | `filters.py:70-76` | **FIXES** — Sprint 1 |
| `settings_row` auto-detect misses common status words | `settings_row.html:30-34` | **FIXES** — Sprint 1 |
| `register_filters` skips globals silently | `filters.py:579` | **FIXES** — Sprint 1 |
| Variant defaults differ: `""`, `"primary"`, `"info"`, `"default"` | badge, button, alert, status_indicator | **FIXES** — Sprint 2 |
| Size vocabulary: `"md"` vs `"medium"` vs `none` | modal vs avatar vs skeleton | **FIXES** — Sprint 2 |
| `btn()` has 22 parameters | `button.html:11-15` | **FIXES** — Sprint 2 |
| `color: white` hardcoded 20+ times | chirpui.css (multiple) | **FIXES** — Sprint 3 |
| `--chirpui-spacing-2xs` used but undefined | chirpui.css:11614 | **FIXES** — Sprint 3 |
| Breakpoints mix px/rem units | chirpui.css:2002, 11327 | **FIXES** — Sprint 3 |
| `localStorage` throws in Safari private browsing | chirpui.js:11 | **FIXES** — Sprint 3 |
| `data-theme="system"` has no CSS rule | chirpui.js + chirpui.css | **FIXES** — Sprint 3 |
| conftest stubs check `dict` not `Mapping` | conftest.py:35 | **FIXES** — Sprint 4 |
| conftest stubs ignore strict mode | conftest.py:64-70 | **FIXES** — Sprint 4 |
| 106/195 templates undocumented | COMPONENT-OPTIONS.md vs templates/ | **FIXES** — Sprint 5 |
| No modal/tray/drawer decision tree | docs/ | **FIXES** — Sprint 5 |
| `overflow: hidden` clips nested content | 55+ CSS rules | **MITIGATES** — Sprint 3 (document + selective fix) |
| Legacy + modern slot patterns coexist | post_card, card, channel_card | **MITIGATES** — Sprint 2 (deprecation markers) |
| Undocumented provide/consume inheritance | badge, callout, settings_row | **MITIGATES** — Sprint 5 (document) |
| `segmented_control` macro name collision | forms.html + segmented_control.html | **FIXES** — Sprint 6 |
| `tab` macro name collision | tabs.html + tabs_panels.html | **FIXES** — Sprint 6 |
| `bem()` doesn't strip invalid modifiers (warns but renders them) | filters.py:338-350 | **FIXES** — Sprint 6 |
| `html_attrs()` raw string bypass for space-prefixed strings | filters.py:613-614 | **FIXES** — Sprint 6 |
| `contrast_text()` returns "white" on invalid color with no warning | filters.py:250-267 | **FIXES** — Sprint 6 |
| `_warn()` hardcodes stacklevel=3, wrong for some call depths | validation.py:64-77 | **FIXES** — Sprint 6 |
| No z-index token system (values 1–10000 scattered across 40+ rules) | chirpui.css | **FIXES** — Sprint 7 |
| 51 hardcoded `font-weight: 600` instead of tokens | chirpui.css (51 sites) | **FIXES** — Sprint 7 |
| 50+ hardcoded animation durations not using motion tokens | chirpui.css | **FIXES** — Sprint 7 |
| 20+ raw `rgba()` values in shadows/glass instead of tokens | chirpui.css | **MITIGATES** — Sprint 7 |
| 7 templates still use `variant="default"` as parameter default | surface.html, confirm.html, etc. | **FIXES** — Sprint 8 (residual) |
| No `reset_colors()` or strict-mode query API | filters.py | **FIXES** — Sprint 8 |
| `tab_is_active()` with empty `href=""` matches all paths | route_tabs.py:25-28 | **FIXES** — Sprint 8 |
| `register_colors()` silently coerces non-string keys/values | filters.py:85-86 | **FIXES** — Sprint 8 |
| `STATUS_WORDS` missing "warning", "pending", "info" | filters.py:452-469 | **FIXES** — Sprint 8 |

---

### Invariants

1. **All existing tests continue to pass** — no behavioral regression. New warnings are additive, not breaking.
2. **No silent wrong output** — every validation fallback logs a warning (at minimum) that appears in dev-mode output.
3. **Token system is self-consistent** — every CSS custom property used in a rule is defined in `:root`; every spacing/color in a component rule uses a token.
4. **Each sprint ships independently** — a sprint can be merged and released without any later sprint.

---

## Target Architecture

No structural rewrite. Same files, same macros, same API. The changes are:

```
filters.py:     validate_* functions emit warnings on fallback
                register_colors validates eagerly, raises on invalid
                register_filters warns when skipping globals

templates:      Consistent defaults (variant="" everywhere, size="md" everywhere)
                btn() accepts hx={} dict, reducing params from 22 to ~12
                Legacy slot macros marked {% comment "DEPRECATED: use slots" %}

chirpui.css:    All hardcoded colors → tokens
                Missing tokens defined (spacing-2xs, breakpoint consistency)
                overflow: hidden → overflow: clip where safe (preserves layout, allows escape)

chirpui.js:     try/catch localStorage, [data-theme="system"] uses prefers-color-scheme

conftest.py:    Stubs match real filter signatures (Mapping, strict mode, serialization)

docs:           COMPONENT-OPTIONS.md covers all 195 templates
                Decision trees for overlapping component families
                Context propagation documented per-macro
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design & validate | 3–4h | Low | Yes (plan doc only) ✓ |
| 1 | Warning system — stop silent failures | 6–8h | Low | Yes ✓ |
| 2 | API normalization — consistent names/defaults | 6–10h | Medium | Yes ✓ |
| 3 | CSS/JS correctness — tokens, overflow, theme | 6–10h | Medium | Yes ✓ |
| 4 | Test infrastructure — align stubs with reality | 4–6h | Low | Yes ✓ |
| 5 | Documentation — close the 54% gap | 6–12h | Low | Yes ✓ |
| **6** | **Filter & macro safety — collisions, validation, escapes** | **6–8h** | **Medium** | **Yes ✓** |
| **7** | **CSS token completeness — z-index, font-weight, animation** | **8–10h** | **Low** | **Yes ✓** |
| **8** | **Residual cleanup — leftover defaults, missing APIs** | **4–6h** | **Low** | **Yes ✓** |

---

## Sprint 0: Design & Validate ✓

**Goal:** Resolve ambiguous design decisions on paper before writing code.
**Status:** Complete (2026-04-13)

### Decision 0.1: `hx={}` dict pattern for signature reduction

**Decision:** Add `hx=none` parameter to all 11 macros across 9 files that currently accept individual `hx_*` params. Keep individual `hx_*` params as deprecated aliases for one release cycle. When both `hx={}` and individual params are present, individual params win (explicit override).

**Scope:** All 11 macros, not just bloated ones. Consistency matters more than minimizing diff size.

| Macro | File | hx_* count | Total params → new |
|-------|------|-----------|-------------------|
| `btn()` | button.html | 11 | 22 → 13 |
| `form()` | forms.html | 12 | 22 → 12 |
| `icon_btn()` | icon_btn.html | 4 | 12 → 9 |
| `filter_chip()` | filter_chips.html | 4 | 10 → 7 |
| `confirm_dialog()` | confirm.html | 4 | 11 → 8 |
| `safe_region()` | fragment_island.html | 3 | 6 → 4 |
| `fragment_island()` | fragment_island.html | 3 | 6 → 4 |
| `fragment_island_with_result()` | fragment_island.html | 3 | 6 → 4 |
| `pagination()` | pagination.html | 4 | 9 → 6 |
| `tab()` | tabs.html | 3 | 8 → 6 |
| `ascii_tab()` | ascii_tabs.html | 3 | 8 → 6 |

**Before/after call-site example:**
```jinja2
{# Before: #}
{{ btn("Save", variant="primary", hx_post="/save", hx_target="#result", hx_swap="innerHTML") }}

{# After: #}
{{ btn("Save", variant="primary", hx={"post": "/save", "target": "#result", "swap": "innerHTML"}) }}
```

**Implementation:** Inside the macro, merge `hx` dict with individual params:
```jinja2
{% set _hx = (hx or {}) | merge_hx(hx_post=hx_post, hx_target=hx_target, ...) %}
{{ build_hx_attrs(**_hx) | html_attrs }}
```
Since `build_hx_attrs` already converts underscores to hyphens and `html_attrs` already skips `None`, the dict keys should use short names without `hx_` prefix: `{"post": "/save"}` not `{"hx_post": "/save"}`. The `hx-` prefix is added by `build_hx_attrs`.

---

### Decision 0.2: Canonical defaults for variant and size

**Variant convention:**
- **`variant=""`** is the canonical default for all components (empty string = unstyled/default appearance)
- Components with semantic defaults (`alert→"info"`, `badge→"primary"`, `callout→"info"`) keep their defaults because changing them would break existing call sites with no args
- `surface_variant=`, `status_variant=`, `skeleton_variant=` are acceptable namespaced variants — they serve different purposes than the primary `variant`

**Changes required:**

| Macro | Current default | New default | Breaking? |
|-------|----------------|-------------|-----------|
| `status_indicator` | `variant="default"` | `variant=""` | No (CSS maps both to same style) |
| `page_header` | `variant="default"` | `variant=""` | No |
| `section_header` | `variant="default"` | `variant=""` | No |
| `surface` | `variant="default"` | `variant=""` | No |
| `band` | `variant="default"` | `variant=""` | No |
| `feature_section` | `variant="default"` | `variant=""` | No |
| `modal_overlay_trigger` | `variant="default"` | `variant=""` | No |
| `ascii_empty` | `variant="default"` | `variant=""` | No |

**Size convention:**
- **`size=""`** is the canonical default (empty string = component's natural size)
- Components that ship with a meaningful default size (spinners, avatars, progress bars) use `size="md"`

**Changes required:**

| Macro | Current default | New default | Breaking? |
|-------|----------------|-------------|-----------|
| `modal` | `size="medium"` | `size="md"` | **Yes** — call sites using `size="medium"` need updating |
| `btn` | `size=none` | `size=""` | No (None and "" both resolve to no-size class) |

**Note:** `modal` with `size="medium"` is the only truly breaking change. All CSS selectors for `.chirpui-modal--medium` must be renamed to `.chirpui-modal--md`. A `validate_size` check should emit a deprecation warning for `"medium"` → `"md"` during the transition.

---

### Decision 0.3: `overflow: hidden` catalog and migration plan

**Audit found 80 instances** (not 55 as initially estimated). Categorized by action:

**Convert to `overflow: clip` (42 instances) — LOW RISK:**
These are text truncation and border-radius containment rules where no child content needs to escape. `overflow: clip` provides identical visual clipping without creating a scroll container or trapping absolutely-positioned descendants.

- Text truncation (21): `.chirpui-stepper__label`, `.chirpui-dl__detail--path`, `.chirpui-settings-row__detail`, `.chirpui-conversation-item__preview`, `.chirpui-video-card__title`, `.chirpui-playlist-item__title`, `.chirpui-bar-chart__label`, `.chirpui-calendar__event`, breadcrumb current item, all ASCII text lines (12 rules)
- Simple border-radius (21): `.chirpui-avatar`, `.chirpui-post-card`, `.chirpui-profile-header`, `.chirpui-card__media`, `.chirpui-video-card`, `.chirpui-video-thumbnail`, `.chirpui-accordion__item`, `.chirpui-collapse`, `.chirpui-segmented`, `.chirpui-progress-bar__track`, `.chirpui-bar-chart__track`, `.chirpui-input-group`, `.chirpui-search-bar__inner`, `.chirpui-ascii-border`, `.chirpui-ascii-toggle__rail`, `.chirpui-ascii-switch__slot`, `.chirpui-tooltip__bubble::after`, `.chirpui-ascii-table__td`

**Keep as `overflow: hidden` (33 instances) — needed for stacking/animation:**
- Flex layout containers (8): `.chirpui-panel`, `.chirpui-chat-layout__messages`, `.chirpui-tray__panel`, `.chirpui-modal__panel`, `.chirpui-app-shell__topbar-center`, `.chirpui-app-shell__main--fill`, `.chirpui-split-panel`, `.chirpui-command-palette`
- Animation containment (20): All effect components (shimmer, ripple, border-beam, marquee, meteor, glow-card, spotlight-card, particle-bg, typewriter, aurora, scanline, grain, texture, confetti, symbol-rain, holy-light, rune-field, constellation, split-flap)
- Overlay containers (5): `.chirpui-band`, `.chirpui-surface--static-overlay`, `.chirpui-marquee`, `.chirpui-nav-progress`, `.chirpui-command-palette__inner`

**Special case — `.chirpui-card` (line 4530):**
Convert to `overflow: clip`. Cards frequently contain tooltips and dropdowns. Current `overflow: hidden` clips them. The border-radius containment goal is equally served by `clip`.

**Special case — `.chirpui-children--clip > *` (line 937):**
Keep as-is. This is a utility class that users opt into explicitly.

**Special case — `.chirpui-visually-hidden` (line 3446):**
Already optimal (uses `clip: rect()`), leave untouched.

---

### Decision 0.4: Warning infrastructure

**Decision:** Use Python's `warnings.warn()` with a custom `ChirpUIWarning` category. This is the standard Python mechanism — users control visibility with `-W` flags and `warnings.filterwarnings()`.

**Warning category hierarchy:**
```python
class ChirpUIWarning(UserWarning):
    """Base warning for chirp-ui issues."""

class ChirpUIDeprecationWarning(ChirpUIWarning, DeprecationWarning):
    """Deprecated chirp-ui feature."""

class ChirpUIValidationWarning(ChirpUIWarning):
    """Invalid input that was silently corrected."""
```

**Strict mode escalation:** When `set_strict(True)` is active, `ChirpUIValidationWarning` raises as `ValueError` instead. `ChirpUIDeprecationWarning` remains a warning even in strict mode (deprecation ≠ error).

**Warning sites and messages:**

| Site | Category | Message format |
|------|----------|---------------|
| `validate_variant` fallback | `ChirpUIValidationWarning` | `"chirp-ui: variant '{value}' not in {allowed} for {component}; using '{default}'"` |
| `validate_size` fallback | `ChirpUIValidationWarning` | `"chirp-ui: size '{value}' not in {allowed} for {component}; using '{default}'"` |
| `register_colors` invalid | `ValueError` (always) | `"chirp-ui: invalid color value '{value}' for key '{key}'"` |
| `register_filters` skip globals | `ChirpUIWarning` | `"chirp-ui: app has no template_global(); build_hx_attrs will not be available as a template global"` |
| `icon()` unrecognized | `ChirpUIValidationWarning` | `"chirp-ui: unrecognized icon name '{name}'"` |
| `hx_*` individual params | `ChirpUIDeprecationWarning` | `"chirp-ui: individual hx_* params are deprecated; use hx={...} dict instead"` |
| `size="medium"` on modal | `ChirpUIDeprecationWarning` | `"chirp-ui: size='medium' is deprecated; use size='md'"` |

**Not using HTML comments:** Template-level `<!-- warning -->` comments leak into production HTML if not stripped. Python warnings are dev-only and filterable. Clean separation.

**Implementation:** Add `_warn(message, category=ChirpUIValidationWarning)` helper to `validation.py` that checks strict mode and either warns or raises.

---

## Sprint 1: Warning System — Stop Silent Failures

**Goal:** Every validation fallback, skipped registration, and unrecognized input produces a visible warning in development.

### Task 1.1: `validate_variant` and `validate_size` warn on fallback

- **Description:** When the provided value doesn't match `allowed`, emit a warning before returning the default. Include component name, provided value, and allowed values in the message.
- **Files:** `filters.py:354-411`
- **Acceptance:** `uv run pytest -q` passes; `python -W all -c "from chirp_ui.filters import validate_variant; validate_variant('xl', ('sm','md','lg'), 'md')"` emits a `UserWarning`.

### Task 1.2: `register_colors` validates eagerly

- **Description:** On registration, run `sanitize_color` on each value. If any value is invalid, raise `ValueError` with the bad key+value. Fail fast, not at render time.
- **Files:** `filters.py:70-76`
- **Acceptance:** `register_colors({"brand": "not-a-color"})` raises `ValueError`. `register_colors({"brand": "#ff0000"})` succeeds silently.

### Task 1.3: `register_filters` warns when skipping globals

- **Description:** When `hasattr(app, "template_global")` is false, emit a warning explaining that template globals (like `build_hx_attrs`) won't be available.
- **Files:** `filters.py:579`
- **Acceptance:** `python -W all` + register with a mock app lacking `template_global` → `UserWarning` emitted.

### Task 1.4: `settings_row` status detection becomes extensible

- **Description:** Replace hardcoded word lists with a `STATUS_WORDS` registry (dict mapping strings to variants). Ship sensible defaults but allow `STATUS_WORDS.update({"ready": "success", "active": "success", "offline": "error"})`.
- **Files:** `settings_row.html:30-34`, `validation.py`
- **Acceptance:** `settings_row(status="ready")` renders with success variant. Unknown words still fall back to muted but emit a warning.

### Task 1.5: `icon()` warns on unrecognized names in all modes

- **Description:** Currently only warns in strict mode. Change to always warn (non-strict = warning, strict = exception).
- **Files:** `filters.py:414-424`
- **Acceptance:** `icon("nonexistent_icon_xyz")` emits warning regardless of strict mode.

---

## Sprint 2: API Normalization — Consistent Names and Defaults ✓

**Goal:** A developer who learns one macro's conventions can predict every other macro's conventions.

### Task 2.1: Standardize variant defaults

- **Description:** Per Sprint 0 Task 0.2 decision, update all macros to use the canonical variant default (likely `variant=""`). Update validation calls and tests accordingly.
- **Files:** All templates with `variant=` parameter, `test_components.py`
- **Acceptance:** `rg 'variant="' src/chirp_ui/templates/chirpui/ | grep -v 'variant=""'` returns zero results (excluding internal `_variant` variables).

### Task 2.2: Standardize size vocabulary

- **Description:** All size parameters use `"sm"`, `"md"`, `"lg"` (not `"small"`, `"medium"`, `"large"`). `modal` is the main offender (`size="medium"`).
- **Files:** `modal.html`, `chirpui.css` (modal size selectors), `test_components.py`
- **Acceptance:** `rg 'size="(small|medium|large)"' src/chirp_ui/templates/` returns zero results.

### Task 2.3: Introduce `hx={}` dict pattern for bloated macros

- **Description:** Per Sprint 0 Task 0.1 decision, add `hx=none` parameter to `btn()`, `confirm_dialog()`, and other 10+ param macros. When `hx` is a dict, merge into `build_hx_attrs`. Keep individual `hx_*` params as deprecated aliases for one release cycle.
- **Files:** `button.html`, `confirm_dialog.html`, `filters.py:build_hx_attrs`
- **Acceptance:** `btn("Save", hx={"post": "/save", "target": "#result"})` renders identical output to `btn("Save", hx_post="/save", hx_target="#result")`.

### Task 2.4: Document interdependent parameters

- **Description:** For every macro with params that must be used together (e.g., `form_action` + `attrs_map` in `config_row_toggle`), add a `{# REQUIRES: form_action AND attrs_map #}` comment at the macro top and emit a warning if only one is provided.
- **Files:** `config_row.html`, `inline_edit_field.html`
- **Acceptance:** `config_row_toggle(name="x", label="X", form_action="/save")` (without `attrs_map`) emits a warning.

### Task 2.5: Mark legacy slot patterns as deprecated

- **Description:** In `post_card.html`, `card.html`, and `channel_card.html`, add `{# DEPRECATED: Use named slots instead. See migration guide. #}` above legacy macros. Remove `use_slots` parameter from `channel_card` (always use slots).
- **Files:** `post_card.html`, `card.html`, `channel_card.html`
- **Acceptance:** Legacy macros still function (no breakage) but grep shows deprecation comments.

---

## Sprint 3: CSS/JS Correctness — Tokens, Overflow, Theme ✓

**Goal:** The token system is self-consistent and the theme script works in all browsers.

### Task 3.1: Define missing CSS tokens

- **Description:** Add `--chirpui-spacing-2xs` to `:root`. Audit for any other used-but-undefined custom properties.
- **Files:** `chirpui.css` `:root` block
- **Acceptance:** `rg 'var\(--chirpui-' chirpui.css | grep -oP '--chirpui-[\w-]+' | sort -u` cross-referenced with `:root` definitions — zero undefined properties.

### Task 3.2: Replace hardcoded `color: white` with tokens

- **Description:** Replace all 20+ instances of `color: white` with `var(--chirpui-on-primary)` or `var(--chirpui-surface)` as appropriate for the component's context.
- **Files:** `chirpui.css`
- **Acceptance:** `rg 'color:\s*white' chirpui.css` returns zero results.

### Task 3.3: Standardize breakpoints to rem tokens

- **Description:** Replace `767px`, `768px`, `960px` media queries with the defined `--chirpui-layout-bp-*` values (use rem equivalents since media queries can't use custom properties).
- **Files:** `chirpui.css`
- **Acceptance:** `rg '@media.*\d+px' chirpui.css` returns zero results (all use rem).

### Task 3.4: Replace hardcoded component padding with tokens

- **Description:** Badges, pills, labels, and segmented controls use hardcoded padding (`0.15rem 0.45rem`, `2px`, etc.). Replace with spacing tokens or define new fine-grained tokens if needed (e.g., `--chirpui-spacing-3xs: 0.125rem`).
- **Files:** `chirpui.css` (badge, pill, label, segmented sections)
- **Acceptance:** Hardcoded padding values in component rules reduced by 80%+ (some exceptions documented).

### Task 3.5: Selective `overflow: hidden` → `overflow: clip` migration

- **Description:** Per Sprint 0 Task 0.3 audit, change safe instances of `overflow: hidden` to `overflow: clip` (CSS clip doesn't create a scroll container and doesn't affect `position: absolute` escape). Document remaining `overflow: hidden` rules that must stay.
- **Files:** `chirpui.css`
- **Acceptance:** Tooltip inside card renders without clipping. `uv run pytest -q` passes.

### Task 3.6: Fix chirpui.js — localStorage + system theme

- **Description:** (a) Wrap `localStorage.getItem` in try/catch, falling back to `"system"`. (b) Add `[data-theme="system"]` CSS rules that use `light-dark()` or `prefers-color-scheme`. (c) Add inline comment documenting synchronous execution requirement.
- **Files:** `chirpui.js`, `chirpui.css`
- **Acceptance:** Script runs without error when `localStorage` throws. `data-theme="system"` respects OS dark mode preference.

---

## Sprint 4: Test Infrastructure — Align Stubs with Reality ✓

**Goal:** Test stubs match real filter behavior so green CI means green runtime.

### Task 4.1: `_field_errors_stub` → check `Mapping` not `dict`

- **Description:** Change `isinstance(errors, dict)` to `isinstance(errors, Mapping)` to match real `field_errors` behavior.
- **Files:** `conftest.py:35`
- **Acceptance:** Test with `OrderedDict` input passes through stub correctly.

### Task 4.2: `_validate_variant_stub` → respect strict mode

- **Description:** Mirror real `validate_variant` behavior: in strict mode, raise on invalid values.
- **Files:** `conftest.py:64-70`
- **Acceptance:** Strict-mode test with invalid variant raises instead of silently returning default.

### Task 4.3: `_html_attrs_stub` → use shared serialization

- **Description:** Extract `_serialize_attr_value` from `filters.py` into a testable helper. Use it in both the real filter and the test stub so serialization logic is shared, not duplicated.
- **Files:** `filters.py:519-523`, `conftest.py:89-111`
- **Acceptance:** Stub and real filter produce identical output for dict, list, string, int, None, and bool inputs.

### Task 4.4: Add stub-vs-real parity test

- **Description:** Write a parametrized test that calls both the real filter and the stub with the same inputs, asserting identical output. This prevents future drift.
- **Files:** `tests/test_stub_parity.py` (new)
- **Acceptance:** `uv run pytest tests/test_stub_parity.py -q` passes with 20+ input combinations.

---

## Sprint 5: Documentation — Close the 54% Gap ✓

**Goal:** Every shipped component is discoverable and the overlapping families have decision guidance.

### Task 5.1: Document remaining 106 components in COMPONENT-OPTIONS.md

- **Description:** For each undocumented template, add a section with: purpose, macro signature, parameter descriptions, and one usage example. Prioritize by component family (all cards together, all layout primitives together, etc.).
- **Files:** `docs/COMPONENT-OPTIONS.md`, cross-reference `src/chirp_ui/templates/chirpui/`
- **Acceptance:** `ls src/chirp_ui/templates/chirpui/*.html | wc -l` matches count of documented sections in COMPONENT-OPTIONS.md (within 5, allowing for multi-macro files).

### Task 5.2: Add "When to Use" decision trees

- **Description:** Write decision trees for the four most confusing overlapping families:
  1. **Overlays:** modal vs tray vs drawer vs popover vs tooltip
  2. **Cards:** card vs resource_card vs config_card vs metric_card vs glow_card
  3. **Filters:** filter_bar vs filter_chips vs filter_row
  4. **Layout:** frame vs grid vs stack vs cluster vs block vs layer
- **Files:** `docs/COMPONENT-OPTIONS.md` (new sections) or `docs/DECISION-TREES.md`
- **Acceptance:** Each tree has ≥3 decision criteria (e.g., "Does it need user input?" → form modal; "Is it persistent?" → tray).

### Task 5.3: Document context propagation per macro

- **Description:** For every macro that uses `consume()` or `provide()`, add a `Context:` line in its COMPONENT-OPTIONS.md entry listing what keys it reads/writes and what the effect is.
- **Files:** `docs/COMPONENT-OPTIONS.md`
- **Acceptance:** `rg 'consume\(' src/chirp_ui/templates/chirpui/` — every file listed has a corresponding `Context:` entry in docs.

### Task 5.4: Add CLAUDE.md entries for undocumented conventions

- **Description:** Add entries for deprecated patterns (`section_header_inline`, legacy slot macros), the `hx={}` dict pattern (from Sprint 2), and the warning system (from Sprint 1).
- **Files:** `CLAUDE.md`
- **Acceptance:** CLAUDE.md mentions deprecation policy, hx dict pattern, and warning behavior.

---

---

# Phase 2: Second Audit Findings

The second full-stack audit (2026-04-13) confirmed Sprints 0–5 are complete and revealed a new layer of sharp edges: macro name collisions, asymmetric validation, CSS token gaps in z-index/font-weight/animation, and several filter edge cases.

## Phase 2 Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 6 | Filter & macro safety — name collisions, validation asymmetry, escape hatches | 6–8h | Medium | Yes |
| 7 | CSS token completeness — z-index, font-weight, animation duration | 8–10h | Low | Yes |
| 8 | Residual cleanup — leftover defaults, missing APIs, edge cases | 4–6h | Low | Yes |

---

## Sprint 6: Filter & Macro Safety ✓

**Goal:** Eliminate macro name collisions, make validation consistently correct-or-warn, and close the `html_attrs` escape hatch.

### Task 6.1: Disambiguate `segmented_control` name collision

- **Description:** `forms.html` and `segmented_control.html` both define `segmented_control()` with incompatible signatures (form field vs display component). Importing both silently shadows one. Rename the form version to `segmented_control_field()` and add a deprecation alias.
- **Files:** `forms.html:336`, `segmented_control.html:20`, `test_components.py`
- **Acceptance:** Both macros importable in the same template. `rg 'def segmented_control\b' src/chirp_ui/templates/chirpui/` returns exactly one result (the display version).

### Task 6.2: Disambiguate `tab` name collision

- **Description:** `tabs.html` and `tabs_panels.html` both define `tab()` — one for htmx server-side, one for Alpine client-side. Rename the Alpine version to `tab_button()` (it renders a `<button>`, not a panel). Add deprecation alias.
- **Files:** `tabs.html:21`, `tabs_panels.html:19`, `test_components.py`
- **Acceptance:** Both macros importable together. `rg 'def tab\b' src/chirp_ui/templates/chirpui/` returns exactly one result.

### Task 6.3: `bem()` strips invalid modifiers (match variant/size behavior)

- **Description:** `bem()` validates variants and sizes and **corrects** them (falls back to default), but validates modifiers and **leaves invalid ones in the output**. This is asymmetric. Change to filter out invalid modifiers after warning, consistent with variant/size behavior.
- **Files:** `filters.py:338-350`
- **Acceptance:** `bem("btn", modifier="nonexistent")` emits warning AND omits the invalid modifier class from output. `uv run pytest -q` passes.

### Task 6.4: `contrast_text()` warns on invalid color

- **Description:** Returns `"white"` on invalid color with no warning, unlike `icon()` which warns on unrecognized names. Add `ChirpUIValidationWarning` when color parsing fails.
- **Files:** `filters.py:250-267`
- **Acceptance:** `contrast_text("not-a-color")` emits warning. Still returns `"white"` as fallback (non-breaking).

### Task 6.5: Remove `html_attrs()` raw string bypass

- **Description:** Strings with a leading space bypass escaping and render as raw `Markup`. This is an undocumented security escape hatch. Remove the special-case: all string inputs should be escaped, or at minimum require an explicit `Markup()` wrapper.
- **Files:** `filters.py:610-615`
- **Acceptance:** `html_attrs(" onclick=alert(1)")` returns escaped output, not raw HTML. Grep templates for any call sites relying on the old behavior and update them.

### Task 6.6: `_warn()` dynamic stacklevel

- **Description:** `_warn()` hardcodes `stacklevel=3`, which is wrong when called from different depths (e.g., `bem()` → validation → `_warn()` vs `validate_variant()` → `_warn()`). Accept an optional `stacklevel` parameter, default to 3 for backwards compat.
- **Files:** `validation.py:64-77`
- **Acceptance:** Warnings from `bem()` point to the correct caller line, not an internal function.

---

## Sprint 7: CSS Token Completeness ✓

**Goal:** Extend the token system to cover z-index, font-weight, and animation duration — the three areas where hardcoded values are most prevalent.

### Task 7.1: Z-index token system

- **Description:** Define `--chirpui-z-*` tokens in `:root` with a documented hierarchy. Replace all 40+ scattered z-index values with token references.
- **Tokens:** `--chirpui-z-deep: -1`, `--chirpui-z-base: 0`, `--chirpui-z-raised: 1`, `--chirpui-z-dropdown: 10`, `--chirpui-z-sticky: 20`, `--chirpui-z-overlay: 50`, `--chirpui-z-modal: 100`, `--chirpui-z-popover: 1100`, `--chirpui-z-toast: 1200`, `--chirpui-z-max: 10000`
- **Files:** `chirpui.css`
- **Acceptance:** `rg 'z-index:\s*\d' chirpui.css | grep -v 'var(--chirpui-z-'` returns zero results (excluding `:root` definitions).

### Task 7.2: Font-weight tokens

- **Description:** Define `--chirpui-font-weight-semibold: 600` and `--chirpui-font-weight-bold: 700` tokens. Replace all 51 hardcoded `font-weight: 600` instances.
- **Files:** `chirpui.css`
- **Acceptance:** `rg 'font-weight:\s*600' chirpui.css` returns zero results outside `:root`.

### Task 7.3: Animation duration tokens

- **Description:** Define `--chirpui-anim-*` tokens for the ~12 distinct animation durations used (0.4s, 0.6s, 0.8s, 1s, 1.2s, 1.4s, 1.5s, 2s, 3s, 4s, 8s, 15s, 20s). Not every value needs a unique token — group into semantic categories (pulse, cycle, ambient, marquee). Replace hardcoded values in `animation:` declarations.
- **Files:** `chirpui.css`
- **Acceptance:** `test_transition_tokens.py` extended to cover `animation` declarations (not just `transition`). Test passes.

### Task 7.4: Shadow/glass rgba consolidation (stretch)

- **Description:** Replace the most common raw `rgba()` values in shadow and glass effects with tokens. Focus on the ~10 most-repeated patterns, not all 20+.
- **Files:** `chirpui.css`
- **Acceptance:** Top 10 repeated rgba patterns use tokens. Remaining documented as intentional.

---

## Sprint 8: Residual Cleanup ✓

**Goal:** Fix leftover issues from Phase 1 and small filter edge cases found in the second audit.

### Task 8.1: Fix remaining `variant="default"` defaults

- **Description:** 7 templates still use `variant="default"` as macro parameter default: `surface.html`, `shell_actions.html`, `resource_index.html`, `confirm.html`, `command_bar.html`, `app_shell.html`, `action_strip.html`. Change to `variant=""` per Sprint 0 Decision 0.2.
- **Files:** 7 template files listed above, `test_components.py`
- **Acceptance:** `rg 'variant="default"' src/chirp_ui/templates/chirpui/` returns zero results in macro parameter defaults (CSS class references are fine).

### Task 8.2: Add `reset_colors()` and `is_strict()` APIs

- **Description:** `register_colors()` merges but has no reset. `set_strict()` sets but can't be queried. Add `reset_colors()` to clear the ContextVar and `is_strict()` as a public API.
- **Files:** `filters.py`, `validation.py`, `__init__.py` (exports)
- **Acceptance:** `reset_colors()` clears registered colors. `is_strict()` returns current strict mode state.

### Task 8.3: Guard `tab_is_active()` against empty href

- **Description:** With `href=""` and `match="prefix"`, the condition `current_path.startswith("" + "/")` matches every path starting with `/`. Add an early return `False` when `href` is empty.
- **Files:** `route_tabs.py:25-28`
- **Acceptance:** `tab_is_active({"href": ""}, "/anything")` returns `False`.

### Task 8.4: Expand `STATUS_WORDS` registry

- **Description:** Add common missing status words: `"warning" → "warning"`, `"pending" → "muted"`, `"info" → "info"`, `"active" → "success"`, `"inactive" → "muted"`, `"ready" → "success"`, `"offline" → "error"`, `"degraded" → "warning"`.
- **Files:** `filters.py` (STATUS_WORDS dict)
- **Acceptance:** `resolve_status_variant("warning")` returns `"warning"`, not `"muted"`.

### Task 8.5: `register_colors()` type validation

- **Description:** Currently `str()`-coerces non-string keys and values silently. Add type checking: keys must be `str`, values must be `str`. Raise `TypeError` on non-string input.
- **Files:** `filters.py:85-86`
- **Acceptance:** `register_colors({123: "#fff"})` raises `TypeError`.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Changing variant defaults breaks existing apps | Medium | High | Sprint 0 catalogs every deviation; Sprint 2 changes only defaults that are `""` vs named (empty string is always safe as "no variant") |
| `overflow: clip` not supported in older browsers | Low | Medium | Sprint 0 Task 0.3 checks `caniuse`; `clip` has 95%+ support; keep `hidden` for critical layout containers |
| Warning spam annoys developers | Medium | Medium | Sprint 0 Task 0.4 designs filterable warnings via `warnings.warn()` — developers control visibility with standard Python `-W` flags |
| `hx={}` dict pattern rejected by users | Low | Medium | Sprint 2 keeps individual `hx_*` params as deprecated aliases; no forced migration |
| Documenting 106 components is too large for one sprint | Medium | Low | Sprint 5 can be split across releases; prioritize by component family popularity |
| Test stub parity test becomes maintenance burden | Low | Low | Sprint 4 Task 4.3 shares serialization code, so parity is structural, not manually maintained |
| Macro rename breaks existing imports | Medium | High | Sprint 6 adds deprecation aliases — old names still work for one release cycle |
| Removing `html_attrs` raw string bypass breaks call sites | Low | High | Sprint 6 Task 6.5 greps all templates for affected patterns before removing |
| Z-index token migration causes visual regressions | Low | Medium | Sprint 7 maps existing values to tokens 1:1 — no visual changes, only indirection |
| 51 font-weight replacements cause subtle rendering shifts | Low | Low | Sprint 7 tokens define exact same numeric values; purely a maintainability change |

---

## Success Metrics

| Metric | Before Phase 1 | After Phase 1 (Sprint 5) | After Phase 2 (Sprint 8) |
|--------|----------------|--------------------------|--------------------------|
| Silent validation fallbacks | ~15 sites, 0 warnings | 0 sites without warnings ✓ | 0 (+ contrast_text warns) |
| Variant default conventions | 4 different defaults | 1 default (`""`) (7 residual) | 0 residual |
| Size vocabulary variants | 3 (`md`, `medium`, `none`) | 1 (`md`) ✓ | 1 |
| `btn()` parameter count | 22 | ~12 (with `hx={}`) ✓ | ~12 |
| Hardcoded `color: white` in CSS | 20+ | 0 ✓ | 0 |
| Undefined CSS custom properties | ≥1 (`spacing-2xs`) | 0 ✓ | 0 |
| chirpui.js browser failures | Safari private browsing | 0 ✓ | 0 |
| Documented components | 89/195 (46%) | 195/195 ✓ | 195/195 |
| Test stub divergences | 3 known | 0 ✓ | 0 |
| Macro name collisions | 2 (`segmented_control`, `tab`) | 2 (not addressed) | 0 |
| `bem()` invalid modifiers rendered | Yes (warns but keeps) | Yes | 0 (stripped after warning) |
| `html_attrs` raw string bypass | Yes | Yes | Removed |
| Z-index values without tokens | 40+ scattered | 40+ | 0 (all use `--chirpui-z-*`) |
| Hardcoded `font-weight: 600` | 51 instances | 51 | 0 (all use token) |
| Hardcoded animation durations | 50+ instances | 50+ | 0 (all use `--chirpui-anim-*`) |
| `STATUS_WORDS` coverage | 3 states | 3 states | 11 states |

---

## Relationship to Existing Work

- **PLAN-color-system-hardening** (Complete) — Sprint 1's warning pattern for `validate_variant` follows the same approach used for `sanitize_color` validation.
- **PLAN-context-aware-theming** (Complete) — Sprint 5's context propagation documentation covers the provide/consume patterns introduced by that epic.
- **PLAN-descriptor-coverage** — ComponentDescriptor registration is orthogonal; this plan does not change descriptor structure.
- **PLAN-ascii-maturity** — Sprint 5 documentation covers ASCII components whose Sprint 4 (docs) was deferred.
- **PLAN-sharp-edges-phase3** (Complete) — structural/behavioral hardening (sprints 9–13): template defaults, filter hardening, a11y, Alpine resilience, provide/consume docstrings.
- **[PLAN-sharp-edges-phase4](PLAN-sharp-edges-phase4.md)** (Complete) — API consistency & developer ergonomics (sprints 14–19): slot naming, attrs safety, hx={} promotion, neumorphic refactor, test hardening, docs index.

---

## Changelog

- **2026-04-13**: Initial draft from full-stack sharp edges audit.
- **2026-04-13**: Sprint 0 complete — all four design decisions resolved (hx dict pattern, canonical defaults, overflow catalog of 80 rules, warning infrastructure with ChirpUIWarning hierarchy).
- **2026-04-13**: Sprints 1–5 implemented and merged (#61, #62).
- **2026-04-13**: Phase 2 — second full-stack audit. Confirmed Sprints 0–5 complete. Found 15 new sharp edges not covered by Phase 1: macro name collisions (2), filter validation asymmetry (3), CSS token gaps in z-index/font-weight/animation (3), residual defaults (7 files), missing APIs (2), edge cases (3). Added Sprints 6–8.
- **2026-04-13**: Sprints 6–8 implemented. Sprint 6: renamed segmented_control→segmented_control_field and tab→tab_button, fixed bem() modifier stripping, added contrast_text warning, dynamic _warn stacklevel, is_strict() API. Sprint 7: added 8 z-index tokens (replaced 18 values), replaced 62 font-weight values, added 8 animation tokens (replaced 34 values). Sprint 8: added reset_colors(), type validation for register_colors, empty href guard, expanded STATUS_WORDS from 16→25 entries.
