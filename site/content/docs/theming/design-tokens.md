---
title: Design tokens
description: Spacing, semantic aliases, elevation, and token precedence
draft: false
weight: 31
lang: en
type: doc
keywords: [chirp-ui, tokens, css]
icon: sliders
---

# Design tokens

`chirpui.css` defines **`--chirpui-*` variables** in three conceptual tiers:

1. **Core primitives** — spacing, radius, typography, color foundations, motion, shadows.
2. **Semantic tokens** — interaction/state and theme-aware aliases.
3. **Component aliases** — optional defaults mapping to semantic/core tokens.

## Spacing scale

The raw spacing scale is the base contract. All values live on `:root`.

| Token | Step | Typical role | Examples |
|-------|------|--------------|----------|
| `--chirpui-spacing-xs` | xs | tight adjacency | badge/code clusters, icon-text spacing, compact meta |
| `--chirpui-spacing-sm` | sm | control grouping | button groups, compact stacks, inline forms |
| `--chirpui-spacing` | base | default component rhythm | card body padding, standard stack/grid gaps |
| `--chirpui-spacing-md` | md | section rhythm | section header spacing, result areas, denser page groups |
| `--chirpui-spacing-lg` | lg | page rhythm | page-level stacks, larger split layouts |
| `--chirpui-spacing-xl` | xl | hero/shell breathing room | large bands, roomy shells |
| `--chirpui-spacing-2xl` | 2xl | hero/shell breathing room | marketing/editorial layouts |
| `--chirpui-spacing-3xl` | 3xl | hero/shell breathing room | full-bleed hero sections |

## Semantic spacing aliases

Prefer semantic aliases over raw steps when the spacing communicates intent.

| Token | Purpose | Default |
|-------|---------|---------|
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

## Page header tokens

Override `--chirpui-page-header-*` to customize `page_header` without BEM class overrides.

| Token | Purpose | Default |
|-------|---------|---------|
| `--chirpui-page-header-padding` | Header bar padding | `spacing-md` |
| `--chirpui-page-header-gap` | Gap between title block and actions | `space-page-gap` |
| `--chirpui-page-header-title-size` | H1 font size | `ui-lg` |
| `--chirpui-page-header-title-weight` | H1 font weight | `ui-font-weight-bold` |
| `--chirpui-page-header-bg` | Header background | `transparent` |
| `--chirpui-page-header-border` | Header border | `none` |

## Elevation tokens

### Core shadows

Five raw shadow intensities:

```css
--chirpui-shadow-xs
--chirpui-shadow-sm
--chirpui-shadow-md
--chirpui-shadow-lg
--chirpui-shadow-xl
```

### Semantic elevation

| Token | Use |
|-------|-----|
| `--chirpui-elevation-0` | Flat / no shadow |
| `--chirpui-elevation-1` | Resting cards and surfaces |
| `--chirpui-elevation-2` | Hovered cards |
| `--chirpui-elevation-3` | Raised panels |
| `--chirpui-elevation-4` | Maximum emphasis |
| `--chirpui-elevation-card-rest` | Card default (maps to `elevation-1`) |
| `--chirpui-elevation-card-hover` | Card hover (maps to `elevation-2`) |
| `--chirpui-elevation-floating` | Menus, tooltips, toasts |
| `--chirpui-elevation-overlay` | Modal, drawer, tray, popover panels |
| `--chirpui-elevation-topbar` | Top bar separation (subtle) |

Components should consume semantic aliases so style presets can restyle without markup changes. With `data-style="neumorphic"`, the style layer remaps elevation through `--chirpui-neu-raised`, `--chirpui-neu-inset`, `--chirpui-neu-pressed`, and `--chirpui-neu-highlight-border`.

## State tokens

| Token | Purpose |
|-------|---------|
| `--chirpui-state-surface-hover` | Surface background on hover |
| `--chirpui-state-surface-active` | Surface background on active/press |
| `--chirpui-state-border-hover` | Border color on hover |
| `--chirpui-state-border-active` | Border color on active/press |
| `--chirpui-state-text-hover` | Text color on hover |
| `--chirpui-state-focus-outline` | Focus-visible outline color |
| `--chirpui-state-focus-offset` | Focus-visible outline offset |

Focus-visible styles should prefer the state focus aliases for consistency.

## Two-axis theming

chirp-ui supports both a **color mode** and a **style preset** on the root element:

- `data-theme` — `light`, `dark`, or `system`
- `data-style` — `default` or `neumorphic`

```html
<html data-theme="dark" data-style="neumorphic">
```

If `data-style` is absent, runtime defaults to `default`.

## Precedence

Token resolution order:

1. `:root` defaults
2. `[data-theme="light"|"dark"|"system"]`
3. `[data-style="default"|"neumorphic"]`
4. Capability overrides in `@supports` (e.g. `oklch`, `color-mix`)

## Motion tokens

### Durations

```css
--chirpui-motion-fast
--chirpui-motion-base
--chirpui-motion-slow
--chirpui-motion-slower
```

### Easing curves

```css
--chirpui-ease-standard
--chirpui-ease-emphasized
--chirpui-ease-spring
```

### Compatibility aliases

```css
--chirpui-transition            /* maps to motion-base + ease-standard */
--chirpui-transition-slow       /* maps to motion-slow + ease-standard */
--chirpui-transition-emphasized /* maps to motion-base + ease-emphasized */
```

Transitions should use tokenized timings and easing, not raw `ms`/`s` values in component rules.

## Related

- [Typography](./typography.md)
- [Creating themes](./creating-themes.md)
