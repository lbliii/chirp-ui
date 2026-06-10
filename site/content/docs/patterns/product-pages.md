---
title: Product Page Patterns
description: Product, marketing, proof, lifecycle, story, and CTA composition recipes
draft: false
weight: 20
lang: en
type: doc
keywords: [chirp-ui, product pages, marketing, cta, logo cloud, story card]
tags: [patterns, marketing, cta]
category: patterns
---

Product pages should be composed from named primitives and registry-backed
components, not page-specific utility classes.

Use the canonical repository guide for the full recipe set:
[`docs/patterns/product-page-patterns.md`](https://github.com/lbliii/chirp-ui/blob/main/docs/patterns/product-page-patterns.md?plain=1).

## Use This When

- A product needs a first-viewport claim and clear primary action.
- Proof should appear near the hero before deep feature copy.
- A page explains product lifecycle jobs such as build, observe, evaluate, and
  deploy.
- Related products, frameworks, customer stories, or final CTAs need consistent
  structure.

## Blessed Surfaces

- `hero`, `page_hero`, `band`, `container`, `stack`, `cluster`, and `grid`.
- `btn` for calls to action.
- `logo_cloud` for customer, partner, device, integration, or ecosystem proof.
- `lifecycle_showcase` for stable job sequences.
- `index_card` or `resource_index` for product choice surfaces.
- `story_card` for customer outcomes.
- `cta_band` for mid-page and final calls to action.

## Checks

- The H1 names the product or literal offer.
- CTAs use existing button variants.
- Logo images have text alternatives.
- The proof band appears before long feature copy.
- Product choice cards explain decision criteria.
- The CTA band does not hide section chrome inside a nested card.
