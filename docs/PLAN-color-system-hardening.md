# Epic: Color System Hardening — Correct, Complete, Tested

**Status**: Draft
**Created**: 2026-04-10
**Target**: 0.3.0
**Estimated Effort**: 8–14h
**Dependencies**: None (self-contained in `filters.py` + tests)
**Source**: Codebase exploration + manual audit of `filters.py` color pipeline

---

## Why This Matters

The color subsystem (`sanitize_color` → `resolve_color` → `contrast_text`) is the accessibility backbone for every component that accepts user-defined colors — badges, status indicators, progress bars, and filter chips. A bug here silently produces illegible text on colored backgrounds.

**Consequences of the current state:**

1. **`_linear_to_srgb` has an inverted formula** — line 208 divides by 12.92 instead of multiplying. For near-black OKLch colors (linear value ≤ 0.0031308), gamma-encoded output is **166× too dark**. The contrast_text result is still correct for these values (they're dark → white text), but any future consumer of `_oklch_to_channels` gets wrong sRGB values.
2. **`sanitize_color` regex blocks valid CSS colors** — negative hue values (`oklch(0.5 0.2 -30)`), `none` keyword in modern color syntax, `lab()`/`lch()` functions, and CSS named colors all fail validation. Components silently drop these to no-color fallback.
3. **Only 14 test assertions** cover the entire color pipeline (hex, rgb, rgba, hsl, oklch, resolve, sanitize) — no boundary cases, no malformed input fuzzing, no round-trip verification.
4. **No `oklcha()` support** — the regex and parser both reject alpha-channel oklch syntax, which is valid CSS.
5. **`_COLOR_RE` doesn't allow decimal-starting values** — `oklch(.5 .2 30)` (no leading zero) fails the regex even though it's valid CSS.

**The fix:** Correct the gamma bug, widen the sanitize regex to accept valid modern CSS color syntax, and build a comprehensive test suite that prevents regressions.

### Evidence Table

| Finding | Source | Proposal Impact |
|---------|--------|-----------------|
| `_linear_to_srgb` divides instead of multiplies for c ≤ 0.0031308 | `filters.py:208` | **FIXES** — Sprint 1 |
| `sanitize_color` rejects negative numbers, `none`, leading-dot decimals | `filters.py:43-45` | **FIXES** — Sprint 2 |
| oklch alpha channel not parsed | `filters.py:173-210` | **FIXES** — Sprint 2 |
| 14 assertions for 6 color formats + 2 utility functions | `test_filters.py` | **FIXES** — Sprint 1+2 |
| 4 components depend on color pipeline (badge, status, progress, filter_chips) | template grep | **MITIGATES** — tests catch rendering regressions |

---

### Invariants

1. **`contrast_text` returns WCAG-readable text color for all parseable inputs** — verified by round-trip tests against known luminance values.
2. **`sanitize_color` never passes a string that could enable CSS injection** — the regex is a security boundary; widening it must not allow `url()`, `var()`, `expression()`, or unbalanced parens.
3. **All existing tests continue to pass** — no behavioral regression for currently-valid inputs.

---

## Target Architecture

No structural change. Same functions, same API, same call sites. The changes are:

```
_linear_to_srgb:  c / 12.92  →  12.92 * c        (bug fix)
_COLOR_RE:        tighter     →  wider but safe    (accept modern CSS)
_oklch_to_channels:  3 args   →  3-4 args          (alpha tolerance)
test coverage:     14 asserts  →  80+ asserts       (comprehensive)
```

---

## Sprint Structure

| Sprint | Focus | Effort | Risk | Ships Independently? |
|--------|-------|--------|------|---------------------|
| 0 | Design: regex safety analysis | 1–2h | Low | Yes (analysis doc) |
| 1 | Fix `_linear_to_srgb` + test suite for existing formats | 3–5h | Low | Yes |
| 2 | Widen `sanitize_color` regex + oklch alpha + new format tests | 3–5h | Medium | Yes |
| 3 | Property-based fuzz tests (optional) | 2–3h | Low | Yes |

---

## Sprint 0: Design — Regex Safety Analysis

**Goal**: Prove that the widened `_COLOR_RE` cannot pass injection payloads before writing code.

### Task 0.1 — Catalog valid CSS color syntax that should pass

Survey CSS Color Level 4 spec for all function forms:
- `rgb()` / `rgba()` with space syntax and `/` alpha
- `hsl()` / `hsla()` with `deg`/`turn`/`rad` units
- `oklch()` / `oklcha()` with `none`, negative hue, `%` lightness
- `lab()` / `lch()` (stretch goal)
- Bare hex `#RGB` through `#RRGGBBAA`

**Acceptance**: Markdown list of ≥15 valid color strings that currently fail `sanitize_color`.

### Task 0.2 — Catalog dangerous strings that must NOT pass

- `url(...)`, `var(...)`, `expression(...)`, `calc(...)` with nested parens
- Strings with `<`, `>`, `"`, `'`, `;`, `{`, `}`
- Strings exceeding reasonable length (>100 chars)

**Acceptance**: List of ≥10 attack strings confirmed blocked by the new regex.

### Task 0.3 — Draft the new regex

Write the replacement `_COLOR_RE` and validate against both catalogs.

**Acceptance**: Python script that asserts all valid strings match and all dangerous strings don't.

---

## Sprint 1: Fix Gamma Bug + Baseline Test Suite

**Goal**: Correct the `_linear_to_srgb` formula and establish comprehensive tests for all existing color formats.

### Task 1.1 — Fix `_linear_to_srgb`

**File**: `src/chirp_ui/filters.py:208`

Change:
```python
return c / 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055
```
To:
```python
return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055
```

**Acceptance**:
- `uv run pytest tests/test_filters.py -q` passes
- New test verifies `_oklch_to_channels("oklch(0.1 0 0)")` returns sRGB value ≈ 0.01292 (not 0.0000774)

### Task 1.2 — Hex format tests

Add parametrized tests for:
- `#RGB`, `#RRGGBB`, `#RRGGBBAA` (valid)
- `#RR`, `#RRGGB`, `#` (invalid → None)
- Known color values: `#000000` → (0,0,0), `#ffffff` → (1,1,1), `#ff0000` → (1,0,0)

**Acceptance**: `uv run pytest tests/test_filters.py -k hex -q` — ≥8 new assertions pass.

### Task 1.3 — RGB/RGBA format tests

Parametrized tests for:
- Comma syntax: `rgb(255, 128, 0)`
- Space syntax: `rgb(255 128 0)`
- Percent syntax: `rgb(100%, 50%, 0%)`
- Alpha variants: `rgba(255, 128, 0, 0.5)`, `rgba(255 128 0 / 0.5)`
- Boundary values: `rgb(0, 0, 0)`, `rgb(255, 255, 255)`
- Malformed: `rgb()`, `rgb(a, b, c)`, `rgb(999, 0, 0)` (clamped)

**Acceptance**: ≥12 new assertions pass.

### Task 1.4 — HSL/HSLA format tests

Parametrized tests for known conversions:
- `hsl(0, 100%, 50%)` → red (1, 0, 0)
- `hsl(120, 100%, 50%)` → green (0, 1, 0)
- `hsl(240, 100%, 50%)` → blue (0, 0, 1)
- `hsl(0, 0%, 50%)` → gray (0.5, 0.5, 0.5)
- Achromatic: `hsl(0, 0%, 0%)`, `hsl(0, 0%, 100%)`

**Acceptance**: ≥8 new assertions with known sRGB values (tolerance ±0.01).

### Task 1.5 — OKLch format tests

Parametrized tests:
- `oklch(1 0 0)` → white ≈ (1, 1, 1)
- `oklch(0 0 0)` → black ≈ (0, 0, 0)
- `oklch(0.5 0 0)` → mid-gray
- `oklch(0.1 0 0)` → near-black (validates gamma fix)
- `oklch(50% 0 0)` → same as 0.5 (percent syntax)

**Acceptance**: ≥6 new assertions; near-black test specifically validates the gamma fix.

### Task 1.6 — `contrast_text` boundary tests

Test the luminance threshold (0.179) with colors near the boundary:
- Pure mid-grays that land on each side
- Saturated colors: yellow (bright), blue (dark), green (medium)
- Edge: `contrast_text("")` → `"white"`, `contrast_text("garbage")` → `"white"`

**Acceptance**: ≥8 new assertions.

---

## Sprint 2: Widen `sanitize_color` + OKLch Alpha

**Goal**: Accept valid modern CSS color syntax without opening injection vectors.

### Task 2.1 — Replace `_COLOR_RE` with widened regex

Apply the regex designed in Sprint 0. Key changes:
- Allow negative numbers (for hue values)
- Allow `none` keyword
- Allow leading-dot decimals (`.5` without `0`)
- Allow `deg`/`turn`/`rad` units
- Allow `/` alpha separator
- Keep blocking `url()`, `var()`, `expression()`, unbalanced parens

**File**: `src/chirp_ui/filters.py:43-45`

**Acceptance**:
- `rg 'url\(' tests/test_filters.py` returns hits confirming injection strings are tested
- All Sprint 0 valid strings pass `sanitize_color`
- All Sprint 0 dangerous strings return `None`

### Task 2.2 — Add `oklcha()` tolerance to parser

Modify `_oklch_to_channels` to also match `oklcha(...)` and ignore a 4th (alpha) argument.

**File**: `src/chirp_ui/filters.py:175`

**Acceptance**: `contrast_text("oklcha(0.8 0.1 200 / 0.5)")` returns `"#1a1a1a"` (light color).

### Task 2.3 — Tests for newly-accepted color strings

Parametrized tests confirming:
- `sanitize_color("oklch(.5 .2 30)")` → valid
- `sanitize_color("oklch(0.5 0.2 -30)")` → valid
- `sanitize_color("oklcha(0.5 0.2 30 / 0.8)")` → valid
- `sanitize_color("hsl(120deg 100% 50%)")` → valid
- `sanitize_color("url(evil)")` → None
- `sanitize_color("var(--x)")` → None
- `sanitize_color("expression(alert())")` → None

**Acceptance**: ≥15 new assertions.

---

## Sprint 3: Property-Based Fuzz Tests (Optional)

**Goal**: Use Hypothesis to generate random color strings and verify the pipeline never crashes or returns unsafe output.

### Task 3.1 — Install Hypothesis in dev group

**File**: `pyproject.toml`

### Task 3.2 — Fuzz `sanitize_color` with arbitrary strings

Strategy: generate strings from the alphabet of color characters plus injection characters. Assert: never raises, and if it returns non-None, the result matches a safe pattern.

### Task 3.3 — Fuzz `contrast_text` with valid color strings

Strategy: generate valid hex/rgb/hsl/oklch strings with random numeric values. Assert: always returns `"white"` or `"#1a1a1a"`, never raises.

**Acceptance**: `uv run pytest tests/test_filters.py -k fuzz -q` passes with 1000+ examples.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Widened regex allows CSS injection | Low | High | Sprint 0 designs + tests injection catalog before any code change |
| Gamma fix changes contrast_text output for edge colors | Low | Medium | Sprint 1.6 tests boundary cases; the bug only affects linear values ≤ 0.003 |
| Regex change breaks existing valid inputs | Low | Medium | Invariant 3: all existing tests must pass; Sprint 2 tests are additive |
| Component rendering changes from widened color acceptance | Low | Low | Only 4 components use the pipeline; behavior improves (fewer dropped colors) |

---

## Success Metrics

| Metric | Current | After Sprint 1 | After Sprint 2 |
|--------|---------|-----------------|-----------------|
| Color test assertions | 14 | ~60 | ~80+ |
| `_linear_to_srgb` correctness | ✗ (166× error in low range) | ✓ | ✓ |
| Valid CSS colors accepted by `sanitize_color` | ~60% of CSS Color L4 | ~60% | ~90% |
| Injection strings blocked | ✓ | ✓ | ✓ (verified by catalog) |

---

## Relationship to Existing Work

- **0.3.0 deprecation cleanup** — independent; this hardens infrastructure, deprecation removes API surface
- **SIZE_REGISTRY expansion** — independent; different subsystem
- **ASCII component family** — independent; ASCII components don't use color pipeline

---

## Changelog

- 2026-04-10: Draft created from codebase exploration
