---
title: chirp-ui
description: Gorgeous Chirp components — htmx-native, Kida macros, Alpine.js for interactivity
template: home.html
weight: 100
type: page
draft: false
lang: en
keywords: [chirp-ui, components, ui, htmx, kida, chirp, templates, alpine]
category: home

blob_background: true

cta_buttons:
  - text: Get Started
    url: /docs/get-started/
    style: primary
  - text: Components
    url: /docs/components/
    style: secondary

show_recent_posts: false
---

## HTML Over the Wire, Gorgeous by Default

**Kida macros. htmx-native. Alpine.js for interactivity.**

chirp-ui is an optional companion design system for [Chirp](https://lbliii.github.io/chirp). It provides Kida template macros — cards, modals, forms, layouts — that render as HTML. Use them with htmx for swaps, SSE for streaming, and View Transitions for polish. Zero JavaScript for layout.

```html
{% from "chirpui/layout.html" import container, grid, block %}
{% from "chirpui/card.html" import card %}

{% call container() %}
    {% call grid(cols=2) %}
        {% call block() %}{% call card(title="Hello") %}<p>Card one.</p>{% end %}{% end %}
        {% call block() %}{% call card(title="World") %}<p>Card two.</p>{% end %}{% end %}
    {% end %}
{% end %}
```

---

## What's good about it

:::{cards}
:columns: 2
:gap: medium

:::{card} Gorgeous by Default
:icon: palette
Full visual design out of the box. Override `--chirpui-*` CSS variables to customize.
:::{/card}

:::{card} htmx-Native
:icon: zap
Interactive components use htmx or native HTML. Dropdown, modal, tray, tabs use Alpine.js for declarative behavior.
:::{/card}

:::{card} Composable
:icon: layers
`{% slot %}` for content injection. Components nest freely. No wrapper classes.
:::{/card}

:::{card} Modern CSS
:icon: code
`:has()`, container queries, fluid typography, `prefers-color-scheme` dark mode.
:::{/card}

:::{/cards}

---

## Quick Install

```bash
pip install chirp-ui
# or
uv add chirp-ui
```

Requires Python 3.14+. When used with Chirp, components are auto-detected — no configuration needed.

---

## The Bengal Ecosystem

A structured reactive stack — every layer written in pure Python for 3.14t free-threading.

| | | | |
|--:|---|---|---|
| **ᓚᘏᗢ** | [Bengal](https://lbliii.github.io/bengal/) | Static site generator | [Docs](https://lbliii.github.io/bengal/) |
| **∿∿** | [Purr](https://github.com/lbliii/purr) | Content runtime | — |
| **⌁⌁** | [Chirp](https://lbliii.github.io/chirp/) | Web framework | [Docs](https://lbliii.github.io/chirp/) |
| **ʘ** | **chirp-ui** | Component library ← You are here | [Docs](/docs/) |
| **=^..^=** | [Pounce](https://lbliii.github.io/pounce/) | ASGI server | [Docs](https://lbliii.github.io/pounce/) |
| **)彡** | [Kida](https://lbliii.github.io/kida/) | Template engine | [Docs](https://lbliii.github.io/kida/) |
| **ฅᨐฅ** | [Patitas](https://lbliii.github.io/patitas/) | Markdown parser | [Docs](https://lbliii.github.io/patitas/) |
| **⌾⌾⌾** | [Rosettes](https://lbliii.github.io/rosettes/) | Syntax highlighter | [Docs](https://lbliii.github.io/rosettes/) |

Python-native. Free-threading ready. No npm required.
