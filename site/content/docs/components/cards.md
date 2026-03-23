---
title: Cards
description: card, glow_card, spotlight_card, index_card, config_card
draft: false
weight: 12
lang: en
type: doc
keywords: [chirp-ui, card, surface]
icon: cards
---

# Cards

Surface chrome for grouped content. Templates live under `chirpui/card.html`, `chirpui/glow_card.html`, `chirpui/spotlight_card.html`, `chirpui/index_card.html`, `chirpui/config_card.html`.

## When to use

- **`card`** — default dashboard / list item surface
- **`glow_card`**, **`spotlight_card`** — emphasis and marketing-style highlights
- **`index_card`** — directory / hub navigation tiles
- **`config_card`** — settings panels with structured rows

## Variants and sizes

`glow_card` and `spotlight_card` participate in `VARIANT_REGISTRY` / `SIZE_REGISTRY` (e.g. `glow-card`, `spotlight-card`, `border-beam`). Use `validate_variant_block` / `validate_size` in templates.

## Composition

Cards accept body slots for titles, actions, and footers depending on the macro. Nest `stack()` or `cluster()` inside for internal layout.

## CSS

Roots include `chirpui-card`, `chirpui-glow-card`, `chirpui-spotlight-card`, `chirpui-index-card`, `chirpui-config-card`.

## Related

- [Layout](./layout.md) — `grid()` + `block()` for card grids
- [Theming](../theming/design-tokens.md) — elevation and surfaces
