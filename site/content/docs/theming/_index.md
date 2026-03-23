---
title: Theming
description: Tokens, typography, color, motion, and custom themes
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, theming, css, tokens]
category: theming
---

# Theming

chirp-ui is driven by **`--chirpui-*` CSS variables** and optional `data-theme` / `data-style` attributes. Override tokens instead of forking component CSS when possible.

:::{cards}
:columns: 2
:gap: medium

:::{card} Design tokens
:icon: sliders
:link: ./design-tokens.md
Spacing, elevation, state, motion tiers.
:::{/card}

:::{card} Typography
:icon: text-t
:link: ./typography.md
UI vs prose scales, weights, utilities.
:::{/card}

:::{card} Color system
:icon: palette
:link: ./color-system.md
Palettes, `resolve_color`, `register_colors`, contrast.
:::{/card}

:::{card} Motion and transitions
:icon: wave-sine
:link: ./motion-and-transitions.md
HTMX swaps, view transitions, motion tokens.
:::{/card}

:::{card} Creating themes
:icon: paint-brush
:link: ./creating-themes.md
`data-theme`, `data-style`, holy-light example.
:::{/card}

:::{/cards}

## Quick reference

- **`chirpui.js`** sets `data-theme` and `data-style` from `localStorage` before paint.
- Optional **`themes/holy-light.css`** demonstrates a dark token layer.

See also [Concepts](../concepts/design-philosophy.md).
