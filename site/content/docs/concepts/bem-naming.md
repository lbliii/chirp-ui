---
title: BEM naming
description: chirpui-* blocks, elements, and modifiers
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, bem, css, classes]
icon: tag
---

# BEM naming

chirp-ui follows **BEM-style** naming so classes stay predictable in templates and in custom CSS.

## Pattern

- **Block:** `chirpui-<block>` — e.g. `chirpui-card`, `chirpui-btn`
- **Element:** `chirpui-<block>__<element>` — e.g. `chirpui-card__title`
- **Modifier:** `chirpui-<block>--<modifier>` — e.g. `chirpui-btn--primary`, `chirpui-modal--large`

Some components use a single root class with child elements; others expose multiple modifiers for variants and sizes.

## `bem` filter

Use the `bem` filter in templates to build class strings safely:

```text
{{ "card" | bem(variant="primary") }}
```

Produces roots like `chirpui-card chirpui-card--primary` (exact output depends on block and args).

See [Filters](../reference/filters.md) for the full `bem` signature.

## Validation blocks

`VARIANT_REGISTRY` and `SIZE_REGISTRY` keys use **block** names (often with `__` for nested pieces, e.g. `dropdown__item`). See [Validation](../reference/validation.md).

## CSS contract

Every `chirpui-*` class referenced in templates should exist in `chirpui.css`. The project tests enforce this — see [CSS class index](../reference/css-class-index.md).
