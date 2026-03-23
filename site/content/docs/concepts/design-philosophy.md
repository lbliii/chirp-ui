---
title: Design philosophy
description: HTML over the wire, companion layer, and composable components
draft: false
weight: 10
lang: en
type: doc
keywords: [chirp-ui, philosophy, htmx, kida]
icon: lightbulb
---

# Design philosophy

chirp-ui is an **optional companion** to [Chirp](https://lbliii.github.io/chirp/). It is not the framework itself and not the only way to build UIs with Chirp.

## Core ideas

- **HTML over the wire.** Components render as HTML for htmx swaps, SSE streams, and View Transitions. Prefer server-rendered fragments over client bundles for layout and content.
- **Companion, not core.** You can use Chirp without chirp-ui. chirp-ui adds Kida macros, CSS, and filters — nothing mandatory in the framework.
- **CSS as the design language.** Modern CSS (`:has()`, container queries, `clamp()`, `color-mix()`) powers the default look. Override `--chirpui-*` tokens instead of fighting the cascade.
- **Composable.** Use `{% call %}` and `{% slot %}` to inject content. Nest cards, grids, and forms without wrapper soup.
- **Minimal runtime.** Layout and typography need no JavaScript. Interactive pieces use Alpine.js (injected by Chirp when enabled) for declarative behavior.

## Thread safety

The package is built for **Python 3.14+** and free-threading readiness. Public APIs avoid module-level mutable singletons where it matters; color registration uses context variables.

## Where to go next

- [BEM naming](./bem-naming.md) — class naming rules
- [Macros and slots](./macros-and-slots.md) — template patterns
- [About](../about/) — `use_chirp_ui` and integration
