---
name: chirpui-token-audit
description: |
  Audit chirp-ui CSS for token discipline: flag hardcoded durations, easings, hex
  colors, and spacing values that bypass --chirpui-* custom properties. Verify the
  three-layer token hierarchy (primitive → semantic → component) is coherent.
  Outputs a prioritized findings table and a list of missing token definitions.
tags:
  - chirpui
  - css
  - tokens
  - audit
  - design-system
triggers:
  - "::chirpui-token-audit"
  - "::cta"
  - "token audit"
  - "audit chirpui tokens"
  - "check chirpui css"
inputs:
  - target: "Optional — CSS file or section to audit (default: chirpui.css)"
outputs:
  - report: "Token audit findings table + missing token list"
---

# chirpui Token Audit

Verify that `chirpui.css` uses the `--chirpui-*` token system consistently and
that the three token layers are coherent.

## Token Layer Model

```
Primitive  — raw values, rarely used directly
  --chirpui-color-blue-600: #2563eb;
  --chirpui-duration-fast: 150ms;

Semantic   — purpose aliases, used in component rules
  --chirpui-color-primary: var(--chirpui-color-blue-600);
  --chirpui-duration-interaction: var(--chirpui-duration-fast);

Component  — component-specific tokens, consume semantic tokens
  --chirpui-btn-bg: var(--chirpui-color-primary);
  --chirpui-btn-transition: var(--chirpui-duration-interaction) var(--chirpui-easing-standard);
```

---

## Audit Procedure

### Step 1 — Hardcoded durations and easings (automated by test_transition_tokens.py)

Search for raw values that should be tokens:

```bash
grep -n "[0-9]\+ms" src/chirp_ui/templates/chirpui.css
grep -n "ease-in\|ease-out\|ease-in-out\|linear" src/chirp_ui/templates/chirpui.css
grep -n "cubic-bezier" src/chirp_ui/templates/chirpui.css
```

Every `transition:` or `animation:` must use `--chirpui-duration-*` and `--chirpui-easing-*`.

### Step 2 — Hardcoded colors

```bash
grep -n "#[0-9a-fA-F]\{3,8\}" src/chirp_ui/templates/chirpui.css
grep -n "rgb\|rgba\|hsl\|hwb" src/chirp_ui/templates/chirpui.css
```

Hardcoded hex/rgb/hsl in component rules (below the primitive layer) is a finding.
Exception: values inside `@layer primitive` or a clearly marked primitive block.

### Step 3 — Hardcoded spacing

```bash
grep -n "padding:\s*[0-9]" src/chirp_ui/templates/chirpui.css
grep -n "margin:\s*[0-9]" src/chirp_ui/templates/chirpui.css
grep -n "gap:\s*[0-9]" src/chirp_ui/templates/chirpui.css
```

Component spacing should reference `--chirpui-space-*` tokens, not raw `px`/`rem`.

### Step 4 — Missing semantic tokens

Check that every primitive token has a semantic alias before being used in components.
Flag cases where a primitive is used directly in a component rule.

### Step 5 — Orphan tokens

Tokens defined but never referenced in any rule or template are dead weight.

```bash
grep -o "\-\-chirpui-[a-z0-9-]*" src/chirp_ui/templates/chirpui.css | sort | uniq -c | sort -rn
```

---

## Output Format

```markdown
## Token Audit: chirpui.css

### Findings

| Line | Category | Issue | Suggested Fix | Tier |
|------|----------|-------|---------------|------|
| 142 | Duration | `transition: 200ms ease` | `var(--chirpui-duration-interaction) var(--chirpui-easing-standard)` | 1 |
| 87  | Color    | `#2563eb` in .chirpui-btn | `var(--chirpui-color-primary)` | 2 |
| 210 | Spacing  | `padding: 0.5rem 1rem` in .chirpui-badge | `var(--chirpui-space-sm) var(--chirpui-space-md)` | 3 |

### Missing tokens

These values appear multiple times but have no named token:
- `16px` (spacing) — appears 7 times
- `#6366f1` (color) — appears 3 times

### Orphan tokens

Defined but unreferenced:
- `--chirpui-color-accent-muted`

### Summary

- **Tier 1 (blockers):** Transition/animation rules bypassing motion tokens — caught by CI
- **Tier 2 (high):** Hardcoded colors in component rules
- **Tier 3 (medium):** Hardcoded spacing not using space tokens
- **Tier 4 (low):** Orphan token definitions
```

---

## DORI Lifecycle

- `dori_begin(skill="chirpui-token-audit")`
- `dori_complete(files_reviewed="src/chirp_ui/templates/chirpui.css")`
