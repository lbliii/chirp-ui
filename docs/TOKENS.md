# chirp-ui Tokens

This document defines the token contract for `chirpui.css`.

## Token tiers

1. **Core primitives**: raw spacing, radius, typography, color foundations, motion, and shadows.
2. **Semantic tokens**: interaction/state semantics and theme-aware aliases.
3. **Component aliases**: optional component-level defaults that map to semantic/core tokens.

## Precedence

Token resolution follows this order:

1. `:root` defaults
2. `[data-theme="light"|"dark"|"system"]` mode overrides
3. `[data-style="default"|"neumorphic"]` artistic style overrides
4. capability overrides in `@supports` blocks (for example `oklch` and `color-mix(in oklch, ...)`)

## Two-axis theming model

chirp-ui supports both a color mode and a style preset:

- `data-theme`: `light`, `dark`, `system`
- `data-style`: `default`, `neumorphic`

Use them together on the root element:

```html
<html data-theme="dark" data-style="neumorphic">
```

If `data-style` is missing, runtime defaults to `default`.

## Motion tokens

- `--chirpui-motion-fast`, `--chirpui-motion-base`, `--chirpui-motion-slow`, `--chirpui-motion-slower`
- `--chirpui-ease-standard`, `--chirpui-ease-emphasized`, `--chirpui-ease-spring`
- Compatibility aliases:
  - `--chirpui-transition`
  - `--chirpui-transition-slow`
  - `--chirpui-transition-emphasized`

Guideline: transitions should use tokenized timings/easing, not raw `ms`/`s` values in component rules.

## Elevation tokens

- Core shadows: `--chirpui-shadow-xs|sm|md|lg|xl`
- Semantic elevation:
  - `--chirpui-elevation-0..4`
  - `--chirpui-elevation-card-rest`
  - `--chirpui-elevation-card-hover`
  - `--chirpui-elevation-floating`
  - `--chirpui-elevation-overlay`
  - `--chirpui-elevation-topbar`

Suggested mapping:

- Resting cards/surfaces: `card-rest` or `elevation-1`
- Hovered cards: `card-hover` or `elevation-2`
- Menus/tooltips/toasts: `elevation-floating`
- Modal/drawer/tray/popover panels: `elevation-overlay`
- Top bar separation: `elevation-topbar` (subtle)

### Neumorphism semantic aliases

With `data-style="neumorphic"`, the style layer remaps component elevation/state aliases through:

- `--chirpui-neu-raised`
- `--chirpui-neu-inset`
- `--chirpui-neu-pressed`
- `--chirpui-neu-highlight-border`

Guideline: components should consume semantic aliases (`--chirpui-elevation-*`, `--chirpui-state-*`) so style presets can restyle without markup changes.

## State tokens

- `--chirpui-state-surface-hover`
- `--chirpui-state-surface-active`
- `--chirpui-state-border-hover`
- `--chirpui-state-border-active`
- `--chirpui-state-text-hover`
- `--chirpui-state-focus-outline`
- `--chirpui-state-focus-offset`

Guideline: focus-visible styles should prefer the state focus aliases for consistency.
