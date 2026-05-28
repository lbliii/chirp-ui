---
title: HTML UI for Python apps
description: Reusable components for Python projects that render plain HTML and enhance with htmx or Alpine when needed.
template: home.html
weight: 100
type: page
draft: false
lang: en
keywords: [chirp-ui, components, ui, htmx, kida, chirp, templates, alpine, marketing pages]
category: home

blob_background: false

hero_eyebrow: chirp-ui
hero_summary: Build forms, navigation, docs, and app shells from Python templates that render plain HTML.
hero_points:
  - Server-rendered HTML
  - Optional htmx and Alpine

cta_buttons:
  - text: Start building
    url: /docs/get-started/
    style: primary
  - text: Browse components
    url: /docs/components/
    style: secondary

hero_preview:
  eyebrow: Example interface
  title: Common app screens, ready to render.
  summary: Use ready-made UI for common screens, then customize the rendered HTML and CSS for your app.
  nav_items: [Overview, Docs, Settings]
  proof_items: [Forms, Navigation, Content]
  feature_title: Account settings
  feature_text: Labels, inputs, validation messages, and actions render as normal HTML.
  cta_text: Open the docs
  cta_url: /docs/
  resource_text: API reference

proof_metrics:
  - value: 100+
    label: components and patterns
    hint: Forms, cards, nav, overlays, and shell UI.
  - value: 0
    label: utility classes
    hint: Compose with components, not class strings.
  - value: HTML
    label: by default
    hint: Add htmx or Alpine only where interaction needs it.

marketing_shapes:
  - eyebrow: Pages
    title: Product and documentation pages
    description: Start with page sections for headings, feature blocks, proof points, resource cards, and calls to action.
    href: /docs/patterns/product-pages/
    layout: hero
  - eyebrow: Apps
    title: Application screens
    description: Use forms, drawers, navigation, modals, tabs, and command surfaces for everyday product UI.
    href: /docs/components/
    layout: feature
  - eyebrow: Data
    title: Status and summary views
    description: Show counters, badges, tables, timelines, and resource lists without designing each screen from scratch.
    href: /showcase/
    layout: proof
  - eyebrow: Docs
    title: Guides and reference surfaces
    description: Build catalog pages, release lists, API references, and long-form documentation with consistent navigation.
    href: /docs/
    layout: links
  - eyebrow: CTA
    title: Next-step sections
    description: Give people a clear path to install, read, browse, or open a working example.
    href: /docs/app-shell/
    layout: cta

feature_sections:
  - eyebrow: Server-rendered pages
    title: Use components where you already render HTML
    description: Chirp UI fits static sites, docs, and Python web apps that return HTML first. Add interaction only where the screen needs it.
    label: Page patterns
    href: /docs/patterns/product-pages/
    reverse: false
    visual_title: Page kit
    visual_items:
      - Hero and section headers
      - Feature and resource cards
      - Metrics and calls to action
  - eyebrow: App interfaces
    title: Keep common product screens consistent
    description: Forms, navigation, overlays, and app-shell layouts use the same component library, so docs and product screens do not drift apart.
    label: App shell guide
    href: /docs/app-shell/
    reverse: true
    visual_title: App kit
    visual_items:
      - Forms and validation
      - Sidebar and page map
      - Command palette

ecosystem_logos:
  - name: Bengal
    href: https://lbliii.github.io/bengal/
    external: true
  - name: Chirp
    href: https://lbliii.github.io/chirp/
    external: true
  - name: Kida
    href: https://lbliii.github.io/kida/
    external: true
  - name: Pounce
    href: https://lbliii.github.io/pounce/
    external: true
  - name: Patitas
    href: https://lbliii.github.io/patitas/
    external: true
  - name: Rosettes
    href: https://lbliii.github.io/rosettes/
    external: true

quick_links:
  - title: Component library
    href: /docs/components/
    description: Browse reusable UI for layout, forms, navigation, overlays, and data display.
  - title: Pattern recipes
    href: /docs/patterns/
    description: See how components combine into product, media, forum, and workspace screens.
  - title: Release notes
    href: /releases/
    description: Track shipped changes and migration notes.

final_cta:
  title: Start with a working component, then adapt it.
  description: Install Chirp UI, render a component from Python, and layer in htmx or Alpine only when a screen needs client-side behavior.
  primary_text: Get started
  primary_url: /docs/get-started/
  secondary_text: Open the API reference
  secondary_url: /api/

show_recent_posts: false
---
