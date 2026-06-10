---
title: Reference
description: The chirp-theme authoring vocabulary — shortcodes and directives, with parameters and rendered examples
draft: false
weight: 35
lang: en
type: doc
keywords: [chirp-theme, reference, shortcodes, directives, admonition, component_specimen, figure, gallery, ref, relref, param]
category: reference

cascade:
  type: doc
---

The chirp-theme ships a small authoring vocabulary on top of Markdown: inline
**shortcodes** (`{{</* name */>}}`) for media, callouts, and live component
specimens, and block **directives** (`:::{name}`) for admonitions and card
grids. Everything here renders with Chirp UI markup, so authored content matches
the rest of the site.

You do not need to leave this site to learn the vocabulary — every shortcode and
directive below has its parameters and a rendered example on the page.

## In this section

:::{cards}
:columns: 2
:gap: medium

:::{card} Shortcodes
:icon: code
:link: /docs/reference/shortcodes/
Inline `{{</* name */>}}` helpers — `component_specimen`, the `tip` /
`warning` / `danger` callout family, `figure` / `gallery` / `img` / `audio`
media, `details`, `highlight`, `blockquote`, and the `ref` / `relref` / `param`
link helpers.
:::{/card}

:::{card} Directives
:icon: layers
:link: /docs/reference/directives/
Block `:::{name}` containers — `admonition` for the full semantic callout
family, plus `card`, `cards`, and `child_cards` for card grids that mirror the
component vocabulary.
:::{/card}

:::{/cards}

## When to reach for what

| You want to… | Use |
|--------------|-----|
| Show a live, rendered Chirp UI component inside prose | `{{</* component_specimen */>}}` shortcode |
| Call out a tip, warning, or danger inline | `{{</* tip */>}}` / `{{</* warning */>}}` / `{{</* danger */>}}` shortcodes |
| Author any semantic admonition (note, hint, caution, …) as a block | `:::{admonition}` directive |
| Embed an image with a caption | `{{</* figure */>}}` shortcode |
| Lay out several images in a grid | `{{</* gallery */>}}` wrapping `{{</* img */>}}` |
| Link to another page by source path (resolved at build) | `{{</* ref */>}}` / `{{</* relref */>}}` shortcodes |
| Echo a config or front-matter value into prose | `{{</* param */>}}` shortcode |
| Group several linked cards | `:::{cards}` + `:::{card}` directives |

Looking for the components themselves? Browse the
[component catalog](/docs/components/) for every public macro with options and
live examples.
