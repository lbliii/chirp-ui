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
print(chirp_ui.__version__)  # e.g. "0.2.2"
```

## Next Steps

- [Components](/docs/components/) — Browse layout, UI, forms, and streaming components
- [Theming](/docs/theming/) — Customize with CSS variables
- [App Shell](/docs/app-shell/) — Build dashboard layouts with sidebar and breadcrumbs
