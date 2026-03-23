---
title: First component
description: Render a card with Kida in a few minutes
draft: false
weight: 15
lang: en
type: doc
keywords: [chirp-ui, quickstart, card]
icon: rocket
---

# First component

After [Installation](./installation.md), add a template that imports chirp-ui macros.

## 1. Template

Create `templates/hello.html`:

```html
{% from "chirpui/layout.html" import container, grid, block %}
{% from "chirpui/card.html" import card %}

{% call container() %}
  {% call grid(cols=2) %}
    {% call block() %}
      {% call card(title="Hello") %}
        {% slot "body" %}<p>Your first chirp-ui card.</p>{% endslot %}
      {% end %}
    {% end %}
    {% call block() %}
      {% call card(title="World") %}
        {% slot "body" %}<p>Add routes and htmx next.</p>{% endslot %}
      {% end %}
    {% end %}
  {% end %}
{% end %}
```

Slot names match the card macro in your installed version — adjust if the API differs slightly.

## 2. Wire the view

Point a Chirp route at this template (or render it from a test `App`). Ensure **`use_chirp_ui(app)`** ran at startup so loaders resolve **`chirpui/*`** — see [Chirp integration](./chirp-integration.md).

## 3. CSS

Include **`chirpui.css`** (Chirp static pipeline) or load from **`chirp_ui.static_path()`** for standalone setups.

## Next

- [Components: Cards](../components/cards.md)
- [Theming](../theming/)
