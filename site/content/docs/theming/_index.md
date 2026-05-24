---
title: Theming
description: CSS variables, dark mode, and customization
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, theming, css, dark mode, variables]
category: theming
---

# Theming

chirp-ui uses `prefers-color-scheme` for dark mode. Override any `--chirpui-*` variable to customize.

## Base Variables

```css
:root {
    --chirpui-accent: #7c3aed;
    --chirpui-container-max: 80rem;
}
```

Base colors drive derived states (hover, active, light, muted) via `color-mix()`.

## Manual Light/Dark Toggle

Set `data-theme="light"` or `data-theme="dark"` on `<html>`.

## Optional Themes

```html
<link rel="stylesheet" href="/static/themes/holy-light.css">
```

## Curated Theme Packs

Chirp UI also ships token-only catalog packs for fresh apps:

```html
<link rel="stylesheet" href="/static/chirpui.css">
<link rel="stylesheet" href="/static/themes/atlas.css">
```

Packaged options are `atlas`, `ember`, and `sage`. Each defines light, dark,
and `system` branches using only `--chirpui-*` tokens. The canonical source
guide is
[`docs/theming/app-theme.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/theming/app-theme.md?plain=1).
The runnable component showcase includes a theme-pack matrix at `/theme-packs`.

## Bengal Theme

For fully static Bengal sites, `chirp-ui` now also ships `chirp-theme`, a
static-first docs and marketing theme packaged in this project.

- [chirp-theme](/docs/theming/chirp-theme/) - packaged Bengal theme with the `b-site`-inspired aesthetic
- [Bengal theme controls anatomy](/docs/theming/bengal-theme-controls/) - packaged theme hooks for appearance, search, mobile navigation, TOC, and docs tabs

## Motion

All animations respect `prefers-reduced-motion`. No configuration needed.
