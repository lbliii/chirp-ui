# chirp-theme - CSS Architecture

**Architecture:** Cascade layers + Semantic Design Token System + Responsive Design System

The shipped surface is the bespoke `chirp-theme.css` (active palette + every
`.chirp-theme-*` rule), composed over a retained Bengal token/base/component
baseline. chirp-theme.css overrides the chirp-ui component library
(`--chirpui-*` tokens + classes) emitted by `library_asset_tags()`.

---

## ⚠️ Important: Cascade layers & override contract

`chirpui.css` (loaded first) declares
`@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility`.
`style.css` then declares its own layers and pins the active theme last:

```css
@layer tokens, base, utilities, components, pages, chirp-theme;
```

`chirp-theme.css` wraps **all** of its rules — including the `:root` /
`[data-theme="dark"]` token blocks — in `@layer chirp-theme { … }`. Because that
layer is declared after every chirpui and theme layer, the theme fully restyles
the chirp-ui baseline **and stays overridable**: a downstream site wins by
adding an even-later layer, e.g. `@layer app.overrides { … }`, with no
specificity tricks. The contrast-checked `--chirpui-on-accent` pairing rides
inside the layer so it travels with the theme (enforced by
`tests/test_theme_token_parity.py`).

**Key principles:**
1. New theme CSS goes in `chirp-theme.css` (the `chirp-theme` layer).
2. Author new rules against the public `--chirpui-*` token namespace; the legacy
   `--color-*` bridge in `tokens/semantic.css` is being migrated away (issue
   #173) and is steward-frozen so it can only shrink.
3. Scope selectors to a `.chirp-theme-*` block; test with nested components.

**📖 Background:**
- [CSS Scoping Rules](./CSS_SCOPING_RULES.md)
- [Quick Reference](./CSS_QUICK_REFERENCE.md)

---

## 📱 Responsive Design System

**Bengal uses standardized breakpoints and responsive patterns.**

**📖 Essential reading for component development:**
- [Responsive Design System](./RESPONSIVE_DESIGN_SYSTEM.md) - Complete guide

**Key principles:**
1. **Mobile-first approach** - Start with mobile, enhance for larger screens
2. **Standard breakpoints** - 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
3. **Semantic patterns** - Stack→Side-by-side, Compress→Expand, Hide→Show
4. **Avoid overlap** - Use `max-width: 639px` (not 640px) with `min-width: 640px`
5. **Test at key sizes** - 375px (iPhone), 768px (tablet), 1280px (desktop)

---

## Overview

This theme uses a **two-layer design token system** following modern CSS architecture best practices:

```
Foundation Tokens → Semantic Tokens → Components
(primitives)       (purpose-based)    (UI elements)
```

## File Structure

```
css/
├── tokens/
│   ├── foundation.css    # Primitive values (color scales, sizes, fonts)
│   ├── typography.css    # Typography tokens
│   └── semantic.css      # Purpose-based --color-* tokens + chirpui bridge
├── base/
│   ├── reset.css         # CSS reset
│   ├── typography.css    # Text styling
│   ├── utilities.css     # Utility classes
│   ├── interactive-patterns.css  # Common interactive patterns (extracted)
│   ├── accessibility.css # A11y styles
│   ├── print.css         # Print styles
│   └── transitions.css   # Shared transition rules
├── composition/
│   └── layouts.css       # Layout primitives
├── layouts/              # Retained layout chrome (header, footer, grid, page-header)
├── utilities/            # motion.css, gradient-borders.css
├── components/           # ~39 retained theme-specific component files - MODULAR
│   ├── buttons.css       # Button component (~464 lines)
│   ├── forms.css         # Form component
│   └── ... (kept only while the retained theme surface needs them)
├── style.css             # @layer entry point (imports the above, then chirp-theme.css)
└── chirp-theme.css       # BESPOKE ACTIVE SURFACE — active palette + .chirp-theme-* rules
                          #   (self-wrapped in `@layer chirp-theme`)
```

There is no `tokens/palettes/` or `pages/` directory — the active palette lives
in `chirp-theme.css`'s `:root` / `[data-theme="dark"]` blocks.

**📖 Why Modular CSS?** See [MODULAR_CSS_RATIONALE.md](./MODULAR_CSS_RATIONALE.md) for detailed explanation of why we keep components separate instead of consolidating.

## Design Token Layers

### 1. Foundation Tokens (`tokens/foundation.css`)

**Purpose:** Raw, primitive values  
**Usage:** Never use directly in components

Provides:
- Color scales (blue-50 to blue-900, etc.)
- Size primitives (--size-0 to --size-32)
- Font size primitives (--font-size-12 to --font-size-72)
- Base values for transitions, shadows, etc.

**Example:**
```css
--blue-500: #2196f3;
--size-4: 1rem;
--font-size-16: 1rem;
```

### 2. Semantic Tokens (`tokens/semantic.css`)

**Purpose:** Purpose-based, meaningful names  
**Usage:** ALWAYS use these in components

Maps foundation tokens to semantic purposes:

**Colors:**
- `--color-primary`, `--color-secondary`, `--color-accent`
- `--color-text-primary`, `--color-text-secondary`, `--color-text-muted`
- `--color-bg-primary`, `--color-bg-secondary`, `--color-bg-hover`
- `--color-border`, `--color-border-light`, `--color-border-dark`
- `--color-success`, `--color-warning`, `--color-error`, `--color-info`

**Spacing:**
- `--space-0` through `--space-32` (maps to --size-*)
- `--space-component-gap`, `--space-section-gap`

**Typography:**
- `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--text-xl`, etc.
- `--text-heading-1` through `--text-heading-6`
- `--font-light`, `--font-normal`, `--font-medium`, `--font-semibold`, `--font-bold`
- `--leading-tight`, `--leading-normal`, `--leading-relaxed`
- `--tracking-tight`, `--tracking-normal`, `--tracking-wide`

**Shadows & Borders:**
- `--shadow-sm`, `--shadow-md`, `--shadow-lg`, `--shadow-xl`
- `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-xl`

**Transitions:**
- `--transition-fast`, `--transition-base`, `--transition-slow`
- `--ease-in`, `--ease-out`, `--ease-in-out`

**Layout:**
- `--container-sm`, `--container-md`, `--container-lg`, `--container-xl`
- `--prose-width`, `--content-width`
- `--breakpoint-sm`, `--breakpoint-md`, `--breakpoint-lg`

**Z-Index:**
- `--z-dropdown`, `--z-sticky`, `--z-fixed`, `--z-modal`, `--z-tooltip`

### 3. Components

**Rule:** ONLY use semantic tokens, never foundation tokens or hardcoded values.

**Good:**
```css
.button {
  padding: var(--space-4);
  background: var(--color-primary);
  border-radius: var(--radius-md);
  transition: var(--transition-fast);
}
```

**Bad:**
```css
.button {
  padding: 16px;                    /* ❌ Hardcoded */
  background: var(--blue-500);      /* ❌ Foundation token */
  border-radius: 0.25rem;           /* ❌ Hardcoded */
}
```

## Dark Mode

The **active** dark palette lives in `chirp-theme.css` (the shipped surface),
which redefines the `--chirpui-*` tokens and the legacy `--color-*` aliases for
`[data-theme="dark"]`:

```css
@layer chirp-theme {
  [data-theme="dark"] {
    --chirpui-text: #e8efea;
    --chirpui-accent: #2dd4bf;
    /* A theme that overrides --chirpui-accent MUST pair it with a
       contrast-checked --chirpui-on-accent (enforced by the parity test). */
    --chirpui-on-accent: #0a1012;
    /* ... legacy --color-* aliases remapped onto the above */
  }
}
```

The retained `semantic.css` still ships its own neutral `[data-theme="dark"]`
block plus a `@media (prefers-color-scheme: dark)` fallback for the baseline
token system; `chirp-theme.css` overrides it via the late `chirp-theme` layer.

## Adding New Tokens

### For New Colors (active theme):
1. Define the value as a `--chirpui-*` token in `chirp-theme.css`'s `:root`
   (and `[data-theme="dark"]`) — this is the active palette.
2. If a `--color-*` alias is needed for retained baseline CSS, map it in the
   same block.

### For New Components (active theme):
1. Add `.chirp-theme-*` rules to `chirp-theme.css` (the `chirp-theme` layer).
2. Author against the public `--chirpui-*` namespace; fall back to a `--color-*`
   alias only for tokens with no chirpui equivalent.

> Retained baseline files (`components/`, `layouts/`, `semantic.css`) still use
> the `--color-*` semantic tokens; new bespoke work belongs in `chirp-theme.css`.

## Migration: legacy `--color-*` → public `--chirpui-*`

`chirp-theme.css` historically styled itself through the legacy `--color-*`
namespace. It is migrating onto the public `--chirpui-*` tokens (issue #173) so
upstream chirp-ui token changes reach theme components directly. The migration
is **incremental**:

- New rules author against `--chirpui-*` directly.
- `tokens/semantic.css` documents the 1:1 legacy→chirpui mapping and remains the
  bridge for not-yet-migrated rules and tokens with no chirpui equivalent.
- `tests/test_theme_token_parity.py` freezes the legacy reference count at a
  ceiling that may only shrink, blocking any **new** legacy color token.

## Best Practices

✅ **Do:**
- Use semantic tokens exclusively
- Follow the cascade: Foundation → Semantic → Component
- Add dark mode overrides for new color tokens
- Use CSS custom properties for dynamic values

❌ **Don't:**
- Use foundation tokens directly in components
- Hardcode values (colors, sizes, etc.)
- Create component-specific variables in foundation.css
- Mix semantic and hardcoded values

## Performance

- **Semantic tokens:** ~240 `--color-*`/`--space-*`/etc. definitions in
  `semantic.css`, plus the active `--chirpui-*` palette in `chirp-theme.css`.
- **Build:** concat-from-`@import`, stdlib-only — no preprocessor step.
- **Runtime:** cascade-layer ordering resolves overrides without specificity
  inflation; optimized CSS custom property cascade.

## Resources

- [CSS Custom Properties (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Design Tokens (W3C)](https://design-tokens.github.io/community-group/format/)
- [CUBE CSS Methodology](https://cube.fyi/)

## Questions?

- [CSS_ARCHITECTURE_EVALUATION.md](./CSS_ARCHITECTURE_EVALUATION.md) — local
  architecture evaluation.
- `docs/plans/PLAN-css-scope-and-layer.md` (repo root) — the `@scope` + `@layer`
  decision and migration plan that this theme dogfoods.
