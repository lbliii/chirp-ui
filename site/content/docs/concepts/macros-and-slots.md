---
title: Macros and slots
description: Kida {% def %}, {% call %}, and {% slot %} patterns in chirp-ui
draft: false
weight: 30
lang: en
type: doc
keywords: [chirp-ui, kida, macros, slots]
icon: code
---

# Macros and slots

chirp-ui templates use **Kida** (`kida-templates`). Components are defined with `{% def name(...) %}` and composed with `{% call %}` and `{% slot %}`.

## Import and call

```text
{% from "chirpui/card.html" import card %}

{% call card(title="Hello") %}
  {% slot "body" %}
    <p>Card content.</p>
  {% endslot %}
{% end %}
```

Slot names and defaults vary per component — see each [component category](../components/) page.

## No scripts in macros

Do not embed `<script>` tags inside component templates. Interactivity uses **Alpine.js** `x-data` attributes where needed; Chirp is the single place that injects Alpine when enabled.

## `| safe`

Only mark output `| safe` when it is already escaped (e.g. from `html_attrs`) or trusted markup. See [Security](../guides/security.md).

## Composition

Prefer **small components** composed in the view rather than mega-templates. For HTMX, return fragments that reuse the same macros so full page and partial stay in sync.

Further reading: [Composition](https://github.com/lbliii/chirp-ui/blob/main/docs/COMPOSITION.md) in the repository.
