---
title: chirp-theme
description: Static-first Bengal theme packaged inside the chirp-ui project
draft: false
weight: 35
lang: en
type: doc
keywords: [chirp-theme, bengal theme, chirp-ui, docs theme]
tags: [theme, theming]
category: theming
---

`chirp-theme` is a **static-first Bengal theme** packaged in the `chirp-ui` project.
It takes the visual language from the `b-site` marketing shell and adapts it to
Bengal's documentation and content templates: warm paper surfaces, phosphor dark
mode, cyan and amber accents, crisp radii, and an editorial docs chrome.

The `chirp-ui` docs site uses this theme directly, so the package gets exercised
on a real Bengal site rather than living as a disconnected example.

## Quickstart: Adopt It on a Bengal Site

If you have a [Bengal](https://github.com/lbliii/bengal) site, applying
chirp-theme is three steps. No separate theme package — the theme ships inside
`chirp-ui` and registers through the `bengal.themes` entry point.

**1. Install (this also installs the theme).**

```bash
uv add chirp-ui
# or
pip install chirp-ui
```

`chirp-ui` declares the theme entry point
`chirp-theme = "bengal_themes.chirp_theme"`, so Bengal discovers it
automatically once the package is installed. You also need **Bengal >=0.3.3**
(for the `library_asset_tags()` hook described below); add it as a build
dependency if it is not already present:

```bash
uv add "bengal>=0.3.3"
```

**2. Set the theme in your site config.**

```yaml
# config/_default/theme.yaml  (or the theme block in bengal.toml)
theme:
  name: "chirp-theme"
```

**3. Build and serve.**

```bash
uv run bengal build
uv run bengal serve
```

That is enough to render a Bengal docs or marketing site with chirp-theme's
shell, typography, and dark mode.

> **Requires Bengal >=0.3.3 — `library_asset_tags()`.** chirp-theme's
> `base.html` calls Bengal's `library_asset_tags()` to inject the component
> library's bundled `chirpui.css` (the base tokens, reset, layout grid, and
> component styles). That hook ships in **Bengal 0.3.3**. On older Bengal the
> call is silently skipped, `chirpui.css` never loads, and the page renders
> with collapsed spacing and a broken grid in the footer and top bar. If your
> theme looks unstyled, check your Bengal version first.

A new-user adoption checklist also lives on the
[[/docs/get-started/installation/#apply-the-chirp-theme-bengal-theme|Installation]]
page.

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
- Retained core parity templates for `blog/shell.html`, `blog/list.html`, `blog/single.html`, `post.html`, `search.html`, and `404.html`
- Retained taxonomy/archive/author, learning/content, autodoc/API reference,
  shortcode/embed, root alias, and utility templates listed in the parity matrix

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

In the current cutover, "standalone" means the package owns the full runtime
surface. The theme currently vendors the Bengal default asset and partial
baseline into `chirp-theme`, then layers the `chirp-theme` shell and styling on
top. The next phase is to replace more of that inherited baseline with more
opinionated `chirp-ui`-driven patterns.

## Longer-Term Direction

The broader goal is to build a better and more comprehensive alternative to the
historical Bengal default theme using modern `chirp-ui`, Kida, and Alpine-era
patterns. The original default theme carries early-project CSS and template
conventions; `chirp-theme` is the place to reach parity, simplify the old
patterns, and then go beyond them.

That evolution happens from a standalone package baseline, not through continued
runtime dependence on Bengal default internals.

## Parity Policy

`chirp-theme` treats Bengal default's broad output coverage as the long-term
target, but it does not treat the copied default templates and CSS as the target
implementation.

- Retained: shell, docs, generic pages, blog/post, search, 404, taxonomy/archive/authors, learning/content, autodoc/reference/API-hub, shortcodes/embeds, root aliases, and utility pages
- Retained surfaces should be rebuilt with Chirp UI-native templates and tokens rather than preserved as copied default-theme implementations
- Deferred: niche graph/data-table/experimental UI until an output contract needs them

The repo-level parity matrix in `docs/theming/chirp-theme-parity-matrix.md` is the
source of truth for those decisions.

The canonical source guide is
[`docs/theming/chirp-theme.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/theming/chirp-theme.md?plain=1).
