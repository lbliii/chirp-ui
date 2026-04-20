# CSS override surface

**Status:** stable API as of chirp-ui 0.4.x
**Related:** `docs/plans/PLAN-css-scope-and-layer.md`, `docs/DESIGN-css-registry-projection.md`

## The one-line contract

chirp-ui declares its cascade order at the top of every generated `chirpui.css`:

```css
@layer chirpui.reset, chirpui.token, chirpui.base, chirpui.component, chirpui.utility;
```

Every chirp-ui rule lives in one of those layers. **Any layer you declare after loading `chirpui.css` wins over all of them, no specificity tricks required.**

## Quick recipe

```css
/* your-app.css — loaded AFTER chirpui.css */
@layer app.overrides {
    .chirpui-card      { border-color: var(--brand-teal); }
    .chirpui-btn--primary { background: var(--brand-violet); }
}
```

That's it. No `!important`, no `.app .chirpui-card` specificity stacking, no wrapping selectors. The `@layer app.overrides` block is declared later than any of chirp-ui's layers, so CSS's layer cascade resolves in your favor automatically.

## Three override paths — pick the lightest-weight one

chirp-ui exposes three override surfaces. Reach for the one whose scope matches your change.

### 1. Design tokens (`--chirpui-*` custom properties) — prefer this

For colorway, spacing scale, elevation, motion curve, typography. No layer needed; custom properties inherit normally.

```css
:root {
    --chirpui-accent: oklch(0.65 0.18 290);
    --chirpui-radius: 0.75rem;
}

[data-theme="dark"] {
    --chirpui-accent: oklch(0.72 0.18 290);
}
```

This is the cheapest override and the one most consumer apps need. A token edit reflows every component that references the token — no per-component rules to maintain.

### 2. Component rules via `@layer app.overrides` — the escape hatch

When a change isn't expressible via a token (layout tweak, disabling a behavior, swapping a pseudo-element, one-off branding flourish), write the rule in `@layer app.overrides`:

```css
@layer app.overrides {
    .chirpui-card {
        border-radius: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    /* Your own layout — lives outside the chirp-ui namespace entirely. */
    .my-feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
    }
}
```

Within `app.overrides`, normal cascade rules apply (specificity + source order). chirp-ui's layers cannot beat anything you write here.

### 3. Unlayered rules — supported, but avoid for new work

Rules you write outside any `@layer { … }` block still win over chirp-ui's layered rules (unlayered beats layered in the cascade). This is how pre-layer override styles keep working after upgrading to a layered `chirpui.css`.

```css
/* Works — unlayered rules always beat layered ones. */
.chirpui-card { border-color: var(--brand-teal); }
```

It's preserved for backwards-compatibility. For new work, prefer `@layer app.overrides` — it makes the override intent explicit and keeps the override surface discoverable in consumer codebases.

## Migrating from specificity-stacked overrides

Before:

```css
/* pre-layer override — still works, but fragile */
.app .chirpui-card,
body .chirpui-card {
    border-color: var(--brand-teal) !important;
}
```

After:

```css
@layer app.overrides {
    .chirpui-card { border-color: var(--brand-teal); }
}
```

The rule wins via layer order, not specificity. You stop fighting future chirp-ui changes that bump their own selector weight.

## What each chirpui layer contains today

| Layer | Contents | S-state |
|-------|----------|---------|
| `chirpui.reset` | Declared but empty today. Browser reset (`*`, `body`, `img`, etc.) currently lives inside `chirpui.component` and will migrate here in a later sprint. | Reserved |
| `chirpui.token` | Declared but empty today. `:root { --chirpui-* }` tokens currently live inside `chirpui.component` and will migrate here in a later sprint. | Reserved |
| `chirpui.base` | Declared but empty today. Element-level defaults (`html { scrollbar-gutter }`, `:root { accent-color }`, etc.) will migrate here in a later sprint. | Reserved |
| `chirpui.component` | Every component's rules (`.chirpui-card`, `.chirpui-btn`, modifiers, theme/style variants). | Populated |
| `chirpui.utility` | Framework utilities (`.chirpui-visually-hidden`, `.chirpui-focus-ring`, `.chirpui-flow`, `.chirpui-grid--auto-fill`, prose styles). Beats components. | Populated |

The "Reserved" layers are declared so future reorganization sprints can move rules into them without changing the public cascade API. Consumers that declare `@layer app.overrides` today will continue to win regardless of where chirp-ui's rules live internally.

## Gotchas

- **Custom properties are not layer-aware** in the cascade-order sense. If `chirpui.token` sets `--chirpui-accent` and your `@layer app.overrides` also sets `--chirpui-accent` on the same element, cascade resolves at the property level and your layer wins. But if you set `--chirpui-accent` on a *different* selector with lower specificity, specificity decides — not layer position. Rule of thumb: set tokens on `:root`, `[data-theme="*"]`, or a top-level wrapper you control.
- **Inside `app.overrides`, specificity still matters.** `.chirpui-card` and `.foo .chirpui-card` inside the same layer resolve by specificity. The layer only gives you priority over chirp-ui, not inside your own code.
- **Load order matters for layer registration.** If `chirpui.css` is loaded *after* your override stylesheet, your `app.overrides` layer gets declared first, then chirp-ui's declaration appends its layers *before* `app.overrides` in the cascade order — and chirp-ui wins. Always load `chirpui.css` first.
- **Pre-processors like Sass don't speak `@layer`.** If you're compiling from Sass, make sure `@layer` blocks survive the pipeline — Dart Sass 1.34+ passes them through unchanged.
