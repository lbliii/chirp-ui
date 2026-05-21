---
title: Patterns
description: Composition recipes for navigation, search, product, media, and community surfaces
draft: false
weight: 45
lang: en
type: doc
keywords: [chirp-ui, patterns, navigation, search shells, product pages, media sites, forums]
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

:::{card} Search Shells
:icon: search
:link: ./search-shells/
Build dense catalog, reference, and object-library search surfaces with scoped
counts, facets, HTMX updates, and responsive command surfaces.
:::{/card}

:::{card} Workspace Shells
:icon: panels-top-left
:link: ./workspace-shells/
Build dense search, operations, support, and admin workspaces with shell,
rail, result, metric, and inspector primitives.
:::{/card}

:::{card} Layout Affinity
:icon: layout-template
:link: ./layout-affinity/
Describe parent-scoped layout intent for dense responsive recipes without
adding utility classes or premature public manifest fields.
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
