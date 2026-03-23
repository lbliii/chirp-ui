---
title: Chirp integration
description: use_chirp_ui, filters, and static assets
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, chirp, use_chirp_ui]
icon: plug
---

# Chirp integration

## `use_chirp_ui`

From **Chirp** (not `chirp_ui`):

```python
from chirp import App, AppConfig, use_chirp_ui

app = App(AppConfig(template_dir="templates"))
use_chirp_ui(app)
```

This typically:

- Registers **template filters** from chirp-ui (`bem`, `html_attrs`, …).
- Registers **`tab_is_active`** as a template global when supported.
- Wires **static files** for `chirpui.css`, `chirpui.js`, and optional themes.
- Enables **Alpine** by default for interactive components.

Options (prefix, strict, etc.) depend on your Chirp version — see Chirp docs.

## Manual registration

If you cannot use `use_chirp_ui`:

```python
import chirp_ui

chirp_ui.register_filters(app)
```

Call **before** any template render.

## Static path

```python
from chirp_ui import static_path

# Mount or copy files from static_path() for self-hosted assets.
```

## Loaders

Templates import **`chirpui/...`** paths; the package loader must include chirp-ui’s template directory — `use_chirp_ui` handles this for Chirp apps.

## Related

- [Standalone usage](./standalone-usage.md)
- [About](../about/)
