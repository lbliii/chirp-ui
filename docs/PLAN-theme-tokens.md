# chirp-ui: Standardized Theme Token Set

## Goal

Define a minimal, standardized set of CSS custom properties that a user can fill in so their theme "just works" with chirp-ui. No component-specific overrides required. Convert holy-light as the first example.

---

## Current State

- **chirpui.css** defines `--chirpui-*` tokens with defaults; most components use them
- **Hardcoded colors** remain in: badge variants, status indicator, progress bar, field error
- **holy-light.css** overrides tokens AND adds 200+ lines of component-specific overrides (`.chirpui-card`, `.chirpui-modal`, etc.) with theme-specific logic and `rgba()` values

---

## Standardized Theme Token Set

### Tier 1: Core (required for any theme)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-text` | Primary text | `#1e293b` / `#f1f5f9` |
| `--chirpui-text-muted` | Secondary text | `#64748b` / `#94a3b8` |
| `--chirpui-surface` | Cards, modals, inputs | `#ffffff` / `#1e293b` |
| `--chirpui-surface-alt` | Alternating surfaces | `#f8fafc` / `#334155` |
| `--chirpui-surface-elevated` | Modals, dropdowns | `var(--chirpui-surface-alt)` |
| `--chirpui-border` | Borders | `#e2e8f0` / `#475569` |
| `--chirpui-bg` | Page background | `#f8fafc` / `#0f172a` |
| `--chirpui-bg-subtle` | Subtle backgrounds | `#f1f5f9` / `#1e293b` |
| `--chirpui-accent` | Primary accent (links, buttons, focus) | `#0284c7` / `#38bdf8` |
| `--chirpui-accent-hover` | Accent hover state | derived via color-mix |
| `--chirpui-focus-ring` | Focus ring (e.g. `rgba(2,132,199,0.3)`) | derived from accent |

### Tier 2: Semantic (badges, alerts, status, progress, errors)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-primary` | Primary badge/status | `#5b9cf5` |
| `--chirpui-primary-muted` | Primary background tint | derived via color-mix |
| `--chirpui-success` | Success state | `#22c55e` |
| `--chirpui-success-muted` | Success background | derived |
| `--chirpui-warning` | Warning state | `#f59e5b` |
| `--chirpui-warning-muted` | Warning background | derived |
| `--chirpui-error` | Error state | `#dc2626` |
| `--chirpui-error-muted` | Error background | derived |
| `--chirpui-info` | Info state (alerts, docs) | `#0284c7` / `#38bdf8` |
| `--chirpui-muted` | Default/neutral (status) | `#6b7280` |
| `--chirpui-muted-bg` | Default background | derived |

### Tier 3: Generic Shade Modifiers (apply to any color via color-mix)

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-shade-hover` | Darker mix (85% base + 15% black) | `85%` |
| `--chirpui-shade-active` | Even darker | `70%` |
| `--chirpui-shade-light` | Light tint (15% base + 85% white) | `15%` |
| `--chirpui-shade-dim` | Dimmed | `40%` |
| `--chirpui-shade-bright` | Bright highlight | `85%` |
| `--chirpui-shade-muted` | Muted background tint | `15%` |

### Tier 4: Optional (themes with extra palette)

| Token | Purpose | Example (holy-light) |
|-------|---------|----------------------|
| `--chirpui-accent-dim` | Dimmed accent (borders, hover) | derived |
| `--chirpui-accent-bright` | Bright accent (highlights) | derived |
| `--chirpui-card-header-color` | Card header text | default: `var(--chirpui-text)` |
| `--chirpui-card-hover-border` | Card hover border | default: `var(--chirpui-border)` |
| `--chirpui-card-hover-shadow` | Card hover shadow | default: `var(--chirpui-shadow-md)` |
| `--chirpui-card-body-link-color` | Links in card body (titles, primary actions) | default: `var(--chirpui-text)` |
| `--chirpui-card-body-link-decoration` | Link underline (typically `none`; card signals clickability) | default: `none` |
| `--chirpui-card-body-link-hover-color` | Card body link hover | default: `var(--chirpui-accent)` |

### Tier 5: HTTP Methods (API docs), Code Syntax, Example/Admonition

- `--chirpui-method-get`, `--chirpui-method-post`, etc. (color, bg, border)
- `--chirpui-code-bg`, `--chirpui-code-text`, `--chirpui-code-type`, `--chirpui-code-keyword`, etc.
- `--chirpui-example`, `--chirpui-alert-example-bg`, `--chirpui-alert-example-border`, `--chirpui-alert-example-color`

### Tier 6: Typography (UI vs. Prose)

See [docs/TYPOGRAPHY.md](TYPOGRAPHY.md) for full reference. UI scale: `--chirpui-ui-xs` … `--chirpui-ui-xl`, `--chirpui-ui-font-family`, `--chirpui-ui-font-weight-*`. Prose scale: `--chirpui-prose-base` … `--chirpui-prose-3xl`, `--chirpui-prose-font-family`, `--chirpui-prose-font-weight-*`. Override independently for dashboard density vs. content readability.

---

## Generic Shade Derivation (color-mix)

All state variants (hover, active, light, dim, bright, muted) are derived via `color-mix()` using generic shade tokens. Themes override base colors only; states follow automatically. When `oklch` is supported, `color-mix(in oklch, ...)` is used for better perceptual uniformity.

```css
--chirpui-accent-hover: color-mix(in srgb, var(--chirpui-accent) var(--chirpui-shade-hover), black);
--chirpui-primary-muted: color-mix(in srgb, var(--chirpui-primary) var(--chirpui-shade-muted), white);
```

**Benefits:** Themes override `--chirpui-accent` (and optionally `--chirpui-primary`, etc.) and get `accent-dim`, `accent-bright`, `*-muted` variants automatically. Themes can still override derived tokens for custom palettes (e.g. holy-light’s gold-dim).

---

## Implementation Plan

### Phase 1: Add missing tokens to chirpui.css

1. Add `--chirpui-surface-elevated` (default: `var(--chirpui-surface-alt)`)
2. Add `--chirpui-focus-ring` (default: `color-mix(in srgb, var(--chirpui-accent) 30%, transparent)` with hex fallback)
3. Add semantic tokens: `--chirpui-primary`, `--chirpui-primary-muted`, `--chirpui-success`, `--chirpui-success-muted`, `--chirpui-warning`, `--chirpui-warning-muted`, `--chirpui-error`, `--chirpui-error-muted`, `--chirpui-muted`, `--chirpui-muted-bg`
4. Add optional: `--chirpui-accent-dim`, `--chirpui-accent-bright` (components use `var(--chirpui-accent-dim, var(--chirpui-accent))`)
5. Add optional: `--chirpui-card-header-color`, `--chirpui-card-hover-border`, `--chirpui-card-hover-shadow`

### Phase 2: Replace hardcoded colors in chirpui.css

| Location | Current | Replace with |
|----------|---------|--------------|
| `.chirpui-field__error` | `color: #dc2626` | `color: var(--chirpui-error)` |
| `.chirpui-badge--primary` | `#5b9cf5`, `rgba(...)` | `var(--chirpui-primary)`, `var(--chirpui-primary-muted)` |
| `.chirpui-badge--success` | `#22c55e`, `rgba(...)` | `var(--chirpui-success)`, `var(--chirpui-success-muted)` |
| `.chirpui-badge--warning` | `#f59e5b`, `rgba(...)` | `var(--chirpui-warning)`, `var(--chirpui-warning-muted)` |
| `.chirpui-badge--error` | `#dc2626`, `rgba(...)` | `var(--chirpui-error)`, `var(--chirpui-error-muted)` |
| `.chirpui-status-indicator--default` | `#6b7280`, `rgba(...)` | `var(--chirpui-muted)`, `var(--chirpui-muted-bg)` |
| `.chirpui-status-indicator--success` | etc. | `var(--chirpui-success)`, `var(--chirpui-success-muted)` |
| `.chirpui-status-indicator--warning` | etc. | `var(--chirpui-warning)`, `var(--chirpui-warning-muted)` |
| `.chirpui-status-indicator--error` | etc. | `var(--chirpui-error)`, `var(--chirpui-error-muted)` |
| `.chirpui-progress-bar--gold` | `#c9a227` | `var(--chirpui-accent-dim, var(--chirpui-accent))` |
| `.chirpui-progress-bar--radiant` | gradient | `linear-gradient(90deg, var(--chirpui-accent-dim, var(--chirpui-accent)), var(--chirpui-accent-bright, var(--chirpui-accent)))` |
| `.chirpui-progress-bar--success` | `#22c55e` | `var(--chirpui-success)` |

### Phase 3: Use optional tokens in base components

- `.chirpui-card__header`: `color: var(--chirpui-card-header-color, var(--chirpui-text))`
- `.chirpui-card:hover`: `border-color: var(--chirpui-card-hover-border, var(--chirpui-border))`; `box-shadow: var(--chirpui-card-hover-shadow, var(--chirpui-shadow-md))`
- `.chirpui-table__th`: use `--chirpui-table-header-color` if we add it (optional)

### Phase 4: Convert holy-light to token-only theme

**Before:** 361 lines — token overrides + component overrides for cards, modals, tables, forms, tabs, dropdowns, toasts, pagination.

**After:** ~60 lines — single `:root` block with token overrides only. Remove all `.chirpui-*` selectors.

```css
/* chirp-ui Holy Light Theme — token-only */
:root {
    /* Core */
    --chirpui-bg: #0d0d0d;
    --chirpui-surface: #1a1a1a;
    --chirpui-surface-alt: #1a1a1a;
    --chirpui-surface-elevated: #262626;
    --chirpui-border: #333333;
    --chirpui-text: #e5e5e5;
    --chirpui-text-muted: #a8a8a8;

    /* Accent = gold spectrum */
    --chirpui-accent: #c9a227;
    --chirpui-accent-hover: #ffd700;
    --chirpui-accent-dim: #8a7235;
    --chirpui-accent-bright: #ffd700;

    /* Semantic */
    --chirpui-primary: #c9a227;
    --chirpui-primary-muted: rgba(201, 162, 39, 0.1);
    --chirpui-success: #22c55e;
    --chirpui-success-muted: rgba(34, 197, 94, 0.1);
    --chirpui-warning: #4f46e5;
    --chirpui-warning-muted: rgba(79, 70, 229, 0.15);
    --chirpui-error: #7c3aed;
    --chirpui-error-muted: rgba(124, 58, 237, 0.15);
    --chirpui-muted: #a8a8a8;
    --chirpui-muted-bg: rgba(168, 168, 168, 0.1);

    /* Focus */
    --chirpui-focus-ring: rgba(255, 215, 0, 0.3);

    /* Alerts (holy-light maps info→gold, warning→void-indigo, error→void-purple) */
    --chirpui-alert-info-bg: rgba(201, 162, 39, 0.15);
    --chirpui-alert-info-border: var(--chirpui-accent-dim);
    --chirpui-alert-info-color: var(--chirpui-accent);
    --chirpui-alert-success-bg: rgba(34, 197, 94, 0.15);
    --chirpui-alert-success-border: var(--chirpui-success);
    --chirpui-alert-success-color: var(--chirpui-success);
    --chirpui-alert-warning-bg: rgba(79, 70, 229, 0.15);
    --chirpui-alert-warning-border: var(--chirpui-warning);
    --chirpui-alert-warning-color: var(--chirpui-warning);
    --chirpui-alert-error-bg: rgba(124, 58, 237, 0.15);
    --chirpui-alert-error-border: var(--chirpui-error);
    --chirpui-alert-error-color: var(--chirpui-error);

    /* Optional component accents */
    --chirpui-card-header-color: var(--chirpui-accent);
    --chirpui-card-hover-border: var(--chirpui-accent);
    --chirpui-card-hover-shadow: 0 4px 12px rgba(255, 215, 0, 0.15);
}
```

**Additional:** holy-light uses `--chirpui-color-gold`, `--chirpui-color-radiant`, etc. in some places. After conversion, those become redundant — we use `--chirpui-accent`, `--chirpui-accent-bright` instead. The table header color, tab active color, etc. would use `--chirpui-accent` or `--chirpui-accent-bright`. We may need `--chirpui-table-header-color` and `--chirpui-tab-active-color` as optional tokens so holy-light can set them. Add to Tier 3 if needed.

---

## User-Facing Documentation

After implementation, document in README:

```markdown
## Theming

Create a theme by overriding tokens. Minimal example (accent only):

:root {
    --chirpui-accent: #7c3aed;
    --chirpui-accent-hover: #8b5cf6;
}

Full theme example: see `themes/holy-light.css`. Override any `--chirpui-*` token.
```

---

## File Structure

```
chirp-ui/
├── src/chirp_ui/templates/
│   ├── chirpui.css          # Base + all tokens with defaults
│   └── themes/
│       └── holy-light.css   # Token-only override (~60 lines)
└── docs/
    └── PLAN-theme-tokens.md # This plan
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Add `--chirpui-surface-elevated`, `--chirpui-focus-ring`, semantic tokens, optional tokens to chirpui.css |
| 2 | Replace all hardcoded hex/rgba in badge, status, progress, field-error with tokens |
| 3 | Use optional tokens in card (header color, hover border/shadow) |
| 4 | Rewrite holy-light.css as token-only; delete component overrides |
| 5 | Add oklch `@supports` block to holy-light for modern browsers |
| 6 | Update README theming section |
