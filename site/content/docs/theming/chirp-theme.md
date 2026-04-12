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
- A standalone theme package with its own shell templates, partials, and assets
- Static-first templates for `base.html`, `home.html`, `page.html`, `doc/home.html`, `doc/list.html`, and `doc/single.html`

## Design Scope

v1 focuses on:

- docs sites
- product/marketing pages
- content-heavy static sites

v1 does **not** try to reproduce every Chirp application-shell pattern inside
Bengal. The goal is a strong static-site shell first, with enough coverage to
grow into a credible Bengal default-v2 candidate over time.

## Ownership Model

`chirp-theme` is owned by the `chirp-ui` project and should behave like a real,
installable Bengal theme package, not a thin overlay on Bengal default.

That means the package itself should own:

- the shell templates
- theme partials/macros
- the canonical `assets/css/style.css` entrypoint
- any JS, icons, fonts, favicons, or manifests referenced by the shell

The `chirp-ui` docs site is the acceptance target for that contract, so the
theme is continuously dogfooded on a real Bengal site.

## Longer-Term Direction

The broader goal is to build a better and more comprehensive alternative to the
historical Bengal default theme using modern `chirp-ui`, Kida, and Alpine-era
patterns. The original default theme carries early-project CSS and template
conventions; `chirp-theme` is the place to reach parity, simplify the old
patterns, and then go beyond them.

That evolution happens from a standalone package baseline, not through continued
runtime dependence on Bengal default internals.
