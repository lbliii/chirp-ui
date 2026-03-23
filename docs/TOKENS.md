# chirp-ui Tokens

This document defines the token contract for `chirpui.css`.

## Token tiers

1. **Core primitives**: raw spacing, radius, typography, color foundations, motion, and shadows.
2. **Semantic tokens**: interaction/state semantics and theme-aware aliases.
3. **Component aliases**: optional component-level defaults that map to semantic/core tokens.

## Spacing tokens

### Core spacing scale

The raw spacing scale remains the base contract:

- `--chirpui-spacing-xs`
- `--chirpui-spacing-sm`
- `--chirpui-spacing`
- `--chirpui-spacing-md`
- `--chirpui-spacing-lg`
- `--chirpui-spacing-xl`
- `--chirpui-spacing-2xl`
- `--chirpui-spacing-3xl`

Recommended usage by step:

| Token | Typical role | Examples |
| ------- | -------------- | ---------- |
| `xs` | tight adjacency | badge/code clusters, icon-text spacing, compact meta |
| `sm` | control grouping | button groups, compact stacks, inline forms |
| `base` | default component rhythm | card body padding, standard stack/grid gaps |
| `md` | section rhythm | section header spacing, result areas, denser page groups |
| `lg` | page rhythm | page-level stacks, larger split layouts |
| `xl+` | hero and shell breathing room | large bands, roomy shells, marketing/editorial layouts |

### Semantic spacing aliases

ChirpUI should prefer semantic aliases over raw steps when the spacing communicates intent.

Current semantic spacing aliases:

| Token | Purpose | Default |
| ------- | --------- | --------- |
| `--chirpui-space-inline-gap` | Tight inline adjacency | `spacing-xs` |
| `--chirpui-space-control-gap` | Small control/button grouping | `spacing-sm` |
| `--chirpui-space-cluster-gap` | Wrapping inline clusters | `spacing-xs` |
| `--chirpui-space-stack-gap` | Default vertical layout rhythm | `spacing` |
| `--chirpui-space-section-gap` | Section header/content separation | `spacing-md` |
| `--chirpui-space-page-gap` | Page-level stack separation | `spacing-lg` |
| `--chirpui-space-container-gutter` | Container inline padding | `spacing` |
| `--chirpui-space-card-padding` | Card inset/padding | `spacing` |
| `--chirpui-space-card-gap` | Card internal grouping | `spacing-sm` |
| `--chirpui-space-surface-padding` | Surface inset/padding | `spacing` |
| `--chirpui-space-result-gap` | Result/status follow-up spacing | `spacing-md` |

### Spacing doctrine by layer

- **Primitives**: `container`, `grid`, `stack`, and `cluster` expose reusable rhythm. Use these first.
- **Components**: cards, surfaces, toolbars, and headers should consume semantic aliases like card/control/section spacing rather than hard-coded lengths.
- **Sections**: section headers and section bodies should align to `section-gap`.
- **Pages**: page shells and top-level stacks should align to `page-gap`.
- **Utilities**: helper classes should be small, named by role, and mainly exist to bridge markup that does not need a dedicated component.

### Page header component tokens

Override these to customize `page_header` without BEM class overrides:

| Token | Purpose | Default |
| ------- | --------- | --------- |
| `--chirpui-page-header-padding` | Header bar padding | `spacing-md` |
| `--chirpui-page-header-gap` | Gap between title block and actions | `space-page-gap` |
| `--chirpui-page-header-title-size` | H1 font size | `ui-lg` |
| `--chirpui-page-header-title-weight` | H1 font weight | `ui-font-weight-bold` |
| `--chirpui-page-header-bg` | Header background | `transparent` |
| `--chirpui-page-header-border` | Header border | `none` |

### Micro-spacing

Small optical adjustments are still allowed for tiny UI details such as inline code chips, cursors, or small glyph pairs, but they should stay exceptional. When a micro-pattern repeats across several components, promote it into a named alias instead of scattering raw values.

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

## Typography overrides

ChirpUI inherits font settings from the document. To avoid layout shift when using webfonts, follow the usual pattern: load faces with `font-display: optional` (or swap) in your app CSS, and map heading/body roles to semantic typography tokens (`--chirpui-ui-*`, `--chirpui-font-*`) already defined in `chirpui.css` rather than hard-coding `font-family` on every component.

Override at the shell or page level, for example:

```css
:root {
  font-size: var(--chirpui-font-base);
}
```

For marketing or code-heavy areas, set `font-family` on a wrapper class so ChirpUI components inside still inherit consistently.
