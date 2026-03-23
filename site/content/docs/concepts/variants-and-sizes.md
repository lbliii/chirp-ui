---
title: Variants and sizes
description: VARIANT_REGISTRY, SIZE_REGISTRY, and strict mode
draft: false
weight: 40
lang: en
type: doc
keywords: [chirp-ui, variants, validation, strict]
icon: sliders-horizontal
---

# Variants and sizes

Many components accept **variant** and **size** parameters. Allowed values are centralized in registries so templates stay consistent and typos fail loudly in development.

## Registries

- **`VARIANT_REGISTRY`** — maps BEM **block** names to allowed variant strings (e.g. `btn`, `alert`, `ascii-border`).
- **`SIZE_REGISTRY`** — maps blocks to allowed sizes where applicable (e.g. `btn`, `modal`, `icon-btn`).

Use filters in templates:

- `validate_variant_block(variant, "btn")` — look up allowed variants for that block.
- `validate_size(size, "btn")` — validate size for that block.

Full tables: [Validation reference](../reference/validation.md).

## Strict mode

`set_strict(True)` enables warnings (and fallbacks to defaults) when a variant or size is unknown. With Chirp, `use_chirp_ui(app)` can align strict mode with `app.debug`.

## Custom variants

If you need values outside the registry for a one-off, prefer **extra classes** via `cls` / `html_attrs` rather than silently passing invalid variant names — or extend the registry in a fork for long-lived design tokens.
