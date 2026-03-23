---
title: Creating themes
description: data-theme, data-style, and token overrides
draft: false
weight: 35
lang: en
type: doc
keywords: [chirp-ui, theme, dark mode]
icon: paint-brush
---

# Creating themes

## Two axes

- **`data-theme`**: `light`, `dark`, `system` — color mode.
- **`data-style`**: `default`, `neumorphic` — artistic style.

Set both on the root element (typically `<html>`):

```html
<html data-theme="dark" data-style="default">
```

## Bootstrapping

`chirpui.js` reads `localStorage` keys **`chirpui-theme`** and **`chirpui-style`** and applies them before first paint to avoid flash.

## Holy Light

Optional **`themes/holy-light.css`** demonstrates a dark “Holy Light” token layer — override `--chirpui-*` variables without duplicating component rules.

## Overrides

Prefer token overrides in a small app stylesheet loaded after `chirpui.css`:

```css
:root {
  --chirpui-radius-md: 12px;
  --chirpui-space-page-gap: var(--chirpui-spacing-xl);
}
```

## Related

- [Design tokens](./design-tokens.md)
- [Color system](./color-system.md)
