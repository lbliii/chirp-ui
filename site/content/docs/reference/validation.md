---
title: Validation
description: VARIANT_REGISTRY, SIZE_REGISTRY, and strict mode
draft: false
weight: 47
lang: en
type: doc
keywords: [chirp-ui, validation, variants]
icon: checks
---

# Validation

## Strict mode

`set_strict(True)` causes invalid variant/size values to **log warnings** and fall back to defaults. With Chirp, `use_chirp_ui(app, strict=None)` can mirror **`app.debug`**.

## VARIANT_REGISTRY

Maps **BEM block** names (e.g. `btn`, `alert`, `ascii-border`) to allowed **variant** strings. The canonical source is `chirp_ui/validation.py` in the package — it is long and evolves each release.

**Examples:**

- `btn`: `""`, `default`, `primary`, `ghost`, `danger`, `success`, `warning`
- `alert`: `info`, `success`, `warning`, `error`
- `surface`: `default`, `muted`, `elevated`, `accent`, `glass`, …

Use **`validate_variant_block`** in templates when passing dynamic variants.

## SIZE_REGISTRY

Maps blocks to allowed **sizes** where applicable:

- `btn`: `""`, `sm`, `md`, `lg`
- `modal`: `small`, `medium`, `large`
- `icon-btn`, `orbit`, `sparkle`, … — see source.

## Extending

Library authors can fork **`validation.py`** or wrap components with fixed variant strings in app templates. Prefer **tokens + cls** over unlisted variants unless you maintain a fork.

## Related

- [Filters](./filters.md)
- [Concepts: Variants](../concepts/variants-and-sizes.md)
