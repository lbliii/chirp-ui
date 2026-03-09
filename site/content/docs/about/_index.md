---
title: About
description: Architecture, Chirp integration, and design philosophy
draft: false
weight: 50
lang: en
type: doc
keywords: [chirp-ui, about, architecture, chirp]
category: about
---

# About chirp-ui

chirp-ui is an optional companion design system for [Chirp](https://lbliii.github.io/chirp). It is not the framework itself and not the only way to use Chirp.

## Key Ideas

- **HTML over the wire.** Components render as blocks for htmx swaps, SSE streams, and View Transitions.
- **Companion, not core.** chirp-ui is an optional layer on top of Chirp.
- **CSS as the design language.** Modern features (`:has()`, `aspect-ratio`, `clamp()`) used where they add value.
- **Composable.** `{% slot %}` for content injection. Components nest freely.
- **Minimal dependency.** `kida-templates` only. Chirp optional for auto-registration.

## Chirp Integration

When chirp-ui is installed with Chirp, use `use_chirp_ui(app)` to wire static assets and filters:

```python
from chirp import App, AppConfig, use_chirp_ui

app = App(AppConfig(template_dir="templates"))
use_chirp_ui(app)
```

Templates resolve `chirpui/layout.html`, `chirpui/card.html`, etc. from the package automatically.
