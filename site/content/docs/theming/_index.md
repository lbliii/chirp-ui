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

## Motion

All animations respect `prefers-reduced-motion`. No configuration needed.
