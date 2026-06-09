---
title: "Step 1 — Render your first component"
description: Install chirp-ui and render a card from a Kida template.
draft: false
weight: 10
lang: en
keywords: [chirp-ui, install, card, kida, first component]
---

## Install the library

chirp-ui works standalone or alongside Chirp. For a quick start:

```bash
pip install chirp-ui
# or, with the Chirp web framework
pip install "bengal-chirp[ui]"
```

## Render a card

In any Kida template, import a macro and call it. No build step, no client
bundle — the macro emits plain HTML:

```jinja
{% from "chirpui/card.html" import card %}

{% call card(title="Welcome") %}
  <p>This is server-rendered HTML, styled by chirp-ui.</p>
{% end %}
```

Load the page and you have a styled card on first paint. Nothing hydrates;
nothing waits on JavaScript. When this renders, move on to wiring an
interaction in the next step.
