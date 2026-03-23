---
title: ASCII kit
description: Retro ASCII UI primitives and backgrounds
draft: false
weight: 25
lang: en
type: doc
keywords: [chirp-ui, ascii, retro]
icon: terminal
---

# ASCII kit

Templates named `ascii_*.html` plus `ascii_split_flap.html`, `ascii_breaker_panel.html` provide **retro terminal** aesthetics: borders, dividers, progress, tables, toggles, radios, steppers, tickers, VU meters, 7-segment displays, and more.

## Variants

ASCII blocks have extensive `VARIANT_REGISTRY` entries (`ascii-border`, `ascii-divider`, `ascii-table`, …). Use `validate_variant_block` when passing dynamic variant strings.

## Composition

Pair ASCII components with [Effects](./effects.md) (`scanline`, `grain`) for cohesive retro scenes.

## Related

- [Typography effects](./typography-effects.md)
