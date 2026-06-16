---
title: Chirp UI Team — Profile
description: A structured, data-driven resume rendered from YAML with chirp-ui components.
draft: false
weight: 10
lang: en
template: resume/single.html
keywords: [chirp-ui, resume, profile, components, data-driven]
resume:
  name: Chirp UI Team
  headline: Server-first UI components for Python web apps
  location: Built in the open
  social:
    github: lbliii/chirp-ui
    website: https://lbliii.github.io/chirp-ui/
  summary: >-
    We design and maintain chirp-ui — a component library for Python web apps
    that renders semantic HTML on the server and enhances it with htmx and
    Alpine only where a screen needs interactivity. A Python vocabulary for UI,
    not a string vocabulary: render first, enhance second.
  metrics:
    - value: "100+"
      label: Kida macros
      icon: stack
    - value: "6"
      label: Layout primitives
      icon: cube
    - value: "0"
      label: Build steps
      icon: zap
  experience:
    - role: Component Library
      org: chirp-ui
      start: "2023"
      end: Present
      location: Open source
      summary: >-
        100+ Kida macros for layout, forms, navigation, overlays, and data
        display, validated against a variant/size registry.
      highlights:
        - Registry-driven vocabulary projected to macros, CSS, docs, and a manifest agents can inspect
        - Composition primitives (stack, cluster, grid, frame, block) instead of a utility-class string vocabulary
        - Escape-by-default rendering with html_attrs / attrs_map trust boundaries
        - Cascade-layer public API so apps override without specificity tricks
      tech:
        - Python 3.14
        - Kida
        - htmx
        - Alpine.js
        - CSS @layer
    - role: chirp-theme
      org: Bengal documentation theme
      start: "2023"
      end: Present
      location: Open source
      summary: The documentation theme that ships with chirp-ui, used to build this very site.
      highlights:
        - Token-parity theme package built on chirp-ui components, not a private CSS fork
        - App shell, marketing kit, and docs chrome assembled from registry macros
      tech:
        - Bengal
        - Kida
        - chirp-ui
    - role: Patterns & recipes
      org: chirp-ui
      start: "2022"
      end: Present
      summary: >-
        Recipes for app shells, marketing pages, and fragment-swap islands that
        stay legible without a client framework.
      highlights:
        - Server-driven data grid with typed sort/selection state
        - Mobile nav drawer, suspense slots, and OOB composition helpers
  projects:
    - name: Server-driven data grid
      role: Composite + typed helper
      date: "2024"
      summary: Sortable, selectable grid rendered from a Chirp-agnostic Python state helper.
      highlights:
        - aria-sort projected from server state so headers can't drift from ORDER BY
        - Page-scoped select-all with htmx load-more and re-seeded selection
      tech:
        - Python
        - htmx
        - Alpine.js
    - name: Component manifest
      role: Agent grounding
      date: "2024"
      url: https://lbliii.github.io/chirp-ui/
      summary: A machine-readable manifest so coding agents cite components instead of guessing class strings.
      highlights:
        - Deterministic, schema-versioned output built from the registry
      tech:
        - Python
        - JSON Schema
  skills:
    - category: Languages & runtime
      items:
        - Python 3.14
        - Free-threading
        - HTML
        - CSS
    - category: Rendering
      items:
        - Kida templates
        - Jinja-like macros
        - BEM
        - "@scope / @layer"
    - category: Interactivity
      items:
        - htmx
        - Alpine.js
        - SSE
        - Progressive enhancement
    - category: Tooling
      items:
        - uv
        - pytest
        - Playwright
        - ruff
  education:
    - degree: Design principles
      institution: Render first, enhance second
      start: "2022"
      end: Present
      highlights:
        - Make the common screen consistent so docs and product never drift apart
        - Prefer composition and tokens over bespoke CSS
  languages:
    - language: Python
      proficiency: Native
    - language: HTML / CSS
      proficiency: Fluent
    - language: htmx
      proficiency: Conversational
---

This profile is generated entirely from the `resume:` block in its YAML
front-matter — edit the data, not the markup, to update the resume.
