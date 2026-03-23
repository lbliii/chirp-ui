---
title: Standalone usage
description: Use chirp-ui with Kida without a Chirp App
draft: false
weight: 25
lang: en
type: doc
keywords: [chirp-ui, kida, standalone]
icon: package
---

# Standalone usage

chirp-ui only requires **Kida** for templates. You can render macros outside Chirp if you:

1. Add **`chirp_ui`** templates to the Kida environment loader (e.g. `PackageLoader` / combined loader).
2. Register filters manually if your host exposes a compatible **`template_filter`** API — or stub filters in tests (see `chirp-ui` **`tests/conftest.py`**).
3. Serve **`chirpui.css`** and **`chirpui.js`** from **`static_path()`** or your asset pipeline.

## Tests without Chirp

The chirp-ui test suite uses a fixture that stubs Chirp-provided filters so components render without a full app.

## Limitations

- **`tab_is_active`** and htmx shell integration examples assume Chirp request context.
- Alpine injection is **your responsibility** if you need interactive widgets outside Chirp.

## Related

- [Chirp integration](./chirp-integration.md)
- [Concepts](../concepts/)
