---
title: Patterns
description: Composition recipes for navigation, product, media, and community surfaces
draft: false
weight: 45
lang: en
type: doc
keywords: [chirp-ui, patterns, navigation, product pages, media sites, forums]
category: patterns

cascade:
  type: doc
---

Chirp UI patterns are recipes for composing registry-backed macros into real
pages. Start here when a page feels bigger than one component but does not yet
justify a new public macro.

## Pattern Families

:::{cards}
:columns: 2
:gap: medium

:::{card} Navigation
:icon: sidebar
:link: ./navigation/
Choose between global shell navigation, object context, route tabs, command
launchers, sidebars, and page-local tools.
:::{/card}

:::{card} Product Pages
:icon: rocket
:link: ./product-pages/
Build product, marketing, proof, lifecycle, story, and CTA pages from stable
composition primitives.
:::{/card}

:::{card} Media Sites
:icon: monitor
:link: ./media-sites/
Compose acquisition, catalog, title detail, watch-side, live event, profile, and
plan comparison surfaces.
:::{/card}

:::{card} Forums
:icon: users
:link: ./forums/
Compose community, topic list, thread, Q&A, moderation, and activity surfaces
without adding forum-specific API too early.
:::{/card}

:::{/cards}

The component registry is still the source of truth. Promote a recipe into a
component only after repeated real pages prove that the shape is stable.
