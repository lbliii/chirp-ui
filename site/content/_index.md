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
  - text: Component showcase
    url: /showcase/
    style: secondary
  - text: Components
    url: /docs/components/
    style: secondary

features:
  - title: Component Library
    href: /docs/components/
    description: Explore Chirp UI macros for forms, cards, navigation, overlays, marketing pages, and application chrome.
  - title: Site Patterns
    href: /docs/patterns/
    description: Translate product, media, forum, and documentation ideas into composable Chirp UI primitives.
  - title: Release Notes
    href: /releases/
    description: Track shipped contracts, migration notes, and the latest Bengal theme adoption work.

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

<div class="chirpui-grid chirpui-grid--cols-2 chirpui-grid--gap-md chirp-theme-directive-cards">
  <article class="chirpui-card chirp-theme-directive-card">
    <header class="chirpui-card__header">
      <div class="chirpui-card__header-content">
        <span class="chirpui-card__title">Gorgeous by Default</span>
      </div>
    </header>
    <div class="chirpui-card__body">
      <p class="chirpui-text-muted chirpui-font-sm">Full visual design out of the box. Override <code>--chirpui-*</code> CSS variables to customize.</p>
    </div>
  </article>
  <article class="chirpui-card chirp-theme-directive-card">
    <header class="chirpui-card__header">
      <div class="chirpui-card__header-content">
        <span class="chirpui-card__title">htmx-Native</span>
      </div>
    </header>
    <div class="chirpui-card__body">
      <p class="chirpui-text-muted chirpui-font-sm">Interactive components use htmx or native HTML. Dropdown, modal, tray, tabs use Alpine.js for declarative behavior.</p>
    </div>
  </article>
  <article class="chirpui-card chirp-theme-directive-card">
    <header class="chirpui-card__header">
      <div class="chirpui-card__header-content">
        <span class="chirpui-card__title">Composable</span>
      </div>
    </header>
    <div class="chirpui-card__body">
      <p class="chirpui-text-muted chirpui-font-sm"><code>&#123;% slot %&#125;</code> for content injection. Components nest freely. No wrapper classes.</p>
    </div>
  </article>
  <article class="chirpui-card chirp-theme-directive-card">
    <header class="chirpui-card__header">
      <div class="chirpui-card__header-content">
        <span class="chirpui-card__title">Modern CSS</span>
      </div>
    </header>
    <div class="chirpui-card__body">
      <p class="chirpui-text-muted chirpui-font-sm"><code>:has()</code>, container queries, fluid typography, <code>prefers-color-scheme</code> dark mode.</p>
    </div>
  </article>
</div>

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
