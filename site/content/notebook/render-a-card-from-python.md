---
title: "Render a card from Python"
description: A short executable note showing how a chirp-ui macro renders to HTML.
draft: false
weight: 10
lang: en
date: 2026-04-02
template: notebook/single.html
tags: [notebook, examples]
keywords: [chirp-ui, notebook, jupyter, card, kida]
notebook:
  cell_count: 3
  kernel_name: python3
  language_version: "Python 3.14"
---

## Set up the environment

We import the Kida environment and the chirp-ui loader so macros resolve from
the packaged templates.

```python
from kida import Environment
from chirp_ui import get_loader, register_filters

env = Environment(loader=get_loader())
register_filters(env)
```

## Render a card

Calling the `card` macro returns plain HTML — no build step, no client bundle.

```python
template = env.from_string(
    '{% from "chirpui/card.html" import card %}'
    '{% call card(title="Welcome") %}<p>Server-rendered.</p>{% end %}'
)
print(template.render())
```

```text
<article class="chirpui-card">
  <header class="chirpui-card__header">
    <span class="chirpui-card__title">Welcome</span>
  </header>
  <div class="chirpui-card__body"><p>Server-rendered.</p></div>
</article>
```

## Why this matters

The same macro renders identically inside a notebook, a Bengal page, or a Chirp
route. The notebook layout above summarizes the kernel and language in a metric
grid, then renders this body — a stand-in until Bengal exposes structured
`params.notebook.cells` for a per-cell code/output/exec-count renderer.
