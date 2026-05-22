---
title: Search Shell Patterns
description: Dense catalog and reference search shell recipes for Chirp UI pages
draft: false
weight: 15
lang: en
type: doc
keywords: [chirp-ui, search, htmx, catalog, facets, responsive]
category: patterns
---

Search shells combine query controls, suggested searches, facet rails, scoped
counts, and dense result cards. They remain recipe-first until repeated real
applications prove a stable public macro surface.

Use the canonical repository guide for the full contract:
[`docs/SEARCH-SHELL-RECIPES.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/SEARCH-SHELL-RECIPES.md?plain=1).
For HTMX target-boundary guidance, see
[`docs/HTMX-PATTERNS.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/HTMX-PATTERNS.md?plain=1).
For responsive proof expectations, see
[`docs/RESPONSIVE.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/RESPONSIVE.md?plain=1).
For the prototype parent-scoped layout-affinity attributes used by command
surfaces, see [Layout Affinity](../layout-affinity/).

## Source Of Truth

This page is a published bridge. The repository docs remain the contract for
progressive enhancement, scoped count semantics, responsive command surfaces,
facet rails, and browser proof:

- `docs/SEARCH-SHELL-RECIPES.md` owns the recipe contract.
- `docs/HTMX-PATTERNS.md` owns HTMX enhancement and target-boundary rules.
- `docs/RESPONSIVE.md` owns stress-width behavior.
- `docs/DESIGN-layout-affinity.md` owns the prototype parent-scoped layout
  intent vocabulary used by command surfaces.
- `docs/VERIFICATION.md` owns required proof for search shells.
- `docs/plans/done/PLAN-search-shell-contracts.md` owns active not-now promotion
  questions.

Do not add a published-only search-shell API here. New public macros,
parameters, emitted classes, or manifest facts must ship through the registry,
templates, generated CSS, generated component options, examples, and tests.

## Use This When

- A catalog or reference page needs search plus layered facets.
- Counts need to explain what is visible in the current query and scope.
- A dense result grid must stay readable across phone, tablet, and desktop.
- HTMX live search should feel responsive while preserving link-native URLs.

## Checks

- The search form works as a native GET form.
- Suggested searches and facet items are real links before HTMX enhancement.
- HTMX requests name target, selected fragment, URL push behavior, request
  coordination, and pending status.
- Counts use user-facing domain nouns and match the current visible scope.
- Primary search controls wrap instead of creating horizontal page overflow.
- Browser proof covers 320px, 390px, 768px, 1024px, and desktop widths before
  recipe promotion.
