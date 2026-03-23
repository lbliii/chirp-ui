---
title: Concepts
description: Design philosophy, BEM naming, Kida macros, variants, and Alpine integration
draft: false
weight: 5
lang: en
type: doc
keywords: [chirp-ui, concepts, bem, kida, variants]
category: concepts
---

# Concepts

Understand how chirp-ui is structured before you dive into components and guides.

:::{cards}
:columns: 2
:gap: medium

:::{card} Design philosophy
:icon: lightbulb
:link: ./design-philosophy.md
HTML over the wire, companion to Chirp, composable macros.
:::{/card}

:::{card} BEM naming
:icon: tag
:link: ./bem-naming.md
`chirpui-*` blocks, modifiers, and element classes.
:::{/card}

:::{card} Macros and slots
:icon: code
:link: ./macros-and-slots.md
`{% def %}`, `{% call %}`, and `{% slot %}` patterns.
:::{/card}

:::{card} Variants and sizes
:icon: sliders-horizontal
:link: ./variants-and-sizes.md
Registries, validation, and strict mode.
:::{/card}

:::{card} Alpine integration
:icon: lightning
:link: ./alpine-integration.md
Events, magics, and how Chirp injects Alpine.
:::{/card}

:::{/cards}

---

## Related

- [About](../about/_index.md) — architecture and Chirp integration
- [Reference](../reference/_index.md) — filters and validation APIs
- [Guides](../guides/_index.md) — layout, HTMX, and pitfalls
