---
title: chirp-theme
description: Static-first Bengal theme packaged inside the chirp-ui project
draft: false
weight: 35
lang: en
type: doc
keywords: [chirp-theme, bengal theme, chirp-ui, docs theme]
category: theming
---

`chirp-theme` is a **static-first Bengal theme** packaged in the `chirp-ui` project.
It takes the visual language from the `b-site` marketing shell and adapts it to
Bengal's documentation and content templates: warm paper surfaces, phosphor dark
mode, cyan and amber accents, crisp radii, and an editorial docs chrome.

The `chirp-ui` docs site uses this theme directly, so the package gets exercised
on a real Bengal site rather than living as a disconnected example.

## Enable It

Set the active Bengal theme in your site configuration:

```yaml
theme:
  name: "chirp-theme"
```

## What v1 Includes

- A packaged Bengal theme entry point: `chirp-theme = "bengal_themes.chirp_theme"`
- A reusable theme stylesheet layered on top of Bengal's `default` theme
- Static-first overrides for `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, and `doc/single.html`

## Design Scope

v1 focuses on:

- docs sites
- product/marketing pages
- content-heavy static sites

v1 does **not** try to reproduce every Chirp application-shell pattern inside
Bengal. The goal is a strong static-site shell first, with a small template
surface and a clear upgrade path.

## Why The Theme Is Self-Contained

Today Bengal's template integration loads theme templates from filesystem-backed
theme directories. That means a Bengal theme package cannot yet import
`chirp_ui` package templates directly during theme resolution.

For v1, `chirp-theme` stays self-contained:

- Bengal resolves the theme package on its own
- the theme carries the templates it needs
- the docs site can build without any special theme-loader bridge

## Future Loader Bridge

The follow-up plan is to add a Bengal loader bridge so packaged themes can
consume `chirp-ui` templates directly instead of carrying their own copies or
parallel markup.

That later step should:

- reduce duplication between `chirp_ui` and `chirp-theme`
- make the Bengal theme a thinner composition layer
- let future theme templates import package-provided UI primitives more directly
