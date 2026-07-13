---
title: Installation
description: Install chirp-ui using pip or uv
draft: false
weight: 10
lang: en
type: doc
tags: [installation]
keywords: [install, pip, uv, python 3.14]
icon: download
---

# Installation

## Requirements

:::{checklist} Prerequisites
:show-progress:
- [ ] Python 3.14+ installed
- [ ] Chirp installed (for full integration) or Kida (for standalone use)
:::{/checklist}

## Install

:::{tab-set}
:::{tab-item} uv

```bash
uv add chirp-ui
```

:::{/tab-item}

:::{tab-item} pip

```bash
pip install chirp-ui
```

:::{/tab-item}

:::{tab-item} With Chirp (recommended)

```bash
uv add "bengal-chirp[ui]"
# or
pip install "bengal-chirp[ui]"
```

:::{/tab-item}
:::{/tab-set}

## Verify Installation

```python
import chirp_ui
print(chirp_ui.__version__)  # e.g. "0.11.4"
```

## Apply the chirp-theme Bengal Theme

The same `chirp-ui` package also ships **chirp-theme**, a static-first Bengal
theme. If you build a documentation or marketing site with
[Bengal](https://github.com/lbliii/bengal), you can adopt the theme without a
separate install — `uv add chirp-ui` registers it through the
`bengal.themes` entry point (`chirp-theme = "bengal_themes.chirp_theme"`).

:::{checklist} Theme prerequisites
:show-progress:
- [ ] Bengal **>=0.3.3** (needed for `library_asset_tags()`, which links the
  bundled `chirpui.css`)
- [ ] `chirp-ui` installed (brings the theme via its `bengal.themes` entry point)
:::{/checklist}

Point your Bengal site config at the theme by setting `theme.name`:

```yaml
# config/_default/theme.yaml  (or the theme block in bengal.toml)
theme:
  name: "chirp-theme"
```

Then build and serve the site:

```bash
uv run bengal build
uv run bengal serve
```

> **Why Bengal >=0.3.3?** chirp-theme's `base.html` calls
> `library_asset_tags()` to inject the component library's `chirpui.css`. That
> hook lands in Bengal **0.3.3**. On older Bengal the call is skipped and the
> base CSS never loads, so spacing and grid layout collapse in the footer and
> top bar. Pin `bengal>=0.3.3` to be safe.

For the theme's architecture, ownership model, and parity policy, see
[[/docs/theming/chirp-theme/|chirp-theme]].

## Next Steps

- [[/docs/theming/chirp-theme/|Apply chirp-theme]] — Adopt the static-first Bengal theme on your own site
- [[/docs/components/|Components]] — Browse layout, UI, forms, and streaming components
- [[/docs/theming/|Theming]] — Customize with CSS variables
- [[/docs/app-shell/|App Shell]] — Build dashboard layouts with sidebar and breadcrumbs
